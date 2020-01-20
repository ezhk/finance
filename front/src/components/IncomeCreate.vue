<template>
  <div class="category-add">
    <h6>Create income</h6>
    <form>
      <div class="form-group">
        <input
          type="text"
          class="form-control"
          id="income-create-name"
          v-model="incomeName"
          placeholder="Name"
        />
      </div>
      <div class="category-add-buttons">
        <button class="btn btn-light" @click.prevent="createIncome">Create</button>
        <button class="btn btn-light" @click.prevent="closeBlock">Close</button>
      </div>
    </form>
  </div>
</template>

<script>
import methods from "../methods.js";

export default {
  name: "IncomeCreate",

  data() {
    return {
      incomeName: "",

      getURL: methods.getURL,
      getCookie: methods.getCookie,
      resetInitData: methods.resetInitData
    };
  },

  methods: {
    showError(error) {
      return this.$parent.$parent.$refs.error.showError(error);
    },

    createIncome() {
      const url = this.getURL("createIncome");
      const csrfToken = this.getCookie("csrftoken");
      const body = JSON.stringify({
        description: this.incomeName
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
