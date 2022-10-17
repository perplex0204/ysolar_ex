<template>
    <div class="update_bill_container" style="">
        <div class="update_bill_selector d-flex flex-wrap">
            <div class="update_bill_title">{{station_name}}</div>
            <dateMonthPicker
                :parent-date="dateSelected"
                :parent-is-disabled="isDisabled"
                @set-date="set_date"
            />
        </div>
        <label>{{ 'starttime' in report_data? `${report_data.starttime}~${report_data.endtime}`: 'time' in report_data? this.report_data.time: '' }}</label>
        <div v-if="!isUpdated" class="card mt-3 mb-3 col-12" v-loading="isLoading">
            <div v-if="file_url != null"
                class="w-100 mb-4"
                style="min-height: 70vh;"
            >
                <embed 
                    class="w-100 mb-4"
                    style="min-height: 70vh;"
                    v-if="show_pdf"
                    :src="file_url"
                    type="application/pdf"
                />
            </div>
            <div class="w-100 mb-4 d-flex align-items-center justify-content-center" 
            style="min-height: 70vh;" v-else>
                <h1>
                    <i class="fas fa-file-excel"></i>
                </h1>
            </div>
        </div>


        <div class="col-12 col-lg-12 mx-0 px-0 d-lg-flex justify-content-center">
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
                                        <label class="fs-6 d-lg-none">{{data.kwh}}</label>
                                    </div>
                                    <label class="fs-6 w-100 text-center d-none d-lg-block">{{data.kwh}}</label>
                                </div>
                                <div class="col-12 d-lg-none mt-2 mb-2" style="border-bottom: 0.25px solid black;"></div>
                                <div class="col-12 col-lg-3 pt-lg-4 pb-lg-4">
                                    <div class="d-lg-none">
                                        <label class="fs-6 fw-bold d-lg-none">{{$t('table.電費')}}:</label>
                                        <label class="fs-6 d-lg-none">{{data.fee}}</label>
                                    </div>
                                    <label class="fs-6 w-100 text-center d-none d-lg-block">{{data.fee}}</label>
                                </div>
                                <div class="col-12 col-lg-4 pt-lg-4 pb-lg-4">
                                    <div class="d-lg-none">
                                        <label class="fs-6 fw-bold d-lg-none">{{$t('table.Pvsyst_DMY')}}:</label>
                                        <label class="fs-6 d-lg-none">{{data.dmy}}</label>
                                    </div>
                                    <label class="fs-6 w-100 text-center d-none d-lg-block">{{data.dmy}}</label>
                                </div>
                            </div> 
                        </div>
                    </div>
                </div>
            </div>
        </div>

        <div v-if="!isUpdated && !isLoading" class="btn_update_bill_wrapper mt-2">
            <button class="btn btn-danger me-2 ps-4 pe-4" v-if="file_url != null"
            @click="deleteBillRecord">
                {{$t("report.刪除紀錄")}}
            </button>
            <el-button
                class="btn_chart_update_bill ms-auto"
                type="primary"
                @click="updateBillRecord"
            >
                {{$t("report.更新此紀錄")}}
            </el-button>
        </div>
    </div>
</template>

<script>
import dateMonthPicker from "../datepicker/monthPicker.vue";
import c from "@/assets/js/common.js"

export default {
    name: "updateBillReocrd",
    data() {
        return {
            isLoading: false,
            isUpdated: false,
            dateSelected: new Date(),
            isDisabled: false,
            station_name: null,
            file_url: null,
            report_data: {},
            show_pdf: false,
            tableData: [],
            date_value: c.formatDate(new Date()),
            station_ID: null,
        };
    },
    components: {
        dateMonthPicker,
    },
    mounted(){
        this.axios_instance = this.axios.create({
            baseURL: '/',
            timeout: 1000,
        })
    },
    methods: {
        deleteBillRecord() {
            const answer = confirm(this.$i18n.t('report.confirm_delete'))
            if(answer){
                this.axios.post('/delete_electricBill', {
                    ID: this.station_ID,
                    starttime: this.date_value, endtime: this.date_value
                }).then(data=>{
                    this.$message.success('成功')
                    this.callParentCloseUpload()
                })
            }
        },
        reset(){
            this.isLoading = false
            this.isUpdated = false
            this.isDisabled = false
            this.station_name = null
            this.file_url = null
            this.show_pdf = false
            this.report_data = {},
            this.station_ID = null
        },
        open_pop(data){
            this.isLoading = true
            this.report_data = data
            this.station_name = `${data.PV}/${data.lgroup}`
            this.dateSelected = new Date(data.month.substring(0, 4), data.month.substring(5,7)-1, data.month.substring(8,10))
            this.date_value = c.formatDate(this.dateSelected)
            this.station_ID = data.ID
            this.is_report_exist(data.url)
        },
        updateBillRecord() {
            //this.isUpdated = true;
            // this.$parent.isShow = true
            this.$parent.$refs.updateBillRecord.style.display = "none"
            this.$parent.createBill()
            this.$parent.$refs.createBill.remove_file()
            this.$parent.$refs.createBill.electricBill_data.station_name = this.station_name
            this.$parent.$refs.createBill.electricBill_data.station_ID = this.station_ID
            this.$parent.$refs.createBill.date_value = 'starttime' in this.report_data ? [
                new Date(this.report_data.starttime.substring(0, 4), this.report_data.starttime.substring(5,7)-1, this.report_data.starttime.substring(8,10)), 
                new Date(this.report_data.endtime.substring(0, 4), this.report_data.endtime.substring(5,7)-1, this.report_data.endtime.substring(8,10))] : [this.date_value, this.date_value]
            this.$parent.$refs.createBill.date_value_str = this.$parent.$refs.createBill.get_format_date()
            this.$parent.$refs.createBill.get_electricBill_data()
        },
        callParentCloseUpload() {
            this.reset()
            this.$emit("close-bill-upload");
        },
        async is_report_exist(file_url=null){
            this.show_pdf = false
            this.isLoading = true
            let request_dict = {
                ID: this.station_ID,
                starttime: this.date_value, endtime: this.date_value}
            this.axios.post('/get_electricBill_data', request_dict).then(data => {
                this.tableData = data.data.data.tableData
                let element = data.data.data.bill_pdf
                this.report_data = element
                if(Object.keys(element).length == 0){
                    this.file_url = null
                    this.isLoading = false
                    return false
                }
                file_url = 'starttime' in element? `solar_static/uploadBill/${element.PV_ID}/${element.ID}/${element._id}/bill.pdf`: `solar_static/uploadBill/${element.PV_ID}/${element.ID}/${element.time}/bill.pdf`
                this.report_data['file_url'] = file_url
                console.log(file_url)
                this.axios_instance.get(file_url)
                .then(data=>{
                    this.file_url = file_url
                    setTimeout(()=>{
                        this.show_pdf = true
                        this.isLoading = false
                    }, 500)
                })
                .catch(err=>{
                    console.error("No PDF")
                    this.file_url = null
                    setTimeout(()=>{
                        this.isLoading = false
                    }, 500)
                })
            })
        },
        set_date(new_date){
            /* let current_month = new_date.substring(0, 7)
            if(Object.keys(this.report_data).length > 0){
                this.report_data.month = current_month
                this.isLoading = true
                this.is_report_exist(`solar_static/uploadBill/${this.report_data.PV_ID}/${this.report_data.ID}/${current_month}/bill.pdf`)
            } */
            this.date_value = new_date
            this.is_report_exist()
        }
    },
};
</script>

<style scoped>
.update_bill_container .bill_record {
	height: 60vh;
	border-radius: 1rem;
	box-shadow: 0 0 15px #dee4ea;
	margin-bottom: 1rem;
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
.btn_update_bill_wrapper {
	display: flex;
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
.btn_chart_delete_record {
	margin-right: auto;
	margin-left: 0;
}
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
}
@media(max-width: 991px){
    .bill_upload_page .el-upload-dragger{
        width: 70vw !important;
    }
    .update_bill_container .bill_record {
        width: 70vw !important;
    }
    .update_bill_selector{
        width: 70vw !important;
    }
    .bill_upload_page .bill_upload_area, 
    .bill_upload_page .el-upload {
        width: 70vw;
    }
}
</style>