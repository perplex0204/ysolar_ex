<template>
    <div>
        <button class="btn btn-warning w-100" @click="openModal()"
        :class="{'d-none': hideButton}">
            <div class="d-none d-lg-block">{{$t('dispatch.手動新增工單')}}</div>
            <i class="fa-solid fa-plus d-lg-none"></i>
        </button>
        <div class="modal" id="create_dispatch_modal">
            <div class="modal-dialog modal-fullscreen-lg-down">
                <div class="modal-content" v-show="choose_alarm == false" style="overflow-y: scroll;">
                    <div class="modal-header">
                        <h5 class="modal-title">{{$t('dispatch.手動新增工單')}}</h5>
                        <button type="button" class="btn-close" @click="close_dispatch"></button>
                    </div>
                    <div class="modal-body">
                        <div class="row">
                            <select-station class="mt-2 d-none" 
                            v-if="station_ID == null"
                            @plant-select="set_plant_select" @get-ID="set_plant_ID"></select-station>
                            <el-autocomplete
                                class="col-12 col-lg-3 col-xl-2 mt-2"
                                v-model="plant_search"
                                :fetch-suggestions="querySearchAsync"
                                :placeholder="$t('廠區')"
                                value-key="name"
                                v-if="station_ID == null"
                                @select="handleSelect"
                                size="large"
                            ></el-autocomplete>
                            <div class="col-12 col-lg-3 col-xl-2 mt-2">
                                <button class="btn btn-success w-100" @click="choose_alarm = true"
                                v-if="step == 'alarm_cause' && station_ID != null">{{$t('dispatch.新增警報')}}</button>
                            </div>
                        </div>
                        <div class="row mt-4 g-0" :class="{'disable-div': station_ID == null}">
                            <!-- Dispatch Information -->
                            <div class="col-lg-4 col-12 card p-2 pt-4">
                                <div>
                                    <h5><i class="el-icon-warning text-primary"></i>{{$t('dispatch.工單資訊')}}</h5>
                                    <div class="d-flex flex-wrap dispatch_data_block pt-3 pb-3">
                                        <label class="col-12 col-lg-5">{{$t('dispatch.廠區')}}</label>
                                        <label class="col-12 col-lg-7 text-primary mt-3 mt-lg-0">{{plant_search}}</label>
                                    </div>
                                    <div class="d-flex flex-wrap dispatch_data_block pt-3 pb-3 d-none">
                                        <label class="col-12 col-lg-5">{{$t('dispatch.單號')}}</label>
                                        <label class="col-12 col-lg-7 text-primary mt-3 mt-lg-0">{{$t('未儲存')}}</label>
                                    </div>
                                    <div class="d-flex flex-wrap dispatch_data_block pt-3 pb-3">
                                        <label class="col-12 col-lg-5">{{$t('dispatch.派工日期')}}</label>
                                        <div class="col-12 col-lg-6 mt-3 mt-lg-0">
                                            <el-date-picker class="w-100" type="date" :placeholder="$t('dispatch.派工日期')" v-model="dispatch_date"
                                            size="large"
                                            format="YYYY-MM-DD"
                                            value-format="YYYY-MM-DD"
                                            :disabledDate="(_date)=>{
                                                if(_date < new Date().setHours(0,0,0,0)){
                                                    return true
                                                }
                                                else{
                                                    return false
                                                }
                                            }"
                                            :disabled="Object.keys(merge_dispatch_dict).length > 0"
                                            :teleported="false">
                                            </el-date-picker>
                                            <p class="fw-light m-0" v-if="Object.keys(merge_dispatch_dict).length > 0"
                                            style="font-size: .75rem;"><i class="fas fa-exclamation-circle"></i>{{$t("dispatch['merge_dispatch_date_lock']")}}</p>
                                        </div>
                                    </div>
                                    <div class="d-flex flex-wrap dispatch_data_block pt-3 pb-3 mt-3 mt-lg-0 d-none">
                                        <label class="col-12 col-lg-5"></label>
                                        <label class="col-12 col-lg-7 text-primary">{{$t('未派工')}}</label>
                                    </div>
                                </div>
                                <!-- <div class="mt-4">
                                    <h5><i class="el-icon-warning text-primary"></i>工單資訊</h5>
                                </div> -->
                            </div>
                            <!-- Alarm and Cause -->
                            <div class="col-lg-7 col-12 ms-lg-3 mt-4 mt-lg-0">
                                <div class="card p-2 pt-4" v-if="step == 'alarm_cause' || step == 'overview'">
                                    <h5><i class="icon-wrench text-primary"></i>{{$t('dispatch.工單內容')}}</h5>
                                    <div class="mt-3">
                                        <alarm-reason-collapse :alarm-data="alarm_data"
                                        :disable="step == 'overview'? true: false"></alarm-reason-collapse>
                                    </div>
                                </div>
                                <div class="card p-2 pt-4" v-if="step == 'merge_dispatch' ||step == 'overview'"
                                :class="{'mt-3': step == 'overview'}">
                                    <merge-dispatch :station-id="station_ID"
                                    :dispatch-date="dispatch_date"
                                    :merge-obj="merge_dispatch_dict"
                                    @dispatch-selected="merge_dispatch_update" 
                                    :emptyText="step != 'overview'?$t('無資料'):$t('dispatch.無合併工單')"
                                    :disable="step == 'overview'? true: false"></merge-dispatch>
                                </div>
                            </div>
                        </div>
                    </div>
                    <div class="modal-footer justify-content-start">
                        <button type="button" class="btn btn-danger" @click="delete_dispatch">{{$t('刪除')}}</button>
                        <button type="button" class="btn btn-success opacity-75 ms-auto" @click="previous_step()"
                        v-if="step != 'alarm_cause' && station_ID != null">   {{$t('上一步')}}
                        </button>
                        <button type="button" class="btn btn-success " @click="next_step()"
                        :class="{'ms-auto': step == 'alarm_cause' && station_ID != null}"
                        v-if="station_ID != null">
                            <div v-if="step != 'overview'">{{$t('下一步')}}</div>
                            <div v-if="step == 'overview'">{{$t('新增派工單')}}</div>
                        </button>
                    </div>
                </div>
                <div class="modal-content" v-if="choose_alarm == true" style="overflow-y: scroll;">
                    <choose-alarm @choose-alarm-done="alarm_selected" :alarm-input="alarm_data" :station-id="station_ID"></choose-alarm>
                </div>
            </div>
        </div>
    </div>
</template>
<script>
import selectStation from '@/components/station/selectStationSingleLgroup.vue'
import chooseAlarm from './choose_alarm.vue'
import alarmReasonCollapse from './alarm_reason_collapse.vue'
import mergeDispatch from './merge_dispatch.vue'
import { ElMessage } from 'element-plus'

import {Modal} from 'bootstrap'
export default {
    name: "Create_dispatch",
    components:{
        selectStation,
        chooseAlarm,
        alarmReasonCollapse,
        mergeDispatch
    },
    data(){
        return {
            plant_search: "",
            plant_select: [],
            choose_alarm: false,
            alarm_data: {},
            step: "alarm_cause",
            dispatch_date: null,
            merge_dispatch_dict: {},
            station_ID: null,
        }
    },
    props: {
        hideButton: {
            type: Boolean,
            default: false
        }
    },
    emits: ['reload-table'],
    mounted(){
        this.myModal = new Modal(document.getElementById('create_dispatch_modal'), {backdrop: 'static', keyboard: false})
    },
    methods: {
        openModal(){
            this.$store.commit("set_prevent_leave_at_once", true)
            this.myModal.show()
        },
        async querySearchAsync(queryString, cb) {
			//console.log(queryString)
			//console.log(this.PV_data)
            await this.axios.post('/station_search_regex_lgroup', {
                query: queryString,
                only_lgroup: true
            }).then(data => {
                //console.log(data.data.data)
                if(data.data.data.length == 0){
                    cb([{'name': '無資料'}])
                }else{
                    cb(data.data.data)
                }
            })
			
		},
		handleSelect(item) {
			//console.log(item)
			if(item.name == '無資料'){
				return false
			}
            this.station_ID = item.ID
		},
        alarm_selected(alarm_obj){
            this.choose_alarm = false
            this.alarm_obj = alarm_obj
        },
        next_step(){
            console.log(this.alarm_data)
            switch(this.step){
                case "alarm_cause":
                    if(Object.keys(this.alarm_data).length == 0){
                        alert(this.$i18n.t("dispatch.請選取至少一則警報"))
                        return false
                    }
                    this.step = "merge_dispatch"
                    break
                case "merge_dispatch":
                    this.step = "overview"
                    break
                case "overview":
                    // Save Dispatch
                    this.save_dispatch()
                    break
            }
        },
        previous_step(){
            switch(this.step){
                case "merge_dispatch":
                    this.step = "alarm_cause"
                    break
                case "overview":
                    this.step = "merge_dispatch"
                    break
            }
        },
        merge_dispatch_update(data){
            console.log(data)
            this.merge_dispatch_dict = data
        },
        set_plant_select(data){
            this.plant_select = data
            this.plant_search = `${data[1]}/${data[2]}`
        },
        set_plant_ID(ID){
            this.station_ID = ID
        },
        //-----------------------------------------------------------------------------
        save_dispatch(){
            // alarm_data to array
           let alarm_list = []
           for(var ID in this.alarm_data){
               let cause_dict =  {}
                if('alarm_cause' in this.alarm_data[ID]){
                    this.alarm_data[ID].alarm_cause.forEach(cause_ID=>{
                        cause_dict[cause_ID] = {
                            ID: cause_ID,
                            info: "",
                            photo: [],
                            fix: false
                        }
                    })
                }
                /* 所有警報自動新增"其他"給使用者填寫 */
                cause_dict['else'] = {
                    ID: 'else',
                    info: "",
                    photo: [],
                    fix: false
                }
                alarm_list.push({
                   ID: ID,
                   cause: cause_dict
               })
            }

            // data send to server
            let request_dict = {
                ID: this.station_ID,
                alarm_data: alarm_list,
                merge_dispatch: Object.keys(this.merge_dispatch_dict),
                dispatch_date: this.dispatch_date
            }
            this.axios.post('create_dispatch_save', request_dict).then(data=>{
                //console.log(data.data.data)
                this.$emit('reload-table')
                ElMessage.success({message: this.$i18n.t("成功")})
                this.close_dispatch()
            })
            console.log(request_dict)
        },
        //-----------------------------------------------------------------------------
        reset_modal(){
            this.station_ID = null
            this.plant_select = []
            this.plant_search = ""
            this.choose_alarm = false
            this.alarm_data = {}
            this.step = "alarm_cause",
            this.dispatch_date = null,
            this.merge_dispatch_dict = {}
        },
        delete_dispatch(){
            this.close_dispatch()
        },
        close_dispatch(){
            this.$store.commit("set_prevent_leave_at_once", false)
            this.reset_modal()
            this.myModal.hide()
        }
    },
    beforeUnmount(){
        this.$store.commit("set_prevent_leave_at_once", false)
        this.myModal.dispose()
    }
}
</script>
<style scoped>
@media (min-width: 992px){
    .modal-dialog{
        width: 95vw !important;
        max-width: 95vw !important;
    }
}
.dispatch_data_block{
    border-bottom: .5px solid gray;
}
.disable-div{
    pointer-events: none;
    opacity: 0.4;
}
.disabled_components{
    pointer-events: none;
    opacity: 0.4;
}
</style>