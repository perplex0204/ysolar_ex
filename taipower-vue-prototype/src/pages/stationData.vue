<template>
    <div class="p-1">
        <div >
            <div class="container p-0">
                <div class="card col-12">
                    <div class="row g-0">
                        <div class="col-12 col-md-4">
                            <el-image class="card border-0 h-100" :src="card_overview.imgsrc" style="max-height: 250px;" :fit="'cover'"
                            :preview-src-list="[card_overview.imgsrc]">
                                <template #error>
                                    <div class="d-flex h-100 w-100 justify-content-center align-items-center fs-3 p-4">
                                        <i class="fa-solid fa-image"></i>
                                    </div>
                                </template>
                            </el-image>
                        </div>
                        <div class="col-12 col-md-8">
                            <div class="card-body">
                                <div class="d-flex flex-wrap align-items-center">
                                    <!-- 案場名稱 -->
                                    <h3 class="card-title">
                                        {{
                                            card_overview.type == 'PV'? card_overview.name : 
                                            card_overview.type == 'pv_lgroup' ? `${card_overview.PV}/${card_overview.name}` :
                                            `${card_overview.PV}/${card_overview.lgroup}/${card_overview.name}`
                                        }}
                                    </h3>
                                    <el-popover
                                        v-if="$store.state.user_data.is_superuser"
                                        placement="top-start"
                                        :width="200"
                                        trigger="hover"
                                        :content="`${card_overview.ID}`"
                                    >
                                        <template #reference>
                                            <button class="btn d-inline-block"><i class="fa-solid fa-circle-info"></i></button>
                                        </template>
                                    </el-popover>
                                    <div class="d-flex ms-auto text-success align-items-center" v-if="card_overview.led_state < 1 || card_overview.led_state > 3">
                                        <i class="fas fa-check-circle card-title"></i>
                                        <h6 class="card-title">{{$t('level.0')}}</h6>
                                    </div>
                                    <div class="d-flex ms-auto align-items-center" v-else
                                        :class="{'text-danger': card_overview.led_state == 1,
                                            'text-warning': card_overview.led_state == 2,
                                            'text-secondary': card_overview.led_state == 3
                                        }"
                                    >
                                        <i class="fas fa-exclamation-triangle card-title"></i>
                                        <h6 class="card-title" v-if="card_overview.led_state == 1">{{$t('level.1')}}</h6>
                                        <h6 class="card-title" v-else-if="card_overview.led_state == 2">{{$t('level.2')}}</h6>
                                        <h6 class="card-title" v-else-if="card_overview.led_state == 3">{{$t('level.3')}}</h6>
                                    </div>
                                </div>
                                <div class="row ms-1 ">
                                    <div class="col-lg-5 col-md-4 col-sm-3 col-12 ps-0 fs-6 align-items-end ">
                                        <i class="fas fa-database fs-4"></i><i class="fas fa-bolt fs-6"></i>
                                        <span style="font-size: 0.25rem;">&nbsp; &nbsp; &nbsp; &nbsp; &nbsp;</span>
                                        <span>{{$t('案場容量')}}</span>
                                    </div>
                                    <div class="d-flex col-xxl-3 col-xl-4 col-lg-7 col-md-8 col-sm-9 col-12 fs-6 ps-0 justify-content-center align-items-end">
                                        <label class="fs-5 fw-bold">{{card_overview.capacity}}</label>
                                        <label class="fs-7">kW</label>
                                    </div>
                                </div>
                                <div class="row ms-1 ">
                                    <div class="col-lg-5 col-md-4 col-sm-3 col-12 ps-0 fs-6 align-items-end ">
                                        <i class="fas fa-charging-station fs-4"></i><span style="font-size: 0.25rem; color: green;">Day &nbsp; &nbsp;</span>
                                        <span>{{$t('本日發電量')}}</span>
                                    </div>
                                    <div class="d-flex col-xxl-3 col-xl-4 col-lg-7 col-md-8 col-sm-9 col-12 fs-6 ps-0 justify-content-center align-items-end">
                                        <label class="fs-5 fw-bold">{{card_overview.today_kwh}}</label>
                                        <label class="fs-7">kWh</label>
                                    </div>
                                </div>
                                <div class="row ms-1 ">
                                    <div class="col-lg-5 col-md-4 col-sm-3 col-12 ps-0 fs-6 align-items-end ">
                                        <i class="fas fa-charging-station fs-4"></i><span style="font-size: 0.25rem; color: orange;">Month</span>
                                        <span>{{$t('本月發電量')}}</span>
                                    </div>
                                    <div class="d-flex col-xxl-3 col-xl-4 col-lg-7 col-md-8 col-sm-9 col-12 fs-6 ps-0 justify-content-center align-items-end">
                                        <label class="fs-5 fw-bold">{{card_overview.month_kwh}}</label>
                                        <label class="fs-7">kWh</label>
                                    </div>
                                </div>
                                <div class="row ms-1 ">
                                    <div class="col-lg-5 col-md-4 col-sm-3 col-12 ps-0 fs-6 align-items-end ">
                                        <i class="fas fa-charging-station fs-4"></i><span style="font-size: 0.25rem; color: red;">Year &nbsp; &nbsp;</span>
                                        <span>{{$t('本年發電量')}}</span>
                                    </div>
                                    <div class="d-flex col-xxl-3 col-xl-4 col-lg-7 col-md-8 col-sm-9 col-12 fs-6 ps-0 justify-content-center align-items-end">
                                        <label class="fs-5 fw-bold">{{card_overview.year_kwh}}</label>
                                        <label class="fs-7">kWh</label>
                                    </div>
                                </div>
                                
                                <!-- <p class="card-text"><small class="text-muted">Last updated 3 mins ago</small></p> -->
                            </div>
                        </div>
                    </div>
                    <div class="navbar navbar-expand-lg navbar-light pb-0">
                        <div class="w-100">
                            <button class="w-100 d-lg-none btn btn-primary" type="button" data-bs-toggle="collapse" data-bs-target="#navbarNav" aria-controls="navbarNav" aria-expanded="false" aria-label="Toggle navigation">
                                {{$t(`stationData.tabs.${pageMode}`)}}
                            </button>
                            <div class="collapse navbar-collapse" id="navbarNav">
                                <!-- 如果有 constrain  則collection 在constrain中的才會顯示 -->
                                <ul class="navbar-nav col-12 col-lg-12 bg-transparent text-main">
                                    <li class="nav-item col-12 col-lg-2" v-for="tab in tabs_first_data" :key="tab.value" v-show="(!(no_equip && $store.state.user_data.pageType == 'taipower' && tab.value=='equipment'))">
                                        <a class="nav-link h-100 d-flex align-items-center justify-content-center" :class="{'active': pageMode == tab.value}" @click="pageMode=tab.value; tab_reset_timestamp=Date.now()" v-show="!no_equip && $store.state.user_data.pageType == 'taipower' && tab.value=='equipment'">{{tab.name_i18n[$store.state.language]}}</a>
                                    </li>
                                    <!-- More -->
                                    <li class="nav-item col-12 col-lg-2" v-if="tabs.length>5">
                                        <a class="nav-item w-100 h-100 d-flex align-items-center justify-content-center">
                                            <el-popover
                                                placement="bottom"
                                                :width="$store.state.isMobile? '90%' : 200"
                                                trigger="click"
                                                class="p-0"
                                                popper-class="p-0"
                                            >
                                                <template #reference>
                                                    <div class="nav-link w-100 text-center" :class="{'active': tabs_second_data.filter(t=> t.value == pageMode).length > 0 }">
                                                        <i class="fa-solid fa-ellipsis"></i>
                                                    </div>
                                                </template>
                                                <div class="d-flex flex-column align-items-center" v-for="tab_data in tabs_second_data" :key="tab_data.value"
                                                v-show="(!(no_equip && $store.state.user_data.pageType == 'taipower' && tab_data.value=='equipment'))">
                                                    <button class="btn w-100 p-3" @click="pageMode = tab_data.value"
                                                    :class="{'bg-warning': pageMode == tab_data.value, 'text-dark': pageMode == tab_data.value}">
                                                        {{
                                                            tab_data.name_i18n[$store.state.language] == undefined ?
                                                            tab_data.name_i18n['zh-TW'] : tab_data.name_i18n[$store.state.language]
                                                        }}
                                                    </button>
                                                </div>
                                            </el-popover>
                                        </a>
                                    </li>
                                </ul>
                            </div>
                        </div>
                    </div>
                </div>
                <div class="card w-100" style="min-height: 500px;">
                    <transition name="fade" mode="out-in">
                        <div :key="pageMode" style="max-width: 100%; overflow-y: scroll;">
                            <equipment v-if="pageMode == 'equipment' && Object.keys(equipment_select_data).length > 0" 
                                :station-data="stationData"
                                :key="tab_reset_timestamp"
                                :equip-select-data="equipment_select_data">
                            </equipment>
                            <organization v-if="pageMode == 'treeview'" 
                                :station-data="stationData">
                            </organization>
                            <overview v-if="pageMode == 'overview'"
                                :station-data="stationData">
                            </overview>
                            <station-alarm v-if="pageMode == 'alarm'"
                                :station-data="stationData">
                            </station-alarm>
                            <station-report v-if="pageMode == 'report'"
                                :station-data="stationData">
                            </station-report>
                            <drone-sld v-if="pageMode == 'drone_sld'"
                                :station-data="stationData">
                            </drone-sld>
                            <station-report-overview v-if="pageMode == 'reportOverview'"
                                :station_preSelect="{ID_list: [stationData.ID], col_list: [stationData.collection]}"
                            ></station-report-overview>
                        </div>
                    </transition>
                </div>
            </div>
        </div>
    </div>    
</template>

<script>
import equipment from "@/components/station/Data/equipment.vue"
import organization from "@/components/station/Data/organization.vue"
import overview from "@/components/station/Data/overview.vue"
import stationAlarm from "@/components/station/Data/stationAlarm.vue"
import stationReport from "@/components/station/Data/stationReport.vue"
import droneSld from "@/components/station/Data/drone_sld.vue"
import stationReportOverview from "@/pages/reportOverview.vue"
import c from "@/assets/js/common.js"

export default {
    name: "stationData",
    components:{
        equipment,
        organization,
        overview,
        stationAlarm,
        stationReport,
        droneSld,
        stationReportOverview
    },
    data(){
        return {
            pageMode: "",
            tabs: [
                {name: "overview"},
                {name: "treeview"},
                {name: "equipment"},
                {name: "alarm"},
                {name: "report"}
            ],
            tabs_first_data: [],
            tabs_second_data: [],

            stationData:{
                ID: undefined,
                collection: undefined
            },
            equipment_select_data: {},
            card_overview: {
                capacity: '---',
                today_kwh: '---',
                month_kwh: '---',
                year_kwh: '---',
                imgsrc: '',
            },
            tab_reset_timestamp: Date.now(),
            no_equip: false
        }
    },
    methods: {
        get_equipment_selection(){
            let that = this
            if(this.stationData.ID != undefined && this.stationData.collection != undefined){
                console.log(this.stationData.collection)
                this.axios.post('/get_equip_select', {
                    ID: this.stationData.ID ,
                    collection: this.stationData.collection
                }).then(data => {
                    // console.log(data.data.data)
                    that.equipment_select_data = data.data.data
                    that.no_equip = true
                    Object.keys(that.equipment_select_data).forEach(key=>{
                        if(that.equipment_select_data[key].length > 0)
                            that.no_equip = false
                    })
                    // if pageMode in that.$route.query, then jump to target
                    if('pageMode' in that.$route.query){
                        this.tabs.forEach(tab => {
                            if(tab.value == that.$route.query.pageMode){
                                that.pageMode = that.$route.query.pageMode
                            }
                            ['equip_ID', 'datatype', 'datepicker1', 'datepicker2'].forEach(q=>{
                                if(q in that.$route.query){
                                    that.$store.state.stationData_jump[q] = that.$route.query[q]
                                }
                            })
                        })
                    }

                })

            }
        },
        get_card_overview(){
            let that = this
            if(this.stationData.ID != undefined && this.stationData.collection != undefined){
                this.axios.post('/get_card_overview_real', {
                    ID_list: [this.stationData.ID],
                    col_list: [this.stationData.collection]
                }).then(function(data){
                    console.log(data.data.data)
                    if(data.data.data.length > 0){
                        that.card_overview = data.data.data[0]
                        that.card_overview.today_kwh = c.numberWithCommas(that.card_overview.today_kwh)
                        that.card_overview.month_kwh = c.numberWithCommas(that.card_overview.month_kwh)
                        that.card_overview.year_kwh = c.numberWithCommas(that.card_overview.year_kwh)
                    }
                    
                })

            }
        }
    },
    beforeMount(){
        let that = this
        Object.keys(this.stationData).forEach(key => {
            if(that.$route.query[key] == undefined){
                that.$router.push({path: "stationList"})
            }
            that.stationData[key] = that.$route.query[key]  
        })
        this.axios.post('get_tab_data', {"path": this.$route.path})
        .then(data => {
            this.tabs = data.data.data.data
            if(this.tabs.length>0){
                let origin_tab = this.tabs
                for(var i in origin_tab){
                    if('constrain' in origin_tab[i] && origin_tab[i]['constrain'] != null && !origin_tab[i]['constrain'].includes(this.stationData.collection)){
                        this.tabs.splice(i, 1)
                    }
                }
                console.log(this.tabs)
                if(this.tabs.length>5){
                    this.tabs_first_data = this.tabs.slice(0, 5)
                    this.tabs_second_data = this.tabs.slice(5)
                }
                else{
                    this.tabs_first_data = this.tabs
                }
                that.pageMode = this.tabs[0].value
            }
            this.get_equipment_selection()
            this.get_card_overview()
        })
    }

}
</script>
<style scoped>
@media (min-width: 992px){
    .nav-item:nth-child(n+2){
        border-left: .2px solid rgba(0, 0, 0, 0.7);
    }
}
.nav-item:deep(.active){
    color: black !important;
}
@media (prefers-color-scheme: dark) {
    @media (min-width: 992px){
        .nav-item:nth-child(n+2){
            border-left: .2px solid rgba(250, 250, 250, 0.7);
        }
    }
}
</style>