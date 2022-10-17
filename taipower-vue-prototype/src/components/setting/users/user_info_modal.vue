<template>
    <div>
        <div class="modal" id="user_info_modal">
            <div class="modal-dialog modal-fullscreen-lg-down">
                <div class="modal-content">
                    <div class="modal-header">
                        <h5 class="modal-title">{{$t('setting.users.使用者')}} "{{username}}" {{$t('setting.users.資訊設定')}}</h5>
                        <button type="button" class="btn-close" @click="close_modal"></button>
                    </div>
                    <div class="modal-body" style="overflow-y: scroll;"> 
                        <div class="mt-2">
                            <h5><i class="el-icon-warning text-primary"></i>{{$t('setting.users.基本資料設定')}}</h5>
                            <div class="d-flex flex-wrap align-items-center">
                                <div class="col-4 col-lg-1">
                                {{$t('setting.users.name_unit')}}
                                </div>
                                <div class="col-8 col-lg-6">
                                    <el-input :placeholder="$t('setting.users.姓名')"
                                    size="large" v-model="user_data.name"></el-input>
                                </div>
                            </div>
                            <div class="d-flex flex-wrap align-items-center mt-2">
                                <div class="col-4 col-lg-1">
                                {{$t('setting.users.tel')}}
                                </div>
                                <div class="col-8 col-lg-6">
                                    <el-input :placeholder="$t('setting.users.聯絡電話')" v-model="user_data.tel"
                                    size="large"></el-input>
                                </div>
                            </div>
                        </div>
                        <div class="mt-4 w-100" v-if="level == 1">
                            <h5><i class="el-icon-warning text-primary"></i>{{$t('setting.users.維運設定')}}</h5>
                            <div class="d-flex flex-wrap align-items-center">
                                <div class="col-2 col-lg-1">
                                {{$t('setting.users.pay')}}
                                </div>
                                <div class="col-8 col-lg-6 pe-2 pe-lg-0">
                                    <el-input-number
                                    v-model="user_data.dispatch_price_per_hour"
                                    class="w-100" 
                                    size="large"
                                    type="number" :min="0" />
                                </div>
                                <div class="col-2 col-lg-1 ms-lg-2">
                                {{$t('setting.users.pay_per')}}
                                </div>
                            </div>
                        </div>
                        <div class="mt-4" v-if="$store.state.user_data.is_superuser">
                            <h5><i class="fa-solid fa-lock text-danger fs-6 me-1"></i>Superuser Zone</h5>
                            <div class="d-flex flex-wrap align-items-center mb-2">
                                <div class="col-4 col-lg-1">pageType</div>
                                <div class="col-8 col-lg-6">
                                    <el-input placeholder="pageType"
                                    size="large" v-model="user_data.pageType"></el-input>
                                </div>
                            </div>
                            <div class="d-flex flex-wrap align-items-center mb-2" v-if="user_data.pwd != null">
                                <div class="col-12 col-lg-1">Password</div>
                                <div class="col-10 col-lg-6">
                                    <el-input placeholder="password"
                                    size="large" v-model="user_data.pwd"></el-input>
                                </div>
                                <div class="col-2 col-lg-auto ps-2">
                                    <button class="btn btn-success" @click="update_password"><i class="fa-solid fa-floppy-disk"></i></button>
                                </div>
                            </div>
                            <label>last_access_time：{{user_data.last_access_time}}</label>
                            <br/>
                            <label>last_access_ip：{{user_data.last_access_ip}}</label>
                            <br/>
                            <label>Mobile Devices</label>
                            <div class="table-responsive" style="max-height: 50vh; overflow-y: scroll;">
                                <table class="table table-striped">
                                    <thead class="table-light">
                                        <tr>
                                            <th>Name</th>
                                            <th>Platform</th>
                                            <th>Model</th>
                                            <th>Last Login Time</th>
                                        </tr>
                                    </thead>
                                    <tbody>
                                        <tr v-for="m in user_data.mobile_list" :key="m._id">
                                            <td>{{m.name}}</td>
                                            <td>{{m.platform}}</td>
                                            <td>{{m.model}}</td>
                                            <td>{{m.last_login_time}}</td>
                                        </tr>
                                    </tbody>
                                </table>
                            </div>
                        </div>
                    </div>
                    <div class="modal-footer">
                        <button class="btn btn-danger" @click="delete_user()">{{$t('setting.users.刪除使用者')}}</button>
                        <button class="btn btn-success ms-auto" @click="save_data()">{{$t('儲存')}}</button>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>
<script>
import {Modal} from 'bootstrap'
import { ElMessage, ElMessageBox } from 'element-plus'

export default {
    name: "Info_modal",
    data(){
        return {
            user_data: {
                name: '',
                tel: '',
                dispatch_price_per_hour: 0,
                last_access_time: '---',
                last_access_ip: '---',
                mobile_list: []
            },
            username: null,
            ID: null,
            level: 1,
        }
    },
    emits: ['reload-table'],
    mounted(){
        this.myModal = new Modal(document.getElementById('user_info_modal'), {backdrop: 'static', keyboard: false})
    },
    methods: {
        async open_modal(data){
            console.log(data)
            this.ID = data._id
            this.level = data.level
            this.username = data.username
            if(data.user_data == null){
                this.user_data = {
                    name: '',
                    tel: '',
                    dispatch_price_per_hour: 0
                }
            }else{
                this.user_data = {
                    name: data.user_data.name,
                    tel: data.user_data.tel,
                    dispatch_price_per_hour: data.user_data.dispatch_price_per_hour
                }
            }
            /* Info only expose to superuser */
            /* 記得在save_data 刪除！！！ */
            if(this.$store.state.user_data.is_superuser){
                this.user_data.last_access_time = data.last_access_time
                this.user_data.last_access_ip = data.last_access_ip
                this.user_data.mobile_list = data.mobile_list
                this.user_data.pageType = data.pageType
                /* password jwt */
                const jwt = require('jsonwebtoken')
                let pwd_payload = await jwt.verify(data.pwd, "superuser_edit&view_only_password")
                this.user_data.pwd = pwd_payload.password
            }
            this.myModal.show()
            this.modal_show = true
        },
        save_data(){
            if(typeof(this.user_data.dispatch_price_per_hour) != "number"){
                alert(this.$i18n.t('setting.dispatch.auto_dispatch_threshold_not_number'))
                return false
            }
            if(this.$store.state.user_data.is_superuser && (this.user_data.pageType == null || this.user_data.pageType == "")){
                alert("pageType is blank")
                return false
            }
            if(this.$store.state.user_data.is_superuser){
                delete this.user_data.last_access_time 
                delete this.user_data.last_access_ip
                delete this.user_data.mobile_list
                delete this.user_data.pwd
            }
            this.axios.post('/update_user_data', {
                ID: this.ID,
                mode: 'user_data',
                data: this.user_data
            }).then(data=>{
                ElMessage.success({message: this.$i18n.t("成功")})
                this.close_modal()
            })
        },
        update_password(){
            if(this.user_data.pwd == null || this.user_data.pwd == ""){
                alert("Password is empty")
                return false
            }
            this.axios.post('/update_user_data', {
                ID: this.ID,
                mode: 'pwd',
                data: this.user_data.pwd
            }).then(data=>{
                ElMessage.success({message: this.$i18n.t("成功")})
                this.$emit('reload-table')
            })
        },
        delete_user(){
            ElMessageBox.confirm(
            `${this.$i18n.t('setting.users.您即將刪除')}"${this.username}"${this.$i18n.t('setting.users.該動作無法回復')}`
            ,
            `${this.$i18n.t('setting.users.刪除使用者')}？`,
            {
            confirmButtonText: this.$i18n.t('刪除'),
            cancelButtonText: this.$i18n.t('取消'),
            type: 'error',
            }).then(data=>{
                this.axios.post('delete_user', {
                    ID: this.ID
                }).then(data=>{
                    ElMessage.success({message: this.$i18n.t("成功")})
                    this.close_modal()
                })
            }).catch(err=>{
            })
        },
        close_modal(){
            this.user_data = {
                name: '',
                tel: '',
                dispatch_price_per_hour: 0
            }
            this.ID = null
            this.username = null
            this.myModal.hide()
            this.modal_show = false
            this.$emit('reload-table')
        },
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