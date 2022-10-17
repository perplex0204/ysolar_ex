<template>
    <div>
        <button class="btn btn-warning w-100" 
        :class="{'d-none': hideButton}"
        data-bs-toggle="modal" data-bs-target="#modal">
            <div class="d-none d-lg-block">{{$t('新增排程')}}</div>
            <i class="fa-solid fa-plus d-lg-none"></i>
        </button>
        <div class="modal" id="modal">
            <div class="modal-dialog modal-fullscreen-down">
                <div class="modal-content">
                    <div class="modal-header">
                        <!-- 新增 -->
                        <h5 class="modal-title" v-if="schedule_form._id == null && !view_history">{{$t('新增排程')}}</h5>
                        <!-- 載入歷史 -->
                        <div class="d-flex flex-wrap w-100 align-items-center" v-else-if="view_history">
                            <button class="btn btn-warning" @click="view_history = false">
                                <i class="fa-solid fa-angle-left"></i>
                            </button>
                            <h5 class="modal-title ms-auto me-auto" >{{$t('dispatch.載入歷史排程')}}</h5>
                        </div>
                        <!-- 編輯現有 -->
                        <h5 class="modal-title" v-else>{{schedule_form.name}}</h5>
                        <button type="button" class="btn-close" @click="cancel"></button>
                    </div>
                    <div v-if="!view_history">
                        <div class="modal-body">
                            <el-form
                                ref="schedule_form_ref"
                                :model="schedule_form"
                                :rules="schedule_form_rule"
                            >
                                <div class="row">
                                    <div class="col-12 col-lg-6 col-xl-4 col-xxl-3 ms-lg-2 mt-2">
                                        <el-form-item prop="plant_search">
                                            <el-autocomplete
                                                v-model="schedule_form.plant_search"
                                                class="w-100"
                                                :fetch-suggestions="querySearchAsync"
                                                :placeholder="$t('廠區')"
                                                value-key="name"
                                                @select="handleSelect"
                                                size="large"
                                            ></el-autocomplete>
                                        </el-form-item>
                                    </div>
                                    <div class="col-12 col-lg-6 col-xl-4 col-xxl-3 ms-lg-2 mt-2">
                                        <el-form-item prop="name">
                                            <el-input :placeholder="$t('名稱')"  size="large"
                                            v-model="schedule_form.name" />
                                        </el-form-item>
                                    </div>
                                    <div class="col-12 col-lg-6 col-xl-4 col-xxl-3 ms-lg-2 mt-2">
                                        <el-form-item prop="schedule_type">
                                            <el-select :placeholder="$t('類別')" size="large" class="w-100"
                                            v-model="schedule_form.schedule_type">
                                                <el-option
                                                    :label="$t('dispatch.type.regular')"
                                                    value="regular"
                                                >
                                                </el-option>
                                                <el-option
                                                    :label="$t('dispatch.type.wash')"
                                                    value="wash"
                                                >
                                                </el-option>
                                            </el-select>
                                        </el-form-item>
                                    </div>
                                </div>
                                <label class="ms-lg-2 mt-4">{{$t('dispatch.排程')}}</label>
                                <div class="row">
                                    <div class="col-12 col-lg-6 col-xl-4 col-xxl-3 ms-lg-2 mt-2">
                                        <el-form-item prop="repeat">
                                            <el-select :placeholder="$t('dispatch.類別')" size="large" class="w-100" v-model="schedule_form.repeat"
                                            @change="cal_schedule_date">
                                                <el-option
                                                    :label="$t('dispatch.interval.none')"
                                                    value="none"
                                                >
                                                </el-option>
                                                <el-option
                                                    :label="$t('dispatch.interval.temporary')"
                                                    value="temporary"
                                                    v-if="$store.state.user_data.pageType == 'SPS'"
                                                >
                                                </el-option>
                                                <el-option
                                                    :label="$t('dispatch.interval.week')"
                                                    value="week"
                                                >
                                                </el-option>
                                                <el-option
                                                    :label="$t('dispatch.interval.month')"
                                                    value="month"
                                                >
                                                </el-option>
                                                <el-option
                                                    :label="$t('dispatch.interval.quarter')"
                                                    value="quarter"
                                                >
                                                </el-option>
                                                <el-option
                                                    :label="$t('dispatch.interval.half_year')"
                                                    value="half_year"
                                                    v-if="$store.state.user_data.pageType == 'SPS'"
                                                >
                                                </el-option>
                                                <el-option
                                                    :label="$t('dispatch.interval.year')"
                                                    value="year"
                                                >
                                                </el-option>
                                            </el-select>
                                        </el-form-item>
                                    </div>
                                    <div class="col-12 col-lg-6 col-xl-4 col-xxl-3 ms-lg-2 mt-2">
                                        <el-form-item prop="repeat_interval"
                                        :rules="[
                                            {required: true, 
                                                message: this.$i18n.t(`dispatch['repeat_interval_blank']`),trigger: 'blur',
                                            },
                                            { type: 'number', message: $t(`dispatch['repeat_interval_must_number']`)},
                                        ]">
                                            <el-input :placeholder="$t('dispatch.區間間隔')" size="large"
                                            type="number"
                                            v-model.number="schedule_form.repeat_interval"
                                            @change="cal_schedule_date"
                                            :disabled="['none', 'temporary'].includes(schedule_form.repeat)" />
                                        </el-form-item>
                                    </div>
                                    <div class="col-12 col-lg-6 col-xl-4 col-xxl-3 ms-lg-2 mt-2">
                                        <el-form-item prop="starttime">  
                                            <el-date-picker class="w-100" type="date" :placeholder="$t('dispatch.開始日期')" size="large"
                                                format="YYYY-MM-DD"
                                                value-format="YYYY-MM-DD"
                                                v-model="schedule_form.starttime" :disabledDate="(_date)=>{
                                                    if(_date < new Date().setHours(0,0,0,0)){
                                                        return true
                                                    }
                                                    else{
                                                        return false
                                                    }
                                                }"
                                                @change="cal_schedule_date"
                                                :teleported="false">
                                            </el-date-picker>
                                        </el-form-item>
                                    </div>
                                    <div class="col-12 col-lg-6 col-xl-8 col-xxl-9 ms-lg-2 mt-2 ps-3 pe-xxl-0">
                                        <div class="alert alert-info" role="alert">
                                            <div v-if="!['none', 'temporary'].includes(schedule_form.repeat)">
                                                {{$t('dispatch.dispatch_every_1')}}<span v-if="schedule_form.repeat_interval > 1">{{schedule_form.repeat_interval}}</span>{{$t(`dispatch.time_interval.${schedule_form.repeat}`)}}{{$t('dispatch.dispatch_every_2')}}
                                            </div>
                                            <div v-else>
                                                {{$t(`dispatch.time_interval.none`)}}
                                            </div>
                                            <div>
                                                {{$t(`dispatch.開始工作日期`)}}：{{schedule_form.starttime}}
                                                <span v-if="!['none', 'temporary'].includes(schedule_form.repeat)">，
                                                    {{$t(`dispatch.下次工作日期`)}}：{{next_dispatch_time}}
                                                </span>
                                            </div>
                                        </div>
                                    </div>
                                </div>
                            </el-form>
                            
                            <div class="row mt-4 ps-2">
                                <div class="col-12 col-lg-9 mt-2 mt-lg-0 pe-0">
                                    <div class="d-flex mb-1 align-items-center">
                                        {{$t('dispatch.工作內容')}}
                                        <button class="btn btn-success ms-auto me-2" v-if="!group_delete.enable" @click="view_history = true">
                                            <i class="fa-solid fa-clock-rotate-left"></i>
                                        </button>
                                        <button class="btn btn-warning"
                                        @click="group_edit.enable = true" v-if="!group_delete.enable">
                                            <i class="fas fa-plus"></i>
                                        </button>
                                        <button class="btn"
                                        @click="open_group_delete_swappable" v-if="!group_delete.enable">
                                            <i class="fas fa-gear"></i>
                                        </button>
                                        <button class="btn btn-danger ms-auto" v-if="group_delete.enable"
                                        @click="group_delete_save">{{$t('完成')}}</button>
                                    </div>
                                    <div class="card m-2 p-2" v-show="group_delete.enable">
                                        <label class="mb-2 fs-7">{{$t('dispatch.請點選來刪除')}}</label>
                                        <div class="d-flex flex-wrap" ref="group_swappable">
                                            <div class="check_content p-2 ms-2 shaking_div mt-2"
                                            v-for="group in schedule_group" :key="group.name"
                                            :class="{'alert-danger': group_delete.delete_list.includes(group.name), 
                                            }"
                                            @click="group_click_prepare_delete(group.name)"
                                            v-bind:name="group.name"
                                            >
                                                <i class="fas fa-times-circle text-danger"
                                                v-if="group_delete.delete_list.includes(group.name)"></i>
                                                {{group.name}}
                                            </div>
                                        </div>
                                    </div>
                                    <div class="card p-2 me-4 mb-4" v-if="group_edit.enable">
                                        <div class="d-flex align-items-center flex-wrap p-2">
                                            <button class="btn"
                                            @click="group_edit.enable=false"><i class="fas fa-times-circle text-danger"></i></button> 
                                            <label>{{$t('dispatch.群組名稱')}}：</label>
                                            <div class="col-12 col-lg-4">
                                                <el-input v-model="group_edit.name" />
                                            </div>
                                            <button class="btn btn-success ms-lg-auto" @click="group_edit_save">{{$t('儲存')}}</button>
                                        </div>
                                    </div>
                                    <el-collapse class="w-100">
                                        <el-collapse-item v-for="group, i in schedule_group" :key="group.name">
                                            <template #title>
                                                <div class="w-100 d-flex">
                                                    <div v-if="!group.name_edit.enable">
                                                        {{i+1}}. {{group.name}}
                                                    </div>
                                                    <div class="col-12 col-lg-5 col-xl-4 col-xxl-3 d-flex align-items-center" v-if="group.name_edit.enable">
                                                        <el-input size="default" class="mt-2 mb-2" v-model="group.name_edit.name"  />
                                                    </div>
                                                    <button class="btn btn-success mt-2 mb-2 ms-auto" v-if="group.name_edit.enable"
                                                    @click.stop="group_name_edit_save(group)">{{$t('完成')}}</button>
                                                    <button class="ms-auto btn" v-if="!group.name_edit.enable"
                                                    @click.stop="group.name_edit.enable=true">
                                                        <i class="fa-solid fa-pen"></i>
                                                    </button>
                                                </div>
                                            </template>
                                            <div class="d-flex w-100 pe-2">
                                                <label v-if="group.child_delete.enable">{{$t('dispatch.請點選來刪除')}}</label>
                                                <button class="btn btn-primary ms-auto"
                                                v-if="!group.child_delete.enable"
                                                @click="group.child_edit.enable=true">
                                                    <i class="fas fa-plus"></i>
                                                </button>
                                                <button class="btn" @click="open_child_delete_swappable(group, $refs[`child_swappable_${i}`])">
                                                    <i class="fas fa-gear"
                                                    v-if="!group.child_delete.enable"></i></button>
                                                <button class="btn btn-danger ms-auto" v-if="group.child_delete.enable"
                                                @click="child_delete_save(group)">{{$t('儲存')}}</button>
                                            </div>
                                            <div class="d-flex flex-wrap" :ref="`child_swappable_${i}`">
                                                <div class="check_content p-2 ms-2 mt-2"
                                                v-for="child, ii in group.child" :key="child.name"
                                                :class="{'alert-danger': group.child_delete.delete_list.includes(child.name), 
                                                'shaking_div': group.child_delete.enable}" @click="group_click(group, child)"
                                                v-bind:name="child.name">
                                                    <i class="fas fa-times-circle text-danger"
                                                    v-if="group.child_delete.delete_list.includes(child.name)"></i>
                                                    {{`${i+1}-${ii+1} `}}{{child.name}}
                                                </div>
                                            </div>
                                            <div class="card p-2 me-4 mt-2" v-if="group.child_edit.enable==true">
                                            <div class="d-flex align-items-center flex-wrap">
                                                <button class="btn mt-2"
                                                @click="reset_child_edit(group)">
                                                    <i class="fas fa-times-circle text-danger"></i>
                                                </button> 
                                                <label class="mt-2">{{$t('dispatch.項目名稱')}}：</label>
                                                <div class="col-12 col-lg-4 col-xl-5 col-xxl-3">
                                                    <input class="form-control mt-2 " v-model="group.child_edit.name" />
                                                </div>
                                                <label class="mt-2 ms-lg-2">{{$t('dispatch.項目類別')}}：</label>
                                                <div class="col-12 col-lg-4">
                                                    <select class="form-control mt-2" v-model="group.child_edit.category">
                                                        <option value="none" selected>{{$t('dispatch.請選擇類別')}}</option>
                                                        <option value="choice">{{$t('dispatch.正常/異常')}}</option>
                                                        <option value="numeric">{{$t('dispatch.數值')}}</option>
                                                        <option value="normal_choice_na" v-if="!['taipower'].includes($store.state.user_data.pageType)">{{$t('dispatch.正常/異常/NA')}}</option>
                                                        <option value="yes_choice_na" v-if="!['taipower'].includes($store.state.user_data.pageType)">{{$t('dispatch.是/否/NA')}}</option>
                                                    </select>
                                                </div>
                                                <label class="mt-2 ms-lg-2" v-if="group.child_edit.category == 'numeric'">{{$t('dispatch.建議數值')}}：</label>
                                                <div class="col-12 col-lg-5 col-xl-4 col-xxl-3" v-if="group.child_edit.category == 'numeric'">
                                                    <input class="form-control mt-2 " type="number" v-model="group.child_edit.suggest_value" />
                                                </div>
                                                <div class="d-flex ms-lg-2 col-lg-5 col-xl-4 col-xxl-3 mt-2
                                                align-items-center">
                                                    <input class="form-check-input mt-0" type="checkbox" value="" v-model="group.child_edit.photo_required" />
                                                    <label>{{$t('dispatch.需要照片上傳')}}</label>
                                                </div>
                                                <button class="btn btn-success ms-auto mt-2" @click="child_edit_save(group)">{{$t('儲存')}}</button>
                                            </div>
                                        </div>
                                        </el-collapse-item>
                                    </el-collapse>
                                </div>
                                <div class="col-12 col-lg-3 ms-lg-0 mt-2 mt-lg-0 d-flex justify-content-end align-items-start p-0 d-none">
                                    <button class="btn btn-primary" @click="$refs['csv_upload'].click()">上傳設定檔</button>
                                    <input type="file" class="d-none" id="input" ref="csv_upload" accept=".csv">
                                </div>
                            </div>
                        </div>
                        <div class="modal-footer">
                            <button type="button" class="btn btn-danger" @click="delete_schedule"
                            v-if="$store.state.user_data.level >= 3">{{$t('刪除')}}</button>
                            <button type="button" class="btn btn-secondary ms-auto" @click="cancel">{{$t('取消')}}</button>
                            <button type="button" class="btn btn-success" @click="save_schedule">{{$t('儲存')}}</button>
                        </div>
                    </div>
                    <div v-else>
                        <load-history @load-history="load_history" />
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>
<script>
import {Modal} from 'bootstrap'
import { ElMessage } from 'element-plus'
import loadHistory from './load_history.vue'
import {Swappable} from '@shopify/draggable'

export default {
    name: "ScheduleModal",
    components: {
        loadHistory
    },
    data(){
        return {
            schedule_group: [
            ],
            group_edit: {
                name: null,
                enable: false
            },
            group_delete:{
                enable: false,
                delete_list: []
            },
            schedule_form: {
                _id: null,
                ID: null,
                plant_search: "",
                name: null,
                schedule_type: null,
                repeat: "none",
                repeat_interval: 1,
                starttime: null
            },
            schedule_form_rule: {
                plant_search: {
                    required: true,
                    message: this.$i18n.t('dispatch["station_blank"]'),
                    trigger: 'blur',
                },
                name: {
                    required: true,
                    message: this.$i18n.t('dispatch["name_blank"]'),
                    trigger: 'blur',
                },
                schedule_type: {
                    required: true,
                    message: this.$i18n.t('dispatch["schedule_type_not_select"]'),
                    trigger: 'blur',
                },
                repeat: {
                    required: true,
                    message: this.$i18n.t('dispatch["repeat_not_select"]'),
                    trigger: 'blur',
                },
                starttime:{ 
                    required: true,
                    message: this.$i18n.t('dispatch["starttime_blank"]'),
                    trigger: 'blur',
                }
            },
            view_history: false,
            next_dispatch_time: null,
        }
    },
    props: {
        hideButton: {
            type: Boolean,
            default: false
        }
    },
    mounted(){
        this.myModal = new Modal(document.getElementById('modal'), {backdrop: 'static', keyboard: false})
    },
    emits: ['reload-table'],
    methods: {
        //-----------------------------------------------------------------------------
        // Open by parents
        open_modal(data){
            console.log(data)
            this.schedule_form = {
                _id: data._id,
                ID: data.ID,
                plant_search: data.place,
                name: data.name,
                schedule_type: data.schedule_type,
                repeat: data.repeat,
                repeat_interval: data.repeat_interval,
                starttime: data.start_time
            }
            this.schedule_group = [
            ]
            data.group_data.forEach(group => {
                let _group = group
                _group.child_delete = {
                    enable: false,
                    delete_list: [],
                }
                _group.child_edit = {
                    name: null,
                    origin_name: null,
                    category: "none",
                    suggest_value: null,
                    photo_required: false,
                    enable: false,
                }
                _group.name_edit = {
                    name: _group.name,
                    enable: false
                }
                this.schedule_group.push(_group)
            })
            this.cal_schedule_date()
            this.myModal.show()
        },
        //-----------------------------------------------------------------------------
        //open model blank
        open_modal_blank(data={}){
            this.myModal.show()
            if(Object.keys(data).length > 0){
                for(var key in data)
                    this.schedule_form[key] = data[key]
            }
        },
        //-----------------------------------------------------------------------------
        //Plant Select
        async querySearchAsync(queryString, cb) {
			//console.log(queryString)
			//console.log(this.PV_data)
            await this.axios.post('/station_search_regex_lgroup', {
                query: queryString,
                only_lgroup: true
            }).then(data => {
                //console.log(data.data.data)
                if(data.data.data.length == 0){
                    cb([{'name': '無資料'}])
                }else{
                    cb(data.data.data)
                }
            })
			
		},
		handleSelect(item) {
			//console.log(item)
			if(item.name == '無資料'){
				return false
			}
            this.schedule_form.ID = item.ID
            this.$refs.schedule_form_ref.validateField('plant_search')
		},
        //-----------------------------------------------------------------------------
        load_history(data){
            console.log(data)
            this.view_history = false
            data.group_data.forEach(group => {
                let _group = group
                _group.child_delete = {
                    enable: false,
                    delete_list: [],
                }
                _group.child_edit = {
                    name: null,
                    origin_name: null,
                    category: "none",
                    suggest_value: null,
                    photo_required: false,
                    enable: false,
                }
                _group.name_edit = {
                    name: _group.name,
                    enable: false
                }
                this.schedule_group.push(_group)
            })
        },
        //-----------------------------------------------------------------------------
        child_delete_save(group){
            let _new_child_list = []
            group.child_delete.swappable_obj.getDraggableElements().forEach(n=>{
                group.child.forEach(child => {
                    if(child.name == n.getAttribute("name") && !group.child_delete.delete_list.includes(child.name)){
                        _new_child_list.push(child)
                        return
                    }
                })
            })
            group.child = _new_child_list
            group.child_delete.swappable_obj.destroy()
            group.child_delete.delete_list = []
            group.child_delete.enable = false
        },
        group_click(group, child){
            if(group.child_delete.enable){
                if(group.child_delete.delete_list.includes(child.name)){
                    const index = group.child_delete.delete_list.indexOf(child.name)
                    group.child_delete.delete_list.splice(index,1)
                }else{
                    group.child_delete.delete_list.push(child.name)
                }
            }else{
                group.child_edit.enable = true
                group.child_edit.name = child.name
                group.child_edit.origin_name = child.name
                group.child_edit.category = child.category
                group.child_edit.suggest_value = child.suggest_value
                group.child_edit.photo_required = child.photo_required
            }
        },
        open_child_delete_swappable(group, target){
            group.child_delete.enable = true
            group.child_delete.swappable_obj = new Swappable(target, {
                draggable: ".check_content",
                mirror: {
                    constrainDimensions: true,
                },
                delay: 200,
            })
        },
        child_edit_save(group){
            let error_str = ""
            // Error Alert
            if(group.child_edit.name == '' || group.child_edit.name == null){
                error_str += this.$i18n.t('dispatch["name_blank"]')
            }
            if(group.child_edit.category == '' || group.child_edit.category == null || group.child_edit.category == 'none'){
                error_str += `\n${this.$i18n.t('dispatch["category_blank"]')}`
            }
            if(error_str != ""){
                alert(error_str)
                return false
            }
            // Reset 
            group.child_edit.enable = false
            // Delete Original if name_change
            for(var i in group.child){
                if(group.child_edit.origin_name != null && group.child_edit.origin_name != group.child_edit.name){
                    group.child.splice(i,1)
                    break
                }
            }
            // Overide if already exist
            for(var i in group.child){
                let child = group.child[i]
                if(child.name == group.child_edit.name){
                    child.category = group.child_edit.category
                    child.suggest_value = group.child_edit.suggest_value
                    child.photo_required = group.child_edit.photo_required
                    // Reset 
                    group.child_edit.name = null
                    group.child_edit.category = "none"
                    group.child_edit.suggest_value = null
                    group.child_edit.photo_required = false
                    return true
                }
            }
            // push new one
            group.child.push({
                name: group.child_edit.name,
                category: group.child_edit.category,
                suggest_value: group.child_edit.suggest_value,
                photo_required: group.child_edit.photo_required
            })
            // Reset 
            group.child_edit.name = null
            group.child_edit.category = "none"
            group.child_edit.suggest_value = null
            group.child_edit.photo_required = false

        },
        reset_child_edit(group){
            group.child_edit = {
                name: null,
                origin_name: null,
                category: "none",
                suggest_value: null,
                photo_required: false,
                enable: false,
            }
        },
        group_edit_save(){
            if(this.group_edit.name == null || this.group_edit.name == ""){
                alert(this.$i18n.t('dispatch["name_blank"]'))
                return false
            }
            for(var i in this.schedule_group){
                if(this.schedule_group[i].name == this.group_edit.name){
                    alert(this.$i18n.t('dispatch["name_duplicate"]'))
                    return false
                }
            }
            this.schedule_group.push(
                {
                    name: this.group_edit.name, 
                    child: [],
                    child_delete: {
                        enable: false,
                        delete_list: [],
                    },
                    child_edit: {
                        name: null,
                        origin_name: null,
                        category: "none",
                        suggest_value: null,
                        photo_required: false,
                        enable: false,
                    },
                    name_edit:{
                        name: this.group_edit.name,
                        enable: false
                    },
                }
            )
            this.group_edit.enable = false
            this.group_edit.name = null
        },  
        open_group_delete_swappable(){
            this.group_delete.enable = true
            this.group_swappable = new Swappable(this.$refs.group_swappable, {
                draggable: ".check_content",
                mirror: {
                    constrainDimensions: true,
                },
                delay: 200,
            })
        },
        group_click_prepare_delete(name){
            if(this.group_delete.delete_list.includes(name)){
                let index = this.group_delete.delete_list.indexOf(name)
                this.group_delete.delete_list.splice(index, 1)
            }else{
                this.group_delete.delete_list.push(name)
            }
        },
        group_delete_save(){
            this.group_delete.delete_list.forEach(name => {
                for(var i in this.schedule_group){
                    if(this.schedule_group[i].name == name){
                        this.schedule_group.splice(i, 1)
                        break
                    }
                }                
            })
            let new_list = []
            this.group_swappable.getDraggableElements().forEach(n=>{  
                for(var i in this.schedule_group){
                    if(this.schedule_group[i].name == n.getAttribute("name")){
                        new_list.push(this.schedule_group[i])
                        return
                    }
                }              
            })
            this.schedule_group = new_list
            this.group_swappable.destroy()
            this.group_delete.enable = false
            this.group_delete.delete_list = []
        },
        group_name_edit_save(group){
            if(group.name_edit.name == null || group.name_edit.name == ""){
                alert(this.$i18n.t('dispatch["name_blank"]'))
                return false
            }
            group.name_edit.enable = false
            group.name = group.name_edit.name
        },
        // Save this schedule
        save_schedule(){
            //check form validate
            this.$refs.schedule_form_ref.validate((valid) => {
                if (valid) {
                    console.log('submit!')
                    // Schedule Group Data , prepare to send
                    let schedule_group = []
                    this.schedule_group.forEach(group=>{
                        schedule_group.push({
                            name: group.name,
                            child: group.child,
                        })
                    })
                    // Upload to backend
                    this.axios.post('/schedule_data', {
                        schedule_data: this.schedule_form,
                        group_data: schedule_group
                    }).then(data=>{
                        console.log(data.data.data)
                        this.$emit('reload-table')
                        ElMessage.success({message: this.$i18n.t("成功")})
                        this.cancel()
                    }).catch(error=>{
                        if( error.response ){
                            if(error.response.data.error.detail == "Bad Request. Already Exists."){
                                ElMessage.error({message: this.$i18n.t("該排程已經存在")})
                            }
                        }
                        //console.log(error)
                    })
                    
                } else {
                    console.log('error submit!')
                    return false
                }
            })
            
        },
        delete_schedule(){
            const answer = confirm(this.$i18n.t('dispatch["delete_confirm"]'))
            if(answer){
                this.axios.post('schedule_data_delete',{'ID': this.schedule_form._id}).then((data)=>{
                    ElMessage.success({message: this.$i18n.t("成功")})
                    this.$emit('reload-table')
                    this.reset_Modal()
                    this.myModal.hide()
                })
            }
        },
        cancel(){
            this.reset_Modal()
            this.myModal.hide()
        },
        reset_Modal(){
            this.view_history = false
            this.schedule_group = []
            this.schedule_form = {
                _id: null,
                ID: null,
                plant_search: "",
                name: null,
                schedule_type: null,
                repeat: "none",
                repeat_interval: 1,
                starttime: null
            }
            this.group_edit = {
                name: null,
                enable: false
            }
            this.group_delete = {
                enable: false,
                delete_list: []
            }
        },
        cal_schedule_date(){
            this.axios.post('/cal_schedule_date', {
                repeat: this.schedule_form.repeat,
                repeat_interval: this.schedule_form.repeat_interval,
                starttime: this.schedule_form.starttime
            }).then(data=>{
                this.next_dispatch_time = data.data.data.next_dispatch_time
            })
        }
    },
}
</script>
<style scoped>
@media (min-width: 992px){
    .modal-dialog{
        width: 95vw !important;
        max-width: 95vw !important;
    }
}
.draggable-mirror{
    z-index: 2000;
    animation: unset;
}
</style>