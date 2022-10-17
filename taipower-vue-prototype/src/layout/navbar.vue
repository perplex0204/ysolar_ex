<template>
    <div class="d-flex position-fixed nav_obj" style="z-index: 800;">
        <!-- 左側navbar -->
        <div class="d-lg-flex flex-column flex-shrink-0 p-3 my_navbar"
        ref="my_navbar"
        :style="{width:navopen==true?'200px':'100px', height: height}" :class="{'w-0': !navopen}">
            <a href="/" class="text-cneter link-dark text-decoration-none">
                <!-- <div :class="{'text-center': content_center, 'w-100': content_center}" style="width: 40">
                    <img  :src="navlogo" width="40" height="32"/>
                </div> -->
                <div :class="{'text-center': true, 'w-100': true}" style="width: 60">
                    <img  :src="get_logo_src" width="60"/>
                </div> 
                <div class="my-2 mb-2" :class="{'text-center': true, 'w-100': true}" style="min-height: 24px;">
                    <h5 class="m-0" v-if="navopen">{{get_title_name}}</h5>
                </div> 
                <!-- <transition name="title_animation">
                    <span class="fs-4" v-if="navopen==true" style="z-index:10; position: relative;">台灣電力公司</span>
                </transition> -->
            </a>
            <ul class="nav nav-pills flex-column mb-auto mt-2">
                <!-- Use compute to hide route for level  -->
                <li @click="change_page" class="nav-item" v-for="i in url_data" :key="i.name" :title="navopen? null: i.name_i18n[$store.state.language]">
                    <router-link :to="i.route" class="nav-link link-dark d-flex" aria-current="page" :class="{
                    'active': current_url == i.route}" style="height: 44px;">
                        <div class="d-flex justify-content-center align-items-center position-relative translate-middle" style="width: 32px; left: 26px; top: 50%;">
                            <div class="nav_alert_round" v-if="i.alert"></div>
                            <i :class="i.icon" class="fs-4"></i>
                        </div>
                        <transition name="content_animation">
                            <span class="ms-2 align-self-center" style="white-space: nowrap;" v-if="navopen == true">{{i.name_i18n[$store.state.language]}}</span>
                        </transition>
                    </router-link>
                </li>
            </ul>
            <hr>
            <ul class="nav nav-pills flex-column">
                <li class="nav-item" v-bind="tooltipShow" :title="navopen? null:  $t(`navLink.登出`)">
                    <router-link to="/logout" class="nav-link link-dark d-flex" aria-current="page" :class="{
                    'active': current_url == '/logout'}" style="height: 44px;">
                        <div class="d-flex justify-content-center align-items-center position-relative translate-middle" style="width: 32px; left: 26px; top: 50%;">
                            <i class="icon-nav_log fs-4"></i>
                        </div>
                        <transition name="content_animation">
                            <span class="ms-2 align-self-center" style="white-space: nowrap;" v-if="navopen == true">{{$t(`navLink.登出`)}}</span>
                        </transition>
                    </router-link>
                </li>
            </ul>
        </div>
        <!-- 左側navbar的開攏收合按鍵 -->
        <div class="d-flex btn_nav_open align-items-center text-white justify-content-center" @click="navopen=!navopen" style="color:gray;background-color:rgb(3,19,39);">
            ||
        </div>
    </div>
</template>
<script>
import {Tooltip} from 'bootstrap'
export default {
    name: 'Navbar',
    data(){
        return {
            navlogo: require('@/assets/logo.png'),
            navopen: localStorage.getItem('solar_vue_nav_close') == 'true' ? false : true,
            width: {open: "200px", off: "120px"},
            height: 'calc(100vh - .5rem)',
            content_center: false,
            current_url: window.location.pathname,
            user_level: this.$store.state.user_data.level,
            route_name: "",
            clicked_page:"售電平台"
        }
    },
    methods:{
        get_nav_alert(){
            for(var i in this.url_data){
                const index = i
                switch(this.url_data[i].route){
                    case "/dispatch":
                        this.axios.post('/get_disaptch_overview_count', {
                            stage: ['wait_admin_confirm_date', 'auto_reviewed_wait_for_manual', 'review_failed']
                        }).then(data => {
                            if(data.data.data.dispatch_count > 0){
                                this.url_data[index].alert = true
                            }else{
                                this.url_data[index].alert = false
                            }
                        })
                        break
                    case "/alarm":
                        this.axios.get('/alarm_total_count').then(data => {
                            if(parseInt(data.data.data) > 0){
                                this.url_data[index].alert = true
                            }else{
                                this.url_data[index].alert = false
                            }
                        })
                        break
                }
            }
        },
        navopen_change(){
            let that = this
            localStorage.setItem('solar_vue_nav_close', !that.navopen)
            //set vuex
            setTimeout(function(){
                that.$store.commit('set_nav_open', that.navopen)
            }, 400)
            
            if(this.navopen == true){
                that.content_center = !that.navopen
                return false
            }
            setTimeout(function(){
                that.content_center = !that.navopen
            }, 400)
        },
        get_navLink(){
            this.$store.dispatch('get_navLink')
        },
        get_nav_height(){   /* Dynamic Calc Nav Height */
            if('my_navbar' in this.$refs){   /* nav position to top differs when top navbar(MaoHong new/old site switching bar) occured. */
                this.height = `calc(${window.innerHeight - this.$refs.my_navbar.getBoundingClientRect().top}px - .5rem)`
            }else{
                this.height = 'calc(100vh - .5rem)'
            }
        },
        change_page:function(event){
            this.clicked_page = event.target.innerText
        }
    },
    beforeMount(){
        this.get_navLink()
    },
    mounted(){
        let that = this
        if(document.body.clientWidth < 991){
            this.$store.commit('setMobile', true)
            this.navopen = false
        }else{
            this.$store.commit('setMobile', false)
        }
        window.addEventListener("resize", function(event) {
            if(document.body.clientWidth < 991){
                that.$store.commit('setMobile', true)
                that.navopen = false
            }else{
                that.$store.commit('setMobile', false)
                that.navopen = true
            }
            that.get_nav_height()
        })
        this.syncdata = window.setInterval(this.get_nav_alert, 1000)
        this.navopen_change()
        this.get_nav_height()
    },
    unmounted(){
        window.removeEventListener("resize")
        window.clearInterval(this.syncdata)
    },
    watch:{
        navopen: function (){
            this.navopen_change()
        },
        $route (){
            this.current_url = window.location.pathname
            if(document.body.clientWidth < 991){
                this.navopen = false
            }
        },
        user_data(new_user_data) {
            if(new_user_data.level != undefined && new_user_data.level != this.user_level){
                this.user_level = new_user_data.level
                this.get_navLink()
            }
        }
    },
    computed:{
        tooltipShow(){
            if(this.navopen)
            return {}
            else
                return {
                    "data-bs-toggle": "tooltip",
                    "data-bs-placement": "right",
                }
        },
        url_data(){
            this.$store.state.navLink.forEach(element => {
                if(element.route == this.current_url){
                    this.route_name = element.name_i18n[this.$store.state.language]
                }
            })
            return this.$store.state.navLink
        },
        user_data() {
            return this.$store.state.user_data
        },
        get_title_name(){
            return this.$i18n.te(`navLink.title.${this.$store.state.user_data.pageType}`) ? this.$i18n.t(`navLink.title.${this.$store.state.user_data.pageType}`) :
            ""
        },
        get_logo_src(){
            try {
                if (this.clicked_page == '售電平台'){
                    console.log(this.clicked_page)
                    return require(`/public/imgs/logo.png`)
                } else if (this.clicked_page == '供需配適'){
                    console.log(this.clicked_page)
                    return require(`/public/imgs/logo.png`)
                } else if (this.clicked_page == '太陽光電'){
                    console.log(this.clicked_page)
                    return require(`/public/imgs/logo2.png`)
                } else if (this.clicked_page == '儲能系統'){
                    console.log(this.clicked_page)
                    return require(`/public/imgs/logo3.png`)
                } else {
                    return require(`/public/imgs/logo.png`)
                }
            } catch (error) {
                console.error(`logo of pageType "${this.$store.state.user_data.pageType}" not found use default\n${error}`)
                return require("/public/imgs/logo.png")   
            }
        }
    }
}
</script>
<style scoped>
    .my_navbar{
        max-height: calc(100vh - 1rem); 
        overflow:auto; 
        border-radius: 5px;
        margin-top: 0.5rem !important;
        margin-bottom: 0.5rem !important;
        -webkit-transition: all .2s ease-in-out;
        -moz-transition: all .2s ease-in-out;
        -o-transition: all .2s ease-in-out;
        transition: all .2s ease-in-out;
        transition-delay: .2s;
        box-shadow: 5px 0 15px -1px rgba(0, 0, 0, 0.58);
        background-color: rgb(3,19,39);
    }
    .btn_nav_open{
        display: inline-block;
        position: relative;
        top: 69vh;
        width: 1rem;
        height: 3rem;
        background-color: rgba(255, 255, 255, 0.9);
        border-top-right-radius: 5px;
        border-bottom-right-radius: 5px;
        border-top: 0.2px solid black;
        border-bottom: 0.2px solid black;
        border-right: 0.2px solid black;
        box-shadow: 5px 0 15px -1px rgba(0, 0, 0, 0.58);
    }
    .content_animation-enter-active {
        transition: all .4s ease;
    }
    .content_animation-leave-active {
        transition: all .4s ease;
    }
    .content_animation-enter-from,.content_animation-leave-to{
        /* .content_animation-leave-active below version 2.1.8 */ 
        transform: translateX(-10px);
        opacity: 0;
    }
    .title_animation-enter-active {
        transition: all .2s ease;
        transition-delay: .5s;
    }
    .title_animation-leave-active {
        transition: all .0s ease;
    }
    .title_animation-enter-from,.content_animation-leave-to{
        /* .content_animation-leave-active below version 2.1.8 */ 
        transform: translateX(-10px);
        opacity: 0;
    }
    .nav-link{
        padding: .5rem;
        color: gray;
    }
    /* 左側navbar滑鼠hover時的顏色 */
    .nav-pills .nav-link:hover{
        color: #fff;
        background-color: rgba(9, 49, 97, 0.5);
    }

    .icon-ttl_sunboard:focus::before, .icon-ttl_sunboard:hover::before{
        color: unset;
    }
    .icon-ttl_sunboard,
    .icon-wrench {
        font-size: 1.25rem!important;
    }
    .nav_alert_round{
        position: absolute;
        top: 0;
        left: 0;
        width: 8px;
        height: 8px;
        border-radius: 50%;
        background-color: var(--bs-danger);
        opacity: 0.8;
    }
    
    .nav_alert_round_active{
        position: absolute;
        top: -2px;
        right: -2px;
        width: 8px;
        height: 8px;
        border-radius: 50%;
        background-color: var(--bs-danger);
        transition: visibility 0s, opacity 0.5s linear;
    }
    @media (max-width: 991px) {
        .w-0{
            width: 0 !important;
            padding: 0 !important;
        }
        .btn_nav_open{
            width: 2rem;
            z-index: 9;
        }
        .my_navbar{
            z-index: 9;
        }
    }
    .nav-pills .nav-link.active, .nav-pills .show > .nav-link{
        color: #fff;
        background-color: rgba(34, 65, 102, 0.8);
    }
</style>