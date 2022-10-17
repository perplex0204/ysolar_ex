<template>
    <div class="card col-12 col-lg-8 p-0 mt-3 me-2 shadow">
        <div class="card-header text-center fw-bold fs-4">
            <i class="fa-solid fa-chart-bar me-3 fs-4"></i>
            {{$t('homePage.dispatch_stats.派工資訊總覽')}}
        </div>
        <div class="p-4">
            <div class="d-flex flex-wrap mb-4">
                <div class="col-12 col-lg-4 mt-2 mt-lg-0">
                    <autocomplete @station-select="station_select" @clear="lgroup_ID = null" />
                </div>
                <el-popover placement="bottom-start" trigger="click" width="fit-content">
                    <template #reference>
                        <el-button
                            size="large"
                            class="col-12 col-lg-4 ms-lg-auto mt-3 mt-lg-0">
                            <i class="far fa-clock"></i>{{$t('時間篩選')}}
                        </el-button>
                    </template>
                    <time-range-picker @setDate="setDate"></time-range-picker>
                </el-popover>
            </div>
            <stats :embed="true" :station-id="lgroup_ID" :date-select="date_selection"></stats>
        </div>
    </div>
</template>

<script>
import stats from '../dispatch/archive/stats.vue'
import autocomplete from '@/components/autocomplete/lgroup_only.vue'
import timeRangePicker from "@/components/datepicker/timeRangePicker.vue"

export default {
    name: "dispatchStats",
    components: {
        stats,
        autocomplete,
        timeRangePicker
    },
    data(){
        return {
            lgroup_ID: null,
            date_selection: {},
        }
    },
    methods: {
        station_select(item){
            this.lgroup_ID = item.ID
        },
        setDate(data){
            this.date_selection = {
                mode:data.mode,
                start_date:data.date_list[0],
                end_date:data.date_list[1]
            }
        },
    }
}
</script>
