<template>
    <div class="mt-2">
        <div class="d-flex flex-wrap mb-3">
            <div class="col-12 col-lg-5 col-xl-4 col-xxl-3">
                <autocomplete @station-select="station_select" :layout="layout" :key="layout"></autocomplete>
            </div>
            <div class="col-12 col-lg-auto" v-if="station_ID != null">
                <div class="fs-4 text-success ms-lg-2 mt-3 mt-lg-0">
                    <div>{{station_name}}</div>
                </div>
            </div>
        </div>
        <div class="d-flex flew-wrap">
            <svg-zone :plant_select="plant_select" :svg_path="svg_path" @change-layout="change_layout"></svg-zone>   <!-- SVG Loading Area -->
        </div>
    </div>
</template>

<script>
import autocomplete from '../autocomplete/sld.vue'
import svgZone from './svgZone.vue'

export default {
    name: "SLD",
    components: {
        autocomplete,
        svgZone
    },
    props: {
        layout: {
            default: 0
        }
    },
    data(){
        return {
            station_ID: "",
            station_name: "",
            plant_select: null,
            svg_path: null,
        }
    },
    methods: {
        station_select(item){
            this.station_name = item.name
            this.station_ID = item.ID 
            this.plant_select = [null, item.PV, item.collection == 'pv_lgroup' ? item.realName : item.lgroup, item.collection == 'pv_group' ? item.realName : null]
            this.SLD_path_analysis(item.PV, item.collection == 'pv_lgroup' ? item.realName : item.lgroup, item.collection == 'pv_group' ? item.realName : undefined)
        },
        SLD_path_analysis(plant, lgroup, svg){
            this.axios.post('/SLD_path_analysis', {
                plant: plant,
                lgroup: lgroup,
                svg: svg,
                layout: this.layout
            }).then( data => {
                let _data = data.data.data
                this.svg_path = `./solar_static/SLD/${_data.plant}/${_data.lgroup}/${_data.svg}.svg`
            })
        },
        change_layout(attr){
            this.SLD_path_analysis(this.plant_select[1], this.plant_select[2], attr)
        },
        reset(){
            this.station_ID = ""
            this.station_name = ""
            this.plant_select = null
            this.svg_path = null
        }
    },
    watch:{
        layout(){
            this.reset()
        }
    }
}
</script>
