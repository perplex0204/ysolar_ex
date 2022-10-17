<template>
    <div class="col-12 col-lg-12 responsive_table">
        <div style="overflow-y: scroll;">
            <div class="w-100 row responsive_table_header  fw-bold m-0 d-none d-lg-flex flex-nowrap">
                <div class="col-2 text-center">
                    <label class="fs-6">{{$t('report.download')}}</label>
                </div>
                <div class="col-2 text-center">
                    <label class="fs-6">{{$t('dispatch.廠區')}}</label>
                </div>
                <div class="col-3 text-center">
                    <label class="fs-6">{{$t('dispatch.單號')}}</label>
                </div>
                <div class="col-2 text-center">
                    <label class="fs-6">{{$t('dispatch.類別')}}</label>
                </div>
                <div class="col-2 text-center">
                    <label class="fs-6">{{$t('dispatch.派工日期')}}</label>
                </div>
                <div class="col-2 text-center">
                    <label class="fs-6">{{$t('dispatch.預估成本')}}</label>
                </div>
                <div class="col-4 text-center">
                    <label class="fs-6">{{$t('dispatch.維運人員')}}</label>
                </div>
                <!-- <div class="col-2 text-center">
                    <label class="fs-6">{{$t('report.download')}}</label>
                </div> -->
            </div>
            <div class="w-100 pt-2 pb-2 text-center" v-if="tableData.length == 0">
                {{$t(emptyText)}}
            </div>
            <transition mode="out-in" :name="page_direction == 'to' ? 'table_animation_to':'table_animation_back'">
                <div class="w-100 responsive_table_body" :key="currentPage">
                        <div class="row m-0 responsive_table_content mt-2 mt-lg-0 pt-2 pb-3 p-lg-0 hover" 
                        v-for="data in tableData" :key="data._id" @click="$emit('row-click', data)">
                            <div class="col-12 d-lg-none mt-2"></div>
                            <div class="col-12 col-lg-2 pt-lg-4 pb-lg-4">
                                <div class="d-lg-none d-flex">
                                    <label class="fs-6 fw-bold d-lg-none">{{$t('report.download')}}:</label>
                                    <button class="btn btn-success ms-1" @click.stop="download(data)">{{$t("預覽")}}</button>
                                </div>
                                <button class="d-none d-lg-block btn btn-success position-relative top-50 start-50 translate-middle" @click.stop="download(data)">{{$t("預覽")}}</button>
                            </div>
                            <div class="col-12 col-lg-2 pt-lg-4 pb-lg-4">
                                <div class="d-flex d-lg-none">
                                    <label class="fs-6 fw-bold">{{$t('dispatch.廠區')}}：</label>
                                    <label class="fs-6">{{data.place}}</label>
                                </div>
                                <label class="fs-6 w-100 text-center d-none d-lg-block">{{data.place}}</label>
                            </div>
                            <div class="col-12 col-lg-3 pt-lg-4 pb-lg-4">
                                <div class="d-lg-none">
                                    <label class="fs-6 fw-bold d-lg-none">{{$t('dispatch.單號')}}：</label>
                                    <label class="fs-6 d-lg-none">{{data.name}}</label>
                                </div>
                                <label class="fs-6 w-100 text-center d-none d-lg-block">{{data.name}}</label>
                            </div>
                            <div class="col-12 col-lg-2 pt-lg-4 pb-lg-4">
                                <div class="d-lg-none">
                                    <label class="fs-6 fw-bold d-lg-none">{{$t('dispatch.類別')}}：</label>
                                    <label class="fs-6 d-lg-none me-2" v-for="type in data.type"
                                    :key="type">{{$t(`dispatch.type["${type}"]`)}}</label>
                                </div>
                                <div class="w-100">
                                    <label class="fs-6 w-100 text-center d-none d-lg-block" v-for="type in data.type"
                                    :key="type">
                                        {{$t(`dispatch.type["${type}"]`)}}
                                    </label>
                                </div>
                            </div>
                            <div class="col-12 col-lg-2 pt-lg-4 pb-lg-4">
                                <div class="d-lg-none">
                                    <label class="fs-6 fw-bold d-lg-none">{{$t('dispatch.派工日期')}}：</label>
                                    <label class="fs-6 d-lg-none">{{data.dispatch_time}}</label>
                                </div>
                                <label class="fs-6 w-100 text-center d-none d-lg-block">{{data.dispatch_time}}</label>
                            </div>
                            <div class="col-12 col-lg-2 pt-lg-4 pb-lg-4">
                                <div class="d-lg-none">
                                    <label class="fs-6 fw-bold d-lg-none">{{$t('dispatch.預估成本')}}：</label>
                                    <label class="fs-6 d-lg-none">{{data.auto_review_cost}}</label>
                                </div>
                                <label class="fs-6 w-100 text-center d-none d-lg-block">{{data.auto_review_cost}}</label>
                            </div>
                            <div class="col-12 col-lg-4 pt-lg-4 pb-lg-4">
                                <div class="d-lg-none">
                                    <label class="fs-6 fw-bold d-lg-none">{{$t('dispatch.維運人員')}}：</label>
                                    <label class="fs-6 d-lg-none">{{data.maintainer_data.name}}</label>
                                </div>
                                <label class="fs-6 w-100 text-center d-none d-lg-block">{{data.maintainer_data.name}}</label>
                            </div>
                            <!-- <div class="col-12 col-lg-2 pt-lg-4 pb-lg-4">
                                <div class="d-lg-none d-flex">
                                    <label class="fs-6 fw-bold d-lg-none">{{$t('report.download')}}:</label>
                                    <button class="btn btn-success ms-1" @click.stop="download(data)">{{$t("預覽")}}</button>
                                </div>
                                <button class="d-none d-lg-block btn btn-success position-relative top-50 start-50 translate-middle" @click.stop="download(data)">{{$t("預覽")}}</button>
                            </div> -->
                        </div>
                </div>
            </transition>
        </div>
        <div class="w-100 responsive_table_footer pt-2 pb-2 d-flex justify-content-between justify-content-lg-center"
        v-if="tableData.length > 0">
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

        <div class="modal fade" id="modal">
            <div class="modal-dialog modal-dialog-centered modal-fullscreen-lg-down modal-dialog-scrollable">
                <div class="modal-content">
                    <div class="modal-header">
                        <h5 class="modal-title">{{$t("預覽")}}</h5>
                        <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
                    </div>
                    <div class="modal-body">
                        <div ref="file"></div>
                    </div>
                    <div class="modal-footer">
                        <button type="button" class="btn btn-secondary me-auto" data-bs-dismiss="modal">{{$t("關閉")}}</button>
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
    name: "Dispatch_table",
    props: {
        tableData: {
            type: Array,
            required: true
        },
        currentPage: {
            type: Number,
            required: true
        },
        totalPage: {
            type: Number,
            required: true,
        },
        emptyText: {
            type: String,
            default: "無資料"
        }
    },
    emits: ['row-click'],
    data(){
        return {
            page_direction: 'to',
            response: undefined
        }
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
        async download(data){
            let response = await this.axios.post('get_dispatch_report',{ID: data._id}, { responseType: 'blob' })
            if (response.status === 200){
                console.log(response)
                this.myModal.show()
                docx.renderAsync(response.data, this.$refs.file)
                this.response = response
                // that.myModal.show()
            }
            else{
                console.log("Bad Request")
            }
        },
        async download_active(){
            try{
                this.myModal.hide()
                let contentDisposition = this.response.headers["content-disposition"]
                let matches = contentDisposition.split("filename=")
                let filename = "report.docx"
                if (matches != null && matches[1]) {
                    filename = matches[1].replace(/['"]/g, '')
                    filename = decodeURIComponent(filename)
                }

                let obj = [new Blob([this.response.data], {type: ''}), filename]
                let link = document.createElement("a")
                document.body.appendChild(link)
                link.href = URL.createObjectURL(obj[0], {type: ''})
                link.download = obj[1]
                link.click()
                document.body.removeChild(link)
            }
            catch{
                console.log("no report")
            }
        },
    },
    mounted(){
        this.myModal = new Modal(document.getElementById('modal'), {backdrop: 'static', keyboard: false})
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