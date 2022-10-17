<template>
    <div>
        <div class="modal-header d-flex flex-wrap">
            <h5 class="modal-title">{{$t('dispatch.新增警報')}}</h5>
            <el-popover
                placement="bottom"
                :width="200"
                trigger="click"
            >
                <template #reference>
                    <el-button>{{$t('dispatch.已選取')}}{{Object.keys(select_alarm_obj).length}}{{$t('dispatch.則警報')}}</el-button>
                </template>
                <div class="d-flex align-items-center pt-2 pb-2" v-for="(alarm, _id) in select_alarm_obj" :key="_id" style="border-bottom: .5px solid black;">
                    {{`${alarm.equip_name}/${alarm.alarm_event}`}}
                    <button class="btn ms-auto" @click="removeAlarm(_id)"><i class="fas fa-trash"></i></button> 
                </div>
            </el-popover>
            <button type="button" class="btn btn-success" @click="$emit('choose-alarm-done', select_alarm_obj)">{{$t('確認')}}</button>
        </div>
        <div class="modal-body">
            <div class="d-flex mb-4 mt-2">
                <el-popover class="ms-auto" placement="bottom-start" trigger="click" width="fit-content">
                    <template #reference>
                        <el-button
                            size="default"
                            class="col-12 col-lg-3 col-xl-2 ms-lg-auto mt-2 mt-lg-0">
                            <i class="far fa-clock"></i>{{$t('時間篩選')}}
                        </el-button>
                    </template>
                    <time-range-picker @setDate="setDate"></time-range-picker>
                </el-popover>
            </div>
            <alarm-table :alarm-data="alarmData" 
            :current-page="current_page" :total-page="total_page"
            :alarm-tools-enable="false" @page-change="pageChange"
            :select-Enable="true" :hover-Enable="true"
            @row-click="alarm_choose" :select-alarm="select_alarm_obj"></alarm-table>
        </div>
    </div>
</template>

<script>
import alarmTable from "@/components/alarm/alarmTable.vue"
import TimeRangePicker from "@/components/datepicker/timeRangePicker.vue"
export default {
    name: 'Choose_alarm',
    components: {
        alarmTable,
        TimeRangePicker
    },
    props:{
        alarmInput: {
            type: Object
        },
        stationId: {
            type: String,
            required: true
        }
    },
    data(){
        return {
            alarmData: [
                // Example
                /* {
                    ID: "60bd86d4320c621ad8b6b420",
                    _id: "1_1",
                    alarm_event: "超過30分鐘串列電流差異過大",
                    alarm_group: "軟體",
                    alarm_place: "地面型-天權-UNIT-12-天權20",
                    checktime: "",
                    dispatchRecord: "",
                    equip_name: "sm11-4",
                    equip_type: "串電流錶",
                    level: 1,
                    returntime: "2022-01-16 16:00:00",
                    time: "2022-01-16 12:20:00"
                }, */
            ],
            current_page: 1,
            total_page: 1,
            date_selection: {},
            select_alarm_obj: {},
        }
    },
    methods:{
        alarm_get(){
            //use api alarm_get to obtain alarm
            this.axios.post('alarm_get', {
                time: this.date_selection,
                plant:{"all":false,"ID":[this.stationId],"col":['pv_lgroup']},
                alarm_type:"all",
                alarm_group:"all",
                equip_type:"all",
                page:this.current_page,
                filter: {'dispatch_ID': {'$exists': false}}
            }).then(data => {
                console.log(data.data.data)
                this.total_page = data.data.data.total_page
                this.alarmData = data.data.data.data
            })
        },
        pageChange(page){
            console.log('current page: ',page)
            this.current_page = page
            this.alarm_get() // to get alarm data again
        },
        setDate(data){
            this.date_selection = {
                mode:data.mode,
                start_date:data.date_list[0],
                end_date:data.date_list[1]
            }
            this.alarm_get()
        },
        alarm_choose(alarm){
            //console.log(alarm)
            if(alarm._id in this.select_alarm_obj){
                delete this.select_alarm_obj[alarm._id]
            }else{
                this.select_alarm_obj[alarm._id] = alarm
            }
        },
        removeAlarm(_id){
            delete this.select_alarm_obj[_id]
        }
    },
    mounted(){
        this.select_alarm_obj = this.alarmInput
        this.syncdata = window.setInterval(this.alarm_get, 5000)
    },
    unmounted(){
        window.clearInterval(this.syncdata)
    }
}
</script>