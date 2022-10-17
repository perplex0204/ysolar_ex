<template>
    <div class="bill_upload_page d-flex d-lg-block flex-wrap" style="align-items: unset;">
        <div class="create_bill_selector flex-wrap">
            <autocomplete class="me-0 me-lg-3 col-lg-2 mt-lg-1" :class="{'col-12': isComponent, 'col-11': !isComponent}" @station-select="(item) => {
                electricBill_data.station_name = item.name;
                electricBill_data.station_ID = item.ID; 
                this.get_electricBill_data()   
            }"></autocomplete>
            <label class="mt-2 mb-2 d-block">{{$t('report.電費單區間')}}</label>
            <el-date-picker
                v-model="date_value"
                type="daterange"
                start-placeholder="Start date"
                end-placeholder="End date"
                size="large"
                class="d-none d-lg-block"
                @change="()=>{
                    date_value_str=this.get_format_date()
                    this.get_electricBill_data()
                }"
            />
        </div>
        <div class="update_bill_selector mb-3">
            <div class="update_bill_title" v-if="electricBill_data.station_ID != null">{{electricBill_data.station_name}}</div>
        </div>
        <div class="mb-3" v-if="Object.keys(bill_pdf).length > 0">
            <el-alert
                :title="$t(`report.上傳過電費單`)"
                type="warning"
                show-icon
                :closable="false"
            >
            </el-alert>
        </div>
        <el-upload
            class="bill_upload_area el-upload"
            drag
            :action="`${axios.defaults.baseURL}/electricBill_upload_file`"
            accept="application/pdf"
            :auto-upload="false"
            :on-change="file_select"
            v-show="upload_file_blob_url == null"
            ref="uploader"
            :on-success="upload_success"
            :on-error="upload_error"
            :data="{
              ID:  electricBill_data.station_ID,
              starttime: date_value_str[0],
              endtime: date_value_str[1]
            }"
        >
            <div>
                <i class="el-icon-upload"></i>
                <div>
                    {{$t("report.文件拖曳到此")}}<span>&nbsp;</span><em class="text-primary">{{$t("report.點擊上傳")}}</em>
                </div>
                <!-- <div class="el-upload__tip" slot="tip">
                    上傳您的電費單 .png
                </div> -->
            </div>
        </el-upload>
        <embed 
        v-if="upload_file_blob_url != null"
        class="w-100 mb-4"
        style="min-height: 70vh;"
        :src="upload_file_blob_url" />
        <div class="d-flex flex-wrap w-100 mt-2">
            <el-button
                class="btn_chart_new_bill ms-0"
                type="danger"
                v-show="parentIsShow && upload_file_blob_url != null"
                @click.stop.prevent="remove_file"
            >
                {{$t("取消")}}
            </el-button>
            <el-button
                class="btn_chart_new_bill ms-auto"
                type="primary"
                v-show="parentIsShow"
                v-loading="is_loading"
                @click.stop.prevent="confirm_upload"
            >
                {{$t("report.確認上傳")}}
            </el-button>
        </div>
        
        <h5 v-if="electricBill_data.station_ID != null"><i class="fa-solid fa-pen text-success me-2 mt-4"></i>{{$t("report.電費單填寫")}}</h5>
        <div class="col-12 col-lg-12 mx-0 px-0 d-lg-flex justify-content-center mt-2" v-if="electricBill_data.station_ID != null">
            <div class="card shadow col-lg-12">
                <div class="responsive_table shadow-none">
                    <div style="overflow-y: scroll;">
                        <div class="w-100 row responsive_table_header fw-bold m-0 d-none d-lg-flex flex-nowrap">
                            <div class="col-2 text-center">
                                <label class="fs-6">{{$t('table.類別')}}</label>
                            </div>
                            <div class="col-3 text-center">
                                <label class="fs-6">{{$t('table.kWh')}}</label>
                            </div>
                            <div class="col-3 text-center">
                                <label class="fs-6">{{$t('table.電費')}}</label>
                            </div>
                            <div class="col-4 text-center">
                                <label class="fs-6">{{$t('table.Pvsyst_DMY')}}</label>
                            </div>
                        </div>
                        <div class="w-100 pt-2 pb-2 text-center" v-if="tableData.length == 0">
                            {{$t('無資料')}}
                        </div>
                        <div class="w-100 col-lg-12 responsive_table_body" style="max-height: 400px">
                            <div class="row m-0 responsive_table_content mt-2 mt-lg-0" v-for="data in tableData" :key="data.method" 
                            >
                                <div class="col-12 d-lg-none mt-2"></div>
                                <div class="col-12 col-lg-2 pt-lg-4 pb-lg-4">
                                    <div class="d-flex d-lg-none flex-wrap">
                                        <label class="fs-6 fw-bold">{{$t('table.類別')}}:</label>
                                        <label class="fs-6">{{data.method}}</label>
                                    </div>
                                    <label class="fs-6 w-100 text-center d-none d-lg-block">{{data.method}}</label>
                                </div>
                                <div class="col-12 col-lg-3 pt-lg-4 pb-lg-4">
                                    <div class="d-lg-none">
                                        <label class="fs-6 fw-bold d-lg-none">{{$t('table.kWh')}}:</label>
                                        <label class="fs-6 d-lg-none">
                                            <el-input v-model="data.kwh" type="number"
                                            @change="tableData_update" :readonly="data.readonly"></el-input>
                                        </label>
                                    </div>
                                    <label class="fs-6 w-100 text-center d-none d-lg-block">
                                        <el-input v-model="data.kwh" type="number"
                                        @change="tableData_update" :readonly="data.readonly"></el-input>
                                    </label>
                                </div>
                                <div class="col-12 d-lg-none mt-2 mb-2" style="border-bottom: 0.25px solid black;"></div>
                                <div class="col-12 col-lg-3 pt-lg-4 pb-lg-4">
                                    <div class="d-lg-none">
                                        <label class="fs-6 fw-bold d-lg-none">{{$t('table.電費')}}:</label>
                                        <label class="fs-6 d-lg-none">
                                            <el-input v-model="data.fee" type="number"
                                            @change="tableData_update" :readonly="data.readonly"></el-input>
                                        </label>
                                    </div>
                                    <label class="fs-6 w-100 text-center d-none d-lg-block">
                                        <el-input v-model="data.fee" type="number"
                                        @change="tableData_update" :readonly="data.readonly"></el-input>
                                    </label>
                                </div>
                                <div class="col-12 d-lg-none mt-2 mb-2" style="border-bottom: 0.25px solid black;"></div>
                                <div class="col-12 col-lg-4 pt-lg-4 pb-lg-4">
                                    <div class="d-lg-none">
                                        <label class="fs-6 fw-bold d-lg-none">{{$t('table.Pvsyst_DMY')}}:</label>
                                        <label class="fs-6 d-lg-none col-6">
                                            <el-input v-model="data.dmy" type="number"
                                            @change="tableData_update" :readonly="data.readonly"></el-input> 
                                        </label>
                                    </div>
                                    <label class="fs-6 w-100 text-center d-none d-lg-block">
                                        <el-input v-model="data.dmy" type="number"
                                        @change="tableData_update" :readonly="data.readonly"></el-input>    
                                    </label>
                                </div>
                            </div> 
                        </div>
                    </div>
                </div>
            </div>
        </div>

    </div>
</template>

<script>
import autocomplete from "../autocomplete/lgroup_only.vue";
import c from "assets/js/common.js";

export default {
    name: "createNewBill",
    components: {
        autocomplete,
    },
    props: {
        parentIsShow: {
            type: Boolean,
            default: true
        },
        isComponent: {type: Boolean, default: false}
    },
    data(){
      return {
            upload_file_blob_url: null,
            electricBill_data: {
                station_name: null,
                station_ID: null,
            },
            isDisabled: true,
            dateSelected: new Date(),
            is_loading: false,
            tableData: [
                {
                    method: "TaipowerBill",
                    kwh: null,
                    fee: null,
                    dmy: null,
                    readonly: false,
                },
                /* {
                    method: "Pvsyst",
                    kwh: null,
                    fee: null,
                    dmy: null,
                    readonly: false,
                } */
            ],
            bill_pdf: {},
            date_value: [new Date(), new Date()],
            date_value_str: [
                c.formatDate(new Date()),
                c.formatDate(new Date())
            ]
      }  
    },
    methods: {
        callParentCloseUpload() {
            this.$emit("close-bill-upload");
        },
        file_select(file, fileList){
            this.upload_file_blob_url = URL.createObjectURL(fileList[0].raw)
        },
        confirm_upload(){
            if(this.electricBill_data.station_ID == null){
                alert("請選擇案場")
                return false
            }
            if(this.upload_file_blob_url == null){
                alert("請上傳資料")
                return false
            }
            if(this.date_value == null || this.date_value.length == 0){
                alert("請選擇開始與結束日期")
                return false
            }
            this.is_loading = true
            this.$refs.uploader.submit()
        },
        upload_success(response, file, fileList){
            //console.log(response, file, fileList)
            this.$message.success('成功')
            this.is_loading = false
            this.remove_file()
            this.station_ID = null
            this.callParentCloseUpload()
        },
        upload_error(){
            this.is_loading = false
            this.$message.error('上傳失敗')
            this.remove_file()
        },
        remove_file(){
            this.$refs.uploader.clearFiles();
            this.upload_file_blob_url = null;
        },
        get_electricBill_data(){
            this.bill_pdf = {}
            if(this.electricBill_data.station_ID != null)
                this.axios.post('/get_electricBill_data', {
                    ID: this.electricBill_data.station_ID,
                    starttime: this.date_value_str[0],
                    endtime: this.date_value_str[1]
                }).then(data => {
                    console.log(data.data.data)
                    this.bill_pdf = data.data.data.bill_pdf
                    this.tableData = data.data.data.tableData
                })
        },
        tableData_update(){
            console.log(this.tableData)
            this.axios.post('/update_electricBill_tableData', {
                ID: this.electricBill_data.station_ID,
                tableData: this.tableData,
                starttime: this.date_value_str[0],
                endtime: this.date_value_str[1]
            })
        },
        get_format_date(){
            return [
                c.formatDate(this.date_value[0]),
                c.formatDate(this.date_value[1])
            ]
        }
    }
};
</script>

<style scoped>
.bill_upload_page {
	display: flex;
	flex-direction: column;
	width: 100%;
	margin-bottom: 1rem;
	justify-content: center;
	align-items: center;
	border-radius:6px;
}

.bill_upload_page .bill_upload_area, 
.bill_upload_page .el-upload {
	width: 100%;
	margin-bottom: 1rem;
}
.el-upload{
    text-align: left !important;
}
.bill_upload_page .el-upload-dragger{
	border:1px solid #d9d9d9;
	display: flex;
	justify-content: center;
	align-items: center;
    box-sizing: border-box;
    width: 100%;
    text-align: center;
    position: relative;
}
.create_new_bill_wrap .create_bill_selector {
	margin-bottom: 1rem;
	display: flex;
	align-items: center;
}

.create_new_bill_wrap .create_bill_selector span {
	margin-right: 0.5rem;
}
.update_new_bill_wrap .update_bill_selector {
	margin-bottom: 1rem;
	display: flex;
	align-items: center;
}

.update_bill_selector .update_bill_title {
	margin-right: auto;
	color:#00AD74;
	font-size: 1.8rem;
}
.bill_upload_area:last-child .el-upload-list {
	width: 95%;
	position: absolute;
	bottom: 4.5rem;
    left: 50%;
	transform: translateX(-50%);
    text-align: center;
}

.bill_upload_area .el-upload-dragger{
	min-height: 50% !important;
	height: 75%;
    width: 100%;
}
.btn_chart_delete_record,
.btn_chart_update_bill,
.btn_chart_new_bill,
.btn_chart_download {
	display: flex;
	font-size: 14px;
	margin-left: auto;
	justify-content: center;
	align-items: center;
	height: 40px;
	width: 100px;
}
.el-upload-dragger .el-upload__text{
    color:#2B333B;
    font-size:1rem;
    text-align:center
}
.el-upload-dragger .el-upload__text em{
    font-style:normal
}
.el-upload-dragger{
    width: 100% !important;
}
.el-icon-upload{
    font-size: 67px;
    color: #dee4ea;
    margin: 40px 0 16px;
    line-height: 50px;
}
@media(max-width: 991px){
    .bill_upload_area .el-upload-dragger{
        width: 100vw;
    }
}
</style>