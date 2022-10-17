<template>
    <div>
        <div class="card p-4 mt-2">
            <h5><i class="el-icon-warning text-primary"></i>{{$t('setting.dispatch.模板清洗成本')}}</h5>
            <div v-if="stationId != null">
                <module-table :tableData="table_data" :currentPage="current_page" :totalPage="total_page"
                @data-update="update_wash_cost" />
            </div>
        </div>
    </div>
</template>

<script>
import { ElMessage } from 'element-plus'
import moduleTable from './module_table.vue'

export default {
    name: "Wash Cost",
    props: {
        stationId: {
            type: String,
            required: true
        },
        stationCollection: {
            type: String,
            required: true
        },
        stationName: {
            type: String,
            required: true
        }
    },
    components: {
        moduleTable
    },
    data(){
        return {
            current_page: 1,
            total_page: 1,
            table_data: [],
        }
    },
    methods: {
        get_station_pv_module(){
            this.axios.get(`/get_station_pv_module?ID=${this.stationId}`).then(data=>{
                console.log(data.data.data)
                this.table_data = data.data.data.module_list
            })
        },
        page_change(new_page){
            this.current_page = new_page
        },
        update_wash_cost(data){
            console.log(data.model, data.wash_cost)
            this.axios.post(`/get_station_pv_module`, {
                ID: this.stationId,
                model: data.model,
                wash_cost: data.wash_cost
            }).then(data=>{
                this.get_station_pv_module()
                ElMessage.success({message: this.$i18n.t("成功")})
            })
        },
    },
    mounted(){
        this.get_station_pv_module()
    },
    watch: {
        stationId(){
            this.get_station_pv_module()
        }
    }
}
</script>