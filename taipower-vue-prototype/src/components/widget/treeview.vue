<template>
    <div class="card col-12 col-lg-8 p-1 mt-3 me-2 shadow" style="min-height: 500px;">
        <div class="treeview_container"  v-loading="loading">
            <div style="display: flex; align-items: center; padding: 1rem;">
                    <el-select v-model="TreeViewSelect" placeholder="Select" class="date_type_selection"
                    size="large">
                    <el-option
                    v-for="item in options"
                    :key="item.value"
                    :label="item.label"
                    :value="item.value"
                    >
                    </el-option>
                </el-select>
            </div>
            <div style="max-width: 100%; overflow-y: scroll;">
                <organization :station-data="stationData" :zoom="false" v-if="this.TreeViewSelect != ''"></organization>
            </div>
        </div>
    </div>
</template>
<script>
import organization from "@/components/station/Data/organization.vue"
export default {
    name:"treeview",
    components: {
        organization
    },
    data(){
        return {
            TreeViewSelect: '',
            loading : false,
            options:[],
            stationData:{
                "ID": "",
                "collection": "",
            }
        }
    },
    methods:{

    },
    mounted(){
        let that = this
        this.loading = true
        var options = []
        this.axios.get('/tawian3d_plant_overview')
            .then(function (response) {
                var data = response.data.data
                console.log(data)
                for(let i = 0 ; i < data.length; i++){
                    options.push({
                        value:i+1,
                        label:data[i].name,
                        collection:data[i].collection,
                        ID:data[i].ID,
                    })
                }
                console.log(options)
                that.options = options
                that.TreeViewSelect = 1
            })
        this.loading = false
    },
    watch:{
        TreeViewSelect(){
            let that = this
            let select = this.options.find(element => element.value == this.TreeViewSelect)
            that.stationData.ID = select.ID
            that.stationData.collection = select.collection
        }
    }
}
</script>