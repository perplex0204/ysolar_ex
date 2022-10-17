<template>
    <div>
        <!-- manual -->
        <el-popover
            v-if="$store.state.user_data.is_superuser"
            placement="top-start"
            width="fit-content"
            trigger="hover"
        >
            <template #reference>
                <button class="btn d-inline-block"><i class="fa-solid fa-circle-question"></i></button>
            </template>
            <h5><i class="fa-solid fa-face-kiss-wink-heart me-2"></i>Info For Our Dear Superuser</h5>
            <label>Where to store svg?</label>
            <br/>
            <label class="fs-7 fst-italic">Due to possibly station renaming, the SLD folder structure is different from 99M/paets/YuanFu's Version</label>
            <ul>
                <li>pv_plant: solar_static/SLD/plantID/plantID.svg</li>
                <li>pv_lgroup: solar_static/SLD/plantID/lgroupID/lgroupID.svg</li>
                <li>pv_group: solar_static/SLD/plantID/lgroupID/groupID/group.svg</li>
            </ul>
            <label>Currently finding .svg at：</label>
            <label class="fw-bold">{{svgPath}}</label>
        </el-popover>
        <svg-zone :plant_select="[null, null, null]" :svg_path="svgPath" min-height="30vh"></svg-zone>
    </div>
</template>

<script>
import svgZone from "../../stationGraphic/svgZone.vue"

export default {
    name: "droneSld",
    components: {
        svgZone
    },
    props: {
        stationData: {
            type: Object,
            required: true
        }
    },
    data(){
        return {
            svgPath: null,
            parent_data: {}
        }
    },
    mounted(){
        this.ID_get_parent_data()
    },
    methods:{
        get_svg_path(){
            switch(this.stationData.collection){
                case "pv_plant":
                    this.svgPath = `solar_static/SLD/${this.parent_data.ID}/${this.parent_data.ID}.svg`
                    break
                case "pv_lgroup":
                    this.svgPath = `solar_static/SLD/${this.parent_data.PV_ID}/${this.parent_data.ID}/${this.parent_data.ID}.svg`
                    break
                case "pv_group":
                    this.svgPath = `solar_static/SLD/${this.parent_data.PV_ID}/${this.parent_data.lgroup_ID}/${this.parent_data.ID}//${this.parent_data.ID}.svg`
                    break
            }
        },
        ID_get_parent_data(){
            this.axios.post('/ID_get_parent_data', {
                ID: this.stationData.ID
            }).then(data=>{
                this.parent_data = data.data.data
                this.get_svg_path()
            })
        }
    }
}
</script>