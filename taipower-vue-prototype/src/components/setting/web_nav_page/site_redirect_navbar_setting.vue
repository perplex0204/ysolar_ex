<template>
    <div>
        <div class="card p-2 mb-3" v-loading="loading">
            <h5>
               <i class="fa-solid fa-plane-departure text-primary me-2"></i>
                Site Redirect Navbar Setting
                <el-popover
                    width="90vw"
                    trigger="hover"
                >
                    <template #reference>
                        <button class="btn float-end"><i class="fa-solid fa-circle-question"></i></button>
                    </template>
                    <h5><i class="fa-solid fa-lightbulb me-2"></i>The Navbar at the Top, Bring You to Another Site</h5>
                    <label>Example: </label>
                    <img class="img-fluid" src="imgs/info/site_redirect_navbar_example.png" />
                    <label class="mt-2"></label>
                    <label>After Modification, You need to refresh the site.</label>
                </el-popover>
            </h5>
            <el-switch v-model="enable" active-text="Enable" inactive-text="Disable" @change="post_site_redirect_navbar('enable', enable)" />
            <h6 class="mt-3">Live Preview</h6>
            <div class="d-flex justify-content-center">
                <div v-if="!enable">Site Redirect Navbar is Disabled</div>
                <div v-else-if="body_data.length == 0">
                    Site Redirect Navbar is Empty
                </div>
                <div class="w-100" v-else>
                    <site-redirect-navbar :url-data="body_data"></site-redirect-navbar>
                </div>
            </div>
            <div class="mt-3">
                <button class="btn float-end" @click="beautify_string">
                    <u>Beautify</u>
                </button>
                <el-input
                    v-model="body_json"
                    :rows="textarea_row"
                    type="textarea"
                    :class="{'error': json_error}"
                    placeholder='[ {"name": "太陽能新網站", "name_i18n": { "zh-TW": "太陽能新網站", "en-US": "New Website" }, "route": "#"} ]'
                />
                <button class="btn btn-primary mt-2" @click="load_example">Load Example</button>
                <button class="btn btn-success mt-2 float-end" @click="save"><i class="fa-solid fa-save"></i></button>
            </div>
        </div>
    </div>
</template>

<script>
import siteRedirectNavbar from '@/layout/site_redirect_navbar.vue'
import { ElMessage } from 'element-plus'

export default {
    name: "siteRedirectNavbarSetting",
    components: {
        siteRedirectNavbar
    },
    data(){
        return {
            enable: false,
            body_json: "[]",
            body_data: [],
            json_error: false,
            loading: false,
            textarea_row: 2
        }
    },
    mounted(){
        this.get_site_redirect_navbar()
    },
    methods: {
        get_site_redirect_navbar(){
            this.loading = true
            this.axios.get('/site_redirect_navbar').then(data=>{
                this.enable = data.data.data.enable
                this.body_json = data.data.data.json_string
                this.loading = false
                this.beautify_string()
            })
        },
        post_site_redirect_navbar(mode, data){
            this.axios.post('/site_redirect_navbar', {
                mode: mode,
                data: data
            }).then(data=>{
                ElMessage.success({message: this.$i18n.t("成功")})
                this.get_site_redirect_navbar()
                window.setTimeout(()=>{
                    const answer = confirm("Reload page? You need to reload to see the update.")
                    if(answer)
                        window.location.reload()
                }, 1000)
            }).catch(err=>{
                ElMessage.error({message: this.$i18n.t("錯誤")})
            })
        },
        save(){
            this.validate().then(()=>{
                this.post_site_redirect_navbar('data', this.body_json)
            }).catch((err)=>{
                alert(`Json Format Error\n${err}`)
            })
        },
        load_example(){
            this.body_json = `[
                {"name": "太陽能網站", "name_i18n": { "zh-TW": "太陽能網站", "en-US": "Solar Web"}, "url": "#", "pageType": "all"},
                {"name": "Apple", "name_i18n": { "zh-TW": "蘋果", "en-US": "Apple"}, "url": "https://apple.com", "pageType": ["taipower"]},
                {"name": "Google", "name_i18n": { "zh-TW": "谷歌", "en-US": "Google"}, "url": "https://google.com", "pageType": ["SPS"]}
            ]`
            this.beautify_string()
        },
        async validate(){
            if(this.body_json == null || this.body_json == ""){
                this.body_json = "[]"
            }
            try {
                this.body_data = await JSON.parse(this.body_json)
                this.json_error = false
                return new Promise((resolve, reject)=>{
                    resolve(null)
                })
            } catch (error) {
                this.json_error = true
                return new Promise((resolve, reject)=>{
                    reject(error)
                })
            }
        },
        beautify_string(){
            this.validate().then(()=>{
                this.body_json = JSON.stringify(this.body_data, null, "\t")
                this.textarea_row = this.body_json.split(/\r\n|\r|\n/).length
            })
        }
    },
    watch:{
        body_json(){
            this.validate()
        }
    }
}
</script>
<style scoped>
.el-textarea.error:deep(.el-textarea__inner){
    border: 1px solid var(--bs-danger) !important;
}
</style>