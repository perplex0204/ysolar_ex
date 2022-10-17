<template>
    <div>
        <div class="d-flex flex-wrap mb-2">
            <div class="col-9 col-lg-5 col-xl-4 col-xxl-3 mt-2 mt-lg-0 mb-lg-2"> 
                <el-select v-model="schedule_repeat" :placeholder="$t('dispatch.選擇排程')" size="large" class="w-100"
                @change="get_schedule_overview">
                    <el-option
                        :label="$t('dispatch.interval.all')"
                        value="all"
                    >
                    </el-option>
                    <el-option
                        :label="$t('dispatch.interval.none')"
                        value="none"
                    >
                    </el-option>
                    <el-option
                        :label="$t('dispatch.interval.temporary')"
                        value="temporary"
                        v-if="$store.state.user_data.pageType == 'SPS'"
                    >
                    </el-option>
                    <el-option
                        :label="$t('dispatch.interval.week')"
                        value="week"
                    >
                    </el-option>
                    <el-option
                        :label="$t('dispatch.interval.month')"
                        value="month"
                    >
                    </el-option>
                    <el-option
                        :label="$t('dispatch.interval.quarter')"
                        value="quarter"
                    >
                    </el-option>
                    <el-option
                        :label="$t('dispatch.interval.half_year')"
                        value="half_year"
                        v-if="$store.state.user_data.pageType == 'SPS'"
                    >
                    </el-option>
                    <el-option
                        :label="$t('dispatch.interval.year')"
                        value="year"
                    >
                    </el-option>
                </el-select>
            </div>
            <schedule-modal class="col-2 col-lg-3 col-xl-2 ms-auto mt-2 mt-lg-0" ref="schedule_modal"
            @reload-table="get_schedule_overview" :hideButton="$store.state.user_data.level == 3? false : true"></schedule-modal>
        </div>
        <schedule-table :table-data="scheduleData" :current-page="current_page" 
        :total-page="total_page" @row-dblclick="schedule_choose" @page-change="page_change"></schedule-table>
    </div>
</template>
<script>
import scheduleTable from "./schedule/schedule_table.vue"
import scheduleModal from "./schedule/schedule_modal.vue"
export default {
    name: "Schedule",
    components: {
        scheduleTable,
        scheduleModal
    },
    props: {
        stationId : {
            default: null
        },
        dateSelect: {
            type: Object,
            default: ()=>{
                return {}
            }
        }
    },
    data(){
        return {
            scheduleData: [],
            current_page: 1,
            total_page: 1,
            schedule_repeat: 'all',
        }
    },
    methods: {
        schedule_choose(d){
            //console.log(data)
            this.axios.post('/get_schedule_data', {
                ID: d._id
            }).then(data=>{
                this.$refs.schedule_modal.open_modal(data.data.data.schedule_data)
            })
        },
        get_schedule_overview(){
            this.axios.post('/get_schedule_overview', {
                ID: this.stationId,
                //time: this.dateSelect,
                page: this.current_page,
                schedule_repeat: this.schedule_repeat
            }).then(data=>{
                console.log(data.data.data)
                this.total_page = data.data.data.total_page
                this.scheduleData = data.data.data.schedule_list
            })
        },
        page_change(new_page){
            this.current_page = new_page
            this.get_schedule_overview()
        }
    },
    mounted(){
        if(this.dateSelect != {} && this.dateSelect != null && this.dateSelect != undefined){
            this.get_schedule_overview()
        }
    },
    watch: {
        stationId(){
            console.log(this.stationId)
            this.get_schedule_overview()
        },
        dateSelect(){
            this.get_schedule_overview()
        }
    }
}
</script>