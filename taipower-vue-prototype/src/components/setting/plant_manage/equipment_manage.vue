<template>
    <div class="card p-4 mt-3">
        <h5>
            <i class="fa-solid fa-screwdriver-wrench text-primary me-2"></i>設備管理 - 新增設備
        </h5>
        <div class="d-flex flex-wrap mt-2 align-items-center">
            <button class=" btn btn-primary mt-2 btn-sm col-12 col-sm-12 col-md-6 col-lg-3 col-xl-1" @click="
            plant_create" v-if="$store.state.user_data.is_superuser">Plant</button>
            <button class=" btn btn-primary mt-2 ms-lg-2 btn-sm col-12 col-sm-12 col-md-6 col-lg-3 col-xl-1" @click="
            lgroup_create" v-if="$store.state.user_data.is_superuser">Lgroup</button>
            <button class=" btn btn-primary mt-2 ms-lg-2 btn-sm col-12 col-sm-12 col-md-6 col-lg-3 col-xl-1" @click="
            group_create" v-if="$store.state.user_data.is_superuser">Group</button>
            <button class=" btn btn-primary mt-2 ms-lg-2 btn-sm col-12 col-sm-12 col-md-6 col-lg-3 col-xl-1" @click="
            inverter_create">Inverter</button>
            <button class=" btn btn-primary mt-2 ms-lg-2 btn-sm col-12 col-sm-12 col-md-6 col-lg-3 col-xl-1" @click="
            sensor_create">Sensor</button>
            <button class=" btn btn-primary mt-2 ms-lg-2 btn-sm col-12 col-sm-12 col-md-6 col-lg-3 col-xl-1" @click="
            meter_create">Meter</button>
        </div>
        <el-divider></el-divider>
        <div class="d-flex flex-wrap align-items-center">
            <auto-complete @search-select="search_select" @station-select="station_select"
                class="col-12 col-lg-3 me-lg-2 mt-2 mb-lg-0"></auto-complete>
        </div>
        <!-- 設備filter:checkbox -->
        <div class="d-flex flex-wrap mt-2 align-items-center">
            <input class="me-2" type="checkbox" id="lgroup" value="pv_lgroup" v-model="type_checked"
                v-if="$store.state.user_data.is_superuser" />
            <label class="me-2" for="lgroup" v-if="$store.state.user_data.is_superuser">lgroup</label>
            <input class="me-2" type="checkbox" id="group" value="pv_group" v-model="type_checked"
                v-if="$store.state.user_data.is_superuser" />
            <label class="me-2" for="group" v-if="$store.state.user_data.is_superuser">group</label>
            <input class="me-2" type="checkbox" id="inverter" value="inverter" v-model="type_checked" />
            <label class="me-2" for="inverter">inverter</label>
            <input class="me-2" type="checkbox" id="sensor" value="sensor" v-model="type_checked" />
            <label class="me-2" for="sensor">sensor</label>
            <input class="me-2" type="checkbox" id="string_meter" value="string_meter" v-model="type_checked" />
            <label class="me-2" for="string_meter">string meter</label>
            <input class="me-2" type="checkbox" id="meter" value="meter" v-model="type_checked" />
            <label class="me-2" for="meter">meter</label>
        </div>
        <!-- 設定header -->
        <div class="d-flex flex-wrap mt-2 align-items-center">
            <div class="col-6 col-lg-12 responsive_table ms-lg-2">
                <div style="overflow-y: scroll;">
                    <div class="w-100 row responsive_table_header  fw-bold m-0 d-none d-lg-flex flex-nowrap">
                        <div class="col-2 text-center">
                            <label class="fs-6">設備種類</label>
                        </div>
                        <div class="col-2 text-center">
                            <label class="fs-6">Lgroup</label>
                        </div>
                        <div class="col-2 text-center">
                            <label class="fs-6">group</label>
                        </div>
                        <div class="col-2 text-center">
                            <label class="fs-6">Name</label>
                        </div>
                        <div class="col-2 text-center">
                            <label class="fs-6">刪除</label>
                        </div>
                        <div class="col-2 text-center">
                            <label class="fs-6">更多資訊</label>
                        </div>
                    </div>
                    <div>
                        <!-- 設定無資料的狀況 -->
                        <div class="w-100 pt-2 pb-2 text-center" v-if="this.equipment_data.length == 0">
                            {{ $t('setting.iec61850.無資料') }}
                        </div>
                        <!-- 設定body -->
                        <div class="w-100 responsive_table_body">
                            <div class="row m-0 responsive_table_content mt-2 mt-lg-0 pt-2 pb-3 p-lg-0"
                                v-for="data in this.equipment_data" :key="data.name">
                                <div class="col-12 col-lg-2 pt-lg-4 pb-lg-4">
                                    <div class="d-flex d-lg-none">
                                        <label class="fs-6 fw-bold">設備種類:</label>
                                        <label class="fs-6">{{ data.collection }}</label>
                                    </div>
                                    <label class="fs-6 w-100 text-center d-none d-lg-block">{{ data.collection
                                    }}</label>
                                </div>
                                <div class="col-12 col-lg-2 pt-lg-4 pb-lg-4">
                                    <div class="d-flex d-lg-none">
                                        <label class="fs-6 fw-bold">Lgroup:</label>
                                        <label class="fs-6">{{ data.lgroup }}</label>
                                    </div>
                                    <label class="fs-6 w-100 text-center d-none d-lg-block">{{ data.lgroup
                                    }}</label>
                                </div>
                                <div class="col-12 col-lg-2 pt-lg-4 pb-lg-4">
                                    <div class="d-flex d-lg-none">
                                        <label class="fs-6 fw-bold">group:</label>
                                        <label class="fs-6">{{ data.group }}</label>
                                    </div>
                                    <label class="fs-6 w-100 text-center d-none d-lg-block">{{ data.group
                                    }}</label>
                                </div>
                                <div class="col-12 col-lg-2 pt-lg-4 pb-lg-4">
                                    <div class="d-flex d-lg-none">
                                        <label class="fs-6 fw-bold">Name:</label>
                                        <label class="fs-6">{{ data.name }}</label>
                                    </div>
                                    <label class="fs-6 w-100 text-center d-none d-lg-block">{{ data.name
                                    }}</label>
                                </div>
                                <div class="col-12 col-lg-2 pt-lg-4 pb-lg-4">
                                    <label class="fs-6 fw-bold d-lg-none">刪除</label>
                                    <div class="d-flex justify-content-center align-items-center w-100">
                                        <button class="btn" @click="delete_equipment(data.ID)"><i
                                                class="fa-solid fa-trash"></i></button>
                                    </div>
                                </div>
                                <div class="col-12 col-lg-2 pt-lg-4 pb-lg-4">
                                    <label class="fs-6 fw-bold d-lg-none">更多</label>
                                    <div class="d-flex justify-content-center align-items-center w-100">
                                        <button class="btn" @click="more_info(data)"><i
                                                class="fas fa-ellipsis-h"></i></button>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
        <div class="modal" tabindex="-1" ref="more_info_modal" id="more_info_nodal">
            <div class="modal-dialog modal-dialog-centered">
                <div class="modal-content">
                    <div class="modal-header">
                        <h5 class="modal-title"> 更多資訊 - {{ this.more_info_data.name }}
                        </h5>
                        <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
                    </div>
                    <div class="modal-body">
                        <ul>
                            <li v-for="(item, key) in this.more_info_data" :key="item.name">
                                {{ key }}：{{ item }}
                            </li>
                        </ul>
                    </div>
                    <div class="modal-footer">
                        <button type="button" class="btn btn-success" @click="confirm_clicked"> 確定 </button>
                    </div>
                </div>
            </div>
        </div>
        <plant-modal :modal-status="plant_modal_status" @update="plantUpdateInfo"></plant-modal>
        <lgroup-modal :modal-status="lgroup_modal_status" @update="lgroupUpdateInfo"></lgroup-modal>
        <group-modal :modal-status="group_modal_status" @update="groupUpdateInfo"></group-modal>
        <inverter-modal :modal-status="inverter_modal_status" @update="inverterUpdateInfo"></inverter-modal>
        <sensor-modal :modal-status="sensor_modal_status" @update="sensorUpdateInfo"></sensor-modal>
        <meter-modal :modal-status="meter_modal_status" @update="meterUpdateInfo"></meter-modal>
    </div>
</template>

<script>
import { Modal } from "bootstrap";
import autoComplete from '@/components/autocomplete/plant_only.vue'
import plantModal from '@/components/setting/plant_manage/equipment_manage_plant_modal.vue'
import lgroupModal from '@/components/setting/plant_manage/equipment_manage_lgroup_modal.vue'
import groupModal from '@/components/setting/plant_manage/equipment_manage_group_modal.vue'
import inverterModal from '@/components/setting/plant_manage/equipment_manage_inverter_modal.vue'
import sensorModal from '@/components/setting/plant_manage/equipment_manage_sensor_modal.vue'
import meterModal from '@/components/setting/plant_manage/equipment_manage_meter_modal.vue'

export default {
    name: "equipmentManage",
    components: {
        autoComplete,
        plantModal,
        lgroupModal,
        groupModal,
        inverterModal,
        sensorModal,
        meterModal
    },
    data() {
        return {
            screenWidth: document.body.clientWidth,
            plant_modal_status: false,
            lgroup_modal_status: false,
            group_modal_status: false,
            inverter_modal_status: false,
            sensor_modal_status: false,
            meter_modal_status: false,
            station: {},
            equipment_data: {},
            more_info_data: {},
            type_checked: ['pv_lgroup', 'pv_group', 'inverter', 'sensor', 'string_meter', 'meter'],
        };
    },
    watch: {
        type_checked: function () {
            console.log(this.type_checked)
            this.refresh()
        },
    },
    methods: {
        search_select(item) {
            this.search = item
        },
        station_select(item) {
            this.station = item
            this.refresh()
        },
        delete_equipment(id) {
            console.log(id)
            var check = confirm('確定刪除該設備？')
            if (check) {
                this.axios.post("/setting/equipment_manage/delete", { id })
                alert('已刪除設備')
            }
        },
        more_info(obj) {
            this.more_info_data = obj
            // console.log(this.more_info_data)
            this.more_info_modal.show()
        },
        confirm_clicked() {
            this.more_info_modal.hide()
        },
        async refresh() {
            const obj = {
                'station':this.station,
                'type_checked':this.type_checked
            }
            await this.axios
                .post("/setting/equipment_manage", obj)
                .then((data) => {
                    console.log('data : ', data.data.data.data);
                    this.equipment_data = data.data.data.data;
                })
                .catch((err) => {
                    console.log(err);
                });
            // this.loading = false;
        },
        plant_create() {
            console.log('plant create clicked');
            console.log(this.type_checked);
            this.plant_modal_status = true;
        },
        lgroup_create() {
            console.log('lgroup create clicked');
            this.lgroup_modal_status = true;
        },
        group_create() {
            console.log('group create clicked');
            this.group_modal_status = true;
        },
        inverter_create() {
            console.log('inverter create clicked');
            this.inverter_modal_status = true;
        },
        sensor_create() {
            console.log('sensor create clicked');
            this.sensor_modal_status = true;
        },
        meter_create() {
            console.log('meter create clicked');
            this.meter_modal_status = true;
        },
        plantUpdateInfo(val) {
            this.plant_modal_status = val;
        },
        lgroupUpdateInfo(val) {
            this.lgroup_modal_status = val;
        },
        groupUpdateInfo(val) {
            this.group_modal_status = val;
        },
        inverterUpdateInfo(val) {
            this.inverter_modal_status = val;
        },
        sensorUpdateInfo(val) {
            this.sensor_modal_status = val;
        },
        meterUpdateInfo(val) {
            this.meter_modal_status = val;
        },
    },
    mounted() {
        this.more_info_modal = new Modal(
            this.$refs.more_info_modal
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
    }
};
</script>