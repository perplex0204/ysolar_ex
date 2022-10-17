<template>
    <div>
        <div v-show="edit_dispatch_mode == 'none'">
            <div class="d-flex flex-wrap">
                <div class="col-lg-3 col-12">
                    <el-select class="m-2 w-100 mt-4" size="large" placeholder="Select" v-model="select_cursor" ref="select_ref">
                        <el-option
                            :label="$t('dispatch.總覽')"
                            value="overview"
                        >
                        </el-option>
                        <el-option-group
                            :key="'alarm'"
                            :label="$t('dispatch.type.alarm')"
                            v-if="'alarm_list' in dispatchData && dispatchData.alarm_list.length > 0"
                        >
                            <el-option
                            v-for="alarm, i in dispatchData.alarm_list"
                            :key="alarm._id"
                            :label="`${alarm.equip_name}/${alarm.event}`"
                            :value="`alarm_${i}`"
                            >
                                <div :class="{'text-danger': 'alarm' in error_validate && alarm._id in error_validate['alarm'] && show_error_validate}">
                                    <i class="fa-solid fa-triangle-exclamation"
                                    v-if="'alarm' in error_validate && alarm._id in error_validate['alarm'] && show_error_validate"></i>
                                    <span>{{ `${alarm.equip_name}/${alarm.event}` }}</span>
                                </div>
                            </el-option>
                        </el-option-group>
                        <el-option-group
                            :key="'regular'"
                            :label="$t('dispatch.type.regular')"
                            v-if="'regular_list' in dispatchData && dispatchData.regular_list.length > 0"
                        >
                            <el-option
                            v-for="group, i in dispatchData.regular_list"
                            :key="group.name"
                            :label="`${group.name}`"
                            :value="`regular_${i}`"
                            >
                                <div :class="{'text-danger': 'regular' in error_validate && group.name in error_validate['regular'] && show_error_validate}">
                                    <i class="fa-solid fa-triangle-exclamation"
                                    v-if="'regular' in error_validate && group.name in error_validate['regular'] && show_error_validate"></i>
                                    <span>{{ `${group.name}` }}</span>
                                </div>
                            </el-option>
                        </el-option-group>
                        <el-option-group
                            :key="'wash'"
                            :label="$t('dispatch.type.wash')"
                            v-if="'wash_list' in dispatchData && dispatchData.wash_list.length > 0"
                        >
                            <el-option
                            v-for="group, i in dispatchData.wash_list"
                            :key="group.name"
                            :label="`${group.name}`"
                            :value="`wash_${i}`"
                            >
                            </el-option>
                        </el-option-group>
                    </el-select>
                </div>
                <div class="col-lg-2 col-12 mt-4 ms-auto"
                v-if="editable &&  $store.state.user_data.level == 3">
                    <button class="btn btn-warning w-100" @click="edit_dispatch('merge_dispatch')"
                    v-if="!['dispatched_wait_for_review', 'auto_reviewed_wait_for_manual',
                    'review_failed', 'dispatch_finish'].includes(dispatchData.stage)">
                        {{$t('dispatch.合併工單')}}
                    </button>
                </div>
            </div>
            <div>
                <!-- ====================================================================== -->
                <!-- 總覽 -->
                <div class="w-100 p-3" v-if="this.current_display[0] == 'overview'">
                    <el-collapse v-model="overview_collapse">
                        <el-collapse-item name="1"
                        v-if="'alarm_list' in this.dispatchData && this.dispatchData.alarm_list.length > 0">
                            <template #title>
                                <div class="d-flex w-100">
                                    <h6>{{$t('dispatch.type.alarm')}}</h6>
                                    <button class="ms-auto btn" @click.stop="edit_dispatch('alarm')"
                                    v-if="editable &&  $store.state.user_data.level == 3">
                                        <i class="fa-solid fa-gear"></i>
                                    </button>
                                </div>
                            </template>
                            <div v-for="alarm, i in dispatchData.alarm_list"
                            class="fs-6 d-flex" style="cursor: pointer;"
                            @click="select_cursor = `alarm_${i}`"
                            :key="alarm._id">
                                <div class="text-danger me-2" v-if="'alarm' in error_validate && (alarm._id in error_validate['alarm'])">
                                    <i class="fa-solid fa-circle-xmark"></i>
                                </div>
                                <div class="text-success me-2" v-else>
                                    <i class="fa-solid fa-circle-check"></i>
                                </div>
                                {{ `${alarm.equip_name}/${alarm.event}` }}
                            </div>
                        </el-collapse-item>
                        <el-collapse-item name="2"
                        v-if="'regular_list' in this.dispatchData && this.dispatchData.regular_list.length > 0">
                            <template #title>
                                <div class="d-flex w-100">
                                    <h6>{{$t('dispatch.type.regular')}}</h6>
                                    <button class="ms-auto btn" @click.stop="edit_dispatch('regular')"
                                    v-if="editable &&  $store.state.user_data.level == 3">
                                        <i class="fa-solid fa-gear"></i>
                                    </button>
                                </div>
                            </template>
                            <div v-for="group, i in dispatchData.regular_list"
                            class="fs-6 d-flex" style="cursor: pointer;"
                            @click="select_cursor = `regular_${i}`"
                            :key="group.name">
                                <div class="text-danger me-2" v-if="'regular' in error_validate && (group.name in error_validate['regular'])">
                                    <i class="fa-solid fa-circle-xmark"></i>
                                </div>
                                <div class="text-success me-2" v-else>
                                    <i class="fa-solid fa-circle-check"></i>
                                </div>
                                {{ `${group.name}` }}
                            </div>
                        </el-collapse-item>
                        <el-collapse-item name="3"
                        v-if="'wash_list' in this.dispatchData && this.dispatchData.wash_list.length > 0">
                            <template #title>
                                <div class="d-flex w-100">
                                    <h6>{{$t('dispatch.type.wash')}}</h6>
                                    <button class="ms-auto btn" @click.stop="edit_dispatch('wash')"
                                    v-if="editable &&  $store.state.user_data.level == 3">
                                        <i class="fa-solid fa-gear"></i>
                                    </button>
                                </div>
                            </template>
                            <div v-for="group, i in dispatchData.wash_list"
                            class="fs-6 d-flex" style="cursor: pointer;"
                            @click="select_cursor = `wash_${i}`"
                            :key="group.name">
                                <div class="text-danger me-2" v-if="'wash' in error_validate && (group.name in error_validate['wash'])">
                                    <i class="fa-solid fa-circle-xmark"></i>
                                </div>
                                <div class="text-success me-2" v-else>
                                    <i class="fa-solid fa-circle-check"></i>
                                </div>
                                {{ `${group.name}` }}
                            </div>
                        </el-collapse-item>
                    </el-collapse>

                </div>
                <!-- ====================================================================== -->
                <!-- 告警檢修 -->
                <div class="w-100 p-3" 
                v-if="current_display[0] == 'alarm'">
                    <div>
                        <div class="d-flex flex-wrap">
                            <div class="col-12 col-lg-1">
                                <label>{{$t('alarm.警報名稱')}}：</label>
                            </div>
                            <div class="col-12 col-lg-4">
                                <label>{{dispatchData.alarm_list[current_display[1]].event}}</label>
                            </div>
                        </div>
                        <div class="d-flex flex-wrap">
                            <div class="col-12 col-lg-1">
                                <label>{{$t('alarm.廠區')}}：</label>
                            </div>
                            <div class="col-12 col-lg-4">
                                <label>{{`${dispatchData.station_data.name}/${dispatchData.station_data.PV}`}}</label>
                            </div>
                        </div>
                        <div class="d-flex flex-wrap">
                            <div class="col-12 col-lg-1">
                                <label>{{$t('alarm.設備名稱')}}：</label>
                            </div>
                            <div class="col-12 col-lg-4">
                                <label>{{dispatchData.alarm_list[current_display[1]].equip_name}}</label>
                            </div>
                        </div>
                        <div class="d-flex flex-wrap">
                            <div class="col-12 col-lg-1">
                                <label>{{$t('alarm.警報發生')}}：</label>
                            </div>
                            <div class="col-12 col-lg-4">
                                <label>{{dispatchData.alarm_list[current_display[1]].time}}</label>
                            </div>
                        </div>
                        <div class="d-flex flex-wrap">
                            <div class="col-12 col-lg-1">
                                <label>{{$t('alarm.警報修復')}}：</label>
                            </div>
                            <div class="col-12 col-lg-4">
                                <label>{{dispatchData.alarm_list[current_display[1]].returntime}}</label>
                            </div>
                        </div>
                    </div>
                    <el-collapse>
                        <el-collapse-item :title="`${cause.group}/${cause.event}`" 
                        v-for="cause, cause_ID in alarm_list[current_display[1]].cause_data.user_select" :key="cause_ID" >
                            <div class="d-flex align-items-center" v-if="cause.ID != 'else' || Object.keys(alarm_list[current_display[1]].cause_data.user_select).length == 1">
                                <el-radio-group v-model="cause.fix"
                                :class="{'radio_readonly': !editable}"
                                @change="update_dispatch(
                                    dispatchData.alarm_list[current_display[1]].dispatch_ID, alarm_list[current_display[1]]._id, 'alarm', cause)">
                                    <el-radio-button :label="true" :value="true">修復</el-radio-button>
                                    <el-radio-button :label="false" :value="false">未修復</el-radio-button>
                                </el-radio-group>
                                <div class="ms-2 d-flex text-danger align-items-center"
                                v-if="!cause.fix && Object.keys(error_validate).length > 0 && 
                                (cause.ID != 'else' || Object.keys(alarm_list[current_display[1]].cause_data.user_select).length == 1) &&
                                show_error_validate">
                                    <i class="fa-solid fa-triangle-exclamation"></i>
                                    {{$t('dispatch["未完成"]')}}
                                </div>
                            </div>
                            <div class="mt-2">
                                <el-upload
                                    :action="`${this.axios.defaults.baseURL}/dispatch_photo_save`"
                                    list-type="picture-card"
                                    v-if="editable"
                                    :data="{
                                        dispatch_ID:  dispatchData.alarm_list[current_display[1]].dispatch_ID,
                                        type: 'alarm',
                                        alarm_ID: dispatchData.alarm_list[current_display[1]]._id,
                                        cause_ID: cause.ID
                                    }" 
                                    :on-success="(response, file, fileList)=>{
                                        photo_upload_success(response, file, fileList, cause)
                                    }"
                                    :on-preview="photo_upload_preview"
                                    :on-remove="(file)=>{
                                        photo_upload_remove(file.name, dispatchData.alarm_list[current_display[1]].dispatch_ID, 
                                        'alarm', 
                                        dispatchData.alarm_list[current_display[1]]._id, cause.ID)
                                        }"
                                >
                                <!-- Manual Upload when user clicking save -->
                                    <el-icon><plus /></el-icon>
                                </el-upload>
                                <div class="d-flex flex-wrap">
                                    <div class="mt-2 me-2">
                                        <div class="position-relative" style="width: 100px; height: 100px"
                                        v-for="photo_data in cause.photo_data"
                                        :key="photo_data.filename">
                                            <el-image
                                                class="w-100 h-100"
                                                :src="photo_data.filepath"
                                                :preview-src-list="[photo_data.filepath]"
                                                :fit="'cover'"
                                            ></el-image>
                                            <div class="position-absolute top-0 end-0">
                                                <button class="btn fs-6 p-0 text-danger me-2" v-if="editable"
                                                @click="photo_upload_remove(
                                                    photo_data.filename, dispatchData.alarm_list[current_display[1]].dispatch_ID, 
                                                    'alarm', 
                                                    dispatchData.alarm_list[current_display[1]]._id, cause.ID,
                                                    cause.photo_data
                                                )">
                                                    <i class="fa-solid fa-xmark"></i>
                                                </button>
                                            </div>
                                        </div>
                                    </div>
                                </div>
                            </div>
                            <div class="mt-2">
                                <el-input placeholder="說明" v-model="cause.info" :readonly="!editable"
                                @change="update_dispatch(
                                    dispatchData.alarm_list[current_display[1]].dispatch_ID, alarm_list[current_display[1]]._id, 'alarm', cause)" />
                            </div>
                        </el-collapse-item>
                    </el-collapse>
                </div>
                <!-- ====================================================================== -->
                <!-- 清洗與定檢 -->
                <div class="w-100 p-3" v-if="['wash', 'regular'].includes(current_display[0])">
                    <div>
                        <div class="d-flex flex-wrap mb-4">
                            <div class="col-12 col-lg-1">
                                <label>{{$t('dispatch.群組名稱')}}：</label>
                            </div>
                            <div class="col-12 col-lg-4">
                                <label>{{schedule_data[current_display[0]][current_display[1]].name}}</label>
                            </div>
                        </div>
                    </div>
                    <el-collapse>
                        <el-collapse-item v-for="child in schedule_data[current_display[0]][current_display[1]].child"
                        :key="child.name" :title="child.name">
                            <!-- Normal or abnormal choice -->
                            <div v-if="child.category == 'choice'">
                                <el-radio-group v-model="child.choice"
                                :class="{'radio_readonly': !editable}"
                                @change="update_dispatch(schedule_data[current_display[0]][current_display[1]].dispatch_ID, 
                                schedule_data[current_display[0]][current_display[1]].name, 
                                current_display[0], child)">
                                    <el-radio-button label="正常">
                                        <template #default>
                                            <i class="fa-solid fa-check"></i>
                                        </template>
                                    </el-radio-button>
                                    <el-radio-button label="異常">
                                        <template #default>
                                            <i class="fa-solid fa-xmark"></i>
                                        </template>
                                    </el-radio-button>
                                </el-radio-group>
                            </div>
                            <!-- normal_choice_na -->
                            <div v-else-if="child.category == 'normal_choice_na'">
                                <el-radio-group v-model="child.choice"
                                :class="{'radio_readonly': !editable}"
                                @change="update_dispatch(schedule_data[current_display[0]][current_display[1]].dispatch_ID, 
                                schedule_data[current_display[0]][current_display[1]].name, 
                                current_display[0], child)">
                                    <el-radio-button label="y">
                                        <template #default>
                                            {{$t('dispatch.正常')}}
                                        </template>
                                    </el-radio-button>
                                    <el-radio-button label="n">
                                        <template #default>
                                            {{$t('dispatch.異常')}}
                                        </template>
                                    </el-radio-button>
                                    <el-radio-button label="NA">
                                        <template #default>
                                            NA
                                        </template>
                                    </el-radio-button>
                                </el-radio-group>
                            </div>
                            <!-- yes_choice_na -->
                            <div v-else-if="child.category == 'yes_choice_na'">
                                <el-radio-group v-model="child.choice"
                                :class="{'radio_readonly': !editable}"
                                @change="update_dispatch(schedule_data[current_display[0]][current_display[1]].dispatch_ID, 
                                schedule_data[current_display[0]][current_display[1]].name, 
                                current_display[0], child)">
                                    <el-radio-button label="y">
                                        <template #default>
                                            {{$t('dispatch.是')}}
                                        </template>
                                    </el-radio-button>
                                    <el-radio-button label="n">
                                        <template #default>
                                            {{$t('dispatch.否')}}
                                        </template>
                                    </el-radio-button>
                                    <el-radio-button label="NA">
                                        <template #default>
                                            NA
                                        </template>
                                    </el-radio-button>
                                </el-radio-group>
                            </div>
                            <!-- Measurement -->
                            <div v-else-if="child.category == 'numeric'">
                                <div class="mt-2 d-flex flex-wrap">
                                    <div class="col-12 col-lg-1">
                                        <label>{{$t('dispatch["要求值"]')}}:</label>
                                    </div>
                                    <div class="col-12 col-lg-4">
                                        <label>{{child.suggest_value != null ? child.suggest_value: $t('dispatch["無要求"]')}}</label>
                                    </div>
                                </div>
                                <div class="mt-2">
                                    <el-input-number :placeholder="$t('dispatch.數值')" v-model="child.value" :readonly="!editable"
                                    @change="update_dispatch(
                                        schedule_data[current_display[0]][current_display[1]].dispatch_ID, schedule_data[current_display[0]][current_display[1]].name, 
                                    current_display[0], child)" />
                                </div>
                            </div>
                            <div class="ms-2 d-flex text-danger align-items-center"
                            v-if="((['choice', 'normal_choice_na', 'yes_choice_na'].includes(child.category) && child.choice == null) ||
                                (child.category == 'numeric' && child.value == null)) &&
                                Object.keys(error_validate).length > 0 && show_error_validate">
                                <i class="fa-solid fa-triangle-exclamation"></i>
                                {{$t('dispatch["未完成"]')}}
                            </div>
                            <div class="mt-2">
                                <el-upload
                                    :action="`${this.axios.defaults.baseURL}/dispatch_photo_save`"
                                    list-type="picture-card"
                                    v-if="editable"
                                    :data="{
                                        dispatch_ID:  schedule_data[current_display[0]][current_display[1]].dispatch_ID,
                                        type: current_display[0],
                                        group_name: schedule_data[current_display[0]][current_display[1]].name,
                                        child_name: child.name
                                    }" 
                                    :on-success="(response, file, fileList)=>{
                                        photo_upload_success(response, file, fileList, child)
                                    }"
                                    :on-preview="photo_upload_preview"
                                    :on-remove="(file)=>{
                                        photo_upload_remove(file.name, schedule_data[current_display[0]][current_display[1]].dispatch_ID, 
                                        current_display[0], 
                                        schedule_data[current_display[0]][current_display[1]].name, child.name, child.photo_data)
                                        }"
                                >
                                <!-- Manual Upload when user clicking save -->
                                    <el-icon><plus /></el-icon>
                                </el-upload>
                                <div class="d-flex align-items-center" v-if="child.photo_required && child.photo_data.length == 0">
                                    <i class="fa-solid fa-triangle-exclamation text-danger" v-if="Object.keys(error_validate).length > 0 && child.photo_data.length == 0"></i>
                                    <i class="fa-solid fa-circle-exclamation" v-else></i>
                                    {{$t('dispatch["photo_required"]')}}
                                </div>
                                <div class="d-flex flex-wrap">
                                    <div class="mt-2 me-2">
                                        <div class="position-relative" style="width: 100px; height: 100px"
                                        v-for="photo_data in child.photo_data"
                                        :key="photo_data.filename">
                                            <el-image
                                                class="w-100 h-100"
                                                :src="photo_data.filepath"
                                                :preview-src-list="[photo_data.filepath]"
                                                :fit="'cover'"
                                            ></el-image>
                                            <div class="position-absolute top-0 end-0">
                                                <button class="btn fs-6 p-0 text-danger me-2" v-if="editable"
                                                @click="photo_upload_remove(photo_data.filename, 
                                                schedule_data[current_display[0]][current_display[1]].dispatch_ID, current_display[0], 
                                                    schedule_data[current_display[0]][current_display[1]].name, child.name ,child.photo_data)
                                                ">
                                                    <i class="fa-solid fa-xmark"></i>
                                                </button>
                                            </div>
                                        </div>
                                    </div>
                                </div>
                            </div>
                            <div class="mt-2">
                                <el-input :placeholder="$t('dispatch.說明')" v-model="child.info" :readonly="!editable"
                                @change="update_dispatch(schedule_data[current_display[0]][current_display[1]].dispatch_ID, schedule_data[current_display[0]][current_display[1]].name, 
                                current_display[0], child)" />
                            </div>
                        </el-collapse-item>
                    </el-collapse>
                </div>
            </div>
            <!-- Photo Preview -->
            <el-dialog v-model="dialogImage.visible">
                <img class="w-100" :src="dialogImage.url" alt="" />
            </el-dialog>
        </div>
        <edit-alarm v-if="edit_dispatch_mode == 'alarm' && this.dispatchData.alarm_list.length > 0"
        :alarm-data="this.dispatchData.alarm_list" :dispatch-data="dispatchData"
        @dispatch-edit-finish="dispatch_edit_finish"></edit-alarm>
        <edit-schedule v-if="edit_dispatch_mode == 'regular' && this.dispatchData.regular_list.length > 0"
        schedule-type="regular"
        :schedule-data="this.dispatchData.regular_list" :dispatch-data="dispatchData"
        @dispatch-edit-finish="dispatch_edit_finish"></edit-schedule>
        <edit-schedule v-if="edit_dispatch_mode == 'wash' && this.dispatchData.wash_list.length > 0"
        schedule-type="wash"
        :schedule-data="this.dispatchData.wash_list" :dispatch-data="dispatchData"
        @dispatch-edit-finish="dispatch_edit_finish"></edit-schedule>
        <merge-dispatch v-if="edit_dispatch_mode == 'merge_dispatch'"
        :dispatch-id="dispatchData._id"
        :station-id="dispatchData.ID" :dispatch-date="dispatchData.dispatch_time"
        @dispatch-edit-finish="dispatch_edit_finish"></merge-dispatch>
    </div>
</template>
<script>
import { Plus } from '@element-plus/icons-vue'
import editAlarm from './edit_alarm/edit_alarm.vue'
import editSchedule from './edit_schedule/edit_schedule.vue'
import mergeDispatch from './merge_dispatch.vue'

export default {
    name: "Dispatch_content",
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
        Plus,
        editAlarm,
        editSchedule,
        mergeDispatch
    },
    data(){
        return {
            select_cursor: 'overview',
            current_display: ['overview', null],
            alarm_list: [],
            schedule_data: {
                wash: [],
                regular: []
            },
            dialogImage: {
                visible: false,
                url: '#'
            },
            error_validate: {},
            show_error_validate: false,
            edit_dispatch_mode: "none",
            overview_collapse: ["1", "2", "3"]
        }
    },
    methods: {
        init(){
            if('alarm_list' in this.dispatchData && this.dispatchData.alarm_list.length > 0){
                this.alarm_list = this.dispatchData.alarm_list
            }
            if('regular_list' in this.dispatchData && this.dispatchData.regular_list.length > 0){
                this.schedule_data.regular = this.dispatchData.regular_list
            }
            if('wash_list' in this.dispatchData && this.dispatchData.wash_list.length > 0){
                this.schedule_data.wash = this.dispatchData.wash_list
            }
        },
        photo_upload_success(response, file, fileList, data){
            //console.log(response)
            console.log(file)
            data.photo_data.push(response.data)
            file.url = response.data.filepath
            //console.log(fileList)
            window.setTimeout(()=>{
                const index = fileList.indexOf(file.name)
                fileList = fileList.splice(index, 1)
            }, 1000)
        },
        photo_upload_preview(file){
            this.dialogImage.visible = true
            this.dialogImage.url = `${file.url}`
        },
        photo_upload_remove(filename, dispatch_ID, type, alarm_ID, cause_ID, photo_data=null){
            //console.log(filename, dispatch_ID, type, alarm_ID, cause_ID)
            this.axios.post('/dispatch_photo_remove', {
                filename: filename,
                dispatch_ID: dispatch_ID,
                type: type,
                group_ID: alarm_ID,
                child_ID: cause_ID
            }).then(data=>{
                // Old Photo remove
                if(photo_data != null){
                    for(var i in photo_data){
                        if(photo_data[i].filename == filename){
                            photo_data.splice(i, 1)
                            return true
                        }
                    }
                }
            })
        },
        update_dispatch(dispatch_id, ID, type, cause){
            console.log(dispatch_id, type, ID ,cause)
            this.axios.post('/dispatch_update_content', {
                dispatch_ID: dispatch_id,
                ID: ID,
                type: type,
                cause: cause
            }).then(data=>{
                console.log(data.data.data)
            })
        },
        edit_dispatch(mode){
            this.edit_dispatch_mode = mode
            this.$parent.dispatch_in_edit = true
        },
        dispatch_edit_finish(){
            this.axios.post('/get_dispatch_data', {
                ID: this.dispatchData._id
            }).then(data=>{
                //console.log(data.data.data)
                this.$parent.dispatchData = data.data.data.dispatch_data
                this.init()
                this.edit_dispatch_mode = 'none'
                this.$parent.dispatch_in_edit = false
            })
        },
        dispatch_auto_review(){
            this.axios.post('/dispatch_auto_review', {
                dispatch_ID: this.dispatchData._id,
                dispatch_finish: false
            }).then(data=>{
                this.error_validate = data.data.data.error_data
            })
        }
    },
    mounted(){
        this.init()
        this.sync_auto_review = window.setInterval(this.dispatch_auto_review, 1000)
        // inital dispaly
        /* if('alarm_list' in this.dispatchData && this.dispatchData.alarm_list.length > 0){
            this.select_cursor = 'alarm_0'
            this.current_display = ['alarm', 0]
        }
        else if('regular_list' in this.dispatchData && this.dispatchData.regular_list.length > 0){
            this.select_cursor = 'regular_0'
            this.current_display = ['regular', 0]
        }
        else if('wash_list' in this.dispatchData && this.dispatchData.wash_list.length > 0){
            this.select_cursor = 'wash_0'
            this.current_display = ['wash', 0]
        } */
    },
    unmounted(){
        window.clearInterval(this.sync_auto_review)
    },
    watch:{
        select_cursor(){
            //console.log(this.select_cursor)
            this.current_display = this.select_cursor.split('_')
        }
    }
}
</script>
<style>
.infinite-list {
  height: 300px;
  padding: 0;
  margin: 0;
}
.radio_readonly{
    pointer-events: none;
}
</style>
<style scoped>
    .el-collapse:deep(.el-collapse-item__header){
        background-color: transparent;
    }
    .el-collapse:deep(.el-collapse-item__wrap){
        background-color: transparent;
    }
</style>