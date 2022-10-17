<template>
    <div>
        <div class="navbar navbar-expand-lg navbar-light mb-lg-2">
            <div class="w-100">
                <button class="w-100 d-lg-none btn btn-primary" type="button" data-bs-toggle="collapse" data-bs-target="#navbarNav" aria-controls="navbarNav" aria-expanded="false" aria-label="Toggle navigation" v-if="tab_datas.length>0">
                    {{button_value()}}
                </button>
                <!-- <div class="collapse navbar-collapse" id="navbarNav">
                    <ul class="navbar-nav w-100">
                        <li class="nav-item col-12 col-lg-2-4 text-center">
                            <a class="nav-link text-dark" :class="{'active': pageMode == 'overview'}" @click="changePageMode('overview')">{{$t('dispatch.tabs.overview')}}</a>
                        </li>
                        <li class="nav-item col-12 col-lg-2-4 text-center">
                            <a class="nav-link text-dark" :class="{'active': pageMode == 'schedule'}" @click="changePageMode('schedule')">{{$t('dispatch.tabs.schedule')}}</a>
                        </li>
                        <li class="nav-item col-12 col-lg-2-4 text-center">
                            <a class="nav-link text-dark d-flex align-items-center justify-content-center" :class="{'active': pageMode == 'wait_for_dispatch'}" @click="changePageMode('wait_for_dispatch')">
                                <div class="alert_round" v-if="alert_round.wait_for_dispatch"></div>
                                {{$t('dispatch.tabs.wait_for_dispatch')}}
                            </a>
                        </li>
                        <li class="nav-item col-12 col-lg-2-4 text-center">
                            <a class="nav-link text-dark d-flex align-items-center justify-content-center" :class="{'active': pageMode == 'review'}" @click="changePageMode('review')">
                                <div class="alert_round" v-if="alert_round.dispatch"></div>
                                {{$t('dispatch.tabs.review')}}
                            </a>
                        </li>
                        <li class="nav-item col-12 col-lg-2-4 text-center">
                            <a class="nav-link text-dark"  :class="{'active': pageMode == 'archive'}" @click="changePageMode('archive')">{{$t('dispatch.tabs.archive')}}</a>
                        </li>
                    </ul>
                </div> -->
                <div class="collapse navbar-collapse" id="navbarNav" v-if="tab_datas.length>0">
                    <ul class="navbar-nav w-100">
                        <li class="nav-item col-12 col-lg-2-4 text-center"
                        v-for="tab_data in tab_datas" :key="tab_data.value"
                        >
                            <a class="nav-link text-dark" :class="{'active': pageMode == tab_data.value, 'd-flex align-items-center justify-content-center': tab_data.value=='wait_for_dispatch' || tab_data.value=='review'}" @click="changePageMode(tab_data.value)">
                                <div class="alert_round" v-if="alert_round.wait_for_dispatch&&tab_data.value=='wait_for_dispatch'"></div>
                                <div class="alert_round" v-if="alert_round.dispatch&&tab_data.value=='review'"></div>
                                {{
                                    tab_data.name_i18n[$store.state.language] == undefined ?
                                    tab_data.name_i18n['zh-TW'] : tab_data.name_i18n[$store.state.language]
                                }}
                            </a>
                        </li>
                    </ul>
                </div>
            </div>
        </div>
        <div class="d-flex flex-wrap mb-2">
            <select-station class="d-none"
            @get-ID="plant_select"></select-station>
            <div class="col-12 col-lg-5 col-xl-4 col-xxl-3 mt-2 mt-lg-0" v-if="!['overview'].includes(pageMode)">
                <autocomplete @station-select="station_select" @clear="lgroup_ID = null" :preSelect="$store.state.user_data.pageType == 'taipower'"/>
            </div>
            <el-popover placement="bottom-start" trigger="click" :width="$store.state.user_data.pageType == 'taipower' ? '60vw' : 'fit-content'"
            v-if="!['overview', 'schedule'].includes(pageMode)">
                <template #reference>
                    <el-button
                        size="large"
                        class="col-12 col-lg-3 col-xl-2 ms-lg-auto mt-3 mt-lg-0">
                        <i class="far fa-clock"></i>{{$t('時間篩選')}}
                    </el-button>
                </template>
                <time-range-picker @setDate="setDate"></time-range-picker>
            </el-popover>
            

        </div>
        <transition mode="out-in" name="table_animation_to">
            <div :key="pageMode">
                <overview v-if="pageMode=='overview'" :station-id="lgroup_ID" :date-select="date_selection"></overview>
                <schedule v-if="pageMode=='schedule'" :station-id="lgroup_ID" :date-select="date_selection"></schedule>
                <wait-for-dispatch v-else-if="pageMode=='wait_for_dispatch'" :station-id="lgroup_ID" :date-select="date_selection"></wait-for-dispatch>
                <dispatch-page v-else-if="pageMode=='review'"></dispatch-page>
                <archive v-else-if="pageMode =='archive'" :station-id="lgroup_ID" :date-select="date_selection"></archive>
            </div>
        </transition>
    </div>
</template>
<script>
import selectStation from "@/components/station/selectStationSingleLgroup.vue"
import autocomplete from '../components/autocomplete/lgroup_only.vue'
import TimeRangePicker from "@/components/datepicker/timeRangePicker.vue"
import Overview from "@/components/dispatch/overview.vue"
import Schedule from "@/components/dispatch/schedule.vue"
import waitForDispatch from "@/components/dispatch/wait_for_dispatch.vue"
import dispatchPage from "@/components/dispatch/dispatch.vue"
import Archive from "@/components/dispatch/archive.vue"

export default {
    name: "Dispatch",
    components:{
        selectStation,
        Overview,
        Schedule,
        TimeRangePicker,
        waitForDispatch,
        dispatchPage,
        Archive,
        autocomplete
    },
    data(){
        return {
            pageMode: "",
            plant_search: "",
            lgroup_ID: null,
            date_selection: {},
            alert_round: {
                wait_for_dispatch: false,
                dispatch: false
            },
            tab_datas: [],
            li_length: 0,
        }
    },
    methods: {
        changePageMode(mode){
            this.pageMode = mode
        },
        station_select(item){
            this.lgroup_ID = item.ID
        },
        plant_select(val){
            if(val != null && val != undefined && val != ""){
                this.lgroup_ID = val
            }
        },
        setDate(data){
            this.date_selection = {
                mode:data.mode,
                start_date:data.date_list[0],
                end_date:data.date_list[1]
            }
        },
        get_alert_round(){
            this.axios.post('/get_disaptch_overview_count',{
                stage: 'wait_admin_confirm_date'
            }).then(data=>{
                if(data.data.data.dispatch_count > 0){
                    this.alert_round.wait_for_dispatch = true
                }else{
                    this.alert_round.wait_for_dispatch = false
                }
            })
            this.axios.post('/get_disaptch_overview_count',{
                stage: 'auto_reviewed_wait_for_manual'
            }).then(data=>{
                if(data.data.data.dispatch_count > 0){
                    this.alert_round.dispatch = true
                }else{
                    this.alert_round.dispatch = false
                }
            })
        },
        button_value(){
            let tab_data = this.tab_datas.find((value) => {
                return (value.value == this.pageMode)
            })
            return tab_data.name_i18n[this.$store.state.language] == undefined ?
            tab_data.name_i18n['zh-TW'] : tab_data.name_i18n[this.$store.state.language]
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
        this.get_alert_round()
        this.sync_data = window.setInterval(this.get_alert_round, 5000)
    },
    unmounted(){
        window.clearInterval(this.sync_data)  
    },
    beforeRouteLeave(to, from) {
        if(this.$store.state.prevent_leave_at_once){
            const answer = window.confirm('您尚未儲存')
            if (answer) {
                this.$store.commit("set_prevent_leave_at_once")
                return true
            } else {
                return false
            }
        }else{
            return true
        }
    },
    watch: {
        lgroup_ID(){
        }
    }
}
</script>
<style scoped>
.navbar-nav{
    border-radius: 5px;
}
.nav-link.active{
    background-color: var(--bs-warning);
    border-radius: 5px;
}
</style>