<template>
    <div class="card col-12 col-lg-8 p-0 mt-3 me-2 shadow mb-2">
        <div class="sequence_container">
            <div style="align-items: center; padding: 1rem;" class="d-lg-flex">
                <auto-complete :preSelect="preSelect" @search-select="search_select" @station-select="station_select" class="col-12 col-lg-3 me-lg-3 mb-2 mb-lg-0"></auto-complete>

                <el-popover placement="bottom-start" trigger="click" :width="this.$store.state.isMobile? '95vw':'fit-content'"
                class="date_popover"
                style="max-width: 100vw; overflow-y: scroll;">
                    <template #reference>
                        <el-button
                            size="large"
                            class="col-12 col-lg-3 col-xl-2 ms-lg-auto mt-3 mt-lg-0 mb-2 mb-lg-0">
                            <i class="far fa-clock"></i>{{$t('時間篩選')}}
                        </el-button>
                    </template>
                    <time-range-picker @setDate="setDate" :initial_mode="'week'" ></time-range-picker>
                </el-popover>
            </div>

            <alarm-sequence-diagram :station="station" :date_selection="date_selection" :shadow="false" :search="search"
            ></alarm-sequence-diagram>
        </div>
    </div>
</template>


<script>
import autoComplete from '@/components/autocomplete/all_type.vue'
import alarmSequenceDiagram from '@/components/alarm/alarmSequenceDiagram.vue'
import TimeRangePicker from "@/components/datepicker/timeRangePicker.vue"
export default {
    name: "sequenceChart",
    data() {
        return {
            station: {},
            search: "",
            date_selection: {},
            preSelect: true
        }
    },
    components: {
        autoComplete,
        alarmSequenceDiagram,
        TimeRangePicker
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
        setDate(data){
            this.date_selection = {
                mode:data.mode,
                start_date:data.date_list[0],
                end_date:data.date_list[1]
            }
        }
    },
    watch: {
        search(){
            if(this.search == ""){
                this.station = {}
            }
        }
    },
    mounted() {
        
    },
    unmounted(){
        
    }
}
</script>

<style scoped>
.sequence_container{
    height: 750px;
    max-height: 750px;
    position: relative;
    min-width: 80%;
    border-radius: .5rem;
    /* box-shadow: 0 0 15px #DEE4EA; */
}
.sequence_container:deep #plot_sequence{
    height: 600px;
    max-height: 600px;
    position: relative;
    min-width: 80%;
    border-radius: .5rem;
    /* box-shadow: 0 0 15px #DEE4EA; */
}
.sequence_container:deep .img{
    box-shadow: none;
    width: 100%;
}
@media(max-width: 991px){
    .sequence_container{
        height: 750px;
        max-height: 750px;
    }
}
</style>