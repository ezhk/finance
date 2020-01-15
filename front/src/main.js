import Vue from 'vue';
import VueRouter from 'vue-router';

import App from './App.vue';
import Common from './components/Common.vue';

Vue.config.productionTip = false;

const router = new VueRouter({
  mode: 'history',
  routes: [
    // main code URLs
    {
      path: '/',
      component: Common,
    },
  ],
});

Vue.use(VueRouter);
new Vue({
  router,
  render: h => h(App),
}).$mount('#app');