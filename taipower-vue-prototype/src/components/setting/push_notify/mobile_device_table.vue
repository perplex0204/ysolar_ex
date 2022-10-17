<template>
    <div class="col-12 col-lg-12 responsive_table">
        <div style="overflow-y: scroll;">
            <div class="w-100 row responsive_table_header  fw-bold m-0 d-none d-lg-flex flex-nowrap">
                <div class="col-2 text-center">
                    <label class="fs-6">{{$t('setting.push_notify.name')}}</label>
                </div>
                <div class="col-2 text-center">
                    <label class="fs-6">{{$t('setting.push_notify.platform')}}</label>
                </div>
                <div class="col-2 text-center">
                    <label class="fs-6">{{$t('setting.push_notify.model')}}</label>
                </div>
                <div class="col-2 text-center">
                    <label class="fs-6">{{$t('setting.push_notify.last_login_time')}}</label>
                </div>
                <div class="col-2 text-center">
                    <label class="fs-6">{{$t('setting.push_notify.enable_push_notify')}}</label>
                </div>
                <div class="col-2 text-center">
                    <label class="fs-6">{{$t('setting.push_notify.delete_device')}}</label>
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
                            <!-- name -->
                            <div class="col-12 col-lg-2 pt-lg-4 pb-lg-4">
                                <div class="d-flex d-lg-none flex-wrap">
                                    <label class="fs-6 fw-bold">{{$t('setting.push_notify.name')}}</label>
                                    <label class="fs-6 ms-2">{{data.name}}</label>
                                </div>
                                <label class="fs-6 w-100 text-center d-none d-lg-block">{{data.name}}</label>
                            </div>
                            <!-- platform -->
                            <div class="col-12 col-lg-2 pt-lg-4 pb-lg-4">
                                <div class="d-flex d-lg-none">
                                    <label class="fs-6 fw-bold">{{$t('setting.push_notify.platform')}}</label>
                                    <label class="fs-6 ms-2">{{data.platform}}</label>
                                </div>
                                <label class="fs-6 w-100 text-center d-none d-lg-block">{{data.platform}}</label>
                            </div>
                            <!-- model -->
                            <div class="col-12 col-lg-2 pt-lg-4 pb-lg-4">
                                <div class="d-flex d-lg-none">
                                    <label class="fs-6 fw-bold">{{$t('setting.push_notify.model')}}</label>
                                    <label class="fs-6 ms-2">{{data.model}}</label>
                                </div>
                                <label class="fs-6 w-100 text-center d-none d-lg-block">{{data.model}}</label>
                            </div>
                            <!-- last_login_time -->
                            <div class="col-12 col-lg-2 pt-lg-4 pb-lg-4">
                                <div class="d-flex d-lg-none">
                                    <label class="fs-6 fw-bold">{{$t('setting.push_notify.last_login_time')}}</label>
                                    <label class="fs-6 ms-2">{{data.last_login_time}}</label>
                                </div>
                                <label class="fs-6 w-100 text-center d-none d-lg-block">{{data.last_login_time}}</label>
                            </div>
                            <!-- enable_push_notify -->
                            <div class="col-12 col-lg-2 pt-lg-4 pb-lg-4">
                                <label class="fs-6 fw-bold d-lg-none">{{$t('setting.push_notify.enable_push_notify')}}</label>
                                <div class="d-flex justify-content-center align-items-center w-100">
                                    <el-switch v-model="data.enable_push_notify"
                                    @change="update_enable_push_notify(data._id, data.enable_push_notify)"
                                    :disabled="!userEnablePushNotify" />
                                </div>
                            </div>
                            <!-- delete_device -->
                            <div class="col-12 col-lg-2 pt-lg-4 pb-lg-4">
                                <label class="fs-6 fw-bold d-lg-none">{{$t('setting.push_notify.delete_device')}}</label>
                                <div class="d-flex justify-content-center align-items-center w-100">
                                    <button class="btn" @click="delete_device(data._id)"><i class="fa-solid fa-trash"></i></button>
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
    </div>
</template>
<script>

export default {
    name: "Mobile_device_table",
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
        },
        userEnablePushNotify: {
            type: Boolean,
            default: true
        }
    },
    data(){
        return {
            page_direction: 'to',
            my_table_data:[]
        }
    },
    emits: ['reload-table', 'page-change'],
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
        delete_device(ID){
            const answer = confirm(this.$i18n.t('setting.push_notify.ask_delete_device'))
            if(answer){
                this.axios.post('/my_mobile_device', {
                    ID: ID,
                    mode: 'delete_device'
                }).then(data=>{
                    this.$emit('reload-table')
                })
            }
        },
        update_enable_push_notify(ID, enable){
            this.axios.post('/my_mobile_device', {
                ID: ID,
                mode: 'update_enable_push_notify',
                data: enable
            }).then(data=>{
                this.$emit('reload-table')
            })
        }
    },
    watch: {
        tableData(){
            this.my_table_data = this.tableData
        }
    }
}
</script>