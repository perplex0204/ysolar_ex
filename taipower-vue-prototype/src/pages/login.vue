<template>
    <div class="login_page">
        <!-- Logo Area -->
        <div class="position-absolute  top-0 col-12 col-lg-auto">
            <div class="d-flex align-items-center justify-content-center justify-content-lg-start p-4"
            v-if="logo_title_show">
                <img :src="get_logo_src" width="60" />
                <h4 class="title-color ms-2 fst-italic">{{get_title_name}}</h4>
            </div>
        </div>
        <div class="position-absolute top-50 start-50 translate-middle col-12 col-lg-4">
            <div class="m-0">
                <div>
                    <transition name="login-form-fade">
                        <div class="login-form mt-4 p-4" v-if="login_form_display">
                            <div action="" method="" class="row g-3">
                                <h4>{{$t('login.please_login')}}</h4>
                                <div class="col-12">
                                    <label>{{$t('login.username')}}</label>
                                    <div class="input-group has-validation">
                                        <input type="text" name="username" class="form-control" :placeholder="$t('login.username')"
                                        :class="{'is-invalid': username_invalid}" v-model="login_form.username">
                                        <div class="invalid-feedback">
                                            {{$t('login.username_vaild')}}
                                        </div>
                                    </div>
                                </div>
                                <div class="col-12">
                                    <label>{{$t('login.password')}}</label>
                                    <div class="input-group has-validation">
                                        <input type="password" name="password" class="form-control" :placeholder="$t('login.password')"
                                        :class="{'is-invalid': password_invalid}" v-model="login_form.password">
                                        <div class="invalid-feedback">
                                            {{$t('login.password_vaild')}}
                                        </div>
                                    </div>
                                </div>
                                <div class="col-12 d-flex flex-wrap">
                                    <!-- <GoogleLogin :callback="callback"></GoogleLogin> -->
                                    <button @click="login()" class="btn btn-dark float-end ms-auto">{{$t('login.login')}}</button>
                                </div>
                            </div>
                            <hr class="mt-4">
                            <div class="col-12">
                                <p class="text-center mb-0">©2022</p>
                            </div>
                        </div>
                    </transition>
                </div>
            </div>
        </div>
        <!-- Background Animation from https://www.csscodelab.com/water-effect-simple-css-wave-animation/ -->
        <svg class="waves" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink"
        viewBox="0 24 150 28" preserveAspectRatio="none" shape-rendering="auto">
            <defs>
                <path id="gentle-wave" d="M-160 44c30 0 58-18 88-18s 58 18 88 18 58-18 88-18 58 18 88 18 v44h-352z" />
            </defs>
            <g class="parallax">
                <use xlink:href="#gentle-wave" x="48" y="0" />
                <use xlink:href="#gentle-wave" x="48" y="3" />
                <use xlink:href="#gentle-wave" x="48" y="5" />
                <use xlink:href="#gentle-wave" x="48" y="7" />
            </g>
        </svg>
        <!-- modal -->
        <div class="modal" tabindex="-1" id="myModal">
            <div class="modal-dialog modal-sm modal-dialog-centered">
                <div class="modal-content">
                    <div class="modal-header">
                        <h5 class="modal-title">Error</h5>
                        <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
                    </div>
                    <div class="modal-body">
                        <p>Password Error</p>
                    </div>
                    <div class="modal-footer">
                        <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Close</button>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>

<script>
import {Modal} from 'bootstrap'
import Oidc from "oidc-client"
import { googleOpenIdConnectSetting, githubOpenIdConnectSetting, gitlabOpenIdConnectSetting } from "@/assets/js/oidc.js"
export default {
    name: 'Login',
    data(){
        return {
            login_form_display: false,
            username_invalid: false,
            password_invalid: false,
            login_form:{
                username: '',
                password: ''
            },
            logo_title_show: false, 
        };
    },
    beforeMount(){
        this.logo_title_show = "VUE_APP_PAGETYPE" in process.env
    },
    methods:{
        valid_input(){
            let result = true
            if(this.login_form.username == null || this.login_form.username == ''){
                this.username_invalid = true
                result = false
            }
            if(this.login_form.password == null || this.login_form.password == ''){
                this.password_invalid = true
                result = false
            }
            return result
        },
        login(){
            if(this.login_form.username.length>0){
                if(this.login_form.username.includes("gmail")){
                    if(process.env.VUE_APP_OIDC_GOOGLE_CLIENT_ID != undefined){
                        this.$store.commit('set_oidc', 'gmail')
                        let mgr = new Oidc.UserManager(googleOpenIdConnectSetting)
                        mgr.signinRedirect()
                    }
                }
                else if(this.login_form.username.includes("github")){
                    if(process.env.VUE_APP_OIDC_GITHUB_CLIENT_ID != undefined && process.env.VUE_APP_OIDC_GITHUB_CLIENT_SECRET != undefined){
                        this.$store.commit('set_oidc', 'github')
                        let mgr = new Oidc.UserManager(githubOpenIdConnectSetting)
                        mgr.signinRedirect()
                    }
                }
                else if(this.login_form.username.includes("gitlab")){
                    if(process.env.VUE_APP_OIDC_GITLAB_CLIENT_ID != undefined && process.env.VUE_APP_OIDC_GITLAB_CLIENT_SECRET != undefined){
                        this.$store.commit('set_oidc', 'gitlab')
                        let mgr = new Oidc.UserManager(gitlabOpenIdConnectSetting)
                        mgr.signinRedirect()
                    }
                }
            }
            let that = this
            if(this.valid_input()){
                this.login_form_display = false
                var login_form = new FormData();
                login_form.append("username", this.login_form.username);
                login_form.append("password", this.login_form.password);
                this.axios.post('/login', login_form)
                .then(data => {
                    //console.log(data.data.data)
                    this.$store.dispatch('get_navLink').then(()=>{
                        setTimeout(function(){
                            const next_route = localStorage.getItem('solar_vue_previous_route')
                            if(![null, '/login', '/logout'].includes(next_route)){
                                // redirect to previous page
                                localStorage.removeItem('solar_vue_previous_route')
                                that.$router.push(next_route)
                            }else{
                                that.$router.push('/')
                            }
                        }, 500)
                    }).catch(e => {
                        alert("Error")
                        this.$router.go()
                    })
                    })
                .catch(e => {
                    this.myModal.show()
                    this.login_form_display = true
                    this.login_form.password = null
                })
                                
            }
            return false
        },
    },
    mounted(){
        // console.log(window.location.origin)
        if(this.$store.state.language != undefined && this.$store.state.language != null)
            this.$store.commit('setLang', this.$store.state.language)
        else 
            this.$store.commit('setLang', 'zh-TW')
        let that = this
        this.myModal = new Modal(document.getElementById('myModal'))
        setTimeout(function(){
            that.login_form_display = true
        }, 500)
    },
    computed:{
        get_title_name(){
            let pageType = process.env.VUE_APP_PAGETYPE
            if(pageType == undefined){
                return ""
            }
            return this.$i18n.te(`title.${pageType}`) ? this.$i18n.t(`title.${pageType}`) :
            ""
        },
        get_logo_src(){
            let pageType = process.env.VUE_APP_PAGETYPE
            if(pageType == undefined){
                return require("/public/imgs/logo.png")   
            }
            try {
                return require(`/public/imgs/${pageType}/logo.png`)
            } catch (error) {
                console.error(`logo of pageType "${pageType}" not found use default\n${error}`)
                return require("/public/imgs/logo.png")   
            }
        }
    }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
.login_page{
    width: 100vw;
    height: 100vh;
    background: linear-gradient(60deg, rgba(84,58,183,1) 0%, rgba(0,172,193,1) 100%);
}
/* waves */
.waves {
    position:absolute;
    bottom: 0;
    left: 0;
    width: 100%;
    height:15vh;
    min-height:100px;
    max-height:150px;
    z-index: 0;
}

/* Animation and color */

.parallax > use {
    animation: move-forever 25s cubic-bezier(.55,.5,.45,.5)     infinite;
}
.parallax > use:nth-child(1) {
    animation-delay: -2s;
    animation-duration: 7s;
    fill: rgba(255,255,255,0.7);
}
.parallax > use:nth-child(2) {
    animation-delay: -3s;
    animation-duration: 10s;
    fill: rgba(255,255,255,0.5);
}
.parallax > use:nth-child(3) {
    animation-delay: -4s;
    animation-duration: 13s;
    fill: rgba(255,255,255,0.3);
}
.parallax > use:nth-child(4) {
    animation-delay: -5s;
    animation-duration: 20s;
    fill: #fff;
}
@keyframes move-forever {
    0% {
        transform: translate3d(-90px,0,0);
    }
    100% { 
        transform: translate3d(85px,0,0);
    }
}
/*Shrinking for mobile*/
@media (max-width: 768px) {
    .waves {
        height:40px;
        min-height:40px;
    }
}


.login-form-fade-enter-active,
.login-form-fade-leave-active {
    transition: opacity 0.5s ease;
}

.login-form-fade-enter-from,
.login-form-fade-leave-to {
    opacity: 0;
}

.login-form{
    position: relative;
    border-radius: 5px;
    z-index: 1;
}

/* modal fix */
@media (min-width: 992px){
    .modal:deep(.modal-dialog){
        width: 500px !important;
        max-width: 500px !important;
    }
}

.title-color{
    color: rgb(255, 255, 255);
    border-bottom: 1px solid rgb(255, 255, 255);  
}

/* Dark Mode */
@media (prefers-color-scheme: dark) {
    .login_page{
        background: linear-gradient(60deg, rgb(55, 38, 120) 0%, rgb(1, 88, 100) 100%);
    }
    .parallax > use:nth-child(1) {
        fill: rgba(210, 210, 210,0.7);
    }
    .parallax > use:nth-child(2) {
        fill: rgba(210, 210, 210,0.5);
    }
    .parallax > use:nth-child(3) {
        fill: rgba(210, 210, 210,0.3);
    }
    .parallax > use:nth-child(4) {
        fill: rgb(210, 210, 210);
    }
    .title-color{
        color: rgb(220, 220, 220); 
        border-bottom: 1px solid rgb(220, 220, 220);       
    }
}
</style>
