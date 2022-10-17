<template>
    <div class="mt-2 mt-lg-4">
        <div class="d-flex flex-wrap">
            <div class="col-12 col-lg-2 mt-2 mt-lg-0 ms-lg-5 mb-2 mb-lg-0">
                <el-select v-model="value" class="col-12 col-lg-10" size="large">
                    <el-option
                        v-for="item in options"
                        :key="item.value"
                        :label="$t(`report.${item.label}`)"
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
                    <time-range-picker-single @setDate="setDate"></time-range-picker-single>
            </el-popover>
        </div>

        <div class="col-11 ms-3 ms-lg-5">
            <report-schedule-table :reportScheduleData="reportScheduleData" :totalPage="total_page"
                                :time_interval="value" :currentPage="current_page"
                                @page-change="pageChange" class="mt-4"
            >
            </report-schedule-table>
        </div>
    </div>
</template>




<script>
import TimeRangePickerSingle from "@/components/datepicker/timeRangePickerSingle.vue"
import reportScheduleTable from "@/components/report/reportScheduleTable.vue"
export default {
    name: "stationReport",
    components: {
        TimeRangePickerSingle,
        reportScheduleTable
    },
    props: {
        stationData: {
            type: Object,
            required: true
        },
    },
    data() {
        return {
            date_selection:{},
            value:"day",
            current_page: 1,
            total_page: 1,
            reportScheduleData: [
                //example
                // {
                //     report_place: "上萬安段",
                //     time_interval: "day",
                //     date: "2022-01-16"
                // }
            ],
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
        }
    },
    methods: {
        setDate(date){
            this.date_selection = date
        },
        get_table_data(){
            let that = this
            this.axios.post('/get_word_table_data', {
                ID: this.stationData.ID,
                datepicker1: this.date_selection.date_list[0],
                datepicker2: this.date_selection.date_list[1],
                time_interval: this.value,
                current_page: this.current_page,
                col: this.stationData.collection
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
    mounted() {
        console.log(this.stationData)
    },
    watch: {
        date_selection(){
            console.log(this.date_selection)
            this.current_page = 1
            this.get_table_data()
        },
        value(){
            this.current_page = 1
            this.get_table_data()
        }
    }
}
</script>