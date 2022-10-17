<template>
    <div>
        <div class="modal" id="new_user_modal">
            <div class="modal-dialog modal-fullscreen-lg-down">
                <div class="modal-content">
                    <div class="modal-header">
                        <h5 class="modal-title">{{$t('setting.users.新增使用者')}}</h5>
                        <button type="button" class="btn-close" @click="close_modal"></button>
                    </div>
                    <div class="modal-body" style="overflow-y: scroll;"> 
                        <div>
                            <el-form
                                ref="user_form"
                                :model="form_data"
                                :rules="rules"
                                size="large"
                            >
                                <!-- 帳號與密碼 -->
                                <div>
                                    <h5><i class="el-icon-warning text-primary"></i>{{$t('setting.users.帳號密碼')}}</h5>
                                </div>
                                <div class="d-flex flex-wrap align-items-center p-2 pt-0">
                                    <!-- Username -->
                                    <label class="col-4 col-lg-1 mt-4 text-lg-center">{{$t('setting.users.username')}}</label>
                                    <div class="col-8 col-lg-3 mt-4">
                                        <el-form-item prop="username" class="mb-0">
                                            <el-input v-model="form_data.username" @change="username_duplicate_check" />
                                        </el-form-item>
                                    </div>
                                    <!-- Password -->
                                    <label class="col-4 col-lg-1 mt-4 text-lg-center">{{$t('setting.users.password')}}</label>
                                    <div class="col-8 col-lg-3 mt-4">
                                        <el-form-item prop="password" class="mb-0">
                                            <el-input v-model="form_data.password" type="password"  />
                                        </el-form-item>
                                    </div>
                                    <!-- Password valid -->
                                    <label class="col-4 col-lg-1 mt-4 text-lg-center">{{$t('setting.users.password_valid')}}</label>
                                    <div class="col-8 col-lg-3 mt-4">
                                        <el-form-item prop="password_valid" class="mb-0">
                                            <el-input v-model="form_data.password_valid" type="password" />
                                        </el-form-item>
                                    </div>
                                </div>
                                <!-- 權限 -->
                                <div class="mt-4">
                                    <h5><i class="el-icon-warning text-primary"></i>{{$t('setting.users.權限')}}</h5>
                                </div>
                                <div class="d-flex flex-wrap align-items-center p-2 pt-0">
                                    <!-- level -->
                                    <label class="col-4 col-lg-1 mt-4 text-lg-center">{{$t('setting.users.account_level')}}</label>
                                    <div class="col-8 col-lg-3 mt-4">
                                        <el-form-item prop="level" class="mb-0">
                                            <el-select v-model="form_data.level" size="large" class="w-100">
                                                <el-option :value="1" :label="`1 ${$t('setting.users.level.1')}`"/>
                                                <el-option :value="2" :label="`2 ${$t('setting.users.level.2')}`"/>
                                                <el-option :value="3" :label="`3 ${$t('setting.users.level.3')}`"/>
                                            </el-select>
                                        </el-form-item>
                                    </div>
                                    <!-- plant_access -->
                                    <label class="col-4 col-lg-1 mt-4 text-lg-center">{{$t('setting.users.plant_access')}}</label>
                                    <div class="col-8 col-lg-3 mt-4">
                                        <plant-access-popover :user-data="form_data" @update_plant="new_plant => form_data.plant = new_plant.slice(0)">
                                        </plant-access-popover>
                                    </div>
                                </div>
                                <!-- 基本資料 -->
                                <div class="mt-4">
                                    <h5><i class="el-icon-warning text-primary"></i>{{$t('setting.users.基本資料設定')}}</h5>
                                </div>
                                <div class="d-flex flex-wrap align-items-center p-2 pt-0">
                                    <!-- name and unit -->
                                    <label class="col-4 col-lg-1 mt-4 text-lg-center">{{$t('setting.users.name_unit')}}</label>
                                    <div class="col-8 col-lg-3 mt-4">
                                        <el-form-item prop="name_unit" class="mb-0">
                                            <el-input v-model="form_data.user_data.name" />
                                        </el-form-item>
                                    </div>
                                    <!-- tel -->
                                    <label class="col-4 col-lg-1 mt-4 text-lg-center">{{$t('setting.users.tel')}}</label>
                                    <div class="col-8 col-lg-3 mt-4">
                                        <el-form-item prop="tel" class="mb-0">
                                            <el-input v-model="form_data.user_data.tel" />
                                        </el-form-item>
                                    </div>
                                </div>
                                <div v-if="form_data.level == 1">
                                    <!-- 維運設定 -->
                                    <div class="mt-4">
                                        <h5><i class="el-icon-warning text-primary"></i>{{$t('setting.users.維運設定')}}</h5>
                                    </div>
                                    <div class="d-flex flex-wrap align-items-center p-2 pt-0">
                                        <!-- dispatch_price_per_hour -->
                                        <div class="col-2 col-lg-1">
                                            {{$t('setting.users.pay')}}
                                        </div>
                                        <div class="col-8 col-lg-6 pe-2 pe-lg-0">
                                            <el-input-number
                                            v-model="form_data.user_data.dispatch_price_per_hour"
                                            class="w-100" 
                                            size="large"
                                            type="number" :min="0" />
                                        </div>
                                        <div class="col-2 col-lg-1 ms-lg-2">
                                            {{$t('setting.users.pay_per')}}
                                        </div>
                                    </div>
                                </div>
                            </el-form>
                        </div>
                    </div>
                    <div class="modal-footer">
                        <button class="btn btn-success" @click="save_data()">{{$t('儲存')}}</button>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>
<script>
import {Modal} from 'bootstrap'
import { ElMessage } from 'element-plus'
import plantAccessPopover from './plant_access_popover.vue'


export default {
    name: "Info_modal",
    components: {
        plantAccessPopover
    },
    data(){
        return {
            form_data: {
                username: null,
                password: null,
                password_valid: null,
                level: 1,
                plant: ['total'],
                user_data: {
                    name: null,
                    tel: null,
                    dispatch_price_per_hour: 0
                }
            },
            username_no_duplicate: true,
            rules: {
                username: [
                    { required: true, message: this.$i18n.t('setting.users.please_input_username'), trigger: 'blur' },
                    { validator: this.is_username_duplicate, message: this.$i18n.t('setting.users.username_duplicate'), trigger: 'blur' }
                ],
                password: [
                    { required: true, message: this.$i18n.t('setting.users.please_input_password'), trigger: 'blur' },
                ],
                password_valid: [
                    { required: true, message: this.$i18n.t('setting.users.please_input_password'), trigger: 'blur' },
                    { validator: this.password_validator, message: this.$i18n.t('setting.users.please_password_not_same'), trigger: 'blur' }
                ],
                dispatch_price_per_hour: [
                    { type: Number, message: this.$i18n.t('setting.users.must_be_number'), trigger: 'blur'}
                ]
            }
        }
    },
    emits: ['reload-table'],
    mounted(){
        this.myModal = new Modal(document.getElementById('new_user_modal'), {backdrop: 'static', keyboard: false})
    },
    methods: {
        open_modal(data){
            this.myModal.show()
            this.modal_show = true
        },
        save_data(){
            this.$refs.user_form.validate().then(result=>{
                console.log(this.form_data)
                if(this.form_data.plant.length == 0){
                    alert(this.$i18n.t("setting.users.plant_empty_error"))
                    return false
                }
                this.axios.post('/create_new_user', this.form_data).then(data=>{
                    ElMessage.success({message: this.$i18n.t("成功")})
                    this.close_modal()
                })
            }).catch(err=>{})
        },
        close_modal(){
            this.myModal.hide()
            this.modal_show = false
            this.$emit('reload-table')
        },
        /* Check form */
        password_validator(){
            if(this.form_data.password != this.form_data.password_valid){
                return false
            }else{
                return true
            }
        },
        is_username_duplicate(){
            return this.username_no_duplicate
        },
        username_duplicate_check(){
            this.axios.post('/username_duplicate_check', {
                username: this.form_data.username
            }).then(async(data)=>{
                if(data.data.data == false){
                    this.username_no_duplicate = false
                }else{
                    this.username_no_duplicate = true
                }
                await this.$refs.user_form.validateField('username')
            })
        }
    },
    beforeUnmount(){
        this.myModal.dispose()
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
</style>