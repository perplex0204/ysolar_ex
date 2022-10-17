<template>
    <div>
        <div class="d-flex flex-wrap mb-2 mt-2">
            <div class="col-12 col-lg-3 col-xl-2 mt-2 mt-lg-0" v-if="tableType == 'no_require'">
                <el-select size="large" v-model="stage_select" @change="get_dispatch_overview">
                    <el-option value="all" selected :label="$t('全部')" />
                    <el-option value="wait_for_take" :label="$t('dispatch.stage.wait_for_take')" />
                    <el-option value="took_wait_date_enter" :label="$t('dispatch.stage.took_wait_date_enter')" />
                    <el-option value="wait_for_dispatch" :label="$t('dispatch.stage.wait_for_dispatch')" />
                </el-select>
            </div>
            <create-dispatch-modal class="col-2 col-lg-3 col-xl-2 ms-auto mt-2 mt-lg-0"
            @reload-table="get_dispatch_overview" :hideButton="$store.state.user_data.level == 3? false : true"></create-dispatch-modal>
        </div>
        <div class="table_tab_container mt-3" v-if="$store.state.user_data.pageType != 'SPS'"> <!-- Hide SPS -->
            <button class="table_tab col-4 col-lg-2 p-2" :class="{'active': tableType == 'require_confirm'}" @click="set_tableType('require_confirm')">
                <div class="alert_round skew" v-if="alert_round"></div><label>{{$t('dispatch.待處理工單')}}</label>
            </button>
            <button class="table_tab col-4 col-lg-2 p-2" style="position: relatvie; left: -25px;"  :class="{'active': tableType == 'no_require'}" @click="set_tableType('no_require')">
                <label>{{$t('dispatch.待出工派工')}}</label>
            </button>
            <button class="table_tab col-4 col-lg-2 p-2" style="position: relatvie; left: -25px;"  :class="{'active': tableType == 'not_meet_priority'}" @click="set_tableType('not_meet_priority')"
            v-if="$store.state.user_data.pageType == 'taipower'">
                <label>{{$t('dispatch.未符合優先度派工')}}</label>
            </button>
        </div>
        <dispatch-table :table-data="scheduleData" :current-page="current_page" 
        @page-change="page_change" :mode="tableType"
        :total-page="total_page" @row-click="dispatch_choose"></dispatch-table>
        <dispatch-page ref="dispatch_page" @reload-table="get_dispatch_overview"></dispatch-page>
    </div>
</template>
<script>
import dispatchTable from "./wait_for_dispatch/dispatch_table.vue"
import createDispatchModal from "./wait_for_dispatch/create_dispatch_modal.vue"
import dispatchPage from "../dispatch_work/dispatch_page.vue"
import { ElNotification} from 'element-plus'

export default {
    name: "Wait_for_dispatch",
    components: {
        dispatchTable,
        createDispatchModal,
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
            scheduleData: [
            ],
            current_page: 1,
            total_page: 1,
            tableType: this.$store.state.user_data.pageType == 'SPS' ?  'no_require' : 'require_confirm',
            alert_round: false,
            stage_select: 'all',
        }
    },
    methods: {
        dispatch_choose(dispatch_data){
            this.axios.post("/get_dispatch_data", {ID: dispatch_data._id}).then(data=>{
                this.$refs.dispatch_page.dispatchData = data.data.data.dispatch_data
                this.$refs.dispatch_page.modalControl = {
                    title: this.$i18n.t('dispatch.編輯工單'),
                    editable: true,
                    level: this.$store.state.user_data.level,
                }
                this.$refs.dispatch_page.openModal()
            })
        },
        get_dispatch_overview(){
            // determine table tab alert round
            this.axios.post('/get_disaptch_overview_count',{
                stage: 'wait_admin_confirm_date'
            }).then(data=>{
                if(data.data.data.dispatch_count > 0){
                    this.alert_round = true
                }else{
                    this.alert_round = false
                }
            })
            this.axios.post('/get_dispatch_overview',{
                ID: this.stationId,
                page: this.current_page,
                dispatch_time: this.dateSelect,
                stage: this.tableType == 'require_confirm'?'wait_admin_confirm_date':
                this.tableType == 'not_meet_priority'?  'wait_for_priority': 
                this.stage_select == 'all'? ['wait_for_dispatch',
                'wait_for_take', 'took_wait_date_enter'] : this.stage_select,
                sort: this.tableType == 'not_meet_priority'? {'predict_dispatch_cost': -1} : {'dispatch_time': -1}
            }).then(data=>{
                console.log(data.data.data)
                this.scheduleData = data.data.data.dispatch_list
                this.total_page = data.data.data.total_page
            })
        },
        set_tableType(new_type){
            this.tableType = new_type
            this.current_page = 1
            this.total_page = 1
            this.get_dispatch_overview()
            if(new_type == 'not_meet_priority'){
                ElNotification.info({
                    title: '未符合優先度派工',
                    message: this.$i18n.t('setting.dispatch.auto_dispatch_setting_info'),
                })
            }
        },
        page_change(new_page){
            this.current_page = new_page
            this.get_dispatch_overview()
        }
    },
    mounted(){
        this.get_dispatch_overview()
        this.syncdata = window.setInterval(this.get_dispatch_overview, 5000)
    },
    unmounted(){
        window.clearInterval(this.syncdata)
    },
    watch: {
        stationId(){
            this.get_dispatch_overview()
        },
        dateSelect(){
            this.get_dispatch_overview()
        }
    }
}
</script>