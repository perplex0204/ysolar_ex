<template>
    <div class="card p-4">
        <h5><i class="fa-solid fa-screwdriver-wrench text-primary me-2"></i>{{$t('setting.tabs.IEC61850')}}</h5>
        <div class="d-flex flex-wrap mt-2 align-items-center">
            <div class="col-12 col-lg-5 col-xl-4 col-xxl-3">
                <autocomplete @station-select="station_select" :preSelect="$store.state.user_data.pageType == 'taipower'"></autocomplete>
            </div>

        </div>
    </div>
    <div class="mt-3">
        <div class="card p-4">
            <div class="d-flex flex-wrap align-items-center">
                <h5><i class="icon-ttl_sunboard"></i>{{$t('setting.iec61850.設備')}}</h5>
            </div>
            <information-table class="mt-2" :tableData="inverter_data" :commandList="commandList" :loading="loading">
            </information-table>
        </div>
    </div>
</template>
<script>
import autocomplete from "../../autocomplete/all_type.vue"
import informationTable from "./informationTable.vue"
export default {
    name:"iec61850Setting",
    components: {
        autocomplete,
        informationTable
    },
    props:{
        commandList:{
            type:Object,
            require:true,
            default:function(){
                return {}
            }
        }
    },
    data(){
        return {
            ID: null,
            collection: null,
            name: "",
            realName: "",
            equip_obj: {},
            equip_type: null,
            equip: null,
            current_page:1,
            total_page:1,
            inverter_data:[],
            loading : false
        }
    },
    methods:{
        station_select(item){
            this.loading = true
            this.ID = item.ID
            this.collection = item.collection
            this.name = item.name
            this.realName = item.realName
            this.rename = null
            this.get_equip_select()
        },
        get_equip_select(){
            this.axios.post('/get_equip_select', {
                ID: this.ID,
                collection: this.collection
            }).then(data=>{
                console.log(data.data.data)
                this.equip_obj = {}
                this.equip_obj['station'] = [{
                    label: this.realName,
                    value: this.collection,
                    ID: this.ID
                }]
                this.equip_type = 'station'
                this.equip = this.ID
                let equip_select = data.data.data
                for(var type in equip_select){
                    if(equip_select[type].length > 0){
                        equip_select[type].forEach(element => {
                            if(!(type in this.equip_obj)){
                                this.equip_obj[type] = []
                            }
                            this.equip_obj[type].push({
                                label: element.name,
                                model: element.Device_model,
                                value: type,
                                ID: element.ID,
                                address:null,
                                values:null,
                                start:null,
                                mac:element.mac,
                            })
                        })
                    }
                }
                this.inverter_data = typeof(this.equip_obj['inv']) != 'undefined' ? this.equip_obj['inv'] : []
                this.loading = false
            }).catch(error => {
                console.log(error)
                this.loading = false
            })

            
        },
    },
    watch:{
        // equip_obj:{
        //     handler(newVal, oldVal){
        //         this.inverter_data = typeof(newVal['inv']) != 'undefined' ? newVal['inv'] : []
        //     },
        //     deep: true
        // }
    },
}
</script>
<style scoped>
</style>