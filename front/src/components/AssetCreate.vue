<template>
  <div class="category-add">
    <h6>Create asset</h6>
    <form>
      <div class="form-group">
        <input
          type="text"
          class="form-control"
          id="asset-create-name"
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
          id="asset-create-balance"
          v-model="assetBalance"
          placeholder="Balance"
          required
        />
      </div>
      <select class="form-control" id="asset-create-type" v-model="assetType">
        <option value="CA" selected="selected">Cash</option>
        <option value="BC">Bank card</option>
        <option value="CC">Credit card</option>
      </select>
      <div class="category-add-buttons">
        <button class="btn btn-light" @click.prevent="createAsset" :disabled="$v.$invalid">Create</button>
        <button class="btn btn-light" @click.prevent="closeBlock">Close</button>
      </div>
    </form>
  </div>
</template>

<script>
import { required, decimal } from "vuelidate/lib/validators";
import methods from "../methods.js";

export default {
  name: "AssetCreate",

  data() {
    return {
      assetName: "",
      assetBalance: "",
      assetType: "BC",

      getURL: methods.getURL,
      getCookie: methods.getCookie,
      resetInitData: methods.resetInitData
    };
  },

  validations: {
    assetName: { required },
    assetBalance: { required, decimal }
  },

  methods: {
    showError(error) {
      return this.$parent.$parent.$refs.error.showError(error);
    },

    createAsset() {
      const url = this.getURL("createAsset");
      const csrfToken = this.getCookie("csrftoken");
      const body = JSON.stringify({
        description: this.assetName,
        balance: parseFloat(this.assetBalance),
        type: this.assetType
      });
      console.log(this.$root);
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
