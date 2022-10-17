<template>
    <div class="w-100">
        <div class=" col-12 col-lg-12 d-lg-flex mb-1">
            <auto-complete @search-select="search_select" @station-select="station_select" class="col-12 col-lg-3 mb-2"
            :preSelect="$store.state.user_data.pageType == 'taipower'" ></auto-complete>

            <el-popover placement="bottom-start" trigger="click" :width="this.$store.state.isMobile? '95vw': this.$store.state.user_data.pageType == 'taipower' ? '60vw' : 'fit-content'"
            class="date_popover"
            style="max-width: 100vw; overflow-y: scroll;"
            v-if="$store.state.user_data.pageType == 'taipower'">
                <template #reference>
                    <el-button
                        size="large"
                        class="col-12 col-lg-3 col-xl-2 ms-lg-auto mt-3 mt-lg-0 mb-2 mb-lg-0">
                        <i class="far fa-clock"></i>{{$t('時間篩選')}}
                    </el-button>
                </template>
                <timeRangePickerSimple @setDate="setDate"/>
            </el-popover>
        </div>
        <timeRangePickerSimple @setDate="setDate" v-if="$store.state.user_data.pageType != 'taipower'"/>
        
        <forecasting-chart :ID="place_ID" :date_selection="date_selection['date_list']"
                    :place_select="place_select" :place="search" class="mt-3" :mode="date_selection['mode2']"
        ></forecasting-chart>
    </div>
</template>


<script>
import autoComplete from '@/components/autocomplete/all_type.vue'
import TimeRangePickerSimple from "@/components/datepicker/timeRangePickerSimple.vue"
import forecastingChart from "@/components/deep_learning/forecastingChart.vue"

export default {
    name: "powerForecasting",
    components: {
        TimeRangePickerSimple,
        autoComplete,
        forecastingChart
    },
    data() {
        return {
            station: {},
            search: "",
            date_selection: {"date_list": []},
            place_ID: "",
            place_select: false
        }
    },
    methods: {
        station_select(item) {
            if(item.name == '無資料'){
				return false
			}
            this.station = {
                ID_list: [item.ID],
                col_list: [item.collection]
            }
        },
        search_select(item) {
            this.search = item
        },
        setDate(date) {
            this.date_selection = date
            // console.log(this.date_selection)
        },
    },
    watch: {
        search() {
            if (this.search == ""){
                this.place_select = false
            }
        },
        station() {
            this.place_ID = this.station["ID_list"][0]
            this.place_select = true
        }
    }
}

</script>