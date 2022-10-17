<template>
    <div class="">
        <div class="d-flex flex-wrap">
            <el-select class="col-12 col-lg-2" v-model="date_range" v-if="date_range != 0" size="large" :placeholder="$t('option.請選擇')">
                <el-option
                v-for="item in options"
                :key="item.value"
                :label="$t(`option.${item.label}`)"
                :value="item.value"
                >
                </el-option>
            </el-select>
            <el-select v-model="datatype" :placeholder="$t('option.請選擇')" size="large" class="col-12 col-lg-2 ms-lg-3 mt-3 mt-lg-0">
                <el-option label="DMY" value="dmy"></el-option>
                <el-option label="PR" value="pr"></el-option>
            </el-select>
            <el-popover placement="bottom-start" trigger="click" :width="this.$store.state.isMobile? '95vw':'fit-content'"
            class="date_popover"
            style="max-width: 100vw; overflow-y: scroll;"
            >
                <template #reference>
                    <el-button
                        size="large"
                        class="col-12 col-lg-2 col-xl-2 ms-lg-3 mt-3 mt-lg-0">
                        <i class="far fa-clock"></i>{{$t('時間篩選')}}
                    </el-button>
                </template>
                <time-range-picker @setDate="setDate" ></time-range-picker>
            </el-popover>
        </div>
        <div class="card shadow mt-3 mb-3" :style="apply_style" v-loading="loading">
            <div class="d-flex">
                <el-button  type="primary" size="large" class="mt-3 ms-4" @click="online_download">
                    {{$t("輸出CSV")}}
                </el-button>
            </div>
            <div id="plot_dmy"></div>
        </div>
    </div>
</template>


<script>
import c from 'assets/js/common.js'
import timeRangePicker from "@/components/datepicker/timeRangePickerSimple.vue";
export default {
    name: "dmyCompare",
    components:{
        timeRangePicker
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
            loading: false,
            date_range: 1,
            ID_list: [],
            capacity_list: [],
            datatype: 'dmy',
            plot_data_length: 0,
            modebar: true,
            data: [],
            plot_style: {},
            stbigimg_style: {},
            apply_style: {},
            layout: {}
        }
    },
    methods: {
        initial(){
            let that = this
            that.axios.post('/get_all_group_ID')
            .then(function(data) {
                let compareData = data.data.data
                that.ID_list = compareData.ID_list
                that.capacity_list = compareData.capacity_list
                // console.log(that.capacity_list)
                that.history_data_list()
            })
        },
        plot(dmyDataList, irrhDataList){
            if (irrhDataList != undefined){
                this.stbigimg_style = {height: String(600 + (dmyDataList.length + irrhDataList.length)*20)+"px"}
                this.plot_style = {height: this.stbigimg_style.height>"1500px" ? 1400 : 500 + (dmyDataList.length + irrhDataList.length)*20}
            }
            else{
                this.stbigimg_style = {height: String(600 + (dmyDataList.length)*20)+"px"}
                this.plot_style = {height: this.stbigimg_style.height>"1500px" ? 1400 : 500 + dmyDataList.length*20}
            }
            this.$store.state.isMobile ? this.apply_style = this.stbigimg_style : this.apply_style = {}
            let plot_obj = document.getElementById('plot_dmy')
            var data = []
            for(var i in dmyDataList){
                data.push({
                    type: "scatter",
                    mode: "lines+markers",
                    x: dmyDataList[i].x_axis,
                    y: dmyDataList[i].y_axis,
                    name: dmyDataList[i].label,
                    yaxis: "y",
                    line: { 
                        // color: color[i],
                        shape: 'linear'
                    },
                    marker: {
                        size: 8
                    }
                })
            }
            this.plot_data_length = data.length
            if(this.datatype == 'dmy'){
                for(var i=0; i < irrhDataList.length; i++){
                    data.push({
                        type: "scatter",
                        mode: "lines+markers",
                        x: irrhDataList[i].x_axis,
                        y: irrhDataList[i].y_axis,
                        name: irrhDataList[i].label,
                        yaxis: "y",
                        line: { 
                            // color: color[i+counter],
                            shape: 'linear',
                            dash: 'dot'
                        },
                        marker:{
                            size: 8
                        }
                    })
                }
            }
            console.log(this.datatype)
            var layout = {
                title: {
                    text: this.datatype == 'dmy' ? "DMY" : "PR",
                    font: {
                        family: "Courier New, monospace",
                        size: this.$store.state.isMobile ? 20 : 30
                    },
                },
                // xaxis: {
                //     domain: [0.1, 0.94],
                //     anchor: "free",
                //     position: 0,
                // },
                yaxis: {
                    title: {
                        text: this.datatype == 'dmy' ? this.$i18n.t("plot.小時") : this.$i18n.t("plot.pr"),
                    },
                },
                width: document.getElementById("plot_dmy").clientWidth,
                height: this.$store.state.isMobile ? this.plot_style.height: document.getElementById("plot_dmy").clientHeight,
                margin: {
                    l: 70,
                    t: 50,
                    pad: 10,
                },
                legend:{
                    x: this.$store.state.isMobile ? -0.2 : 1,
                    y: this.$store.state.isMobile ? -2 : 1,
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
                plot_bgcolor: "transparent",
            }
            this.data = data
            this.layout = layout
            // console.log(this.plot_style)
            try{
                this.Plotly.newPlot(plot_obj, data, layout, {
                    displaylogo: false,
                    displayModeBar: true,
                    modeBarButtonsToRemove: [
                        "sendDataToCloud",
                        "hoverClosestCartesian",
                        "hoverCompareCartesian",
                        "toggleSpikelines",
                    ],
                })
                this.modebar = true
                if (this.$store.state.isMobile){
                    plot_obj.on('plotly_doubleclick', this.modebar_event)
                }
                c.plot_text_color_fix(plot_obj)
            }
            catch(e){
                console.log(e)
            }
            
        },
        history_data_list(){
            this.loading = true
            let that = this
            if(this.ID_list.length == 0){
                return false
            }
            this.axios.post('/ID_get_dmy_irrh_interval',{
                ID_list: this.ID_list,
                datepicker1: this.date_selection.start_date,
                datepicker2: this.date_selection.end_date,
                date_range: this.date_range,
                datatype: [this.datatype]
            }).then(function(data){
                let plotData = []
                if(that.datatype == 'dmy')
                    plotData = data.data.data.dmy_list
                else if(that.datatype == 'pr')
                    plotData = data.data.data.pr_list
                let irrhData = data.data.data.sun_list
                // console.log(dmyData)
                // console.log(irrhData)
                if(data.data.data.remote_error_msg.length > 0){
                    alert(data.data.data.remote_error_msg)
                }

                try{
                    that.plot(plotData, irrhData)
                }
                catch(e){
                    console.log(e)
                }

                that.loading = false
            })


        },
        online_download(){
            var csvList = []
            var memberContent = ""
            var csvContent
            let title = this.datatype == 'dmy' ? "DMY比較_" : "PR比較_"
            let datepicker1 = this.date_selection.start_date
            let datepicker2 = this.date_selection.end_date
            let select = this.options.find(element => element.value == this.date_range)

            if (datepicker1 === datepicker2){
                title += datepicker1
            }else{
                title = title + datepicker1 + "_" + datepicker2
            }
            title = title + "_" + select.label
            let filename = title + ".csv"

            var gd = document.getElementById("plot_dmy")
            var regList = ["number", "time"]
            var all_data_length = gd.data.length
            for (var i = 0; i < all_data_length; i++) {
                // console.log(gd.data[i])
                if (i < this.plot_data_length){
                    if(this.datatype == 'dmy'){
                        regList.push(gd.data[i].name+"(DMY)")
                        regList.push(gd.data[i].name+"(發電量)")
                    }
                    else{
                        regList.push(gd.data[i].name+"(PR)")
                    }
                }
                else{
                    regList.push(gd.data[i].name)
                }
            }
            csvList.push(regList)

            var x = gd.data[0].x

            for (var j = 0; j < x.length; j++) {
                var regList = []
                regList.push(j + 1)
                regList.push(x[j])
                for (var i = 0; i < gd.data.length; i++) {
                    // regList.push(gd.data[i].y[j])
                    if (i < this.plot_data_length){
                        regList.push(gd.data[i].y[j])
                        if(this.datatype == 'dmy')
                            regList.push(gd.data[i].y[j] * this.capacity_list[i])
                    }
                    else{
                        regList.push(gd.data[i].y[j])
                    }
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
        setDate(data){
            this.date_selection = {
                mode:data.mode,
                start_date:data.date_list[0],
                end_date:data.date_list[1]
            }
        },
        plot_resize() {
            this.modebar = true
            let plot_obj = document.getElementById('plot_dmy')
            try{
                plot_obj.removeEventListener('plotly_doubleclick', this.modebar_event)
            }
            catch(e){
                console.log(e)
            }
            this.$store.state.isMobile ? this.apply_style = this.stbigimg_style : this.apply_style = {}
            let update = {
                width: "",
                heigth: "",
            }
            update = {
                width: document.getElementById('plot_dmy').clientWidth,
                height:  this.$store.state.isMobile ? this.plot_style.height: document.getElementById("plot_dmy").clientHeight,
                title: {
                    text: this.datatype == 'dmy' ? "DMY" : "PR",
                    font: {
                        family: "Courier New, monospace",
                        size: this.$store.state.isMobile ? 20 : 30,
                    },
                },
                yaxis: {
                    title: {
                        text: this.datatype == 'dmy' ? this.$i18n.t("plot.小時") : this.$i18n.t("plot.pr"),
                    },
                },
                legend:{
                    x: this.$store.state.isMobile ? -0.2 : 1,
                    y: this.$store.state.isMobile ? -1 : 1
                },
                margin: {
                    l: 70,
                    t: 50,
                    pad: 10,
                }
            }
            try{
                this.Plotly.relayout("plot_dmy", update)
                if (this.$store.state.isMobile){
                    plot_obj.on('plotly_doubleclick', this.modebar_event)
                }
                else{
                    this.modebar = false
                    this.modebar_event()
                }
                c.plot_text_color_fix(document.getElementById('plot_dmy'))
            }
            catch(e){
                console.error(e)
            }
        },
        modebar_event(){
            try{
                this.modebar = !this.modebar
                let conf = {
                    displayModeBar: this.modebar,
                    displaylogo: false,
                    modeBarButtonsToRemove: [
                        "sendDataToCloud",
                        "hoverClosestCartesian",
                        "hoverCompareCartesian",
                        "toggleSpikelines",
                    ],
                }
                console.log(this.modebar)
                this.Plotly.react("plot_dmy", this.data, this.layout, conf)
                
            }
            catch(e){
                console.log(e)
            }
        }
    },
    watch: {
        date_range(){
            this.history_data_list()
        },
        date_selection(){
            this.history_data_list()
        },
        "$store.state.language": function() {
            this.plot_resize()
        },
        "$store.state.navOpen": function() {
            if(!this.$store.state.isMobile) {
                this.plot_resize()
            }
        },
        datatype(){
            console.log(this.datatype)
            this.history_data_list()
        }
    },
    mounted(){
        this.initial()
        window.addEventListener("resize", this.plot_resize)
    },
    unmounted(){
        let plot_obj = document.getElementById('plot_dmy')
        window.removeEventListener("resize", this.plot_resize)
        try{
            plot_obj.removeEventListener('plotly_doubleclick', this.modebar_event)
        }
        catch(e){
            console.log(e)
        }
    }
}
</script>

<style scoped>
#plot_dmy{
    position: relative; 
    padding: 1rem; 
    min-height: 500px;
    /* height: 500px; */
    max-height: 550px;
    width: 95%;
    max-width: 95%;
}
.stbigimg{
    position: relative;
	width: 80vw;
	min-height: 65vh;
	border-radius: 1rem;
	box-shadow: 0 0 15px #DEE4EA;
	overflow: hidden;
	background-color: #fff;
}
@media (max-width: 991px){
    #plot_dmy{
        padding: 0rem;
        /* min-height: 900px; */
        max-height: 1500px;
        width: 100%;
        max-width: 100%;
    }
    .stbigimg{
        width: 100%;
        /* min-height: 600px; */
        max-height: 1500px;
        overflow: scroll;
    }

}
</style>
