<template>
    <div>
        <div class="d-flex flex-wrap w-100">
            <!-- upload -->
            <el-upload
                :action="`${this.axios.defaults.baseURL}/documents/upload_video`"
                :data="{
                    ID: stationId
                }"
                list-type="picture-card"
                class="col-12 col-lg-auto upload_btn"
                :multiple="true"
                :on-error="upload_error"
                :on-preview="video_upload_preview"
                :on-remove="(file)=>{
                    delete_data(file.response.data.result[0]._id, false)
                }"
                :on-progress="upload_process"
                accept="video/*"
            >
           <!-- Manual Upload when user clicking save -->
                <div class="w-100 text-center">
                    <el-icon><plus /></el-icon>
                </div>
            </el-upload>
            <!-- datepicker -->
            <el-popover placement="bottom-start" trigger="click"
            :width="this.$store.state.isMobile? '95vw': '60vw'">
                <template #reference>
                    <el-button
                        size="large"
                        class="col-12 col-lg-3 col-xl-2 ms-lg-auto mt-2 mt-lg-0">
                        <i class="far fa-clock"></i>{{$t('上傳日期')}}
                    </el-button>
                </template>
                <time-range-picker @setDate="setDate"></time-range-picker>
            </el-popover>
        </div>
        <div class="d-flex flex-wrap">
            <div class="m-2" v-for="file in file_list"
            :key="file._id">
                <label class="fs-7">{{time_label_dict[file.filename]}}</label>
                <div class="position-relative" style="width: 100px; height: 100px">
                    <div @click.prevent="video_preview(file)"
                    class="w-100 h-100">
                        <el-image
                            class="card w-100 h-100"
                            :src="file.thumbnail_path"
                            :lazy="true"
                            fit="cover"
                        />
                    </div>
                    <div class="position-absolute top-0 end-0">
                        <button class="btn fs-6 p-1 text-light"
                        @click="delete_data(file._id)">
                            <i class="fa-solid fa-xmark"></i>
                        </button>
                    </div>
                </div>
            </div>
        </div>
        <div class="mt-auto">
            <el-pagination
                class="d-flex justify-content-center w-100"
                v-if="file_list.length>0"
                background
                layout="prev, pager, next"
                :total="total_file"
                :page-size="20"
                :pager-count="5"
                v-model:currentPage="current_page"
                @current-change="upload_documents_video_get()">
			</el-pagination>
        </div>
        <!-- video preview -->
        <div class="modal" tabindex="-1" id="video_modal">
            <div class="modal-dialog modal-fullscreen-lg-down">
                <div class="modal-content">
                    <div class="modal-header">
                        <h5 class="modal-title">{{$t('預覽')}}</h5>
                        <button type="button" class="btn-close" @click="close_modal"></button>
                    </div>
                    <div class="modal-body d-flex justify-content-center w-100">
                        <div class="col-10 col-lg-8 text-center">
                            <video v-if="video_modal.url != null && video_modal.visible" :src="video_modal.url"
                            controls preload="metadata"
                            style="object-fit: cover; max-width: 100%; max-height: 80vh;" />
                        </div>
                    </div>
                </div>
            </div>
        </div>
        <div class="d-none">
            <video src="#" ref="video_thumbnail"
            playsinline muted preload="none"
            @playing="video_to_thumbnail()"
            style="object-fit: cover; width: 500px; height: 500px;"/>
        </div>
    </div>
</template>

<script>
import TimeRangePicker from "@/components/datepicker/timeRangePicker.vue"
import { Plus } from '@element-plus/icons-vue'
import {Modal} from 'bootstrap'
import { ElMessage } from 'element-plus'

export default {
    name: "Video",
    components: {
        TimeRangePicker,
        Plus
    },
    props: {
        stationId: {
            type: String,
        }
    },
    data(){
        return {
            isMounted: false,
            date_selection: {},
            file_list: [],
            filepath_list: [],
            current_page: 1,
            total_file: 0,
            video_modal: {
                url: null,
                visible: false,
            },
            time_label_dict: {}
        }
    },
    mounted(){
        this.myModal = new Modal(document.getElementById('video_modal'), {backdrop: 'static', keyboard: false})
        this.isMounted = true
        this.sync_data = window.setInterval(this.upload_documents_video_get, 1000)
    },
    unmounted(){
        window.clearInterval(this.sync_data)
    },
    methods: {
        upload_documents_video_get(){
            this.axios.post('/documents/upload_documents_video_get', {
                ID: this.stationId,
                time: this.date_selection,
                current_page: this.current_page
            }).then(data=>{
                //console.log(data.data.data)
                let file_list = []
                let filepath_list = []
                this.time_label_dict = {}
                let time_list = []
                data.data.data.file_list.forEach(file=>{
                    file_list.push(file)
                    filepath_list.push(file.filepath)
                    if(time_list.includes(file.upload_time_simple)){
                        this.time_label_dict[file.filename] = ""
                    }else{
                        time_list.push(file.upload_time_simple)
                        this.time_label_dict[file.filename] = file.upload_time_simple
                    }
                })
                this.total_file = data.data.data.total_file
                this.file_list = file_list
                this.filepath_list = filepath_list
            })
        },
        setDate(data){
            this.date_selection = {
                mode:data.mode,
                start_date:data.date_list[0],
                end_date:data.date_list[1]
            }
            this.upload_documents_video_get()
        },
        delete_data(file_id, ask=true){
            let answer = false
            if(ask == false){
                answer = true
            }
            else{   //from old
                answer = confirm(this.$i18n.t('delete_confirm'))
            }
            if(answer){
                console.log(file_id)
                this.axios.post('/documents/upload_documents_video_delete', {ID: file_id}).then(data=>{
                    this.upload_documents_video_get()
                })
            }else{
                return false
            }
        },
        video_upload_preview(file){
            this.video_modal.url = file.url
            this.video_modal.visible = true
            this.myModal.show()
        },
        video_preview(file){
            this.video_modal.url = file.filepath
            this.video_modal.visible = true
            this.myModal.show()
        },
        upload_error(err){
            if(String(err).includes('413 Request Entity Too Large')){
                ElMessage.error({message: this.$i18n.t("上傳失敗，檔案過大")})
            }else{
                ElMessage.error({message: this.$i18n.t("上傳失敗")})
            }
            console.log(err)
        },
        close_modal(){
            this.myModal.hide()
            this.video_modal.visible = false
        },
        upload_process(e){
            console.log(e)
            e.percent = Math.round(e.percent)
        }
    }
}
</script>

<style scoped>
.upload_btn{
    max-width: 100%; 
}
@media (max-width: 991px){
    .upload_btn:deep(.el-upload--picture-card){
        width: 100%;
    }
}
</style>
