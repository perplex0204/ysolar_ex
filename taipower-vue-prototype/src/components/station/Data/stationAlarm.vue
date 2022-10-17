<template>
    <div class="mt-2 mt-lg-4">
        <div class="d-flex flex-wrap">
            <div class="col-12 col-lg-2 mt-2 mt-lg-0 ms-lg-5 mb-2 mb-lg-0">
                <el-select v-model="alarm_value" size="large" class="col-12 col-lg-12">
                    <el-option
                        v-for="item in alarm_table_options"
                        :key="item.value"
                        :label="$t(`alarm.${item.label}`)"
                        :value="item.value"
                    >
                    </el-option>
                </el-select>
            </div>

            <el-popover placement="bottom-start" trigger="click" :width="this.$store.state.isMobile? '95vw': $store.state.user_data.pageType == 'taipower' ? '60vw' : 'fit-content'"
            class="date_popover"
            style="max-width: 100vw; overflow-y: scroll;"
            >
                <template #reference>
                    <el-button
                        size="large"
                        class="col-12 col-lg-3 col-xl-2 ms-lg-auto mt-2 mt-lg-0 me-lg-5">
                        <i class="far fa-clock"></i>{{$t('時間篩選')}}
                    </el-button>
                </template>
                <time-range-picker @setDate="setDate"></time-range-picker>
            </el-popover>
        </div>

        <div class="col-11 ms-3 ms-lg-5">
            <alarm-table :alarm-data="alarmData" 
            :current-page="current_page" :total-page="total_page"
            @handle-alarm="handleAlarm" @page-change="pageChange"
            class="mt-4"></alarm-table>
        </div>
    </div>
</template>




<script>
import TimeRangePicker from "@/components/datepicker/timeRangePicker.vue"
import alarmTable from "@/components/alarm/alarmTable.vue"
export default {
    name: "stationAlarm",
    components: {
        TimeRangePicker,
        alarmTable
    },
    props: {
        stationData: {
            type: Object,
            required: true
        },
    },
    data() {
        return {
            alarmData: [],
            current_page: 1,
            total_page: 1,
            date_selection: {},
            station: {},

            alarm_table_options: [
                {label: "全部警報", value: "all"},
                {label: "設備警報", value: "設備"},
                {label: "軟體警報", value: "軟體"},
            ],
            alarm_value: "all"
        }
    },
    methods: {
        alarm_get(){
            if(Object.keys(this.station).length > 0){
                //use api alarm_get to obtain alarm
                this.axios.post('alarm_get', {
                    time: this.date_selection,
                    plant: {"all": false, "ID": this.station.ID_list, "col": this.station.col_list},
                    alarm_type:"all",
                    alarm_group:this.alarm_value,
                    equip_type:"all",
                    page:this.current_page
                }).then(data => {
                    console.log(data.data.data)
                    this.total_page = data.data.data.total_page
                    this.alarmData = data.data.data.data
                })
            }
            
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
        handleAlarm(_id, type){
            console.log(_id, type)
            // you can use api alarm_tools
        },
    },
    mounted(){
        // console.log(this.stationData)
        this.station = {
            ID_list: [this.stationData.ID],
            col_list: [this.stationData.collection]
        }
        console.log(this.station)
        this.alarm_get()
        this.syncdata = window.setInterval(this.alarm_get, 5000)
    },
    unmounted(){
        window.clearInterval(this.syncdata)
    },
    watch: {
        alarm_value(){
            this.alarm_get()
        }
    }
}
</script>