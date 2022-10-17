<template>
    <div>
        <div class="d-flex flex-wrap mb-3">
            <div class="col-12 col-lg-5 col-xl-4 col-xxl-3 mt-2 mt-lg-0">
                <autocomplete @station-select="station_select" :preSelect="$store.state.user_data.pageType == 'taipower'"></autocomplete>
            </div>
        </div>

        <div v-if="station_ID != null">
            <div class="card col-12">
                <div class="row g-0">
                    <div class="col-md-4" v-loading="get_card_overview_loading">
                        <el-image class="card border-0 h-100" :src="station_data.imgsrc" style="max-height: 150px;" :fit="'cover'"
                        :preview-src-list="[station_data.imgsrc]">
                            <template #error>
                                <el-upload
                                    class="main_photo_upload w-100 h-100"
                                    list-type="picture-card"
                                    :action="`${this.axios.defaults.baseURL}/documents/upload_main_photo`"
                                    accept="image/*"
                                    :data="{
                                        ID: station_ID
                                    }"
                                    :show-file-list="false"   
                                    :on-success="upload_success"   
                                    :before-upload="upload_main_photo"
                                >
                                    <template #default>
                                        <div class="d-flex flex-column justify-content-center align-items-center">
                                            <i class="fa-solid fa-image fs-3"></i>
                                        </div>
                                    </template>
                                </el-upload>
                            </template>
                        </el-image>
                        <!-- <img  class="img-fluid rounded-start" alt="..." :src="station_data.imgsrc" > -->
                    </div>
                    <div class="col-md-8">
                        <div class="card-body h-100 d-flex flex-column">
                            <div class="d-flex align-items-center">
                                <h3 class="card-title">{{station_item.name}}</h3>
                            </div>
                            <div class="d-flex flex-column w-100 mt-auto">
                                <div class="ms-auto">
                                    <el-upload
                                        :action="`${this.axios.defaults.baseURL}/documents/upload_main_photo`"
                                        accept="image/*"
                                        :data="{
                                            ID: station_ID
                                        }"
                                        :show-file-list="false"   
                                        :on-success="upload_success"   
                                        :before-upload="upload_main_photo"
                                    >
                                        <template #default>
                                            <button class="btn btn-light">
                                                <i class="fa-solid fa-upload"></i>
                                                {{$t('documents.upload_main_photo')}}
                                            </button>
                                        </template>
                                    </el-upload>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
                <div class="navbar navbar-expand-lg navbar-light pb-0">
                    <div class="w-100">
                        <button class="w-100 d-lg-none btn btn-primary" type="button" data-bs-toggle="collapse" data-bs-target="#navbarNav" aria-controls="navbarNav" aria-expanded="false" aria-label="Toggle navigation">
                            {{$t(`documents.tabs.${pageMode}`)}}
                        </button>
                        <div class="collapse navbar-collapse" id="navbarNav">
                            <ul class="navbar-nav col-12 col-lg-12 bg-transparent text-main">
                                <li class="nav-item col-12 col-lg-3 text-center">
                                    <a class="nav-link" :class="{'active': pageMode == 'photo'}" @click="pageMode='photo'">{{$t('documents.tabs.photo')}}</a>
                                </li>
                                <li class="nav-item col-12 col-lg-3 text-center">
                                    <a class="nav-link" :class="{'active': pageMode == 'video'}"  @click="pageMode='video'">{{$t('documents.tabs.video')}}</a>
                                </li>
                                <li class="nav-item col-12 col-lg-3 text-center">
                                    <a class="nav-link" :class="{'active': pageMode == 'sld'}"  @click="pageMode='sld'">{{$t('documents.tabs.sld')}}</a>
                                </li>
                                <li class="nav-item col-12 col-lg-3 text-center">
                                    <a class="nav-link" :class="{'active': pageMode == 'drone'}"  @click="pageMode='drone'">{{$t('documents.tabs.drone')}}</a>
                                </li>
                            </ul>
                        </div>
                    </div>
                </div>
            </div>
            <div class="card col-12 p-4">
                <transition name="fade" mode="out-in">
                    <div :key="pageMode">
                        <photo :station-Id="station_ID" v-if="pageMode=='photo'"></photo>
                        <my-video :station-Id="station_ID" v-else-if="pageMode =='video'"></my-video>
                        <sld :station-Id="station_ID" v-if="pageMode=='sld'"></sld>
                        <drone :station-Id="station_ID" v-if="pageMode=='drone'"></drone>
                    </div>
                </transition>
            </div>
        </div>

    </div>
</template>

<script>
import autocomplete from '@/components/autocomplete/all_type.vue'
import photo from '@/components/documents/photo.vue'
import myVideo from '@/components/documents/video.vue'
import sld from '@/components/documents/sld.vue'
import drone from '@/components/documents/drone.vue'
import { ElNotification} from 'element-plus'
import { UploadFilled } from '@element-plus/icons-vue'


export default {
    name: "Documents",
    components:{
        autocomplete,
        photo,
        myVideo,
        sld,
        drone
    },
    data(){
        return {
            station_ID: null,
            station_item: {},
            station_data: {},
            get_card_overview_loading: false,
            pageMode: 'photo',
            notify: null,
        }
    },
    methods: {
        station_select(item){
            this.station_ID = item.ID
            this.station_item = item
            this.get_card_overview()
        },
        get_card_overview(){
            this.get_card_overview_loading = true
            this.axios.post('/get_card_overview_real', {
                ID_list: [this.station_ID],
                col_list: [this.station_item.collection]
            }).then(data=>{
                console.log(data.data.data)
                data.data.data[0].imgsrc += `?${new Date().getTime()}`
                this.station_data = data.data.data[0]
                this.get_card_overview_loading = false
            })
        },
        upload_main_photo(){
            this.notify = ElNotification({
                icon: UploadFilled,
                title: 'Uploading',
                message: '上傳中',
                showClose: false,
                duration: 0,
                customClass: 'upload_notify'
            })

        },
        upload_success(){
            this.notify.close();
            this.get_card_overview()
        }
    },
}
</script>

<style scoped>
.main_photo_upload:deep(.el-upload--picture-card){
    width: 100% !important;
    background-color: rgba(255, 255, 255, 0.1);
}
@media (min-width: 992px){
    .nav-item:nth-child(n+2){
        border-left: .2px solid rgba(0, 0, 0, 0.7);
    }
}
.nav-item:deep(.active){
    color: black !important;
}
@media (prefers-color-scheme: dark) {
    @media (min-width: 992px){
        .nav-item:nth-child(n+2){
            border-left: .2px solid rgba(250, 250, 250, 0.7);
        }
    }
}
</style>