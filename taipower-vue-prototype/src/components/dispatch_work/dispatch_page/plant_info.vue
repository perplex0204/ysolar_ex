<template>
    <div>
        <div class="row mt-4 g-0 ">
            <div class="col-lg-4 col-12">
                <div class="card p-2 pt-4 h-100">
                    <h5><i class="el-icon-warning text-primary"></i>{{$t('dispatch.工單資訊')}}</h5>
                    <div class="d-flex flex-wrap dispatch_data_block pt-3 pb-3">
                        <label class="col-12 col-lg-5">{{$t('dispatch.單號')}}</label>
                        <label class="col-12 col-lg-7  mt-3 mt-lg-0">{{dispatchData.name}}</label>
                    </div>
                    <div class="d-flex flex-wrap dispatch_data_block pt-3 pb-3">
                        <label class="col-12 col-lg-5">{{$t('dispatch.派工日期')}}</label>
                        <div class="col-12 col-lg-6  mt-3 mt-lg-0">
                            <el-date-picker class="w-100" type="date" :placeholder="$t('dispatch.派工日期')"
                                size="large"
                                v-model="local_dispatch_data.dispatch_time"
                                @change="(val) => { 
                                    if (val == null) dispatch_time_save();
                                }"
                                :teleported="false"
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
                                :readonly="!editable || (dispatchData.stage != 'took_wait_date_enter' && !(dispatchData.stage == 'wait_for_take' && $store.state.user_data.level == 3)) "
                            >
                            </el-date-picker>
                            <!-- 等待接單後才能輸入 -->
                            <!-- 按鈕 wait_for_take維運人員也能用 -->
                            <button class="btn btn-success mt-2" v-if="(dispatchData.stage == 'took_wait_date_enter' || (dispatchData.stage == 'wait_for_take' && $store.state.user_data.level == 3)) 
                            && local_dispatch_data.dispatch_time != null" @click="dispatch_time_save()">{{$t('dispatch.確認日期')}}</button>
                            <p class="fw-light m-0" v-if="dispatchData.stage == 'wait_for_take' && dispatchData.dispatch_time == null"
                            style="font-size: .75rem;"><i class="fas fa-exclamation-circle"></i>{{$t("dispatch.date_select['take_to_enter_date']")}}</p>
                            <!-- 管理人員已輸入派工日期 -->
                            <p class="fw-light m-0" v-if="dispatchData.stage == 'wait_for_take' && dispatchData.dispatch_time != null"
                            style="font-size: .75rem;"><i class="fas fa-exclamation-circle"></i>{{$t("dispatch.date_select['admin_had_set_date']")}}</p>
                            <!-- 管理人員確認派工日期 -->
                            <p class="fw-light m-0" v-if="dispatchData.stage == 'wait_admin_confirm_date' && $store.state.user_data.level == 3"
                            style="font-size: .75rem;"><i class="fas fa-exclamation-circle"></i>{{$t("dispatch.date_select['admin_please_confirm']")}}</p>
                            <div class="d-flex flex-wrap" v-if="dispatchData.stage == 'wait_admin_confirm_date' && $store.state.user_data.level == 3">
                                <button class="btn btn-success mt-2 ms-2" @click="dispatch_time_confirm(true)">{{$t("dispatch['同意']")}}</button>
                                <button class="btn btn-danger mt-2 ms-2" @click="dispatch_time_confirm(false)">{{$t("dispatch['不同意']")}}</button>
                            </div>
                        </div>
                    </div>
                    <div class="d-flex flex-wrap dispatch_data_block pt-3 pb-3 mt-3 mt-lg-0">
                        <label class="col-12 col-lg-5">{{$t('dispatch.狀態')}}</label>
                        <label class="col-12 col-lg-7 ">{{$t(`dispatch.stage["${dispatchData.stage}"]`)}}</label>
                    </div>
                    <div class="d-flex flex-wrap dispatch_data_block pt-3 pb-3 mt-3 mt-lg-0">
                        <label class="col-12 col-lg-5">{{$t('dispatch.預估維運成本')}}</label>
                        <label class="col-12 col-lg-7 ">{{dispatchData.predict_dispatch_cost}}</label>
                    </div>
                    <div class="mt-4" v-if="dispatchData.stage != 'wait_for_take'">
                        <h5><i class="fa-solid fa-users text-primary me-2"></i>{{$t('dispatch.維運人員資訊')}}</h5>
                        <div class="d-flex flex-wrap dispatch_data_block pt-3 pb-3">
                            <label class="col-12 col-lg-5">
                                <!-- <span class="text-success"><i class="icon-briefcase"></i></span> -->
                                {{$t('dispatch.維運人員')}}：
                            </label>
                            <label class="col-12 col-lg-7  mt-3 mt-lg-0">
                                {{dispatchData.maintainer_data.name}}
                                <br/>
                                {{dispatchData.maintainer_data.tel}}
                            </label>
                        </div>
                    </div>
                </div>
                <!-- <div class="mt-4">
                    <h5><i class="el-icon-warning "></i>工單資訊</h5>
                </div> -->
            </div>
            <div class="col-lg-8 col-12">
                <div class="ms-lg-3 mt-4 mt-lg-0 card p-2 pt-4 h-100">
                    <h5><i class="el-icon-warning text-primary"></i>{{$t('案場資訊')}}</h5>
                    <div class="d-flex flex-wrap dispatch_data_block pt-3 pb-3">
                        <label class="col-12 col-lg-5">
                            <span class="text-success"><i class="icon-ttl_time"></i></span>
                            {{$t('掛錶日期')}}
                        </label>
                        <label class="col-12 col-lg-7  mt-3 mt-lg-0">{{dispatchData.station_data.plant_data.start_date}}</label>
                    </div>
                    <div class="d-flex flex-wrap dispatch_data_block pt-3 pb-3">
                        <label class="col-12 col-lg-5">
                            <span class="text-success"><i class="icon-ttl_thunder"></i></span>
                            {{$t('裝置容量')}}
                        </label>
                        <label class="col-12 col-lg-7  mt-3 mt-lg-0">{{dispatchData.station_data.capacity}} kWp</label>
                    </div>
                    <div class="d-flex flex-wrap dispatch_data_block pt-3 pb-3">
                        <label class="col-12 col-lg-5">
                            <span class="text-success"><i class="el-icon-location"></i></span>
                            {{$t('案場位置')}}
                        </label>
                        <label class="col-12 col-lg-7  mt-3 mt-lg-0">{{dispatchData.station_data.plant_data.plant_address}}</label>
                    </div>
                    <div class="d-flex flex-wrap dispatch_data_block pt-3 pb-3">
                        <label class="col-12 col-lg-5">
                            <span class="text-success"><i class="icon-globe"></i></span>
                            {{$t('經緯度')}}
                        </label>
                        <label class="col-12 col-lg-7  mt-3 mt-lg-0">{{dispatchData.station_data.plant_data.coordinates}}</label>
                    </div>
                    <div class="d-flex flex-wrap dispatch_data_block pt-3 pb-3">
                        <label class="col-12 col-lg-5">
                            <span class="text-success"><i class="el-icon-s-tools"></i></span>
                            {{$t('模組型號')}}
                        </label>
                        <label class="col-12 col-lg-7  mt-3 mt-lg-0">{{dispatchData.station_data.module_model}}</label>
                    </div>
                    <div class="d-flex flex-wrap dispatch_data_block pt-3 pb-3">
                        <label class="col-12 col-lg-5">
                            <span class="text-success"><i class="icon-pencil"></i></span>
                            {{$t('備註欄')}}
                        </label>
                        <label class="col-12 col-lg-7  mt-3 mt-lg-0">
                            <div v-for="event, i in dispatchData.station_data.plant_data.event" :key="event">{{`${i+1}. ${event}`}}</div>
                        </label>
                    </div>
                    <div class="d-flex flex-wrap dispatch_data_block pt-3 pb-3">
                        <label class="col-12 col-lg-5">
                            <span class="text-success"><i class="icon-briefcase"></i></span>
                            {{$t('受託者')}}
                        </label>
                        <label class="col-12 col-lg-7  mt-3 mt-lg-0">
                            {{dispatchData.station_data.plant_data.client_info.unit}}
                            <br/>
                            {{dispatchData.station_data.plant_data.client_info.TEL}}
                        </label>
                    </div>
                </div>
            </div>
            <div class="col-12 card p-2 pt-4 mt-4">
                <div>
                    <h5><i class="fa-solid fa-map text-primary me-2"></i>{{$t('dispatch.工作路徑')}}</h5>
                    <div class="d-flex flex-wrap dispatch_data_block pt-3 pb-3">
                        <label class="col-12 col-lg-2">{{$t('dispatch.出發地址')}}</label>
                        <div class="col-12 col-lg-10 ">
                            <!-- <el-input placeholder="出發地址"/> -->
                            <input class="form-control" type="text" id="map_autocomplete" :placeholder="$t('dispatch.出發地址')"
                            v-model="location_autocomplete"
                            :disabled="!editable || !['wait_admin_confirm_date', 'wait_for_dispatch'].includes(dispatchData.stage)" />
                            <!-- 日期確認後才能輸入 -->
                            <p class="fw-light m-0" v-if="['took_wait_date_enter','wait_for_take'].includes(dispatchData.stage)"
                            style="font-size: .75rem;"><i class="fas fa-exclamation-circle"></i>{{$t("dispatch['wait_dispatch_date_select']")}}</p>
                        </div>
                    </div>
                    <div class="d-flex flex-wrap dispatch_data_block pt-3 pb-3">
                        <label class="col-12 col-lg-2">{{$t('dispatch.預估交通成本')}}</label>
                        <label class="col-12 col-lg-10 " v-if="transit_cost != null">NTD$ {{transit_cost}}</label>
                    </div>
                    <div id="google_map_zone" class="w-100" style="height: 450px;">
                        <iframe v-if="![null, undefined].includes(origin_id)" width="100%" height="450" style="border:0" loading="lazy" allowfullscreen 
                        :src="`https://www.google.com/maps/embed/v1/directions?origin=place_id:${origin_id}&destination=place_id:${dispatchData.station_data.plant_data.location.place_id}&key=${google_api_key}`"></iframe>
                        <iframe v-else width="100%" height="450" style="border:0" loading="lazy" allowfullscreen 
                        :src="`https://www.google.com/maps/embed/v1/place?q=place_id:${dispatchData.station_data.plant_data.location.place_id}&key=${google_api_key}`"></iframe>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>
<script>
import { Loader } from "@googlemaps/js-api-loader";
import { ElMessage } from 'element-plus'

export default {
    name: "Plant_info",
    props: {
        dispatchData: {
            type: Object,
            default: ()=>{
                return {}
            }
        },
        modalControl: {
            type: Object,
            default: ()=>{
                return {}
            }
        },
        editable: {
            type: Boolean,
            default: true
        }
    },
    data(){
        return {
            origin_id: null,
            local_dispatch_data: {
                dispatch_time: null
            },
            worker_data: [],
            location_autocomplete: null,
            transit_cost: null,
            google_api_key: process.env.VUE_APP_GOOGLE_API_KEY,
        }
    },
    methods: {
        map(){
            let that = this
            const loader = new Loader({
                apiKey: process.env.VUE_APP_GOOGLE_API_KEY,
                version: "weekly",
                libraries: ["places"],
                language: "zh-TW",
            })
            loader.load().then(google=>{
            //console.log(google)
            /* autocomplete */
            const options = {
                componentRestrictions: { country: ["tw"] },
                fields: ["formatted_address", "geometry", "name", "place_id"],
                strictBounds: false,
                /* types: ["establishment"], */
            }
            this.map_autocomplete = new google.maps.places.Autocomplete(document.getElementById("map_autocomplete"), options)
            /* maps */
            const plant_location = { lat: this.dispatchData.station_data.plant_data.location.Latitude, 
            lng: this.dispatchData.station_data.plant_data.location.Longitude};
            this.directionsService = new google.maps.DirectionsService()
            /* autocomplete listener */
            this.map_autocomplete.addListener("place_changed", () =>{
                const place = this.map_autocomplete.getPlace();
                console.log(place)
                if("place_id" in place){
                    this.origin_id = place.place_id
                    // Make Direction
                    const request = {
                        origin: { 
                            lat: place.geometry.location.lat(),
                            lng: place.geometry.location.lng()
                        },
                        destination: plant_location,
                        travelMode: 'DRIVING'
                    };
                    this.directionsService.route(request, (result, status) => {
                        if (status == 'OK') {
                            console.log(result)
                            console.log(this.origin_id, place.formatted_address, )
                            this.location_autocomplete = place.formatted_address
                            this.axios.post('/dispatch_worker_transit', {
                                dispatch_ID: this.dispatchData._id,
                                address: place.formatted_address,
                                place_id: place.place_id,
                                distance: result.routes[0].legs[0].distance.value

                            }).then(data => {
                                console.log(data.data.data)
                                this.transit_cost = data.data.data.transit.total_cost
                            })
                        }
                    })
                }
                else{
                    alert(this.$i18n.t('無資料'))
                }
            })
            
        })
        
        },
        dispatch_time_save(){
            const answer = this.$store.state.user_data.level == 3 ? true : confirm(this.$i18n.t('dispatch["dispatch_time_confirm"]'))
            if(answer){
                this.axios.post("/dispatch_update_stage", {
                    ID: this.dispatchData._id,
                    stage: this.dispatchData.stage,
                    to_stage: this.dispatchData.stage == 'wait_for_take'? 'wait_for_take' : '',
                    data: {
                        dispatch_time: this.local_dispatch_data.dispatch_time
                    }
                }).then(data => {
                    console.log(data.data.data)
                    ElMessage.success({message: this.$i18n.t("成功")})
                    if(this.$store.state.user_data.level < 3)
                        this.$parent.close_modal()
                })
            }
        },
        dispatch_time_confirm(agree){
            if(agree){
                const answer = confirm(this.$i18n.t('dispatch["admin_dispatch_time_confirm"]'))
                if(answer){
                    this.axios.post("/dispatch_update_stage", {
                        ID: this.dispatchData._id,
                        stage: this.dispatchData.stage,
                        data: true,
                    }).then(data => {
                        ElMessage.success({message: this.$i18n.t("成功")})
                        this.$parent.close_modal()
                    })
                }
            }else{
                const answer = confirm(this.$i18n.t('dispatch["admin_dispatch_time_confirm_reject"]'))
                if(answer){
                    this.axios.post("/dispatch_update_stage", {
                        ID: this.dispatchData._id,
                        stage: this.dispatchData.stage,
                        data: false
                    }).then(data => {
                        ElMessage.success({message: this.$i18n.t("成功")})
                        this.$parent.close_modal()
                    })
                }
            }
        }
    },
    mounted(){
        this.local_dispatch_data = this.dispatchData
        if(!['wait_for_take', 'wait_for_priority'].includes(this.dispatchData.stage)){
            let working_data = this.dispatchData.working_data[this.dispatchData.working_data.length - 1]
            this.location_autocomplete = working_data.transit.start_address
            this.origin_id = working_data.transit.position_id
            this.transit_cost = working_data.transit.fee
        }
        this.map()
    },
}
</script>
<style>
/* map autocomplete */
.pac-container{
    z-index: 8888 !important;
}
</style>