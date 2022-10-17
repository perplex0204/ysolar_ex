<template>
    <div class="img shadow">
        <div id="plot_div"></div>
        <div v-if="tableData.length > 0" style="margin-bottom: 5vh">
            <alarm-pie-table :tableData="tableData"></alarm-pie-table>
        </div>
    </div>
</template>

<script>
import alarmPieTable from '@/components/alarm/alarmPieTable.vue'
import c from 'assets/js/common.js'

export default {
    name: "alarmPieChart",
    data() {
        return {
            screenWidth: document.body.clientWidth,
            legend : [1, 1],
            font_size: 16,
            textposition: [],
            position_full: [],
            position_mobile: [],
            tableData : []
            // limit: true,
            // today:""
        }
    },
    components: {
        alarmPieTable
    },
    props: {
        station: {type: Object, required: true},
        date_selection: {type: Object, required: true},
        alarm_option: {type: String, required: true},
    },
    methods: {
        alarm_get(){
            // this.loading = true
            //use api alarm_get to obtain alarm
            let that = this
            this.axios.post('alarm_get', {
                time:this.date_selection,
                plant: Object.keys(this.station).length == 0 ? {"all":true,"ID":null,"col":null}:
                {"all": false, "ID": this.station.ID_list, "col": this.station.col_list},
                alarm_type:"all",
                alarm_group:"all",
                equip_type:"all",
                page:1,
                documents_per_page:9999999
            }).then(data => {
                console.log(data.data.data.data)
                that.get_pie_chart_data(data.data.data.data)
                // that.limit = true
            })
        },
        get_pie_chart_data(data) {
            let that = this
            this.axios.post('get_alarm_pie_chart_data', {
                alarm_option: this.alarm_option,
                alarms: data
            }).then(data => {
                console.log(data.data.data.data)
                var plot_data = data.data.data.data.data
                that.plot_alarm_pie_chart(plot_data)
                that.tableData = data.data.data.data.table_data
            })
        },
        plot_alarm_pie_chart(chart_data) {
            var labels = []
            var values = []
            this.textposition = []
            var key = Object.keys(chart_data)
            var key_length = key.length
            for (var i=0; i<key_length; i++){
                // console.log(key[i])
                if (key[i] !== "losing") {
                    labels.push(key[i]+`(${this.$i18n.t("plot.總損失")}`+`${chart_data["losing"][key[i]].toFixed(2)}`+"kWh)")
                    values.push(chart_data[key[i]])
                }
            }
            for (var i=0; i<key_length; i++){
                if (values[i] === 0){
                    this.textposition.push("none")
                }
                else{
                    this.textposition.push("outside")
                }
            }
            // console.log(textposition)
            var data = [
                {
                    values: values,
                    labels: labels,
                    type: "pie",
                    textinfo: this.$store.state.isMobile ? "percent" : "label+percent",
                    textposition: this.textposition,
                    name: "alarm",
                    textfont: {
                        size: this.$store.state.isMobile ? 16 : 10
                    },
                    hole: 0.4
                }
            ]
            var layout = {
                // height: 400,
                // width: 400,
                width: document.getElementById("plot_div").clientWidth,
                height: this.$store.state.isMobile ? 600:550,
                // autosize:true,
                // height: document.getElementById("plot_div").clientHeight,
                legend: {
                    x: this.$store.state.isMobile ? 0 : 1,
                    y: this.$store.state.isMobile ? -1.2 : 1,
                },
                paper_bgcolor: "transparent",
                plot_bgcolor: "transparent"
                // margin: {"t": 0},
                // margin: {'pad': 20},
            }
            this.Plotly.newPlot('plot_div', data, layout, {
                displaylogo: false,
                modeBarButtonsToRemove: [
                "sendDataToCloud",
                "hoverClosestCartesian",
                "hoverCompareCartesian",
                "toggleSpikelines",
                ],
            })
            c.plot_text_color_fix(document.getElementById('plot_div'))
        },
        plot_resize() {
            let update = {
                width: "",
                heigth: "",
            }
            update = {
                width: document.getElementById('plot_div').clientWidth,
                height: this.$store.state.isMobile ? 600:550,
                legend:{
                    x: 1,
                    y: 1,
                    
                },
            }
            let update_data = {
                textinfo: this.$store.state.isMobile ? "percent" : "label+percent",
                textfont: {
                    size: this.$store.state.isMobile ? 16 : 10
                }
            }
            if(document.getElementById('plot_div').clientWidth < 576){
                // update.heigth = document.getElementById('plot_div').clientHeight
                update.legend.x = 0
                update.legend.y = -1.2
            }
            try{
                this.Plotly.relayout("plot_div", update)
                this.Plotly.restyle("plot_div", update_data)
                c.plot_text_color_fix(document.getElementById('plot_div'))
            }
            catch{
                return false
            }
        }
    },
    watch: {
        date_selection() {
            console.log(this.date_selection)
            this.alarm_get()
        },
        alarm_option(){
            this.alarm_get()
        },
        'station.ID_list': function(){
            // console.log(this.station)
            this.alarm_get()
        },
        'station.col_list': function(){
            // console.log(this.station)
            this.alarm_get()
        },
        '$store.state.navOpen': function() {
            if(!this.$store.state.isMobile) {
                this.plot_resize()
            }
        },
        "$store.state.language": function() {
            this.alarm_get()
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
            this.legend = [1, 1]
            // this.font_size = 16
        }
        else {
            this.legend = [0, -1]
            // this.font_size = 14
        }
    },
    unmounted() {
        let that = this
        window.removeEventListener("resize", this.plot_resize)
        window.removeEventListener("resize", function() {
            return (() => {
                that.screenWidth = this.document.body.clientWidth
            })()
        })
    }
}

</script>

<style scoped>
#plot_div{
    position: relative; 
    padding: 1rem;
    padding-bottom: 0;
    min-height: 600px;
    max-height: 700px;
    max-width: 95%;
}
@media (max-width: 991px){
#plot_div{
    padding: 0rem;
    max-height: 600px;
    max-width: 100% 
}

}

.img{
    position: relative;
	width: 100%;
	min-height: 65vh;
	border-radius: 1rem;
	box-shadow: 0 0 15px #DEE4EA;
	overflow: hidden;
}
</style>