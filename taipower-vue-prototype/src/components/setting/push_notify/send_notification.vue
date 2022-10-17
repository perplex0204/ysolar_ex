<template>
    <div class="mb-3">
        <div class="card p-4 mt-3" v-loading="is_loading">
            <div class="d-flex flex-wrap align-items-center">
                <h5><i class="fa-solid fa-paper-plane text-primary me-2"></i>{{$t('setting.push_notify.手動發送訊息')}}</h5>
            </div>
            <el-form
                ref="user_form"
                :model="form_data"
                :rules="rules"
                size="large"
            >
                <div class="d-flex flex-wrap align-items-center">
                    <!-- Title -->
                    <label class="col-4 col-lg-1 mt-lg-4 text-lg-center">{{$t('setting.push_notify.標題')}}</label>
                    <div class="col-12 col-lg-4 mt-lg-4">
                        <el-form-item prop="title" class="mb-0">
                            <el-input v-model="form_data.title" />
                        </el-form-item>
                    </div>
                    <!-- Content -->
                    <label class="col-4 col-lg-1 mt-lg-4 text-lg-center">*{{$t('setting.push_notify.內容')}}</label>
                    <div class="col-12 col-lg-6 mt-lg-4">
                        <el-form-item prop="content" class="mb-0">
                            <el-input v-model="form_data.content" />
                        </el-form-item>
                    </div>
                </div>
                <div class="d-flex flex-wrap align-items-center">
                    <!-- Route -->
                    <label class="col-4 col-lg-1 mt-lg-4 text-lg-center">{{$t('setting.push_notify.導向路徑')}}</label>
                    <div class="col-12 col-lg-4 mt-lg-4">
                        <el-form-item prop="route" class="mb-0">
                            <el-input v-model="form_data.route" placeholder="/dashboard" @change="is_route_exist" />
                        </el-form-item>
                    </div>
                    <button class="btn btn-success ms-lg-2 mt-2 mt-lg-4 col-12 col-lg-auto" @click.prevent="open_route">{{$t('setting.push_notify.測試')}}</button>
                </div>
                <div class="d-flex flex-wrap align-items-center">
                    <!-- rule -->
                    <label class="col-4 col-lg-1 mt-lg-4 text-lg-center">{{$t('setting.push_notify.發送條件')}}</label>
                    <div class="col-12 col-lg-4 mt-lg-4">
                        <el-form-item prop="rule" class="mb-0">
                            <el-select v-model="form_data.rule" class="w-100"
                            @change="rule_change">
                                <el-option value="all" :label="$t('setting.push_notify.rule.全部')"/>
                                <el-option value="user_level" :label="$t('setting.push_notify.rule.使用者等級')"/>
                                <el-option value="user_list" :label="$t('setting.push_notify.rule.使用者列表')"/>
                                <el-option value="superuser" :label="$t('setting.push_notify.rule.限超級使用者')"/>
                            </el-select>
                        </el-form-item>
                    </div>
                    <div class="col-lg-2"></div>
                    <!-- platform -->
                    <label class="col-4 col-lg-1 mt-2 mt-lg-4 text-lg-center">*{{$t('setting.push_notify.platform')}}</label>
                    <div class="col-12 col-lg-4 mt-lg-4">
                        <el-form-item prop="platform" class="mb-0">
                            <el-checkbox v-model="form_data.platform.ios">
                                <template #default>
                                    <i class="fa-brands fa-apple fs-4"></i>
                                </template>
                            </el-checkbox>
                            <el-checkbox v-model="form_data.platform.android">
                                <template #default>
                                    <i class="fa-brands fa-android fs-4"></i>
                                </template>
                            </el-checkbox>
                        </el-form-item>
                    </div>
                </div>
                <div class="d-flex flex-wrap flex-column" v-if="['user_list', 'user_level'].includes(form_data.rule)">
                    <!-- send_to -->
                    <label class="col-lg-12 mt-4 mt-lg-4">*{{$t('setting.push_notify.發送給')}}
                        <span class="fw-light ms-4" style="font-size: .75rem;">
                            <i class="fas fa-exclamation-circle"></i>{{$t("setting.push_notify.sep_by_comma")}}
                        </span>
                    </label>
                    <div class="col-12">
                        <el-form-item prop="send_to" class="mb-0">
                            <el-input v-model="form_data.send_to" :autosize="{ minRows: 2, maxRows: 5 }" type="textarea" />
                        </el-form-item>
                    </div>
                </div>
            </el-form>
            <div class="w-100 d-flex flex-wrap mt-4 align-items-center">
                <label class="me-2">
                    <i class="fa-solid fa-circle-info"></i>
                    請謹慎填寫標題內容與選擇接收用戶！
                    CAREFULLY Choose who to send and what to write!
                </label>
                <button class="btn btn-primary col-12 col-lg-auto mt-2 mt-lg-0 ms-auto" @click="send">{{$t('setting.push_notify.傳送')}}</button>
            </div>
        </div>
    </div>
</template>

<script>
import { ElMessage } from 'element-plus'

export default {
    name: "SendNotification",
    data(){
        return {
            form_data: {
                title: null,
                content: null,
                route: "/dashboard",
                rule: 'all',
                send_to: '',
                platform: {
                    android: true,
                    ios: true
                }
            },
            rules: {
                content: [
                    { required: true, message: this.$i18n.t('setting.push_notify.content_can_not_empty'), trigger: 'blur' },
                ],
                route: [
                    { required: true, message: this.$i18n.t('setting.push_notify.router_can_not_empty'), trigger: 'blur' },
                    { validator: this.check_router_error, message: this.$i18n.t('setting.push_notify.router_error'), trigger: 'blur' }
                ],
                platform: [
                    { validator: this.check_platform, message: this.$i18n.t('setting.push_notify.at_least_one_platform_should_select'), trigger: 'blur' }
                ],
                send_to: [
                    { required: true, message: this.$i18n.t('setting.push_notify.send_to_can_not_empty'), trigger: 'blur' },
                ]
            },
            is_loading: false,
            router_error: false,
        }
    },
    methods:{
        is_route_exist(){
            if(this.form_data.route != null && this.form_data.route != ""){
                let l = this.$router.resolve(this.form_data.route)
                if( l.matched.length > 0){
                    this.router_error = true
                    return true
                }else{
                    this.router_error = false
                    return false
                }
            }
            return false
        },
        check_router_error(){
            return this.router_error
        },
        async open_route(){
            if(this.is_route_exist()){
                window.open(this.form_data.route)
            }else{
                await this.$refs.user_form.validateField('route')
            }
        },
        check_platform(){
            return !(this.form_data.platform.ios == false && this.form_data.platform.android == false)
        },
        rule_change(){
            if(this.form_data.rule == 'user_level'){
                this.form_data.send_to = '1,2,3'
            }else if(this.form_data.rule == 'user_list'){
                this.axios.get('get_all_users_data?per_page=10000').then(data=>{
                    let username_list = []
                    data.data.data.users_list.forEach(c=>{
                        username_list.push(c.username)
                    })
                    this.form_data.send_to = username_list.join(',')
                })
            }
        },
        send(){
            console.log(this.form_data)
            this.is_route_exist() // validate url first
            this.$refs.user_form.validate().then(res=>{
                this.is_loading = true
                this.axios.post('/manual_send_push_notification', this.form_data).then(data=>{
                    ElMessage.success({message: this.$i18n.t("成功")})
                    this.is_loading = false
                }).catch(err=>{
                    ElMessage.error({message: this.$i18n.t("失敗")})
                    this.is_loading = false
                })
            }).catch(err=>{
                console.log(err)
            })
        }
    },
    mounted(){
    }
}
</script>