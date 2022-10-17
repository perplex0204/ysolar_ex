<template>
    <div class="card col-12 col-lg-8 p-0 mt-3 me-2 shadow">
        <div class="compare_container"  v-loading="loading">
            <div style="display: flex; align-items: center; padding: 1rem;">
                <el-select v-model="date_range" v-if="date_range !== -1" placeholder="Select" class="date_type_selection">
                    <el-option
                    v-for="item in options"
                    :key="item.value"
                    :label="$t(`option.${item.label}`)"
                    :value="item.value"
                    >
                    </el-option>
                </el-select>
                <el-button size="large" type="primary" @click="online_download_compare">
                    CSV
                </el-button>
            </div>
            <div id="plot_compare"></div>
        </div>
    </div>
</template>


<script>
import c from 'assets/js/common.js'

export default {
    name: "compareChart",
    data() {
        return {
            date_range: 1,
            loading: false,
            options: [{
                value: 1,
                label: '日'
            },{
                value: 2,
                label: '月'
            }, {
                value: 3,
                label: '年'
            },{
                value: 4,
                label: '歷年'
            }],
            data_length: 0,
        }
    },
    methods: {
        get_plot_data(){
            let that = this
            this.loading = true
            this.axios.post('/get_home_page_compare_data', {
                date_range: this.date_range
            }).then(function(response) {
                let data = response.data.data.data
                console.log(data)
                that.data_length = data["y_axis"].length
                let taipower_names = []
                if (that.$store.state.user_data.pageType == 'taipower'){
                    for (var i=0; i<data["name_list"].length; i++){
                        taipower_names.push(data["name_list"][i].split("_")[1])
                    }
                }
                that.plot(data["x_axis"], data["y_axis"], data["name_list"], taipower_names)
            })
        },
        online_download_compare() {
            // this.get_plot_data()
            var csvList = []
            var memberContent = ""
            var csvContent
            let title = "發電量比較"
            let select = this.options.find(element => element.value == this.date_range)

            title = title + "_" + select.label
            let filename = title + ".csv"

            var gd = document.getElementById("plot_compare")
            var regList = ["number", "time"]
            var all_data_length = gd.data.length
            for (var i = 0; i < all_data_length; i++) {
                // console.log(gd.data[i])
                regList.push(gd.data[i].name)
            }
            csvList.push(regList)

            var x = gd.data[0].x

            for (var j = 0; j < x.length; j++) {
                var regList = []
                regList.push(j + 1)
                regList.push(x[j])
                for (var i = 0; i < gd.data.length; i++) {
                    // regList.push(gd.data[i].y[j])
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
        plot(x, y, names, taipower_names=[]) {
            const MyPlot = document.getElementById('plot_compare')
            MyPlot.innerHTML = ""
            var data = []
            for (var i=0; i<names.length; i++) {
                data.push({
                    x: x,
                    y: y[names[i]],
                    mode: "lines",
                    name: this.$store.state.user_data.pageType != 'taipower' ? names[i] : taipower_names[i]
                })
            }

            // console.log(data)
            var layout = {
                title: {
                    text: this.$i18n.t("setting.widget.compareChart"),
                    font: {
                        family: "Courier New, monospace",
                        size: this.$store.state.isMobile ? 15 : 30,
                    },
                },
                yaxis: {
                    title: {
                        text: this.$i18n.t("plot.發電量")+"(kWh)",
                    },
                },
                width: MyPlot.clientWidth,
                height: MyPlot.clientHeight,
                margin: this.plot_margin(),
                legend:{
                    x: this.$store.state.isMobile ? 0 : 1,
                    y: this.$store.state.isMobile ? -2 : 1
                },

                // hovermode: "closest",
                // hoverlabel: {
                //     bgcolor: "#FFFFFF",
                //     bordercolor: "#888888",
                //     font: {
                //         color: "#000000",
                //     },
                // },
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
            this.loading = false
        },
        plot_resize() {
            let update = {
                width: "",
                heigth: "",
            }
            update = {
                width: document.getElementById('plot_compare').clientWidth,
                height:  400,
                legend:{
                    x: 1,
                    y: 1,
                },
                margin: this.plot_margin(),
                title: {
                    text:  this.$i18n.t("setting.widget.compareChart"),
                    font: {
                        family: "Courier New, monospace",
                        size: this.$store.state.isMobile ? 15 : 30,
                    },
                },
                yaxis: {
                    title: {
                        text: this.$i18n.t("plot.發電量")+"(kWh)",
                    },
                },
            }
            if(document.getElementById('plot_compare').clientWidth < 576){
                update.heigth = document.getElementById('plot_compare').clientHeight
                update.legend.x = 0
                update.legend.y = -2
            }
            try{
                this.Plotly.relayout("plot_compare", update)
                c.plot_text_color_fix(document.getElementById(("plot_compare")))
            }
            catch{
                return false
            }
        },
        plot_margin(){
            let margin =  {
                l: 70,
                r: 50,
                b: 50,
                t: 50,
                pad: 20,
            }
            if(document.getElementById('plot_compare').clientWidth < 550){
                margin.l = 40
                margin.r = 30
                margin.pad = 0
                // margin.pad.b = 0
            }
            return margin
        },
    },
    watch: {
        date_range() {
            this.get_plot_data()
        },
        '$store.state.navOpen': function() {
            if(!this.$store.state.isMobile) {
                this.plot_resize()
            }
        },
        '$store.state.language': function() {
            this.plot_resize()
        }
    },
    mounted() {
        this.get_plot_data()
        window.addEventListener("resize", this.plot_resize)
    },
    unmounted(){
        window.removeEventListener("resize", this.plot_resize)
    }
}
</script>

<style scoped>
.date_type_selection{
    margin-right: 1rem;
}
#plot_compare{
    position: relative; 
    padding: 1rem; 
    padding-bottom: 0;
    min-height: 450px;
    max-height: 500px;
    max-width: 95%;
    border-radius: .5rem;
}
.compare_container{
    height: 550px;
    max-height: 650px;
    position: relative;
    min-width: 80%;
    border-radius: .5rem;
    /* box-shadow: 0 0 15px #DEE4EA; */
}
@media(max-width: 991px){
    .compare_container{
        height: 650px;
        max-height: 750px;
    }
    #plot_compare{
        min-height: 550px;
        max-height: 550px;
        max-width: 95%;
        padding-bottom: 0
    }
}
</style>