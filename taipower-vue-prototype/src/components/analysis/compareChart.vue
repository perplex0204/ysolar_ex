<template>
    <div>
        <div class="d-flex flex-wrap mb-3 w-100">
            <div class="col-12 col-lg-3">
                <el-autocomplete
                    v-model="plant_search"
                    :fetch-suggestions="querySearchAsync"
                    :placeholder="$t('analysis.compareChart.search_station')"
                    value-key="name"
                    @select="handleSelect"
                    size="large"
                    class="w-100"
                ></el-autocomplete>
            </div>
            <div class="col-12 col-lg-2 ms-lg-2 mt-2 mt-lg-0">
                <el-popover
                placement="bottom-start"
                width="unset"
                popper-class="screen-limit"
                trigger="click"
                @hide="selectedDevice = []">
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
            <div class="col-12 col-lg-2 ms-auto mt-2 mt-lg-0">
                <el-popover
                placement="bottom"
                width="200"
                trigger="click">
                    <template #reference>
                        <el-button 
                        class="w-100"
                        size="large" >
                            <i class="el-icon-star-off"></i> 
                            <label v-if="myfavorite_name == null">{{$t('analysis.compareChart.my_favorite')}}</label>
                            <label v-else>{{myfavorite_name}}</label>
                        </el-button>
                    </template>
                    <div class="text-center">
                        <div>
                            <div v-show="myfavorite.length == 0">{{$t('analysis.compareChart.fav_no_text')}}</div>
                            <div
                            class="p-2"
                            style="cursor: pointer;"
                            v-for="(item, idx) in myfavorite"
                            :key="item.label">
                                <span
                                :class="{ active: item.isActive }"
                                @click="selectFavo(item, idx)">
                                    {{ item.label }}
                                </span>
                                <span 
                                @click="deleteSearchDevice(idx)"
                                >
                                    <i class="el-icon-error"></i>
                                </span>
                            </div>
                        </div>
                    </div>
                </el-popover>
            </div>
        </div>
        <div class="card p-1 p-lg-3 mb-3">
            <div class="d-flex flex-wrap">
                <!-- 選擇的儀器 -->
                <div
                class="card bg-white text-dark ms-lg-2 mt-2 p-2"
                v-for="(item, idx) in searchDeviceList"
                :key="idx">
                    <div class="d-flex align-items-center">
                        <label class="ms-2" @click="selectSearchDevice(item)">{{ item.name }}</label>
                        <button class="btn"
                        @click="deleteSearchDevice(idx)"><i class="el-icon-close"></i></button>
                    </div>
                </div>
            </div>
            <div class="d-flex flex-wrap mt-4">
                <div class="col-12 col-lg-10">
                    <el-input v-model="addFavoName" :placeholder="$t('analysis.compareChart.enter_favorite_name')" size="large"></el-input>
                </div>
                <div class="col-12 col-lg-auto ms-lg-2 mt-2 mt-lg-0">
                    <button class="btn btn-light" @click="addToMyFavo()">
                        {{$t('analysis.compareChart.save_favorite')}}
                    </button>
                </div>
            </div>
            <el-divider></el-divider>
            <div class="w-100">
                <timeRangePicker @setDate="setDate" />
            </div>
            <div class="d-flex w-100 mt-3 d-none">
                <button class="btn btn-primary ms-auto" @click="get_compare_data()">
                    {{$t('analysis.compareChart.start_compare')}}
                </button>
            </div>
        </div>
        <div class="card p-lg-3 mb-3" v-loading="loading">
            <button class="btn btn-primary col-12 col-lg-2" @click="oneline_download">
                {{$t('analysis.compareChart.export_csv')}}
            </button>
            <div id="plot_div" class="mt-3 rounded-3 plot_div_compare"></div>
        </div>
    </div>
</template>

<script>

import c from 'assets/js/common.js';
import timeRangePicker from "@/components/datepicker/timeRangePickerSimple.vue";

export default {
    name: "compareChart",
    components:{
        timeRangePicker
    },
    data(){
        return {
            myfavorite_name: null,
            loading: false,
            //plant search
            plant_select: {'ID_list': [], 'col_list': []},
            plant_search: "",
            //device list after station choose 
            device_list: [],
            //cascader selected device
            selectedDevice: [],
            searchDeviceList: {},
            //favorite group
            myfavorite: [],
            addFavoName: '',
            //date select
            date_selection: {},
        }
    },
    methods: {
        //-----------------------------------------------------------
        async querySearchAsync(queryString, cb) {
			//console.log(queryString)
			//console.log(this.PV_data)
            await this.axios.post('/station_search_regex', {
                query: queryString
            }).then(data => {
                //console.log(data.data.data)
                if(data.data.data.length == 0){
                    cb([{'name': '無資料'}])
                }else{
                    cb(data.data.data)
                }
            })	
		},
        //-----------------------------------------------------------
        handleSelect(item) {
			//console.log(item)
			this.plant_select.ID_list = [item.ID]
            this.plant_select.col_list = [item.collection]
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
        // get favorite tool
        get_compare_group(){
            let that = this
            this.axios.get('/compare_group_tool').then(data=>{
                that.myfavorite = []
                //console.log(data.data.data)
                data.data.data.group_data.forEach(group => {
                    that.myfavorite.push({
                        label: group.name,
                        isActive: false,
                        favoList: group.equip_data
                    })
                })
            })
        },
        //-----------------------------------------------------------
        deleteSearchDevice(idx){
            delete this.searchDeviceList[idx]
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
        selectFavo(item){
            //console.log(item)
            this.myfavorite_name = item.label
            this.addFavoName = item.label
            this.myfavorite.forEach(el => el.isActive = false);
            item.isActive = true;
            this.myfavoriteSelect = item.label;
            this.searchDeviceList = {}
            item.favoList.forEach(equip=>{
                this.searchDeviceList[`${equip.ID}_${equip.about}`] = ({
                    name: equip.label,
                    type: equip.type,
                    select: false
                })
            })
        },
        //-----------------------------------------------------------
        addToMyFavo(){
            if(this.addFavoName == null || this.addFavoName == undefined || this.addFavoName == ""){
                this.$message({
                    message: '請輸入我的最愛名稱',
                    type: 'error'
                })
                return false
            }
            //console.log(this.searchDeviceList)
            let equip_list = []
            for(var _id in this.searchDeviceList){
                if(this.searchDeviceList[_id].type == 'sensor'){
                    equip_list.push({
                        ID: _id.slice(0, _id.indexOf('_')),
                        type: this.searchDeviceList[_id].type,
                        about: _id.slice(_id.indexOf('_')+1),
                        parentID: this.searchDeviceList[_id].parentID
                    })
                }else{
                    equip_list.push({
                        ID: _id.slice(0, _id.indexOf('_')),
                        type: this.searchDeviceList[_id].type,
                        about: _id.slice(_id.indexOf('_')+1)
                    })
                }
                
            }
            let that = this
            this.axios.post('/compare_group_tool', {
                'name': this.addFavoName,
                'equip_data': equip_list
            }).then(data => {
                that.$message({
                    message: '已成功加入我的最愛',
                    type: 'success'
                })
                that.get_compare_group()
            }).catch(error => {
                console.log(error)
                that.$message({
                    message: '儲存失敗',
                    type: 'error'
                })
            })
        },
        //-----------------------------------------------------------
        //取得比較資料
        get_compare_data(){
            if(Object.keys(this.searchDeviceList).length == 0){
                alert('請至少選擇一樣儀器')
                return false
            }
            this.axios.post('/get_compare_data', {
                datepicker1: this.date_selection.date_list[0],
                datepicker2: this.date_selection.date_list[1],
                equip_list: Object.keys(this.searchDeviceList)
            }).then(data=>{
                console.log(data.data.data)
                const plot_obj = document.getElementById('plot_div')
                plot_obj.innerHTML = ""
                var alldata = data.data.data.return_dict
                var axisdict = data.data.data.axisdict
                let plot_data = []
                var num = 1
                let layout = {
                    width: plot_obj.clientWidth,
                    height: plot_obj.clientHeight + Object.keys(alldata).length * 20,
                    margin: c.plot_margin(),
                    paper_bgcolor: "transparent",
                    plot_bgcolor: "transparent",
                    font: {
                        color: window.getComputedStyle( document.body ,null).getPropertyValue('color')
                    },
                    title: {
                        text: this.$i18n.t('plot.比較圖表'),
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
            })
        },
        //-----------------------------------------------------------
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
        //-----------------------------------------------------------
        setDate(date){
            this.date_selection = date
        },
        plot_rename() {
            let update = {
                title: {
                        text: this.$i18n.t('plot.比較圖表'),
                        font: {
                            family: "Courier New, monospace",
                            size: 24,
                        },
                    },
            }
            this.Plotly.relayout("plot_div", update)
        }
    },
    mounted(){
        this.get_compare_group()
        window.addEventListener("resize", c.plot_resize)
    },
    unmounted(){
        window.removeEventListener("resize", c.plot_resize)
    },
    watch:{
		plant_select: function(){
            this.get_equip_select()
		},
        date_selection(){
            if(Object.keys(this.searchDeviceList).length == 0){
                return false
            }
            this.get_compare_data()
        },
        '$store.state.language': function() {
            try{
                this.plot_rename()
            }
            catch{
                console.log("plot yet")
            }
        },
	},

}
</script>
<style scoped>
.no-border-inside{
    border: 0px !important;
}
.plot_div_compare{
    min-height: 500px;
    overflow: scroll;
}
</style>