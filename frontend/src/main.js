import Vue from 'vue';
import App from './App.vue';
import router from './router';
import '../public/favicon.ico'
// import vuetify from './plugins/vuetify';
// import Vuetify from 'vuetify';
// import 'vuetify/dist/vuetify.min.css';

Vue.config.productionTip = false;

// Vue.use(Vuetify);

new Vue({
  router,
  render: h => h(App)
  // vuetify,
  
}).$mount('#app');

console.log("Vue app mounted!");
