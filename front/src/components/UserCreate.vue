<template>
  <div class="create-user">
    <form>
      <div class="form-group">
        <input
          type="text"
          class="form-control"
          id="username"
          placeholder="Username"
          v-model="username"
        />
      </div>
      <div class="form-group">
        <input
          type="password"
          class="form-control"
          id="password"
          placeholder="Password"
          v-model="password"
        />
      </div>
      <div class="form-group">
        <input
          type="password"
          class="form-control"
          id="passwordRepeat"
          placeholder="Repeat password"
          v-model="passwordRepeat"
        />
      </div>
      <div class="auth-buttons">
        <button class="btn btn-light" @click.prevent="createUser">Create</button>
      </div>
    </form>
  </div>
</template>

<script>
import methods from "../methods.js";

export default {
  name: "UserLogin",

  data() {
    return {
      showLogin: false,
      username: "",
      password: "",
      passwordRepeat: "",

      getURL: methods.getURL,
      getCookie: methods.getCookie
    };
  },

  methods: {
    showError(error) {
      return this.$parent.$refs.error.showError(error);
    },

    createUser() {
      const url = this.getURL("createUser");
      const csrfToken = this.getCookie("csrftoken");
      const body = JSON.stringify({
        username: this.username,
        password1: this.password,
        password2: this.passwordRepeat
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
        .then(data => {
          // created successful status eq 201
          if (data.status == 201) {
            this.$parent.$refs.login.getUserInfo();
            this.$router.push("/");
          }
        })
        .catch(error => this.showError(error));
    }
  }
};
</script>

<style scoped>
.create-user {
  display: flex;
  justify-content: center;

  text-align: center;
}

form {
  min-width: 400px;
  padding: 5px;

  border: 0.5px dashed darkgray;
  border-radius: 5px;
}
</style>
