import Vue from 'vue';
import Router from 'vue-router';
import ChannelListPage from './views/ChannelListPage.vue';
import ChannelPage from './views/ChannelPage.vue';

Vue.use(Router);

export default new Router({
  mode: 'history',
  base: process.env.BASE_URL,
  routes: [
    {
      path: '/',
      name: 'home',
      redirect: { name: 'channels' },
    },
    {
      path: '/channels',
      name: 'channels',
      component: ChannelListPage,
    },
    {
      path: '/channels/:channelId',
      name: 'channel',
      component: ChannelPage,
    },
    {
      path: '/login/?v',
      name: 'login',
      beforeEnter: (to, from, next) => {
        next(false);
        window.location.replace(to.fullPath);
      },
    },
    {
      path: '/logout/?v', // 終端スラッシュをトリムされるのでダミークエリ追加
      name: 'logout',
      beforeEnter: (to, from, next) => {
        next(false);
        window.location.replace(to.fullPath);
      },
    },
  ],
});
