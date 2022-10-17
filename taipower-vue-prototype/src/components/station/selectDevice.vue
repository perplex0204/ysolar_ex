<template>
    <div id="selectDevice" class="selc_options_container" style="max-height: 55vh;">
        <div class="selc_options_wrap first_wrap">
            <div
                v-for="(deviceType, idx) in deviceList"
                class="selc_option"
                :class="{ active: deviceType.isActive }"
                @click.stop.prevent="selectDeviceType(deviceType, $event)"
                :key="idx"
            >
                {{ $t(`${deviceType.name}`) }}<i class="el-icon-arrow-right"></i>
            </div>
        </div>
        <div class="selc_options_wrap second_wrap" ref="secondWrap">
            <div
                v-for="(device, idx) in deviceSecondCol"
                class="selc_option"
                :class="{ active: device.isActive }"
                @click.stop.prevent="
                    selectedDeviceType.name === '變流器'
                        ? showInverterPage(device, $event)
                        : showDevicePage(device, $event)
                "
                :key="idx"
            >
                <i class="el-icon-check m-0" v-show="device.isActive"></i>
                <span
                    class="equip_state"
                    v-bind:style="{'background': statusBall[device.state].color}"
                ></span>
                {{ device.name }}
                <i
                    class="el-icon-arrow-right"
                    @click.stop.prevent="selectDeviceChildren(device, $event)"
                    v-show="selectedDeviceType.name === '變流器'"
                ></i>
            </div>
        </div>
        <div class="selc_options_wrap third_wrap" ref="thirdWrap">
            <div
                v-for="(device, idx) in deviceThirdCol"
                class="selc_option"
                :class="{ active: device.isActive }"
                @click.stop.prevent="showDevicePage(device, $event)"
                :key="idx"
            >
                <i class="el-icon-check m-0" v-show="device.isActive"></i>
                <span
                    class="equip_state"
                    v-bind:style="{'background': statusBall[device.state].color}"
                ></span>
                {{ device.name }}
            </div>
        </div>
    </div>
</template>
<style>
</style>

<script>
export default {
    name: "selectDevice",
    props: {
        parentBtnName: {
            type: String,
            required: true,
        },
        equipSelectData: {type: Object, required: true},
        statusBall: {type: Array},
        jumpEquipId: {},
    },
    data() {
        return {
            deviceSecondCol: [],
            deviceThirdCol: [],
            selectedDeviceType: "",
            selectedParentDevice: [],
            selectedDevice: [],
            deviceList: [
                /* {
                    name: "變流器",
                    ID: "變流器",
                    isActive: false,
                    children: [
                        {
                            name: "Inverter 1",
                            ID: "Inverter 1",
                            isActive: false,
                            children: [
                                {
                                    name: "sm1-1",
                                    ID: "sm1-1",
                                    isActive: false,
                                },
                                {
                                    name: "sm1-2",
                                    ID: "sm1-2",
                                    isActive: false,
                                },
                            ],
                        },
                        {
                            name: "Inverter 2",
                            ID: "Inverter 2",
                            isActive: false,
                            children: [
                                {
                                    name: "sm2-1",
                                    ID: "sm2-1",
                                    isActive: false,
                                },
                                {
                                    name: "sm2-2",
                                    ID: "sm2-2",
                                    isActive: false,
                                },
                            ],
                        },
                        {
                            name: "Inverter 3",
                            ID: "Inverter 3",
                            isActive: false,
                            children: [
                                {
                                    name: "sm3-1",
                                    ID: "sm3-1",
                                    isActive: false,
                                },
                                {
                                    name: "sm3-2",
                                    ID: "sm3-2",
                                    isActive: false,
                                },
                            ],
                        },
                        {
                            name: "Inverter 4",
                            ID: "Inverter 4",
                            isActive: false,
                            children: [
                                {
                                    name: "sm4-1",
                                    ID: "sm4-1",
                                    isActive: false,
                                },
                                {
                                    name: "sm4-2",
                                    ID: "sm4-2",
                                    isActive: false,
                                },
                            ],
                        },
                    ],
                },
                {
                    name: "環境感測器",
                    ID: "環境感測器",
                    isActive: false,
                    children: [
                        {
                            name: "日照計",
                            ID: "日照計",
                            isActive: false,
                        },
                        {
                            name: "風速計",
                            ID: "風速計",
                            isActive: false,
                        },
                        {
                            name: "大氣溫度",
                            ID: "大氣溫度",
                            isActive: false,
                        },
                        {
                            name: "列組溫度",
                            ID: "列組溫度",
                            isActive: false,
                        },
                    ],
                },
                {
                    name: "智慧電表",
                    ID: "智慧電表",
                    isActive: false,
                    children: [
                        {
                            name: "SMP",
                            ID: "SMP",
                            isActive: false,
                        },
                        {
                            name: "VCB1",
                            ID: "VCB1",
                            isActive: false,
                        },
                        {
                            name: "VCB2",
                            ID: "VCB2",
                            isActive: false,
                        },
                        {
                            name: "VCB3",
                            ID: "VCB3",
                            isActive: false,
                        },
                    ],
                }, */
            ],
        };
    },
    methods: {
        selectDeviceType(typeVal, e) {
            // 將選定設備類型
            this.selectedDeviceType = typeVal;
            // 將選定的設備類型的子物件帶入第二列
            this.deviceSecondCol = typeVal.children;

            // 確認設備清單中第一層物件，名字符合就加上active狀態
            this.deviceList.forEach((item) => {
                if (item.name === typeVal.name) {
                    this.selectedDeviceType.isActive = true;
                } else {
                    item.isActive = false;
                }
            });

            // 將第二列與第三列中的isActive值全數改為false
            this.resetIsActive();
            this.$refs.secondWrap.style.display = "block";
            this.$refs.thirdWrap.style.display = "none";
        },
        selectDeviceChildren(deviceVal, e) {
            this.selectedParentDevice = deviceVal;
            this.deviceThirdCol = deviceVal.children;
            this.$refs.thirdWrap.style.display = "block";
            this.deviceSecondCol.forEach((item) => {
                if (item.name === deviceVal.name) {
                    item.isActive = true;
                } else {
                    item.isActive = false;
                }
            });
            this.deviceThirdCol.forEach((item) => {
                item.isActive = false;
            });
        },
        showDevicePage(selectedVal, e) {
            this.selectedDevice = selectedVal;

            if (this.selectedDeviceType.name === "變流器") {
                this.deviceThirdCol.forEach((item) => {
                    if (item.name === this.selectedDevice.name) {
                        this.selectedDevice.isActive = true;
                    } else {
                        item.isActive = false;
                    }
                });
                // console 選定設備
                /* console.log(
                    "open page",
                    this.selectedDeviceType.name,
                    ">",
                    this.selectedParentDevice.name,
                    ">",
                    this.selectedDevice.name
                ); */
            } else {
                //switch options status
                this.deviceSecondCol.forEach((item) => {
                    if (item.name === this.selectedDevice.name) {
                        this.selectedDevice.isActive = true;
                    } else {
                        item.isActive = false;
                    }
                });
                // console 選定設備
                /* console.log(
                    "open page：",
                    this.selectedDeviceType.name,
                    ">",
                    this.selectedDevice.name
                ); */
            }
            // 呼叫父元件，使父元件調用方法轉換到新頁面
            this.$emit("update-parent-btn-name", this.selectedDevice);
        },
        showInverterPage(deviceVal, e) {
            //console.log("open Inverter Page");
            this.deviceSecondCol.forEach((item) => {
                if (item.name === deviceVal.name) {
                    item.isActive = true;
                } else {
                    item.isActive = false;
                }
            });
            this.deviceThirdCol.forEach((item) => {
                item.isActive = false;
            });
            this.$emit("update-parent-btn-name", deviceVal);
        },
        resetIsActive() {
            this.deviceThirdCol.forEach((item) => {
                item.isActive = false;
            });
            this.deviceSecondCol.forEach((item) => {
                item.isActive = false;
            });
            this.deviceThirdCol = [];
        },
        trans_data(){
            this.deviceList = []
            if(this.equipSelectData.inv.length !== 0){
                let inv_data = this.equipSelectData.inv
                let inv_total_list = []
                for(var i in inv_data){
                    let string_list = []
                    for(var ii in inv_data[i].string){
                        string_list.push({
                            name: inv_data[i].string[ii].name,
                            ID: inv_data[i].string[ii].ID,
                            state: inv_data[i].string[ii].state,
                            isActive: false,
                            collection: inv_data[i].string[ii].collection,
                            type: "string"
                        })
                    }
                    inv_total_list.push({
                        name: inv_data[i].name,
                        ID: inv_data[i].ID,
                        children: string_list,
                        state: inv_data[i].state,
                        isActive: false,
                        model: inv_data[i].model,
                        type: "inv",
                        collection: inv_data[i].collection,
                    })
                } 
                this.deviceList.push({
                    name: '變流器',
                    ID: '變流器',
                    children: inv_total_list,
                    isActive: false,
                })
            }
            if(this.equipSelectData.sensor.length !== 0){
                let sensor_data = this.equipSelectData.sensor
                let sensor_total_list = []
                for(var i in sensor_data){
                    sensor_total_list.push({
                        name: sensor_data[i].name,
                        ID: sensor_data[i].ID,
                        isActive: false,
                        state: sensor_data[i].state,
                        collection: sensor_data[i].collection,
                        type: "sensor",
                    })
                }
                this.deviceList.push({
                    name: '環境感測器',
                    ID: '環境感測器',
                    children: sensor_total_list,
                    isActive: false,
                })
            }
            if(this.equipSelectData.meter.length !== 0){
                let meter_data = this.equipSelectData.meter
                let meter_total_list = []
                for(var i in meter_data){
                    meter_total_list.push({
                        name: meter_data[i].name,
                        ID: meter_data[i].ID,
                        isActive: false,
                        state: meter_data[i].state,
                        type: "meter",
                        collection: meter_data[i].collection,
                    })
                }
                this.deviceList.push({
                    name: '智慧電錶',
                    ID: '智慧電錶',
                    children: meter_total_list,
                    isActive: false,
                })
            }
            if(this.equipSelectData.io.length !== 0){
                let io_data = this.equipSelectData.io
                let io_total_list = []
                for(var i in io_data){
                    io_total_list.push({
                        name: io_data[i].name,
                        ID: io_data[i].ID,
                        isActive: false,
                        state: io_data[i].state,
                        type: "io",
                        collection: io_data[i].collection,
                    })
                }
                this.deviceList.push({
                    name: '開關',
                    ID: '開關',
                    children: io_total_list,
                    isActive: false,
                })
            }
            //跳轉至指定儀器
            this.deviceList.forEach(equip_type => {
                equip_type.children.forEach(equip => {
                    if(this.jumpEquipId !== null && this.jumpEquipId == equip.ID){
                        // 呼叫父元件，使父元件調用方法轉換到新頁面
                        this.$emit("update-parent-btn-name", equip)
                    }
                    if(equip.collection == 'inverter'){
                        equip.children.forEach(sm => {
                            if(this.jumpEquipId !== null && this.jumpEquipId == sm.ID){
                                // 呼叫父元件，使父元件調用方法轉換到新頁面
                                this.$emit("update-parent-btn-name", sm)
                            }
                        })
                    }
                })
            })
        }
    },
    watch: {
        equipSelectData(){
            this.trans_data()
        },
        jumpEquipId(){
            this.trans_data()
        }
    },
    mounted(){
        //console.log(this.equipSelectData)
        this.trans_data()
    }
};
</script>
<style>
.equip_state{
    width: 0.6rem;
    height: 0.6rem;
    border-radius: 50%;
    margin-right: .5rem;
}
</style>