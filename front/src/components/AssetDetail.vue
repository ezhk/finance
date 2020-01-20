<template>
  <div class="category-add">
    <div class="category-add-buttons">
      <h5>Asset Detail</h5>
      <button class="btn btn-dark btn-close" @click.prevent="closeBlock">Close</button>
    </div>

    <!-- Edit category block -->
    <h6 class="subheader">Description</h6>
    <form>
      <div class="form-group">
        <input
          type="text"
          class="form-control"
          id="asset-detail-name"
          v-model="assetName"
          placeholder="Name"
          required
        />
      </div>
      <div class="form-group">
        <input
          type="number"
          step="0.01"
          class="form-control"
          id="asset-detail-balance"
          v-model="assetBalance"
          placeholder="Balance"
          required
        />
      </div>
      <select class="form-control" id="asset-detail-type" v-model="assetType">
        <option value="CA" selected="selected">Cash</option>
        <option value="BC">Bank card</option>
        <option value="CC">Credit card</option>
      </select>
      <div class="category-add-buttons">
        <button class="btn btn-danger" @click.prevent="deleteAsset">Delete</button>
        <button class="btn btn-secondary" @click.prevent="updateAsset">Update</button>
      </div>
    </form>

    <!-- Incoming transactions block -->
    <div>
      <hr />

      <h6 class="subheader">Incoming transactions</h6>
      <form>
        <div class="form-group">
          <input
            type="number"
            step="0.01"
            class="form-control"
            id="asset-detail-incoming-amount"
            v-model="inTransactionAmount"
            placeholder="Amount"
            required
          />
        </div>
        <select class="form-control" id="asset-detail-incoming-source" v-model="transactionSource">
          <option v-for="inc in incomes" :key="inc.pk" :value="inc.pk">{{inc.description}}</option>
        </select>
        <div class="category-add-buttons">
          <button class="btn btn-secondary" @click.prevent="createIncomeTransaction">Create</button>
        </div>
      </form>

      <table v-show="incomingTransactions.length" class="table table-borderless">
        <thead>
          <tr>
            <th></th>
            <th scope="col">Source</th>
            <th scope="col">Amount</th>
            <th></th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="transaction in incomingTransactions" :key="transaction.id">
            <td>
              <button
                class="btn btn-light"
                @click.prevent="deleteIncomingTransaction(transaction.id)"
              >&#9850;</button>
            </td>
            <td>{{transaction.income.description}}</td>
            <td>{{transaction.amount}}</td>
            <td style="color: green">&#8592;</td>
          </tr>
        </tbody>
      </table>
    </div>

    <!-- Outgoing transactions block -->
    <div>
      <hr />

      <h6 class="subheader">Outgoing transactions</h6>
      <form>
        <div class="form-group">
          <input
            type="number"
            step="0.01"
            class="form-control"
            id="asset-detail-outgoung-amount"
            v-model="outTransactionAmount"
            placeholder="Amount"
            required
          />
        </div>
        <select
          class="form-control"
          id="asset-detail-outgoung-source"
          v-model="transactionDestination"
        >
          <option v-for="exp in expenses" :key="exp.pk" :value="exp.pk">{{exp.description}}</option>
        </select>
        <div class="category-add-buttons">
          <button class="btn btn-secondary" @click.prevent="createOutgoingTransaction">Create</button>
        </div>
      </form>

      <table v-show="outgoingTransactions.length" class="table table-borderless">
        <thead>
          <tr>
            <th></th>
            <th scope="col">Destination</th>
            <th scope="col">Amount</th>
            <th></th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="transaction in outgoingTransactions" :key="transaction.id">
            <td>
              <button
                class="btn btn-light"
                @click.prevent="deleteOutgoingTransaction(transaction.id)"
              >&#9850;</button>
            </td>
            <td>{{transaction.expense.description}}</td>
            <td>{{transaction.amount}}</td>
            <td style="color: red">&#8594;</td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
</template>

<script>
import methods from "../methods.js";

export default {
  name: "AssetDetail",
  props: ["assetPk", "incomes", "expenses"],

  data() {
    return {
      assetName: "",
      assetBalance: "",
      assetType: "BC",

      incomingTransactions: [],
      outgoingTransactions: [],

      inTransactionAmount: null,
      outTransactionAmount: null,
      transactionSource: null,
      transactionDestination: null,

      getURL: methods.getURL,
      getJSON: methods.getJSON,
      getCookie: methods.getCookie,
      resetInitData: methods.resetInitData
    };
  },

  mounted() {
    this.updateAssetData();
  },

  methods: {
    deleteAsset() {
      const url = this.getURL("detailAsset", this.assetPk);
      const csrfToken = this.getCookie("csrftoken");
      fetch(url, {
        credentials: "include",
        method: "DELETE",
        headers: {
          "Content-Type": "application/json",
          "X-CSRFToken": csrfToken
        }
      }).then(response => {
        if (response.status != 204) return;

        this.$parent.refreshData();
        this.$parent.hidePopups();
      });
    },

    updateAsset() {
      const url = this.getURL("detailAsset", this.assetPk);
      const csrfToken = this.getCookie("csrftoken");
      const body = JSON.stringify({
        description: this.assetName,
        balance: parseFloat(this.assetBalance),
        type: this.assetType
      });

      fetch(url, {
        credentials: "include",
        body,
        method: "PUT",
        headers: {
          "Content-Type": "application/json",
          "X-CSRFToken": csrfToken
        }
      }).then(response => {
        if (response.status != 200) return;

        this.closeBlock();
        this.$parent.refreshData();
      });
    },

    updateAssetData() {
      this.getDetails();
      this.getIncomingTransactions();
      this.getOutgoingTransactions();
    },

    getDetails() {
      this.getJSON(this.getURL("detailAsset", this.assetPk)).then(data => {
        this.assetName = data.description;
        this.assetBalance = data.balance;
        this.assetType = data.type;
      });
    },

    getIncomingTransactions() {
      this.getJSON(this.getURL("incomingAsset", this.assetPk)).then(data => {
        this.incomingTransactions = data.results;
      });
    },

    createIncomeTransaction() {
      const url = this.getURL("createIncomeTransaction", this.assetPk);
      const csrfToken = this.getCookie("csrftoken");
      const body = JSON.stringify({
        asset: { pk: this.assetPk },
        income: { pk: this.transactionSource },
        amount: parseFloat(this.inTransactionAmount)
      });

      fetch(url, {
        credentials: "include",
        body,
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          "X-CSRFToken": csrfToken
        }
      }).then(response => {
        if (response.status != 201) return;

        this.inTransactionAmount = null;
        this.updateAssetData();
        this.$parent.getCommonInfo();
      });
    },

    deleteIncomingTransaction(transactionID) {
      const url = this.getURL("detailIncomeTransaction", transactionID);
      const csrfToken = this.getCookie("csrftoken");
      fetch(url, {
        credentials: "include",
        method: "DELETE",
        headers: {
          "Content-Type": "application/json",
          "X-CSRFToken": csrfToken
        }
      }).then(response => {
        if (response.status != 204) return;

        this.updateAssetData();
        this.$parent.getCommonInfo();
      });
    },

    getOutgoingTransactions() {
      this.getJSON(this.getURL("outgoingAsset", this.assetPk)).then(data => {
        this.outgoingTransactions = data.results;
      });
    },

    createOutgoingTransaction() {
      const url = this.getURL("createExpenseTransaction", this.assetPk);
      const csrfToken = this.getCookie("csrftoken");
      const body = JSON.stringify({
        asset: { pk: this.assetPk },
        expense: { pk: this.transactionDestination },
        amount: parseFloat(this.outTransactionAmount)
      });

      fetch(url, {
        credentials: "include",
        body,
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          "X-CSRFToken": csrfToken
        }
      }).then(response => {
        if (response.status != 201) return;

        this.outTransactionAmount = null;
        this.updateAssetData();
        this.$parent.getCommonInfo();
      });
    },

    deleteOutgoingTransaction(transactionID) {
      const url = this.getURL("detailExpenseTransaction", transactionID);
      const csrfToken = this.getCookie("csrftoken");

      fetch(url, {
        credentials: "include",
        method: "DELETE",
        headers: {
          "Content-Type": "application/json",
          "X-CSRFToken": csrfToken
        }
      }).then(response => {
        if (response.status != 204) return;

        this.updateAssetData();
        this.$parent.getCommonInfo();
      });
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
