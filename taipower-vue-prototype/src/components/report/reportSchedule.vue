<template>
    <div>
        <!-- <div class="complete mb-2 col-12 col-lg-3">
            <autocomplete @station-select="station_seelct"></autocomplete>
        </div> -->
        <div :class="{'d-lg-flex': $store.state.user_data.pageType == 'taipower'}">
            <div class="complete mb-2 col-lg-3 me-lg-2" :class="{'mt-2': $store.state.user_data.pageType == 'taipower'}">
                <auto-complete @search-select="search_select" @station-select="station_select" :preSelect="$store.state.user_data.pageType == 'taipower'"
                ></auto-complete>
            </div>
            <div class="selection col-lg-3" :class="{'mt-2 me-lg-2': $store.state.user_data.pageType == 'taipower',
            'mb-2': $store.state.user_data.pageType != 'taipower'}">
                <el-select v-model="value" class="col-12 col-lg-12" size="large">
                    <el-option
                        v-for="item in options"
                        :key="item.value"
                        :label="$t(`report.${item.label}`)"
                        :value="item.value"
                    >
                    </el-option>
                </el-select>
            </div>
            <timeRangePickerSingle @setDate="setDate" v-if="$store.state.user_data.pageType == 'taipower'" 
            class="col-lg-6" />
        </div>

        <timeRangePickerSingle @setDate="setDate" v-if="$store.state.user_data.pageType != 'taipower'" />
        <report-schedule-table :reportScheduleData="reportScheduleData" :totalPage="total_page"
                               :time_interval="value" :currentPage="current_page"
                                @page-change="pageChange"
        >
        </report-schedule-table>
    </div>
</template>



<script>
import autoComplete from "../autocomplete/all_type.vue"
import TimeRangePickerSingle from "@/components/datepicker/timeRangePickerSingle.vue"
import reportScheduleTable from "@/components/report/reportScheduleTable.vue"

export default {
    name: "report",
    components:{
        TimeRangePickerSingle,
        reportScheduleTable,
        autoComplete
    },
    data(){
        return {
            date_selection:{},
            search:"",
            options:[
               {
                   value:"year",
                   label:"year"
               },
               {
                   value:"month",
                   label:"month"
               },
               {
                   value:"day",
                   label:"day"
               },
               {
                   value:"hour",
                   label:"hour"
               },
               {
                   value:"15min",
                   label:"15min"
               }
            ],
            value:"year",
            plant_select: {'ID_list': [""], 'col_list': [""]},
            device_id:"",
            reportScheduleData: [
                // {
                //     report_place: "上萬安段",
                //     time_interval: "day",
                //     date: "2022-01-16"
                // }
            ],
            current_page: 1,
            total_page: 1,
            number_per_page: this.$store.state.user_data.pageType == 'taipower' ? 8 : 10
        }
    },
    methods:{
        station_select(item) {
            if(item.name == '無資料'){
				return false
			}
            this.plant_select = {
                ID_list: [item.ID],
                col_list: [item.collection]
            }
        },
        search_select(item) {
            this.search = item
        },
        setDate(date){
            this.date_selection = date
        },
        get_table_data(){
            let that = this
            this.axios.post('/get_word_table_data', {
                ID: this.plant_select['ID_list'][0],
                datepicker1: this.date_selection.date_list[0],
                datepicker2: this.date_selection.date_list[1],
                time_interval: this.value,
                current_page: this.current_page,
                col: this.plant_select['col_list'][0],
                number_per_page: this.number_per_page
            })
            .then(response => {
                that.reportScheduleData = response.data.data
                that.total_page = response.data.total_page
            })
        },
        pageChange(page){
            console.log('current page: ',page)
            this.current_page = page
            this.get_table_data() // to get report data again
        },
    },
    watch: {
        date_selection(){
            this.current_page = 1
            this.get_table_data()
        },
        search(){
            if (this.search == ""){
                this.plant_select['ID_list'][0] = this.search
                this.plant_select["col_list"][0] = ""
                this.current_page = 1
                this.get_table_data()
            }
            // else {
            //     this.current_page = 1
            //     this.get_table_data()
            // }
        },
        value(){
            if (this.search == ""){
                this.plant_select['ID_list'][0] = this.search
                this.plant_select["col_list"][0] = ""
                this.current_page = 1
                this.get_table_data()
            }
            else {
                this.current_page = 1
                this.get_table_data()
            }
        },
        "plant_select.ID_list": function() {
            if (this.search != ""){
                this.current_page = 1
                this.get_table_data()
            }
        }
    }
}
</script>
