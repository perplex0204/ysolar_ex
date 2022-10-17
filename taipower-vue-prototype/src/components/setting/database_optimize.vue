<template>
    <div class="card p-4">
        <h5>
            <i class="fa-solid fa-screwdriver-wrench text-primary me-2"></i>資料庫優化
        </h5>
        <div v-loading="this.loading">
            <div class="d-flex flex-wrap mt-4 align-items-center">
                <h6>目前使用之資料庫：{{  this.host  }}:{{  this.port  }}</h6>
            </div>
            <div class="d-flex flex-wrap mt-4 align-items-center">
                <h6>目前資料庫使用空間：{{  this.spaceUsage  }}MB</h6>
            </div>
            <div class="d-flex flex-wrap mt-4 align-items-center">
                <p>目前設定容量上限：{{  this.max_usage_to_show  }}MB</p>
            </div>
        </div>
        <div class="d-flex flex-wrap mt-2 align-items-center">
            <button @click="refresh" class="btn btn-primary mt-2 btn-sm ">重新獲取資料</button>
            <button @click="optimize" class="btn btn-primary mt-2 ms-lg-2 btn-sm ">立即優化</button>
            <button @click="set_usage" class="btn btn-primary mt-2 ms-lg-2 btn-sm ">設定容量上限</button>
        </div>
        <el-divider></el-divider>
        <!-- 設定header -->
        <div class="d-flex">
            <div class="col-6 col-lg-12 responsive_table ms-lg-2">
                <div style="overflow-y: scroll;">
                    <div class="w-100 row responsive_table_header  fw-bold m-0 d-none d-lg-flex flex-nowrap">
                        <div class="col-3 text-center">
                            <label class="fs-6">Collection</label>
                        </div>
                        <div class="col-3 text-center">
                            <label class="fs-6">Size</label>
                        </div>
                        <div class="col-3 text-center">
                            <label class="fs-6">Oldest data</label>
                        </div>
                        <div class="col-3 text-center">
                            <label class="fs-6">Count</label>
                        </div>
                    </div>
                    <div v-loading="this.loading">
                        <!-- 設定無資料的狀況 -->
                        <div class="w-100 pt-2 pb-2 text-center" v-if="this.collectionData.length == 0">
                            {{  $t('setting.iec61850.無資料')  }}
                        </div>
                        <!-- 設定body -->
                        <div class="w-100 responsive_table_body">
                            <div class="row m-0 responsive_table_content mt-2 mt-lg-0 pt-2 pb-3 p-lg-0"
                                v-for="data in this.collectionData" :key="data.name">
                                <div class="col-12 col-lg-3 pt-lg-4 pb-lg-4">
                                    <div class="d-flex d-lg-none">
                                        <label class="fs-6 fw-bold">Collection:</label>
                                        <label class="fs-6">{{  data.name  }}</label>
                                    </div>
                                    <label class="fs-6 w-100 text-center d-none d-lg-block">{{  data.name 
                                    }}</label>
                                </div>
                                <div class="col-12 col-lg-3 pt-lg-4 pb-lg-4">
                                    <div class="d-flex d-lg-none">
                                        <label class="fs-6 fw-bold">Size:</label>
                                        <label class="fs-6">{{  data.Size  }}</label>
                                    </div>
                                    <label class="fs-6 w-100 text-center d-none d-lg-block">{{  data.Size 
                                    }}MB</label>
                                </div>
                                <div class="col-12 col-lg-3 pt-lg-4 pb-lg-4">
                                    <div class="d-flex d-lg-none">
                                        <label class="fs-6 fw-bold">Oldest data:</label>
                                        <label class="fs-6">{{  data.Oldest_data  }}</label>
                                    </div>
                                    <label class="fs-6 w-100 text-center d-none d-lg-block">{{  data.Oldest_data 
                                    }}</label>
                                </div>
                                <div class="col-12 col-lg-3 pt-lg-4 pb-lg-4">
                                    <div class="d-flex d-lg-none">
                                        <label class="fs-6 fw-bold">Count:</label>
                                        <label class="fs-6">{{  data.Count  }}</label>
                                    </div>
                                    <label class="fs-6 w-100 text-center d-none d-lg-block">{{  data.Count 
                                    }}筆</label>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
        <!-- 設定容量上限的modal -->
        <div class="modal" tabindex="-1" ref="change_username_password_modal">
            <div class="modal-dialog modal-dialog-centered">
                <div class="modal-content">
                    <div class="modal-header">
                        <h5 class="modal-title"> 容量上限設定 </h5>
                        <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
                    </div>
                    <div class="modal-body">
                        <el-input v-model="max_usage" type="text" placeholder="請輸入欲設定之容量上限(MB)" />
                    </div>
                    <div class="modal-footer">
                        <button type="button" class="btn btn-success" @click="set_usage_clicked"> 確定 </button>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>

<script>
import { Modal } from "bootstrap";
export default {
    name: "databaseOptimize",
    components: {
    },
    data() {
        return {
            host: 'err',
            port: 'err',
            spaceUsage: 'err',
            collectionData: [],
            screenWidth: document.body.clientWidth,
            max_usage: '',
            max_usage_to_show: '',
            loading: true
        }
    },
    mounted() {
        this.change_username_password_modal = new Modal(
            this.$refs.change_username_password_modal
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
        set_usage() {
            this.change_username_password_modal.show();
        },
        // 按下設定容量上限
        async set_usage_clicked() {
            const typeObj = {
                max_usage: this.max_usage,
                function_type: 'set_max_usage'
            };
            await this.axios
                .post("/setting/database_optimize", typeObj)
                .then((typeObj) => { })
                .catch((err) => {
                    console.log(err);
                });
            this.change_username_password_modal.hide();
            this.refresh()
        },
        // 按下重新獲取資料
        async refresh() {
            this.loading = true;
            const typeObj = {
                function_type: 'refresh'
            };
            await this.axios
                .post("/setting/database_optimize", typeObj)
                .then((data) => {
                    console.log('refresh clicked!')
                    this.host = data.data.data['host'];
                    this.port = data.data.data['port'];
                    this.spaceUsage = data.data.data['space_usage'];
                    this.collectionData = data.data.data['collection_data'];
                    this.max_usage_to_show = data.data.data['max_usage_to_show'];
                })
                .catch((err) => {
                    console.log(err);
                });
            console.log(this.collectionData)
            if (Number(this.spaceUsage) > Number(this.max_usage_to_show)) {
                alert('注意：已使用容量大於設定值')
            }
            this.loading = false;
        },
        // 按下立即優化
        optimize() {
            var check = confirm('確定刪除五年以上資料庫資料？')
            if (check) {
                const typeObj = {
                    function_type: 'optimize'
                };
                this.axios
                    .post("/setting/database_optimize", typeObj)
                    .then((typeObj) => {
                        console.log('optimize clicked!')
                        console.log(this.max_uasge)
                    })
                    .catch((err) => {
                        console.log(err);
                    });
                alert('已刪除資料')
            } else {
                alert('已取消動作')
            }
        },
    },
    // 初次載入畫面
    created() {
        this.loading = true;
        const typeObj = {
            function_type: 'first_load'
        };
        this.axios
            .post("/setting/database_optimize", typeObj)
            .then((data) => {
                console.log('first_load : ', data.data.data);
                this.host = data.data.data['host'];
                this.port = data.data.data['port'];
                this.spaceUsage = data.data.data['space_usage'];
                this.collectionData = data.data.data['collection_data'];
                this.max_usage_to_show = data.data.data['max_usage_to_show'];
                if (Number(this.spaceUsage) > Number(this.max_usage_to_show)) {
                    alert('注意：已使用容量大於設定值')
                }
                this.loading = false;
            })
            .catch((err) => {
                console.log(err);
            });
    }
}
</script>