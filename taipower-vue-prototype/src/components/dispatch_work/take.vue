<template>
    <div class="mt-3">        
        <dispatch-table :table-data="scheduleData" :current-page="current_page" @page-change="page_change" 
        :total-page="total_page" @dispatch-take="dispatch_take" :emptyText="$t('無資料')"
        @row-click="preview_dispatch"></dispatch-table>
        <dispatch-page ref="dispatch_page"></dispatch-page>
    </div>
</template>
<script>
import dispatchTable from "./take/dispatch_table.vue"
import dispatchPage from "./dispatch_page.vue"

export default {
    name: "Take",
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
                /* {
                    "_id": "1234",
                    "ID": "4567",
                    "place": "測試1/UNIT-01",
                    "name": "20220101-A",
                    "type": "告警檢修",
                    "cost": "50,000",
                    "dispatch_time": "2022-01-01",
                    "maintainer_data": {
                        name: "人員1"
                    }
                }, */
            ],
            current_page: 1,
            total_page: 1,
            tableType: "not_accept" 
        }
    },
    methods: {
        get_dispatch_overview(){
            this.axios.post('/get_dispatch_overview', {
                ID: this.stationId,
                dispatch_time: this.dateSelect,
                'stage': 'wait_for_take',
                page: this.current_page
            }).then(data=>{
                console.log(data.data.data)
                this.scheduleData = data.data.data.dispatch_list
                this.total_page = data.data.data.total_page
            })
        },
        dispatch_take(dispatch_data, editable=true){
            //console.log(data)
            if(editable){
                // Take
                this.axios.post("/dispatch_take", {
                    ID: dispatch_data._id
                }).then(r => {
                    this.axios.post('/get_dispatch_data', {ID: dispatch_data._id}).then(data=>{
                        console.log(data.data.data)
                        this.$refs.dispatch_page.dispatchData = data.data.data.dispatch_data
                        this.$refs.dispatch_page.modalControl = {
                            title: this.$i18n.t("dispatch.take_and_view"),
                            editable: editable,
                            level: this.$store.state.user_data.level,
                        }
                        this.get_dispatch_overview()  // Refreash Table
                        this.$refs.dispatch_page.openModal()
                    })
                })
            }else{
                this.axios.post('/get_dispatch_data', {ID: dispatch_data._id}).then(data=>{
                    console.log(data.data.data)
                    this.$refs.dispatch_page.dispatchData = data.data.data.dispatch_data
                    // Preview
                    this.$refs.dispatch_page.modalControl = {
                        title: this.$i18n.t("dispatch.工單檢視"),
                        editable: editable,
                        level: this.$store.state.user_data.level,
                    }
                    this.$refs.dispatch_page.openModal()
                })
            }
            
        },
        preview_dispatch(data){
            this.dispatch_take(data, false)
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