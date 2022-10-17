<template>
    <div>
        <div class="card p-4 mt-2">
            <h5><i class="el-icon-warning text-primary"></i>{{$t('setting.dispatch.儀器維運成本')}}</h5>
            <div class="d-flex flex-wrap mb-3">
                <div class="col-12 col-lg-5 col-xl-4 col-xxl-3 mt-2 mt-lg-0">
                    <el-select size="large" class="w-100" v-model="equip_type"
                    @change="all_data_filter">
                        <el-option value="all" :label="$t('全部')" />
                        <el-option value="inv" :label="$t('inverter')" />
                        <el-option value="string" :label="$t('string')" />
                        <el-option value="meter" :label="$t('meter')" />
                        <el-option value="sensor" :label="$t('sensor')" />
                        <el-option value="iot" :label="$t('iot')" />
                    </el-select>
                </div>
            </div>
            <div v-if="stationId != null">
                <equip-table :currentPage="current_page" :totalPage="total_page"
                :tableData="table_data" @page-change="page_change"
                @data-update="data_update"></equip-table>
            </div>
        </div>
    </div>
</template>

<script>
import equipTable from './equip_table.vue'
import { ElMessage } from 'element-plus'

export default {
    name: "Equip Cost",
    components: {
        equipTable
    },
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
    data(){
        return {
            equip_type: 'all',
            current_page: 1,
            total_page: 1,
            all_data: {},
            all_table_data: [],
            table_data: [],
        }
    },
    methods: {
        get_equip_select_setting_dispatch(no_reload=false){
            this.axios.post('/get_equip_select_setting_dispatch', {
                ID: this.stationId,
                collection: this.stationCollection
            }).then(data=>{
                console.log(data.data.data)
                this.all_data = data.data.data
                if(no_reload == false){
                    this.all_data_filter()
                }
                
            })
        },
        all_data_filter(){
                let equip_data = this.all_data.equip_data
                this.current_page = 1
                this.all_table_data = []
                for(var key in equip_data){
                    if(equip_data[key].length > 0){
                        equip_data[key].forEach(equip=>{
                            if(this.equip_type == 'all' || this.equip_type == key){
                                this.all_table_data.push({
                                    place: this.all_data.station_data.station_str.slice(0,(this.all_data.station_data.station_str.length-1)),
                                    type: key,
                                    Device_model: equip.Device_model,
                                    ID: equip.ID,
                                    dispatch_cost: equip.dispatch_cost
                                })
                            }
                            if(key == 'inv' && 'string' in equip && (this.equip_type == 'all' || this.equip_type == 'string')){
                                equip['string'].forEach(string=>{
                                    this.all_table_data.push({
                                        place: this.all_data.station_data.station_str.slice(0,(this.all_data.station_data.station_str.length-1)),
                                        type: 'string',
                                        Device_model: string.Device_model,
                                        ID: string.ID,
                                        dispatch_cost: string.dispatch_cost
                                    })
                                })
                            }
                        })
                    }
                }
                this.total_page = Math.ceil(this.all_table_data.length/10)
                this.set_table_data()
        },
        set_table_data(){
            this.table_data = Array.from(this.all_table_data)
            console.log(this.all_table_data)
            this.table_data = this.table_data.splice((this.current_page-1)*10,
            this.all_table_data.length - (this.current_page-1)*10 >= 10? 10 : 
            this.all_table_data.length - (this.current_page-1)*10)
        },
        page_change(new_page){
            this.current_page = new_page
            this.set_table_data()
        },
        data_update(data){
            this.axios.post('/setting_dispatch_save_equip_param', {
                ID: data.ID,
                type: data.type,
                model: data.Device_model,
                dispatch_cost: data.dispatch_cost
            }).then(data=>{
                this.get_equip_select_setting_dispatch(true)
                ElMessage.success({message: this.$i18n.t("成功")})
            })
        }
    },
    mounted(){
        this.get_equip_select_setting_dispatch()
    },
    watch: {
        stationId(){
            this.get_equip_select_setting_dispatch()
        }
    }
}
</script>

<style>

</style>