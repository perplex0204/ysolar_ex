<template>
    <div>
        <div v-show="!choose_new_alarm">
            <div class="d-flex">
                <button class="btn btn-warning"
                @click="finish">
                    <i class="fa-solid fa-angle-left"></i>
                </button>
                <div class="ms-auto">
                    <button class="btn btn-success w-100" @click="choose_new_alarm = true">{{$t('dispatch.新增警報')}}</button>
                </div>
            </div>
            <div class="col-12 mt-3">
                <div class="card p-2 pt-4">
                    <div class="d-flex align-items-center">
                        <h5 class="mb-0"><i class="icon-wrench text-primary"></i>{{$t('dispatch.type.alarm')}}</h5>
                        <div class="ms-auto">
                            <el-popover
                                placement="bottom"
                                :width="200"
                                trigger="click"
                                size="large"
                            >
                                <template #reference>
                                    <el-button>{{$t('dispatch.已選取')}}{{local_alarmData.length}}{{$t('dispatch.則警報')}}</el-button>
                                </template>
                                <div class="d-flex align-items-center pt-2 pb-2" v-for="(alarm) in local_alarmData" :key="alarm._id" style="border-bottom: .5px solid black;">
                                    {{`${alarm.equip_name}/${alarm.event}`}}
                                    <button class="btn ms-auto" @click="removeAlarm(alarm._id)"><i class="fas fa-trash"></i></button> 
                                </div>
                            </el-popover>
                        </div>
                    </div>
                    <div class="mt-3">
                        <alarm-reason-collapse :alarm-data="local_alarmData" v-if="local_alarmData.length > 0"
                        ref="alarm_reason_collapse"></alarm-reason-collapse>
                    </div>
                </div>
            </div>
        </div>
        <div v-if="choose_new_alarm">
            <alarm-table :station-Id="dispatchData.ID" @new-alarm="new_alarm"></alarm-table>
        </div>
    </div>
</template>
<script>
import alarmReasonCollapse from "./alarm_reason_collapse.vue"
import alarmTable from "./alarm_table.vue"
export default {
    name: "EditAlarm",
    components:{
        alarmReasonCollapse,
        alarmTable
    },
    emits: ['dispatch-edit-finish'],
    props:{
        alarmData: {
            type: Array,
            default: ()=>{
                return []
            }
        },
        dispatchData: {
            type: Object,
            required: true
        }
    },
    data(){
        return {
            choose_new_alarm: false,
            local_alarmData: []
        }
    },
    methods: {
        removeAlarm(_id){
            if(this.local_alarmData.length == 1){
                alert('至少選取一則警報')
                return false
            }
            let index = null
            for(var i in this.local_alarmData){
                console.log(i, _id)
                if(this.local_alarmData[i]._id == _id ){
                    index = i
                    break
                }
            }
            console.log(index)
            if(index != null){
                this.local_alarmData.splice(index, 1)
            }
        },
        new_alarm(alarm){
            console.log(alarm)
            alarm.event = alarm.alarm_event
            this.local_alarmData.push(alarm)
            this.choose_new_alarm = false
        },
        finish(){
            const answer = confirm("是否儲存？")
            if(answer){
                //
                if('alarm_reason_collapse' in this.$refs){
                    //console.log(this.$refs.alarm_reason_collapse)
                    this.axios.post('/dispatch_edit_content', {
                        dispatch_ID: this.dispatchData._id,
                        type: 'alarm',
                        data: this.$refs.alarm_reason_collapse.select_reason
                    }).then(data=>{
                        this.$emit('dispatch-edit-finish')
                    })
                }
            }else{
                this.$emit('dispatch-edit-finish')
            }
        }
    },
    mounted(){
        console.log(this.alarmData)
        console.log(this.dispatchData)
        Object.assign(this.local_alarmData, this.alarmData)
    }
}
</script>