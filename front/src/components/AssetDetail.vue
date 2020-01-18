<template>
  <div class="category-add">
    <h5>Asset Detail</h5>
    <div class="subheader">Description</div>
    <form>
      <div class="form-group">
        <input
          type="text"
          class="form-control"
          id="name"
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
          id="balance"
          v-model="assetBalance"
          placeholder="Balance"
          required
        />
      </div>
      <select class="form-control" id="type" v-model="assetType">
        <option value="CA" selected="selected">Cash</option>
        <option value="BC">Bank card</option>
        <option value="CC">Credit card</option>
      </select>
      <div class="category-add-buttons">
        <button class="btn btn-light" @click.prevent="updateAsset">Update</button>
        <button class="btn btn-light" @click.prevent="closeBlock">Close</button>
      </div>
    </form>
    <hr />
    <div class="subheader">Transaction</div>
    <form>
      <div class="form-group">
        <input
          type="number"
          step="0.01"
          class="form-control"
          id="amount"
          v-model="transactionAmount"
          placeholder="Amount"
          required
        />
      </div>
      <select class="form-control" id="source" v-model="transactionSource">
        <option v-for="option in incomes" :key="option">{{option.description}}</option>
      </select>
      <div class="category-add-buttons">
        <button class="btn btn-light" @click.prevent="createAsset">Add transaction</button>
        <button class="btn btn-light" @click.prevent="closeBlock">Close</button>
      </div>
    </form>
    <hr />
    <div class="subheader">Incoming transactions history</div>
    <table class="table">
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
    <hr />
    <div class="subheader">Outgoing transactions history</div>
    <table class="table">
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
</template>

<script>
import methods from "../methods.js";

export default {
  name: "AssetDetail",
  props: ["assetPk", "incomes"],

  data() {
    return {
      assetName: "",
      assetBalance: "",
      assetType: "BC",

      incomingTransactions: [],
      outgoingTransactions: [],

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
        this.getIncomingTransactions();
      });
    },

    getOutgoingTransactions() {
      this.getJSON(this.getURL("outgoingAsset", this.assetPk)).then(data => {
        this.outgoingTransactions = data.results;
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
        this.getOutgoingTransactions();
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

  max-height: 90%;
}

.category-add-buttons {
  margin-top: 5px;
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
</style>
