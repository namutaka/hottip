import Vue from 'vue';
import moment from 'moment';
import './plugins/vuetify';
import App from './App.vue';
import router from './router';
import { createProvider } from './plugins/vue-apollo';

Vue.config.productionTip = false;

Vue.filter('datetime', function(date: string) {
  return moment(date).format('YYYY/MM/DD HH:mm');
});

new Vue({
  router,
  apolloProvider: createProvider(),
  render: h => h(App),
}).$mount('#app');
