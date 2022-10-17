<template>
    <div class="stationtab_power">
        <div class="d-lg-flex mb-3">
            <div class="complete mt-2 me-lg-3 col-lg-3" >
                <auto-complete @search-select="search_select" @station-select="station_select" :preSelect="$store.state.user_data.pageType == 'taipower'"
            ></auto-complete>
            </div>
            <div :class="{'col-lg-5': $store.state.user_data.pageType == 'taipower'}">
                <dateMonthPicker
                    :parentIsDisabled="false"
                    @set-date="setDate"
                />
            </div>
        </div>
        <heat-map-display :x_axis="x_axis" :y_axis="y_axis"
                          :z_axis="z_axis" :date="dateSelected"
                          :place="search"
        >
        </heat-map-display>
    </div>
</template>



<script>
import dateMonthPicker from "@/components/datepicker/dateMonthPicker.vue"
import heatMapDisplay from "@/components/analysis/heatMapDisplay.vue"
import { ElLoading } from 'element-plus'
import autoComplete from '@/components/autocomplete/group_only.vue'
export default {
    name: "shortCurrentHeatMap",
    components: {
        dateMonthPicker,
        heatMapDisplay,
        autoComplete
    },
    data() {
        return {
            dateSelected: "",
            search: "",
            group_select: {'ID_list': [], 'col_list': []},
            x_axis: [],
            y_axis: [],
            z_axis: []
        }
    },
    methods: {
        setDate(data){
            this.dateSelected = data
            // console.log(this.dateSelected)
            
        },
        station_select(item) {
            if(item.name == '無資料'){
				return false
			}
            this.group_select = {
                ID_list: [item.ID],
                col_list: [item.collection]
            }
        },
        search_select(item) {
            this.search = item
        },
        get_heat_map() {
            const loadingInstance = ElLoading.service()
            let that = this
            this.axios.post("get_heat_map_data",{
                "datepicker": this.dateSelected,
                "ID": this.group_select.ID_list[0]
            })
            .then(function(response) {
                // console.log(response.data.data.data.data)
                that.x_axis = response.data.data.data.data.x_axis
                that.y_axis = response.data.data.data.data.y_axis
                that.z_axis = response.data.data.data.data.z_axis
                // that.x_axis = that.x_axis.slice(108, 193)
                that.heatmapYZData()
                // console.log(that.y_axis)
                // console.log(that.z_axis)
                loadingInstance.close()
            })
        },
        heatmapYZData() {
            let y_data = []
            let z_data = []
            for(var i=0; i<this.y_axis.length; i++){
                y_data = y_data.concat(this.y_axis[i])
                z_data = z_data.concat(this.z_axis[i])
            }
            // z_data = z_data.map((string) => {
            //     return string.slice(108, 193)
            //     // return string.slice(108, 181)
            // })
            // console.log(y_data)
            this.y_axis = y_data
            this.z_axis = z_data
        },
    },
    watch: {
        group_select() {
            // console.log(this.group_select.ID_list)
            // console.log(this.dateSelected)
            // console.log(this.search)
            this.get_heat_map()
        },
        dateSelected() {
            if (this.search){
                this.get_heat_map()
            }
        }
    }
}

</script>