<template>
    <div class="mt-3">        
        <dispatch-table :table-data="scheduleData" :current-page="current_page" 
        :total-page="total_page" @page-change="page_change"
        @row-click="get_dispatch_data"></dispatch-table>
        <dispatch-page ref="dispatch_page"></dispatch-page>
    </div>
</template>
<script>
import dispatchTable from "./dispatch/dispatch_table.vue"
import dispatchPage from "./dispatch_page.vue"

export default {
    name: "Dispatch",
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
                page: this.current_page,
                ID: this.stationId,
                dispatch_time: this.dateSelect,
                'stage': ['dispatched_wait_for_review', 'auto_reviewed_wait_for_manual', 'review_failed']
            }).then(data=>{
                console.log(data.data.data)
                this.total_page = data.data.data.total_page
                this.scheduleData = data.data.data.dispatch_list
            })
        },
        get_dispatch_data(dispatch_data){    
            this.axios.post('/get_dispatch_data', {ID: dispatch_data._id}).then(data=>{
                console.log(data.data.data)
                this.$refs.dispatch_page.dispatchData = data.data.data.dispatch_data
                // Preview
                this.$refs.dispatch_page.modalControl = {
                    title: this.$i18n.t("dispatch.工單檢視"),
                    editable: false,
                    level: this.$store.state.user_data.level,
                }
                this.$refs.dispatch_page.openModal()
            })
            
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
