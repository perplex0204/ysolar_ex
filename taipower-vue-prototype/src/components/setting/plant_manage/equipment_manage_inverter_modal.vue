<template>
    <div class="modal" tabindex="-1" ref="inverter_create_modal">
        <div class="modal-dialog modal-dialog-centered">
            <div class="modal-content">
                <div class="modal-header">
                    <h5 class="modal-title"> Inverter create </h5>
                    <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
                </div>
                <div class="modal-body">
                    <!-- 設備位置 -->
                    <div class="d-flex flex-wrap align-items-center">
                        <label data-toggle="tooltip" title='設定Inverter所在之位置' for="place_select" class="col-2 col-lg-3 mt-2">設備位置：</label>
                        <auto-complete data-toggle="tooltip" title='設定Inverter所在之位置' id="place_select" @station-select="station_select" class="col-12 col-lg-auto me-lg-2 mt-2 mb-lg-0"></auto-complete>
                    </div>
                    <!-- 設備名稱 -->
                    <div class="d-flex flex-wrap align-items-center">
                        <label data-toggle="tooltip" title='Inverter之名稱應為"Inverter+編號"' for="equipment_name" class="col-2 col-lg-3 mt-2">設備名稱：</label>
                        <el-input data-toggle="tooltip" title='Inverter之名稱應為"Inverter+編號"'  id="equipment_name" class="col-12 col-lg-auto me-lg-2 mt-2 mb-lg-0" v-model="equipment_name" />
                    </div>
                    <!-- Device_model，須從mongodb取得可以選擇的設備 -->
                    <div class="d-flex flex-wrap align-items-center">
                        <label data-toggle="tooltip" title='設定Inverter之型號' for="Device_model" class="col-2 col-lg-3 mt-2">Device Model：</label>
                    </div>
                    <!-- Module_model，須從mongodb取得可以選擇的設備 -->
                    <div class="d-flex flex-wrap align-items-center">
                        <label data-toggle="tooltip" title='設定太陽能模組之型號' for="Module_model" class="col-2 col-lg-3 mt-2">Module Model：</label>
                    </div>
                    <!-- COM port，需和TCP系列的選項做防呆 -->
                    <div class="d-flex flex-wrap align-items-center">
                        <label data-toggle="tooltip" title='設定設備COM port' for="COM_port" class="col-2 col-lg-3 mt-2">COM port：</label>
                        <el-select data-toggle="tooltip" title='設定設備COM port' :disabled="this.tcp_port!=''" v-model="com_port" class="col-12 col-lg-auto me-lg-2 mt-2 mb-lg-0">
                                <el-option value="" :label="請選擇"/>
                                <el-option value="COM1"/>
                                <el-option value="COM2"/>
                                <el-option value="COM3"/>
                                <el-option value="COM4"/>
                                <el-option value="COM5"/>
                                <el-option value="COM6"/>
                                <el-option value="COM7"/>
                                <el-option value="COM8"/>
                                <el-option value="COM9"/>
                                <el-option value="COM10"/>
                        </el-select>
                    </div>
                    <!-- TCP port，需和COM系列的選項做防呆 -->
                    <div class="d-flex flex-wrap align-items-center">
                        <label data-toggle="tooltip" title='設定設備TCP port' for="TCP_port" class="col-2 col-lg-3 mt-2">TCP port：</label>
                        <el-input :disabled="this.com_port!=''" data-toggle="tooltip" title='設定設備TCP port'  id="TCP_port" class="col-12 col-lg-auto me-lg-2 mt-2 mb-lg-0" v-model="tcp_port" />
                    </div>
                    <!-- TCP IP，需和COM系列的選項做防呆 -->
                    <div class="d-flex flex-wrap align-items-center">
                        <label data-toggle="tooltip" title='設定設備TCP IP' for="TCP_IP" class="col-2 col-lg-3 mt-2">TCP IP：</label>
                        <el-input :disabled="this.com_port!=''" data-toggle="tooltip" title='設定設備TCP IP'  id="TCP_IP" class="col-12 col-lg-auto me-lg-2 mt-2 mb-lg-0" v-model="tcp_ip" />
                    </div>
                    <!-- Device id -->
                    <div class="d-flex flex-wrap align-items-center">
                        <label data-toggle="tooltip" title='設定設備Device ID' for="Device_id" class="col-2 col-lg-3 mt-2">Device ID：</label>
                        <el-input data-toggle="tooltip" type="number" min="1" max="100" title='設定設備Device ID'  id="Device_id" class="col-12 col-lg-auto me-lg-2 mt-2 mb-lg-0" v-model="device_id" />
                    </div>
                    <!-- Baud rate -->
                    <div class="d-flex flex-wrap align-items-center">
                        <label data-toggle="tooltip" title='設定設備Baud rate' for="Baud_rate" class="col-2 col-lg-3 mt-2">Baud rate：</label>
                        <el-select v-model="baud_rate" class="col-12 col-lg-auto me-lg-2 mt-2 mb-lg-0">
                                <el-option value="9600" :label="9600"/>
                                <el-option value="19200" :label="19200"/>
                                <el-option value="38400" :label="38400"/>
                                <el-option value="115200" :label="115200"/>
                        </el-select>
                    </div>
                    <!-- Periods -->
                    <div class="d-flex flex-wrap align-items-center">
                        <label data-toggle="tooltip" title='設定設備之收費期間' for="periods" class="col-2 col-lg-3 mt-2">Periods：</label>
                    </div>
                    <!-- MPPT data -->
                    <div class="d-flex flex-wrap align-items-center">
                        <label data-toggle="tooltip" title='設定設備串列電流表資料' for="mppt_data" class="col-2 col-lg-3 mt-2">MPPT data：</label>
                    </div>
                </div>
                <div class="modal-footer">
                    <button type="button" class="btn btn-success" @click="set_clicked"> 確定 </button>
                    <button type="button" class="btn btn-success" @click="check_clicked"> 檢查數值 </button>
                </div>
            </div>
        </div>
    </div>
</template>

<script>
import { Modal } from "bootstrap";
import autoComplete from '@/components/autocomplete/all_type.vue'

export default {
    name: "inverterModal",
    components: {
        autoComplete
    },
    props: {
        'modalStatus': {
            type: Boolean,
        }
    },
    data() {
        return {
            screenWidth: document.body.clientWidth,
            max_usage: '',
            inverter_modal_status: this.modalStatus,
            search:{},
            station:'',
            equipment_name:'',
            baud_rate:'',
            com_port:'',
            tcp_port:'',
            tcp_ip:'',
            device_id:'',
        }
    },
    mounted() {
        this.inverter_create_modal = new Modal(
            this.$refs.inverter_create_modal
        );
        let that = this;
        window.addEventListener("resize", this.plot_resize);
        window.addEventListener("resize", function () {
            return (() => {
                that.screenWidth = this.document.body.clientWidth;
            })();
        });
        if (this.screenWidth >= 576) {
            this.csvsize = "large";
            console.log("resize large");
        } else {
            this.csvsize = "small";
            console.log("resize small");
        }
    },
    unmounted() {
        window.removeEventListener("resize", this.plot_resize);
    },
    methods: {
        set_clicked() {
            this.inverter_create_modal.hide();
            console.log(this.station)
        },
        // 數值檢查
        check_clicked() {
            console.log('==========================')
            console.log('equipment_place : ', this.station)
            console.log('equipment_name : ', this.equipment_name)
            console.log('COM port : ', this.com_port)
            console.log('tcp_port : ', this.tcp_port)
            console.log('tcp_ip : ', this.tcp_ip)
            console.log('baud_rate : ', this.baud_rate)
            console.log('device_id : ', this.device_id)
            console.log('==========================')
        },
        search_select(item) {
            this.search = item
        },
        station_select(item) {
            this.station = item
            this.refresh()
        },
    },
    watch: {
        modalStatus: function () {
            if (this.modalStatus == true) {
                this.inverter_create_modal.show();
            }
            this.inverter_modal_status = false
            this.$emit('update', this.inverter_modal_status)
        }
    }
}
</script>