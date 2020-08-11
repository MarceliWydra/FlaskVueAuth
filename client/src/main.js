import Vue from 'vue'
import vuetify from '@/plugins/vuetify' // path to vuetify export
import App from './App.vue'
import vueResource from 'vue-resource'
import router from './router'
import store from './store'
import api from './api'
import axios from 'axios'

Vue.config.productionTip = false
Vue.prototype.$http = api

Vue.use(vueResource)
axios.interceptors.request.use(
  function (config) {
    const token = localStorage.getItem('token')
    if (token) config.headers.Authorization = `Bearer ${token}`
    return config
  },
  function (error) {
    return Promise.reject(error)
  })
axios.interceptors.response.use(
  response => {
    if (response.status === 200 || response.status === 201) {
      return Promise.resolve(response)
    } else {
      return Promise.reject(response)
    }
  },
  error => {
    if (error.response.status) {
      switch (error.response.status) {
        case 400:
          router.replace({
            path: '/',
            query: { redirect: router.currentRoute.fullPath }
          })
          break
        case 401:
          router.replace({
            path: '/',
            query: { redirect: router.currentRoute.fullPath }
          })
          break
        case 403:
          router.replace({
            path: '/',
            query: { redirect: router.currentRoute.fullPath }
          })
          break
        case 404:
          alert('page not exist')
          break
        case 502:
          setTimeout(() => {
            router.replace({
              path: '/',
              query: {
                redirect: router.currentRoute.fullPath
              }
            })
          }, 1000)
      }
      return Promise.reject(error.response)
    }
  }
)

/* eslint-disable no-new */
new Vue({
  el: '#app',
  router,
  store,
  vuetify,
  template: '<App/>',
  components: { App }
})
