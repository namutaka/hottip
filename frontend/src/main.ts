import Vue from 'vue';
import moment from 'moment';
import './plugins/vuetify';
import App from './App.vue';
import router from './router';
import { createProvider } from './plugins/vue-apollo';
import Confirm from '@/components/Confirm.vue';

Vue.config.productionTip = false;

//
// フィルタ
//

Vue.filter('datetime', function(date: string) {
  return moment(date).format('YYYY/MM/DD HH:mm');
});

Vue.filter('ellipsis', function(value: string, length: number) {
  if (value.length <= length) {
    return value;
  } else {
    return value.substring(0, length - 1) + '…';
  }
});

//
// $root 拡張
//

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

//
// Vue起動
//

new Vue({
  router,
  apolloProvider: createProvider(),
  render: h => h(App),
}).$mount('#app');
