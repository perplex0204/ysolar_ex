<template>
    <div class="footer mt-2" v-if="$store.state.user_data.pageType != 'taipower'">
        <div class="d-flex flex-wrap justify-content-between align-items-center ps-4 pe-4 mt-2 mb-4">
            <div></div>
            <label class="col-12 col-lg-auto text-center">©2022</label>
            <div class="col-12 col-lg-auto d-flex flex-wrap align-items-center flex-lg-row-reverse">
                <div class="col-12 col-lg-auto">
                    {{$t('選擇語言')}}
                    <select class="form-select" aria-label="Default select example" v-model="language">
                        <option v-for="lang, val in lang" :key="val" :value="val">{{lang}}</option>
                    </select>
                </div>
                <div class="mt-1 mb-1 d-flex flex-wrap align-items-center" v-if="app_badge">
                    <a :href="ios_url" v-if="ios_url != '#'"><img :src="`imgs/app/${language}/app_store_badge.svg`" /></a>
                    <a :href="android_url" v-if="android_url != '#'"><img width="144" :src="`imgs/app/${language}/google_play_badge.png`" /></a>
                </div>
            </div>
        </div>
    </div>
</template>
<script>
import c from 'assets/js/common.js'
export default{ 
    data(){
        return{
            language: "zh-TW",
            ios_url: '#',
            android_url: '#',
            lang: {
                'zh-TW': '中文',
                'en-US': 'English'
            }
        }
    },
    mounted(){
        if(this.$store.state.language != undefined && this.$store.state.language != null){
            if(Object.keys(this.lang).includes(this.$store.state.language))
                this.language = this.$store.state.language
            else
                this.$store.commit('setLang', this.language)
        }
        this.axios.get('/get_app_store_url').then(data=>{
            this.ios_url = data.data.data.ios
            this.android_url = data.data.data.android
        })
    },
    computed: {
        app_badge(){
            if(c.getCookie('is_app') != ""){
                return false
            }else{
                return true
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
.footer{
    position: absolute;
    left: 0px;
    min-height: 80px;
    width: 100%;
    background: rgb(200,200,200);
    background: var(--footer-bg-gradient);
    background-size: 400% 400%;
    animation: gradient 8s ease infinite;
}
@keyframes gradient {
	0% {
		background-position: 0% 50%;
	}
	50% {
		background-position: 100% 50%;
	}
	100% {
		background-position: 0% 50%;
	}
}
</style>
