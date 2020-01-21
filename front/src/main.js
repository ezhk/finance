import Vue from 'vue';
import VueRouter from 'vue-router';
import Vuelidate from 'vuelidate';

import App from './App.vue';
import Common from './components/Common.vue';
import UserCreate from './components/UserCreate.vue';

Vue.config.productionTip = false;

const router = new VueRouter({
  mode: 'history',
  routes: [
    // main code URLs
    {
      path: '/',
      component: Common,
    },

    {
      path: '/user/create',
      component: UserCreate,
    }
  ],
});

Vue.use(VueRouter);
Vue.use(Vuelidate);
new Vue({
  router,
  render: h => h(App),
}).$mount('#app');