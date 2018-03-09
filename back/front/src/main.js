// The Vue build version to load with the `import` command
// (runtime-only or standalone) has been set in webpack.base.conf with an alias.
import Vue from 'vue'
import App from './App';
import router from './router';
import store from './store/';
import * as firebase from 'firebase';

import Chat from '@/components/small-comp/dir-chat.vue'
import CardUser from '@/components/small-comp/dir-user-card.vue'

Vue.component('dir-chat', Chat);
Vue.component('dir-user-card', CardUser);

firebase.initializeApp({
  apiKey: "AIzaSyCcI4kBCa8LTxpDiS8YeKp12uAcuk9sjZ8",
  authDomain: "mental-7912c.firebaseapp.com",
  databaseURL: "https://mental-7912c.firebaseio.com",
  projectId: "mental-7912c",
  storageBucket: "",
  messagingSenderId: "7528187351"
});

Vue.config.productionTip = false;

/* eslint-disable no-new */
new Vue({
  el: '#app',
  router,
  store,
  template: '<App/>',
  components: { App }
});
