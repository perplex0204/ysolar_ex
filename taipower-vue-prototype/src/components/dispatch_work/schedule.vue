<template>
    <div class="mt-3">        
        <dispatch-table :table-data="scheduleData" :current-page="current_page" 
        :total-page="total_page" @dispatch-edit="get_dispatch_data" @page-change="page_change"
        @row-click="preview_dispatch"></dispatch-table>
        <dispatch-page ref="dispatch_page" @reload-table="get_dispatch_overview"></dispatch-page>
    </div>
</template>
<script>
import dispatchTable from "./schedule/dispatch_table.vue"
import dispatchPage from "./dispatch_page.vue"

export default {
    name: "Schedule",
    components: {
        dispatchTable,
        dispatchPage
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
            scheduleData: [
            ],
            current_page: 1,
            total_page: 1,
        }
    },
    methods: {
        get_dispatch_overview(){
            this.axios.post('/get_dispatch_overview', {
                'stage': ['took_wait_date_enter', 'wait_for_dispatch', 'wait_admin_confirm_date'],
                ID: this.stationId,
                dispatch_time: this.dateSelect,
                page: this.current_page
            }).then(data=>{
                console.log(data.data.data)
                this.scheduleData = data.data.data.dispatch_list
                this.total_page = data.data.data.total_page
            })
        },
        get_dispatch_data(dispatch_data, editable=true){
            //console.log(dispatch_data)
            this.axios.post('/get_dispatch_data', {ID: dispatch_data._id}).then(data => {
                //console.log(data.data.data)
                console.log(editable)
                this.$refs.dispatch_page.dispatchData = data.data.data.dispatch_data
                if(editable){
                    this.$refs.dispatch_page.modalControl = {
                        title: this.$i18n.t('dispatch.編輯工單'),
                        editable: editable,
                        level: this.$store.state.user_data.level,
                    }
                }else{
                    this.$refs.dispatch_page.modalControl = {
                        title: this.$i18n.t("dispatch.工單檢視"),
                        editable: editable,
                        level: this.$store.state.user_data.level,
                    }
                }
                this.$refs.dispatch_page.openModal()
            })
        },
        preview_dispatch(data){
            this.get_dispatch_data(data, false)
        },
        page_change(new_page){
            this.current_page = new_page
            this.get_dispatch_overview()
        }
    },
    mounted(){
        this.get_dispatch_overview()
        this.sync_data = window.setInterval(this.get_dispatch_overview, 5000)
    },
    unmounted(){
        window.clearInterval(this.sync_data)
    },
    watch: {
        stationId(){
            this.get_dispatch_overview()
        },
        dateSelect(){
            this.get_dispatch_overview()
        }
    }
}
</script>