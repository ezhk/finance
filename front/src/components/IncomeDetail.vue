<template>
  <div class="category-add">
    <div class="category-add-buttons">
      <h5>Income Detail</h5>
      <button class="btn btn-dark btn-close" @click.prevent="closeBlock">Close</button>
    </div>

    <!-- Edit category block -->
    <h6 class="subheader">Description</h6>
    <form>
      <div class="form-group">
        <input
          type="text"
          class="form-control"
          id="income-detail-name"
          v-model="incomeName"
          placeholder="Name"
          required
        />
      </div>
      <div class="category-add-buttons">
        <button class="btn btn-danger" @click.prevent="deleteIncome">Delete</button>
        <button class="btn btn-secondary" @click.prevent="updateIncome">Update</button>
      </div>
    </form>

    <!-- Incoming transactions block -->
    <div>
      <hr />

      <h6 class="subheader">Transactions</h6>
      <form>
        <div class="form-group">
          <input
            type="number"
            step="0.01"
            class="form-control"
            id="income-detail-transaction-amount"
            v-model="transactionAmount"
            placeholder="Amount"
            required
          />
        </div>
        <select
          class="form-control"
          id="income-detail-transaction-source"
          v-model="transactionDestination"
        >
          <option
            v-for="option in assets"
            :key="option.pk"
            :value="option.pk"
          >{{option.description}}</option>
        </select>
        <div class="category-add-buttons">
          <button class="btn btn-secondary" @click.prevent="createTransaction">Create</button>
        </div>
      </form>

      <table v-show="transactions.length" class="table table-borderless">
        <thead>
          <tr>
            <th></th>
            <th scope="col">Destination</th>
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
            <td style="color: green">&#8592;</td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
</template>

<script>
import methods from "../methods.js";

export default {
  name: "IncomeDetail",
  props: ["incomePk", "assets"],

  data() {
    return {
      incomeName: "",

      transactions: [],
      transactionDestination: null,
      transactionAmount: null,

      getURL: methods.getURL,
      getJSON: methods.getJSON,
      getCookie: methods.getCookie,
      resetInitData: methods.resetInitData
    };
  },

  mounted() {
    this.updateIncomeData();
  },

  methods: {
    showError(error) {
      return this.$parent.$parent.$refs.error.showError(error);
    },

    deleteIncome() {
      const url = this.getURL("detailIncome", this.incomePk);
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

    updateIncome() {
      const url = this.getURL("detailIncome", this.incomePk);
      const csrfToken = this.getCookie("csrftoken");
      const body = JSON.stringify({
        description: this.incomeName
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

    updateIncomeData() {
      this.getDetails();
      this.getTransactions();
    },

    getDetails() {
      this.getJSON(this.getURL("detailIncome", this.incomePk))
        .then(data => {
          this.incomeName = data.description;
        })
        .catch(error => this.showError(error));
    },

    getTransactions() {
      this.getJSON(this.getURL("outgoingIncome", this.incomePk))
        .then(data => {
          this.transactions = data;
        })
        .catch(error => this.showError(error));
    },

    createTransaction() {
      const url = this.getURL("createIncomeTransaction");
      const csrfToken = this.getCookie("csrftoken");
      const body = JSON.stringify({
        income: { pk: this.incomePk },
        asset: { pk: this.transactionDestination },
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

          this.transactionAmount = null;
          this.updateIncomeData();
          this.$parent.getCommonInfo();
        })
        .catch(error => this.showError(error));
    },

    deleteTransaction(transactionID) {
      const url = this.getURL("detailIncomeTransaction", transactionID);
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

          this.updateIncomeData();
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
