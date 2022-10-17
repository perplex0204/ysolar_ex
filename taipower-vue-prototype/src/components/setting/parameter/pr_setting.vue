<template>
    <div class="mb-3">
        <div class="card p-4 mt-3">
            <div class="d-flex flex-wrap align-items-center">
                <h5><i class="fa-solid fa-sun text-warning me-2"></i>{{$t('setting.parameter.PR設定')}}</h5>
            </div>
            <div class="d-flex flex-wrap align-items-center">
                {{$t('setting.parameter.使用溫度計算PR')}}
                <el-switch
                    class="ms-2"
                    size="large"
                    :active-text="$t('setting.parameter.使用')"
                    :inactive-text="$t('setting.parameter.不使用')"
                    v-model="pr_use_temp"
                    @change="update_pr"
                />
            </div>
        </div>
    </div>
</template>
<script>
export default {
    name: "pr_setting",
    props: {
        pr: {
            type: String,
            default: "pr"
        }
    },
    data(){
        return {
            pr_use_temp: false
        }
    },
    emits: ['update-pr'],
    methods: {
        update_pr( ){
            this.$emit('update-pr', 'pr', this.pr_use_temp? "pr_temp":"pr")
        }
    },
    mounted(){
        this.pr == "pr" ? this.pr_use_temp = false : this.pr_use_temp = true
    },
    watch: {
        pr(){
            this.pr == "pr" ? this.pr_use_temp = false : this.pr_use_temp = true
        }
    }
}
</script>