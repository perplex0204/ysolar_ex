<template>
    <div class="d-flex flex-column">
        <div class="d-flex flex-wrap w-100">
            <!-- upload -->
            <el-upload
                :action="`${this.axios.defaults.baseURL}/documents/upload_photo`"
                :data="{
                    ID: stationId
                }"
                list-type="picture-card"
                class="col-12 col-lg-auto upload_btn"
                :multiple="true"
                :on-preview="photo_upload_preview"
                :on-remove="(file)=>{
                    delete_data(file.response.data.result[0], false)
                }"
                :on-progress="upload_process"
                accept="image/*"
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
            <div class="m-2" v-for="file, i in file_list"
            :key="file._id">
                <label class="fs-7">{{time_label_dict[file.filename]}}</label>
                <div class="position-relative" style="width: 100px; height: 100px">
                    <el-image
                        class="card w-100 h-100"
                        :src="file.filepath"
                        :preview-src-list="filepath_list"
                        :initial-index="i"
                        fit="cover"
                    />
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
                v-model:currentPage="current_page"
                :page-size="20"
                :pager-count="5"
                @current-change="upload_documents_photo_get()">
			</el-pagination>
        </div>
        <!-- Photo Preview -->
        <el-dialog v-model="dialogImage.visible">
            <img class="w-100" :src="dialogImage.url" alt="" />
        </el-dialog>
    </div>
</template>

<script>
import TimeRangePicker from "@/components/datepicker/timeRangePicker.vue"
import { Plus } from '@element-plus/icons-vue'

export default {
    name: "Photo",
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
            date_selection: {},
            file_list: [],
            filepath_list: [],
            current_page: 1,
            total_file: 0,
            dialogImage: {
                visible: false,
                url: '#'
            },
            time_label_dict: {}
        }
    },
    mounted(){
        this.sync_data = window.setInterval(this.upload_documents_photo_get, 1000)
    },
    unmounted(){
        window.clearInterval(this.sync_data)
    },
    methods: {
        upload_documents_photo_get(){
            this.axios.post('/documents/upload_documents_photo_get', {
                ID: this.stationId,
                time: this.date_selection
            }).then(data=>{
                //console.log(data.data.data)
                this.file_list = []
                this.filepath_list = []
                this.time_label_dict = {}
                let time_list = []
                data.data.data.file_list.forEach(file=>{
                    this.file_list.push(file)
                    this.filepath_list.push(file.filepath)
                    this.total_file = data.data.data.total_file
                    if(time_list.includes(file.upload_time_simple)){
                        this.time_label_dict[file.filename] = ""
                    }else{
                        time_list.push(file.upload_time_simple)
                        this.time_label_dict[file.filename] = file.upload_time_simple
                    }
                })
            })
        },
        setDate(data){
            this.date_selection = {
                mode:data.mode,
                start_date:data.date_list[0],
                end_date:data.date_list[1]
            }
            this.upload_documents_photo_get()
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
                this.axios.post('/documents/upload_documents_photo_delete', {ID: file_id})
                let index = null
                for(var i in this.file_list){
                    if(file_id == this.file_list[i]._id){
                        index = i
                    }
                }
                if(index != null){
                    this.file_list.splice(index, 1)
                }
            }else{
                return false
            }
        },
        photo_upload_preview(file){
            this.dialogImage.visible = true
            this.dialogImage.url = `${file.url}`
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
