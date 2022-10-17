<template>
    <div>
        <div class="modal" id="dispatch_modal">
            <div class="modal-dialog modal-fullscreen-lg-down">
                <div class="modal-content" style="overflow-y: scroll;" v-if="modal_show">
                    <div class="modal-header">
                        <h5 class="modal-title">{{modalControl.title}}</h5>
                        <button type="button" class="btn-close" @click="close_modal"></button>
                    </div>
                    <div class="modal-body">
                        <el-steps :active="page_active" simple
                        v-if="!dispatch_in_edit"> <!-- hide when editing dispatch -->
                            <el-step :title="$t('dispatch.案場資訊')">
                                <template #icon>
                                    <i class="fs-5 icon-nav_factory"></i>
                                </template>
                            </el-step>
                            <el-step :title="$t('dispatch.工單內容')">
                                <template #icon>
                                    <i class="fs-5 icon-nav_works"></i>
                                </template>
                            </el-step>
                            <el-step :title="$t('dispatch.審查')">
                                <template #icon>
                                    <i class="fs-5 fas fa-check"></i>
                                </template>
                            </el-step>
                        </el-steps>  
                        <plant-info v-show="page_active == 0" :dispatch-data="dispatchData" :editable="modalControl.editable"
                        :modal-control="modalControl" />
                        <dispatch-content ref="dispatch_content" v-show="page_active == 1" 
                        :dispatch-data="dispatchData"
                        :editable="modalControl.editable &&
                        (this.$store.state.user_data.level < 3 ? ['wait_for_dispatch'].includes(this.dispatchData.stage):
                        !(['dispatch_finish'].includes(this.dispatchData.stage)))"/>        
                        <review v-show="page_active == 2" 
                        ref="dispatch_review"
                        :dispatch-data="dispatchData" 
                        :modal-control="modalControl"
                        :editable="modalControl.editable && dispatchData.dispatch_time != null 
                        && ['wait_for_dispatch'].includes(dispatchData.stage)"/>       
                    </div>
                    <div class="modal-footer justify-content-start"
                    v-if="!dispatch_in_edit"> <!-- hide when editing dispatch -->
                        <button type="button" class="btn btn-danger"
                        v-if="modalControl.editable && modalControl.level >=3 && false">
                            {{$t('刪除')}}
                        </button>
                        <button type="button" class="btn btn-success"
                        @click="dispatch_take"
                        v-if="['wait_for_take'].includes(dispatchData.stage) && $store.state.user_data.pageType != 'taipower'">
                            {{$t('dispatch.接單')}}
                        </button>
                        <button type="button" class="btn btn-light"
                        @click="dispatch_worker_transfer"
                        v-if="modalControl.editable && !['wait_for_take', 'merged', 'dispatch_finish'].includes(dispatchData.stage)">
                            {{$t('轉單')}}
                        </button>
                        <button type="button" class="btn btn-secondary" @click="close_modal"
                        v-if="modalControl.editable">{{$t('關閉')}}</button>
                        <button type="button" class="btn btn-success ms-auto" 
                        v-if="page_active > 0"
                        @click="page_active = page_active > 0 ? page_active - 1 : page_active">{{$t('上一頁')}}</button>
                        <button type="button" class="btn btn-success"
                        v-if="next_step_compute" 
                        :class="{'ms-auto': page_active == 0}"
                        @click="next_step">{{$t('下一頁')}}</button>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>
<script>
import {Modal} from 'bootstrap'
import PlantInfo from './dispatch_page/plant_info.vue'
import DispatchContent from './dispatch_page/dispatch_content.vue'
import Review from './dispatch_page/review.vue'
import { ElMessage } from 'element-plus'

export default {
    name: "Dispatch_Page",
    components:{
        PlantInfo,
        DispatchContent, 
        Review
    },
    data(){
        let currDate = new Date()
        const offset = currDate.getTimezoneOffset()
        currDate = new Date(currDate.getTime() - (offset*60*1000))

        return {
            page_active: 0,
            modalControl: {
                // title: str,
                // editable: bool
                // level: int
            },
            dispatchData: {},
            today: currDate.toISOString().split('T')[0],
            dispatch_in_edit: false,
            modal_show: false
        }
    },
    emits: ['reload-table'],
    mounted(){
        this.myModal = new Modal(document.getElementById('dispatch_modal'), {backdrop: 'static', keyboard: false})
    },
    methods: {
        openModal(){
            this.page_active = 0
            this.dispatch_in_edit = false
            this.$store.commit("set_prevent_leave_at_once", true)
            this.myModal.show()
            this.modal_show = true
            // nav to review page if review failed
            if(this.dispatchData.stage == 'review_failed'){
                this.page_active = 2
            }
        },
        dispatch_take(){
            this.axios.post('/dispatch_take', {
                ID: this.dispatchData._id,
            }).then(data=>{
                ElMessage.success({message: this.$i18n.t("成功")})
                this.close_modal()
            })
        },
        dispatch_worker_transfer(){
            const answer = confirm(this.$i18n.t('dispatch["dispatch_worker_transfer_confirm"]'))
            if(answer){
                this.axios.post("/dispatch_update_stage", {
                    ID: this.dispatchData._id,
                    to_stage: 'wait_for_take'
                }).then(data => {
                    console.log(data.data.data)
                    ElMessage.success({message: this.$i18n.t("成功")})
                    this.close_modal()
                })
            }
        },
        close_modal(){
            this.modalControl = {
                // title: str,
                // editable: bool
            }
            this.dispatchData = {}
            this.page_active = 0
            this.myModal.hide()
            this.modal_show = false
            this.$store.commit("set_prevent_leave_at_once", false)
            this.$emit('reload-table')
        },
        next_step(){
            this.page_active = this.page_active < 2 ? this.page_active + 1 : this.page_active
            if(this.page_active == 2){
                this.$refs.dispatch_review.dispatch_auto_review()
            }
        }
    },
    computed: {
        next_step_compute(){
            if(this.page_active < 1){
                return true
            }
            else if(this.page_active == 1){
                if(['wait_for_dispatch', 'dispatched_wait_for_review',
                'auto_reviewed_wait_for_manual', 'dispatch_finish', 'review_failed'].includes(this.dispatchData.stage)){
                    return true
                }
            }
            return false
        }
    },
    beforeUnmount(){
        this.myModal.dispose()
        this.$store.commit("set_prevent_leave_at_once", false)
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
.dispatch_data_block{
    border-bottom: .5px solid gray;
}
.disable-div{
    pointer-events: none;
    opacity: 0.4;
}
</style>
<style scoped>
.el-step.is-simple:deep(.el-step__icon.is-text){
    border: 0px;
}
/* step change on mobile */
@media (max-width: 991px){
    .el-step.is-simple:not(:last-of-type):deep(.el-step__title){
        max-width: unset;
        flex-grow: 1;
        text-align: center;
    }
    .el-step.is-simple:deep(.el-step__title){
        max-width: unset;
        flex-grow: 1;
        text-align: center;
    }
    .el-step.is-simple:deep(.el-step__arrow){
        flex-grow: unset;
    }
    .el-step.is-simple{
        min-width: 200px;
        justify-content: center;
        margin-bottom: .5rem;
    }
    .el-steps{
        flex-wrap: wrap;
        justify-content: center;
    }
}
</style>