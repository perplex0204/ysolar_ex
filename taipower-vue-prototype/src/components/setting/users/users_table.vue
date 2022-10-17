<template>
    <div class="col-12 col-lg-12 responsive_table">
        <div style="overflow-y: scroll;">
            <div class="w-100 row responsive_table_header  fw-bold m-0 d-none d-lg-flex flex-nowrap">
                <div class="col-3 text-center">
                    <label class="fs-6">{{$t('setting.users.username')}}</label>
                </div>
                <div class="col-3 text-center">
                    <label class="fs-6">{{$t('setting.users.account_level')}}</label>
                </div>
                <div class="col-4 text-center">
                    <label class="fs-6">{{$t('setting.users.plant_access')}}</label>
                </div>
                <div class="col-2 text-center">
                    <label class="fs-6">{{$t('setting.users.more_info')}}</label>
                </div>
            </div>
            <div class="w-100 pt-2 pb-2 text-center" v-if="my_table_data.length == 0">
                {{$t(emptyText)}}
            </div>
            <transition mode="out-in" :name="page_direction == 'to' ? 'table_animation_to':'table_animation_back'">
                <div class="w-100 responsive_table_body" :key="currentPage">
                        <div class="row m-0 responsive_table_content mt-2 mt-lg-0 pt-2 pb-3 p-lg-0" 
                        v-for="data in my_table_data" :key="data._id">
                            <div class="col-12 d-lg-none mt-2"></div>
                            <div class="col-12 col-lg-3 pt-lg-4 pb-lg-4">
                                <div class="d-flex d-lg-none">
                                    <label class="fs-6 fw-bold">{{$t('setting.users.username')}}：</label>
                                    <label class="fs-6">{{data.username}}</label>
                                </div>
                                <label class="fs-6 w-100 text-center d-none d-lg-block">{{data.username}}</label>
                            </div>
                            <div class="col-12 col-lg-3 pt-lg-4 pb-lg-4">
                                <label class="fs-6 fw-bold d-lg-none">{{$t('setting.users.account_level')}}</label>
                                <div class="d-flex w-100 algin-items-center justify-content-start justify-content-lg-center flex-column">
                                    <el-select v-model="data.level" size="large" :disabled="data.level >= 3 && $store.state.user_data.is_superuser == false"
                                        @change="$emit('update-user-data', data._id, 'level', data.level)">
                                        <el-option :value="1" :label="`1 ${$t('setting.users.level.1')}`"/>
                                        <el-option :value="2" :label="`2 ${$t('setting.users.level.2')}`"/>
                                        <el-option :value="3" :label="`3 ${$t('setting.users.level.3')}`"/>
                                    </el-select>
                                    <label v-if="$store.state.user_data.is_superuser && data.pageType != $store.state.user_data.pageType" class="fs-7">{{`pageType: ${data.pageType}`}}</label>
                                </div>
                            </div>
                            <div class="col-12 col-lg-4 pt-lg-4 pb-lg-4">
                                <label class="fs-6 fw-bold d-lg-none">{{$t('setting.users.plant_access')}}</label>                                    
                                <div class="d-flex w-100 algin-items-center justify-content-start justify-content-lg-center">
                                    <div class="col-lg-6 col-12">
                                        <plant-access-popover :user-data="data" 
                                            @update_plant="new_plant => $emit('update-user-data', data._id, 'plant', new_plant)"></plant-access-popover>
                                    </div>
                                </div>
                            </div>
                            <div class="col-12 col-lg-2 pt-lg-4 pb-lg-4">
                                <label class="fs-6 fw-bold d-lg-none">{{$t('setting.users.more_info')}}</label>
                                <div class="d-flex justify-content-center align-items-center w-100">
                                    <button class="btn" @click="open_modal(data)"><i class="fas fa-ellipsis-h"></i></button>
                                </div>
                            </div>
                        </div>
                </div>
            </transition>
        </div>
        <div class="w-100 responsive_table_footer pt-2 pb-2 d-flex justify-content-between justify-content-lg-center"
        v-if="my_table_data.length > 0">
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
        <info-modal ref="info_modal" @reload-table="$emit('reload-table')"></info-modal>
    </div>
</template>
<script>
import infoModal from './user_info_modal.vue'
import plantAccessPopover from './plant_access_popover.vue'

export default {
    name: "Users_table",
    components: {
        infoModal,
        plantAccessPopover
    },
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
    data(){
        return {
            page_direction: 'to',
            my_table_data:[]
        }
    },
    emits: ['reload-table', 'update-user-data', 'page-change'],
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
        open_modal(data){
            this.$refs.info_modal.open_modal(data)
        }
    },
    watch: {
        tableData(){
            this.my_table_data = this.tableData
        }
    }
}
</script>