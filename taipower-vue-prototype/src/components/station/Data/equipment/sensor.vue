<template>
    <div class="row g-0">
        <div class="col-lg-3 col-12" style="display: flex;flex-direction: column;">
            <div>
                <button class="point_btn" v-for="i, count in equipSelectData.sensor" :key="i.ID" @click="switch_sensor(i.ID, i.name)" 
                :class="{active: equip_point_type ==  i.ID}" >{{i.name}}：{{equip_point_info && equip_point_info.length == 0 ?'---':equip_point_info[count].value}}<span class="ms-2">{{i.unit}}</span></button>
            </div>    
            <div class="point_btn_remain"></div>
        </div>
        <div class="col-lg-9 col-12" style="display: flex;flex-direction: column;">
            <data-history-data
                :key="equip_point_type"
                :data-id="sensor_ID"
                :data-type="'value'"
                :data-collection="'sensor'"
                :data-name="sensor_name"
                :parent-name="sensor_name"
            ></data-history-data>
        </div>
    </div>
    
    
</template>

<script>
import dataHistoryData from "./dataHistoryData.vue"
export default {
    name: "sensor", 
    props: {
        equipSelect: {
            type: Object,
            required: true
        },
        equipSelectData: {
            type: Object,
            required: true
        }
    },
    components:{
        dataHistoryData
    },
    data(){
        return{
            sensor_model: this.equipSelect.model,
            sensor_ID: this.equipSelect.ID,
            sensor_name: this.equipSelect.name,
            ID_list: [],
            equip_point_type: this.equipSelect.ID,
            equip_point_info: []
        }
    },
    methods:{
        pv_sensor_data(){
            const that = this
            this.axios.post('/pv_sensor_data', {
                ID_list: this.ID_list
            })
            .then(function (data) {
                //console.log(data.data.data)
                that.equip_point_info = data.data.data
            })
        },
        switch_sensor(ID, name){
            this.sensor_ID = ID
            this.equip_point_type = ID
            this.sensor_name = name
        }
    },
    mounted(){
        let that = this
        this.equipSelectData.sensor.forEach(element => {
            this.ID_list.push(element['ID'])
        })
        this.syncdata = setInterval(this.pv_sensor_data, 5000)
        this.pv_sensor_data()
    },
    unmounted(){
        clearInterval(this.syncdata)
    }
}
</script>
