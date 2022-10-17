<template>
    <div class="w-100">
        <el-collapse v-if="Object.keys(alarmData).length > 0">
            <el-collapse-item
                v-for="alarm, alarm_id in alarmData"
                :key="alarm_id"
                :title="alarm.alarm_event" 
            >
                <div class="row w-100">
                    <div class="col-12 col-lg-4">
                        {{$t('廠區')}}：{{alarm.alarm_place}}
                        <br/>
                        {{$t('alarm.設備名稱')}}：{{alarm.equip_name}}
                        <br/>
                        {{$t('alarm.警報發生')}}：{{alarm.time}}
                        <br/>
                        {{$t('alarm.警報修復')}}：{{alarm.returntime}}
                    </div>
                    <div class="col-12 col-lg-8 mt-3 mt-lg-0">
                        <label style="margin-bottom: .5rem;"><span><i class="el-icon-s-opportunity"></i></span>{{$t('dispatch.原因分析')}}</label>
                        <el-collapse v-if="alarm_id in reason_obj">
                            <el-collapse-item v-for="(data, group) in reason_obj[alarm_id]" :key="group">
                                <template #title>
                                    <div class="d-flex align-items-center">
                                        <input type="checkbox" class="me-2"
                                        :id="alarm_id+'_'+group+'_checkbox'"
                                        :disabled="disable"
                                        @click.stop="cause_group_click($event, alarm, data, group)"
                                        @change="cause_group_click($event, alarm, data, group)"
                                        :checked="'alarm_cause' in alarm && Object.keys(data).every(i => alarm.alarm_cause.includes(i))"
                                        >
                                        <label :for="alarm_id+'_'+group+'_checkbox'" @click.stop>{{group}}</label>
                                    </div>
                                </template>
                                <div class="d-flex flex-wrap">
                                    <div 
                                        class="dis_option mb-2 me-2 p-1"
                                        v-for="(cause, cause_id) in data"
                                        :class="{'select': 'alarm_cause' in alarm && alarm.alarm_cause.includes(cause_id)}"
                                        @click="cause_click(alarm_id, cause_id, group, cause.event)"
                                        :key="cause_id"
                                    >
                                        {{cause.event}}
                                    </div>
                                </div>
                            </el-collapse-item>
                        </el-collapse>
                        <div 
                        style="margin: 1rem 0 0; display: block;"
                        class="d-flex flex-wrap aling-items-center"
                        v-if="'alarm_cause' in alarm">
                            <div class="p-1 mt-2 ">{{$t('dispatch.已選取原因')}}：</div>
                            <div v-for="event_name in alarm.alarm_cause_event" :key="event_name"
                            class="p-1 mt-2 me-2 reason_selected">
                                {{event_name}}
                            </div>
                        </div>
                    </div>
                </div>
            </el-collapse-item>
        </el-collapse>
        <div class="w-100 text-center" v-if="Object.keys(alarmData).length == 0">{{$t('無警報')}}</div>
    </div>
</template>
<script>
export default {
    name: "Alarm_reason_collapse",
    props: {
        alarmData: {
            type: Object,
            default: function(){
                return {}
            }
        },
        disable: {
            type: Boolean,
            default: false
        }
    },
    data(){
        return {
            reason_obj: {}
        }
    },
    methods: {
        alarm_id_get_reason(){
            let that = this
            this.axios.post('/alarm_id_get_reason', {
                ID_list: Object.keys(this.alarmData)
            }).then(data => {
                console.log(data.data.data)
                for(var _id in this.alarmData){
                    if(!(_id in this.reason_obj)){
                        this.reason_obj[_id] = {}
                    }
                    if(_id in data.data.data.data){
                        Object.assign(this.reason_obj[_id], data.data.data.data[_id].user_select)
                    }
                }
                //console.log(this.reason_obj)
            })
        },
        cause_click(alarm_id, cause_id, cause_group, cause_event){
            if(this.disable){
                return false
            }
            if(!("alarm_cause" in this.$parent.alarm_data[alarm_id])){
                this.$parent.alarm_data[alarm_id]["alarm_cause"] = []
                this.$parent.alarm_data[alarm_id]["alarm_cause_event"] = []
            }
            if(this.$parent.alarm_data[alarm_id]["alarm_cause"].includes(cause_id)){
                let index = this.$parent.alarm_data[alarm_id]["alarm_cause"].indexOf(cause_id)
                if (index !== -1) {
                    this.$parent.alarm_data[alarm_id]["alarm_cause"].splice(index, 1)
                    this.$parent.alarm_data[alarm_id]["alarm_cause_event"].splice(index, 1)
                }
            }else{
                this.$parent.alarm_data[alarm_id]["alarm_cause"].push(cause_id)
                this.$parent.alarm_data[alarm_id]["alarm_cause_event"].push(`${cause_group}/${cause_event}`)

            }
            //console.log(this.$parent.alarm_data[alarm_id])
        },
        cause_group_click(event, alarm, data, cause_group){
            if(this.disable){
                return false
            }
            let select = event.target.checked
            console.log(select)
            console.log(alarm, data)
            if(!("alarm_cause" in alarm)){
                alarm["alarm_cause"] = []
                alarm["alarm_cause_event"] = []
            }
            for(var _id in data){
                if(event.target.checked){
                    if(!(alarm["alarm_cause"].includes(_id))){
                        alarm["alarm_cause"].push(_id)
                        alarm["alarm_cause_event"].push(`${cause_group}/${data[_id].event}`)
                    }
                }else{
                    if((alarm["alarm_cause"].includes(_id))){
                        let index = alarm["alarm_cause"].indexOf(_id)
                        alarm["alarm_cause"].splice(index, 1)
                        alarm["alarm_cause_event"].splice(index, 1)
                    }
                }
            }
        }
    },
    mounted(){
        this.alarm_id_get_reason()
    },
    watch: {
        alarmData:{
            handler(newValue, oldValue) {
                this.alarm_id_get_reason()
            },
            deep: true //Deep Watchers
        }
    }
}
</script>
<style>
.dis_option{
    width: fit-content;
    cursor: pointer;
    background-color: rgb(233, 233, 233);
    color: black;
    border-radius: 5px;
}
.dis_option.select{
    background-color: rgb(87, 86, 86);
    color: white;
}
.reason_selected{
    width: fit-content;
    border-radius: 5px;
    background-color: rgb(87, 86, 86);
    color: white;
}
</style>