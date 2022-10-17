<template>
    <div>
        <div class="navbar navbar-expand-lg navbar-light mb-2 ms-lg-2">
            <div class="w-100">
                <button class="w-100 d-lg-none btn btn-primary" type="button" data-bs-toggle="collapse" data-bs-target="#navbarNav" aria-controls="navbarNav" aria-expanded="false" aria-label="Toggle navigation" v-if="tab_datas.length>0">
                    {{button_value()}}
                </button>
                <!-- <div class="collapse navbar-collapse" id="navbarNav">
                    <ul class="navbar-nav col-12 col-lg-9">
                        <li class="nav-item col-12 col-lg-4 text-center">
                            <a class="nav-link text-dark" :class="{'active': pageMode == 'table'}" @click="changePageMode('table')">{{$t('alarm.tabs.table')}}</a>
                        </li>
                        <li class="nav-item col-12 col-lg-4 text-center">
                            <a class="nav-link text-dark" :class="{'active': pageMode == 'pieChart'}" @click="changePageMode('pieChart')">{{$t('alarm.tabs.pieChart')}}</a>
                        </li>
                        <li class="nav-item col-12 col-lg-4 text-center">
                            <a class="nav-link text-dark" :class="{'active': pageMode == 'sequenceDiagram'}" @click="changePageMode('sequenceDiagram')">{{$t('alarm.tabs.sequenceDiagram')}}</a>
                        </li>
                    </ul>
                </div> -->
                <div class="collapse navbar-collapse" id="navbarNav" v-if="tab_datas.length>0">
                    <ul class="navbar-nav col-12" :class="'col-lg-'+tab_datas.length*3">
                        <li class="nav-item col-12 text-center" :class="'col-lg-'+li_length"
                        v-for="tab_data in tab_datas" :key="tab_data.value"
                        >
                            <a class="nav-link text-dark" :class="{'active': pageMode == tab_data.value}" @click="changePageMode(tab_data.value)">
                                {{
                                    tab_data.name_i18n[$store.state.language] == undefined ?
                                    tab_data.name_i18n['zh-TW'] : tab_data.name_i18n[$store.state.language]
                                }}</a>
                        </li>
                    </ul>
                </div>
            </div>
        </div>
        <!-- 圓餅圖inverter選擇 -->
        <div class="d-flex mb-1 ms-lg-2 flex-wrap">
            <auto-complete @search-select="search_select" @station-select="station_select" class="col-12 col-lg-3 mb-2"
            :preSelect="$store.state.user_data.pageType == 'taipower'" ></auto-complete>
            <div class="col-12 col-lg-2 ms-lg-2" v-if="pageMode == 'pieChart'">
                <el-select v-model="value" size="large" :disabled="notgroup" class="col-12 col-lg-12" @change="getLabel">
                    <el-option
                        v-for="item in options"
                        :key="item.value"
                        :label="item.label == '案場總錶' ? $t(`option.${item.label}`) : item.label"
                        :value="item.value"
                    >
                    </el-option>
                </el-select>
            </div>
            <!--圓餅圖選擇設備/軟體-->
            <!-- <div class="col-12 col-lg-3 mt-2 mt-lg-0 ms-lg-2" v-if="pageMode == 'pieChart'">
                <el-select v-model="alarm_pie_value" size="large" class="col-12 col-lg-8">
                    <el-option
                        v-for="item in alarm_options"
                        :key="item.value"
                        :label="item.label"
                        :value="item.value"
                    >
                    </el-option>
                </el-select>
            </div> -->
            <!--table警報類型-->
            <div class="col-12 col-lg-4 mt-2 mt-lg-0 ms-lg-2" v-if="['table', 'diagnostic'].includes(pageMode)">
                <el-select v-model="alarm_value" size="large" class="col-12 col-lg-5">
                    <el-option
                        v-for="item in alarm_table_options"
                        :key="item.value"
                        :label="$t(`alarm.${item.label}`)"
                        :value="item.value"
                    >
                    </el-option>
                </el-select>
            </div>
            <!--table時間篩選-->
            <el-popover placement="bottom-start" trigger="click" :width="this.$store.state.isMobile? '95vw': this.$store.state.user_data.pageType == 'taipower' ? '60vw' : 'fit-content'"
            class="date_popover"
            style="max-width: 100vw; overflow-y: scroll;"
            v-if="['table', 'diagnostic'].includes(pageMode)">
                <template #reference>
                    <el-button
                        size="large"
                        class="col-12 col-lg-3 col-xl-2 ms-lg-auto mt-3 mt-lg-0 mb-2 mb-lg-0">
                        <i class="far fa-clock"></i>{{$t('時間篩選')}}
                    </el-button>
                </template>
                <time-range-picker @setDate="setDate"></time-range-picker>
            </el-popover>

            <!--圓餅圖時間篩選-->
            <el-popover placement="bottom-start" trigger="click" :width="this.$store.state.isMobile? '95vw': this.$store.state.user_data.pageType == 'taipower' ? '60vw' : 'fit-content'"
            class="date_popover"
            style="max-width: 100vw; overflow-y: scroll;"
            v-if="pageMode == 'pieChart'">
                <template #reference>
                    <el-button
                        size="large"
                        class="col-12 col-lg-3 col-xl-2 ms-lg-auto mt-3 mt-lg-0 mb-2 mb-lg-0">
                        <i class="far fa-clock"></i>{{$t('時間篩選')}}
                    </el-button>
                </template>
                <time-range-picker-simple @setDate="setDateSimple"></time-range-picker-simple>
            </el-popover>

            <!--時序圖時間篩選-->
            <el-popover placement="bottom-start" trigger="click" :width="this.$store.state.isMobile? '95vw': this.$store.state.user_data.pageType == 'taipower' ? '60vw' : 'fit-content'"
            class="date_popover"
            style="max-width: 100vw; overflow-y: scroll;"
            v-if="pageMode == 'sequenceDiagram'">
                <template #reference>
                    <el-button
                        size="large"
                        class="col-12 col-lg-3 col-xl-2 ms-lg-auto mt-3 mt-lg-0 mb-2 mb-lg-0">
                        <i class="far fa-clock"></i>{{$t('時間篩選')}}
                    </el-button>
                </template>
                <time-range-picker @setDate="setDate" :initial_mode="'week'" ></time-range-picker>
            </el-popover>
        </div>
        <transition mode="out-in" name="table_animation_to">
            <div class="ms-lg-2 mt-2 mb-2" :key="pageMode">
                <!-- <time-range-picker-simple v-if="pageMode == 'pieChart'" @setDate="setDateSimple"></time-range-picker-simple> -->
                <alarm-table v-if="pageMode == 'table'" :alarm-data="alarmData" 
                :current-page="current_page" :total-page="total_page" :type="'table'"
                @handle-alarm="handleAlarm" @page-change="pageChange" @row-dblclick="rowDblclick"
                @open-dispatch="open_dispatch"></alarm-table>

                <alarm-table v-if="pageMode == 'diagnostic'" :alarm-data="alarmDataEvent" 
                :current-page="current_page" :total-page="total_page" :type="'diagnostic'"
                @handle-alarm="handleAlarm" @page-change="pageChange" @row-dblclick="rowDblclick"
                @open-dispatch="open_dispatch"></alarm-table>

                <div class="card" v-if="pageMode == 'pieChart'">
                    <alarm-pie-chart :station="station" :date_selection="date_selection"
                    :alarm_option="alarm_pie_value" class="mt-2"
                    ></alarm-pie-chart>
                </div>
                <div class="card" v-if="pageMode == 'sequenceDiagram'">
                    <alarm-sequence-diagram :station="station" :date_selection="date_selection" :search="search"
                    ></alarm-sequence-diagram>
                </div>
            </div>
        </transition>
        <dispatch-page ref="dispatch_page" @reload-table="syncfunction"></dispatch-page>
    </div>
</template>

<script>
import alarmTable from "@/components/alarm/alarmTable.vue"
import TimeRangePicker from "@/components/datepicker/timeRangePicker.vue"
import TimeRangePickerSimple from "@/components/datepicker/timeRangePickerSimple.vue"
import autoComplete from '@/components/autocomplete/all_type.vue'
import alarmPieChart from '@/components/alarm/alarmPieChart.vue'
import alarmSequenceDiagram from '@/components/alarm/alarmSequenceDiagram.vue'
import dispatchPage from "@/components/dispatch_work/dispatch_page.vue"
import { ElMessage } from 'element-plus'

export default {
    name: 'Alarm',
    components: {
        alarmTable,
        TimeRangePicker,
        TimeRangePickerSimple,
        autoComplete,
        alarmPieChart,
        alarmSequenceDiagram,
        dispatchPage
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
            alarmDataEvent:[],
            current_page: 1,
            total_page: 1,
            date_selection: {},

            pageMode: "",
            station: {},
            value: "",
            options: [],
            notgroup: true,
            search: "",
            place_ID: "",
            // place_select: false,
            // isinverter: false,
            inverter_total_value: "",

            alarm_options: [
                {label: "全部警報", value: "all"},
                {label: "設備", value: "設備"},
                {label: "軟體", value: "軟體"},
                // {label: "日照計發電異常", value: "日照計數值異常"},
                // {label: "溫度計發電異常", value: "溫度計數值異常"},
                // {label: "設備斷線", value: "斷線"},
                // {label: "變流器內部警報", value: "內部警報"}
            ],
            alarm_all_options: [
                {label: "全部警報", value: "all"},
                {label: "變流器發電異常", value: "變流器發電異常"},
                {label: "串電流發電異常", value: "串電流異常"},
                {label: "日照計發電異常", value: "日照計數值異常"},
                {label: "溫度計發電異常", value: "溫度計數值異常"},
                {label: "設備斷線", value: "斷線"},
                {label: "變流器內部警報", value: "內部警報"}
            ],
            alarm_inv_options: [
                {label: "全部警報", value: "all"},
                {label: "設備", value: "設備"},
                {label: "軟體", value: "軟體"},
            ],
            alarm_value: "all",
            alarm_pie_value: "all",

            alarm_table_options: [
                {label: "全部警報", value: "all"},
                {label: "設備警報", value: "設備"},
                {label: "軟體警報", value: "軟體"},
            ],
            tab_datas: [],
            li_length: 0,
            documents_per_page: this.$store.state.user_data.pageType == 'taipower' ? 7 : 10
        }
    },
    methods:{
        changePageMode(mode){
            this.pageMode = mode
        },
        station_select(item) {
            if(item.name == '無資料'){
				return false
			}
            this.station = {
                ID_list: [item.ID],
                col_list: [item.collection]
            }
        },
        search_select(item) {
            this.search = item
        },
        get_group() {
            let that=this
            // console.log(this.search)
            if (this.search != "") {
                // console.log(this.station["ID_list"][0])
                this.axios.post('get_equip_select', {
                    ID: this.station["ID_list"][0],
                    collection: this.station["col_list"][0]
                }).then(data => {
                    // console.log(data.data.data.inv)
                    that.options_produce(this.station["ID_list"][0], data.data.data.inv)
                })
            }
        },
        options_produce(group_ID, invs) {
            if (this.search != "") {
                this.options = []
                this.value = group_ID
                this.inverter_total_value = group_ID
                this.options.push({
                    value: group_ID,
                    label: "案場總錶"
                })
                for (var i=0; i<invs.length; i++){
                    this.options.push({
                        value: invs[i]["ID"],
                        label: invs[i]["name"]
                    })
                }
                this.notgroup = false
            }
        },
        getLabel(val) {
            let obj = {}
            obj = this.options.find((item) => {
                return item.value == val
            })
            if (obj.label == "案場總錶") {
                this.alarm_options = this.alarm_all_options
            }
            else {
                this.alarm_options = this.alarm_inv_options
            }
            this.alarm_value = "all"
            this.alarm_pie_value = "all"
        },
        async alarm_get(){
            if (this.pageMode == 'table'){
                //use api alarm_get to obtain alarm
                this.axios.post('alarm_get', {
                    time: this.date_selection,
                    plant: Object.keys(this.station).length == 0 ? {"all":true,"ID":null,"col":null}:
                    {"all": false, "ID": this.station.ID_list, "col": this.station.col_list},
                    alarm_type:"all",
                    alarm_group:this.alarm_value,
                    equip_type:"all",
                    page:this.current_page,
                    documents_per_page: this.documents_per_page
                }).then(data => {
                    console.log(data.data.data)
                    this.total_page = data.data.data.total_page
                    this.alarmData = data.data.data.data
                })
            }
        },
        async alarm_get_event(){
            if (this.pageMode == 'diagnostic'){
                //use api alarm_get to obtain alarm
                this.axios.post('alarm_get_event', {
                    time: this.date_selection,
                    plant: Object.keys(this.station).length == 0 ? {"all":true,"ID":null,"col":null}:
                    {"all": false, "ID": this.station.ID_list, "col": this.station.col_list},
                    alarm_type:"all",
                    alarm_group:this.alarm_value,
                    equip_type:"all",
                    page:this.current_page,
                    documents_per_page: this.documents_per_page
                }).then(data => {
                    console.log(data.data.data)
                    this.total_page = data.data.data.total_page
                    this.alarmDataEvent = data.data.data.data
                })
            }
        },
        handleAlarm(_id, type){
            //console.log(_id, type)
            this.axios.post('/alarm_tools', {
                ID: _id,
                mode: type
            }).then(data=>{
                ElMessage.success(this.$i18n.t('成功'))
                this.syncfunction()
            }).catch(err=>{
                ElMessage.error(this.$i18n.t('錯誤'))
            })
        },
        pageChange(page){
            console.log('current page: ',page)
            this.current_page = page
            this.syncfunction() // to get alarm data again
        },
        setDate(data){
            this.date_selection = {
                mode:data.mode,
                start_date:data.date_list[0],
                end_date:data.date_list[1]
            }
            this.syncfunction()
        },
        setDateSimple(data){
            // console.log(data)
            this.date_selection = {
                start_date:data.date_list[0],
                end_date:data.date_list[1],
                mode:data.mode
            }
        },

        rowDblclick(alarm){
            console.log("dblclick alarm:",alarm)
            if(alarm.about != null && alarm.about != "" && alarm.about != "斷線"){
                let that = this
                this.axios.post('/equip_ID_get_group_data',{
                    ID:alarm.ID
                }).then(function(data){
                    console.log(data.data.data)
                    var time1 = alarm.time.split(" ")[0]
                    var time2 = alarm.returntime
                    if(time2 == ""){
                        var today = new Date()
                        time2 = `${today.getFullYear()}-${today.getMonth()+1}-${today.getDate()}`
                    }
                    else{
                        time2 = time2.split(" ")[0]
                    }
                    var response = data.data.data
                    if(response.ID != undefined && response.ID != null && response.collection != undefined && response.collection != null){
                        var url = "/stationData?"
                        url += `ID=${response.ID}&collection=${response.collection}&pageMode=equipment`
                        url += `&equip_ID=${alarm.ID}&datatype=${alarm.about}`
                        url += `&datepicker1=${time1}&datepicker2=${time2}`
                        console.log(url)
                        that.$router.push(url)
                    }
                })
            }
        },
        open_dispatch(alarm){
            this.axios.post('/get_dispatch_data', {ID: alarm.dispatch_ID}).then(data => {
                this.$refs.dispatch_page.dispatchData = data.data.data.dispatch_data
                this.$refs.dispatch_page.modalControl = {
                    title: this.$i18n.t("dispatch.工單編輯"),
                    editable: true,
                    level: this.$store.state.user_data.level,
                }
                this.$refs.dispatch_page.openModal()
            })
        },
        button_value(){
            let tab_data = this.tab_datas.find((value) => {
                return (value.value == this.pageMode)
            })
            return tab_data.name_i18n[this.$store.state.language] == undefined ?
            tab_data.name_i18n['zh-TW'] : tab_data.name_i18n[this.$store.state.language]
        },
        syncfunction(){
            if (this.pageMode=="table"){
                this.alarm_get()
            }
            else if (this.pageMode=="diagnostic"){
                this.alarm_get_event()
            }
        }
    },
    beforeMount(){
        console.log(this.$route)
        let that = this
        this.axios.post('get_tab_data', {"path": this.$route.path})
        .then(data => {
            console.log(data.data.data.data)
            that.tab_datas = data.data.data.data
            if(that.tab_datas.length>0){
                that.li_length = 12/that.tab_datas.length
                that.pageMode = that.tab_datas[0].value
            }
        })
    },
    mounted(){
        this.syncdata = window.setInterval(this.syncfunction, 5000)
    },
    unmounted(){
        window.clearInterval(this.syncdata)
    },
    watch: {
        search() {
            // console.log(this.station)
            this.inverter_total_value = ""
            console.log(this.value)
            if (this.search != ""){
                if (this.station.col_list[0] == "pv_group"){
                    this.get_group()
                }
                else{
                    this.place_ID = this.station["ID_list"][0]
                    this.alarm_options = this.alarm_all_options
                    this.alarm_value = "all"
                    this.alarm_pie_value = "all"
                    // this.place_select = true
                    this.notgroup = true
                }
            }
            else if (this.search == "") {
                this.place_ID = ""
                this.value = ""
                this.subplace = ""
                this.notgroup = true
                // this.place_select = false
                this.alarm_options = this.alarm_all_options
                this.alarm_value = "all"
                this.alarm_pie_value = "all"
                this.station = {}
                this.syncfunction()
            }
            console.log(this.station)
        },
        value() {
            // console.log(this.value)
            // this.place_select = true
            if (this.search == "") {
                this.place_ID = ""
                this.station = {}
            }
            else {
                this.place_ID = this.value
                this.station["ID_list"] = [this.value]
                if(this.station["ID_list"][0] != this.inverter_total_value){
                    this.station["col_list"] = ["equipment"]
                }
                else{
                    this.station["col_list"] = ["pv_group"]
                }
            }
            // console.log(this.station)
        },
        alarm_value(){
            this.syncfunction()
        },
        station() {
            console.log(this.station)
           if(["table", "diagnostic"].includes(this.pageMode)){
                this.current_page=1
                this.syncfunction()
            }
        },
        pageMode(){
            if(["table", "diagnostic"].includes(this.pageMode)){
                this.current_page=1
                this.syncfunction()
            }
        }
    }
}
</script>