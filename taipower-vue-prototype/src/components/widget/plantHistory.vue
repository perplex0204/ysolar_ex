<template>
    <div class="card col-12 col-lg-8 p-0 mt-3 me-2 shadow">
        <div class="history_container"  v-loading="loading">
            <div style="display: flex; align-items: center; padding: 1rem;">
                <!-- <label style="color: #656D74; margin-right: auto;">{{
                    dataName
                }}</label> -->
                    <el-select v-model="date_range" v-if="date_range == -1" placeholder="Select" class="date_type_selection">
                    <el-option
                    v-for="item in options"
                    :key="item.value"
                    :label="$t(`option.${item.label}`)"
                    :value="item.value"
                    >
                    </el-option>
                </el-select>
                <el-button size="large" type="primary" @click="oneline_download">
                    CSV
                </el-button>
            </div>
            <div id="plot_div"></div>
            <div class="el_table_container" style="margin: .5rem; max-width: 99%;"
            v-if="statTableShow">
                <el-table :data="tableData">
                    <el-table-column
                        v-for="(item, i) in tableHead"
                        :key="i"
                        align="center"
                        :prop="item.prop"
                        :label="item.label"
                        min-width="40"
                    >
                    </el-table-column>
                </el-table>
            </div>
            <div class="time_range_selector" style="margin-left: .5rem;">
                <timeRangePicker @setDate="setDate" />
            </div>
        </div>
    </div>
</template>
<script>
import timeRangePicker from "@/components/datepicker/timeRangePickerSingle.vue";
import c from 'assets/js/common.js'

export default {
    name: "plantHistory",
    components: {
        timeRangePicker
    },
    props:{
        dataName: {type: String},
        dataType: {type: String},
        dataCollection: {type: String},
        dataId: {type: String},
        parentName: {type: String},
        statTableShow: {type: Boolean, default:false}
    },
    data(){
        return {
            date_selection: {},
            options: [{
                value: 1,
                label: '日'
            }, {
                value: 2,
                label: '月'
            },{
                value: 3,
                label: '年'
            },{
                value: 4,
                label: '歷年'
            }],
            date_range: 1,
            loading: true,
            tableHead: [{
                lable: '',
                prop: 'datatype'
            },
            {
                lable: '最大值',
                prop: 'max'
            }],
            tableData: [],
        }
    },
    methods: {
        plot(plot_obj, that, x, y, title, name, type, y_title, pf = false) {
            //console.log(id)
            //console.log(x)
            //console.log(y)
            if (pf == false) {
                var trace1 = {
                    type: type,
                    mode: "lines",
                    name: name,
                    x: x,
                    y: y,
                    line: { color: "#17BECF" },
                }
                var yaxis_set = {
                    title: {
                        text: y_title,
                    },
                    rangemode: "tozero",
                    autorange: true,
                    type: "linear",
                }
            } else {
                var text = []
                for (var i in y) {
                    text.push(y[i])
                }
                y = that.pfvalue(y)

                var trace1 = {
                    type: type,
                    mode: "lines",
                    name: name,
                    hoverinfo: "text",
                    x: x,
                    y: y,
                    text: text,
                    line: { color: "#17BECF" },
                }
                var yaxis_set = {
                    title: {
                        text: y_title,
                    },
                    autorange: true,
                    type: "linear",
                    tickmode: "array", // If "array", the placement of the ticks is set via `tickvals` and the tick text is `ticktext`.
                    tickvals: [-1, -0.75, -0.5, -0.25, 0, 0.25, 0.5, 0.75, 1],
                    ticktext: [
                        "0(lag)",
                        "-0.25",
                        "-0.5",
                        "-0.75",
                        "1",
                        "0.75",
                        "0.5",
                        "0.25",
                        "0(lead)",
                    ],
                }
            }

            var data = [trace1]
            var layout = {
                title: {
                    text: title,
                    font: {
                        family: "Courier New, monospace",
                        size: 30,
                },
                },
                xaxis: {},
                yaxis: yaxis_set,
                width: plot_obj.clientWidth,
                height: plot_obj.clientHeight,
                margin: c.plot_margin(),
                paper_bgcolor: "transparent",
                plot_bgcolor: "transparent"
            }
            this.Plotly.newPlot(plot_obj, data, layout, {
                displaylogo: false,
                modeBarButtonsToRemove: [
                "sendDataToCloud",
                "hoverClosestCartesian",
                "hoverCompareCartesian",
                "toggleSpikelines",
                ],
            })
            c.plot_text_color_fix(plot_obj)
        },
        history_info(that, x, min, max, avg, total, _datatype, datatype, num = 1) {
            //console.log(x, min, max, avg, total)
            num = 5
            that.tableHead = []
            that.tableData = []
            for (var i in min) {
                var minimum = c.round(min[i]["value"], num)
                var min_time_index = min[i]["time"]
                var maximum = c.round(max[i]["value"], num)
                var max_time_index = max[i]["time"]
                var avg_num = c.round(avg[i]["value"], 3)
                var total_num = c.round(total[i]["value"], 3)

                if (min_time_index != null) {
                    var min_time = x[min_time_index]
                } else {
                    var min_time = "---"
                }
                if (max_time_index != null) {
                    var max_time = x[max_time_index]
                } else {
                    var max_time = "---"
                }
                //console.log(datatype)
                if (datatype == "kwh") {
                    that.tableHead = [{
                        prop: 'datatype',
                        lable: ''
                        },
                        {
                            prop: 'min',
                            label: '最小值',
                        },
                        {
                            prop: 'max',
                            label: '最大值',
                        },
                        {
                            prop: 'avg',
                            label: '平均值',
                        },
                        {
                            prop: 'total',
                            label: '加總值',
                        }
                    ]
                    that.tableData.push({
                        datatype: Array.isArray(_datatype) ? _datatype[i] : _datatype,
                        min: minimum,
                        max: maximum,
                        avg: avg_num,
                        total: total_num,
                    })
                } else {
                    that.tableHead = [{
                        prop: 'datatype',
                        lable: ''
                        },
                        {
                            prop: 'min',
                            label: '最小值',
                        },
                        {
                            prop: 'max',
                            label: '最大值',
                        },
                        {
                            prop: 'avg',
                            label: '平均值',
                        },
                    ]
                    that.tableData.push({
                        datatype:Array.isArray(_datatype) ? _datatype[i] : _datatype,
                        min: minimum,
                        max: maximum,
                        avg: avg_num,
                    })
                }
            }
            },
        history_data_list(){
            this.loading = true
            let that = this
            let datatype = 'kwh'
            let history_name = ''

            this.axios.post('/all_plant_history_data_list',{
                date_range: this.date_range,
                datepicker1: this.date_selection.date_list[0],
                datepicker2: this.date_selection.date_list[1],

            }).then(function(data){
                let plot_data = data.data.data
                //console.log(plot_data)
                var y_title = ""
                var type = "scatter"
                var x_axis = plot_data.x_axis
                var y_axis = plot_data.y_axis
                var _datatype = [datatype]
                var num = 1
                var time_year = data.time_year

                const MyPlot = document.getElementById('plot_div')
                MyPlot.innerHTML = ""
                y_title = that.$i18n.t("plot.總發電量")+"(kWh)"
                type = "bar"
                x_axis = plot_data.x_axis
                _datatype = [y_title]
                that.plot(
                    MyPlot,
                    that,
                    x_axis,
                    y_axis,
                    history_name + " " + y_title,
                    datatype,
                    type,
                    y_title
                )
                that.history_info(
                    that,
                    x_axis,
                    plot_data.min,
                    plot_data.max,
                    plot_data.avg,
                    plot_data.total,
                    that.$i18n.t("plot.總發電量")+"(kWh)",
                    datatype,
                    2
                )
                
                that.loading = false
            })
        },
        oneline_download() {
            var csvList = []
            var memberContent = ""
            var csvContent

            //csv title 處理
            let title = document.querySelector("#plot_div text.gtitle").innerHTML
            if(title == undefined || title == null){
                title = "export"
            }
            if(title.split(' ').length > 1){
                title = title.split(' ')[0] + "_" + title.split(' ')[1].split('(')[0]
            }else{
                title = title.split(' ')[0].split('(')[0]
            }
            let filename = title + ".csv"

            var gd = document.getElementById("plot_div")

            //console.log(gd.data)
            var regList = ["number", "time"]
            for (var i = 0; i < gd.data.length; i++) {
                regList.push(gd.data[i].name)
            }
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

            console.log(csvList)
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
        },
        setDate(data){
            this.date_selection = data
            this.history_data_list()
        }
    },
    mounted(){
        window.addEventListener("resize", c.plot_resize)
    },
    watch: {
        date_range(){
            this.history_data_list()
        },
        '$store.state.language': function() {
            this.history_data_list()
        }
    },
    unmounted(){
        window.removeEventListener("resize", c.plot_resize)
    }
}
</script>
<style scoped>
.date_type_selection{
    margin-right: 1rem;
}
#plot_div{
    position: relative; 
    padding: 1rem; 
    min-height: 400px;
    max-width: 95%;
}
.history_container{
    height: 650 px;
    position: relative;
    min-width: 80%;
    border-radius: .5rem;
    /* box-shadow: 0 0 15px #DEE4EA; */
}
</style>
<style>
.el-loading-mask{
    border-radius: 8px;
}
.el-table__header tr{
	background-attachment: fixed !important;
}
</style>