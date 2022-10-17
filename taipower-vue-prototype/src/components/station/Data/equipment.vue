<template>
    <div>
        <div class="row g-0 ms-2 mt-2 me-2 ps-lg-4 pt-3">
            <el-popover
                placement="bottom-start"
                trigger="click"
                class="select_device_popup"
                width="unset"
                popper-class="screen-limit"
            >
                <template #reference>
                    <el-button
                        size="large"
                        class="esicon_btn icon-ttl_sunboard col-12 col-lg-3 col-xl-2"
                    >
                        <span
                            class="slec_btn_alert_spot"
                            v-if="btnDeviceName != '選擇設備'"
                            :style="'background:'+ switchAlertClr"
                        ></span>
                        <label class="selc_btn_title" v-if="btnDeviceName == '選擇設備'">{{$t(btnDeviceName)}}</label>
                        <label class="selc_btn_title" v-else>{{btnDeviceName}}</label>
                    </el-button>
                </template>

                <select-device
                    :parent-btn-name="btnDeviceName"
                    :equip-select-data="equipSelectData"
                    :status-ball="statusBall"
                    :jump-equip-id="jumpEquipId"
                    @update-parent-btn-name="updateBtnName"
                />
                <div v-if="empty_equipSelectData">
                    {{$t('無資料')}}
                </div>
            </el-popover>
            <el-popover
                v-if="$store.state.user_data.is_superuser && btnDeviceID != null"
                placement="top-start"
                :width="200"
                trigger="hover"
                :content="`ID: ${btnDeviceID}, Collection: ${btnDeviceCollection}`"
            >
                <template #reference>
                    <button class="btn d-inline-block ms-lg-auto col-auto"><i class="fa-solid fa-circle-info"></i></button>
                </template>
            </el-popover>
        </div>
        <!-- inv total table -->
        <inverter-total-table v-if="inv_list.length > 0 && selectData.type == 'inv_total'" :inverterList="inv_list"
            @update-parent-btn-name="updateBtnName">
        </inverter-total-table>
        <div class="row g-0 mt-4 me-lg-2">
            <inverter :equip-select="selectData" v-if="selectData.type == 'inv'" :key="btnDeviceID"></inverter>
            <string :equip-select="selectData" v-else-if="selectData.type == 'string'" :key="btnDeviceID"></string>
            <sensor :equip-select="selectData" :equip-select-data="equipSelectData" v-else-if="selectData.type == 'sensor'" :key="btnDeviceID"></sensor>
            <pvmeter :equip-select="selectData" v-else-if="['meter', 'pv_meter', 'pv_plant', 'pv_lgroup', 'pv_group'].includes(selectData.type)" :key="btnDeviceID"></pvmeter>
        </div>
    </div>
</template>
<script>
import selectDevice from '../selectDevice.vue'
import inverter from './equipment/inverter.vue'
import string from './equipment/string.vue'
import sensor from './equipment/sensor.vue'
import pvmeter from './equipment/meter.vue'
import inverterTotalTable from './equipment/inverter_total.vue'

export default {
    components: { 
        selectDevice,
        inverter,
        string,
        sensor,
        pvmeter,
        inverterTotalTable
    },
    name: "equipment",
    props: {
        stationData: {
            type: Object,
            required: true
        },
        equipSelectData: {
            type: Object,
            required: true
        }
    },
    data(){
        return {
            alertStatus: 0,
            btnDeviceName: "選擇設備",
            btnDeviceID: null,
            btnDeviceCollection: null,
            btnDeviceType: null,
            jumpEquipId: {},
            statusBall: [
                { name: "正常", color: "#13AD74" },
                { name: "一級警報", color: "#FFC557" },
                { name: "二級警報", color: "#FF4671" },
                { name: "斷線", color: "#9CA3AC" },
            ],
            selectData: {
                type: "inv_total"
            },
            inv_list: []
        }
    },
    methods: {
        updateBtnName(newData) {
            console.log(newData)
            this.selectData = newData
            this.btnDeviceName = newData.name
            this.btnDeviceType = newData.type
            this.btnDeviceID = newData.ID
            this.btnDeviceCollection = newData.collection
            this.alertStatus = newData.state
        },
        resetBtnName() {
            this.btnDeviceName = "選擇設備";
        },
        equip_update(){
            // jump equip ID 
            if('equip_ID' in this.$store.state.stationData_jump){
                this.jumpEquipId = this.$store.state.stationData_jump.equip_ID
                delete this.$store.state.stationData_jump.equip_ID
            }
            // determine inv total table showing
            if('inv' in this.equipSelectData && this.equipSelectData.inv.length > 0){
                this.inv_list = this.equipSelectData.inv
            }else{
                this.inv_list = []
            }
        },
    },
    computed: {
        switchAlertClr: function () {
            /* let newStatusColor = "";
            this.equipData.statusBall.forEach((el) => {
                if (el.name === this.alertStatus) {
                    newStatusColor = el.color;
                }
            }); */
            return this.statusBall[this.alertStatus].color;
        },
        empty_equipSelectData(){
            let no_equip = true
            Object.keys(this.equipSelectData).forEach(key=>{
                if(this.equipSelectData[key].length > 0)
                    no_equip = false
                    return false
            })
            return no_equip
        }
    },
    watch: {
        equipSelectData(){
            this.equip_update()
        }
    },
    mounted(){
        this.equip_update()
    }
}
</script>
<style>
.screen-limit{
    max-width: 90vw !important;
    overflow: hidden;   
    overflow-x: scroll; 
}
</style>