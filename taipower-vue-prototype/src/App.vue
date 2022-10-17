<template>
  <div id="app">
    <site-redirect-navbar v-if="site_redirect_data.enable" :urlData="site_redirect_data.data"
    @nav-show="site_redirect_navbar_show"></site-redirect-navbar>
    <el-config-provider :locale="locale">
      <router-view v-slot="{ Component }">
        <transition name="app-fade" mode="out-in">
          <component :is="Component" />
        </transition>
      </router-view>
    </el-config-provider>
  </div>
</template>

<script>
import { ElConfigProvider } from 'element-plus'
import elementLangEn from 'element-plus/lib/locale/lang/en'
import elementLangZhTw from 'element-plus/lib/locale/lang/zh-tw'
import siteRedirectNavbar from './layout/site_redirect_navbar.vue'
export default {
  name: 'App',
  components: {
    ElConfigProvider,
    siteRedirectNavbar
  },
  data(){
    return {
      locale: elementLangZhTw,
      site_redirect_data: {
        enable: false,
        data: []
      }
    }
  },
  beforeMount(){
    this.get_site_redirect_navbar()
  },
  methods: {
    get_site_redirect_navbar(){
      this.axios.get('/site_redirect_navbar').then(data=>{
        this.site_redirect_data.enable = data.data.data.enable
        this.site_redirect_data.data = data.data.data.json_data
      }).catch(err=>{
        this.site_redirect_data.enable = false
      })
    },
    site_redirect_navbar_show(){
      document.querySelectorAll("meta[name='theme-color']").forEach(i=>{
        i.setAttribute("content", "#3b3b3b")
      })
    }
  },
  watch: {
    '$i18n.locale': function(lang){
      switch(lang){
        case 'en-US':
        case 'en_us':
          this.locale = elementLangEn
          break
        case 'zh-TW':
        case 'zh_tw':
          this.locale = elementLangZhTw
          break
        case 'default':
          this.locale = elementLangZhTw
          break
      }
    },
    '$store.state.user_data': {
      handler(newValue, oldValue) {
        if(typeof newValue == 'object' && !Array.isArray(newValue) && newValue != null && 'pageType' in newValue){
          this.get_site_redirect_navbar()
        }
      },
      deep: true //Deep Watchers
    }
  },
}
</script>

<style>
@import './assets/fontawesome/css/all.css';
#app {
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
}
.fa, .fas, .far, .fal, .fad, .fab{
  line-height: inherit !important;
}
.card{
  border-radius: .5rem;
}
/* button{
  display: block !important;
} */
.app-fade-enter-active{
    transition: opacity .5s;
}
.app-fade-leave-active{
    transition: opacity .5s;
}
.app-fade-enter-from, 
.app-fade-leave-to{
    opacity: 0;
}

</style>