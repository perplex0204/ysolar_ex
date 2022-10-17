<template>
    <div>
        <div class="d-flex flex-wrap mb-3">
            <div class="col-12 col-lg-5 col-xl-4 col-xxl-3">
                <autocomplete @station-select="station_select" :preSelect="$store.state.user_data.pageType == 'taipower'"></autocomplete>
            </div>
            <div class="col-12 col-lg-auto" v-if="station_ID != null">
                <div class="fs-4 text-success ms-lg-2 mt-3 mt-lg-0">
                    <div>{{station_name}}</div>
                </div>
            </div>
        </div>
        <div v-if="station_ID != null">
            <auto-dispatch :station-id="station_ID" :station-collection="station_collection"
            v-if="$store.state.user_data.pageType == 'taipower'"
            :station-name="station_name" />
            <equip-cost :station-id="station_ID" :station-collection="station_collection"
            :station-name="station_name" />
            <wash-cost :station-id="station_ID" :station-collection="station_collection"
            :station-name="station_name" />
        </div>
    </div>
</template>

<script>
import autocomplete from '../autocomplete/lgroup_only.vue'
import equipCost from './dispatch/equip_cost.vue'
import washCost from './dispatch/wash_cost.vue'
import autoDispatch from './dispatch/auto_dispatch.vue'

export default {
    name: "Dispatch",
    components: {
        equipCost,
        autoDispatch,
        washCost,
        autocomplete
    },
    data(){
        return {
            station_ID: null,
            station_collection: null,
            station_name: '',
        }
    },
    methods: {
        station_select(item){
            //console.log(item)
            this.station_ID = item.ID
            this.station_collection = item.collection
            this.station_name = item.name
        },
    }
}
</script>

<style>

</style>