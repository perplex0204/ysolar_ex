<template>
    <div class="card col-12 col-lg-8 p-0 mt-3 me-2 shadow">
        <div class="history_container"  v-loading="loading">
            <div class="d-flex pt-4 ps-4 pe-4">
                <el-popover placement="bottom" trigger="click" 
                :width="$store.state.isMobile? '90%':'50%'">
                    <template #reference>
                        <div class="btn alert alert-primary col-12" role="alert">
                            <div v-if="$store.state.language == 'en-US'">
                                Selected {{Object.keys(this.searchDeviceList).length}} Equipments to compare
                            </div>
                            <div v-else>
                                已選取{{Object.keys(this.searchDeviceList).length}}樣設備進行比較
                            </div>
                        </div>
                    </template>
                    <div class="d-flex flex-wrap">
                        <!-- Plant Search -->
                        <autocomplete class="col-12 col-lg-4" @station-select="station_select" />
                        <!-- Equipment Selection -->
                        <div class="col-12 col-lg-4 ms-lg-2 mt-2 mt-lg-0">
                            <el-popover
                            :teleported="false"
                            placement="bottom-start"
                            width="unset"
                            popper-class="screen-limit"
                            trigger="click">
                                <template #reference>
                                    <el-button 
                                    class="w-100"
                                    size="large">
                                        <i class="icon-ttl_sunboard"></i> {{$t('analysis.compareChart.select_equip')}}
                                    </el-button>
                                </template>
                                <el-cascader-panel 
                                v-model="selectedDevice"
                                class="no-border-inside"
                                @change="checkChange()"
                                :props="{ multiple: true  }"
                                :options="device_list"
                                ref="device_point_ref">
                                </el-cascader-panel>
                            </el-popover>
                        </div>
                    </div>
                    <div class="d-flex flex-wrap">
                        <!-- 選擇的儀器 -->
                        <div
                        class="card ms-lg-2 mt-2 p-2"
                        v-for="(item, idx) in searchDeviceList"
                        :key="idx">
                            <div class="d-flex align-items-center">
                                <label class="ms-2" @click="selectSearchDevice(item)">{{ item.name }}</label>
                                <button class="btn"
                                @click="deleteSearchDevice(idx)"><i class="el-icon-close"></i></button>
                            </div>
                        </div>
                    </div>
                </el-popover>
            </div>
            <div style="display: flex; align-items: center; padding: 1rem;">
                <el-button size="large" type="primary" @click="oneline_download">
                    {{$t('analysis.compareChart.export_csv')}}
                </el-button>
            </div>
            <div ref="plot_div" class="text-dark" style="max-width: 100%; min-height: 300px;"
            v-loading="loading"></div>
            <div class="d-flex flex-wrap p-2">
                <el-popover placement="top-start" trigger="click" width="90%">
                    <template #reference>
                        <el-button
                            size="large"
                            class="col-12 col-lg-3 col-xl-2">
                            <i class="far fa-clock"></i>{{$t('時間篩選')}}
                        </el-button>
                    </template>
                    <time-range-picker @setDate="setDate"></time-range-picker>
                </el-popover>
                <button class="btn btn-primary ms-lg-auto mt-2 mt-lg-0 col-12 col-lg-3"
                @click="get_compare_data()">{{$t('analysis.compareChart.start_compare')}}</button>
            </div>
        </div>
    </div>
</template>
<script>
import timeRangePicker from "@/components/datepicker/timeRangePickerSingle.vue";

import c from 'assets/js/common.js'
import autocomplete from '../autocomplete/all_type.vue'

export default {
    name: "equipmentCompare",
    components: {
        timeRangePicker,
        autocomplete
    },
    data(){
        return {
            loading: false,
            //plant search
            plant_select: {'ID_list': [], 'col_list': []},
            plant_search: "",
            //device list after station choose 
            device_list: [],
            //cascader selected device
            selectedDevice: [],
            searchDeviceList: {},
            //date select
            date_selection: {},
        }
    },
    methods: {
        station_select(item){
            console.log(item)
            this.plant_search = item.name
            this.plant_select['ID_list'] = [item.ID]
            this.plant_select['col_list'] = [item.collection]
            this.get_equip_select()
        },
        //-----------------------------------------------------------
        get_equip_select(){
            let that = this
            this.selectDevice = {}
            for(var i in this.plant_select.ID_list){
                this.axios.post('/get_equip_select_compare', {
                    ID: this.plant_select.ID_list[i],
                    collection: this.plant_select.col_list[i]
                }).then(data=>{
                    console.log(data.data.data)
                    let station_str = data.data.data.station_data.station_str
                    for(var equip_type in data.data.data.equip_data){
                        if(equip_type == 'inv' && data.data.data.equip_data[equip_type].length>0){
                            if(!('變流器' in that.selectDevice)){
                                that.selectDevice['變流器'] = { 
                                    label: '變流器', 
                                    children: []     
                                }
                            }
                            data.data.data.equip_data[equip_type].forEach(inv => {
                                let inv_data = {
                                    label: station_str + inv.name,
                                    value: inv.ID,
                                    children: []
                                }
                                inv.point_info.forEach(point => {
                                    inv_data.children.push({
                                        label: point.name,
                                        type: 'inv',
                                        value: point.about
                                    })
                                })
                                that.selectDevice['變流器'].children.push(inv_data)
                            })
                            
                        }
                        else if(equip_type == 'meter' && data.data.data.equip_data[equip_type].length>0){
                            if(!('智慧電錶' in that.selectDevice)){
                                that.selectDevice['智慧電錶'] = { 
                                    label: '智慧電錶', 
                                    children: []     
                                }
                            }
                            data.data.data.equip_data[equip_type].forEach(meter => {
                                let meter_data = {
                                    label: ['pv_plant', 'pv_lgroup', 'pv_group'].includes(meter.collection)? 
                                        station_str.substr(0, station_str.length-1): 
                                        station_str + meter.name,
                                    value: meter.ID,
                                    children: []
                                }
                                meter.point_info.forEach(point => {
                                    meter_data.children.push({
                                        label: point.name,
                                        type: 'meter',
                                        value: point.about
                                    })
                                })
                                that.selectDevice['智慧電錶'].children.push(meter_data)
                            })
                        }
                        else if(equip_type == 'sensor' && data.data.data.equip_data[equip_type].length>0){
                            if(!('環境感測器' in that.selectDevice)){
                                that.selectDevice['環境感測器'] = { 
                                    label: '環境感測器', 
                                    children: []     
                                }
                            }
                            data.data.data.equip_data[equip_type].forEach(sensor => {
                                let sensor_data = {
                                    label: station_str + sensor.name,
                                    type: 'sensor',
                                    value: sensor.ID,
                                    parentID: that.plant_select.ID_list[i],
                                }
                                that.selectDevice['環境感測器'].children.push(sensor_data)
                            })
                        }
                    }
                    this.device_list = Object.values(this.selectDevice)
                })
            }
        },
        //-----------------------------------------------------------
        checkChange(){
			//this.$refs['seleVal'].style.display = 'block';
            let checked_node = this.$refs['device_point_ref'].getCheckedNodes()
            checked_node.forEach(node => {
                if(node.hasChildren || node.children.length > 0){
                    return
                }
                if(node.pathLabels.length == 3){
                    let name_str = `${node.pathLabels[1]}/${node.pathLabels[2]}`
                    let id_str = `${node.parent.value}_${node.value}` 
                    if(!node.checked){
                        delete this.searchDeviceList[id_str]
                        return
                    }
                    if(!(id_str in this.searchDeviceList)){
                        this.searchDeviceList[id_str] = ({
                            name: name_str,
                            type: node.data.type,
                            select: false
                        })
                    }
                }
                else if(node.pathLabels.length == 2){
                    let name_str = `${node.pathLabels[1]}`
                    let id_str = `${node.value}_value` 
                    if(!node.checked){
                        delete this.searchDeviceList[id_str]
                        return
                    }
                    if(!(id_str in this.searchDeviceList)){
                        this.searchDeviceList[id_str] = ({
                            name: name_str,
                            type: node.data.type,
                            parentID: node.data.parentID,
                            select: false
                        })
                    }
                }
                //console.log(this.searchDeviceList)
            })
		},
        //-----------------------------------------------------------
        selectSearchDevice(item){
            if(  item.select == false ){
                item.select = true;
                this.selectedDeviceList.push( item );
            }else{
                item.select = false;
                this.selectedDeviceList.forEach(function(el, idx, ary){
                    if( el.name == item.name ){
                        ary.splice(idx, 1)
                    }
                })
            }
        },
        //-----------------------------------------------------------
        deleteSearchDevice(idx){
            delete this.searchDeviceList[idx]
        },
        //-----------------------------------------------------------
        setDate(date){
            this.date_selection = date
        },
        //-----------------------------------------------------------
        //取得比較資料
        get_compare_data(){
            if(Object.keys(this.searchDeviceList).length == 0){
                alert('請至少選擇一樣儀器')
                return false
            }
            this.loading = true
            this.axios.post('/get_compare_data', {
                datepicker1: this.date_selection.date_list[0],
                datepicker2: this.date_selection.date_list[1],
                equip_list: Object.keys(this.searchDeviceList)
            }).then(data=>{
                console.log(data.data.data)
                const plot_obj = this.$refs.plot_div
                plot_obj.innerHTML = ""
                var alldata = data.data.data.return_dict
                var axisdict = data.data.data.axisdict
                let plot_data = []
                var num = 1
                let layout = {
                    width: plot_obj.clientWidth,
                    height: plot_obj.clientHeight + Object.keys(alldata).length * 20,
                    margin: c.plot_margin_ref(plot_obj),
                    paper_bgcolor: "transparent",
                    plot_bgcolor: "transparent",
                    title: {
                        text: '比較圖表',
                        font: {
                        family: "Courier New, monospace",
                        size: 24,
                        },
                    },
                    xaxis:{
                        domain: [Object.keys(axisdict).length*0.1, 1],
                        automargin: true,
                        title: {
                        text: 'Date',
                        font: {
                            family: 'Courier New, monospace',
                            size: 18,
                        }
                        },
                        
                        tickangle: 'auto',
                    },
                    legend: {
                        "orientation": "h",
                        "x" : 0, "y" : -0.4
                    },
                }
                for(var i in alldata){
                    alldata[i]['type'] = 'scatter'
                    alldata[i]['yaxis'] = "y" + alldata[i]['yaxis']
                    plot_data.push(alldata[i])
                }
                let position = 0
                for(var i in axisdict){
                    layout['yaxis'+axisdict[i]] = (parseInt(axisdict[i]) <= 1) ? {title: i,
                    } : {title: i,
                    anchor: 'free',
                    overlaying: 'y',
                    side: 'left',
                    position: position
                    }
                    position += 0.1
                }
                console.log('Ploting')
                console.log(plot_data)
                console.log(layout)
                this.Plotly.newPlot(plot_obj, plot_data, layout, {
                    displaylogo: false,
                    modeBarButtonsToRemove: [
                        "sendDataToCloud",
                        "hoverClosestCartesian",
                        "hoverCompareCartesian",
                        "toggleSpikelines",
                    ],
                })
                this.loading = false
            })
        },
        //-----------------------------------------------------------
        oneline_download() {
            var csvList = []
            var memberContent = ""
            var csvContent

            var gd = this.$refs.plot_div

            //csv title 處理
            let title = gd.querySelector("text.gtitle").innerHTML
            if(title == undefined || title == null){
                title = "export"
            }
            if(title.split(' ').length > 1){
                title = title.split(' ')[0] + "_" + title.split(' ')[1].split('(')[0]
            }else{
                title = title.split(' ')[0].split('(')[0]
            }
            let filename = title + ".csv"

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
        //-----------------------------------------------------------
        plot_resize(){
            c.plot_resize_ref(this.$refs.plot_div)
        }
    },
    mounted(){
        window.addEventListener("resize", this.plot_resize)
    },
    watch: {
        '$store.state.navOpen': function(){
            if(!this.$store.state.isMobile){
                this.plot_resize()
            }
        }
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
.history_container{
    height: 650 px;
    position: relative;
    min-width: 80%;
    border-radius: .5rem;
    /* box-shadow: 0 0 15px #DEE4EA; */
}
</style>
