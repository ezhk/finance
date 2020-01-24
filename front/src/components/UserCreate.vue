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
          @blur="$v.username.$touch()"
          :class="$v.username.$error ? 'error-input' : ''"
        />
        <span class="error-description" v-if="$v.username.$error">
          <div
            v-if="!$v.username.minLength"
          >Minimum username length: {{ $v.username.$params.minLength.min }} symbols</div>
          <div v-else>Username field required</div>
        </span>
      </div>

      <div class="form-group">
        <input
          type="password"
          class="form-control"
          id="password"
          placeholder="Password"
          v-model="password"
          @blur="$v.password.$touch()"
          :class="$v.password.$error ? 'error-input' : ''"
        />
        <!-- Validation error -->
        <span class="error-description" v-if="$v.password.$error">
          <div
            v-if="!$v.password.minLength"
          >Minimum password length: {{ $v.password.$params.minLength.min }} symbols</div>
          <div v-else>Password field required</div>
        </span>
      </div>

      <div class="form-group">
        <input
          type="password"
          class="form-control"
          id="passwordRepeat"
          placeholder="Repeat password"
          v-model="passwordRepeat"
          @blur="$v.passwordRepeat.$touch()"
          :class="$v.passwordRepeat.$error ? 'error-input' : ''"
        />
        <!-- Validation error -->
        <span class="error-description" v-if="$v.passwordRepeat.$error">
          <div v-if="!$v.passwordRepeat.sameAsPassword">Passwords must be equals</div>
          <div v-else>Password field required</div>
        </span>
      </div>

      <div class="auth-buttons">
        <button class="btn btn-secondary" @click.prevent="createUser" :disabled="$v.$invalid">Create</button>
      </div>
    </form>
  </div>
</template>

<script>
import { required, minLength, sameAs } from "vuelidate/lib/validators";
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
      getJSON: methods.getJSON,
      getCookie: methods.getCookie
    };
  },

  validations: {
    username: {
      required,
      minLength: minLength(4)
    },
    password: {
      required,
      minLength: minLength(8)
    },
    passwordRepeat: {
      sameAsPassword: sameAs("password")
    }
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

      this.getJSON(url, {
        credentials: "include",
        body,
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          "X-CSRFToken": csrfToken
        }
      })
        .then(data => {
          if (!data.key) throw JSON.stringify(data);

          this.$parent.$refs.login.getUserInfo();
          this.$router.push("/");
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
  min-width: 320px;
  padding: 5px;

  border: 0.5px dashed darkgray;
  border-radius: 5px;
}
</style>
