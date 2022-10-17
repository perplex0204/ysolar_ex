import {createApp} from 'vue'
import App from './App'
import router from './router'
import store from './vuex'

//Bootstrap
import 'bootstrap'

//Axios
import axios from 'axios'
import VueAxios from 'vue-axios'
axios.defaults.baseURL = '/api';

//Element ui
import ElementPlus from 'element-plus'

//i18n
import i18n from './lang'

// Plotly
import Plotly from 'plotly.js-dist-min'

// import vue3GoogleLogin from 'vue3-google-login'

//登入狀態驗證
//if backend return unauth
axios.interceptors.response.use(function (response) {
    return response;
    }, function (error) {
    // 401 Unauth
    console.log(window.location.pathname)
    if(error.response.status === 401 && window.location.pathname != "/login" && window.location.pathname.includes('/openid_connect')) {
        // redirect to login page
        if(window.location.pathname != "/logout"){
            localStorage.setItem('solar_vue_previous_route', window.location.pathname)
        }
        if (!window.location.pathname.includes('/openid_connect')){
            window.location.href = "/login";
        }
        // window.location.href = "/login";
    }
    return Promise.reject(error);
})
router.beforeEach(async(to,from,next)=>{
    if(to.path.includes('/openid_connect')){
        console.log("to openid_connect")
        next()
    }
    else if(to.path != '/login' && to.path != '/logout') {   
        await axios.post('/login_status_navigation_guard', {to: to.path}) // Check login_status
        .then(function(data){
            if(data.data["status"] == true){
                const next_path = data.data.data.next
                delete data.data.data.next
                store.commit('set_user_data', data.data.data)
                
                // stationList history
                if(to.path == '/stationList'){
                    if(from.path != '/stationData'){
                        store.state.stationList_history = {}
                    }
                }

                if(next_path != to.path)
                    next(next_path)
                else
                    next()
            }else{
                next("/login")
            }
        })
        .catch(function(){
            next("/login");
        })
    }else{
        store.commit('set_user_data', {})
        next();
    }
})

/* eslint-disable no-new */
const vm = createApp(App)
// vm.use(vue3GoogleLogin, {
//     clientId: '515379922335-6o2rdu1248ch932f4jj4j4qt6o5uovs4.apps.googleusercontent.com'
// })
vm.use(router)
vm.use(store)
vm.use(VueAxios, axios)
vm.use(i18n)
vm.use(ElementPlus)
vm.config.globalProperties.Plotly = Plotly
vm.mount('#app')

