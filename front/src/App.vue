<template>
  <div id="app" class="container">
    <header>
      <router-link class="header-title" to="/">Personal finances</router-link>
      <user-login ref="login"></user-login>
    </header>

    <div class="top">
      <keep-alive>
        <router-view :key="$route.fullPath"></router-view>
      </keep-alive>
    </div>
    <footer class="site-footer">
      <a href="https://github.com/ezhk">Andrey Kiselev</a> &copy;&nbsp;2020
    </footer>
  </div>
</template>

<script>
import UserLogin from "./components/UserLogin.vue";

export default {
  name: "app",

  components: {
    UserLogin
  }
};
</script>

<style>
header,
footer {
  margin: 5px 0 5px;
  padding: 0 5px;
  height: 45px;

  border-radius: 5px;
  border: 0.5px solid darkgray;

  font-family: "Helvetica Neue", Helvetica, Arial, sans-serif;

  align-items: center;
  min-width: 320px;
}

header {
  display: flex !important;
  flex-direction: row;
  justify-content: space-between;

  padding-left: 15px;

  font-size: 1.3rem;
  font-family: monospace;
  color: goldenrod;
}

.header-title:any-link {
  color: unset;
  text-decoration: none;
}

footer {
  padding-right: 15px;
  text-align: right;

  line-height: 45px;
}

footer > a {
  color: unset;
  text-decoration: none;
}

.container {
  margin: 0 auto;

  max-width: 1000px;
  min-width: 320px;
  min-height: 100%;

  display: flex;
  flex-direction: column;

  padding: 0 5px;
}

.top {
  flex-grow: 1;
}
</style>
