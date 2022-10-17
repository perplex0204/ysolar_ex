<template>
    <div>
        <div class="d-flex flex-wrap align-items-center">
            <h5 class="mb-0"><i class="icon-wrench text-primary"></i>{{$t('dispatch.合併工單')}}</h5>
            <div class="ms-auto">
                <el-popover
                    placement="bottom"
                    :width="200"
                    trigger="click"
                    v-if="!disable"
                >
                    <template #reference>
                        <el-button>{{$t('dispatch.已選取')}}{{Object.keys(this.dispatch_selected).length}}{{$t('則工單')}}</el-button>
                    </template>
                    <div class="d-flex align-items-center pt-2 pb-2" v-for="(dispatch, _id) in dispatch_selected" :key="_id" style="border-bottom: .5px solid black;">
                        {{$t('dispatch.單號')}}：{{`${dispatch.name}`}}
                        <button class="btn ms-auto" @click="removeDispatch(_id)"><i class="fas fa-trash"></i></button> 
                    </div>
                </el-popover>
            </div>
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
                        <div class="col-2 text-center" v-if="mode != 'not_meet_priority'">
                            <label class="fs-6">{{$t('dispatch.預估成本')}}</label>
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
                                v-for="data in tableData" :key="data._id" @click="dispatch_choose(data)"
                                :class="{'select': Object.keys(this.dispatch_selected).includes(data._id)}">
                                    <div class="col-12 d-lg-none mt-2"></div>
                                    <div class="col-12 col-lg-2 ">
                                        <div class="d-flex d-lg-none">
                                            <label class="fs-6 fw-bold">{{$t('dispatch.廠區')}}：</label>
                                            <label class="fs-6">{{data.place}}</label>
                                        </div>
                                        <label class="fs-6 w-100 text-center d-none d-lg-block">{{data.place}}</label>
                                    </div>
                                    <div class="col-12 col-lg-3 ">
                                        <div class="d-lg-none">
                                            <label class="fs-6 fw-bold d-lg-none">{{$t('dispatch.單號')}}：</label>
                                            <label class="fs-6 d-lg-none">{{data.name}}</label>
                                        </div>
                                        <label class="fs-6 w-100 text-center d-none d-lg-block">{{data.name}}</label>
                                    </div>
                                    <div class="col-12 col-lg-2 ">
                                        <div class="d-lg-none">
                                            <label class="fs-6 fw-bold d-lg-none">{{$t('dispatch.派工日期')}}：</label>
                                            <label class="fs-6 d-lg-none">{{data.dispatch_time}}</label>
                                        </div>
                                        <label class="fs-6 w-100 text-center d-none d-lg-block">{{data.dispatch_time}}</label>
                                    </div>
                                    <div class="col-12 col-lg-2 ">
                                        <div class="d-lg-none">
                                            <label class="fs-6 fw-bold d-lg-none">{{$t('dispatch.類別')}}：</label>
                                            <label class="fs-6 d-lg-none">{{$t(`dispatch.type["${data.type}"]`)}}</label>
                                        </div>
                                        <label class="fs-6 w-100 text-center d-none d-lg-block">{{$t(`dispatch.type["${data.type}"]`)}}</label>
                                    </div>
                                    <div class="col-12 col-lg-2 ">
                                        <div class="d-lg-none">
                                            <label class="fs-6 fw-bold d-lg-none">{{$t('dispatch.狀態')}}：</label>
                                            <label class="fs-6 d-lg-none">{{$t(`dispatch.stage["${data.stage}"]`)}}</label>
                                        </div>
                                        <label class="fs-6 w-100 text-center d-none d-lg-block">{{$t(`dispatch.stage["${data.stage}"]`)}}</label>
                                    </div>
                                    <div class="col-12 col-lg-2">
                                        <div class="d-lg-none">
                                            <label class="fs-6 fw-bold d-lg-none">{{$t('dispatch.預估成本')}}：</label>
                                            <label class="fs-6 d-lg-none">{{data.predict_dispatch_cost}}</label>
                                        </div>
                                        <label class="fs-6 w-100 text-center d-none d-lg-block">{{data.predict_dispatch_cost}}</label>
                                    </div>
                                    <div class="col-12 col-lg-4 ">
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
        mergeObj: {
            type: Object,
            default: ()=>{
                return {}
            }
        }
    },
    emits: ['row-dblclick', 'dispatch-selected'],
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
            dispatch_selected: {},
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
        dispatch_choose(dispatch){
            //console.log(dispatch)
            if(this.disable){
                return false
            }
            if(Object.keys(this.dispatch_selected).includes(dispatch._id)){
                delete this.dispatch_selected[dispatch._id]
                this.emit_dispatch_selected()
                return false
            }
            if(this.$parent.dispatch_date == null && dispatch.dispatch_time != null){
                const answer = confirm(this.$i18n.t('dispatch["merge_dispatch_date_not_set_warning"]'))
                if(answer){
                    this.$parent.dispatch_date = dispatch.dispatch_time.substring(0,10)
                }
                else return false
            }
            let that = this
            window.setTimeout(()=>{
                that.dispatch_selected[dispatch._id] = dispatch
                that.emit_dispatch_selected()
            }, 100)
        },
        emit_dispatch_selected(){
            console.log(this.dispatch_selected)
            this.$emit('dispatch-selected', this.dispatch_selected)
        },
        removeDispatch(_id){
            delete this.dispatch_selected[_id]
        },
        //-----------------------------------------------------------------------------
        get_dispatch_overview(){
            this.axios.post('/get_dispatch_overview',{
                ID: this.stationId,
                dispatch_time: this.dispatchDate,
                stage: 'wait_for_take',
                no_merge: true
            }).then(data => {
                //console.log(data.data.data)
                this.tableData = data.data.data.dispatch_list
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