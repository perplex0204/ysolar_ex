<template>
    <div class="w-100">
        <div class=" col-12 col-lg-12 d-lg-flex mb-1">
            <auto-complete @search-select="search_select" @station-select="station_select" class="col-12 col-lg-3 mb-2"
            :preSelect="$store.state.user_data.pageType == 'taipower'" ></auto-complete>
            <div class="col-12 col-lg-5 ms-lg-2">
                <el-select v-model="value" size="large" :disabled="notgroup" class="col-12 col-lg-5" @change="getLabel" :placeholder="$t('option.請選擇')">
                    <el-option
                        v-for="item in options"
                        :key="item.value"
                        :label="item.label == '案場總錶' ? $t(`option.${item.label}`) : item.label"
                        :value="item.value"
                    >
                    </el-option>
                </el-select>
            </div>

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
        <twin-chart :ID="place_ID" :date_selection="date_selection['date_list']"
                    :place_select="place_select" :place="search" :subplace="subplace" class="mt-3"
        ></twin-chart>

    </div>
</template>


<script>
import autoComplete from '@/components/autocomplete/all_type.vue'
import TimeRangePickerSimple from "@/components/datepicker/timeRangePickerSimple.vue"
import twinChart from "@/components/deep_learning/twinChart.vue"

export default {
    name: "digital_twin",
    components: {
        TimeRangePickerSimple,
        autoComplete,
        twinChart
    },
    data() {
        return {
            station: {},
            value: "",
            options: [],
            notgroup: true,
            search: "",
            date_selection: {"date_list": []},
            place_ID: "",
            place_select: false,
            subplace: ""
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
        get_group() {
            let that=this
            // console.log(this.search)
            if (this.search != "") {
                // console.log(this.station["ID_list"][0])
                this.axios.post('get_equip_select', {
                    ID: this.station["ID_list"][0],
                    collection: this.station["col_list"][0]
                }).then(data => {
                    // console.log(data.data.data.inv)
                    that.options_produce(this.station["ID_list"][0], data.data.data.inv)
                })
            }
        },
        options_produce(group_ID, invs) {
            if (this.search != "") {
                this.options = []
                this.options.push({
                    value: group_ID,
                    label: "案場總錶"
                })
                for (var i=0; i<invs.length; i++){
                    this.options.push({
                        value: invs[i]["ID"],
                        label: invs[i]["name"]
                    })
                }
                this.notgroup = false
                this.value = this.options[0]["value"]
                this.getLabel(this.value)
            }
        },
        setDate(date) {
            this.date_selection = date
            // console.log(this.date_selection)
        },
        getLabel(val) {
            let obj = {}
            obj = this.options.find((item) => {
                return item.value == val
            })
            this.subplace = obj.label
        }
    },
    watch: {
        search() {
            if (this.search != ""){
                this.value = ""
                if (this.station.col_list[0] == "pv_group"){
                    this.get_group()
                }
                else{
                    this.subplace = ""
                    this.options = []
                    this.place_ID = this.station["ID_list"][0]
                    this.place_select = true
                    this.notgroup = true
                }
            }
            else if (this.search == "") {
                this.options = []
                this.value = ""
                this.subplace = ""
                this.notgroup = true
                this.place_select = false
            }
        },
        value() {
            if(this.value != ""){
                this.place_select = true
                this.place_ID = this.value
            }
        },
        "station.ID_list": function() {
            if (this.search != ""){
                this.value = ""
                if (this.station.col_list[0] == "pv_group"){
                    this.get_group()
                }
                else{
                    this.subplace = ""
                    this.options = []
                    this.place_ID = this.station["ID_list"][0]
                    this.place_select = true
                    this.notgroup = true
                }
            }
            else if (this.search == "") {
                this.options = []
                this.value = ""
                this.subplace = ""
                this.notgroup = true
                this.place_select = false
            }
            console.log(this.place_ID)
        }
    }
}

</script>