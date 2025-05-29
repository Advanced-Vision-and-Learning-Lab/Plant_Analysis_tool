import Vue from 'vue';
import Router from 'vue-router';
import Welcome from '../views/Welcome.vue';
import ResultViewer from '../views/ResultViewer.vue';

Vue.use(Router);

export default new Router({
  mode: 'history',
  routes: [
    { path: '/', name: 'Welcome', component: Welcome },
    { path: '/analyze', name: 'ResultViewer', component: ResultViewer, props: route => ({ type: route.query.type, plant: route.query.plant }) }
  ]
});
