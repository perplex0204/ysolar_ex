<template>
    <div class="mb-3">
        <div class="card p-4 mt-3">
            <div class="d-flex flex-wrap align-items-center">
                <h5><i class="fa-solid fas fa-exclamation text-warning me-2"></i>{{$t('setting.tabs.forecastVersion')}}</h5>
            </div>
            <div class="d-lg-flex flex-wrap align-items-center">
                <div class="col-12 col-lg-3 mb-3 mb-lg-0">
                    {{$t('setting.forecastVersion.selectPlace')}}:
                    <el-select v-model="city_select" placeholder="Select" class="col-12 col-lg-7 ms-lg-1">
                        <el-option
                        v-for="item in all_city"
                        :key="item.value"
                        :label="item.label"
                        :value="item.value"
                        >
                        </el-option>
                    </el-select>
                </div>
                <div class="col-12 col-lg-5">
                    {{$t('setting.forecastVersion.selectModel')}}:
                    <el-select v-model="model_select" placeholder="Select" class="col-12 col-lg-4 ms-lg-1" :disabled="$store.state.user_data.level < 3">
                        <el-option
                        v-for="item in all_model"
                        :key="item.value"
                        :label="item.label"
                        :value="item.value"
                        >
                        </el-option>
                    </el-select>
                </div>
            </div>
        </div>
    </div>
</template>
<script>
export default {
    name: "versionSelect",
    props: {
        all_city: {
            type: Array,
            default: function(){
                return []
            }
        },
        all_model: {
            type: Array,
            default: function(){
                return []
            }
        },
        current_model: {
            type: String,
            default: ""
        }
    },
    data(){
        return {
            city_select: "",
            model_select: "",
        }
    },
    emits: ['update-city', 'update-model'],
    methods: {
        update_city(){
            this.$emit('update-city', this.city_select)
        }
    },
    mounted(){
        this.all_city.length > 0 ? this.city_select = this.all_city[0] : null
    },
    watch: {
        all_city(){
            if (this.all_city.length > 0 && this.city_select == ""){
                this.city_select = this.all_city[0].value
                this.update_city()
            }
        },
        city_select(){
            console.log(this.city_select)
            this.update_city()
        },
        current_model(){
            if(this.current_model != ""){
                this.model_select = this.current_model
            }
        },
        model_select(){
            console.log(this.model_select)
            this.$emit('update-model', this.model_select)
        }
    }
}
</script>