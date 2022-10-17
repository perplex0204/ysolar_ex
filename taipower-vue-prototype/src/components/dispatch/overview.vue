<template>
    <div>
        <div class="d-flex flex-wrap">
            <div class="col-2 mt-2 mt-lg-0 ms-auto d-none" v-if="$store.state.user_data.level == 3">
                <el-popover
                    :placement="popover_placement"
                    class="w-100"
                >
                    <template #reference>
                        <button class="btn btn-warning w-100">
                            <i class="fa-solid fa-plus"></i>
                        </button>
                    </template>
                    <div class="d-flex btn" @click="click_modal('alarm')">{{$t('dispatch.手動新增工單')}}</div>
                    <div class="d-flex btn" @click="click_modal('schedule')">{{$t('dispatch.新增排程')}}</div>
                </el-popover>
            </div>
        </div>
        <div class="mt-3 card shadow" style="overflow-x: scroll;">
            <el-calendar v-model="calendar_date" ref="calendar_ref" style="min-width: 800px;">
                <template #dateCell="{ data }">
                    <el-popover
                        width="fit-content"
                        trigger="click"
                    >
                        <template  #reference>
                            <div class="w-100 p-1" style="min-height: var(--el-calendar-cell-width);">
                                <label class="text-primary" :class="data.isSelected ? 'is-selected' : ''">
                                    {{ data.day.split('-').slice(1).join('-') }}
                                </label>
                                <div class="card bg-primary p-1 fs-7" v-if="(data.day.split('-').slice(1).join('-')) in calendar_data">
                                    <label class="text-danger" 
                                    v-if="calendar_data[(data.day.split('-').slice(1).join('-'))].count.alarm > 0">
                                        {{$t('dispatch.type.alarm')}}：{{calendar_data[(data.day.split('-').slice(1).join('-'))].count.alarm}}
                                    </label>
                                    <label class="text-warning"
                                    v-if="calendar_data[(data.day.split('-').slice(1).join('-'))].count.regular+calendar_data[(data.day.split('-').slice(1).join('-'))].count.wash > 0">
                                        {{`${$t('dispatch.type.regular')}/${$t('dispatch.type.wash')}`}}：{{calendar_data[(data.day.split('-').slice(1).join('-'))].count.regular+calendar_data[(data.day.split('-').slice(1).join('-'))].count.wash}}
                                    </label>
                                    <label v-if="calendar_data[(data.day.split('-').slice(1).join('-'))].count.schedule >0">
                                        {{$t('dispatch.排程')}}：{{calendar_data[(data.day.split('-').slice(1).join('-'))].count.schedule}}
                                    </label>
                                </div>
                            </div>
                        </template>
                        <div class="text-center d-flex flex-column">
                            <button class="btn btn-secondary" @click="click_modal('alarm')" v-if="$store.state.user_data.pageType != 'taipower'">{{$t('dispatch.手動新增工單')}}</button>
                            <button class="btn btn-secondary mt-2" @click="click_modal('schedule')">{{$t('dispatch.新增排程')}}</button>
                        </div>
                        <div class="d-flex flex-column" v-if="(data.day.split('-').slice(1).join('-')) in calendar_data">
                            <div class="card fs-7 mt-2 p-1 text-main" v-for="date_data in calendar_data[(data.day.split('-').slice(1).join('-'))].child"
                            :key="date_data._id" @click="date_data_click(date_data)"
                            :class="{'bg-primary': date_data.collection == 'dispatch',
                            'bg-secondary': date_data.collection == 'dispatch_calendar'}">
                                <div>
                                    <label class="me-2">{{$t('電站')}}:</label>
                                    <label>{{date_data.station_name}}</label>
                                </div>
                                <div>
                                    <label class="me-2">{{$t('dispatch.類別')}}:</label>
                                    <label class="me-2" v-for="type in date_data.type"
                                    :key="type">{{$t(`dispatch.type["${type}"]`)}}</label>
                                </div>
                                <el-divider class="fs-7 mt-2 mb-2"></el-divider>
                                <div v-if="date_data.collection == 'dispatch'">
                                    <label class="me-2">{{$t('dispatch.狀態')}}:</label>
                                    <label class="me-2">{{$t(`dispatch.stage["${date_data.stage}"]`)}}</label>
                                </div>
                                <div v-if="date_data.collection == 'dispatch'">
                                    <label class="me-2">{{$t('dispatch.維運人員')}}:</label>
                                    <label class="me-2">{{date_data.maintainer_name}}</label>
                                </div>
                                <el-divider class="fs-7 mt-2 mb-2"></el-divider>
                                <div>
                                    <label class="me-2" v-if="date_data.collection == 'dispatch'">{{$t('dispatch.單號')}}:</label>
                                    <label class="me-2" v-else>{{$t('dispatch.排程名稱')}}:</label>
                                    <label>{{date_data.name}}</label>
                                </div>
                            </div>
                        </div>
                    </el-popover>
                </template>
            </el-calendar>
        </div>
        <dispatch-page ref="dispatch_page" @reload-table="get_dispatch_overview_calendar"></dispatch-page>
        <schedule-modal ref="schedule_modal" @reload-table="get_dispatch_overview_calendar"
        :hide-button="true"></schedule-modal>
        <create-dispatch-modal ref="create_dispatch_modal" @reload-table="get_dispatch_overview_calendar"
        :hide-button="true"></create-dispatch-modal>
    </div>
</template>
<script>
import dispatchPage from "../dispatch_work/dispatch_page.vue"
import scheduleModal from "./schedule/schedule_modal.vue"
import createDispatchModal from "./wait_for_dispatch/create_dispatch_modal.vue"
import c from 'assets/js/common.js'

export default {
    name: "Overivew",
    components: {
        dispatchPage,
        scheduleModal,
        createDispatchModal
    },
    data(){
        return {
            calendar_date: new Date(),
            calendar_data: {
            
            },
            calendar_month: c.formatDate(new Date()).substring(0, 7),
        }
    },
    methods: {
        date_data_click(dispatch_data){
            console.log(dispatch_data)
            if(dispatch_data.collection == 'dispatch'){
                this.axios.post('/get_dispatch_data', {ID: dispatch_data._id}).then(data => {
                    this.$refs.dispatch_page.dispatchData = data.data.data.dispatch_data
                    this.$refs.dispatch_page.modalControl = {
                        title: this.$i18n.t("dispatch.工單編輯"),
                        editable: true,
                        level: this.$store.state.user_data.level,
                    }
                    this.$refs.dispatch_page.openModal()
                })
            }
            else if(dispatch_data.collection == 'dispatch_calendar'){
                this.axios.post('/get_schedule_data', {ID: dispatch_data.schedule_id}).then(data => {
                    console.log(data.data.data)
                    this.$refs.schedule_modal.open_modal(data.data.data.schedule_data)
                })
            }
        },
        get_dispatch_overview_calendar(){
            this.axios.post('/get_dispatch_overview_calendar', {
                month: this.calendar_month
            }).then(data=>{
                console.log(data.data.data.data)
                this.calendar_data = data.data.data.data
            })
        },
        set_modal_date(){   // 按下新增排成或警報時，時間會是日曆的時間
            const offset = this.calendar_date.getTimezoneOffset()
            let selectDate = new Date(this.calendar_date.getTime() - (offset*60*1000))
            this.$refs.schedule_modal.schedule_form.starttime = selectDate.toISOString().split('T')[0]
            this.$refs.create_dispatch_modal.dispatch_date = selectDate.toISOString().split('T')[0]
        },
        click_modal(mode){
            if(mode == 'alarm')
                this.$refs.create_dispatch_modal.openModal()
            
            else if(mode == 'schedule')
                this.$refs.schedule_modal.open_modal_blank()
        }
    },
    mounted(){
        console.log(this.$refs.calendar_ref)
        this.get_dispatch_overview_calendar()
        this.sync_data = window.setInterval(this.get_dispatch_overview_calendar, 5000)
        this.set_modal_date()
    },
    watch: {
        calendar_date(){
            //console.log(this.calendar_date)
            if(c.formatDate(this.calendar_date).substring(0, 7) != this.calendar_month){
                this.calendar_month = c.formatDate(this.calendar_date).substring(0, 7)
                this.get_dispatch_overview_calendar()
            }
            this.set_modal_date()
        }
    },
    computed: {
        popover_placement(){
            return this.$store.state.isMobile?'bottom': 'bottom-start'
        }
    },
    unmounted(){
        window.clearInterval(this.sync_data)
    }
}
</script>
<style scoped>
.el-calendar:deep(.el-calendar-day){
    height: auto;
    min-height: var(--el-calendar-cell-width);
    padding: 0;
}
</style>
