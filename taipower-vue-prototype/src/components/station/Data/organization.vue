<template>
    <div class="text-center" style="max-width: 80vw;">
        <org-chart :datasource="ds" :zoom="zoom">
        </org-chart>
    </div>
</template>

<script>
import OrgChart from "./organization/OrganizationChartContainer.vue"
export default {
    name:"Organization",
    components: {
        OrgChart
    },
    props: {
        stationData: {
            type: Object,
            required: true
        },
        zoom : {
            type: Boolean,
            required: false,
            default: true,
        }
    },
    data(){
        return {
            ds:{}
        }
    },
    methods: {
        updateOrgChart(){
            let that = this
            console.log(this.stationData)
            if(this.stationData.ID != undefined){
                this.axios.post("/get_tree_equipment",{
                    plant_id: this.stationData.ID,
                    collection:this.stationData.collection
                }).then(function(data){
                    that.ds = data.data.data.ds
                    //console.log(data.data.data.ds)
                })
            }
        },
    },
    beforeMount(){
        this.updateOrgChart()
    },
    watch:{
        stationData: {
            handler: function(newVal, oldVal) {
                this.updateOrgChart()
            },
            deep: true
        }
    }
}
</script>