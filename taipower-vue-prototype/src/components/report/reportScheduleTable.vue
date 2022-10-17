<template>
    <div>
        <div class="col-12 col-lg-12 responsive_table">
            <div style="overflow-y: scroll;">
                <div class="w-100 row responsive_table_header  fw-bold m-0 d-none d-lg-flex flex-nowrap">
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
                </div>
                <div class="w-100 pt-2 pb-2 text-center" v-if="reportScheduleData.length == 0">
                    {{$t(emptyText)}}
                </div>
                <transition mode="out-in" :name="page_direction == 'to' ? 'table_animation_to':'table_animation_back'">
                    <div class="w-100 col-lg-12 responsive_table_body" :key="currentPage">
                        <div class="row m-0 responsive_table_content mt-2 mt-lg-0" v-for="report in reportScheduleData" :key="report.place" 
                        >
                            <div class="col-12 d-lg-none mt-2"></div>
                            <div class="col-12 col-lg-4 ">
                                <div class="d-flex d-lg-none flex-wrap">
                                    <label class="fs-6 fw-bold">{{$t('report.station')}}:</label>
                                    <label class="fs-6">{{report.place}}</label>
                                </div>
                                <label class="fs-6 w-100 text-center d-none d-lg-block">{{report.place}}</label>
                            </div>
                            <div class="col-12 col-lg-2 ">
                                <div class="d-lg-none">
                                    <label class="fs-6 fw-bold d-lg-none">{{$t('report.time_interval')}}:</label>
                                    <label class="fs-6 d-lg-none">{{$t(`report.${report.interval}`)}}</label>
                                </div>
                                <label class="fs-6 w-100 text-center d-none d-lg-block">{{$t(`report.${report.interval}`)}}</label>
                            </div>
                            <div class="col-12 d-lg-none mt-2 mb-2" style="border-bottom: 0.25px solid black;"></div>
                            <div class="col-12 col-lg-4 ">
                                <div class="d-lg-none">
                                    <label class="fs-6 fw-bold d-lg-none">{{$t('report.time')}}:</label>
                                    <label class="fs-6 d-lg-none">{{report.time}}</label>
                                </div>
                                <label class="fs-6 w-100 text-center d-none d-lg-block">{{report.time}}</label>
                            </div>
                            <div class="col-12 col-lg-2 ">
                                <div class="d-lg-none d-flex">
                                    <label class="fs-6 fw-bold d-lg-none">{{$t('預覽')}}:</label>
                                    <button class="btn btn-success ms-1" @click="download(report.ID, report.filename)">{{$t('預覽')}}</button>
                                </div>
                                <button class="d-none d-lg-block btn btn-success position-relative top-50 start-50 translate-middle" @click="download(report.ID, report.filename)">{{$t('預覽')}}</button>
                            </div>
                            <!-- <div class="col-12 d-lg-none mt-2 mb-2" style="border-bottom: 0.25px solid black;"></div> -->
                            
                        </div> 
                    </div>
                </transition>
                <div class="w-100 responsive_table_footer pt-2 pb-2 d-flex justify-content-between justify-content-lg-center"
                v-if="reportScheduleData.length > 0">
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
            </div>
        </div>

        <div class="modal fade" id="modal_schedule">
            <div class="modal-dialog modal-dialog-centered modal-fullscreen-lg-down modal-dialog-scrollable">
                <div class="modal-content">
                    <div class="modal-header">
                        <h5 class="modal-title">{{$t("預覽")}}</h5>
                        <button type="button" class="btn-close" data-bs-dismiss="modal_schedule" aria-label="Close" @click="close_modal"></button>
                    </div>
                    <div class="modal-body">
                        <!-- <iframe :src="uri" width="95%" height="80%"></iframe> -->
                        <div ref="file"></div>
                    </div>
                    <div class="modal-footer">
                        <button type="button" class="btn btn-secondary me-auto" data-bs-dismiss="modal_schedule" @click="close_modal">{{$t("關閉")}}</button>
                        <button class="btn btn-primary" @click="download_active">{{$t("report.download")}}</button>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>

<script>

import {Modal} from 'bootstrap'
let docx = require("docx-preview")
export default {
    name: "reportScheduleTable",
    data(){
        return {
            page_direction: "",
            reportData: [],
            uri: undefined
        }
    },
    props: {
        reportScheduleData:{type: Array, required: true},
        // date_selection: {type: Object, required: true},
        // ID_list: {type: Array, required: true},
        time_interval: {type: String, required: true, default: "day"},
        emptyText: {type: String, default: "無資料"},
        currentPage: {type: Number, required: true},
        totalPage: {type: Number, required: true},
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
        download(ID, filename){
            this.uri = "solar_static/ID_interval_word"+"/"+ID+"/"+this.time_interval+"/"+filename
            fetch(this.uri)
            .then(response => response.blob())
            .then(res => {
                console.log(res)
                docx.renderAsync(res, this.$refs.file)
            })
            this.myModal.show()
        },
        download_active(){
            try{
                this.myModal.hide()
                let link = document.createElement("a")
                document.body.appendChild(link)
                link.href = this.uri
                link.click()
                document.body.removeChild(link)
            }
            catch{
                console.log("no report")
            }
        },
        close_modal(){
            this.myModal.hide()
        }
        
    },
    watch: {
        // date_selection(){
        //     // console.log(this.date_selection.date_list[0])
        //     // console.log(this.date_selection.date_list[1])
        //     // console.log(this.ID_list[0])
        //     // console.log(this.time_interval)
        //     this.get_table_data()
        // }
    },
    mounted() {
        this.pageChange("b")
        this.myModal = new Modal(document.getElementById('modal_schedule'), {backdrop: 'static', keyboard: false})
    }
}
</script>

<style scoped>
@media (min-width: 992px){
    .modal-dialog{
        width: 95vw !important;
        max-width: 95vw !important;
    }
}
</style>