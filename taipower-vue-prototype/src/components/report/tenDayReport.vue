<template>
    <div>
        <div class="complete mb-3">
            <autocomplete @station-select="station_select" @search-select="search_select"
            class="col-12 col-lg-3" :preSelect="$store.state.user_data.pageType == 'taipower'"></autocomplete>
        </div>
        <time-range-picker class="mb-3" @setDate="setDate" />
        <report-tenday-table :reportTendayData="reportTendayData" :totalPage="total_page"
                             :currentPage="current_page" :pageType="pageType"
                             @page-change="pageChange"
        >
        </report-tenday-table>
    </div>
</template>



<script>
import autocomplete from "../autocomplete/lgroup_only.vue"
import timeRangePicker from "@/components/datepicker/timeRangePickerSimple.vue"
import reportTendayTable from "@/components/report/reportTendayTable.vue"

export default {
    name: "tenDayReport",
    components:{
        timeRangePicker,
        autocomplete,
        reportTendayTable
    },
    data(){
        return {
            date_selection:{},
            search:"",
            lgroup_select: {'ID': ""},
            device_id:"",
            reportTendayData: [],
            current_page: 1,
            total_page: 1,
            pageType: "",
            number_per_page: this.$store.state.user_data.pageType == 'taipower' ? 6 : 10
        }
    },
    methods:{
        setDate(date){
            this.date_selection = date
        },
        get_table_data(){
            let that = this
            this.axios.post('/get_report_tenday', {
                ID: this.lgroup_select["ID"],
                datepicker1: this.date_selection.date_list[0],
                datepicker2: this.date_selection.date_list[1],
                current_page: this.current_page,
                number_per_page: this.number_per_page
            })
            .then(response => {
                console.log(response.data.data.data)
                that.reportTendayData = response.data.data.data
                that.total_page = response.data.data.total_page
                that.pageType = response.data.data.pageType
            })
        },
        pageChange(page){
            console.log('current page: ',page)
            this.current_page = page
            this.get_table_data() // to get report data again
        },
        station_select(item){
            console.log(item)
            this.lgroup_select["ID"] = item["ID"]
        },
        
        search_select(item){
            console.log(item)
            this.search = item
        }
    },
    watch: {
        date_selection(){
            this.current_page = 1
            console.log(this.date_selection)
            this.get_table_data()
        },
        search(){
            if (this.search == ""){
                this.lgroup_select["ID"] = this.search
                this.current_page = 1
                this.get_table_data()
            }
            else {
                this.current_page = 1
                this.get_table_data()
            }
        },
    }
}
</script>