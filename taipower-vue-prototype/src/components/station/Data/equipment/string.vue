<template>
    <div class="row g-0">
        <div class="col-lg-3 col-12" style="display: flex;flex-direction: column;">
            <div>
                <button class="point_btn" @click="equip_point_type = 'sa'" :class="{active: equip_point_type == 'sa'}" >{{$t('全部')}}</button>
                <button class="point_btn" v-for="i, count in equip_point_info.sa" :key="count" @click="equip_point_type = `sa${parseInt(count)+1}`" :class="{active: equip_point_type ==  `sa${parseInt(count)+1}`}" >{{ `sa${parseInt(count)+1}`}}：{{i}}<span class="ms-2">A</span></button>
            </div>    
            <div class="point_btn_remain"></div>
        </div>
        <div class="col-lg-9 col-12" style="display: flex;flex-direction: column;">
            <data-history-data
                :key="equip_point_type+serial_num"
                :data-id="string_ID"
                :data-type="equip_point_type"
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
    name: "string", 
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
            string_model: this.equipSelect.model,
            string_ID: this.equipSelect.ID,
            serial_num: 0,
            equip_point_type: "sa",
            equip_point_info: {}
        }
    },
    methods:{
        pv_string_data(){
            const that = this
            this.axios.post('/pv_string_data', {
                string_ID: this.string_ID
            })
            .then(function (data) {
                console.log(data.data.data)
                that.serial_num = data.data.data.equip_data.serial_num
                that.equip_point_info = data.data.data.string_data
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
        this.syncdata = setInterval(this.pv_string_data, 5000)
        this.pv_string_data()
    },
    unmounted(){
        clearInterval(this.syncdata)
    }
}
</script>
