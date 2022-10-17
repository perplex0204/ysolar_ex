<template>
    <div class="card col-12 col-lg-8 p-0 mt-3 me-2 shadow">
        <div class="multiple_container"  v-loading="loading">
            <div style="align-items: center; padding: 1rem;" class="d-lg-flex">
                <auto-complete :preSelect="preSelect" @search-select="search_select" @station-select="station_select" class="col-12 col-lg-3 me-lg-3 mb-2 mb-lg-0"></auto-complete>
                <el-select v-model="date_range" v-if="date_range !== -1" placeholder="Select" class="col-12 col-lg-3 me-lg-3 mb-2 mb-lg-0" size="large">
                    <el-option
                    v-for="item in options"
                    :key="item.value"
                    :label="$t(`option.${item.label}`)"
                    :value="item.value"
                    >
                    </el-option>
                </el-select>
                <el-select v-model="plot_type" placeholder="Select" class="col-12 col-lg-4 me-lg-3 mb-2 mb-lg-0" size="large">
                    <el-option
                    v-for="item in chart_options"
                    :key="item.value"
                    :label="$t(`option.${item.label}`)"
                    :value="item.value"
                    >
                    </el-option>
                </el-select>
                <el-button v-if="showcsv" size="large" type="primary" @click="online_download_multiple">
                    CSV
                </el-button>
            </div>

            <div class="col-12 col-lg-11 responsive_table mb-2 mb-lg-4" :style="multiple_style" v-if="showcsv === false">
                <div style="overflow-y: scroll;">
                    <div class="w-100 row responsive_table_header  fw-bold m-0 d-none d-lg-flex flex-nowrap">
                        <div class="col-6 text-center">
                            <label class="fs-6">{{$t('homePage.multiple_plot.table.Inverter')}}</label>
                        </div>
                        <div class="col-6 text-center">
                            <label class="fs-6">{{$t('homePage.multiple_plot.table.max_power')}}</label>
                        </div>
                    </div>
                    <div class="w-100 pt-2 pb-2 text-center" v-if="tableData.length == 0">
                        {{$t('無資料')}}
                    </div>
                    <div class="w-100 col-lg-12 responsive_table_body" :key="currentPage">
                        <div class="row m-0 responsive_table_content mt-2 mt-lg-0" v-for="data in tableData[currentPage-1]" :key="data.name" 
                        >
                            <div class="col-12 d-lg-none mt-2"></div>
                            <div class="col-12 col-lg-6">
                                <div class="d-flex d-lg-none ">
                                    <label class="fs-6 fw-bold">{{$t('homePage.multiple_plot.table.Inverter')}}:</label>
                                    <label class="fs-6">{{data.name}}</label>
                                </div>
                                <label class="fs-6 w-100 text-center d-none d-lg-block">{{data.name}}</label>
                            </div>
                            <div class="col-12 col-lg-6">
                                <div class="d-flex d-lg-none">
                                    <label class="fs-6 fw-bold d-lg-none">{{$t('homePage.multiple_plot.table.max_power')}}:</label>
                                    <label class="fs-6 d-lg-none">{{data.value}}</label>
                                </div>
                                <label class="fs-6 w-100 text-center d-none d-lg-block">{{data.value}}</label>
                            </div>
                        </div> 
                    </div>
                    <div class="w-100 responsive_table_footer pt-2 pb-2 d-flex justify-content-between justify-content-lg-center"
                    v-if="tableData.length > 0">
                        <i class="fas fa-angle-double-left footer_icon" @click="pageChange('bb')"></i>
                        <i class="fas fa-angle-left footer_icon" @click="pageChange('b')"></i>
                        <div class="col-1 text-white text-center">
                            <label class="fs-5">{{currentPage}}</label>
                            <label class="fs-6" style="color: orange;">/</label>
                            <label class="fs-7">{{totalPage}}</label>
                        </div>
                        <i class="fas fa-angle-right footer_icon" @click="pageChange('f')"></i>
                        <i class="fas fa-angle-double-right footer_icon" @click="pageChange('ff')"></i>
                
                        
                    </div>
                </div>
            </div>
            <div id="plot_multiple" class="mb-2 mb-lg-0" v-show="showcsv"></div>
        </div>
    </div>
</template>


<script>
import c from 'assets/js/common.js'
import autoComplete from '@/components/autocomplete/plant_only.vue'

export default {
    name: "multipleChart",
    data() {
        return {
            station: {},
            search: "",
            date_range: 1,
            plot_type: 3,
            showcsv: true,
            loading: false,
            options: [{
                value: 1,
                label: '日'
            },{
                value: 2,
                label: '月'
            }],
            chart_options: [{
                value: 3,
                label: '變流器發電量'
            },{
                value: 4,
                label: 'PR值'
            },{
                value: 5,
                label: '最大功率比對'
            }],
            data_length: 0,
            y_text: "",
            plot_title: "",
            plot_width: 0,

            currentPage: 1,
            totalPage: 1,
            tableData: [],
            multiple_style: {margin: '0 35px'},

            mobile_width: 300,
            desktop_width: 600,
            mobile_record: true,

            preSelect: true
        }
    },
    components: {
        autoComplete
    },
    methods: {
        station_select(item) {
            if(item.name == '無資料'){
				return false
			}
            this.station = {
                ID_list: [item.ID],
                col_list: [item.collection]
            }
        },
        search_select(item) {
            this.search = item
        },
        get_plot_data(){
            let that = this
            this.loading = true
            this.axios.post('/get_home_page_multiple_data', {
                ID: this.station.ID_list[0],
                date_range: this.date_range,
                plot_type: this.plot_type
            }).then(function(response) {
                let data = response.data.data.data
                console.log(data)
                that.data_length = data["y_axis"].length
                if (that.plot_type == 3 || that.plot_type == 4) {
                    that.showcsv = true
                    console.log(data)
                    that.plot(data["x_axis"], data["y_axis"], data["name_list"])
                }
                else if (that.plot_type == 5) {
                    that.showcsv = false
                    that.currentPage = 1
                    that.tableData = data["y_axis"]
                    that.totalPage = data["total_page"]
                    that.loading = false
                }
            })
        },
        online_download_multiple() {
            // this.get_plot_data()
            var csvList = []
            var memberContent = ""
            var csvContent
            let title = this.plot_title
            let select = this.options.find(element => element.value == this.date_range)

            title = title + "_" + select.label
            let filename = title + ".csv"

            var gd = document.getElementById("plot_multiple")
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
        y_axis_text(plot_title) {
            try{
                if (plot_title == "變流器發電量") {
                    this.y_text = this.$i18n.t("plot.發電量")+"(kWh)"
                }
                else if (plot_title == "最大功率比對") {
                    this.y_text = this.$i18n.t("plot.功率")+"(kW)"
                }
                else if (plot_title == "PR值"){
                    this.y_text = "PR"
                }
                else {
                    this.y_text = ""
                }
            }
            catch{
                console.log("")
            }
        },
        plot(x, y, names) {
            const MyPlot = document.getElementById('plot_multiple')
            MyPlot.innerHTML = ""
            console.log(MyPlot.clientWidth)
            var data = []
            let plot_select = this.chart_options.find(element => element.value == this.plot_type)
            this.plot_title = plot_select.label
            this.y_axis_text(this.plot_title)
            // console.log(this.y_text)
            // console.log(this.plot_title)
            for (var i=0; i<names.length; i++) {
                data.push({
                    x: x,
                    y: y[names[i]],
                    mode: "lines",
                    name: names[i]
                })
            }

            // console.log(data)
            var layout = {
                title: {
                    text: this.$i18n.t(`option.${this.plot_title}`),
                    font: {
                        family: "Courier New, monospace",
                        size: this.$store.state.isMobile ? 24 : 30,
                    },
                },
                yaxis: {
                    title: {
                        text: this.y_text,
                    },
                },
                width: MyPlot.clientWidth,
                height: MyPlot.clientHeight,
                margin: this.plot_margin(),
                legend:{
                    x: this.$store.state.isMobile ? 0 : 1,
                    y: this.$store.state.isMobile ? -1.5 : 1
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
            this.style_change()
            this.y_axis_text(this.plot_title)
            let update = {
                width: "",
                heigth: "",
            }
            try{
                update = {
                    width: document.getElementById('plot_multiple').clientWidth,
                    height:  400,
                    legend:{
                        x: 1,
                        y: 1,
                    },
                    margin: this.plot_margin(),
                    title: {
                        text: this.$i18n.t(`option.${this.plot_title}`),
                        font: {
                            family: "Courier New, monospace",
                            size: this.$store.state.isMobile ? 24 : 30,
                        },
                    },
                    yaxis: {
                        title: {
                            text: this.y_text,
                        },
                    },
                }
                if(document.getElementById('plot_multiple').clientWidth < 576){
                    update.heigth = document.getElementById('plot_multiple').clientHeight
                    update.legend.x = 0
                    update.legend.y = -2
                }
            }
            catch{
                return false
            }
            try{
                this.Plotly.relayout("plot_multiple", update)
                c.plot_text_color_fix(document.getElementById('plot_multiple'))
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
            if(document.getElementById('plot_multiple').clientWidth < 550){
                margin.l = 40
                margin.r = 30
                margin.pad = 1
            }
            return margin
        },
        pageChange(type){
            switch(type){
                case "bb":
                    this.page_direction = "back"
                    if(this.currentPage > 10)
                        this.currentPage -= 10
                    else
                        this.currentPage = 1
                    break
                case "b":
                    this.page_direction = "back"
                    if(this.currentPage > 1)
                        this.currentPage -= 1
                    else
                        this.currentPage = 1
                    break
                case "ff":
                    this.page_direction = "to"
                    if(this.currentPage < this.totalPage - 10)
                        this.currentPage += 10
                    else
                        this.currentPage = this.totalPage
                    break
                case "f":
                    this.page_direction = "to"
                    if(this.currentPage < this.totalPage)
                        this.currentPage += 1
                    else
                        this.currentPage = this.totalPage
                    break
            }
        },
        style_change() {
            if (this.$store.state.isMobile == true){
                this.multiple_style= {margin: '0'}
            }
            else{
                this.multiple_style= {margin: '0 35px'}
            }
        },
        plot_delay(){
            window.setInterval(() => {
                this.plot_resize()
            }, 500)
        },
    },
    watch: {
        date_range() {
            if (this.search !== "") {
                this.get_plot_data()
            }
        },
        search() {
            if (this.search !== "") {
                this.get_plot_data()
            }
        },
        plot_type() {
            if (this.search !== "") {
                this.get_plot_data()
            }
        },
        '$store.state.navOpen': function() {
            if(!this.$store.state.isMobile) {
                this.plot_delay()
            }
        },
        '$store.state.language': function() {
            this.plot_resize()
        }
    },
    mounted() {
        // this.get_plot_data()
        // console.log(document.getElementById('plot_multiple').clientWidth)
        // let that = this
        this.style_change()
        // if (document.getElementById('plot_multiple').clientWidth > 0){
        //     if (this.$store.state.isMobile == true){
        //         this.mobile_width = document.getElementById('plot_multiple').clientWidth
        //         this.plot_width = this.mobile_width
        //         this.mobile_record = true
        //     }
        //     else{
        //         this.desktop_width = document.getElementById('plot_multiple').clientWidth
        //         this.plot_width = this.desktop_width
        //         this.mobile_record = false
        //     }
        // }
        // var event = window.addEventListener("resize", function(){
        //     try{
        //         var width = 0
        //         width = document.getElementById('plot_multiple').clientWidth
        //     }
        //     catch{
        //         console.log("plot width error")
        //     }
        //     if (that.$store.state.isMobile == true && that.mobile_record == false){
        //         width > 0 ? that.mobile_width = width : null
        //         that.mobile_record = true
        //     }
        //     else if (that.$store.state.isMobile == false && that.mobile_record == true){
        //         width > 0 ? that.desktop_width = width : null
        //         that.mobile_record = false
        //     }
        //     that.$store.state.isMobile == true ? that.plot_width = that.mobile_width : that.plot_width = that.desktop_width
        //     that.plot_resize()
        // })
    },
    unmounted(){
        // let that = this
        // var event = window.addEventListener("resize", function(){
        //     try{
        //         var width = 0
        //         width = document.getElementById('plot_multiple').clientWidth
        //     }
        //     catch{
        //         console.log("plot width error")
        //     }
        //     if (that.$store.state.isMobile == true && that.mobile_record == false){
        //         width > 0 ? that.mobile_width = width : null
        //         that.mobile_record = true
        //     }
        //     else if (that.$store.state.isMobile == false && that.mobile_record == true){
        //         width > 0 ? that.desktop_width = width : null
        //         that.mobile_record = false
        //     }
        //     that.$store.state.isMobile == true ? that.plot_width = that.mobile_width : that.plot_width = that.desktop_width
        //     that.plot_resize()
        // })
        // window.removeEventListener("resize", event)
    }
}
</script>

<style scoped>
#plot_multiple{
    position: relative; 
    padding: 1rem; 
    padding-bottom: 0;
    min-height: 450px;
    max-height: 450px;
    max-width: 95%;
    border-radius: .5rem;
}
.multiple_container{
    height: 550px;
    max-height: 650px;
    position: relative;
    min-width: 80%;
    border-radius: .5rem;
}

@media(max-width: 991px){
    .multiple_container{
        height: 850px;
        max-height: 950px;
    }
    #plot_multiple{
        min-height: 550px;
        max-height: 550px;
        padding-bottom: 0;
        width: 80vw;
        max-width: 80vw;
    }
}
</style>