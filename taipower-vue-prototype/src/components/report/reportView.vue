<template>
    <div class="col-lg-12 responsive_table" :class="{'col-11 ms-auto me-auto': isComponent, 'col-12': !isComponent}">
        <div style="overflow-y: scroll;">
            <div class="w-100 row responsive_table_header  fw-bold m-0 d-none d-lg-flex flex-nowrap" v-if="['week_report', 'month_report', 'year_report', 'Tday_report', 'day_report'].includes(typeSelected)">
                <div class="col-4 text-center">
                    <label class="fs-6">{{$t('report.station')}}</label>
                </div>
                <div class="col-2 text-center">
                    <label class="fs-6">{{$t('report.period')}}</label>
                </div>
                <div class="col-4 text-center">
                    <label class="fs-6">{{$t('report.time')}}</label>
                </div>
                <div class="col-2 text-center">
                    <label class="fs-6">{{$t('report.download')}}</label>
                </div>
            </div>

            <div class="w-100 row responsive_table_header  fw-bold m-0 d-none d-lg-flex flex-nowrap" v-if="['inverter_excel'].includes(typeSelected)">
                <div class="col-4 text-center">
                    <label class="fs-6">{{$t('report.station')}}</label>
                </div>
                <div class="col-2 text-center">
                    <label class="fs-6">{{$t('report.inverter')}}</label>
                </div>
                <div class="col-4 text-center">
                    <label class="fs-6">{{$t('report.time')}}</label>
                </div>
                <div class="col-2 text-center">
                    <label class="fs-6">{{$t('report.download')}}</label>
                </div>
            </div>

            <!-- <div class="w-100 row responsive_table_header  fw-bold m-0 d-none d-lg-flex flex-nowrap" v-if="['day_report'].includes(typeSelected)">
                <div class="col-4 text-center">
                    <label class="fs-6">{{$t('report.station')}}</label>
                </div>
                <div class="col-2 text-center">
                    <label class="fs-6">{{$t('report.time_interval')}}</label>
                </div>
                <div class="col-4 text-center">
                    <label class="fs-6">{{$t('report.time')}}</label>
                </div>
                <div class="col-2 text-center">
                    <label class="fs-6">{{$t('report.download')}}</label>
                </div>
            </div> -->

            <div class="w-100 row responsive_table_header  fw-bold m-0 d-none d-lg-flex flex-nowrap" v-if="['week_report_A'].includes(typeSelected)">
                <div class="col-10 text-center">
                    <label class="fs-6">{{$t('report.time')}}</label>
                </div>
                <div class="col-2 text-center">
                    <label class="fs-6">{{$t('report.download')}}</label>
                </div>
            </div>

            <div class="w-100 row responsive_table_header  fw-bold m-0 d-none d-lg-flex flex-nowrap" v-if="['electricBill'].includes(typeSelected)">
                <div class="col-2 text-center">
                    <label class="fs-6">{{$t('report.station')}}</label>
                </div>
                <!-- <div class="col-1 text-center">
                    <label class="fs-6">{{$t('report.group')}}</label>
                </div> -->
                <div class="col-3 text-center">
                    <label class="fs-6">{{$t('report.month_head')}}</label>
                </div>
                <div class="col-2 text-center">
                    <label class="fs-6">{{$t('report.degree')}}</label>
                </div>
                <div class="col-2 text-center">
                    <label class="fs-6">{{$t('report.bill')}}</label>
                </div>
                <div class="col-2 text-center">
                    <label class="fs-6">{{$t('report.upload')}}</label>
                </div>
                <div class="col-1 text-center">
                    <label class="fs-6">{{$t('report.detail')}}</label>
                </div>
                <div class="col-1 text-center">
                    <label class="fs-6">{{$t('report.download')}}</label>
                </div>
            </div>


            <div class="w-100 pt-2 pb-2 text-center" v-if="reportData.length == 0">
                {{$t(emptyText)}}
            </div>

            <transition mode="out-in" :name="page_direction == 'to' ? 'table_animation_to':'table_animation_back'" v-if="['week_report', 'month_report', 'year_report', 'Tday_report', 'day_report'].includes(typeSelected)">
                <div class="w-100 col-lg-12 responsive_table_body" :key="currentPage" v-if="['week_report', 'month_report', 'year_report', 'Tday_report', 'day_report'].includes(typeSelected)">
                    <div class="row m-0 responsive_table_content mt-2 mt-lg-0" v-for="report in reportData" :key="report.place" 
                    >
                        <div class="col-12 d-lg-none mt-2"></div>
                        <div class="col-12 col-lg-4" v-if="['week_report', 'month_report', 'year_report', 'Tday_report', 'day_report'].includes(typeSelected)">
                            <div class="d-flex d-lg-none flex-wrap">
                                <label class="fs-6 fw-bold">{{$t('report.station')}}:</label>
                                <label class="fs-6">{{report.group}}</label>
                            </div>
                            <label class="fs-6 w-100 text-center d-none d-lg-block">{{report.group}}</label>
                        </div>
                        <!-- <div class="col-12 col-lg-4" v-if="['day_report'].includes(typeSelected)">
                            <div class="d-flex d-lg-none flex-wrap">
                                <label class="fs-6 fw-bold">{{$t('report.station')}}:</label>
                                <label class="fs-6">{{report.place}}</label>
                            </div>
                            <label class="fs-6 w-100 text-center d-none d-lg-block">{{report.place}}</label>
                        </div> -->
                        <div class="col-12 col-lg-2" v-if="['week_report', 'month_report', 'year_report', 'Tday_report', 'day_report'].includes(typeSelected)">
                            <div class="d-flex d-lg-none flex-wrap">
                                <label class="fs-6 fw-bold">{{$t('report.period')}}:</label>
                                <label class="fs-6">{{report.period}}</label>
                            </div>
                            <label class="fs-6 w-100 text-center d-none d-lg-block">{{report.period}}</label>
                        </div>
                        <!-- <div class="col-12 col-lg-2" v-if="['day_report'].includes(typeSelected)">
                            <div class="d-flex d-lg-none flex-wrap">
                                <label class="fs-6 fw-bold">{{$t('report.time_interval')}}:</label>
                                <label class="fs-6">{{report.interval}}</label>
                            </div>
                            <label class="fs-6 w-100 text-center d-none d-lg-block">{{report.interval}}</label>
                        </div> -->
                        <div class="col-12 d-lg-none mt-2 mb-2" style="border-bottom: 0.25px solid black;"></div>
                        <div class="col-12 col-lg-4" v-if="['week_report', 'month_report', 'year_report', 'Tday_report', 'day_report'].includes(typeSelected)">
                            <div class="d-lg-none">
                                <label class="fs-6 fw-bold d-lg-none">{{$t('report.time')}}:</label>
                                <label class="fs-6 d-lg-none">{{report.date}}</label>
                            </div>
                            <label class="fs-6 w-100 text-center d-none d-lg-block">{{report.date}}</label>
                        </div>
                        <!-- <div class="col-12 col-lg-4" v-if="['day_report'].includes(typeSelected)">
                            <div class="d-lg-none">
                                <label class="fs-6 fw-bold d-lg-none">{{$t('report.time')}}:</label>
                                <label class="fs-6 d-lg-none">{{report.time}}</label>
                            </div>
                            <label class="fs-6 w-100 text-center d-none d-lg-block">{{report.time}}</label>
                        </div> -->
                        <div class="col-12 col-lg-2">
                            <div class="d-lg-none d-flex">
                                <label class="fs-6 fw-bold d-lg-none">{{$t('report.download')}}:</label>
                                <button class="btn btn-success ms-1" @click="download(report.url)">{{$t('report.download')}}</button>
                            </div>
                            <button class="d-none d-lg-block btn btn-success position-relative top-50 start-50 translate-middle" @click="download(report.url)">{{$t('report.download')}}</button>
                        </div>
                    </div> 
                </div>
            </transition>
            <transition mode="out-in" :name="page_direction == 'to' ? 'table_animation_to':'table_animation_back'" v-if="['week_report_A', 'inverter_excel'].includes(typeSelected)">
                <div class="w-100 col-lg-12 responsive_table_body" :key="currentPage" v-if="['week_report_A', 'inverter_excel'].includes(typeSelected)">
                    <div class="row m-0 responsive_table_content mt-2 mt-lg-0" v-for="report in reportData" :key="report.place" 
                    >
                        <div class="col-12 d-lg-none mt-2"></div>
                        <div class="col-12 col-lg-4" v-if="['inverter_excel'].includes(typeSelected)">
                            <div class="d-flex d-lg-none flex-wrap">
                                <label class="fs-6 fw-bold">{{$t('report.station')}}:</label>
                                <label class="fs-6">{{report.group}}</label>
                            </div>
                            <label class="fs-6 w-100 text-center d-none d-lg-block">{{report.group}}</label>
                        </div>
                        <div class="col-12 col-lg-2" v-if="['inverter_excel'].includes(typeSelected)">
                            <div class="d-flex d-lg-none flex-wrap">
                                <label class="fs-6 fw-bold">{{$t('report.inverter')}}:</label>
                                <label class="fs-6">{{report.inverter}}</label>
                            </div>
                            <label class="fs-6 w-100 text-center d-none d-lg-block">{{report.inverter}}</label>
                        </div>
                        <div class="col-12 d-lg-none mt-2 mb-2" style="border-bottom: 0.25px solid black;"></div>
                        <div class="col-12 col-lg-4" v-if="['inverter_excel'].includes(typeSelected)">
                            <div class="d-lg-none">
                                <label class="fs-6 fw-bold d-lg-none">{{$t('report.time')}}:</label>
                                <label class="fs-6 d-lg-none">{{report.date}}</label>
                            </div>
                            <label class="fs-6 w-100 text-center d-none d-lg-block">{{report.date}}</label>
                        </div>
                        <div class="col-12 col-lg-10" v-if="['week_report_A'].includes(typeSelected)">
                            <div class="d-lg-none">
                                <label class="fs-6 fw-bold d-lg-none">{{$t('report.time')}}:</label>
                                <label class="fs-6 d-lg-none">{{report.date}}</label>
                            </div>
                            <label class="fs-6 w-100 text-center d-none d-lg-block">{{report.date}}</label>
                        </div>
                        <div class="col-12 col-lg-2">
                            <div class="d-lg-none d-flex">
                                <label class="fs-6 fw-bold d-lg-none">{{$t('report.download')}}:</label>
                                <button class="btn btn-success ms-1" @click="download(report.url)">{{$t('report.download')}}</button>
                            </div>
                            <button class="d-none d-lg-block btn btn-success position-relative top-50 start-50 translate-middle" @click="download(report.url)">{{$t('report.download')}}</button>
                        </div>
                    </div> 
                </div>
            </transition>
            <transition mode="out-in" :name="page_direction == 'to' ? 'table_animation_to':'table_animation_back'" v-if="['electricBill'].includes(typeSelected)">
                <div class="w-100 col-lg-12 responsive_table_body" :key="currentPage" v-if="['electricBill'].includes(typeSelected)">
                    <div class="row m-0 responsive_table_content mt-2 mt-lg-0" v-for="report in reportData" :key="report.place" 
                    >
                        <div class="col-12 d-lg-none mt-2"></div>
                        <div class="col-12 col-lg-2">
                            <div class="d-flex d-lg-none flex-wrap">
                                <label class="fs-6 fw-bold">{{$t('report.station')}}:</label>
                                <label class="fs-6">{{report.station_name}}</label>
                            </div>
                            <label class="fs-6 w-100 text-center d-none d-lg-block">{{report.station_name}}</label>
                        </div>
                        <!-- <div class="col-12 col-lg-1">
                            <div class="d-flex d-lg-none flex-wrap">
                                <label class="fs-6 fw-bold">{{$t('report.group')}}:</label>
                                <label class="fs-6">{{report.lgroup}}</label>
                            </div>
                            <label class="fs-6 w-100 text-center d-none d-lg-block">{{report.lgroup}}</label>
                        </div> -->
                        <!-- <div class="col-12 d-lg-none mt-2 mb-2" style="border-bottom: 0.25px solid black;"></div> -->
                        <div class="col-12 col-lg-3">
                            <div class="d-lg-none">
                                <label class="fs-6 fw-bold d-lg-none">{{$t('report.month_head')}}:</label>
                                <label class="fs-6 d-lg-none">{{report.month}}</label>
                            </div>
                            <label class="fs-6 w-100 text-center d-none d-lg-block">{{report.month}}</label>
                        </div>
                        <div class="col-12 d-lg-none mt-2 mb-2" style="border-bottom: 0.25px solid black;"></div>
                        <div class="col-12 col-lg-2">
                            <div class="d-lg-none">
                                <label class="fs-6 fw-bold d-lg-none">{{$t('report.degree')}}:</label>
                                <label class="fs-6 d-lg-none">{{report.kwh}}</label>
                            </div>
                            <label class="fs-6 w-100 text-center d-none d-lg-block">{{report.kwh}}</label>
                        </div>
                        <!-- <div class="col-12 d-lg-none mt-2 mb-2" style="border-bottom: 0.25px solid black;"></div> -->
                        <div class="col-12 col-lg-2">
                            <div class="d-lg-none">
                                <label class="fs-6 fw-bold d-lg-none">{{$t('report.bill')}}:</label>
                                <label class="fs-6 d-lg-none">{{report.cost}}</label>
                            </div>
                            <label class="fs-6 w-100 text-center d-none d-lg-block">{{report.cost}}</label>
                        </div>
                        <div class="col-12 d-lg-none mt-2 mb-2" style="border-bottom: 0.25px solid black;"></div>
                        <div class="col-12 col-lg-2">
                            <div class="d-lg-none">
                                <label class="fs-6 fw-bold d-lg-none">{{$t('report.upload')}}:</label>
                                <label class="fs-6 d-lg-none">{{report.upload_time}}</label>
                            </div>
                            <label class="fs-6 w-100 text-center d-none d-lg-block">{{report.upload_time}}</label>
                        </div>
                        <div class="col-12 d-lg-none mt-2 mb-2" style="border-bottom: 0.25px solid black;"></div>
                        <div class="col-12 col-lg-1">
                            <div class="d-lg-none d-flex">
                                <label class="fs-6 fw-bold d-lg-none">{{$t('report.detail')}}:</label>
                                <button class="btn btn-success ms-1" @click="updateBill(report)">{{$t('report.detail')}}</button>
                            </div>
                            <button class="d-none d-lg-block btn btn-success position-relative top-50 start-50 translate-middle" @click="updateBill(report)">{{$t('report.detail')}}</button>
                        </div>
                        <div class="col-12 d-lg-none mt-2 mb-2" style="border-bottom: 0.25px solid black;"></div>
                        <div class="col-12 col-lg-1">
                            <div class="d-lg-none d-flex">
                                <label class="fs-6 fw-bold d-lg-none">{{$t('report.download')}}:</label>
                                <button class="btn btn-success ms-1" @click="download(report.url)">{{$t('report.download')}}</button>
                            </div>
                            <button class="d-none d-lg-block btn btn-success position-relative top-50 start-50 translate-middle" @click="download(report.url)">{{$t('report.download')}}</button>
                        </div>
                    </div> 
                </div>
            </transition>
        </div>
        <div class="w-100 responsive_table_footer pt-2 pb-2 d-flex justify-content-between justify-content-lg-center"
        v-if="reportData.length > 0">
            <i class="fas fa-angle-double-left footer_icon" @click="pageChange('bb')"></i>
            <i class="fas fa-angle-left footer_icon" @click="pageChange('b')"></i>
            <div class="col-1 text-white text-center">
                <label class="fs-5">{{currentPage}}</label>
                <label class="fs-6" style="color: orange;">/</label>
                <label class="fs-7">{{totalPage}}</label>
            </div>
            <i class="fas fa-angle-right footer_icon" @click="pageChange('f')"></i>
            <i class="fas fa-angle-double-right footer_icon" @click="pageChange('ff')"></i>
    
            
        </div>

        <div class="es_popup p-0 p-lg-4" ref="createNewBill" style="overflow-x: scroll;">
            <div class="modal-content p-4">
                <createNewBill ref="createBill" @close-bill-upload="closePop" :isComponent="isComponent" />
            </div>
        </div>
        <div class="es_popup p-0 p-lg-4" ref="updateBillRecord" style="overflow-y: scroll;">
            <div class="modal-content p-4">
                <updateBillRecord ref="billRecord" @close-bill-upload="closePop" />
            </div>
        </div>
        <div
            class="close_popup_bill"
            :class="{'component_class': isComponent}"
            v-show="!isShow"
            @click.stop.prevent="closePop"
        >
            <i class="el-icon-close"></i>
        </div>
    </div>
</template>

<script>
import updateBillRecord from "@/components/bill/updateBillRecord.vue"
import createNewBill from "@/components/bill/createNewBill.vue"
export default {
    name: "reportView",
    data(){
        return {
            page_direction: "",
            isShow: true,
        }
    },
    components:{
        updateBillRecord,
        createNewBill
    },
    props: {
        reportData:{type: Array, required: true, default: function(){return []}},
        typeSelected: {type: String, required: true, default: "day_report"},
        emptyText: {type: String, default: "無資料"},
        currentPage: {type: Number, required: true},
        totalPage: {type: Number, required: true},
        isComponent: {type: Boolean, default: false}
    },
    methods: {
        pageChange(type){
            switch(type){
                case "bb":
                    this.page_direction = "back"
                    if(this.currentPage > 10)
                        this.$emit("page-change", this.currentPage - 10)
                    else
                        this.$emit("page-change", 1)
                    break
                case "b":
                    this.page_direction = "back"
                    if(this.currentPage > 1)
                        this.$emit("page-change", this.currentPage - 1)
                    else
                        this.$emit("page-change", 1)
                    break
                case "ff":
                    this.page_direction = "to"
                    if(this.currentPage < this.totalPage - 10)
                        this.$emit("page-change", this.currentPage + 10)
                    else
                        this.$emit("page-change", this.totalPage)
                    break
                case "f":
                    this.page_direction = "to"
                    if(this.currentPage < this.totalPage)
                        this.$emit("page-change", this.currentPage + 1)
                    else
                        this.$emit("page-change", this.totalPage)
                    break
            }
        },
        download(url){
            console.log(url)
            let link = document.createElement("a")
            document.body.appendChild(link)
            link.href = url
            link.click()
            document.body.removeChild(link)
        },
        updateBill(data) {
            this.isShow = false;
            this.$refs.updateBillRecord.style.display = "block";
            this.$refs.billRecord.open_pop(data);
        },
        closePop() {
            this.isShow = true;
            this.$refs.createNewBill.style.display = "none";
            this.$refs.updateBillRecord.style.display = "none";
            this.$refs.billRecord.reset()
            this.$parent.search_bill()
        },
        createBill() {
            this.isShow = false;
            this.$refs.createNewBill.style.display = "block";
        },
        
    },
    mounted() {
        this.pageChange("b")
    }
}
</script>

<style scoped>
/* @popup */
.es_popup{
	position: fixed;
	width: calc(100% - 13rem);
	height: 100%;
	padding: 2rem;
	z-index: 10;
    top: 0;
    right: 0;
	display: none;
	animation: fadeInDown .5s cubic-bezier(0.25, 1, 0.5, 1);
	transition: width .5s;
}
@media(max-width: 991px){
    .es_popup{
        width: 100%;
    }
}
#mainNav.close + #layoutBody .es_popup,
#mainNav.close + #layoutBody .station_pop{
	width: calc(100% - 8rem);
}
.update_new_bill_wrap,
.create_new_bill_wrap {
	width: 100%;
	padding: 2rem;
	margin-top: 2rem;
	border-radius: 1rem;
	z-index: 3;
	background-color: #ffffff;
	box-shadow: 0 0 15px rgba(63,63,63,.1);
}
.create_new_bill_wrap .create_bill_selector {
	margin-bottom: 1rem;
	display: flex;
	align-items: center;
}

.create_new_bill_wrap .create_bill_selector span {
	margin-right: 0.5rem;
}
.update_new_bill_wrap .el-input.is-disabled .el-input__inner,
.chart_tab_bill .el-input.is-disabled .el-input__inner{
	position: relative;
	width: 8.1rem;
    background-color:#FFF2EC;
    border-color:#FFF2EC;
	color: #FF8046;
    cursor: auto;
	padding: 0.6rem 0rem;
	padding-right: 0rem;
	padding-left: 3rem;
}

.update_new_bill_wrap .el-input.is-disabled .el-input__icon::before,
.chart_tab_bill .el-input.is-disabled .el-input__icon::before {
	position: absolute;
	bottom: 0rem;
	left: 0.5rem;
	color: #FF8046;
}
.update_new_bill_wrap .update_bill_selector {
	margin-bottom: 1rem;
	display: flex;
	align-items: center;
}
.update_new_bill_wrap {
	width: 100%;
	padding: 2rem;
	margin-top: 2rem;
	border-radius: 1rem;
	z-index: 3;
	background-color: #ffffff;
	box-shadow: 0 0 15px rgba(63,63,63,.1);
}
.close_popup_bill{
	position: fixed;
	right: 2rem;
	top: 4rem;
	cursor: pointer;
	z-index: 10;
}
.close_popup_bill i:before{
	font-size: 2rem;
	color: var(--text-main);
}
.close_popup_bill:hover{
	opacity: 0.5;
}
.component_class{
    position: fixed;
    top: 3.9rem !important;
    bottom: auto !important;
    z-index: 100;
}
</style>