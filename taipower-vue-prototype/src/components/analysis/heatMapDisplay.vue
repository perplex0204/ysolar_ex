<template>
    <div>
        <div class="fs-4 text-success mb-2" v-if="$store.state.user_data.pageType != 'taipower'">
            <div>{{title}}</div>
        </div>
        <div class="card shadow ps-2 ps-lg-0 pb-lg-2">
            <div id="plot_heatmap" :style="heatmap_style"></div>
        </div>
    </div>
</template>

<script>
import c from 'assets/js/common.js'

export default {
    name: "heatMapDisplay",
    data(){
        return {
            title: "",
            screenWidth: document.body.clientWidth,
            font_size: 25,

            plot_width: 0,
            mobile_width: 300,
            desktop_width: 600,
            mobile_record: true,

            heatmap_style: {width: '700px'}
        }
    },
    props: {
        x_axis: {type: Array, requird: true},
        y_axis: {type: Array, requird: true},
        z_axis: {type: Array, requird: true},
        date: {type: String, requird: true},
        place: {type: String, requird: true}
    },
    methods: {
        plotHeatMap(){
            const MyPlot = document.getElementById('plot_heatmap')
            MyPlot.innerHTML = ""
            var data = [
                {
                    x: this.x_axis,
                    y: this.y_axis,
                    z: this.z_axis,
                    colorscale: [
                        ["0.0", "blue"],
                        ["0.6", "orange"],
                        ["1.0", "red"],
                    ],
                    type: 'heatmap'
                }
            ]
            var layout = {
                title: {
                    text: this.place.replace(/\\/g, "_")+" "+this.date,
                    font: {
                        family: "Courier New, monospace",
                        size: this.font_size,
                    },
                },
                width: document.getElementById('plot_heatmap').clientWidth > 0 ? document.getElementById('plot_heatmap').clientWidth : this.plot_width,
                height: document.getElementById("plot_heatmap").clientHeight,
                legend:{
                    x: 0.11,
                    y: 1
                },
                // margin: this.plot_margin(),
                //paper_bgcolor: this.$store.state.isMobile ? "fff": null,
                hovermode: "closest",
                hoverlabel: {
                    bgcolor: "#FFFFFF",
                    bordercolor: "#888888",
                    font: {
                        color: "#000000",
                    },
                },
                paper_bgcolor: "transparent",
                plot_bgcolor: "transparent",
            }
            this.Plotly.newPlot(MyPlot, data, layout , {
                responsive: true,
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
        plot_resize() {
            this.style_change()
            let update = {
                width: "",
                heigth: "",
            }
            update = {
                width: document.getElementById('plot_heatmap').clientWidth > 0 ? document.getElementById('plot_heatmap').clientWidth : this.plot_width,
                height:  document.getElementById('plot_heatmap').clientHeight,
                title: {
                    text: this.place.replace(/\\/g, "_")+" "+this.date,
                    font: {
                        family: "Courier New, monospace",
                        size: 25,
                    },
                },
                legend:{
                    x: 0.11,
                    y: 1
                },
            }
            if(document.getElementById('plot_heatmap').clientWidth < 576){
                update.title.font.size = 10
            }
            try{
                this.Plotly.relayout("plot_heatmap", update)
                c.plot_text_color_fix(document.getElementById('plot_heatmap'))
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
            if(document.getElementById('plot_heatmap').clientWidth < 550){
                margin.l = 40
                margin.r = 40
                margin.pad = 1
            }
            return margin
        },
        style_change() {
            if (this.$store.state.isMobile == true){
                this.heatmap_style= {
                    // padding-left: '40px';
                    // padding-top: '30px';
                    width: '700px'
                }
            }
            else{
                this.heatmap_style= {width: '300px'}
            }
            // console.log(user_select_none.style)
        }
    },
    watch: {
        z_axis() {
            // console.log(this.x_axis)
            // console.log(this.y_axis)
            // console.log(this.z_axis)
            this.title = this.place.replace(/\\/g, "/")
            if (this.plot_width>=576) {
                this.font_size = 25
            }
            else {
                this.font_size = 10
            }
            this.plotHeatMap()
        },
        '$store.state.navOpen': function() {
            if(!this.$store.state.isMobile) {
                this.plot_resize()
            }
        }
    },
    mounted() {
        let that = this
        this.style_change()
        if (document.getElementById('plot_heatmap').clientWidth > 0){
            if (this.$store.state.isMobile == true){
                this.mobile_width = document.getElementById('plot_heatmap').clientWidth
                this.plot_width = this.mobile_width
                this.mobile_record = true
            }
            else{
                this.desktop_width = document.getElementById('plot_heatmap').clientWidth
                this.plot_width = this.desktop_width
                this.mobile_record = false
            }
        }

        // window.addEventListener("resize", this.plot_resize)
        // window.addEventListener("resize", function() {
        //     return (() => {
        //         that.screenWidth = this.document.body.clientWidth
        //     })()
        // })
        var event = window.addEventListener("resize", function(){
            var width = 0
            width = document.getElementById('plot_heatmap').clientWidth
            if (that.$store.state.isMobile == true && that.mobile_record == false){
                width > 0 ? that.mobile_width = width : null
                that.mobile_record = true
            }
            else if (that.$store.state.isMobile == false && that.mobile_record == true){
                width > 0 ? that.desktop_width = width : null
                that.mobile_record = false
            }
            that.$store.state.isMobile == true ? that.plot_width = that.mobile_width : that.plot_width = that.desktop_width
            that.plot_resize()
        })

        if (this.plot_width>=576) {
            this.font_size = 25
        }
        else {
            this.font_size = 10
        }
    },
    unmounted() {
        let that = this
        // window.removeEventListener("resize", this.plot_resize)
        var event = window.addEventListener("resize", function(){
            var width = 0
            width = document.getElementById('plot_heatmap').clientWidth
            if (that.$store.state.isMobile == true && that.mobile_record == false){
                width > 0 ? that.mobile_width = width : null
                that.mobile_record = true
            }
            else if (that.$store.state.isMobile == false && that.mobile_record == true){
                width > 0 ? that.desktop_width = width : null
                that.mobile_record = false
            }
            that.$store.state.isMobile == true ? that.plot_width = that.mobile_width : that.plot_width = that.desktop_width
            that.plot_resize()
        })
        window.removeEventListener("resize", event)
    }
}
</script>
<style scoped>
#plot_heatmap{
    position: relative; 
    padding-left: 40px;
    padding-top: 30px;
    /* padding-bottom: 50px;  */
    min-height: 500px;
    max-height: 500px;
    max-width: 95%;
    min-width: 95%;
    border-radius: 1rem;
    /* margin: 30px 50px; */
}
.stbigimg{
    position: relative;
	width: 100%;
	min-height: 530px;
	border-radius: 1rem;
	box-shadow: 0 0 15px #DEE4EA;
	/* overflow: hidden; */
	background-color: #fff;
}
/* .svg-container{
    width: 550px !important;
    min-width: 550px !important;
    height: 600px !important;
}
.main-svg{
    width: 550px !important;
    min-width: 550px !important;
    height: 600px !important;
} */
@media (max-width: 991px){
    #plot_heatmap{
        padding: 0rem;
        max-width: 100% ;
        max-height: 600px;
    }
}
@media (min-width: 992px){
    #plot_heatmap{
        padding-left: 40px;
        padding-top: 30px;
        min-height: 500px;
        max-height: 500px;
        max-width: 95%;
        min-width: 95%;
    }
}
</style>