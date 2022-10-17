<template>
    <div class="col-12 responsive_table mt-3">
        <div class="reponsive_table_wrapper">
            <div class="w-100 row responsive_table_header  fw-bold m-0 d-none d-lg-flex flex-nowrap">
                <div class="col-2 text-center">
                    <label class="fs-6">{{$t('setting.data_integrity.案場名稱')}}<i :class="{'fas fa-angle-down': sortData.name.isReverse, 'fas fa-angle-up': !sortData.name.isReverse}" @click="changeType('name')"></i></label>
                </div>
                <div class="col-1 text-center">
                    <label class="fs-6">PR<i :class="{'fas fa-angle-down': sortData.pr.isReverse, 'fas fa-angle-up': !sortData.pr.isReverse}" @click="changeType('pr')"></i></label>
                </div>
                <div class="col-2 text-center">
                    <label class="fs-6">{{$t('案場容量')}}kW<i :class="{'fas fa-angle-down': sortData.capacity.isReverse, 'fas fa-angle-up': !sortData.capacity.isReverse}" @click="changeType('capacity')"></i></label>
                </div>
                <div class="col-1 text-center">
                    <label class="fs-6">{{$t('stationData.運轉狀態')}}<i :class="{'fas fa-angle-down': sortData.work.isReverse, 'fas fa-angle-up': !sortData.work.isReverse}" @click="changeType('work')"></i></label>
                </div>
                <div class="col-1 text-center">
                    <label class="fs-6">{{$t('stationData.通訊狀態')}}<i :class="{'fas fa-angle-down': sortData.communi.isReverse, 'fas fa-angle-up': !sortData.communi.isReverse}" @click="changeType('communi')"></i></label>
                </div>
                <div class="col-1 text-center">
                    <label class="fs-6">{{$t('stationData.警報')}}<i :class="{'fas fa-angle-down': !sortData.alertCount.isReverse, 'fas fa-angle-up': sortData.alertCount.isReverse}" @click="changeType('alertCount')"></i></label>
                </div>
                <div class="col-2 text-center">
                    <label class="fs-6">{{$t('功率')}}kW<i :class="{'fas fa-angle-down': sortData.p.isReverse, 'fas fa-angle-up': !sortData.p.isReverse}" @click="changeType('p')"></i></label>
                </div>
                <div class="col-2 text-center">
                    <label class="fs-6">{{$t('今日發電量')}}kWh<i :class="{'fas fa-angle-down': sortData.kwh.isReverse, 'fas fa-angle-up': !sortData.kwh.isReverse}" @click="changeType('kwh')"></i></label>
                </div>
                <div class="col-2 text-center">
                    <label class="fs-6">{{$t('等效日照小時')}} (hr)<i :class="{'fas fa-angle-down': sortData.irrh.isReverse, 'fas fa-angle-up': !sortData.irrh.isReverse}" @click="changeType('irrh')"></i></label>
                </div>
                <div class="col-2 text-center">
                    <label class="fs-6">{{$t('等效發電小時')}} (hr)<i :class="{'fas fa-angle-down': sortData.dmy.isReverse, 'fas fa-angle-up': !sortData.dmy.isReverse}" @click="changeType('dmy')"></i></label>
                </div>
                <div class="col-2 text-center">
                    <label class="fs-6">{{$t('stationData.overview.最後通訊時間')}}<i :class="{'fas fa-angle-down': sortData.lastTime.isReverse, 'fas fa-angle-up': !sortData.lastTime.isReverse}" @click="changeType('lastTime')"></i></label>
                </div>  
                <div class="col-2 text-center" style="position: sticky; right: 0px; border-radius: 0 .5rem .5rem 0;">
                    <label class="fs-6">{{$t('查看案場')}}</label>
                </div>
            </div>
            <div class="w-100 pt-2 pb-2 text-center" v-if="stationData_sort.length == 0">
                {{$t(emptyText)}}
            </div>

            <transition mode="out-in" :name="page_direction == 'to' ? 'table_animation_to':'table_animation_back'">
                <div class="w-100 responsive_table_body">
                    <div class="row m-0 responsive_table_content mt-2 mt-lg-0" v-for="(station, index) in stationData_sort" :key="index" 
                    >
                        <div class="col-12 d-lg-none mt-2"></div>
                        <div class="col-12 col-lg-2" @dblclick="header_dblclick(station.ID,station.collection)">
                            <div class="d-lg-none">
                                <label class="fs-6 fw-bold d-lg-none">{{$t('setting.data_integrity.案場名稱')}}：</label>
                                <label class="fs-6 d-lg-none">{{station.collection == 'pv_plant'?
                                    station.name:
                                    station.collection == 'pv_lgroup'?
                                    `${station.PV}/${station.name}`:
                                    `${station.PV}/${station.lgroup}/${station.name}`}}
                                </label>
                            </div>
                            <label class="fs-6 w-100 text-center d-none d-lg-block">{{station.collection == 'pv_plant'?
                                station.name:
                                station.collection == 'pv_lgroup'?
                                `${station.PV}/${station.name}`:
                                `${station.PV}/${station.lgroup}/${station.name}`}}
                            </label>
                        </div>
                        <!-- <div class="col-12 d-lg-none mt-2 mb-2" style="border-bottom: 0.25px solid black;"></div> -->
                        <div class="col-12 col-lg-1">
                            <div class="d-lg-none">
                                <label class="fs-6 fw-bold d-lg-none">PR：</label>
                                <label class="fs-6 d-lg-none">{{station.pr}}</label>
                            </div>
                            <label class="fs-6 w-100 text-center d-none d-lg-block">{{station.pr}}</label>
                        </div>
                        <div class="col-12 col-lg-2">
                            <div class="d-lg-none">
                                <label class="fs-6 fw-bold d-lg-none">{{$t('案場容量')}}：</label>
                                <label class="fs-6 d-lg-none">{{station.capacity}}</label>
                            </div>
                            <label class="fs-6 w-100 text-center d-none d-lg-block">{{station.capacity}}</label>
                        </div>
                        <div class="col-12 d-lg-none mt-2 mb-2" style="border-bottom: 0.25px solid black;"></div>
                        <div class="col-12 col-lg-1">
                            <div class="d-lg-none">
                                <label class="fs-6 fw-bold d-lg-none">{{$t('stationData.運轉狀態')}}：</label>
                                <label class="fs-6 d-lg-none">
                                    <i class="fas fa-check-circle"
                                        :class="{'text-success': station.status.work,
                                        'text-danger': !station.status.work}">
                                    </i>
                                </label>
                            </div>
                            <label class="fs-6 w-100 text-center d-none d-lg-block">
                                <i class="fas fa-check-circle"
                                    :class="{'text-success': station.status.work,
                                    'text-danger': !station.status.work}">
                                </i>
                            </label>
                        </div>
                        <div class="col-12 col-lg-1">
                            <div class="d-lg-none mb-2">
                                <label class="fs-6 fw-bold d-lg-none">{{$t('stationData.通訊狀態')}}：</label>
                                <label class="fs-6 d-lg-none">
                                    <i class="fas fa-check-circle"
                                        :class="{'text-success': station.status.communi,
                                        'text-danger': !station.status.communi}">
                                    </i>
                                </label>
                            </div>
                            <label class="fs-6 w-100 text-center d-none d-lg-block">
                                <i class="fas fa-check-circle"
                                    :class="{'text-success': station.status.communi,
                                    'text-danger': !station.status.communi}">
                                </i>
                            </label>
                        </div>
                        <div class="col-12 col-lg-1">
                            <div class="d-lg-none mb-2">
                                <label class="fs-6 fw-bold d-lg-none">{{$t('stationData.警報')}}：</label>
                                <label class="fs-6 d-lg-none">
                                    <i class="fas fa-check-circle"
                                        :class="{'text-success': station.status.alertCount == 0,
                                        'text-danger': station.status.alertCount != 0}">
                                    </i>
                                </label>
                            </div>
                            <label class="fs-6 w-100 text-center d-none d-lg-block">
                                <i class="fas fa-check-circle"
                                    :class="{'text-success': station.status.alertCount == 0,
                                    'text-danger': station.status.alertCount != 0}">
                                </i>
                            </label>
                        </div>
                        <div class="col-12 d-lg-none mt-2 mb-2" style="border-bottom: 0.25px solid black;"></div>
                        <div class="col-12 col-lg-2 ">
                            <div class="d-lg-none mb-2">
                                <label class="fs-6 fw-bold d-lg-none">{{$t('功率')}}：</label>
                                <label class="fs-6 d-lg-none">{{station.p}} kW</label>
                            </div>
                            <label class="fs-6 w-100 text-center d-none d-lg-block">{{station.p}} kW</label>
                        </div>
                        <div class="col-12 col-lg-2 ">
                            <div class="d-lg-none mb-2">
                                <label class="fs-6 fw-bold d-lg-none">{{$t('今日發電量')}}：</label>
                                <label class="fs-6 d-lg-none">{{station.kwh}}</label>
                            </div>
                            <label class="fs-6 w-100 text-center d-none d-lg-block">{{station.kwh}}</label>
                        </div>
                        <div class="col-12 col-lg-2 ">
                            <div class="d-lg-none mb-2">
                                <label class="fs-6 fw-bold d-lg-none">{{$t('等效日照小時')}}：</label>
                                <label class="fs-6 d-lg-none">{{station.irrh}}</label>
                            </div>
                            <label class="fs-6 w-100 text-center d-none d-lg-block">{{station.irrh}}</label>
                        </div>
                        <div class="col-12 col-lg-2 ">
                            <div class="d-lg-none mb-2">
                                <label class="fs-6 fw-bold d-lg-none">{{$t('等效發電小時')}}：</label>
                                <label class="fs-6 d-lg-none">{{station.dmy}}</label>
                            </div>
                            <label class="fs-6 w-100 text-center d-none d-lg-block">{{station.dmy}}</label>
                        </div>
                        <div class="col-12 col-lg-2">
                            <div class="d-lg-none mb-2">
                                <label class="fs-6 fw-bold d-lg-none">{{$t('stationData.overview.最後通訊時間')}}：</label>
                                <label class="fs-6 d-lg-none">{{station.lastTime}}</label>
                            </div>
                            <label class="fs-6 w-100 text-center d-none d-lg-block">{{station.lastTime}}</label>
                        </div>
                        <div class="col-12 col-lg-2" style="position: sticky; right: 0px">
                            <div class="d-lg-none d-flex">
                                <label class="fs-6 fw-bold d-lg-none">{{$t('查看案場')}}:</label>
                                <button class="btn btn-warning ms-1" @click="openStation(station)">{{$t('查看案場')}}</button>
                            </div>
                            <button class="d-none d-lg-block btn btn-warning position-relative top-50 start-50 translate-middle" @click="openStation(station)">{{$t('查看案場')}}</button>
                        </div>
                        <div class="col-12 d-lg-none mt-2"></div>
                    </div>
                </div>
            </transition>
        </div>

    </div>
</template>

<script>
export default {
    name: "listTable",
    props: {
		stationData: {type: Array, default: function(){return []}},
        emptyText: {type: String, default: "無資料"},
	},
    data(){
        return {
            page_direction: 'to',
            sortData: {
                name: {type: "name_total", isReverse: false, db_key: false},
                pr: {type: "pr_num", isReverse: false, db_key: false},
                capacity: {type: "capacity_num", isReverse: false, db_key: false},
                work: {type: "status", sub_type: "work", isReverse: false, db_key: true},
                communi: {type: "status", sub_type: "communi", isReverse: false, db_key: true},
                alertCount: {type: "status", sub_type: "alertCount", isReverse: false, db_key: true},
                p: {type: "p_num", isReverse: false, db_key: false},
                kwh: {type: "kwh_num", isReverse: false, db_key: false},
                irrh: {type: "irrh_num", isReverse: false, db_key: false},
                dmy: {type: "dmy_num", isReverse: false, db_key: false},
                lastTime: {type: "lastTime", isReverse: false, db_key: false},
            },
            sortType: "name"
        }
    },
    methods: {
        changeType(type){
            let that = this
            that.sortType = type
            that.sortData[type]["isReverse"] = !that.sortData[type]["isReverse"]
        },
        header_dblclick(ID, type){
			this.$emit("dblclick-jump", {ID: ID, type: type})
		},
        openStation(data){
            this.$store.state.stationList_history = {
                ID_list: this.$parent.$data.plant_select.ID_list,
                col_list: this.$parent.$data.plant_select.col_list,
                current_page: this.$parent.$data.current_page
            }
            this.$router.push({path: "stationData", query: {ID: data.ID, collection: data.collection}})
        },
    },
    computed: {
        stationData_sort(){
            console.log(this.stationData)
            let that = this
            let type = that.sortType
            if(that.sortData[type]["db_key"] == true){
                return that.stationData.sort(function(a, b){
                    if(that.sortData[type]["isReverse"]){
                        return b[that.sortData[type]["type"]][that.sortData[type]["sub_type"]] - a[that.sortData[type]["type"]][that.sortData[type]["sub_type"]]
                    }
                    else{
                        return a[that.sortData[type]["type"]][that.sortData[type]["sub_type"]] - b[that.sortData[type]["type"]][that.sortData[type]["sub_type"]]
                    }
                })
            }
            else{
                return that.stationData.sort(function(a, b){
                    if(that.sortData[type]["isReverse"]){
                        if(typeof(b[that.sortData[type]["type"]]) == 'string'){
                            return b[that.sortData[type]["type"]].length - a[that.sortData[type]["type"]].length
                        }
                        else{
                            return b[that.sortData[type]["type"]] - a[that.sortData[type]["type"]]
                        }
                        // return b[that.sortData[type]["type"]] - a[that.sortData[type]["type"]]
                    }
                    else{
                         if(typeof(b[that.sortData[type]["type"]]) == 'string'){
                            return a[that.sortData[type]["type"]].length - b[that.sortData[type]["type"]].length
                        }
                        else{
                            return a[that.sortData[type]["type"]] - b[that.sortData[type]["type"]]
                        }
                    }
                })
            }
        }
    },
    watch: {
        stationData_sort(){
            console.log(this.stationData_sort)
        }
    }
}
</script>

<style scoped>
.fas:hover{
    cursor: pointer;
}
</style>