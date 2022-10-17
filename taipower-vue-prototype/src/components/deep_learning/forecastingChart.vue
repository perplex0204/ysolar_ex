<template>
    <div class="card">
        <div class="stbigimg shadow">
            <el-button :size='csvsize' type="primary" class="mt-3 ms-4" @click="online_download">
                CSV
            </el-button>
            <div id="plot_div"></div>
        </div>
    </div>
</template>


<script>
import c from 'assets/js/common.js'

export default {
    name: "forecastingChart",
    data() {
        return {
            name: "",
            screenWidth: document.body.clientWidth,
            csvsize: "large"
        }
    },
    props: {
        ID: {type: String, required: true},
        date_selection: {type: Array, required: true},
        place_select: {type: Boolean, required: true},
        place: {type: String, required: true},
        mode: {type: String, required: true, default: 'today'}
    },
    methods: {
        get_forecasting_data() {
            let that = this
            console.log(this.ID)
            this.axios.post('get_power_forecasting_data', {
                "ID": this.ID,
                "datepicker1": this.date_selection[0],
                "datepicker2": this.date_selection[1],
                "mode": this.mode
            }).then(data => {
                console.log(data.data.data.data.data)
                var plot_data = data.data.data.data.data
                if (plot_data["time"].length > 0) {
                    if (plot_data["time"][0].split(" ")[0] == plot_data["time"][plot_data["time"].length-1].split(" ")[0]){
                        that.name = that.place+"_"+plot_data["time"][0].split(" ")[0]
                    }
                    else {
                        that.name = that.place+"_"+plot_data["time"][0].split(" ")[0]+"_"+plot_data["time"][plot_data["time"].length-1].split(" ")[0]
                    }
                }
                that.plot_forecasting(plot_data["output_kwh"], plot_data["real_kwh"], plot_data["time"])
            })
        },
        plot_forecasting(forecasting_data, real_data, time) {
            const MyPlot = document.getElementById('plot_div')
            MyPlot.innerHTML = ""
            var color = [
                "black",
                "darkred",
                "darkorange",
                "olive"
            ]
            var data = []
            data.push({
                type: "scatter",
                mode: "lines",
                x: time,
                y: real_data,
                name: this.$i18n.t("plot.實際輸出功率"),
                yaxis: "y",
                line: { 
                    color: color[0],
                    shape: 'linear'
                },
                marker: {
                    size: 8
                }
            })
            data.push({
                type: "scatter",
                mode: "lines",
                x: time,
                y: forecasting_data,
                name: this.$i18n.t("plot.預測輸出功率"),
                yaxis: "y",
                line: { 
                    color: color[1],
                    shape: 'linear',
                    dash: 'dot'
                },
                marker:{
                    size: 8
                }
            })
            var layout = {
                title: {
                    text: this.name,
                    font: {
                        family: "Courier New, monospace",
                        size: this.$store.state.isMobile ? 10 : 25
                    },
                },
                xaxis: {
                    // domain: [0.1, 0.94],
                    // anchor: "free",
                    // position: 0,
                },
                yaxis: {
                    title: {
                        text: this.$i18n.t("plot.功率")+"(kWh)",
                    },
                },
                margin: {
                    l: 70,
                    t: 50,
                    pad: 10,
                },
                width: document.getElementById("plot_div").clientWidth,
                height: document.getElementById("plot_div").clientHeight,
                legend:{
                    x: this.$store.state.isMobile ? 0 : 1,
                    y: this.$store.state.isMobile ? -0.4 : 1
                },

                hovermode: "closest",
                hoverlabel: {
                    bgcolor: "#FFFFFF",
                    bordercolor: "#888888",
                    font: {
                        color: "#000000",
                    },
                },
                paper_bgcolor: "transparent",
                plot_bgcolor: "transparent"
            }
            this.Plotly.newPlot(MyPlot, data, layout, {
                displaylogo: false,
                modeBarButtonsToRemove: [
                "sendDataToCloud",
                "hoverClosestCartesian",
                "hoverCompareCartesian",
                "toggleSpikelines",
                ],
            })
            c.plot_text_color_fix(MyPlot)
        },
        online_download(){
            var csvList = []
            var memberContent = ""
            var csvContent
            let title = this.$i18n.t('AIAnalysis.tabs.power_forecasting')+"_"+this.name

            let filename = title + ".csv"

            var gd = document.getElementById("plot_div")
            if (gd.data == undefined) {
                return false
            }
            var regList = ["number", "time"]
            regList.push(this.$i18n.t("plot.實際輸出功率"))
            regList.push(this.$i18n.t("plot.預測輸出功率"))
            csvList.push(regList)

            var x = gd.data[0].x

            for (var j = 0; j < x.length; j++) {
                var regList = []
                regList.push(j + 1)
                regList.push(x[j])
                for (var i = 0; i < gd.data.length; i++) {
                    regList.push(gd.data[i].y[j])
                    
                }
                csvList.push(regList)
            }

            //console.log(csvList)

            // 產生 csv 內容
            csvList.forEach(function (rowArray) {
                var row = rowArray.join(",")
                memberContent += row + "\r\n"
            })

            // 產生 csv Blob
            csvContent = URL.createObjectURL(
                new Blob(["\uFEFF" + memberContent], {
                    type: "text/csv;charset=utf-8;",
                })
            )
            // 產生 csv 連結
            var link = document.createElement("a")
            document.body.appendChild(link)
            link.href = csvContent
            link.download = filename
            link.click()
            document.body.removeChild(link)
        },
        plot_resize() {
            this.csvsize = "large"
            let update = {
                width: "",
                heigth: "",
            }
            update = {
                width: document.getElementById('plot_div').clientWidth,
                height:  document.getElementById('plot_div').clientHeight,
                title: {
                    text: this.name,
                    font: {
                        family: "Courier New, monospace",
                        size: this.$store.state.isMobile ? 10 : 25,
                    },
                },
                yaxis: {
                    title: {
                        text: this.$i18n.t("plot.功率")+"(kWh)",
                    },
                },
                legend:{
                    x: this.$store.state.isMobile ? 0 : 1,
                    y: this.$store.state.isMobile ? -0.4 : 1
                },
                margin: {
                    l: 70,
                    t: 50,
                    pad: 10,
                }
            }
            let update_style = {
                name: [this.$i18n.t("plot.實際輸出功率"), this.$i18n.t("plot.預測輸出功率")]
            }
            if(document.getElementById('plot_div').clientWidth < 576){
                this.csvsize = "small"
            }
            try{
                this.Plotly.relayout("plot_div", update)
                this.Plotly.restyle("plot_div", update_style)
                c.plot_text_color_fix(document.getElementById('plot_div'))
            }
            catch{
                return false
            }
        },
        plot_delay(){
            window.setInterval(() => {
                this.plot_resize()
            }, 500)
        },
    },
    watch: {
        date_selection() {
            if (this.place_select == true) {
                this.get_forecasting_data()
            }
        },
        "$store.state.language": function() {
            this.plot_resize()
        },
        "$store.state.navOpen": function() {
            if(!this.$store.state.isMobile) {
                this.plot_delay()
            }
        },
        ID() {
            if(this.place_select == true){
                this.get_forecasting_data()
            }
        }
    },
    mounted() {
        let that = this
        window.addEventListener("resize", this.plot_resize)
        window.addEventListener("resize", function() {
            return (() => {
                that.screenWidth = this.document.body.clientWidth
            })()
        })
        if (this.screenWidth>=576) {
            this.csvsize = "large"
        }
        else {
            this.csvsize = "small"
        }
    },
    unmounted() {
        window.removeEventListener("resize", this.plot_resize)
    }
}
</script>
<style scoped>
#plot_div{
    position: relative; 
    padding: 1rem; 
    min-height: 460px;
    max-height: 460px;
    width: 95%;
    max-width: 95%
}
.stbigimg{
    position: relative;
	width: 100%;
	min-height: 65vh;
	border-radius: 1rem;
	box-shadow: 0 0 15px #DEE4EA;
	overflow: hidden;
}
@media (max-width: 991px){
    #plot_div{
        padding: 0rem;
        min-height: 500px;
        max-height: 600px;
        width: 100%;
        max-width: 100% 
    }
    .stbigimg{
        width: 100%;
    }

}
</style>