import Vue from 'vue'
import Router from 'vue-router'
import Login from './components/Login'
import Logs from './components/Logs'

Vue.use(Router)

export default new Router({
  routes: [
    {
      path: '/',
      name: 'login',
      component: Login
    },
    {
      path: '/logs',
      name: 'logs',
      component: Logs
    }
  ]
})
