<template>
    <div class="ms-2 mt-2 ms-lg-2 mt-lg-0 mb-4 mb-lg-0 mt-lg-0 ps-3 ps-lg-4 pt-3 me-lg-0">
        <div class="d-flex flex-wrap">
            <!-- <div class="fw-bold fs-2">{{stationData.name}}</div> -->
            <div class="col-12 col-lg-6 mb-4 mb-lg-4" v-if="Object.keys(weather_data).length > 0">
                <!--天氣-->
                <div class="col-12 col-lg-12 d-flex pe-4 pe-lg-0 mb-lg-4">
                    <div class="card col-12 col-lg-12 weather_card">
                        <div class="d-flex flex-wrap align-items-center">

                            <!--天氣 if taipower-->
                            <div class="col-12 col-lg-12 p-2 pb-0 p-lg-2" v-if="$store.state.user_data.pageType == 'taipower' && !$store.state.isMobile">
                                <div class="d-flex flex-wrap justify-content-start">
                                    <img class="col-5 col-sm-3 col-md-2 col-lg-1 weather-icon" :src="weather_data.imgurl" />
                                    <!-- 溫度 -->
                                    <div class="d-flex flex-column">
                                        <label class="fs-5 temp-color" :style="weatherStyleTaipower">
                                            <!-- 溫度 -->
                                            {{weather_data.temperature}}°C
                                        </label>
                                    </div>

                                    <!-- 晴陰雨 -->
                                    <div class="fs-5 ms-lg-auto mt-1">
                                        {{
                                            weather_data.status[$store.state.language] == undefined ?
                                            weather_data.status['zh-TW'] : weather_data.status[$store.state.language]
                                        }}
                                    </div>

                                    <!-- 降雨機率 -->
                                    <div class="d-flex align-top ms-lg-auto mt-1">
                                        <label class="me-2 fs-5 text-center" :class="{'water-color':  weather_data.rain > 0}">
                                            <label class="text-danger">
                                                {{$t("降雨機率")}}：
                                            </label>
                                            {{weather_data.rain}}%
                                        </label>
                                    </div>
                                    
                                </div>
                            </div>
                        </div>
                    </div>
                </div>

                <!--狀態欄 taipower-->
                <div class="card statab_status col-11 col-lg-12 d-flex flex-wrap text-center" v-if="text_colors.length > 0 && $store.state.user_data.pageType == 'taipower' && !$store.state.isMobile">
                    <div class="col-12 col-lg-6 py-2" v-for="(item, index) in status_data" :key="index">
                        <!-- title -->
                        <div class="fs-6">
                            <i :class="['icon-'+item.icon, text_colors[index]]"></i>{{$t(`stationData.overview.${item.title}`)}}
                        </div>
                        <!-- 中間綠色大字1、2 -->
                        <div class="fs-6 py-0 text-center" :class="text_colors[index]" v-if="index<2">{{$t(`stationData.overview.${item.text}`)}}</div>
                        <!-- 中間綠色大字3、4 -->
                        <div class="fs-6 py-0 text-center" :class="text_colors[index]" v-if="index>1">{{item.text}}</div>
                    </div>
                </div>
            </div>

            <div class="col-12 col-lg-6">
                <div id="plot_today"></div>  
            </div>
        </div>
    </div>
</template>

<script>
export default {
    name: "overview",
    data() {
        return {
            weather_data: {},
            status_data: [],
            statabs: ["發電狀態", "4G通訊狀態", "DMY", "警報數"],
            text_colors: [],
            loading: false,
            statusStyle: {},
            statusStyle_title: {},
            statusStyle_time: {}
            // plot_data: {}
        }
    },
    props: {
        stationData: {
            type: Object,
            required: true
        },
    },
    methods: {
        async get_information_data() {
            let that = this
            this.axios.post('/get_basic_data_locale', {
                ID_list: [this.stationData.ID],
                col_list: [this.stationData.collection]
            }).then(function(data){
                console.log(data.data.data[0])
                var response = data.data.data[0]
                that.weather_data = response.weather
                console.log('that.weather_data:',that.weather_data)
                that.status_data = [
                    {
                        error: response.led_state == 0 ? false : true,
                        title: "發電狀態",
                        icon: "ttl_thunder",
                        text: response.led_state == 0 ? "發電正常" : response.led_state == 1 ? "一級警報" : response.led_state == 2 ?
                        "二級警報" : response.led_state == 3 ? "斷線" : null
                    },
                    {
                        error: !response.communi,
                        title: "4G通訊",
                        icon: "ttl_mail",
                        text: response.communi == true ? "正常" : "斷訊",
                        text2: "最後通訊時間",
                        time: response.lastTime_i18n
                    },
                    {
                        error: false,
                        title: "DMY",
                        icon: "ttl_time",
                        text: response.dmy
                    },
                    {
                        error: response.alert_count > 0,
                        title: "警報數",
                        icon: "ttl_alert",
                        text: response.alert_count
                    },
                ]
                for (var i=0; i<that.status_data.length; i++) {
                    if(that.status_data[i].error == true){
                        that.text_colors.push("text-danger")
                    }
                    else{
                        that.text_colors.push("text-success")
                    }
                }
                if (that.text_colors.indexOf("text-danger") > -1){
                    for (var i=0; i<that.text_colors.length; i++) {
                        if(that.text_colors[i] == "text-success"){
                            that.text_colors[i] = "text-primary"
                        }
                    }
                }
                that.get_status_style()
            })
        },
        async get_plot_data() {
            let that = this
            this.loading = true
            this.axios.post('/overview_get_today_power', {
                ID: this.stationData.ID
            }).then(function(data){
                console.log(data.data.data.data)
                var plot_data = data.data.data.data
                that.plot_today(plot_data.x_axis, plot_data.y_axis)
            })
        },
        // plot_today(x, y) {
        plot_today() {
            const MyPlot = document.getElementById('plot_today')
            MyPlot.innerHTML = ""

            // 力暘展示用
            var test_data = {
                "x_axis": [
                    "2022-09-24 00",
                    "2022-09-24 01",
                    "2022-09-24 02",
                    "2022-09-24 03",
                    "2022-09-24 04",
                    "2022-09-24 05",
                    "2022-09-24 06",
                    "2022-09-24 07",
                    "2022-09-24 08",
                    "2022-09-24 09",
                    "2022-09-24 10",
                    "2022-09-24 11",
                    "2022-09-24 12",
                    "2022-09-24 13",
                    "2022-09-24 14",
                    "2022-09-24 15",
                    "2022-09-24 16",
                    "2022-09-24 17",
                    "2022-09-24 18",
                    "2022-09-24 19",
                    "2022-09-24 20",
                    "2022-09-24 21",
                    "2022-09-24 22",
                    "2022-09-24 23"
                ],
                "y_axis": [
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    20.000000000116415,
                    82.19999999983702,
                    151.60000000009313,
                    203.39999999990687,
                    244.20000000018626,
                    190.89999999979045,
                    151.60000000009313,
                    162.19999999983702,
                    173,
                    160,
                    130,
                    111,
                    75,
                    10,
                    0,
                    0,
                    0,
                    0
                ]
            }
            // 力暘展示用
            var data =[]
            data.push({
                x:test_data['x_axis'],
                y:test_data['y_axis'],
                type:'bar',
                marker: {
					size: 8,
					color: '#93FF93'
				},
            })
            // data.push({
            //     x: x,
            //     y: y,
            //     type: "bar",
            // })
            
            var layout = {
                paper_bgcolor: 'rgba(0,0,0,0)',
				plot_bgcolor: 'rgba(0,0,0,0)',
                width:308.38,
				height:230,
                margin: {
					l: 60,
					r: 20,
					b: 40,
					t: 25,
					pad: 10
				},
                title: {
                    text: this.$i18n.t("plot.今日發電量"),
                    font: {
						family: " STHeiti,Copperplate,Courier New",
						size: 15,
						color:'#ffffff'
					},
                },
                yaxis: {
                    title: {
                        text: this.$i18n.t("plot.發電量")+"(kWh)",
                        font:{
							color:'#ffffff',
							family: "STHeiti,Copperplate,Courier New",
					},
                    },
                    "gridcolor":"rgba(224,224,224,0.5)",
                    rangemode: 'nonnegative',
                },
                xaxis: {
                    title: {
                        text: this.$i18n.t("plot.時間"),
                        font:{
							color:'#ffffff',
							family: "STHeiti,Copperplate,Courier New",
					},
                    },
                },
                autoMargin: true,
            }
            var config = {
				// 下面這兩個應該是類似參數設定，不太確定
				displaylogo: false,
				modeBarButtonsToRemove: [
					"sendDataToCloud",
					"hoverClosestCartesian",
					"hoverCompareCartesian",
					"toggleSpikelines",
					"pan2d",
					"lasso2d",
					"zoomIn2d",
					"zoomOut2d",
					"autoScale2d"
				],
			}
            this.Plotly.newPlot(MyPlot, data, layout, config)
            this.loading = false
        }
    },
    mounted() {
        this.get_information_data()
        this.get_plot_data()
    },
}

</script>
<style scoped>
.statab_status{
    flex-direction: row;
}
.statab_status>div{
    position: relative;
    border-right: 1px solid #dee4ea;
    border-bottom: 1px solid #dee4ea;
}
.statab_status>div:nth-child(2){
    border-right: 0;
}
.statab_status>div:nth-child(3){
    border-bottom: 0;
}
.statab_status>div:nth-child(4){
    border-right: 0;
    border-bottom: 0;
}
</style>