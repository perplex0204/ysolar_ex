<template>
    <div class="mb-3" :class="{'d-lg-flex flex-wrap': $store.state.user_data.pageType == 'taipower'}">
        <div class="card p-4 mt-3" :class="{'col-lg-3 me-lg-4': $store.state.user_data.pageType == 'taipower'}">
            <div class="d-flex flex-wrap align-items-center">
                <h5><i class="fa-solid fas fa-cloud-sun text-warning me-2"></i>{{$t('setting.widget.weatherTime')}}</h5>
            </div>
            <div class="d-flex flex-wrap align-items-center">
                {{$t('setting.widget.weatherTime')}}
                <el-switch
                    class="ms-2"
                    size="large"
                    :active-text="$t('setting.parameter.使用')"
                    :inactive-text="$t('setting.parameter.不使用')"
                    v-model="weatherTime_use"
                    @change="update('weatherTime')"
                />
            </div>
            <div class="col-lg-10">
                {{$t('setting.widget.citySelect')}}:
                <el-select v-model="city_select" placeholder="Select" class="col-6 col-lg-2" :class="{'col-lg-6': $store.state.user_data.pageType == 'taipower'}">
                    <el-option
                    v-for="item in all_city"
                    :key="item.value"
                    :label="item.label"
                    :value="item.value"
                    >
                    </el-option>
                </el-select>
            </div>
        </div>

        <div class="card p-4 mt-3" :class="{'col-lg-3 me-lg-4': $store.state.user_data.pageType == 'taipower'}">
            <div class="d-flex flex-wrap align-items-center">
                <h5><i class="fa-solid fas fa-chart-line text-warning me-2"></i>{{$t('setting.widget.compareChart')}}</h5>
            </div>
            <div class="d-flex flex-wrap align-items-center">
                {{$t('setting.widget.compareChart')}}
                <el-switch
                    class="ms-2"
                    size="large"
                    :active-text="$t('setting.parameter.使用')"
                    :inactive-text="$t('setting.parameter.不使用')"
                    v-model="compareChart_use"
                    @change="update('compareChart')"
                />
            </div>
        </div>

        <div class="card p-4 mt-3" :class="{'col-lg-3 me-lg-0': $store.state.user_data.pageType == 'taipower'}">
            <div class="d-flex flex-wrap align-items-center">
                <h5><i class="fa-solid fas fa-map-marked-alt text-warning me-2"></i>{{$t('setting.widget.taiwan3dMap')}}</h5>
            </div>
            <div class="d-flex flex-wrap align-items-center">
                {{$t('setting.widget.taiwan3dMap')}}
                <el-switch
                    class="ms-2"
                    size="large"
                    :active-text="$t('setting.parameter.使用')"
                    :inactive-text="$t('setting.parameter.不使用')"
                    v-model="taiwan3dMap_use"
                    @change="update('taiwan3dMap')"
                />
            </div>
        </div>

        <div class="card p-4 mt-3" :class="{'col-lg-3 me-lg-4': $store.state.user_data.pageType == 'taipower'}">
            <div class="d-flex flex-wrap align-items-center">
                <h5><i class="fa-solid fas fa-sitemap text-warning me-2"></i>{{$t('setting.widget.treeMap')}}</h5>
            </div>
            <div class="d-flex flex-wrap align-items-center">
                {{$t('setting.widget.treeMap')}}
                <el-switch
                    class="ms-2"
                    size="large"
                    :active-text="$t('setting.parameter.使用')"
                    :inactive-text="$t('setting.parameter.不使用')"
                    v-model="treeMap_use"
                    @change="update('treeMap')"
                />
            </div>
        </div>

        <div class="card p-4 mt-3" :class="{'col-lg-3 me-lg-4': $store.state.user_data.pageType == 'taipower'}">
            <div class="d-flex flex-wrap align-items-center">
                <h5><i class="fa-solid fas fa-table text-warning me-2"></i>{{$t('setting.widget.totalInformationTable')}}</h5>
            </div>
            <div class="d-flex flex-wrap align-items-center">
                {{$t('setting.widget.totalInformationTable')}}
                <el-switch
                    class="ms-2"
                    size="large"
                    :active-text="$t('setting.parameter.使用')"
                    :inactive-text="$t('setting.parameter.不使用')"
                    v-model="totalInformationTable_use"
                    @change="update('totalInformationTable')"
                />
            </div>
        </div>

        <div class="card p-4 mt-3" :class="{'col-lg-3 me-lg-0': $store.state.user_data.pageType == 'taipower'}">
            <div class="d-flex flex-wrap align-items-center">
                <h5><i class="fa-solid fas fa-chart-line text-warning me-2"></i>{{$t('setting.widget.plantHistory')}}</h5>
            </div>
            <div class="d-flex flex-wrap align-items-center">
                {{$t('setting.widget.plantHistory')}}
                <el-switch
                    class="ms-2"
                    size="large"
                    :active-text="$t('setting.parameter.使用')"
                    :inactive-text="$t('setting.parameter.不使用')"
                    v-model="plantHistory_use"
                    @change="update('plantHistory')"
                />
            </div>
        </div>

        <div class="card p-4 mt-3" :class="{'col-lg-3 me-lg-4': $store.state.user_data.pageType == 'taipower'}">
            <div class="d-flex flex-wrap align-items-center">
                <h5><i class="fa-solid fas fa-chart-line text-warning me-2"></i>{{$t('setting.widget.multipleChart')}}</h5>
            </div>
            <div class="d-flex flex-wrap align-items-center">
                {{$t('setting.widget.multipleChart')}}
                <el-switch
                    class="ms-2"
                    size="large"
                    :active-text="$t('setting.parameter.使用')"
                    :inactive-text="$t('setting.parameter.不使用')"
                    v-model="multipleChart_use"
                    @change="update('multipleChart')"
                />
            </div>
        </div>

        <div class="card p-4 mt-3" :class="{'col-lg-3 me-lg-4': $store.state.user_data.pageType == 'taipower'}">
            <div class="d-flex flex-wrap align-items-center">
                <h5><i class="fa-solid fas fa-chart-line text-warning me-2"></i>{{$t('setting.widget.equipmentCompareChart')}}</h5>
            </div>
            <div class="d-flex flex-wrap align-items-center">
                {{$t('setting.widget.equipmentCompareChart')}}
                <el-switch
                    class="ms-2"
                    size="large"
                    :active-text="$t('setting.parameter.使用')"
                    :inactive-text="$t('setting.parameter.不使用')"
                    v-model="equipmentCompareChart_use"
                    @change="update('equipmentCompareChart')"
                />
            </div>
        </div>

        <div class="card p-4 mt-3" :class="{'col-lg-3 me-lg-0': $store.state.user_data.pageType == 'taipower'}">
            <div class="d-flex flex-wrap align-items-center">
                <h5><i class="fa-solid fas fa-chart-bar text-warning me-2"></i>{{$t('setting.widget.sequenceChart')}}</h5>
            </div>
            <div class="d-flex flex-wrap align-items-center">
                {{$t('setting.widget.sequenceChart')}}
                <el-switch
                    class="ms-2"
                    size="large"
                    :active-text="$t('setting.parameter.使用')"
                    :inactive-text="$t('setting.parameter.不使用')"
                    v-model="sequenceChart_use"
                    @change="update('sequenceChart')"
                />
            </div>
        </div>

        <div class="card p-4 mt-3" :class="{'col-lg-3 me-lg-2': $store.state.user_data.pageType == 'taipower'}">
            <div class="d-flex flex-wrap align-items-center">
                <h5><i class="fa-solid fas fa-chart-bar text-warning me-2"></i>{{$t('setting.widget.dispatchStats')}}</h5>
            </div>
            <div class="d-flex flex-wrap align-items-center">
                {{$t('setting.widget.dispatchStats')}}
                <el-switch
                    class="ms-2"
                    size="large"
                    :active-text="$t('setting.parameter.使用')"
                    :inactive-text="$t('setting.parameter.不使用')"
                    v-model="dispatchStats_use"
                    @change="update('dispatchStats')"
                />
            </div>
        </div>
    </div>
</template>
<script>
export default {
    name: "widget_setting",
    props: {
        weatherTime: {type: Boolean, default: true},
        compareChart: {type: Boolean, default: true},
        taiwan3dMap: {type: Boolean, default: false},
        treeMap: {type: Boolean, default: false},
        totalInformationTable: {type: Boolean, default: false},
        plantHistory: {type: Boolean, default: false},
        multipleChart: {type: Boolean, default: false},
        equipmentCompareChart: {type: Boolean, default: false},
        sequenceChart: {type: Boolean, default: false},
        dispatchStats: {type: Boolean, default: false}, 
        max_number: {type: Number, default: 3},
        all_city: {type: Array, reqired: true},
        precity: {type: String, reqired: true}
    },
    data(){
        return {
            weatherTime_use: true,
            compareChart_use: true,
            taiwan3dMap_use: false,
            treeMap_use: false,
            totalInformationTable_use: false,
            plantHistory_use: false,
            multipleChart_use: true,
            equipmentCompareChart_use: false,
            sequenceChart_use: false,
            dispatchStats_use: false,
            current_number: 3,

            // options: [{
            //     value: "新北市",
            //     label: '新北市'
            // }],
            city_select: ""
        }
    },
    emits: ['update', 'city_update'],
    methods: {
        update(name){
            if (name == "weatherTime") {
                this.$emit('update', name, this.weatherTime_use ? true:false)
            }
            else if (name == "compareChart") {
                this.$emit('update', name, this.compareChart_use ? true:false)
            }
            else if (name == "taiwan3dMap") {
                this.$emit('update', name, this.taiwan3dMap_use ? true:false)
            }
            else if (name == "treeMap") {
                this.$emit('update', name, this.treeMap_use ? true:false)
            }
            else if (name == "totalInformationTable") {
                this.$emit('update', name, this.totalInformationTable_use ? true:false)
            }
            else if (name == "plantHistory") {
                this.$emit('update', name, this.plantHistory_use ? true:false)
            }
            else if (name == "multipleChart") {
                this.$emit('update', name, this.multipleChart_use ? true:false)
            }
            else if (name == "equipmentCompareChart") {
                this.$emit('update', name, this.equipmentCompareChart_use ? true:false)
            }
            else if (name == "sequenceChart"){
                this.$emit('update', name, this.sequenceChart_use ? true:false)
            }else if(name == "dispatchStats"){
                this.$emit('update', name, this.dispatchStats_use ? true:false)
            }
            this.$emit('city_update', this.city_select)
        }
    },
    mounted(){
        this.weatherTime == false ? this.weatherTime_use = false : this.weatherTime_use = true
        this.compareChart == false ? this.compareChart_use = false : this.compareChart_use = true
        this.taiwan3dMap == false ? this.taiwan3dMap_use = false : this.taiwan3dMap_use = true
        this.treeMap == false ? this.treeMap_use = false : this.treeMap_use = true
        this.totalInformationTable == false ? this.totalInformationTable_use = false : this.totalInformationTable_use = true
        this.plantHistory == false ? this.plantHistory_use = false : this.plantHistory_use = true
        this.multipleChart == false ? this.multipleChart_use = false : this.multipleChart_use = true
        this.equipmentCompareChart == false ? this.equipmentCompareChart_use = false : this.equipmentCompareChart_use = true
        this.sequenceChart == false ? this.sequenceChart_use = false : this.sequenceChart_use = true
        this.dispatchStats == false ? this.dispatchStats_use = false : this.dispatchStats_use = true
        try{
            window.setTimeout(()=>{
                this.precity == "" ? this.city_select = this.all_city[0]["value"] : this.city_select = this.precity
                console.log(this.precity)
                console.log(this.city_select)
            }, 750)
        }
        catch{
            console.log("city error")
            this.city_select = ""
        }
    },
    watch: {
        weatherTime() {
            this.weatherTime == false ? this.weatherTime_use = false : this.weatherTime_use = true
        },
        compareChart() {
            this.compareChart == false ? this.compareChart_use = false : this.compareChart_use = true
        },
        taiwan3dMap() {
            this.taiwan3dMap == false ? this.taiwan3dMap_use = false : this.taiwan3dMap_use = true
        },
        treeMap() {
            this.treeMap == false ? this.treeMap_use = false : this.treeMap_use = true
        },
        totalInformationTable() {
            this.totalInformationTable == false ? this.totalInformationTable_use = false : this.totalInformationTable_use = true
        },
        plantHistory() {
            this.plantHistory == false ? this.plantHistory_use = false : this.plantHistory_use = true
        },
        multipleChart() {
            this.multipleChart == false ? this.multipleChart_use = false : this.multipleChart_use = true
        },
        equipmentCompareChart() {
            this.equipmentCompareChart == false ? this.equipmentCompareChart_use = false : this.equipmentCompareChart_use = true
        },
        sequenceChart() {
            this.sequenceChart == false ? this.sequenceChart_use = false : this.sequenceChart_use = true
        },
        dispatchStats() {
            this.dispatchStats == false ? this.dispatchStats_use = false : this.dispatchStats_use = true
        },
        city_select() {
            this.$emit('city_update', this.city_select)
        }
    }
}
</script>