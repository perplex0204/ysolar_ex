<template>
    <div>
        <div class="mb-3">
            <div class="card p-4 mt-3">
                <div class="d-flex flex-wrap align-items-center">
                    <h5><i class="fa-solid fa-magnifying-glass-plus text-warning me-2"></i>{{$t('setting.parameter.字體大小')}}</h5>
                </div>
                <el-slider v-model="scale" :step="0.1" :min="0.7" :max="1.3" show-stops @change="update_scale" />
            </div>
        </div>    
    </div>
</template>

<script>
export default {
    name: "pageScale",
    data(){
        return {
            scale: this.$store.state.page_scale
        }
    },
    methods: {
        update_scale(){
            this.$store.commit('set_pageScale', this.scale)
        }
    }
}
</script>