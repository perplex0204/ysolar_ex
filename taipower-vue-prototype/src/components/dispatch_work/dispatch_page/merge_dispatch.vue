<template>
    <div>
        <div>
            <div class="d-flex">
                <button class="btn btn-warning"
                @click="finish">
                    <i class="fa-solid fa-angle-left"></i>
                </button>
            </div>
            <div class="col-12 mt-3">
                <div class="card p-2 pt-4">
                    <div class="d-flex align-items-center">
                        <h5 class="mb-0"><i class="icon-wrench text-primary"></i>{{$t('dispatch.合併工單')}}</h5>
                    </div>
                    <div class="mt-3">
                        <div class="col-12 col-lg-12 responsive_table">
                            <div style="overflow-y: scroll;">
                                <div class="w-100 row responsive_table_header  fw-bold m-0 d-none d-lg-flex flex-nowrap">
                                    <div class="col-2 text-center">
                                        <label class="fs-6">{{$t('dispatch.廠區')}}</label>
                                    </div>
                                    <div class="col-3 text-center">
                                        <label class="fs-6">{{$t('dispatch.單號')}}</label>
                                    </div>
                                    <div class="col-2 text-center">
                                        <label class="fs-6">{{$t('dispatch.派工日期')}}</label>
                                    </div>
                                    <div class="col-2 text-center">
                                        <label class="fs-6">{{$t('dispatch.類別')}}</label>
                                    </div>
                                    <div class="col-2 text-center">
                                        <label class="fs-6">{{$t('dispatch.狀態')}}</label>
                                    </div>
                                    <div class="col-2 text-center">
                                        <label class="fs-6">{{$t('dispatch.預估維運成本')}}</label>
                                    </div>
                                    <div class="col-4 text-center">
                                        <label class="fs-6">{{$t('dispatch.維運人員')}}</label>
                                    </div>
                                </div>
                                <div class="w-100 pt-2 pb-2 text-center" v-if="tableData.length == 0">
                                    {{$t(emptyText)}}
                                </div>
                                <transition mode="out-in" :name="page_direction == 'to' ? 'table_animation_to':'table_animation_back'">
                                    <div class="w-100 responsive_table_body" :key="currentPage">
                                            <div class="row m-0 responsive_table_content mt-2 mt-lg-0 pt-2 pb-3 p-lg-0 hover" 
                                            v-for="data in tableData" :key="data._id" @click="dispatch_choose(data)">
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
                                                        <label class="fs-6 fw-bold d-lg-none">{{$t('dispatch.單號')}}：</label>
                                                        <label class="fs-6 d-lg-none">{{data.name}}</label>
                                                    </div>
                                                    <label class="fs-6 w-100 text-center d-none d-lg-block">{{data.name}}</label>
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
                                                        <label class="fs-6 fw-bold d-lg-none">{{$t('dispatch.類別')}}：</label>
                                                        <label class="fs-6 d-lg-none">{{$t(`dispatch.type["${data.type}"]`)}}</label>
                                                    </div>
                                                    <label class="fs-6 w-100 text-center d-none d-lg-block">{{$t(`dispatch.type["${data.type}"]`)}}</label>
                                                </div>
                                                <div class="col-12 col-lg-2 pt-lg-4 pb-lg-4">
                                                    <div class="d-lg-none">
                                                        <label class="fs-6 fw-bold d-lg-none">{{$t('dispatch.狀態')}}：</label>
                                                        <label class="fs-6 d-lg-none">{{$t(`dispatch.stage["${data.stage}"]`)}}</label>
                                                    </div>
                                                    <label class="fs-6 w-100 text-center d-none d-lg-block">{{$t(`dispatch.stage["${data.stage}"]`)}}</label>
                                                </div>
                                                <div class="col-12 col-lg-2 pt-lg-4 pb-lg-4">
                                                    <div class="d-lg-none">
                                                        <label class="fs-6 fw-bold d-lg-none">{{$t('dispatch.預估維運成本')}}：</label>
                                                        <label class="fs-6 d-lg-none">{{data.predict_dispatch_cost}}</label>
                                                    </div>
                                                    <label class="fs-6 w-100 text-center d-none d-lg-block">{{data.predict_dispatch_cost}}</label>
                                                </div>
                                                <div class="col-12 col-lg-4 pt-lg-4 pb-lg-4">
                                                    <div class="d-lg-none">
                                                        <label class="fs-6 fw-bold d-lg-none">{{$t('dispatch.維運人員')}}：</label>
                                                        <label class="fs-6 d-lg-none">{{data.maintainer_data.name}}</label>
                                                    </div>
                                                    <label class="fs-6 w-100 text-center d-none d-lg-block">{{data.maintainer_data.name}}</label>
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
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>
<script>

export default {
    name: "Merge_dispatch",
    props: {
        emptyText: {
            type: String,
            default: "無資料"
        },
        disable: {
            type: Boolean,
            default: false
        },
        stationId: {
            default: null
        },
        dispatchDate: {
            defult: null
        },
        dispatchId: {
            default: null
        }
    },
    emits: ['dispatch-edit-finish'],
    data(){
        return {
            page_direction: 'to',
            // Merge Dispatch Table
            tableData: [
                /* {
                    "_id": "1234",
                    "ID": "4567",
                    "place": "上萬安段/地號4",
                    "name": "20220101-A",
                    "type": "告警檢修",
                    "status": "已派工",
                    "time": "2022-02-28 12:00:00",
                    "maintainer_data": {
                        name: "王大明"
                    }
                } */
            ],
            currentPage: 1,
            totalPage: 1,
        }
    },
    methods: {
        finish(){
            this.$emit('dispatch-edit-finish')
        },
        pageChange(type){
            switch(type){
                case "bb":
                    this.page_direction = "back"
                    if(this.currentPage > 10)
                        this.currentPage -= 10
                    else
                        this.currentPage = 1
                    this.get_dispatch_overview()
                    break
                case "b":
                    this.page_direction = "back"
                    if(this.currentPage > 1)
                        this.currentPage -= 1
                    else
                        this.currentPage = 1
                    this.get_dispatch_overview()
                    break
                case "ff":
                    this.page_direction = "to"
                    if(this.currentPage < this.totalPage - 10)
                        this.currentPage += 10
                    else
                        this.currentPage = this.totalPage
                    this.get_dispatch_overview()
                    break
                case "f":
                    this.page_direction = "to"
                    if(this.currentPage < this.totalPage)
                        this.currentPage += 1
                    this.get_dispatch_overview()
                    break
            }
        },
        dispatch_choose(dispatch){
            const answer = confirm(this.$i18n.t('dispatch["merge_dispatch_ask"]'))
            if(answer){
                this.axios.post('/dispatch_merge_dispatch', {
                    dispatch_ID: this.dispatchId,
                    merge_ID: dispatch._id
                }).then(data => {
                    this.$emit('dispatch-edit-finish')
                })
            }
            else{
                return false
            }
        },
        //-----------------------------------------------------------------------------
        get_dispatch_overview(){
            this.axios.post('/get_dispatch_overview',{
                ID: this.stationId,
                dispatch_ID: this.dispatchId,
                dispatch_time: this.dispatchDate,
                dispatch_time_none: true,
                stage: ['wait_for_take', 'wait_for_priority'],
                page: this.currentPage,
                no_merge: true
            }).then(data => {
                //console.log(data.data.data)
                this.tableData = data.data.data.dispatch_list
                this.totalPage = data.data.data.total_page
            })
        }
    },
    mounted(){
        this.get_dispatch_overview()
        this.dispatch_selected = this.mergeObj
    },
    watch: {
        disable(){
            if(this.disable){
                this.tableData = []
                for(var _id in this.dispatch_selected){
                    this.tableData.push(this.dispatch_selected[_id])
                }
            }
        },
        dispatchDate(){
            this.get_dispatch_overview()
        }
    }
}
</script>