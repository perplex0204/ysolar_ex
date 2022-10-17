<template>
    <div class="row g-0">
        <div class="col-lg-3 col-12" style="display: flex;flex-direction: column;">
            <div>
                <button class="point_btn" @click="equip_point_type = 'p'" :class="{active: equip_point_type == 'p'}" >{{$t("plot.功率")}}：{{equip_point_info["p"]}}<span class="ms-2">kW</span></button>
                <button class="point_btn" @click="equip_point_type = 'v'" :class="{active: equip_point_type == 'v'}" >{{$t("plot.電壓")}}：{{equip_point_info["v"]}}<span class="ms-2">V</span></button>
                <button class="point_btn" @click="equip_point_type = 'i'" :class="{active: equip_point_type == 'i'}" >{{$t("plot.電流")}}：{{equip_point_info["i"]}}<span class="ms-2">A</span></button>
                <button class="point_btn" @click="equip_point_type = 'f'" :class="{active: equip_point_type == 'f'}" >{{$t("plot.頻率")}}：{{equip_point_info["f"]}}<span class="ms-2">Hz</span></button>
                

                <button class="point_btn" @click="equip_point_type = 'kwh_today'" :class="{active: equip_point_type == 'kwh_today'}" >{{$t("本日發電量")}}：{{equip_point_info["kwh_today"]}}<span class="ms-2">kWh</span></button>
                <button class="point_btn" @click="equip_point_type = 'kwh_month'" :class="{active: equip_point_type == 'kwh_month'}" >{{$t("本月發電量")}}：{{equip_point_info["kwh_month"]}}<span class="ms-2">kWh</span></button>
                <button class="point_btn" @click="equip_point_type = 'kwh_year'" :class="{active: equip_point_type == 'kwh_year'}" >{{$t("本年發電量")}}：{{equip_point_info["kwh_year"]}}<span class="ms-2">kWh</span></button>
                
                
                
            </div>
            <div class="point_btn_remain"></div>
        </div>
        <div class="col-lg-9 col-12" style="display: flex;flex-direction: column;">
            <data-history-data
                :key="equip_point_type.includes('kwh')? 'kwh': equip_point_type"
                :data-id="meter_ID"
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
    name: "Pvmeter", 
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
            meter_model: this.equipSelect.model,
            meter_ID: this.equipSelect.ID,
            equip_point_type: "p",
            equip_point_info: {}
        }
    },
    methods:{
        pv_meter_data(){
            const that = this
            this.axios.post('/pv_meter_data', {
                ID_list: [this.meter_ID]
            })
            .then(function (data) {
                //console.log(data.data.data)
                that.equip_point_info = data.data.data.meter_data[0]
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
        this.syncdata = setInterval(this.pv_meter_data, 5000)
        this.pv_meter_data()
    },
    unmounted(){
        clearInterval(this.syncdata)
    }
}
</script>
