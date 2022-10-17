<template>
    <div>
        <div v-loading="Object.keys(user_parameter).length == 0">
            <pr-setting :pr="user_parameter.pr" @update-pr="update_parameter" />
            <page-scale />
        </div>
    </div>
</template>
<script>
import prSetting from './parameter/pr_setting.vue'
import pageScale from './parameter/page_scale.vue'

export default {
    name: "Parameter",
    components: {
        prSetting,
        pageScale
    },
    data(){
        return {
            user_parameter: {}
        }
    },
    methods: {
        load_user_parameter(){
            this.axios.get('/setting/load_user_parameter').then(data=>{
                window.setTimeout(()=>{
                    this.user_parameter = data.data.data
                }, 500)
            })
        },
        update_parameter(key, data){
            //console.log(key, data)
            this.user_parameter[key] = data
            this.axios.post('/setting/load_user_parameter', this.user_parameter).then(data=>{

            })
        }
    },
    mounted(){
        this.load_user_parameter()
    }
}
</script>