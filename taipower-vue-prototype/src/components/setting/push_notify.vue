<template>
    <div>
        <send-notification v-if="$store.state.user_data.is_superuser"></send-notification>
        <div class="d-flex flex-wrap align-items-center">
            {{$t('setting.push_notify.enable_push_notify')}}
            <el-switch
                class="ms-2"
                size="large"
                :active-text="$t('setting.push_notify.啟用')"
                :inactive-text="$t('setting.push_notify.關閉')"
                v-model="user_enable_push_notify"
            />
        </div>
        <div class="card p-4 mt-3">
            <div class="d-flex flex-wrap align-items-center">
                <h5><i class="fa-solid fa-mobile text-primary me-2"></i>{{$t('setting.push_notify.行動裝置')}}</h5>
            </div>
            <mobile-device-table :table-data="table_data" :current-page="current_page" 
            :total-page="total_page" @page-change="page_change" @reload-table="my_mobile_device"
            :user-enable-push-notify="user_enable_push_notify"></mobile-device-table>
        </div>
    </div>
</template>

<script>
import mobileDeviceTable from './push_notify/mobile_device_table.vue'
import SendNotification from './push_notify/send_notification.vue'

export default {
    name: "Push_notify",
    components: {
        mobileDeviceTable,
        SendNotification
    },
    data(){
        return {
            current_page: 1,
            total_page: 1,
            table_data: [],
            user_enable_push_notify: true
        }
    },
    methods: {
        my_mobile_device(){
            this.axios.get(`/my_mobile_device?current_page=${this.current_page}`).then(data=>{
                //console.log(data.data.data)
                this.table_data = data.data.data.mobile_list
                this.total_page = data.data.data.total_page
            })
        },
        page_change(new_page){
            this.current_page = new_page
            this.my_mobile_device()
        }
    },
    mounted(){
        this.my_mobile_device()
        this.sync_data = window.setInterval(this.my_mobile_device, 5000)
    },
    unmounted(){
        window.clearInterval(this.sync_data)
    }
}
</script>
