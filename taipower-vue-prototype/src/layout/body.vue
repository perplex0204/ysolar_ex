<template>
    <div>
        <div class="d-flex flex-wrap" style="overflow-x: hidden; background-color:rgb(5, 30, 61);">
            <navbar ref="navbar"></navbar>
            <router-view class="router_content" v-slot="{ Component }">
                <!-- 原程式：左右有空格 -->
                <!-- <div class="me-2 main-content w-100 ps-lg-4" :style="{'margin-left': navWidth}">
                    <div class="ps-3 pe-3" :style="$store.state.user_data.pageType != 'taipower'?'min-height: 100vh;':''"> -->
                <!-- 能源展用：左右無空格 -->
                <div class="main-content w-100 ps-lg-4" :style=" {'margin-left': navWidth}">
                    <div class="" :style="$store.state.user_data.pageType != 'taipower'?'min-height: 100vh;':''">

                        <!-- <div class="d-flex align-items-center">
                            <h4 class="router-name mt-3 mb-3">{{router_name}}</h4>
                            <el-popover
                                placement="bottom"
                                :width="200"
                                trigger="click"
                                :show-arrow="false"
                            >
                                <template #reference>
                                    <button class="btn ms-auto fs-4 p-0 me-2">
                                        <i class="fa-solid fa-circle-user"></i>                                            
                                    </button>
                                </template>
                                <label class="ms-2 fs-5 fw-bold">{{$store.state.user_data.username}}</label>
                                <label class="float-end fs-8">{{$t(`setting.users.level.${$store.state.user_data.level}`)}}</label>
                                <br/>
                                <ul class="nav nav-pills mt-3 d-flex flex-row align-items-center">
                                    <li class="nav-item">
                                        <router-link to="/setting" class="nav-link link-dark p-0">
                                            <div class="d-flex align-items-center">
                                                <i class="icon-nav_setting fs-4"></i>
                                            </div>
                                        </router-link>
                                    </li>
                                    <li class="nav-item ms-auto col-7" v-if="$store.state.user_data.pageType == 'taipower'">
                                        <el-select v-model="language" size="large">
                                            <el-option v-for="lang, val in lang" :key="val" :value="val" :label="lang"></el-option>
                                        </el-select>
                                    </li>
                                    <li class="nav-item ms-auto">
                                        <router-link to="/logout" class="nav-link link-dark p-0">
                                            <div class="d-flex align-items-center">
                                                <i class="icon-nav_log fs-4"></i>
                                            </div>
                                        </router-link>
                                    </li>
                                </ul>
                            </el-popover>
                        </div> -->
                        <transition name="fade" mode="out-in">
                            <component style="padding: 0rem .5rem;" :is="Component" />
                        </transition>
                    </div>
                    <body-footer></body-footer>
                </div>
            </router-view>
        </div>
    </div>
</template>
<script>
    import navbar from './navbar.vue'
    import bodyFooter from './footer.vue'
    export default{ 
        components: { navbar, bodyFooter },
        data(){
            let lang = require("./footer.vue").default.data()
            return{
                isMounted: false,
                language: "zh-TW",
                lang: lang.lang
            }
        },
        mounted(){
            this.isMounted = true
            if(this.$store.state.language != undefined && this.$store.state.language != null){
                if(Object.keys(this.lang).includes(this.$store.state.language))
                    this.language = this.$store.state.language
                else
                    this.$store.commit('setLang', this.language)
            }
        },
        computed:{
            router_name(){
                if(this.isMounted)
                    return this.$refs.navbar.route_name
                else
                    return this.$route.name
            },
            navWidth(){
                if(!this.isMounted)
                    return "200px"
                if(this.$store.state.isMobile){
                    return '0px'
                }else{
                    if(this.$refs.navbar.navopen)
                        return this.$refs.navbar.width.open
                    else
                        return this.$refs.navbar.width.off
                }
            }
        },
        watch: {
            language(){
                this.$store.commit('setLang', this.language)
            }
        }
    }
</script>

<style>
.router-name{
    color: rgb(68, 66, 66);
}
.main-content{
    min-height: 100%;
    transition: margin .4s ease-in-out;
}
@media (max-width: 991px){
    .main-content{
        position: absolute !important;
    }
    .position-absolute-lg{
        position: absolute;
    }
}

</style>