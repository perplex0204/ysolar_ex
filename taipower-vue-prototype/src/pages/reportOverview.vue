<template>
    <div :class="{'mt-4 col-lg-11 ms-auto me-auto': Object.keys(station_preSelect).length>0}">
        <div class="d-lg-flex mb-2">
            <div class="complete mb-3 col-12 col-lg-2 me-lg-3" v-if="Object.keys(station_preSelect).length==0 && typeSelected != 'week_report_A'">
                <autocomplete @station-select="station_select" @search-select="search_select"></autocomplete>
            </div>
            <div class="selection mb-3">
                <el-select v-model="typeSelected" class="col-12" size="large" :placeholder="$t(`option.${'請選擇'}`)">
                    <el-option
                        v-for="item in options"
                        :key="item.value"
                        :label="$t(`report.${item.label}`)"
                        :value="item.value"
                    >
                    </el-option>
                </el-select>
            </div>
            <button
                @click="createBill"
                v-if="typeSelected=='electricBill'"
                class="btn btn-primary mb-3 ms-lg-3 col-12 col-lg-2"
                size="small"
                :class="{'ms-lg-3': Object.keys(station_preSelect).length==0}"
                >{{$t("report.新增電費單")}}</button
            >
            <button
                @click="download_realtime_week_a_excel"
                v-if="typeSelected=='electricBill'"
                class="btn btn-success ms-lg-2 mb-3 mt-2 mt-lg-0 col-12 col-lg-2"
                v-loading="excel_preview_loading"
            >
                {{$t("report.下載週報表")}}
            </button>
            <el-popover placement="bottom-start" trigger="click" :width="this.$store.state.isMobile? '95vw':'fit-content'"
                class="date_popover"
                style="max-width: 100vw; overflow-y: scroll;"
                >
                    <template #reference>
                        <el-button
                            size="large"
                            class="col-12 col-lg-3 col-xl-2 ms-lg-auto mt-2 mt-lg-0">
                            <i class="far fa-clock"></i>{{$t('時間篩選')}}
                        </el-button>
                    </template>
                    <time-range-picker @setDate="setDate"></time-range-picker>
            </el-popover>
        </div>
        <report-view :reportData="reportData" :typeSelected="typeSelected" :isComponent="Object.keys(station_preSelect).length>0"
        :currentPage="current_page" :totalPage="total_report" @page-change="pageChange" ref="report"></report-view>

        <!-- Week A preview -->
        <div class="modal" ref="preview_modal">
            <div class="modal-dialog modal-xl modal-fullscreen-lg-down">
                <div class="modal-content">
                    <div class="modal-header">
                        <h5 class="modal-title">{{$t('預覽')}}</h5>
                        <button type="button" class="btn-close" @click="previewModal.hide()"></button>
                    </div>
                    <div class="modal-body">
                        <div class="table" v-html="excel_preview_html"></div>
                    </div>
                    <div class="modal-footer">
                        <button class="btn btn-success" @click="download_preview_docx">{{$t("report.download")}}</button>
                    </div>
                </div>
            </div>
        </div>
        
    </div>
</template>

<script>
import autocomplete from "@/components/autocomplete/all_type.vue"
import TimeRangePicker from "@/components/datepicker/timeRangePicker.vue"
import reportView from "@/components/report/reportView.vue"
import {Modal} from 'bootstrap'

export default {
    name: "reportOverview",
    components:{
        autocomplete,
        TimeRangePicker,
        reportView
    },
    props: {
        station_preSelect: {type: Object, default: function(){return {}}}
    },
    data() {
        return {
            date_selection:{},
            plant_select: {'ID_list': [], 'col_list': []},
            search: "",
            options:[
                {
                   value:"day_report",
                   label:"day_report"
               },
            //    {
            //        value:"week_report",
            //        label:"week_report"
            //    },
            //   {
            //        value:"week_report_A",
            //        label:"week_report_A"
            //   },
               {
                   value:"month_report",
                   label:"month_report"
               },
               {
                   value:"Tday_report",
                   label:"Tday_report"
               },
               {
                   value:"inverter_excel",
                   label:"inverter_excel"
               },
               {
                   value:"electricBill",
                   label:"electricBill"
               }
            ],
            typeSelected:"",
            reportData: [],
            current_page: 1,
            total_report: 0,
            timer : "",
            isShow: true,
            excel_preview_html: "",
            excel_preview_loading: false
        }
    },
    methods: {
        setDate(date){
            this.date_selection = date
        },
        station_select(item) {
			//console.log(item)
			if(item.name == '無資料'){
				return false
			}
            this.plant_select = {
                ID_list: [item.ID],
                col_list: [item.collection]
            }
		},
        search_select(item){
            this.search = item
        },
        search_bill(){
            this.reportData = []
            this.reportSelected = []
            if(this.typeSelected == ""){
                return false
            }
            console.log(this.plant_select)
            console.log(this.typeSelected)
            console.log(this.date_selection)
            let request_json = {
                page: this.current_page,
                time: { mode: this.date_selection.mode, start_date: this.date_selection.date_list[0],
                end_date: this.date_selection.date_list[1]},
                ID_list: this.plant_select.ID_list,
                col_list: this.plant_select.col_list,
            }
            switch(this.typeSelected){
                case "day_report":
                    this.report_get_day_report(request_json)
                    break
                case "Tday_report":
                    this.report_get_Tday(request_json)
                    break
                case "inverter_excel":
                    this.report_get_inverter(request_json)
                    break
                case "month_report":
                    this.report_get_month_report(request_json)
                    break
                case "week_report":
                    this.report_get_week_report(request_json)
                    break
                case "week_report_A":
                    this.report_get_week_report_A(request_json)
                    break
                case "electricBill":
                    this.report_get_electricBill(request_json)
                    break
                default:
                    break
            }
        },
        report_get_Tday(request_json){
            let that = this
            this.axios.post("/report_get_Tday", request_json).then(data => {
                console.log(data.data.data)
                that.total_report = data.data.data.total_page/1
                data.data.data.data.forEach(element => {
                    that.reportData.push({
                        reportType: '旬報表',
                        group: element.group,
                        date: element.time,
                        period: element.period,
                        filename: element.filename,
                        url: `solar_static/excel/${element.filename}`
                    })
                })
            })
        },
        report_get_inverter(request_json){
            let that = this
            this.axios.post("/report_get_inverter", request_json).then(data => {
                console.log(data.data.data)
                that.total_report = data.data.data.total_page
                data.data.data.data.forEach(element => {
                    that.reportData.push({
                        reportType: '變流器報表',
                        group: element.group,
                        date: element.time,
                        inverter: element.inverter,
                        filename: element.filename,
                        url: `solar_static/inverter_excel/${element.filename}`
                    })
                })
            })
        },
        report_get_week_report(request_json){
            let that = this
            this.axios.post("/report_get_week_report", request_json).then(data => {
                console.log(data.data.data)
                that.total_report = data.data.data.total_page
                data.data.data.data.forEach(element => {
                    that.reportData.push({
                        reportType: '週報表',
                        group: element.group,
                        date: element.time,
                        period: element.period,
                        filename: element.filename,
                        url: `solar_static/report_plot/${element.filename}`
                    })
                })
            })
        },
        report_get_month_report(request_json){
            let that = this
            this.axios.post("/report_get_month_report", request_json).then(data => {
                console.log(data.data.data)
                that.total_report = data.data.data.total_page
                data.data.data.data.forEach(element => {
                    that.reportData.push({
                        reportType: '月報表',
                        group: element.group,
                        date: element.time,
                        period: element.period,
                        filename: element.filename,
                        url: `solar_static/report_plot/${element.filename}`
                    })
                })
            })
        },
        report_get_week_report_A(request_json){   /* 週報表-A */
            let that = this
            this.axios.post("/report_get_week_report_A", request_json).then(data => {
                //console.log(data.data.data)
                that.total_report = data.data.data.total_page
                data.data.data.data.forEach(element => {
                    that.reportData.push({
                        reportType: '週報表-A',
                        date: element.time,
                        filename: element.filename,
                        url: `solar_static/week_report/${element.filename}`
                    })
                })
            })
        },
        report_get_electricBill(request_json){
            let that = this
            this.axios.post("/report_get_electricBill", request_json).then(data => {
                console.log(data.data.data)
                that.total_report = data.data.data.total_page
                data.data.data.data.forEach(element => {
                    that.reportData.push({
                        reportType: '電費單',
                        date: element.time,
                        filename: element.filename,
                        station_name: `${element.PV}/${element.lgroup}`,
                        PV: element.PV,
                        PV_ID: element.PV_ID,
                        ID: element.ID,
                        lgroup: element.lgroup,
                        month: 'starttime' in element? `${element.starttime}~${element.endtime}`: element.time,
                        _id: element._id,
                        upload_time: element.upload_time,
                        url: 'starttime' in element? `solar_static/uploadBill/${element.PV_ID}/${element.ID}/${element._id}/bill.pdf`: `solar_static/uploadBill/${element.PV_ID}/${element.ID}/${element.time}/bill.pdf`,
                        kwh: element.kwh,
                        cost: element.fee
                    })
                })
            })
        },
        report_get_day_report(request_json){
            console.log("test")
            let that = this
            this.reportData = []
            this.axios.post("/report_get_day_report", request_json).then(data => {
                console.log(data.data)
                that.total_report = data.data.data.total_page/1
                data.data.data.data.forEach(element => {
                    that.reportData.push({
                        reportType: '日報表',
                        group: element.group,
                        date: element.time,
                        period: element.period,
                        filename: element.filename,
                        url: `solar_static/report_plot/${element.filename}`
                    })
                })
            })
        },
        pageChange(page){
            console.log('current page: ',page)
            this.current_page = page
            this.search_bill() // to get report data again
        },
        createBill() {
            this.$refs.report.createBill()
        },
        closePop() {
            this.$refs.report.closePop()
        },
        download_realtime_week_a_excel(){
            this.excel_preview_loading = true
            fetch(`${this.axios.defaults.baseURL}/download_realtime_week_a_excel`)
            .then(response => response.blob())
            .then(async(res)=> {
                this.excel_blob = res
                let XLSX = require("xlsx")
                this.previewModal.show()
                let workbook = XLSX.read(await res.arrayBuffer(), { type: "array" })
                let worksheet = workbook.Sheets[workbook.SheetNames[0]]
                console.log(worksheet)
                this.excel_preview_html = XLSX.utils.sheet_to_html(worksheet)
                this.excel_preview_loading = false
            })
        },
        download_preview_docx(){
            window.location.href = `${this.axios.defaults.baseURL}/download_realtime_week_a_excel`
        }
    },
    watch: {
        "plant_select.ID_list": function(){
            this.current_page = 1
            this.search_bill()
        },
        date_selection(){
            this.current_page = 1
            this.search_bill()
        },
        typeSelected(){
            this.current_page = 1
            this.search_bill()
        },
        search(){
            if (this.search == ""){
                this.plant_select = {'ID_list': [], 'col_list': []}
                // this.search_bill()
            }
        }
    },
    mounted(){
        this.timer = setTimeout(() => {this.typeSelected = "day_report"}, 100)
        if(Object.keys(this.station_preSelect).length>0){
            this.plant_select = this.station_preSelect
        }
        this.previewModal = new Modal(this.$refs.preview_modal, {backdrop: 'static', keyboard: false})
    },
    beforeUnmount(){
        clearTimeout(this.timer)
    }
}
</script>