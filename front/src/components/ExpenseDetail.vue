<template>
  <div class="category-add">
    <div class="category-add-buttons">
      <h5>Expense Detail</h5>
      <button class="btn btn-dark btn-close" @click.prevent="closeBlock">Close</button>
    </div>

    <!-- Edit category block -->
    <h6 class="subheader">Description</h6>
    <form>
      <div class="form-group">
        <input
          type="text"
          class="form-control"
          id="expense-detail-name"
          v-model="expenseName"
          placeholder="Name"
          required
        />
      </div>
      <div class="form-group">
        <input
          type="text"
          class="form-control"
          id="expense-detail-monthly-limit"
          v-model="expenseMonthlyLimit"
          placeholder="Monthly limit"
          required
        />
      </div>
      <div class="category-add-buttons">
        <button class="btn btn-danger" @click.prevent="deleteExpense">Delete</button>
        <button class="btn btn-secondary" @click.prevent="updateExpense">Update</button>
      </div>
    </form>

    <!-- Outgoing transactions block -->
    <div>
      <hr />

      <h6 class="subheader">Transactions</h6>
      <form>
        <div class="form-group">
          <input
            type="number"
            step="0.01"
            class="form-control"
            id="expense-detail-outgoing-amount"
            v-model="transactionAmount"
            placeholder="Amount"
            required
          />
        </div>
        <select
          class="form-control"
          id="expense-detail-outgoing-source"
          v-model="transactionSource"
        >
          <option v-for="asset in assets" :key="asset.pk" :value="asset.pk">{{asset.description}}</option>
        </select>
        <div class="category-add-buttons">
          <button
            class="btn btn-secondary"
            @click.prevent="createTransaction"
            :disabled="$v.$invalid"
          >Create</button>
        </div>
      </form>

      <table v-show="transactions.length" class="table table-borderless">
        <thead>
          <tr>
            <th></th>
            <th scope="col">Source</th>
            <th scope="col">Amount</th>
            <th></th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="transaction in transactions" :key="transaction.id">
            <td>
              <button
                class="btn btn-light"
                @click.prevent="deleteTransaction(transaction.id)"
              >&#9850;</button>
            </td>
            <td>{{transaction.asset.description}}</td>
            <td>{{transaction.amount}}</td>
            <td style="color: red">&#8594;</td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
</template>

<script>
import { required, decimal } from "vuelidate/lib/validators";
import methods from "../methods.js";

export default {
  name: "ExpenseDetail",
  props: ["expensePk", "assets"],

  data() {
    return {
      expenseName: "",
      expenseMonthlyLimit: "",

      transactions: [],
      transactionSource: null,
      transactionAmount: null,

      getURL: methods.getURL,
      getJSON: methods.getJSON,
      getCookie: methods.getCookie,
      resetInitData: methods.resetInitData
    };
  },

  mounted() {
    this.updateExpenseData();
  },

  validations: {
    transactionSource: { required },
    transactionAmount: { required, decimal }
  },

  methods: {
    showError(error) {
      return this.$parent.$parent.$refs.error.showError(error);
    },

    deleteExpense() {
      const url = this.getURL("detailExpense", this.expensePk);
      const csrfToken = this.getCookie("csrftoken");
      fetch(url, {
        credentials: "include",
        method: "DELETE",
        headers: {
          "Content-Type": "application/json",
          "X-CSRFToken": csrfToken
        }
      })
        .then(response => {
          if (response.status != 204)
            throw `Incorrect status code ${response.status}`;

          this.$parent.refreshData();
          this.$parent.hidePopups();
        })
        .catch(error => this.showError(error));
    },

    updateExpense() {
      const url = this.getURL("detailExpense", this.expensePk);
      const csrfToken = this.getCookie("csrftoken");
      const body = JSON.stringify({
        description: this.expenseName,
        monthly_limit: parseFloat(this.expenseMonthlyLimit)
      });

      fetch(url, {
        credentials: "include",
        body,
        method: "PUT",
        headers: {
          "Content-Type": "application/json",
          "X-CSRFToken": csrfToken
        }
      })
        .then(response => {
          if (response.status != 200)
            throw `Incorrect status code ${response.status}`;

          this.closeBlock();
          this.$parent.refreshData();
        })
        .catch(error => this.showError(error));
    },

    updateExpenseData() {
      this.getDetails();
      this.getTransactions();
    },

    getDetails() {
      this.getJSON(this.getURL("detailExpense", this.expensePk))
        .then(data => {
          this.expenseName = data.description;
          this.expenseMonthlyLimit = data.monthly_limit;
        })
        .catch(error => this.showError(error));
    },

    getTransactions() {
      this.getJSON(this.getURL("incomingExpense", this.expensePk))
        .then(data => {
          this.transactions = data;
        })
        .catch(error => this.showError(error));
    },

    createTransaction() {
      const url = this.getURL("createExpenseTransaction", this.assetPk);
      const csrfToken = this.getCookie("csrftoken");
      const body = JSON.stringify({
        asset: { pk: this.transactionSource },
        expense: { pk: this.expensePk },
        amount: parseFloat(this.transactionAmount)
      });

      fetch(url, {
        credentials: "include",
        body,
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          "X-CSRFToken": csrfToken
        }
      })
        .then(response => {
          if (response.status != 201)
            throw `Incorrect status code ${response.status}`;

          this.inTransactionAmount = null;
          this.updateExpenseData();
          this.$parent.getCommonInfo();
        })
        .catch(error => this.showError(error));
    },

    deleteTransaction(transactionID) {
      const url = this.getURL("detailExpenseTransaction", transactionID);
      const csrfToken = this.getCookie("csrftoken");
      fetch(url, {
        credentials: "include",
        method: "DELETE",
        headers: {
          "Content-Type": "application/json",
          "X-CSRFToken": csrfToken
        }
      })
        .then(response => {
          if (response.status != 204)
            throw `Incorrect status code ${response.status}`;

          this.updateExpenseData();
          this.$parent.getCommonInfo();
        })
        .catch(error => this.showError(error));
    },

    closeBlock() {
      this.$parent.hidePopups();
    }
  }
};
</script>

<style scoped>
.category-add {
  width: 350px;
  position: absolute;
  top: 5%;
  padding: 5px;
  z-index: 1;

  background: white !important;

  border: 1px dashed darkgray;
  border-radius: 5px;

  text-align: center;
  overflow-y: scroll;

  /* max-height: 90%; */
  height: 90%;
}

.category-add-buttons {
  margin: 5px 0 5px 0;
  display: flex;
  justify-content: space-around;
}

.subheader {
  font-size: 1rem;
}

table td {
  padding: 0.5rem !important;
  vertical-align: baseline !important;
}

.btn-close {
  position: fixed;
  bottom: 7%;
  opacity: 0.7;
  width: 150px;
}
</style>
