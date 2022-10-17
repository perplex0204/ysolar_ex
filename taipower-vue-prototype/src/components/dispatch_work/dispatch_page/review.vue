<template>
    <div>
        <div class="card mt-4 p-4">
            <!-- loading only -->
            <div class="d-flex justify-content-center align-items-center fs-5" v-if="loading">
                <div class="spinner-border text-success" role="status">
                    <span class="visually-hidden">Loading...</span>
                </div>
            </div>
            <!-- Error -->
            <div class="w-100 text-center fs-4" v-else-if="error">
                <i class="fa-solid fa-triangle-exclamation text-danger"></i>
                {{$t('dispatch.工單尚未完成')}}
            </div>
            <!-- stage dispatched_wait_for_review -->
            <div v-if="!loading && dispatchData.stage == 'dispatched_wait_for_review'">
                <div class="d-flex justify-content-center align-items-center fs-5">
                    <div class="spinner-border text-success" role="status">
                        <span class="visually-hidden">Loading...</span>
                    </div>
                </div>
                <div class="w-100 text-center fs-4">
                    {{$t('dispatch.等待AI驗收中')}}
                </div>
            </div>
            <!-- Summary -->
            <div class="mb-3" v-if="!loading && !['wait_for_take', 'wait_for_priority'].includes(dispatchData.stage) && $store.state.user_data.pageType == 'SPS'">
                <h5><i class="fa-solid fa-pen text-primary me-2"></i>{{$t('dispatch.進場結果與後續處置')}}</h5>
                <el-input
                    v-model="summary"
                    :rows="summary_rows"
                    type="textarea"
                    :placeholder="$t('dispatch.進場結果與後續處置')"
                    @input="update_dispatch_summary"
                    :readonly="dispatchData.stage == 'dispatch_finish'"
                    size="large"
                />
            </div>
            <!-- Enter working hour and submit -->
            <div v-if="!loading && !error && dispatchData.stage == 'wait_for_dispatch'">
                <div>
                    <h5><i class="el-icon-warning text-primary"></i>{{$t('dispatch.工作日誌')}}</h5>
                    <div class="d-flex flex-wrap dispatch_data_block pt-3 pb-3">
                        <label class="col-12 col-lg-5 col-xl-3 col-xxl-2">
                            <span class="text-success"><i class="icon-ttl_time"></i></span>
                            {{$t('dispatch.工作時數')}}
                        </label>
                        <div class="col-12 col-lg-7 col-xl-5 col-xxl-3  mt-3 mt-lg-0">
                            <el-input-number type="number" v-model="working_hour"
                            :disabled="!editable"></el-input-number>
                        </div>
                    </div>
                </div>
                <div class="d-flex w-100 mt-3">
                    <button class="btn btn-primary ms-auto" @click="finish_dispatch()"
                    v-if="editable">
                        {{$t('dispatch["完成工單"]')}}
                    </button>
                </div>
            </div>
            <!-- Maual Review -->
            <div v-if="!loading && (dispatchData.stage == 'auto_reviewed_wait_for_manual' ||
            dispatchData.stage == 'dispatched_wait_for_review') && $store.state.user_data.level == 3">
                <h5><i class="fa-solid fa-toolbox text-primary me-2"></i>{{$t('dispatch.手動驗收工單')}}</h5>
                <button class="btn btn-success d-block" @click="manual_review(true)">
                    <i class="fa-solid fa-check"></i>{{$t('dispatch.驗收通過')}}
                </button>
                <button class="btn btn-danger mt-2 d-block"  @click="manual_review(false)">
                    <i class="fa-solid fa-circle-xmark"></i>{{$t('dispatch.驗收不通過')}}
                </button>
            </div>
            <div class="w-100 text-center fs-4" v-else-if="!loading && dispatchData.stage == 'auto_reviewed_wait_for_manual'">
                <span><i class="icon-ttl_time"></i></span>
                {{$t('dispatch.等待管理人員驗收')}}
            </div>
            <!-- Review Fail -->
            <div v-if="!loading && dispatchData.stage == 'review_failed'">
                <h5><i class="el-icon-warning text-danger"></i>{{$t('dispatch.驗收失敗')}}</h5>
                <div class="d-flex flex-wrap pt-2 pb-2 ps-4 form-control mt-3 mb-3 bg-white text-dark">
                    {{dispatchData.review_failed_reason}}
                </div>
                <button class="btn btn-secondary float-end" @click="rework">
                    {{$t('dispatch.重新填寫工單')}}
                </button>
            </div>
            <!-- Dispatch Finish Show Cost -->
            <div v-if="!loading && dispatchData.stage == 'dispatch_finish'">
                <h5><el-icon class="text-success me-2" style="vertical-align: text-bottom;"><success-filled /></el-icon>{{$t('dispatch.驗收通過')}}</h5>
                <div class="d-flex flex-wrap mt-2">
                    <!-- 工作時數 -->
                    <div class="col-12 col-lg-6 mt-2">
                        <i class="fa-solid fa-clock"></i>
                        {{$t('dispatch.工作時數')}}：
                    </div>
                    <div class="col-12 col-lg-6 mt-2 text-center text-lg-start fw-bold">
                        {{dispatchData.working_data[dispatchData.working_data.length - 1].working_hour}} {{$t('小時')}}
                    </div>
                    <el-divider />
                    <!-- 成本 -->
                    <div class="col-12 col-lg-6 mt-2 d-flex flex-wrap">
                        <label class="me-4">
                            <el-icon style="vertical-align: text-bottom;"><money /></el-icon>
                            {{$t('dispatch.本次維運總成本')}} ({{$t('unit.元')}})
                        </label>
                        <h1 >
                            {{dispatchData.auto_review_cost}}
                        </h1>
                    </div>
                    <div class="col-12 col-lg-6 mt-2">
                        {{$t('dispatch.細節')}}
                        <div class="d-flex flex-wrap justify-content-center align-items-center">
                            <!-- 硬體成本 -->
                            <div class="col-12 col-lg-auto text-center text-lg-start">
                                {{$t('dispatch.硬體成本')}}
                                <span class="ms-2">
                                    {{dispatchData.auto_review_cost_detail.predict_dispatch_cost}}
                                </span>
                            </div>
                            <div class="col-12 col-lg-auto text-center text-lg-start">
                                <i class="fa-solid fa-circle-plus ms-4 me-4"></i>
                            </div>
                            <!-- 交通成本 -->
                            <div class="col-12 col-lg-auto text-center text-lg-start">
                                {{$t('dispatch.交通成本')}}
                                <span class="ms-2">
                                    {{dispatchData.auto_review_cost_detail.transit_fee}}
                                </span>
                            </div>
                            <div class="col-12 col-lg-auto text-center text-lg-start">
                                <i class="fa-solid fa-circle-plus ms-4 me-4"></i>
                            </div>
                            <!-- 人事成本 -->
                            <div class="col-12 col-lg-auto text-center text-lg-start">
                                {{$t('dispatch.人事成本')}}
                                <span class="ms-2">
                                    {{dispatchData.auto_review_cost_detail.worker_fee}}
                                </span>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>
<script>
import { ElMessage } from 'element-plus'
import { SuccessFilled, Money } from '@element-plus/icons-vue'

export default {
    name: "Review",
    props: {
        dispatchData: {
            type: Object,
            default: ()=>{
                return {}
            }
        },
        editable: {
            type: Boolean,
            default: true
        }
    },
    components: {
        SuccessFilled,
        Money
    },
    data(){
        return {
            working_hour: null,
            loading: true,
            error: true,
            summary: null,
            summary_rows: 1,
        }
    },
    methods: {
        finish_dispatch(){
            if(this.working_hour == null){
                alert(this.$i18n.t('dispatch["working_hour_input"]'))
                return false
            }else if(typeof(this.working_hour) != "number"){
                alert(this.$i18n.t('dispatch["working_hour_error"]'))
                return false
            }
            this.dispatch_auto_review(true)
        },
        dispatch_auto_review(dispatch_finish=false){
            this.loading = true
            this.axios.post('/dispatch_auto_review', {
                dispatch_ID: this.dispatchData._id,
                working_hour: this.working_hour,
                dispatch_finish: dispatch_finish
            }).then(data=>{
                setTimeout(()=>{
                    console.log(data.data.data)
                    this.loading = false
                    if(data.data.data.error == true){
                        this.error = true
                        this.$parent.$refs.dispatch_content.error_validate = data.data.data.error_data
                        this.$parent.$refs.dispatch_content.show_error_validate = true
                    }else{
                        this.error = false
                        if(dispatch_finish){
                            this.$parent.close_modal()
                            ElMessage.success({message: this.$i18n.t("成功")})
                        }
                    }
                }, 1000)
            })
        },
        update_dispatch_summary(){
            if(typeof this.summary == "string"){
                this.summary_rows = this.summary.split("\n").length
            }
            this.axios.post('/dispatch/update_dispatch_summary', {
                ID: this.dispatchData._id,
                summary: this.summary
            })
        },
        manual_review(result){
            if(result){
                const answer = confirm(`${this.$i18n.t('dispatch.驗收通過')}？`)
                if(answer){
                    this.axios.post('/dispatch_update_stage', {
                        ID: this.dispatchData._id,
                        stage: 'auto_reviewed_wait_for_manual',
                        data: [true]
                    }).then(data=>{
                        this.$parent.close_modal()
                        ElMessage.success({message: this.$i18n.t("成功")})
                    })
                }
            }else{
                const answer = confirm(`${this.$i18n.t('dispatch.驗收不通過')}？`)
                if(answer){
                    var reason = prompt(`${this.$i18n.t('dispatch.原因')}`)
                    if(reason == null){
                        return false
                    }
                    this.axios.post('/dispatch_update_stage', {
                        ID: this.dispatchData._id,
                        stage: 'auto_reviewed_wait_for_manual',
                        data: [false, reason]
                    }).then(data=>{
                        this.$parent.close_modal()
                        ElMessage.success({message: this.$i18n.t("成功")})
                    })
                }
            }
        },
        rework(){
            this.axios.post('/dispatch_update_stage', {
                ID: this.dispatchData._id,
                stage: 'review_failed',
            }).then(data=>{
                this.$parent.dispatchData.stage = 'wait_for_dispatch'
                this.$parent.page_active = 0
                ElMessage.success({message: this.$i18n.t("成功")})
            })
        }
    },
    mounted(){
       // console.log(this.dispatchData)
        if(this.dispatchData.working_data.length > 0){
            if('working_hour' in this.dispatchData.working_data[this.dispatchData.working_data.length - 1]){
                this.working_hour = this.dispatchData.working_data[this.dispatchData.working_data.length - 1].working_hour
            }
            if('summary' in this.dispatchData.working_data[this.dispatchData.working_data.length - 1]){
                this.summary = this.dispatchData.working_data[this.dispatchData.working_data.length - 1].summary
                if(typeof this.summary == "string"){
                    this.summary_rows = this.summary.split("\n").length
                }
            }
        }
        this.dispatch_auto_review()
    }
}
</script>
