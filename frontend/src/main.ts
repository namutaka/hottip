import Vue from 'vue';
import moment from 'moment';
import './plugins/vuetify';
import App from './App.vue';
import router from './router';
import { createProvider } from './plugins/vue-apollo';
import Confirm from '@/components/Confirm.vue';

Vue.config.productionTip = false;

Vue.filter('datetime', function(date: string) {
  return moment(date).format('YYYY/MM/DD HH:mm');
});

declare module 'vue/types/vue' {
  interface Vue {
    $confirm(title: string, message: string, options?: any): Promise<boolean>;
  }
}

Vue.mixin({
  methods: {
    $confirm: Confirm.open,
  },
});

new Vue({
  router,
  apolloProvider: createProvider(),
  render: h => h(App),
}).$mount('#app');
