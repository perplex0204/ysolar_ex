<template>
    <div :class="{'card': !embed, 'p-4': !embed}">
        <h5 v-if="!embed"><i class="fa-solid fa-chart-bar text-primary me-2"></i>{{$t('dispatch.統計')}}</h5>
        <div class="d-flex flex-column" v-if="Object.keys(archive_data).length != 0">
            <h6><i class="fa-solid fa-industry text-success me-2"></i>{{$t('dispatch.案場篩選')}}：
            {{this.stationId == null ? $t('全部') : archive_data.select_station_name}}
            </h6>
            <div class="w-100 d-flex justify-content-center mb-3" v-if="this.stationId == null">
                <div class="col-12 col-lg-10" style="max-height: 250px; overflow-y: scroll">
                    <div class="table-responsive">
                        <table class="table table-striped">
                            <thead>
                                <tr>
                                    <th scope="col">{{$t('電站')}}</th>
                                    <th scope="col">{{$t('dispatch.總派工次數')}}</th>
                                </tr>
                            </thead>
                            <tbody>
                                <tr v-for="data, ID in archive_data.station_dispatch_count" :key="ID">
                                    <td>
                                        {{data.name}}
                                    </td>
                                    <td>
                                        {{data.count}}
                                    </td>
                                </tr>
                            </tbody>
                        </table>
                    </div>
                </div>
            </div>
            <h6><i class="fa-solid fa-clock text-success me-2"></i>{{$t('dispatch.時間篩選')}}：
            {{get_date_str}}
            </h6>
            <div class="d-flex flex-wrap align-items-center mb-2">
                <div class="col-12 col-lg-4 p-2 d-flex flex-column align-items-center">
                    <i class="icon-nav_works fs-5"></i>
                    {{$t('dispatch.總派工次數')}}
                    <div class="round-container border border-primary mt-3 d-flex flex-wrap align-items-center justify-content-center">
                        <h4>{{archive_data.total_dispatch_count}}</h4>
                        <h6 class="ms-1">{{$t('dispatch.次')}}</h6>
                    </div>
                </div>
                <div class="col-12 col-lg-4 p-2 d-flex flex-column align-items-center">
                    <i class="icon-wrench fs-5"></i>
                    {{$t('dispatch.type.regular')}}/{{$t('dispatch.type.wash')}}
                    <div class="round-container border border-primary mt-3 d-flex flex-wrap align-items-center justify-content-center">
                        <h4>{{archive_data.dispatch_type_stat.regular + archive_data.dispatch_type_stat.wash}}</h4>
                        <h6 class="ms-1">{{$t('dispatch.次')}}</h6>
                    </div>
                </div>
                <div class="col-12 col-lg-4 p-2 d-flex flex-column align-items-center">
                    <i class="icon-nav_alert fs-5"></i>
                    {{$t('dispatch.type.alarm')}}
                    <div class="round-container border border-primary mt-3 d-flex flex-wrap align-items-center justify-content-center">
                        <h4>{{archive_data.dispatch_type_stat.alarm}}</h4>
                        <h6 class="ms-1">{{$t('dispatch.次')}}</h6>
                    </div>
                </div>
            </div>
            <h6 class="mb-4"><el-icon class="text-success me-2"><money/></el-icon>{{$t('dispatch.總維運成本')}}：
                {{archive_data.auto_review_cost_total}}
            </h6>
            <div v-if="!embed">
                <h6><i class="fa-solid fa-clock text-success me-2"></i>{{$t('dispatch.時序圖')}}</h6>
                <div class="w-100 text-center mb-4" v-if="archive_data.sequence_data.length == 0">
                    {{$t('無資料')}}
                </div>
                <div ref="sequence_diagram" class="w-100 mb-4" style="max-width: 100%;" v-else></div>
            </div>
            <div v-if="!embed">
                <h6><i class="fa-solid fa-chart-pie text-success me-2"></i>{{$t('dispatch.警報檢修分析')}}</h6>
                <div class="w-100 text-center" v-if="archive_data.no_alarm">
                    {{$t('無警報')}}
                </div>
                <div ref="alarm_pie" class="w-100 mb-4" style="max-width: 100%;" v-else></div>
            </div>
        </div>
        <div class="d-flex justify-content-center w-100" v-else>
            <div class="spinner-border text-primary" role="status">
                <span class="visually-hidden">Loading...</span>
             </div>
        </div>
    </div>
</template>

<script>
import { Money } from '@element-plus/icons-vue'
import c from '@/assets/js/common.js'

export default {
    name: "stats",
    props: {
        stationId : {
            default: null
        },
        dateSelect: {
            type: Object,
            default: ()=>{
                return {}
            }
        },
        embed: {
            default: false
        }
    },
    components: {
        Money
    },
    data(){
        return {
            archive_data: {}
        }
    },
    methods: {
        get_dispatch_archive_data(reload_plot=false){
            this.axios.post('/get_dispatch_archive_data', {
                ID: this.stationId,
                dispatch_time: this.dateSelect
            }).then(data=>{
                //console.log(data.data.data)
                this.archive_data = data.data.data
                if(reload_plot){
                    this.plot_sequence_diagram()
                    this.plot_alarm_pie()
                }
            })
        },
        plot_sequence_diagram(){
            // sequence_diagram
            let sequence_data = []
            this.archive_data.sequence_data.forEach(element => {
                if(element.overview)
                    sequence_data.push({
                        x: element.x,
                        y: element.y,
                        name: element.name,
                        hovertemplate: 
                            '%{x}<br>' +
                            '%{y}<br>'
                    })
                else
                    sequence_data.push({
                        x: element.x,
                        y: element.y,
                        name: '',
                        hovertemplate: 
                            '%{x}<br>' +
                            '%{y}<br>'
                    })
            })
            window.setTimeout(()=>{
                let plot_obj = this.$refs.sequence_diagram
                this.Plotly.newPlot( plot_obj, sequence_data, this.get_sequence_layout(plot_obj),
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
            }, 100)
        },
        plot_alarm_pie(){
            window.setTimeout(()=>{
                let plot_obj = this.$refs.alarm_pie
                this.archive_data.alarm_pie_data = Object.assign(this.archive_data.alarm_pie_data, {
                    textinfo: "label+percent",
                    textposition: "outside",
                    automargin: true,
                    hole: .4
                })
                this.Plotly.newPlot( plot_obj, [this.archive_data.alarm_pie_data], this.get_pie_layout(plot_obj),
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
            }, 100)
        },
        plot_resize(){
            window.setTimeout(()=>{
                if('sequence_diagram' in this.$refs){
                    this.Plotly.relayout(this.$refs.sequence_diagram, this.get_sequence_layout(this.$refs.sequence_diagram))
                    c.plot_text_color_fix(this.$refs.sequence_diagram)
                }
                if('alarm_pie' in this.$refs){
                    this.Plotly.relayout(this.$refs.alarm_pie, this.get_pie_layout(this.$refs.alarm_pie))
                    c.plot_text_color_fix(this.$refs.alarm_pie)
                }
            }, 400)
        },
        get_sequence_layout(plot_obj){
            return {
                width: plot_obj.clientWidth,
                height: 350,
                margin: c.plot_margin_ref(plot_obj),
                paper_bgcolor: "transparent",
                plot_bgcolor: "transparent",
                showlegend: false,
                yaxis: {
                    automargin: true,
                    showgrid: false
                }
            }
        },
        get_pie_layout(plot_obj){
            return {
                width: plot_obj.clientWidth,
                height: 350,
                margin: c.plot_margin_ref(plot_obj),
                paper_bgcolor: "transparent",
                plot_bgcolor: "transparent",
                legend: {orientation: this.$store.state.isMobile? "h": "v"}
            }
        }
    },
    mounted(){
        this.get_dispatch_archive_data(true)
        this.sync_data = window.setInterval(this.get_dispatch_archive_data, 10000)
        window.addEventListener("resize", this.plot_resize)
    },
    unmounted(){
        window.clearInterval(this.sync_data)
        window.removeEventListener("resize", this.plot_resize)
    },
    watch: {
        stationId(){
            this.archive_data = {}
            this.get_dispatch_archive_data(true)
        },
        dateSelect(){
            this.archive_data = {}
            this.get_dispatch_archive_data(true)
        }
    },
    computed: {
        get_date_str(){
            if(Object.keys(this.dateSelect).length == 0){
                return this.$i18n.t('全部')
            }
            switch(this.dateSelect.mode){
                case "all": 
                    return this.$i18n.t('全部')
                case "today":
                    return this.$i18n.t('本日')
                case "week":
                    return this.$i18n.t('本週')
                case "month":
                    return this.$i18n.t('本月')
                case "year":
                    return this.$i18n.t('本年')
                case "single":
                    return this.dateSelect.start_date
                case "interval":
                    return `${this.dateSelect.start_date} ~ ${this.dateSelect.end_date}`
            }
            return this.$i18n.t('全部')
        }
    }
}
</script>

<style scoped>
.round-container{
    width: 150px;
    height: 150px;
    border-radius: 50%;
}
</style>
