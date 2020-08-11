import Vue from 'vue'
import Vuex from 'vuex'
import axios from 'axios'
import router from './router'

Vue.use(Vuex);

const types = {
    LOGIN: 'LOGIN',
    LOGOUT: 'LOGOUT'
}

const state = {
    logged: localStorage.getItem('token')
}

const getters = {
    isLogged: state => state.logged
}

const actions = {
    login ({commit}, credential) {
        axios.post('/api/login', credential)
            .then((response) => {
                localStorage.setItem('token', response.data.access_token);
                commit(types.LOGIN);
                router.push({path: '/logs'});
            }).catch(err => {
                alert('Try again!');
        });
    },

    logout({commit}) {
        axios.post('/api/logout')
            .then((response) => {
                localStorage.removeItem('token');
                commit(types.LOGOUT);
                router.push({path: '/'});
            });
    }
}

const mutations = {
    [types.LOGIN] (state) {
        state.logged = 1;
    },

    [types.LOGOUT] (state) {
        state.logged = 0;
    }
}

export default new Vuex.Store({
    state,
    getters,
    actions,
    mutations
})