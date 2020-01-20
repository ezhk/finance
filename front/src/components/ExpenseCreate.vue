<template>
  <div class="category-add">
    <h6>Create expense</h6>
    <form>
      <div class="form-group">
        <input
          type="text"
          class="form-control"
          id="expense-create-name"
          v-model="expenseName"
          placeholder="Name"
        />
      </div>
      <div class="form-group">
        <input
          type="number"
          step="0.01"
          class="form-control"
          id="expense-create-monthly-limit"
          v-model="expenseMonthlyLimit"
          placeholder="Monthly limit"
        />
      </div>
      <div class="category-add-buttons">
        <button class="btn btn-light" @click.prevent="createExpense">Create</button>
        <button class="btn btn-light" @click.prevent="closeBlock">Close</button>
      </div>
    </form>
  </div>
</template>

<script>
import methods from "../methods.js";

export default {
  name: "ExpenseCreate",

  data() {
    return {
      expenseName: "",
      expenseMonthlyLimit: "",

      getURL: methods.getURL,
      getCookie: methods.getCookie,
      resetInitData: methods.resetInitData
    };
  },

  methods: {
    showError(error) {
      return this.$parent.$parent.$refs.error.showError(error);
    },

    createExpense() {
      const url = this.getURL("createExpense");
      const csrfToken = this.getCookie("csrftoken");
      const body = JSON.stringify({
        description: this.expenseName,
        monthly_limit: parseFloat(this.expenseMonthlyLimit)
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

          this.closeBlock();
          this.resetInitData();

          this.$parent.refreshData();
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
  position: absolute;
  top: 20%;
  padding: 5px;
  z-index: 1;

  background: white !important;

  border: 1px dashed darkgray;
  border-radius: 5px;

  text-align: center;
}

.category-add-buttons {
  margin-top: 5px;
  display: flex;
  justify-content: space-around;
}

.btn {
  width: 80px !important;
}
</style>
