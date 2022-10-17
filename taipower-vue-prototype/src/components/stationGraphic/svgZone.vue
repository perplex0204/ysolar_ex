<template>
    <div class="card p-0 w-100 mb-3" style="overflow-x: hidden;" :style="{'min-height': minHeight}">
        <div id="svg_zone"></div>
        <div id="tooltip">
            <div id="tooltip_bulr"></div>
            <div id="tooltip_main">
                <div v-if="table_data_type == 'pv_plant' || table_data_type == 'pv_lgroup'">
                    <table class="tooltip_table">
                        <tr>
                            <th>{{$t("名稱")}}</th>
                            <th>{{$t("數值")}}</th>
                        </tr>
                        <tr>
                            <td>{{$t("datatype.發電量")}}(kWh)</td>
                            <td class="kwh">{{table_data[table_data_type].kwh.data}}</td>
                        </tr>
                        <tr>
                            <td>RA(%)</td>
                            <td class="RA">{{table_data[table_data_type].RA.data}}</td>
                        </tr>
                        <tr>
                            <td>PR(%)</td>
                            <td class="PR">{{table_data[table_data_type].PR.data}}</td>
                        </tr>
                    </table>
                    <div class="tooltip_head_color"></div>
                </div>
                <div v-else-if="table_data_type == 'inv'">
                    <table class="tooltip_table">
                        <tr>
                            <th>{{$t("名稱")}}</th>
                            <th>{{$t("數值")}}</th>
                        </tr>
                        <tr>
                            <td>{{$t("datatype.直流功率")}}(kW)</td>
                            <td class="p_cell_total">{{table_data.inv.p_cell_total.data}}</td>
                        </tr>
                        <tr>
                            <td>{{$t("datatype.交流功率")}}(kW)</td>
                            <td class="p_bus_total">{{table_data.inv.p_bus_total.data}}</td>
                        </tr>
                        <tr>
                            <td>{{$t("datatype.發電量")}}(kWh)</td>
                            <td class="kwh">{{table_data.inv.kwh.data}}</td>
                        </tr>
                        <tr>
                            <td>RA(%)</td>
                            <td class="RA">{{table_data.inv.RA.data}}</td>
                        </tr>
                        <tr>
                            <td>PR(%)</td>
                            <td class="PR">{{table_data.inv.PR.data}}</td>
                        </tr>
                    </table>
                    <div class="tooltip_head_color"></div>
                </div>
                <div v-else-if="table_data_type == 'string'">
                    <table class="tooltip_table_string" >
                        <tr>
                            <th colspan="4" class="name">{{table_data['string'].name.data}}</th>
                        </tr>
                        <tr>
                            <th>{{$t("datatype.串列電流")}}</th>
                            <th>{{$t("數值")}}(A)</th>
                            <th>{{$t("datatype.串列電流")}}</th>
                            <th>{{$t("數值")}}(A)</th>
                        </tr>
                        <tr v-for="(item, idx) in table_data['string'].sa.data" :key="idx">
                            <td>{{item[1].ch}}</td>
                            <td>{{item[1].data}}</td>
                            <td>{{item[2].ch}}</td>
                            <td>{{item[2].data}}</td>
                        </tr>
                    </table>
                    <div class="tooltip_head_color"></div>
                    <div v-if="table_data['string'].event.data.length >0"  
                        class="tooltip_head_color" 
                        style="position: relative; border-radius: 0px; margin-top: 2rem"
                    >
                        {{$t("事件")}}
                    </div>
                    <table class="tooltip_table">
                        <tr v-for="(item, idx) in table_data['string'].event.data" :key="idx">
                            <td colspan="4">
                                <p style="color: black;">{{item.first}}</p>
                                {{item.second}}
                            </td>
                        </tr>
                    </table>
                </div>
            </div>
        </div>
    </div>
</template>
<script>
import Hammer from "hammerjs"
import svgPanZoom from "svg-pan-zoom"

export default{
    name: "svgZone",
    props: {
        plant_select: {
            type: Array
        }, 
        svg_path: {
            default: null
        },
        minHeight: {
            default: "50vh"
        }
    },
    data(){
        return{
            IDList: [],
            allData: {},
            timeOut: null,
            tooltipShow: false,
            tooltipTimer: null,
            table_data_type: null,
            table_data: {
                pv_plant: {
                    kwh: {name: 'kwh', round: 1, data: '---'},
                    RA: {name: 'RA', round: 1, data: '---'},
                    PR: {name: 'PR', round: 1, data: '---'}
                },
                pv_lgroup: {
                    kwh: {name: 'kwh', round: 1, data: '---'},
                    RA: {name: 'RA', round: 1, data: '---'},
                    PR: {name: 'PR', round: 1, data: '---'}
                },
                inv: {
                    p_cell_total: {name: 'p_cell_total', round: 1, data: '---'},
                    p_bus_total: {name: 'p_bus_total', round: 1, data: '---'},
                    kwh: {name: 'kwh', round: 1, data: '---'},
                    RA: {name: 'RA', round: 1, data: '---'},
                    PR: {name: 'PR', round: 1, data: '---'}
                },
                string: {
                    name: {name: 'name', data: '串列電流'},
                    sa: {name: 'sa', round: 1, data: []},
                    event: {name: 'event', data: []}
                },
                else: {}
            }
        }
    },
    emits: ["change-layout"],
    methods:{
        loadSVG() {
            let vm = this
            let loading_result = false
            fetch(this.svg_path).then(function(response){
                //console.log(response)
                if(response.ok){
                    return response.text()
                }else{
                    throw new Error('No responding svg found')
                }
            })
            .then(text =>{
                console.log('success_load svg')
                document.getElementById('svg_zone').innerHTML = text
                vm.hammer_svg(vm)
                vm.listen_svg(vm)
                loading_result = true
            })
            .catch(function(e){
                console.error(e)
                fetch('./solar_static/SLD/fail.svg').then(res => res.text())
                .then(text =>{
                    document.getElementById('svg_zone').innerHTML = text
                    loading_result = false
                })
            }) 
            return loading_result
        },
        //-------------------------------------------------------------------------------------------------------------------
        hammer_svg(vm){
            let eventsHandler = {
                haltEventListeners: [
                    "touchstart",
                    "touchend",
                    "touchmove",
                    "touchleave",
                    "touchcancel",
                ],
                init: function (options) {
                    var instance = options.instance,
                    initialScale = 1,
                    pannedX = 0,
                    pannedY = 0

                    // Init Hammer
                    // Listen only for pointer and touch events
                    this.hammer = Hammer(options.svgElement, {
                    inputClass: Hammer.SUPPORT_POINTER_EVENTS
                        ? Hammer.PointerEventInput
                        : Hammer.TouchInput,
                    })

                    // Enable pinch
                    this.hammer.get("pinch").set({ enable: true })

                    // Handle double tap
                    this.hammer.on("doubletap", function (ev) {
                        instance.zoomIn()
                    })

                    // Handle pan
                    this.hammer.on("panstart panmove", function (ev) {
                        // On pan start reset panned variables
                        if (ev.type === "panstart") {
                            pannedX = 0
                            pannedY = 0
                        }

                        // Pan only the difference
                        instance.panBy({ x: ev.deltaX - pannedX, y: ev.deltaY - pannedY })
                        pannedX = ev.deltaX
                        pannedY = ev.deltaY
                    })

                    // Handle pinch
                    this.hammer.on("pinchstart pinchmove", function (ev) {
                        // On pinch start remember initial zoom
                        if (ev.type === "pinchstart") {
                            initialScale = instance.getZoom()
                            instance.zoomAtPoint(initialScale * ev.scale, {
                            x: ev.center.x,
                            y: ev.center.y,
                            })
                        }

                        instance.zoomAtPoint(initialScale * ev.scale, {
                            x: ev.center.x,
                            y: ev.center.y,
                        })
                    })

                    // Prevent moving the page on some devices when panning over SVG
                    options.svgElement.addEventListener("touchmove", function (e) {
                        e.preventDefault()
                    })
                },

                destroy: function () {
                    this.hammer.destroy()
                },
            }
            vm.getSVGIDList(vm).then(() => {
                vm.getIDListData(vm, 1)

                var svgElement = document.querySelector("#svg_zone>svg")
                panZoomInstance = svgPanZoom(svgElement, {
                zoomEnabled: true,
                controlIconsEnabled: true,
                dblClickZoomEnabled: false,
                minZoom: 1,
                refreshRate: "auto",
                beforePan: function (oldPan, newPan) {
                    let gutterWidth = document.getElementById('svg_zone').clientWidth + 0.5
                    let gutterHeight = document.getElementById('svg_zone').clientHeight + 0.5
                    // console.log(gutterWidth, gutterHeight)
                    // Computed variables
                    let sizes = this.getSizes()
                    let leftLimit =
                    -((sizes.viewBox.x + sizes.viewBox.width) * sizes.realZoom) +
                    gutterWidth
                    let rightLimit =
                    sizes.width - gutterWidth - sizes.viewBox.x * sizes.realZoom
                    let topLimit =
                    -((sizes.viewBox.y + sizes.viewBox.height) * sizes.realZoom) +
                    gutterHeight
                    let bottomLimit =
                    sizes.height - gutterHeight - sizes.viewBox.y * sizes.realZoom

                    let customPan = {}
                    customPan.x = Math.max(leftLimit, Math.min(rightLimit, newPan.x))
                    customPan.y = Math.max(topLimit, Math.min(bottomLimit, newPan.y))
                    // console.log(leftLimit, rightLimit, newPan.x)
                    document.getElementById("tooltip").style.display = "none"
                    document.querySelectorAll(".tooltip_table").forEach(element =>{
                        element.style.display = "none"
                    })
                    vm.tooltipShow = false
                    vm.tooltipTimer = clearInterval(vm.tooltipTimer)
                    return customPan
                },
                onZoom: function (e) {
                    if (e <= 1) {
                    panZoomInstance.disablePan()
                    }
                    if (!panZoomInstance.isPanEnabled() && e > 1) {
                    panZoomInstance.enablePan()
                    }
                },
                customEventsHandler: eventsHandler,
                })
            })
            vm.getIDListData(vm, 0)
            let svgElement = document.querySelector("#svg_zone>svg")
            let panZoomInstance = svgPanZoom(svgElement, {
                zoomEnabled: true,
                controlIconsEnabled: true,
                dblClickZoomEnabled: false,
                minZoom: 1,
                refreshRate: "auto",
                beforePan: function (oldPan, newPan) {
                let gutterWidth = document.getElementById('svg_zone').clientWidth + 0.5
                let gutterHeight =document.getElementById('svg_zone').clientHeight + 0.5
                // console.log(gutterWidth, gutterHeight)
                // Computed variables
                let sizes = this.getSizes()
                let leftLimit =
                    -((sizes.viewBox.x + sizes.viewBox.width) * sizes.realZoom) +
                    gutterWidth
                let rightLimit =
                    sizes.width - gutterWidth - sizes.viewBox.x * sizes.realZoom
                let topLimit =
                    -((sizes.viewBox.y + sizes.viewBox.height) * sizes.realZoom) +
                    gutterHeight
                let bottomLimit =
                    sizes.height - gutterHeight - sizes.viewBox.y * sizes.realZoom

                let customPan = {}
                customPan.x = Math.max(leftLimit, Math.min(rightLimit, newPan.x))
                customPan.y = Math.max(topLimit, Math.min(bottomLimit, newPan.y))
                // console.log(leftLimit, rightLimit, newPan.x)

                return customPan
                },
                onZoom: function (e) {
                if (e <= 1) {
                    panZoomInstance.disablePan()
                }
                if (!panZoomInstance.isPanEnabled() && e > 1) {
                    panZoomInstance.enablePan()
                }
                },
                customEventsHandler: eventsHandler,
            })

        },
        //-------------------------------------------------------------------------------------------------------------------
        listen_svg(vm){
            let that = this
            document.querySelectorAll("g").forEach((obj) =>{
                obj.addEventListener("mouseover", function(e){
                    let attr1 = this.getAttribute("data-svg") 
                    let attr2 = this.getAttribute("data-a")
                    let attr3 = this.getAttribute("data-heatmap")
                    let attr4 = this.getAttribute("data-thermal_image")
                    if (
                        (attr1 !== undefined && attr1 !== false  && attr1 !== null) ||
                        (attr2 !== undefined && attr2 !== false && attr2 !== null) ||
                        (attr3 !== undefined && attr3 !== false && attr3 !== null) ||
                        (attr4 !== undefined && attr4 !== false && attr4 !== null)
                    ) {
                        this.style.cursor = "pointer"
                    } 
                })
            })
            //---------------------------------------------------------------------------------------------------------------
            document.querySelectorAll("g[data-hover]").forEach((obj) =>{
                obj.addEventListener("mouseover", function(e){
                    let eid = this.getAttribute("data-eid")
                    let hoverobj = document.querySelector(`g[data-hover="1"][data-eid="${eid}"]`)
                    if(hoverobj == null || hoverobj == undefined){
                        return
                    }
                    Array.from(hoverobj.children).forEach((element)=>{
                        let latestFill = element.getAttribute("fill")
                        let latestFillOpacity = element.getAttribute("fill-opacity")
                        let latestStatus = element.getAttribute("data-status")
                        element.setAttribute("fill", "#212F3D")
                        element.setAttribute("fill-opacity", 0.8)
                        element.setAttribute("data-status", "100")
                        element.setAttribute("latestFillOpacity", latestFillOpacity)
                        element.setAttribute("latestFill", latestFill)
                        element.setAttribute("latestStatus", latestStatus)
                    })
                })
                obj.addEventListener("mouseleave", function(e){
                    let eid = this.getAttribute("data-eid")
                    let hoverobj = document.querySelector(`g[data-hover="1"][data-eid="${eid}"]`)
                    if(hoverobj == null || hoverobj == undefined){
                        return
                    }
                    Array.from(hoverobj.children).forEach((element)=>{
                        let latestFill = element.getAttribute("latestFill")
                        let latestFillOpacity = element.getAttribute("latestFillOpacity")
                        let latestStatus = element.getAttribute("latestStatus")
                        element.setAttribute("fill",latestFill)
                        element.setAttribute("fill-opacity", latestFillOpacity)
                        element.setAttribute("data-status", latestStatus)
                    })
                })
            })
            //---------------------------------------------------------------------------------------------------------------
            document.querySelectorAll("g[data-svg]").forEach((obj) => {
                let attr = obj.getAttribute("data-svg")
                obj.addEventListener("dblclick", function(){
                    that.$emit('change-layout', attr)
                })
            })
            //---------------------------------------------------------------------------------------------------------------
            document.querySelectorAll("g[data-tooltip]").forEach((obj) =>{
                obj.addEventListener("mouseover", function(e){
                    clearTimeout(that.timeOut)
                    this.style.cursor = "pointer"
                    if (that.tooltipShow == false) {
                        let id = this.getAttribute("data-eid")
                        let type = that.allData[id]["type"]
                        that.table_data_type = type

                        that.updateTooltipTable(id, type, e, that)
                        that.tooltipTimer = setInterval(function () {
                            that.updateTooltipTable(id, type, undefined, that)
                        }, 5000)
                        that.tooltipShow = true
                    }
                })
                obj.addEventListener("mouseleave", function(e){
                    that.timeOut = setTimeout(() => {
                        that.tooltipTableReset(that)
                    }, 10)
                    that.tooltipTimer = clearInterval(that.tooltipTimer) 
                    that.tooltipShow = false
                })
            })  
            //---------------------------------------------------------------------------------------------------------------
            let tooltip = document.getElementById("tooltip")
                tooltip.addEventListener("mouseover", function(e){
                    clearTimeout(that.timeOut)
                })
                tooltip.addEventListener("mouseleave", function(e){
                    that.tooltipTableReset(that)
                })
        },
        //-------------------------------------------------------------------------------------------------------------------
        updateTooltipTable(id, type, e, vm) {
            let allData = vm.allData
            //更新tooltipTable
            let keyList = []
            if (type == "pv_plant" || type == "pv_group") {
                keyList = [
                { text: "kwh", round: "1" },
                { text: "RA", round: "1" },
                { text: "PR", round: "1" },
                ]
            } else if (type == "inv") {
                keyList = [
                { text: "p_cell_total", round: "1" },
                { text: "p_bus_total", round: "1" },
                { text: "kwh", round: "1" },
                { text: "RA", round: "1" },
                { text: "PR", round: "1" },
                ]
            } else if (type === "string") {
                keyList = [
                { text: "sa", round: "1" },
                { text: "event", round: null },
                ]
            }
            if (type !== "string") {
                for(var key in vm.table_data[type]){
                    let point = vm.table_data[type][key]
                    vm.table_data[type][key].data = vm.valueSet(allData[id][key], point.round)
                }                
            } else {
                vm.table_data["string"].name.data = allData[id].name
                console.log(id, allData[id].name)
                // console.log(allData[id].name)
                keyList.forEach((key) => {
                    // console.log(id, allData[id], key)
                    const serial_num = allData[id].serial_num
                    if (key.text == "sa") {
                        vm.table_data["string"].sa.data = []
                        //$(".tooltip_table[data-type~=string] .sa").remove()
                        for (let i = 1; i < parseInt(serial_num / 2) + 1; i++) {
                            let _row = {
                                1: {
                                    ch: "#" + (i * 2 - 1), 
                                    data: 
                                        vm.valueSet(
                                            allData[id][key.text] !== undefined
                                            ? allData[id][key.text][i * 2 - 2]
                                            : undefined,
                                            key.round)
                                }, 
                                2: {
                                    ch: "#" + i * 2,
                                    data: 
                                        vm.valueSet(
                                            allData[id][key.text] !== undefined
                                            ? allData[id][key.text][i * 2 - 1]
                                            : undefined,
                                            key.round
                                        )
                                }
                            }
                            vm.table_data["string"].sa.data.push(_row)
                        }
                        if (serial_num % 2 === 1) {
                            let _row = {
                                1: {
                                    ch: "#" + serial_num, 
                                    data: 
                                        vm.valueSet(
                                            allData[id][key.text] !== undefined
                                            ? allData[id][key.text][serial_num - 1]
                                            : undefined,
                                            key.round
                                        )
                                }, 
                                2: {
                                    ch: "",
                                    data: ""
                                }
                            }
                            vm.table_data["string"].sa.data.push(_row)
                        }
                    } else if (key.text == "event") {
                        vm.table_data["string"].event.data = []
                        allData[id].event.forEach((event) => {
                        if (event.event !== undefined) {
                            vm.table_data["string"].event.data.push({
                                first: `${event.channel} ${event.event}`,
                                second: `(${event.start} ~ ${event.end})`
                            })
                        } else {
                            vm.table_data["string"].event.data.push({
                                first: `${event.channel} 異常診斷中`,
                                second: `(${event.start}})`
                            })
                        }
                        })
                    } else {
                        // To Use Below commented code, remember convert to pure js

                        /* $(`.tooltip_table[data-type~=string] .${key.text}`).text(
                        valueSet(allData[id][key.text], key.round)
                        ) */
                    }
                })
            }

            if (e !== undefined) {
                let tooltip = document.getElementById("tooltip")
                let x = e.clientX
                let y = e.clientY
                //console.log(x, y)
                y = y - document.getElementById("svg_zone").getBoundingClientRect().left
                x = x - document.getElementById("svg_zone").getBoundingClientRect().top
                let yLimit = document.getElementById("svg_zone").clientHeight + document.getElementById("svg_zone").getBoundingClientRect().top - 400
                let xLimit = document.getElementById("svg_zone").clientWidth + document.getElementById("svg_zone").getBoundingClientRect().left - 600
                x = x > xLimit ? e.clientX-600 : x < 0 ? 0 : x
                y = y > yLimit ? yLimit : y < 0 ? 0 : y
                //console.log(x, y, xLimit, yLimit)
                tooltip.style.position = 'absolute'
                tooltip.style.top = `${y}px`
                tooltip.style.left = `${x}px`
                tooltip.style.display = 'block'
            }
        },
        //---------------------------------------------------------------------------
        tooltipTableReset(vm) {
          let tooltip = document.getElementById("tooltip")
          vm.table_data_type = null
          tooltip.style.display = "none"
          console.log("leave")
          //$(".tooltip_table").hide()

        },
        //-------------------------------------------------------------------------------------------------------------------
        valueSet(value, round) {
            if (round === null) return
            if (value === undefined) return "---"
            else {
                if (value === null) {
                value = "---"
                } else if (round !== undefined) {
                value = parseFloat(value).toFixed(round)
                }
            }
            return value
        },
        //-------------------------------------------------------------------------------------------------------------------
        async getSVGIDList(vm){
            const nodeList = Array.apply(null, document.querySelectorAll("g[data-eid]"))
            const _IDList = new Set()
            nodeList.forEach((object) => {
                _IDList.add(object.getAttribute("data-eid"))
            })
            vm.IDList = Array.from(_IDList)
        },
        //-------------------------------------------------------------------------------------------------------------------
        getIDListData(vm, e) {
            vm.axios.post("/getIDListData", {
                plant: vm.plant_select[1],
                lgroup:vm.plant_select[2],
                IDList: vm.IDList,
            }).then(
                function (data) {
                    const nodeList = Array.apply(
                    null,
                    document.querySelectorAll("g[data-eid]")
                    )
                    let allData = data.data.data
                    vm.allData = allData 
                    vm.svgValueText(
                    vm,
                    null,
                    "inverter_status",
                    allData.inverterNormalNumber + "/" + allData.inverterNumber,
                    undefined,
                    undefined,
                    undefined
                    )
                    vm.svgValueText(
                    vm,
                    null,
                    "lgroup_inverter_status",
                    allData.lgroup_inverterNormalNumber + "/" + allData.lgroup_inverterNumber,
                    undefined,
                    undefined,
                    undefined
                    )
                    vm.svgValueText(
                    vm,
                    null,
                    "plant_inverter_status",
                    allData.plant_inverterNormalNumber + "/" + allData.plant_inverterNumber,
                    undefined,
                    undefined,
                    undefined
                    )

                    nodeList.forEach((node) => {
                        const ID = node.getAttribute("data-eid") 
                        const datatype = node.getAttribute("data-datatype")
                        const tag = node.getAttribute("data-tag")
                        const round = node.getAttribute("data-round")
                        const unit = node.getAttribute("data-unit")
                        const a = node.getAttribute("data-a")
                        const status = node.getAttribute("data-status")

                        //value
                        if (datatype !== undefined) {
                            vm.svgValueText(
                            vm,
                            ID,
                            datatype,
                            allData[ID] !== undefined ? allData[ID][datatype] : undefined,
                            tag,
                            round,
                            unit
                            )
                        }
                        //status
                        if (status !== undefined) {
                            vm.svgStateSet(vm, ID, allData[ID] !== undefined ? allData[ID].state : 100)
                        }
                        //inverter_status
                        vm.svgValueText(
                            vm,
                            null,
                            "inverter_status",
                            `${allData.inverterNormalNumber} / ${allData.inverterNormalNumber}`,
                            undefined,
                            undefined,
                            undefined
                        )
                        if (e == 1) {
                            //aTag
                            if (a !== undefined) {
                                node.addEventListener("dblclick", function(e){
                                    vm.toPvInfo(this)
                                })
                            }
                        }
                    })
                    for (var eid in allData) {
                        let data = allData[eid]
                        if (data.type == "string") {
                            // console.log(data.event)
                            if (data.event.length != null) {
                            data.event.forEach((event) => {
                                if (event.method == "PVLOF") {
                                let string = event.channel.split("String")[1]
                                //console.log(eid, string)
                                let stringobj = document.querySelector(`g[data-eid="${eid}"][data-string="${string}"]`)
                                //console.log(stringobj)
                                if(stringobj != null && stringobj != undefined){  
                                    let linelist = stringobj.children 
                                    //console.log(linelist)                                
                                    Array.from(linelist).forEach((element)=>{
                                        if (element.hasAttribute("classification")) {
                                            let classification = element.getAttribute("classification")
                                            //console.log(classification)
                                            if (classification * 1 <= event.classification) {
                                                return
                                                }
                                        }
                                        let color = undefined
                                        let strokeWidth = undefined
                                        let blink = ""
                                        //console.log(event)
                                        switch (event.level) {
                                            case 1:
                                            blink = "blink"
                                            color = "#FCE903"
                                            strokeWidth = "5px"
                                            break
                                            case 2:
                                            color = "#fe6c05"
                                            strokeWidth = "5px"
                                            break
                                        }
                                        //console.log(color, strokeWidth)
                                        if (color !== undefined && strokeWidth !== undefined){
                                            element.setAttribute("stroke-width", strokeWidth)
                                            element.setAttribute("stroke", color)
                                            element.setAttribute("stroke-opacity", 1)
                                            element.setAttribute("classification", event.classification)
                                            element.classList.remove("blink")
                                            element.classList.addClass(blink)
                                        }
                                    })
                                }    
                            }
                            })
                        }
                    }
                }
            })
            return false
        },        
        //-------------------------------------------------------------------------------------------------------------------
        svgValueText(vm, ID, datatype, value, tag, round, unit) {
            //console.log(ID, datatype, value, tag, round, unit)
            if (value === undefined) return
            else {
                if (value === null) {
                    value = ""
                } else if (round !== undefined && round !== null) {
                    value = parseFloat(value).toFixed(round)
                }
                if (tag != undefined && tag != null) {
                    value = tag + ":" + value
                }
                if (unit !== undefined && unit !== null) {
                    value = value + unit
                }
            }
            if (ID != null) {
                if (
                    document.querySelector(`#svg_zone g[data-eid="${ID}"][data-datatype="${datatype}"]   foreignObject div div div font b`
                    )!= null
                ) {
                    document.querySelector(`#svg_zone g[data-eid="${ID}"][data-datatype="${datatype}"]   foreignObject div div div font b`
                    ).innerHTML = value
                } else if (
                    document.querySelector(`#svg_zone g[data-eid="${ID}"][data-datatype="${datatype}"]   foreignObject div div div font`
                    )!= null
                ) {
                    document.querySelector(`#svg_zone g[data-eid="${ID}"][data-datatype="${datatype}"]   foreignObject div div div font`
                    ).innerHTML = value 
                } else if (
                    document.querySelector(`#svg_zone g[data-eid="${ID}"][data-datatype="${datatype}"]   foreignObject div div div`
                    )!= null
                ) {
                    document.querySelector(`#svg_zone g[data-eid="${ID}"][data-datatype="${datatype}"]   foreignObject div div div`
                    ).innerHTML = value
                }
            } else {
                if (
                    document.querySelector(`#svg_zone g[data-datatype="${datatype}"]   foreignObject div div div font b`
                    )!= null
                ) {
                    document.querySelector(`#svg_zone g[data-datatype="${datatype}"]   foreignObject div div div font b`
                    ).innerHTML = value
                } else if (
                    document.querySelector(`#svg_zone g[data-datatype="${datatype}"]   foreignObject div div div font`
                    )!= null
                ) {
                    document.querySelector(`#svg_zone g[data-datatype="${datatype}"]   foreignObject div div div font`
                    ).innerHTML = value
                } else if (
                    document.querySelector(`#svg_zone g[data-datatype="${datatype}"]   foreignObject div div div`
                    )!= null
                ) {
                    document.querySelector(`#svg_zone g[data-datatype="${datatype}"]   foreignObject div div div`
                    ).innerHTML = value
                }
            }
        },
        //-------------------------------------------------------------------------------------------------------------------
        svgStateSet(vm, ID, status) {
            let text = ""
            let color = ""
            let blink = ""
            switch (status) {
            case 0:
                text = "正常"
                color = "#0c0"
                break
            case 1:
                text = "一級警報"
                color = "#ffeb3b"
                blink = "blink"
                break
            case 2:
                text = "二級警報"
                color = "#fe6c05"
                blink = "blink"
                break
            case 3:
                text = "斷線"
                color = "rgb(184, 168, 168)"
                blink = "blink"
                break
            default:
                color = "grey"
                blink = "blink"
            }
            document.querySelectorAll(`#svg_zone g[data-eid="${ID}"][data-status="1"]`).forEach((obj) => {
                let list = obj.children
                Array.from(list).forEach((element)=>{
                    element.setAttribute("fill", color)
                    element.classList.add(`"${blink}"`)
                })
            })
            
            

        
            if (
                document.querySelector(
                    `#svg_zone g[data-eid="${ID}"][data-status="2"]   foreignObject div div div font b`
                ) != null
            ) {
                let element = document.querySelector(
                `#svg_zone g[data-eid="${ID}"][data-status="2"]  foreignObject div div div font b`
                )
                element.innerHTML = text
                element.style.color = color
            } else if (
                document.querySelector(
                    `#svg_zone g[data-eid="${ID}"][data-status="2"]   foreignObject div div div font`
                ) != null
            ) {
                let element = document.querySelector(
                    `#svg_zone g[data-eid="${ID}"][data-status="2"]  foreignObject div div div font`
                )
                element.innerHTML = text
                element.style.color = color
            } else if (
                document.querySelector(
                    `#svg_zone g[data-eid="${ID}"][data-status="2"]   foreignObject div div div`
                ) != null
            ) {
                let element = document.querySelector(`#svg_zone g[data-eid="${ID}"][data-status="2"]  foreignObject div div div`)
                element.innerHTML = text
                element.style.color = color
            }
        },
        toPvInfo(e) {
            const ID = e.getAttribute('data-eid')
            this.axios.post('/equip_ID_get_group_data', {
                ID: ID
            }).then(data=>{
                this.$router.push({path: "stationData", query: {ID: data.data.data.ID, collection: data.data.data.collection,
                pageMode: "equipment", equip_ID: ID}})
            })
        }
    },
    //-------------------------------------------------------------------------------------------------------------------
    watch: {
        svg_path: function(newVal, oldVal){
            if(newVal != null && newVal != undefined ){
                if(newVal.length > 0){
                    this.loadSVG()
                }
            }else if(newVal == null){
                document.getElementById('svg_zone').innerHTML = ""
            }
        },
    },
    mounted(){
        let that = this
        this.syncdata = setInterval(function () {
            if (that.IDList.length > 0) {
                that.getIDListData(that)
            }
        }, 10000)
    },
    unmounted(){
        clearInterval(this.syncdata)
    }
}
</script>
<style scoped>
#svg_zone:deep(svg){
    width: 100%;
    height: auto;
}
.blink {
    animation: fade 800ms infinite;
    -webkit-animation: fade 800ms infinite;
}
#tooltip{
    display: none;
    border-radius: 5px;
    border: 1px solid #DCDFE6;
    box-shadow: 0 0 15px rgba(63,63,63,.1);
    color: black;
}
.tooltip_main {
    /* display: inline-block; */
    overflow-y: auto;
    min-height: 50px;
    max-height: 300px;
    /* background-color: #fff; */
    border-radius: 5px;
}
#tooltip_bulr{
    position: absolute;
    width: 100%;
    height: 100%;
    opacity: .5;
    background-color: white;
    opacity: .95;
    border-radius: 5px;
}
.tooltip_head_color{
    height: 25px;
    background-image: linear-gradient(90deg, rgba(255,125,74,1) 0%, rgba(255,199,114,1) 100%);
    width: 100%;
    position: absolute;
    top: 0;
    border-radius: 5px 5px 0 0;
    color: white;
    font-weight: bold;
}
.tooltip_table{
    /* table-layout: fixed; */
    width: 350px;
    text-align: center;
    position: relative;
    z-index: 1;
}
.tooltip_table tr th {
    /* background-attachment: fixed !important;
    background-image: linear-gradient(90deg, rgba(255,125,74,1) 0%, rgba(255,199,114,1) 100%); */
    color: #fff;
    height: 25px;
    font-weight: bold;
}
.tooltip_table tr td:first-child {
    color: #656D74;
}
.tooltip_table tr:nth-child(odd) td {
    background-color: #ffeee6a4;
}
.tooltip_table tr:nth-child(even) td {
    background-color: inherit;
}
.tooltip_table_string {
    /* table-layout: fixed; */
    width: 350px;
    text-align: center;
    position: relative;
    z-index: 1;
}
.tooltip_table_string tr:nth-child(2) th:nth-child(odd) {
    color: #656D74;
}
.tooltip_table_string .name{
    color: #fff;
    height: 25px;
    font-weight: bold;
}
.tooltip_table_string tr:nth-child(odd) td {
    background-color: #ffeee6a4;
}
.tooltip_table_string tr:nth-child(even) td {
    background-color: inherit;
}
.tooltip_table_string tr td:nth-child(odd){
    color: #656D74;
}
</style>
