<template>
    <div>
        <div class="navbar navbar-expand-lg navbar-light mb-2">
            <div class="w-100">
                <button class="w-100 d-lg-none btn btn-primary" type="button" data-bs-toggle="collapse" data-bs-target="#navbarNav" aria-controls="navbarNav" aria-expanded="false" aria-label="Toggle navigation">
                    {{ {'overview': '總覽', take: '接單', schedule: '未出工工單', dispatch: '已出工工單', archive: '已結案工單' }[pageMode] }}
                </button>
                <div class="collapse navbar-collapse" id="navbarNav">
                    <ul class="navbar-nav w-100">
                        <li class="nav-item col-12 col-lg-2-4 text-center">
                            <a class="nav-link text-dark" :class="{'active': pageMode == 'overview'}" @click="changePageMode('overview')">{{$t('dispatch.tabs.overview')}}</a>
                        </li>
                        <li class="nav-item col-12 col-lg-2-4 text-center">
                            <a class="nav-link text-dark" :class="{'active': pageMode == 'take'}" @click="changePageMode('take')">{{$t('dispatch.tabs.take')}}</a>
                        </li>
                        <li class="nav-item col-12 col-lg-2-4 text-center">
                            <a class="nav-link text-dark" :class="{'active': pageMode == 'schedule'}" @click="changePageMode('schedule')">{{$t('dispatch.tabs.wait_for_dispatch')}}</a>
                        </li>
                        <li class="nav-item col-12 col-lg-2-4 text-center">
                            <a class="nav-link text-dark" :class="{'active': pageMode == 'dispatch'}" @click="changePageMode('dispatch')">{{$t('dispatch.tabs.review')}}</a>
                        </li>
                        <li class="nav-item col-12 col-lg-2-4 text-center">
                            <a class="nav-link text-dark"  :class="{'active': pageMode == 'archive'}" @click="changePageMode('archive')">{{$t('dispatch.tabs.archive')}}</a>
                        </li>
                    </ul>
                </div>
            </div>
        </div>
        <div class="d-flex flex-wrap mb-2">
            <select-station class="d-none d-lg-block" v-if="false"></select-station>
            <div class="col-12 col-lg-5 col-xl-4 col-xxl-3 ms-lg-2 mt-2 mt-lg-0">
                <autocomplete @station-select="station_select" @clear="lgroup_ID = null" />
            </div>
            <el-popover placement="bottom-start" trigger="click" width="fit-content" v-if="pageMode != 'overview'">
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

        <transition mode="out-in" name="table_animation_to">
            <div :key="pageMode">
                <overview v-if="pageMode == 'overview'" :station-id="lgroup_ID" :date-select="date_selection"></overview>
                <take v-if="pageMode == 'take'" :station-id="lgroup_ID" :date-select="date_selection"></take>
                <schedule v-if="pageMode == 'schedule'" :station-id="lgroup_ID" :date-select="date_selection"></schedule>
                <dispatch v-if="pageMode == 'dispatch'" :station-id="lgroup_ID" :date-select="date_selection"></dispatch>
                <archive v-if="pageMode == 'archive'" :station-id="lgroup_ID" :date-select="date_selection"></archive>
            </div>
        </transition>
    </div>
</template>
<script>
import selectStation from "@/components/station/selectStationSingleLgroup.vue"
import autocomplete from '../components/autocomplete/lgroup_only.vue'
import TimeRangePicker from "@/components/datepicker/timeRangePicker.vue"
import Overview from "@/components/dispatch_work/overview.vue"
import Take from "@/components/dispatch_work/take.vue"
import Schedule from "@/components/dispatch_work/schedule.vue"
import Dispatch from "@/components/dispatch_work/dispatch.vue"
import Archive from "@/components/dispatch_work/archive.vue"

export default {
    name: "Dispatch_work",
    components:{
        selectStation,
        autocomplete,
        TimeRangePicker,
        Overview,
        Take,
        Schedule, 
        Dispatch,
        Archive
    },
    data(){
        return {
            pageMode: "overview",
            plant_search: "",
            lgroup_ID: null,
            date_selection: {}
        }
    },
    methods: {
        changePageMode(mode){
            this.pageMode = mode
        },
        station_select(item){
            this.lgroup_ID = item.ID
        },
        setDate(data){
            this.date_selection = {
                mode:data.mode,
                start_date:data.date_list[0],
                end_date:data.date_list[1]
            }
        },
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
    }
}
</script>
<style>
.navbar-nav{
    border-radius: 5px;
    background-color: rgb(235, 241, 255) !important;
}
.nav-link.active{
    background-color: var(--bs-warning);
    border-radius: 5px;
}
</style>