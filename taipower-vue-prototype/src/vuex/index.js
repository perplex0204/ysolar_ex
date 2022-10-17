import { createStore } from 'vuex'
import i18n from '@/lang'
import axios from 'axios'

// Create a new store instance.
const store = createStore({
    state () {
      let language = localStorage.getItem('solar_vue_language')
      if(language == null){
        language = navigator.language || navigator.userLanguage
      }
      /* Initial Set Page Scale */
      let page_scale = localStorage.getItem('solar_vue_page_scale')
      if(page_scale == null){
        page_scale = 1
      }
      document.body.style.zoom = page_scale
      return {
        language: language,
        isMobile: false,
        prevent_leave_at_once: false,
        user_data: {},
        navOpen: true,
        stationList_history: {}, //store stationList plant_select
        stationData_jump: {}, // stationData page jump when mounted,
        navLink: [], // navBar Link,
        page_scale: parseFloat(page_scale), // Page scale of enitire website
        oidc_type: "",
        icon_status:0,
      }
    },
    mutations: {
      setLang(state, lang){
        state.language = lang
        i18n.global.locale = lang;
        localStorage.setItem('solar_vue_language', lang)
      },
      setMobile(state, is_mobile){
        state.isMobile = is_mobile
      },
      set_prevent_leave_at_once(state, enable=false){
        state.prevent_leave_at_once = enable
      },
      set_user_data(state, data){
        state.user_data = data
      },
      set_nav_open(state, data){
        state.navOpen = data
      },
      set_navLink(state, data){
        if(data.status == 200){
          state.navLink = data.data.data
        }else{
          state.navLink = []
        }
      },
      set_pageScale(state, data){
        localStorage.setItem('solar_vue_page_scale', data)
        state.page_scale = data
        document.body.style.zoom = data
      },
      set_oidc(state, oidc_type){
        state.oidc_type = oidc_type
        localStorage.setItem('solar_vue_oidc', oidc_type)
      }
    },
    actions: {
      get_navLink({commit}){
        return new Promise((resolve, reject) => {
          axios.get('get_navLink').then(data=> {
            commit('set_navLink', data)
            resolve()
          }).catch(err => {
            console.error(err)
            reject()
          })
        })
      }
    }
  })

  export default store