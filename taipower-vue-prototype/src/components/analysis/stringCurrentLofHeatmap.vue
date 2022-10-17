<template>
    <div>
        <div class="d-flex flex-wrap align-items-center">
            <div class="col-12 col-lg-3">
                <autocomplete @station-select="station_select"></autocomplete>
            </div>
            <div class="col-12 col-lg-auto" v-if="ID != null">
                <div class="fs-4 text-success ms-lg-2 mt-3 mt-lg-0">
                    {{name}}
                </div>
            </div>
            <el-popover placement="bottom-start" trigger="click" :width="this.$store.state.isMobile? '95vw':'fit-content'"
            class="date_popover"
            style="max-width: 100vw; overflow-y: scroll;"
            >
                <template #reference>
                    <el-button
                        size="large"
                        class="col-12 col-lg-2 col-xl-2 ms-lg-auto mt-3 mt-lg-0">
                        <i class="far fa-clock"></i>{{$t('時間篩選')}}
                    </el-button>
                </template>
                <date-picker @setDate="setDate" ></date-picker>
            </el-popover>
        </div>
        <div class="card mt-3 p-2" v-if="ID != null" style="min-height: 60vh;" v-loading="is_loading">
            <div class="w-100" ref="plot_div" style="max-width: 100%;"></div>
        </div>
    </div>
</template>

<script>
import autocomplete from '../autocomplete/group_only.vue'
import datePicker from '../datepicker/timeRangePickerSingle.vue'
import c from 'assets/js/common.js'

export default {
    name: "stringCurrentLofHeatmap",
    components: {
        autocomplete,
        datePicker
    },
    data(){
        return {
            ID: null,
            name: null,
            datepicker: null,
            allData: {},
            is_loading: false,
        }
    },
    methods: {
        station_select(data){
            this.ID = data.ID
            this.name = data.name
            this.pv_heatmap_string_pvlof_plot()
        },
        setDate(date){
            this.datepicker = date.date_list[0]
            this.pv_heatmap_string_pvlof_plot()
        },
        pv_heatmap_string_pvlof_plot(){
            if(this.ID == null || this.datepicker == null)
                return false
            this.is_loading = true
            this.axios.post('/pv_heatmap_string_pvlof_plot', {
                ID: this.ID,
                datepicker: this.datepicker
            }).then(data => {
                this.allData = data.data.data

                let x_data = this.allData.x_axis.slice(108, 181)
                console.log(x_data)
                let [y_data, z_data] = this.heatmapYZData()
                console.log(y_data, z_data)
                let plot_data = [
                    {
                    z: z_data,
                    x: x_data,
                    y: y_data,
                    zmin: 0,
                    zmax: 15,
                    colorscale: [
                        ["0.0", "blue"],
                        ["0.6", "orange"],
                        ["1.0", "red"],
                    ],
                    type: "heatmap",
                    },
                ]

                let layout = this.get_plot_layout()

                this.Plotly.newPlot(this.$refs.plot_div, plot_data, layout, {
                    displaylogo: false,
                    modeBarButtonsToRemove: [
                    "sendDataToCloud",
                    "hoverClosestCartesian",
                    "hoverCompareCartesian",
                    "toggleSpikelines",
                    ],
                })
                c.plot_text_color_fix(this.$refs.plot_div)
                this.is_loading = false
            })
        },
        heatmapYZData() {
            let y_data = []
            let z_data = []
            for(var i in this.allData.y_axis){
                y_data = y_data.concat(this.allData.y_axis[i])
                z_data = z_data.concat(this.allData.z_axis[i])
            }
            z_data = z_data.map((string) => {
                // return string.slice(108, 193)
                return string.slice(108, 181)
            })
            //console.log(y_data, z_data)
            return [y_data, z_data]
        },
        get_plot_layout(){
            return {
                width: this.$refs.plot_div.clientWidth,
                height: this.$refs.plot_div.clientHeight,
                margin: {
                    l: 80,
                    r: 50,
                    b: 40,
                    t: 50,
                    pad: 4,
                },
                title: {
                    text: `${this.name} ${this.datepicker}`,
                    font: {
                        family: "Courier New, monospace",
                        size: 24,
                    },
                },
                paper_bgcolor: "transparent",
                plot_bgcolor: "transparent",
            }
        },
        plot_resize(){
            if('plot_div' in this.$refs){
                window.setTimeout(()=>{
                    this.Plotly.relayout(this.$refs.plot_div, this.get_plot_layout())
                    c.plot_text_color_fix(this.$refs.plot_div)
                }, 500)
            }
        },
    },
    mounted(){
        window.addEventListener("resize", this.plot_resize)
    },
    unmounted(){
        window.removeEventListener("resize", this.plot_resize)
    }
}
</script>
