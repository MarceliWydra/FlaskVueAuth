<template>
    <div>
  <v-simple-table>
    <template v-slot:default>
      <thead>
        <tr>
          <th class="text-left">Datetime</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="item in logs" :key="item">
          <td>{{ item }}</td>
        </tr>
      </tbody>
    </template>
  </v-simple-table>
    <v-btn color="primary" v-on:click="logout">Logout</v-btn>
        </div>
</template>

<script>
import axios from 'axios'
import router from '../router'

export default {
  data () {
    return {
      logs: []
    }
  },
  methods: {
    fetchLogs () {
      const token = localStorage.getItem('token')

      if (token) {
        axios.get('api/logs', { headers: { 'Authorization': 'Bearer ' + token } })
          .then((response) => {
            this.logs = response.data.data
          })
      } else {
        router.replace({
          path: '/login',
          query: { redirect: router.currentRoute.fullPath }
        })
      }
    },
    logout () {
      this.$store.dispatch('logout')
    }
  },
  created: function () {
    this.fetchLogs()
  }
}
</script>

<style scoped>
</style>
