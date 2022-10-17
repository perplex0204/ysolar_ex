<template>
    <div>
        <div class="card col-12">
            <div class="row g-0">
                <div class="col-md-2">
                    <el-image class="card border-0 h-100" :src="$store.state.user_data.main_photo" style="max-height: 150px;" :fit="'cover'"
                    :preview-src-list="[$store.state.user_data.main_photo]"
                    >
                        <template #error>
                            <el-upload
                                class="main_photo_upload w-100 h-100"
                                list-type="picture-card"
                                :action="`${this.axios.defaults.baseURL}/setting/upload_user_photo`"
                                accept="image/*"
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
                <div class="col-md-10">
                    <div class="card-body h-100 d-flex flex-column">
                        <div class="d-flex align-items-center">
                            <h3 class="card-title">{{$store.state.user_data.username}}</h3>
                        </div>
                        <div>
                            <div class="d-flex jusitfy-content-center">
                                <label>{{$t(`setting.users.level["${$store.state.user_data.level}"]`)}}</label>
                            </div>
                        </div>
                        <div class="d-flex flex-column w-100 mt-auto">
                            <div class="d-flex flex-wrap">
                                <button class="btn btn-primary col-12 col-lg-auto mt-2 mt-lg-0"
                                @click="open_change_username_password_modal">
                                    <i class="fa-solid fa-key"></i>
                                    {{$t('setting.users.update_username_password')}}
                                </button>
                                <div class="col-12 col-lg-auto ms-auto upload_button">
                                    <el-upload
                                        :action="`${this.axios.defaults.baseURL}/setting/upload_user_photo`"
                                        accept="image/*"
                                        :show-file-list="false"   
                                        :on-success="upload_success"   
                                        :before-upload="upload_main_photo"
                                    >
                                        <template #default>
                                            <button class="btn btn-light col-12 col-lg-auto mt-2 mt-lg-0 ">
                                                <i class="fa-solid fa-upload"></i>
                                                {{$t('setting.users.upload_user_photo')}}
                                            </button>
                                        </template>
                                    </el-upload>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
        <!-- Change Username Password Modal -->
        <div class="modal" tabindex="-1" ref="change_username_password_modal">
            <div class="modal-dialog modal-dialog-centered">
                <div class="modal-content">
                <div class="modal-header">
                    <h5 class="modal-title">{{$t('setting.users.update_username_password')}}</h5>
                    <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
                </div>
                <div class="modal-body">
                    <el-form
                        ref="user_form"
                        :model="form_data"
                        :rules="rules"
                        size="large"
                    >
                        <div class="d-flex flex-wrap align-items-center p-2 pt-0">
                            <!-- username -->
                            <label class="col-4 mt-4 text-lg-center d-none">{{$t('setting.users.username')}}</label>
                            <div class="col-8 mt-4 d-none">
                                <el-form-item prop="old_password" class="mb-0">
                                    <el-input v-model="form_data.username" type="text" :disabled="true" />
                                </el-form-item>
                            </div>
                            <!-- Old Password -->
                            <label class="col-4 mt-4 text-lg-center">{{$t('setting.users.old_password')}}</label>
                            <div class="col-8 mt-4">
                                <el-form-item prop="old_password" class="mb-0">
                                    <el-input v-model="form_data.old_password" type="password"  />
                                </el-form-item>
                            </div>
                            <!-- New Password -->
                            <label class="col-4 mt-4 text-lg-center">{{$t('setting.users.new_password')}}</label>
                            <div class="col-8 mt-4">
                                <el-form-item prop="new_password" class="mb-0">
                                    <el-input v-model="form_data.new_password" type="password" />
                                </el-form-item>
                            </div>
                            <!-- Password valid -->
                            <label class="col-4 mt-4 text-lg-center">{{$t('setting.users.password_valid')}}</label>
                            <div class="col-8 mt-4">
                                <el-form-item prop="password_valid" class="mb-0">
                                    <el-input v-model="form_data.password_valid" type="password" />
                                </el-form-item>
                            </div>
                        </div>
                    </el-form>
                </div>
                <div class="modal-footer">
                    <button type="button" class="btn btn-success" @click="save_password">{{$t('儲存')}}</button>
                </div>
                </div>
            </div>
        </div>
    </div>
</template>

<script>
import { ElNotification} from 'element-plus'
import { UploadFilled } from '@element-plus/icons-vue'
import { ElMessage } from 'element-plus'
import { Modal } from 'bootstrap'

export default {
    name: "Users_card",
    data(){
        return {
            form_data: {
                username: this.$store.state.user_data.username,
                old_password: null,
                new_password: null,
                password_valid: null,
            },
            old_password_error: false,
            rules: {
                old_password: [
                    { required: true, message: this.$i18n.t('setting.users.please_input_password'), trigger: 'blur' },
                    { validator: this.is_old_password_error, message: this.$i18n.t('setting.users.old_password_error'), trigger: 'blur'}
                ],
                new_password: [
                    { required: true, message: this.$i18n.t('setting.users.please_input_password'), trigger: 'blur' },
                ],
                password_valid: [
                    { required: true, message: this.$i18n.t('setting.users.please_input_password'), trigger: 'blur' },
                    { validator: this.password_validator, message: this.$i18n.t('setting.users.please_password_not_same'), trigger: 'blur' }
                ]
            }
        }
    },
    methods: {
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
            window.location.reload()
        },
        open_change_username_password_modal(){
            this.form_data = {
                username: this.$store.state.user_data.username,
                old_password: null,
                new_password: null,
                password_valid: null,
            }
            this.old_password_error = false
            this.change_username_password_modal.show()
        },
        save_password(){
            this.old_password_error = false
            this.$refs.user_form.validate().then(data => {
                if(!this.password_validator())
                    return false
                this.axios.post('/change_username_password', this.form_data).then(data=>{
                    if(data.data.data.status == false){
                        if(data.data.data.reason == 'not_equal'){
                            this.old_password_error = true
                            this.$refs.user_form.validateField('old_password')
                            return false
                        }
                    }
                    this.change_username_password_modal.hide()
                    this.$refs.user_form.validateField('old_password')
                    ElMessage.success({message: this.$i18n.t("成功")})
                })
            }).catch(err=>{})
        },
        /* Check form */
        password_validator(){
            if(this.form_data.new_password != this.form_data.password_valid){
                return false
            }else{
                return true
            }
        },
        is_old_password_error(){
            return !this.old_password_error
        }
    },
    mounted(){
        console.log(this.$store.state.user_data)
        this.change_username_password_modal = new Modal(this.$refs.change_username_password_modal)
    }
}
</script>
<style scoped>
@media (max-width: 991px){
    .upload_button:deep(.el-upload.el-upload--text){
        width: 100%;
    }
}
</style>