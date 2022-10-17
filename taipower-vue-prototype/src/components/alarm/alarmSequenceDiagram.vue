<template>
    <div class="img" :class="{'shadow': shadow}">
        <div id="plot_sequence"  v-loading="loading"></div>
    </div>
</template>

<script>
import c from 'assets/js/common.js'

export default {
    name: 'alarmSequenceDiagram',
    props: {
        station: {type: Object, required: true},
        date_selection: {type: Object, required: true},
        shadow: {type: Boolean, default: true},
        search: {type: String, required: true}
    },
    data(){
        return {
            loading:false,
            timer: ""
        }
    },
    methods: {
        alarm_get_sequence(){
            let that = this
            this.loading = true
            //use api alarm_get to obtain alarm
            this.axios.post('alarm_get', {
                time: this.date_selection,
                plant: Object.keys(this.station).length == 0 ? {"all":true,"ID":null,"col":null}:
                {"all": false, "ID": this.station.ID_list, "col": this.station.col_list},
                alarm_type:'returned',
                alarm_group:"all",
                equip_type:"all",
                page:1,
                documents_per_page:9999
            }).then(data => {
                console.log(data.data.data)
                that.get_sequence_data(data.data.data.data)
            })
        },
        get_sequence_data(data){
            let that = this
            this.axios.post('/get_alarm_sequence_diagram', {
                alarms: data,
                time: this.date_selection,
                plant: Object.keys(this.station).length == 0 ? {"ID": null, "col": null} : {"ID": this.station.ID_list[0], "col": this.station.col_list[0]}
            }).then(function(data){
                console.log(data.data.data.data)
                var plot_data = data.data.data.data
                that.plot_sequence(plot_data.x_axis, plot_data.y_axis, plot_data.names)
            })
        },
        plot_sequence(x, y, names){
            const MyPlot = document.getElementById('plot_sequence')
            MyPlot.innerHTML = ""
            var data = []
            for (var i=0; i<y.length; i++) {
                data.push({
                    x: x,
                    y: y[i],
                    mode: "lines",
                    name: names[i]
                })
            }

            // console.log(data)
            var layout = {
                title: {
                    text: this.$i18n.t("plot.時序圖"),
                    font: {
                        family: "Courier New, monospace",
                        size: this.$store.state.isMobile ? 24 : 30,
                    },
                },
                yaxis: {
                    title: {
                        text: this.$i18n.t("plot.設備"),
                    },
                },
                width: document.getElementById('plot_sequence').clientWidth,
                height: MyPlot.clientHeight,
                // margin: this.plot_margin(),
                legend:{
                    x: this.$store.state.isMobile ? 0 : 1,
                    y: this.$store.state.isMobile ? -2 : 1
                },

                paper_bgcolor: "transparent",
                plot_bgcolor: "transparent"
            }
            // console.log(layout.width)
            // console.log(this.plot_width)
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
            try{
                update = {
                    width: document.getElementById('plot_sequence').clientWidth,
                    height: document.getElementById('plot_sequence').clientHeight,
                    legend:{
                        x: 1,
                        y: 1,
                    },
                    // margin: this.plot_margin(),
                    title: {
                        text: this.$i18n.t("plot.時序圖"),
                        font: {
                            family: "Courier New, monospace",
                            size: this.$store.state.isMobile ? 24 : 30,
                        },
                    },
                    yaxis: {
                        title: {
                            text: this.$i18n.t("plot.設備"),
                        },
                    },
                }
                if(document.getElementById('plot_sequence').clientWidth < 576){
                    update.heigth = document.getElementById('plot_sequence').clientHeight
                    update.legend.x = 0
                    update.legend.y = -2
                }
            }
            catch{
                return false
            }
            try{
                this.Plotly.relayout("plot_sequence", update)
                c.plot_text_color_fix(document.getElementById('plot_sequence'))
            }
            catch{
                return false
            }
        },
        plot_delay(){
            window.setInterval(() => {
                this.plot_resize()
            }, 500)
        }
    },
    mounted(){
        // this.alarm_get_sequence()
        window.addEventListener("resize", this.plot_resize)
    },
    unmounted(){
        window.removeEventListener("resize", this.plot_resize)
        // clearTimeout(this.timer)
    },
    watch: {
        station(){
            // console.log(this.station)
            // console.log(this.date_selection)
            this.alarm_get_sequence()
        },
        date_selection(){
            console.log(this.date_selection)
            this.alarm_get_sequence()
        },
        '$store.state.navOpen': function() {
            if(!this.$store.state.isMobile) {
                console.log("prepare plot")
                this.plot_delay()
                // clearTimeout(that.timer)
            }
        },
        '$store.state.language': function() {
            this.plot_resize()
        }
    }
}
</script>

<style scoped>
#plot_sequence{
    position: relative; 
    padding: 1rem; 
    min-height: 520px;
    max-height: 520px;
    width: 95%;
    max-width: 95%;
}
@media (max-width: 991px){
    #plot_sequence{
        padding: 0rem;
        min-height: 500px;
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
/* @media (max-width: 991px){
    #plot_sequence{
        padding: 0rem;
        max-height: 700px;
        width: 100%;
        max-width: 100% 
    }
    .img{
        width: 100%;
    }

} */
</style>