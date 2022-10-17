<template>
    <div>
        <div class="d-flex flex-wrap mb-3">
            <div class="col-12 col-lg-5 col-xl-4 col-xxl-3">
                <autocomplete @station-select="station_select" :preSelect="$store.state.user_data.pageType == 'taipower'" ></autocomplete>
            </div>
        </div>
        <div class="card p-4" v-if="Object.keys(all_data).length > 0">
            <div v-if="Object.keys(all_data.daily_show_information).length > 0">
                <div class="d-flex flex-wrap mt-lg-2">
                    <div class="col-12 col-lg-6">
                        <!-- 案場名稱 -->
                        <div class="col-12">
                            <div class="fs-4 text-success ms-lg-2">
                                <div>{{station_name}}</div>
                            </div>
                        </div>
                        <div class="d-flex flex-wrap">
                            <!-- 清潔狀況 -->
                            <div class="col-12 col-lg-6 mt-2">
                                <i class="fa-solid fa-broom"></i>
                                {{$t('AIAnalysis.module_cleaning.清潔狀況')}}：
                            </div>
                            <div class="col-12 col-lg-6 mt-2 text-center text-lg-start"
                            :class="{
                                'text-success': daily_show_info.cleaning_status == '1',
                                'text-warning': daily_show_info.cleaning_status == '2',
                                'text-danger': daily_show_info.cleaning_status == '3',
                            }">
                                {{$t(`AIAnalysis.module_cleaning.cleaning_status.${daily_show_info.cleaning_status}`)}}
                            </div>
                            <!-- 髒污累積起點 -->
                            <div class="col-12 col-lg-6 mt-2">
                                <i class="fa-solid fa-clock"></i>
                                {{$t('AIAnalysis.module_cleaning.髒污累積起點')}}：
                            </div>
                            <div class="col-12 col-lg-6 mt-2 text-center text-lg-start">
                                {{daily_show_info.soiling_start_date}}
                            </div>
                            <!-- 目前髒污率 -->
                            <div class="col-12 col-lg-6 mt-2">
                                <i class="fa-solid fa-percent"></i>
                                {{$t('AIAnalysis.module_cleaning.目前髒污率')}}：
                            </div>
                            <div class="col-12 col-lg-6 mt-2 text-center text-lg-start">
                                {{daily_show_info.current_soiling_value}}%
                            </div>
                            <!-- 預期累積損失 -->
                            <div class="col-12 col-lg-6 mt-2">
                                <i class="fa-solid fa-arrow-trend-down"></i>
                                {{$t('AIAnalysis.module_cleaning.預期累積損失')}}：
                            </div>
                            <div class="col-12 col-lg-6 mt-2 text-center text-lg-start">
                                {{daily_show_info.expected_total_loss}}kWh
                            </div>
                        </div>
                    </div>
                    <div class="col-12 col-lg-6">
                        <!-- 歷史髒污累積圖 -->
                        <div ref="plot_div" class="w-100" style="max-width: 100%;"></div>
                    </div>
                </div>
                <el-divider class="mt-4 mb-4" />
                <div class="d-flex flex-wrap" style="min-height: 200px;">
                    <!-- PR 與 天氣 -->
                    <div class="col-12 col-lg-6">
                        <div class="d-flex flex-wrap">
                            <!-- PR -->
                            <div class="col-12 col-lg-8 mt-2">
                                {{$t('AIAnalysis.module_cleaning.預期清洗後提升之PR')}}：
                            </div>
                            <div class="col-12 col-lg-4 mt-2 text-center text-lg-start fw-bold fs-5">
                                {{daily_show_info.expected_pr}}%
                            </div> 
                            <!-- 天氣預報 -->
                            <div class="col-12 mt-3">
                            <h5>{{$t('AIAnalysis.module_cleaning.未來三日天氣預報')}}</h5>
                            </div>   
                            <div class="col-12 d-flex justify-content-center pe-lg-4">
                                <div class="card w-100 weather_card text-dark">
                                    <div class="d-flex flex-wrap">
                                        <!-- 天氣 -->
                                        <div class="col-xl-4 col-12 p-2" 
                                        v-for="(w, i) in all_data.weather_data" :key="w.date"
                                        :class="{
                                            'border-start': i>0 && !$store.state.isMobile,
                                            'border-top': i>0 && $store.state.isMobile,
                                        }">
                                            <div class="d-flex flex-wrap">
                                                <div class="d-flex flex-column">
                                                    <label class="fs-7">{{w.date}}</label>
                                                    <label class="temp-color fw-bold fs-4">{{w.temperature}}°C</label>
                                                </div>
                                                <img class="ms-auto col-5 col-sm-3 col-md-2 col-xl-5 weather-icon" :src="w.imgurl" />
                                            </div>
                                            <div>
                                                <div>
                                                    {{
                                                        w.status[$store.state.language] == undefined ?
                                                        w.status['zh-TW'] : w.status[$store.state.language]
                                                    }}
                                                </div>
                                                <div>
                                                    {{$t('降雨機率')}}：{{w.rain}}%
                                                </div>
                                            </div>
                                        </div>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>
                    <el-divider class="mt-4 mb-4 d-lg-none" />
                    <!-- 派工 -->
                    <div class="col-12 col-lg-6 mt-2 d-flex flex-wrap">
                        <el-divider direction="vertical" class="m-0 h-100 d-none d-lg-block" />
                        <div class="d-flex flex-wrap col-12 ps-2 pb-2 align-items-center" style="margin-left: -1px;">
                            <!-- 預期清洗成本 -->
                            <div class="col-12 col-lg-4 mt-2">
                                <h5 class="mb-0">
                                    <i class="icon-ttl_money"></i>
                                    {{$t('AIAnalysis.module_cleaning.預期清洗成本')}}
                                </h5>
                            </div>   
                            <div class="col-12 col-lg-8 mt-2 d-flex align-items-center">
                                <el-input class="w-75" type="number" size="large" v-model="daily_show_info.module_cleaning_cost" />
                                <button class="btn btn-success ms-2" @click="save_module_cleaning_cost">{{$t('儲存')}}</button>
                            </div> 
                            <!-- 預期回本天數 -->
                            <div class="col-12 col-lg-4 mt-2">
                                <h5 class="mb-0">
                                    <i class="icon-ttl_money opacity-0 d-none d-lg-inline-block"></i>
                                    {{$t('AIAnalysis.module_cleaning.預期回本天數')}}：
                                </h5>
                            </div>   
                            <div class="col-12 col-lg-8 mt-2 text-center text-lg-start">
                                <h5 class="mb-0">
                                    {{daily_show_info.expected_pay_back_time}}
                                    {{$t('AIAnalysis.module_cleaning.天')}}
                                </h5>
                            </div> 
                            <!-- 派工 -->
                            <div class="col-12 col-lg-4 mt-2">
                                <h5 class="mb-0 opacity-0 d-none d-lg-inline-block"><i class="icon-ttl_money"></i></h5>
                                {{$t('AIAnalysis.module_cleaning.派工日期')}}：
                            </div>
                            <div class="col-12 col-lg-8 mt-2 p-lg-2">
                                <el-date-picker class="w-75" size="large" v-model="dispatch_date"> </el-date-picker>
                            </div> 
                            <!-- 建議清洗 -->
                            <div class="col-12 mt-2 d-none" v-if="dispatch_date != null">
                                <h5 class="mb-0 opacity-0 d-none d-lg-inline-block"><i class="icon-ttl_money"></i></h5>
                                當日不建議進行清洗
                            </div>
                            <!-- 新增派工 -->
                            <div class="col-12">
                                <button class="btn btn-warning ms-auto me-auto mt-2"
                                @click="create_dispatch">{{$t('AIAnalysis.module_cleaning.新增派工')}}</button>
                            </div>
                        </div>
                    </div>
                </div>
        
        
        
            </div>
            <!-- 無資料 -->
            <div class="w-100 p-4 text-center" v-else>
                <h3><i class="fa-solid fa-database me-2"></i>{{$t('無資料')}}</h3>
            </div>
        </div>
        <schedule-modal ref="schedule_modal"
        :hide-button="true"></schedule-modal>
    </div>
</template>

<script>

import c from 'assets/js/common.js'
import autocomplete from '../autocomplete/lgroup_only.vue'
import { ElMessage } from 'element-plus'
import scheduleModal from "@/components/dispatch/schedule/schedule_modal.vue"

export default {
    name: 'Module_cleaning',
    components: {
        autocomplete,
        scheduleModal
    },
    data(){
        
        return {
            station_ID: null,
            station_name: '',
            all_data: {},
            daily_show_info: {},
            dispatch_date: null,
        }
    },
    methods: {
        station_select(item){
            this.station_ID = item.ID
            this.station_collection = item.collection
            this.station_name = item.name
            this.all_data = {}
            this.daily_show_info = {}
            this.get_module_cleaning_data(true)  
        },
        get_module_cleaning_data(first=false){
            this.axios.post('/get_module_cleaning_data', {
                ID: this.station_ID
            }).then(data => {
                console.log(data.data.data)
                this.all_data = data.data.data
                this.daily_show_info = data.data.data.daily_show_information
                // station cleaning data empty
                if(Object.keys(this.daily_show_info).length == 0)
                    return false
                if(first)
                    this.get_module_cleaning_soil_plot()
                this.get_station_pv_module()
            })
            if(this.sync_data){
                window.clearTimeout(this.sync_data)
            }
            this.sync_data = window.setTimeout(this.get_module_cleaning_data, 10000)
        },
        get_station_pv_module(){
            this.axios.get(`/get_station_pv_module?ID=${this.station_ID}`).then(data=>{
                console.log(data.data.data)
                data.data.data.module_list.forEach(i=>{
                    this.daily_show_info['module_model'] = i.model
                    this.daily_show_info['module_cleaning_cost'] = i.wash_cost
                })
            })
        },
        save_module_cleaning_cost(){
            this.axios.post('/get_station_pv_module', {
                ID: this.station_ID,
                model: this.daily_show_info['module_model'],
                wash_cost: this.daily_show_info['module_cleaning_cost']
            }).then(data=>{
                ElMessage.success({message: this.$i18n.t("成功")})
            })
        },
        get_module_cleaning_soil_plot(){
            this.axios.post('/get_module_cleaning_soil_plot', {
                ID: this.station_ID
            }).then(data=>{
                console.log(data.data.data)

                let plot_data = []
                // daily_normalized
                plot_data.push({
                    x: data.data.data.x_axis,
                    y: data.data.data.daily_normalized,
                    mode: 'markers',
                    type: 'scatter',
                    line: { size: 5 },
                    name: "Daily Normalized"
                })
                // perfect_clean
                plot_data.push({
                    x: data.data.data.x_axis,
                    y: data.data.data.perfect_clean,
                    mode: 'line',
                    type: 'scatter',
                    line: { size: 8 },
                    name: "Perfect Clean"
                })
                
                // Plot data
                let plot_obj = this.$refs.plot_div
                this.Plotly.newPlot(plot_obj, plot_data, 
                this.get_plot_layout(plot_obj),
                {
                    displaylogo: false,
                    modeBarButtonsToRemove: [
                    "sendDataToCloud",
                    "hoverClosestCartesian",
                    "hoverCompareCartesian",
                    "toggleSpikelines",
                    ]
                })
                c.plot_text_color_fix(plot_obj)
            })
        },
        get_plot_layout(plot_obj){
            return {
                width: plot_obj.clientWidth,
                height: 350,
                margin: c.plot_margin_ref(plot_obj),
                paper_bgcolor: "transparent",
                plot_bgcolor: "transparent",
                title: {
                    text: this.$i18n.t('AIAnalysis.module_cleaning.歷史髒污累積圖'),
                    font: {
                        size: 10,
                    },
                },
                xaxis: {
                    title:{
                        text: this.$i18n.t('AIAnalysis.module_cleaning.時間'),
                    }
                },
                yaxis: {
                    title: {
                        text: 'Rate',
                    }
                },
                legend: {
                    orientation: "h",
                    x: 0,
                    y: -0.5
                }
            }
        },
        plot_resize(){
            if('plot_div' in this.$refs){
                this.Plotly.relayout(this.$refs.plot_div, this.get_plot_layout(this.$refs.plot_div))
                c.plot_text_color_fix(this.$refs.plot_div)
            }
        },
        create_dispatch(){
            // 按下新增排成或警報時，時間會是日曆的時間
            if(this.dispatch_date != null){
                const offset = this.dispatch_date.getTimezoneOffset()
                let selectDate = new Date(this.dispatch_date.getTime() - (offset*60*1000))
                this.$refs.schedule_modal.schedule_form.starttime = selectDate.toISOString().split('T')[0]
            }
            this.$refs.schedule_modal.open_modal_blank({
                ID: this.station_ID,
                plant_search: this.station_name,
                schedule_type: 'wash'
            })
        }
    },
    watch: {
        '$store.state.language': function() {
            this.plot_resize()
        }
    },
    mounted(){
        window.addEventListener("resize", this.plot_resize)
    },
    unmounted(){
        window.clearTimeout(this.sync_data)
        window.removeEventListener("resize", this.plot_resize)
    }
}
</script>