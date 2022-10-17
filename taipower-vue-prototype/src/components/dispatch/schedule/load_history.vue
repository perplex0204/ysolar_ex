<template>
    <div class="p-3">
        <schedule-table :currentPage="current_page" :tableData="schedule_data"
        :totalPage="total_page" @page-change="(new_page) => { current_page = new_page}"
        @row-dblclick="select_history" />
    </div>
</template>

<script>
import scheduleTable from './schedule_table.vue'

export default {
    name: "Load_history",   
    components: {
        scheduleTable
    },
    data(){
        return {
            current_page: 1,
            total_page: 1,
            schedule_data: []
        }
    },
    emits: ['load-history'],
    methods:{
        select_history(data){
            const answer = confirm(this.$i18n.t('dispatch.載入此筆紀錄'))
            if(answer){
                this.$emit('load-history', data)
            }
        },
        get_schedule_overview(){
            this.axios.post('/get_schedule_overview',{
                ID: null, page: this.current_page, schedule_repeat: "all"
            }).then(data=>{
                //console.log(data)
                this.total_page = data.data.data.total_page
                this.schedule_data = data.data.data.schedule_list
            })
        }
    },
    mounted(){
        this.get_schedule_overview()
        this.sync_data = window.setInterval(this.get_schedule_overview, 5000)
    },
    unmounted(){
        window.clearInterval(this.sync_data)
    }
}
</script>