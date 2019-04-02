import Vue from "vue";
import './plugins/vuetify'
import App from "./App.vue";
import router from "./router";
import { createProvider } from "./plugins/vue-apollo";

Vue.config.productionTip = false;

new Vue({
  router,
  apolloProvider: createProvider(),
  render: h => h(App)
}).$mount("#app");
