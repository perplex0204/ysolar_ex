<template>
    <div>
        <div class="card p-4 pb-1">
            <h5><i class="el-icon-warning text-primary"></i>{{$t('setting.dispatch.案場自動派工設定')}}</h5>
            <div class="mt-2" v-if="stationId != null">
                <div class="d-flex flex-wrap w-100 align-items-center">
                    <div class="col-12 col-lg-auto d-flex align-items-center">
                        <el-icon class="text-success me-1"><credit-card /></el-icon>
                        {{$t('setting.dispatch.最低出工成本')}}
                    </div>
                    <div class="col-12 col-lg-auto d-flex ms-lg-2">
                        <el-input-number v-model="station_data.auto_dispatch_threshold"
                        type="number" :min="0" :disabled="$store.state.user_data.level < 3"/>
                        <button class="btn text-success pt-0 pb-0"
                        @click="save"
                        :disabled="$store.state.user_data.level < 3"
                        >
                            <i class="fa-solid fa-floppy-disk"></i>
                        </button>
                    </div>
                </div>
                <p class="fw-light mt-2 m-0 fs-7" >
                    <i class="fas fa-exclamation-circle"></i>
                    {{$t("setting.dispatch.auto_dispatch_setting_info")}}
                </p>
            </div>
        </div>
    </div>
</template>

<script>
import {CreditCard} from "@element-plus/icons-vue"
import { ElMessage } from 'element-plus'

export default {
    name: "AutoDispatch",
    components: {
        CreditCard
    },
    props: {
        stationId: {
            type: String,
            required: true
        },
        stationCollection: {
            type: String,
            required: true
        },
        stationName: {
            type: String,
            required: true
        }
    },
    data(){
        return {
            station_data: {
                auto_dispatch_threshold: null,
            },
        }
    },
    methods: {
        setting_dispatch_lgroup_auto_dispatch(){
            this.axios.get('/setting_dispatch_lgroup_auto_dispatch', {params: {ID: this.stationId}}).then(data=>{
                //console.log(data.data.data)
                this.station_data = data.data.data
            })
        },
        save(){
            if(typeof(this.station_data.auto_dispatch_threshold) != "number"){
                alert(this.$i18n.t('setting.dispatch.auto_dispatch_threshold_not_number'))
                return false
            }
            this.axios.post('/setting_dispatch_lgroup_auto_dispatch', {
                ID: this.stationId,
                auto_dispatch_threshold: this.station_data.auto_dispatch_threshold
            }).then(data=>{
                ElMessage.success({message: this.$i18n.t("成功")})
            })
        }
    },
    mounted(){
        this.setting_dispatch_lgroup_auto_dispatch()
    },
    watch: {
        stationId(){
            this.setting_dispatch_lgroup_auto_dispatch()
        }
    }
}
</script>

<style>

</style>