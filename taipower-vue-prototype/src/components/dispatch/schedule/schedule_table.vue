<template>
    <div class="col-12 col-lg-12 responsive_table">
        <div style="overflow-y: scroll;">
            <div class="w-100 row responsive_table_header  fw-bold m-0 d-none d-lg-flex flex-nowrap">
                <div class="col-2 text-center">
                    <label class="fs-6">{{$t('dispatch.廠區')}}</label>
                </div>
                <div class="col-3 text-center">
                    <label class="fs-6">{{$t('dispatch.名稱')}}</label>
                </div>
                <div class="col-2 text-center">
                    <label class="fs-6">{{$t('dispatch.類別')}}</label>
                </div>
                <div class="col-2 text-center">
                    <label class="fs-6">{{$t('dispatch.排程')}}</label>
                </div>
                <div class="col-4 text-center">
                    <label class="fs-6">{{$t('dispatch.下次日程')}}</label>
                </div>
            </div>
            <div class="w-100 pt-2 pb-2 text-center" v-if="tableData.length == 0">
                {{$t(emptyText)}}
            </div>
            <transition mode="out-in" :name="page_direction == 'to' ? 'table_animation_to':'table_animation_back'">
                <div class="w-100 responsive_table_body" :key="currentPage">
                        <div class="row m-0 responsive_table_content mt-2 mt-lg-0 pt-2 pb-3 p-lg-0 hover" 
                        v-for="data in tableData" :key="data._id" @click="$emit('row-dblclick', data)">
                            <div class="col-12 d-lg-none mt-2"></div>
                            <div class="col-12 col-lg-2 pt-lg-4 pb-lg-4">
                                <div class="d-flex d-lg-none">
                                    <label class="fs-6 fw-bold">{{$t('dispatch.廠區')}}：</label>
                                    <label class="fs-6">{{data.place}}</label>
                                </div>
                                <label class="fs-6 w-100 text-center d-none d-lg-block">{{data.place}}</label>
                            </div>
                            <div class="col-12 col-lg-3 pt-lg-4 pb-lg-4">
                                <div class="d-lg-none">
                                    <label class="fs-6 fw-bold d-lg-none">{{$t('dispatch.名稱')}}：</label>
                                    <label class="fs-6 d-lg-none">{{data.name}}</label>
                                </div>
                                <label class="fs-6 w-100 text-center d-none d-lg-block">{{data.name}}</label>
                            </div>
                            <div class="col-12 col-lg-2 pt-lg-4 pb-lg-4">
                                <div class="d-lg-none">
                                    <label class="fs-6 fw-bold d-lg-none">{{$t('dispatch.類別')}}：</label>
                                    <label class="fs-6 d-lg-none">{{$t(`dispatch["${data.schedule_type}"]`)}}</label>
                                </div>
                                <label class="fs-6 w-100 text-center d-none d-lg-block">{{$t(`dispatch["${data.schedule_type}"]`)}}</label>
                            </div>
                            <div class="col-12 col-lg-2 pt-lg-4 pb-lg-4">
                                <div class="d-lg-none">
                                    <label class="fs-6 fw-bold d-lg-none">{{$t('dispatch.排程')}}：</label>
                                    <label class="fs-6 d-lg-none">{{data.repeat_interval_format}}</label>
                                </div>
                                <label class="fs-6 w-100 text-center d-none d-lg-block">{{data.repeat_interval_format}}</label>
                            </div>
                            <div class="col-12 col-lg-4 pt-lg-4 pb-lg-4">
                                <div class="d-lg-none">
                                    <label class="fs-6 fw-bold d-lg-none">下次日期：</label>
                                    <label class="fs-6 d-lg-none">{{data.next_dispatch}}</label>
                                </div>
                                <label class="fs-6 w-100 text-center d-none d-lg-block">{{data.next_dispatch}}</label>
                            </div>
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
    </div>
</template>
<script>
export default {
    name: "Schedule_table",
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
    emits: ['row-dblclick', 'page-change'],
    data(){
        return {
            page_direction: 'to'
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
    }
}
</script>