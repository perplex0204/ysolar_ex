<template>
    <div class="w-100">
        <el-collapse v-if="Object.keys(alarmData).length > 0">
            <el-collapse-item
                v-for="alarm in alarmData"
                :key="alarm.id"
                :title="alarm.event" 
            >
                <div class="row w-100">
                    <div class="col-12 col-lg-4">
                        {{$t('alarm.設備名稱')}}：{{alarm.equip_name}}
                        <br/>
                        {{$t('alarm.警報發生')}}：{{alarm.time}}
                        <br/>
                        {{$t('alarm.警報修復')}}：{{alarm.returntime}}
                    </div>
                    <div class="col-12 col-lg-8 mt-3 mt-lg-0">
                        <label style="margin-bottom: .5rem;"><span><i class="el-icon-s-opportunity"></i></span>{{$t('dispatch.原因分析')}}</label>
                        <el-collapse v-if="alarm._id in reason_obj">
                            <el-collapse-item v-for="(data, group) in reason_obj[alarm._id]" :key="group">
                                <template #title>
                                    <div class="d-flex align-items-center">
                                        <input type="checkbox" class="me-2"
                                        :id="alarm._id+'_'+group+'_checkbox'"
                                        :disabled="disable"
                                        @click.stop="cause_group_click($event, alarm._id, data, group)"
                                        @change="cause_group_click($event, alarm._id, data, group)"
                                        :checked="alarm._id in select_reason && Object.keys(data).every(i =>
                                        Object.keys(select_reason[alarm._id]).includes(i))"
                                        >
                                        <label :for="alarm._id+'_'+group+'_checkbox'" @click.stop>{{group}}</label>
                                    </div>
                                </template>
                                <div class="d-flex flex-wrap">
                                    <div 
                                        class="dis_option mb-2 me-2 p-1"
                                        v-for="(cause, cause_id) in data"
                                        :class="{'select': alarm._id in select_reason && cause_id in select_reason[alarm._id]}"
                                        @click="cause_click(alarm._id, cause_id, cause, group)"
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
                        v-if="alarm._id in select_reason">
                            <div class="p-1 mt-2 ">{{$t('dispatch.已選取原因')}}：</div>
                            <div v-for="cause, cause_ID in select_reason[alarm._id]" :key="cause_ID">
                                <div v-if="cause_ID != 'else'" class="p-1 mt-2 me-2 reason_selected">
                                    {{cause.group}}/{{cause.event}}
                                </div>
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
            reason_obj: {},
            select_reason: {},
        }
    },
    methods: {
        alarm_id_get_reason(){
            let that = this
            this.axios.post('/alarm_id_get_reason', {
                ID_list: Object.keys(this.select_reason)
            }).then(data => {
                console.log(data.data.data)
                for(var i in this.alarmData){
                    let _id = this.alarmData[i]._id
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
        cause_click(alarm_id, cause_id, cause, group){
            if(this.disable){
                return false
            }
            if(cause_id in this.select_reason[alarm_id]){
                delete this.select_reason[alarm_id][cause_id]
            }else{
                cause.group = group
                this.select_reason[alarm_id][cause_id] = cause
            }


        },
        cause_group_click(event, alarm_id, data, cause_group){
            if(this.disable){
                return false
            }
            let select = event.target.checked
            //console.log(select)
            //console.log(data)
            for(var _id in data){
                if(event.target.checked){
                    data[_id].group = cause_group
                    this.select_reason[alarm_id][_id] = data[_id]
                }else{
                    if(_id in this.select_reason[alarm_id]){
                        delete this.select_reason[alarm_id][_id]
                    }
                }
            }
            //console.log(this.select_reason)
        },
        alarmData_update(alarmData){
            //console.log(alarmData)
            let ID_list = []
            alarmData.forEach((alarm => {
                ID_list.push(alarm._id)
                if(!(alarm._id in this.select_reason)){
                    this.select_reason[alarm._id] = {}
                    this.alarm_id_get_reason()
                }
            }))
            Object.keys(this.select_reason).forEach(ID => {
                if(!ID_list.includes(ID)){
                    delete this.select_reason[ID]
                    return true
                }
            })
        }
    },
    mounted(){
        for(var alarm_id in this.alarmData){
            let alarm = this.alarmData[alarm_id]
            let reason_dict = {}
            if('cause_data' in alarm){
                if('user_select' in alarm.cause_data){
                    alarm.cause_data.user_select.forEach(s=>{
                        reason_dict[s.ID] = s
                    })
                }
            }else{
                alarm.cause_data = {
                    ai_analysis: {},
                    user_select: {}
                }
            }
            this.select_reason[alarm._id] = reason_dict
        }
        //console.log(this.select_reason)
        this.alarm_id_get_reason()
    },
    watch: {
        alarmData:{
            handler(newValue, oldValue) {
                this.alarmData_update(newValue)
            },
            deep: true //Deep Watchers
        },
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