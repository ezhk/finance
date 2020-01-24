<template>
  <div class="login">
    <img class="userpic" :src="`${imagePath}`" alt="?" @click="showLogin = !showLogin" />
    <div v-show="showLogin">
      <div v-if="user" class="logout-window">
        <p>{{limitWordLength(user, 9)}}</p>
        <button class="btn btn-light" @click="logoutUser">Logout</button>
      </div>
      <div v-else class="auth-window">
        <form>
          <div class="form-group">
            <input
              type="text"
              class="form-control"
              id="authUsername"
              placeholder="Username"
              v-model="authUsername"
              @blur="$v.authUsername.$touch()"
              :class="$v.authUsername.$error ? 'error-input' : ''"
            />
          </div>
          <div class="form-group">
            <input
              type="password"
              class="form-control"
              id="authPassword"
              placeholder="Password"
              v-model="authPassword"
              @blur="$v.authPassword.$touch()"
              :class="$v.authPassword.$error ? 'error-input' : ''"
            />
          </div>
          <div class="auth-buttons">
            <router-link class="btn btn-light" to="/user/create">Sign up</router-link>
            <button class="btn btn-light" @click.prevent="loginUser" :disabled="$v.$invalid">Login</button>
          </div>
        </form>
      </div>
    </div>
  </div>
</template>

<script>
import { required } from "vuelidate/lib/validators";
import methods from "../methods.js";

export default {
  name: "UserLogin",

  data() {
    return {
      showLogin: false,
      authUsername: "",
      authPassword: "",

      imagePath: `${process.env.BASE_URL}img/anonymous-user.svg`,
      user: null,

      getURL: methods.getURL,
      getJSON: methods.getJSON,
      getCookie: methods.getCookie,
      limitWordLength: methods.limitWordLength
    };
  },

  mounted() {
    this.getUserInfo();
  },

  validations: {
    authUsername: { required },
    authPassword: { required }
  },

  methods: {
    showError(error) {
      return this.$parent.$refs.error.showError(error);
    },

    getUserInfo() {
      this.getJSON(this.getURL("showUser"))
        .then(data => {
          this.user = data.username;
        })
        .catch(error => this.showError(error));
    },

    loginUser() {
      const url = this.getURL("loginUser");
      const csrfToken = this.getCookie("csrftoken");
      const body = JSON.stringify({
        username: this.authUsername,
        password: this.authPassword
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

          // Does function refreshData exist?
          const refreshDataFunc = this.$parent.$refs.router.refreshData;
          if (typeof refreshDataFunc === "function") refreshDataFunc();

          this.getUserInfo();
        })
        .catch(error => this.$parent.$refs.error.showError(error));
    },

    logoutUser() {
      const csrfToken = this.getCookie("csrftoken");
      fetch(this.getURL("logoutUser"), {
        credentials: "include",
        method: "POST",
        headers: {
          "X-CSRFToken": csrfToken
        }
      })
        .then(response => {
          if (response.status != 200)
            throw `Incorrect status code ${response.status}`;

          // Does function refreshData exist?
          const refreshDataFunc = this.$parent.$refs.router.refreshData;
          if (typeof refreshDataFunc === "function") refreshDataFunc();

          this.getUserInfo();
        })
        .catch(error => this.$parent.$refs.error.showError(error));
    }
  },

  watch: {
    user: function() {
      this.imagePath = this.user
        ? `${process.env.BASE_URL}img/authenticated-user.svg`
        : `${process.env.BASE_URL}img/anonymous-user.svg`;
    }
  }
};
</script>

<style scoped>
.login {
  position: relative;
}

.userpic {
  display: block;
  padding: 3px;

  height: 32px;
  width: 32px;

  border-radius: 3px;
}

.userpic:hover {
  background: rgb(240, 240, 240);
}

.auth-window,
.logout-window {
  position: absolute;
  top: 48px;
  right: 0px;

  padding: 3px;

  font-size: unset;
  color: black;
  background: white !important;

  border: 0.5px dashed darkgray;
  border-radius: 5px;
}
.auth-window {
  width: 180px;
}
.logout-window {
  font-weight: 300;
  text-align: center;
  width: 100px;
}

.auth-buttons {
  display: flex;
  justify-content: space-around;
}
</style>
