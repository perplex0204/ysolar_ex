<template>
    <div class="col-12 col-lg-12 responsive_table">
        <div class="reponsive_table_wrapper">
            <div class="w-100 row responsive_table_header  fw-bold m-0 d-none d-lg-flex flex-nowrap">
                <div class="col-2 text-center">
                    <label class="fs-6">{{$t('alarm.廠區')}}</label>
                </div>
                <div class="col-1 text-center">
                    <label class="fs-6">{{$t('alarm.警報類型')}}</label>
                </div>
                <div class="col-2 text-center">
                    <label class="fs-6">{{$t('alarm.設備類型')}}</label>
                </div>
                <div class="col-2 text-center">
                    <label class="fs-6">{{$t('alarm.設備名稱')}}</label>
                </div>
                <div class="col-4 text-center">
                    <label class="fs-6">{{$t('alarm.警報名稱')}}</label>
                </div>
                <div class="col-4 text-center" v-if="type=='table'">
                    <label class="fs-6">{{$t('alarm.派工單號')}}</label>
                </div>
                <div class="col-2 text-center">
                    <label class="fs-6">{{$t('alarm.警報發生')}}</label>
                </div>
                <div class="col-2 text-center">
                    <label class="fs-6">{{$t('alarm.警報確認')}}</label>
                </div>
                <div class="col-2 text-center">
                    <label class="fs-6">{{$t('alarm.警報修復')}}</label>
                </div>
                <div class="col-1 text-center" v-if="alarmToolsEnable">
                    
                </div>     
            </div>
            <div class="w-100 pt-2 pb-2 text-center" v-if="alarmData.length == 0">
                {{$t(emptyText)}}
            </div>
            <transition mode="out-in" :name="page_direction == 'to' ? 'table_animation_to':'table_animation_back'">
                <div class="w-100 responsive_table_body" :key="currentPage">
                        <div class="row m-0 responsive_table_content mt-2 mt-lg-0" v-for="alarm in alarmData" :key="alarm._id" 
                        @click="$emit('row-click', alarm)" 
                        :class="{'select': selectEnable && alarm._id in selectAlarm, 'hover': hoverEnable}">
                            <div class="col-12 d-lg-none mt-2"></div>
                            <div class="col-12 col-lg-2 ">
                                <div class="d-flex d-lg-none flex-wrap">
                                    <label class="fs-6 fw-bold">{{$t('alarm.廠區')}}：</label>
                                    <label class="fs-6">{{alarm.alarm_place}}</label>
                                    <div class="d-flex justify-content-center ms-auto">
                                        <div v-if="alarm.level == 1">
                                            <i class="fas fa-exclamation-triangle text-danger"></i>
                                            <label class="fs-7">{{'level.1'}}</label>
                                        </div>
                                        <div v-if="alarm.level == 2">
                                            <i class="fas fa-exclamation-circle text-warning"></i>
                                            <label class="fs-7">{{$t('level.2')}}</label>
                                        </div>
                                        <div v-if="alarm.level == 3">
                                            <i class="fas fa-times-circle text-secondary"></i>
                                            <label class="fs-7">{{$t('level.3')}}</label>
                                        </div>
                                    </div>
                                </div>
                                <label class="fs-6 w-100 text-center d-none d-lg-block">{{alarm.alarm_place}}</label>
                            </div>
                            <div class="col-12 col-lg-1 ">
                                <div class="d-lg-none">
                                    <label class="fs-6 fw-bold d-lg-none">{{$t('alarm.警報類型')}}：</label>
                                    <label class="fs-6 d-lg-none">{{alarm.alarm_group}}</label>
                                </div>
                                <label class="fs-6 w-100 text-center d-none d-lg-block">{{alarm.alarm_group}}</label>
                            </div>
                            <div class="col-12 d-lg-none mt-2 mb-2" style="border-bottom: 0.25px solid black;"></div>
                            <div class="col-12 col-lg-2 ">
                                <div class="d-lg-none">
                                    <label class="fs-6 fw-bold d-lg-none">{{$t('alarm.設備類型')}}：</label>
                                    <label class="fs-6 d-lg-none">{{alarm.equip_type}}</label>
                                </div>
                                <label class="fs-6 w-100 text-center d-none d-lg-block">{{alarm.equip_type}}</label>
                            </div>
                            <div class="col-12 col-lg-2 ">
                                <div class="d-lg-none">
                                    <label class="fs-6 fw-bold d-lg-none">{{$t('alarm.設備名稱')}}：</label>
                                    <label class="fs-6 d-lg-none">{{alarm.equip_name}}</label>
                                </div>
                                <label class="fs-6 w-100 text-center d-none d-lg-block">{{alarm.equip_name}}</label>
                            </div>
                            <div class="col-12 col-lg-4 text-center dblclickStyle" @dblclick="$emit('row-dblclick', alarm)">
                                <div class="d-flex d-lg-block w-100">
                                    <label class="fs-6 fw-bold d-lg-none ">{{$t('alarm.警報名稱')}}：</label>
                                    <div>
                                        <div class="d-none d-lg-flex justify-content-center dblclickStyle">
                                            <div v-if="alarm.level == 1">
                                                <i class="fas fa-exclamation-triangle text-danger"></i>
                                                <label class="fs-7 dblclickStyle">{{$t('level.1')}}</label>
                                            </div>
                                            <div v-if="alarm.level == 2">
                                                <i class="fas fa-exclamation-circle text-warning"></i>
                                                <label class="fs-7 dblclickStyle">{{$t('level.2')}}</label>
                                            </div>
                                            <div v-if="alarm.level == 3">
                                                <i class="fas fa-times-circle text-secondary"></i>
                                                <label class="fs-7 dblclickStyle">{{$t('level.3')}}</label>
                                            </div>
                                        </div>
                                        <label class="fs-6 dblclickStyle">{{alarm.alarm_event}}</label>
                                    </div>
                                </div>
                            </div>
                            <div class="col-12 col-lg-4 text-center dblclickStyle" @dblclick="$emit('open-dispatch', alarm)" v-if="type=='table'">
                                <div class="d-flex d-lg-block w-100">
                                    <label class="fs-6 fw-bold d-lg-none ">{{$t('alarm.派工單號')}}：</label>
                                    <div>                        
                                        <label>{{alarm.dispatch_name != null ? alarm.dispatch_name : ""}}</label>
                                    </div>
                                </div>
                            </div>
                            <div class="col-12 d-lg-none mt-2 mb-2" style="border-bottom: 0.25px solid black;"></div>
                            <div class="col-12 col-lg-2 ">
                                <div class="d-lg-none">
                                    <label class="fs-6 fw-bold d-lg-none">{{$t('alarm.警報發生')}}：</label>
                                    <label class="fs-6 d-lg-none">{{alarm.time}}</label>
                                </div>
                                <label class="fs-6 w-100 text-center d-none d-lg-block">{{alarm.time}}</label>
                            </div>
                            <div class="col-12 col-lg-2 ">
                                <div class="d-lg-none mb-2">
                                    <label class="fs-6 fw-bold d-lg-none">{{$t('alarm.警報確認')}}：</label>
                                    <label class="fs-6 d-lg-none">{{alarm.checktime}}</label>
                                </div>
                                <label class="fs-6 w-100 text-center d-none d-lg-block">{{alarm.checktime}}</label>
                            </div>
                            <div class="col-12 col-lg-2 ">
                                <div class="d-lg-none mb-2">
                                    <label class="fs-6 fw-bold d-lg-none">{{$t('alarm.警報修復')}}：</label>
                                    <label class="fs-6 d-lg-none">{{alarm.returntime}}</label>
                                </div>
                                <label class="fs-6 w-100 text-center d-none d-lg-block">{{alarm.returntime}}</label>
                            </div>
                            <div class="col-12 col-lg-1" v-if="alarmToolsEnable">
                                <div class="d-none d-lg-block">
                                    <el-popover placement="left" :width="'auto'" trigger="click">
                                        <template #reference>
                                            <i class="fas fa-ellipsis-h"></i>
                                        </template>
                                        <div class="d-flex btn text-dark" @click="handleTools(alarm._id, 'check')"><i class="icon-addperson"></i>{{$t('alarm.警報確認')}}</div>
                                        <div class="d-flex btn text-dark" @click="handleTools(alarm._id, 'manual_return')"><i class="icon-configline"></i>{{$t('alarm.手動復歸')}}</div>
                                        <div class="d-flex btn text-dark" @click="handleTools(alarm._id, 'archived')"><i class="icon-save"></i>{{$t('alarm.警報歸檔')}}</div>
                                    </el-popover>
                                </div>
                                <div class="d-lg-none d-flex justify-content-between">
                                    <div class="d-flex btn" @click="handleTools(alarm._id, 'check')"><i class="icon-addperson"></i>{{$t('alarm.警報確認')}}</div>
                                    <div class="d-flex btn" @click="handleTools(alarm._id, 'manual_return')"><i class="icon-configline"></i>{{$t('alarm.手動復歸')}}</div>
                                    <div class="d-flex btn" @click="handleTools(alarm._id, 'archived')"><i class="icon-save"></i>{{$t('alarm.警報歸檔')}}</div>
                                </div>
                            </div>
                        </div>
                </div>
            </transition>
        </div>
        <div class="w-100 responsive_table_footer pt-2 pb-2 d-flex justify-content-between justify-content-lg-center"
        v-if="alarmData.length > 0">
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
    name: 'AlarmTable',
    data(){
        return {
            page_direction: 'to'
        }
    },
    props: {
        alarmData: {
            type: Array,
            required: true,
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
        },
        selectEnable: {
            type: Boolean,
            default: false
        },
        hoverEnable: {
            type: Boolean,
            default: false
        },
        selectAlarm: {
            type: Object,
            default: function(){
                return {}
            }
        },
        alarmToolsEnable: {
            type: Boolean,
            default: true
        },
        type: {
            type: String,
            default: "table"
        }
    },
    emits: ['row-dblclick', 'open-dispatch'],
    methods: {
        handleTools(_id, type){
            this.$emit('handle-alarm', _id, type)
        },
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
        }
    },
}
</script>

<style scoped>
.dblclickStyle:hover{
    cursor: pointer;
}
</style>