<template>
    <div>
        <div class="mt-3 mb-3 card shadow" style="overflow-x: scroll;">
            <el-calendar v-model="calendar_date" ref="calendar_ref" style="min-width: 800px;">
                <template #dateCell="{ data }">
                    <div class="text-main">
                        <label class="text-primary" :class="data.isSelected ? 'is-selected' : ''">
                            {{ data.day.split('-').slice(1).join('-') }}
                        </label>
                        <div class="d-flex flex-column" v-if="(data.day.split('-').slice(1).join('-')) in calendar_data">
                            <div class="card fs-7 mt-2 p-1" v-for="date_data in calendar_data[(data.day.split('-').slice(1).join('-'))].child"
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
                    </div>
                </template>
            </el-calendar>
        </div>
        <dispatch-page ref="dispatch_page" @reload-table="get_dispatch_overview_calendar"></dispatch-page>
    </div>
</template>
<script>
import dispatchPage from "./dispatch_page.vue"
import c from 'assets/js/common.js'

export default {
    name: "Overivew",
    components: {
        dispatchPage,
    },
    props: {
        stationId : {
            default: null
        },
        dateSelect: {
            type: Object,
            default: ()=>{
                return {}
            }
        }
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
                        title: this.$i18n.t('dispatch.工單編輯'),
                        editable: true,
                        level: this.$store.state.user_data.level,
                    }
                    this.$refs.dispatch_page.openModal()
                })
            }
        },
        get_dispatch_overview_calendar(){
            this.axios.post('/get_dispatch_overview_calendar', {
                ID: this.stationId,
                month: this.calendar_month
            }).then(data=>{
                console.log(data.data.data.data)
                this.calendar_data = data.data.data.data
            })
        }
    },
    mounted(){
        //console.log(this.$refs.calendar_ref)
        this.get_dispatch_overview_calendar()
        this.sync_data = window.setInterval(this.get_dispatch_overview_calendar(), 5000)
        this.$watch(
            "$refs.calendar_ref.curMonthDatePrefix",
            (new_value) => {
                this.calendar_month = new_value
                this.get_dispatch_overview_calendar()
            }
        )
    },
    unmounted(){
        window.clearInterval(this.sync_data)
    },
    watch: {
        calendar_date(){
            //console.log(this.calendar_date)
            if(c.formatDate(this.calendar_date).substring(0, 7) != this.calendar_month){
                this.calendar_month = c.formatDate(this.calendar_date).substring(0, 7)
                this.get_dispatch_overview_calendar()
            }
        },
        stationId(){
            this.get_dispatch_overview_calendar()
        }
    }
}
</script>
<style scoped>
.el-calendar:deep(.el-calendar-day){
    height: auto;
    min-height: var(--el-calendar-cell-width);
}
</style>
