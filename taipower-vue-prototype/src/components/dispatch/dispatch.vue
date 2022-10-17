<template>
    <div>
        <div class="table_tab_container mt-3">
            <button class="table_tab col-4 col-lg-2 p-2" :class="{'active': tableType == 'manual_review'}" @click="tableType = 'manual_review'">
                <div class="alert_round" v-if="alert_round"></div>
                <label v-if="$store.state.user_data.pageType == 'SPS'">{{$t('dispatch.待驗收')}}</label>
                <label v-else>{{$t('dispatch.需要手動驗收')}}</label>
            </button>
            <button class="table_tab col-4 col-lg-2 p-2" style="position: relatvie; left: -25px;"  :class="{'active': tableType == 'wait_for_ai_review'}" @click="tableType = 'wait_for_ai_review'"
            v-if="$store.state.user_data.pageType == 'taipower'">
                <label>{{$t('dispatch.等待自動驗收')}}</label>
            </button>
            <button class="table_tab col-4 col-lg-2 p-2" style="position: relatvie; left: -25px;"  :class="{'active': tableType == 'review_fail'}" @click="tableType = 'review_fail'">
                <div class="alert_round" v-if="alert_round_review_failed"></div><label>{{$t('dispatch.驗收退回')}}</label>
            </button>
        </div>
        <dispatch-table :table-data="tableData" :current-page="current_page" 
        :total-page="total_page" @row-click="dispatch_choose"></dispatch-table>
        <dispatch-page ref="dispatch_page" @reload-table="get_dispatch_overview"></dispatch-page>
    </div>
</template>
<script>
import dispatchTable from "./dispatch/dispatch_table.vue"
import dispatchPage from "../dispatch_work/dispatch_page.vue"

export default {
    name: "Dispatch",
    components: {
        dispatchTable,
        dispatchPage
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
            tableData: [
            ],
            current_page: 1,
            total_page: 1,
            tableType: "manual_review",
            alert_round: false,
            alert_round_review_failed: false
        }
    },
    methods: {
        get_dispatch_overview(){
            this.axios.post('/get_disaptch_overview_count',{
                ID: this.stationId,
                dispatch_time: this.dateSelect,
                stage: 'auto_reviewed_wait_for_manual'
            }).then(data=>{
                if(data.data.data.dispatch_count > 0){
                    this.alert_round = true
                }else{
                    this.alert_round = false
                }
            })
            this.axios.post('/get_disaptch_overview_count',{
                ID: this.stationId,
                dispatch_time: this.dateSelect,
                stage: 'review_failed'
            }).then(data=>{
                if(data.data.data.dispatch_count > 0){
                    this.alert_round_review_failed = true
                }else{
                    this.alert_round_review_failed = false
                }
            })
            this.axios.post('/get_dispatch_overview',{
                ID: this.stationId,
                dispatch_time: this.dateSelect,
                page: this.current_page,
                stage: this.tableType == "manual_review"?'auto_reviewed_wait_for_manual':
                this.tableType == 'wait_for_ai_review' ? ['dispatched_wait_for_review'] : 'review_failed'
            }).then(data=>{
                console.log(data.data.data)
                this.tableData = data.data.data.dispatch_list
                this.total_page = data.data.data.total_page
            })
        },
        dispatch_choose(dispatch_data){
            this.axios.post("/get_dispatch_data", {ID: dispatch_data._id}).then(data=>{
                this.$refs.dispatch_page.dispatchData = data.data.data.dispatch_data
                this.$refs.dispatch_page.modalControl = {
                    title: this.tableType == "manual_review"? this.$i18n.t('dispatch.手動驗收工單'):this.$i18n.t('dispatch.編輯工單'),
                    editable: true,
                    level: this.$store.state.user_data.level,
                }
                this.$refs.dispatch_page.openModal()
            })
        },
        page_change(new_page){
            this.current_page = new_page
            this.get_dispatch_overview()
        }
    },
    watch: {
        tableType(){
            this.get_dispatch_overview()
        },
        stationId(){
            this.get_dispatch_overview()
        },
        dateSelect(){
            this.get_dispatch_overview()
        }
    },
    mounted(){
        this.get_dispatch_overview()
        this.sync_data = window.setInterval(this.get_dispatch_overview, 5000)
    },
    unmounted(){
        window.clearInterval(this.sync_data)
    }
}
</script>