import Vue from 'vue';
import Router from 'vue-router';
// import ResultViewer from '../views/ResultViewer.vue';
// import { createRouter, createWebHistory } from 'vue-router'

// const routes = [
//   {
//     path: '/',
//     name: 'HomePage',
//     component: () => import('../views/HomePage.vue'),
//   },
//   {
//     path: '/plant-details/:plantName',
//     name: 'PlantDetails',
//     component: () => import('../views/PlantDetails.vue'),
//     props: true
//   },
//   {
//     path: '/analyze',
//     name: 'ResultViewer',
//     component: ResultViewer,
//     props: route => ({ type: route.query.type, plant: route.query.plant })
//   }
// ]

// const router = createRouter({
//   history: createWebHistory(process.env.BASE_URL),
//   routes
// })

Vue.use(Router);

export default new Router({
  mode: 'history',
  routes: [
    { 
      path: '/',
      name: 'HomePage',
      component: () => import('../views/HomePage.vue')
    },
    {
      path: '/plant-details/:plantName',
      name: 'PlantDetails',
      component: () => import('../views/PlantDetails.vue'),
      props: true
    },
    { 
      path: '/analyze',
      name: 'ResultViewer', 
      component: () => import('../views/ResultViewer.vue'), 
      props: route => ({ type: route.query.type, plant: route.query.plant })
    }
  ]
});
