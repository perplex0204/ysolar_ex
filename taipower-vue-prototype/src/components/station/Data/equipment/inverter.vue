<template>
    <div class="row g-0">
        <div class="col-lg-3 col-12 d-flex flex-column">
            <div v-if="table_data.length == 0">
                <div>
                    <button class="point_btn" @click="equip_point_type = 'Device_model'" :class="{active: equip_point_type == 'Device_model'}">{{$t("型號")}} ：{{equip_point_info["Device_model"]}}</button>
                    <button class="point_btn" @click="equip_point_type = 'serial_number'" :class="{active: equip_point_type == 'serial_number'}">{{$t("序號")}} ：{{equip_point_info["serial_number"]}}</button>
                    <button class="point_btn" @click="equip_point_type = 'kwh_today'" :class="{active: equip_point_type == 'kwh_today'}" >{{$t("本日發電量")}}：{{equip_point_info["kwh_today"]}}<span class="ms-2">kWh</span></button>
                    <button class="point_btn" @click="equip_point_type = 'kwh'" :class="{active: equip_point_type == 'kwh'}" >{{$t("table.累計發電量")}}：{{equip_point_info["kwh"]}}<span class="ms-2">kWh</span></button>
                    <button class="point_btn" @click="equip_point_type = 'p_cell_total'" :class="{active: equip_point_type == 'p_cell_total'}" >{{$t("plot.直流功率")}}：{{equip_point_info["p_cell_total"]}}<span class="ms-2">kW</span></button>
                    <button class="point_btn" @click="equip_point_type = 'p_bus_total'" :class="{active: equip_point_type == 'p_bus_total'}" >{{$t("plot.交流功率")}}：{{equip_point_info["p_bus_total"]}}<span class="ms-2">kW</span></button>
                    <button class="point_btn" @click="equip_point_type = 'PR'" :class="{active: equip_point_type == 'PR'}" >PR：{{equip_point_info["PR"]}}<span class="ms-2"></span></button>
                    <button class="point_btn" @click="equip_point_type = 'RA'" :class="{active: equip_point_type == 'RA'}" >RA：{{equip_point_info["RA"]}}<span class="ms-2"></span></button>
                    <button class="point_btn" @click="equip_point_type = 'temp_sink'" :class="{active: equip_point_type == 'temp_sink'}" >{{$t('變流器')}} {{$t("plot.溫度")}}：{{equip_point_info["temp_sink"]}}<span class="ms-2">°C</span></button>
                    <button class="point_btn" @click="equip_point_type = 'temp_inner'" :class="{active: equip_point_type == 'temp_inner'}" >Ambient {{$t("plot.溫度")}}：{{equip_point_info["temp_inner"]}}<span class="ms-2">°C</span></button>
                    <button class="point_btn" @click="equip_point_type = 'temp_Boost_1'" :class="{active: equip_point_type == 'temp_Boost_1'}" >Boost {{$t("plot.溫度")}}：{{equip_point_info["temp_Boost_1"]}}<span class="ms-2">°C</span></button>
                    
                    <div class="point_btn divide">{{$t("table.交流輸出側")}} L1</div>
                    <button class="point_btn" @click="equip_point_type = 'v_bus_1'" :class="{active: equip_point_type == 'v_bus_1'}" >{{$t("plot.交流電壓")}} 1：{{equip_point_info["v_bus_1"]}}<span class="ms-2">V</span></button>
                    <button class="point_btn" @click="equip_point_type = 'i_bus_1'" :class="{active: equip_point_type == 'i_bus_1'}" >{{$t("plot.交流電流")}} 1：{{equip_point_info["i_bus_1"]}}<span class="ms-2">A</span></button>
                    <button class="point_btn" @click="equip_point_type = 'p_bus_1'" :class="{active: equip_point_type == 'p_bus_1'}" >{{$t("plot.交流功率")}} 1：{{equip_point_info["p_bus_1"]}}<span class="ms-2">kW</span></button>
                    <button class="point_btn" @click="equip_point_type = 'f_bus_1'" :class="{active: equip_point_type == 'f_bus_1'}" >{{$t("plot.交流頻率")}} 1：{{equip_point_info["f_bus_1"]}}<span class="ms-2">Hz</span></button>
                    
                    <div class="point_btn divide">{{$t("table.交流輸出側")}} L2</div>
                    <button class="point_btn" @click="equip_point_type = 'v_bus_2'" :class="{active: equip_point_type == 'v_bus_2'}" >{{$t("plot.交流電壓")}} 2：{{equip_point_info["v_bus_2"]}}<span class="ms-2">V</span></button>
                    <button class="point_btn" @click="equip_point_type = 'i_bus_2'" :class="{active: equip_point_type == 'i_bus_2'}" >{{$t("plot.交流電流")}} 2：{{equip_point_info["i_bus_2"]}}<span class="ms-2">A</span></button>
                    <button class="point_btn" @click="equip_point_type = 'p_bus_2'" :class="{active: equip_point_type == 'p_bus_2'}" >{{$t("plot.交流功率")}} 2：{{equip_point_info["p_bus_2"]}}<span class="ms-2">kW</span></button>
                    <button class="point_btn" @click="equip_point_type = 'f_bus_2'" :class="{active: equip_point_type == 'f_bus_2'}" >{{$t("plot.交流頻率")}} 2：{{equip_point_info["f_bus_2"]}}<span class="ms-2">Hz</span></button>
                
                    <div class="point_btn divide">{{$t("table.交流輸出側")}} L3</div> 
                    <button class="point_btn" @click="equip_point_type = 'v_bus_3'" :class="{active: equip_point_type == 'v_bus_3'}" >{{$t("plot.交流電壓")}} 3：{{equip_point_info["v_bus_3"]}}<span class="ms-2">V</span></button>
                    <button class="point_btn" @click="equip_point_type = 'i_bus_3'" :class="{active: equip_point_type == 'i_bus_3'}" >{{$t("plot.交流電流")}} 3：{{equip_point_info["i_bus_3"]}}<span class="ms-2">A</span></button>
                    <button class="point_btn" @click="equip_point_type = 'p_bus_3'" :class="{active: equip_point_type == 'p_bus_3'}" >{{$t("plot.交流功率")}} 3：{{equip_point_info["p_bus_3"]}}<span class="ms-2">kW</span></button>
                    <button class="point_btn" @click="equip_point_type = 'f_bus_3'" :class="{active: equip_point_type == 'f_bus_3'}" >{{$t("plot.交流頻率")}} 3：{{equip_point_info["f_bus_3"]}}<span class="ms-2">Hz</span></button>

                </div>
            </div>    
            <div v-else>
                <div v-for="group, i in table_data" :key="i">
                    <div class="point_btn divide" v-if="group.name[$store.state.language] != ''">
                        {{group.name[$store.state.language]}}
                    </div>
                    <button v-for="child, i in group.child"
                    :key="i"
                    class="point_btn" 
                    @click="equip_point_type = child.datatype" 
                    :class="{active: equip_point_type == child.datatype}" >
                        {{child.name[$store.state.language]}}：
                        {{equip_point_info[child.datatype]}}
                        <span class="ms-2">
                            {{child.unit[$store.state.language]}}
                        </span>
                    </button>
                </div>
            </div>
            <div class="point_btn_remain"></div>
        </div>
        <div class="col-lg-9 col-12" style="display: flex;flex-direction: column;">
            <data-history-data
                :key="equip_point_type.includes('kwh')? 'kwh': equip_point_type"
                :data-id="inverter_ID"
                :data-type="equip_point_type.includes('kwh')? 'kwh': equip_point_type"
                :data-collection="equipSelect.collection"
                :data-name="equipSelect.name"
                :parent-name="equipSelect.name"
            ></data-history-data>
        </div>
    </div>
    
    
</template>

<script>
import dataHistoryData from "./dataHistoryData.vue"
export default {
    name: "inverter", 
    props: {
        equipSelect: {
            type: Object,
            required: true
        }
    },
    components:{
        dataHistoryData
    },
    data(){
        return{
            inverter_model: this.equipSelect.model,
            inverter_ID: this.equipSelect.ID,
            equip_point_type: "kwh_today",
            equip_point_info: {},
            table_data: []
        }
    },
    methods:{
        pv_inv_data(){
            const that = this
            this.axios.post('/pv_inv_data', {
                inv_ID: this.inverter_ID
            })
            .then(function (data) {
                console.log(data.data.data.inv_data)
                that.equip_point_info = data.data.data.inv_data
            })
        },
        get_inv_table_data(){
            this.axios.post('/get_inv_table_data', {
                inv_ID: this.inverter_ID
            }).then(data=>{
                this.table_data = data.data.data.table_data
                this.syncdata = setInterval(this.pv_inv_data, 5000)
                this.pv_inv_data()
            })
        }
    },
    beforeMount(){
        // 預設跳轉
        if('datatype' in this.$store.state.stationData_jump){
            this.equip_point_type = this.$store.state.stationData_jump.datatype
            delete this.$store.state.stationData_jump.datatype
        }
    },
    mounted(){
        this.get_inv_table_data()
        console.log(this.equipSelect)
    },
    unmounted(){
        clearInterval(this.syncdata)
    }
}
</script>
