<template>
    <div>
        <div v-loading="place_data.length == 0 || loading">
            <version-select :all_city="place_data" :all_model="model_data.model_history" :current_model="current_model"
            @update-city="update_city" @update-model="update_model"></version-select>
        </div>
    </div>
</template>
<script>
import versionSelect from '@/components/setting/forecastversion/versionSelect.vue'
export default {
    name: "forecastVersion",
    components: {
        versionSelect
    },
    data(){
        return {
            place_data: [],
            model_data: {},
            city_select: "",
            model_select: "",
            loading: false,
            current_model: ""
        }
    },
    methods: {
        load_forecast_place_parameter(){
            let that = this
            this.axios.post('/setting/load_forecast_parameter', {
                type: "GET",
                status: "place"
            }).then(data=>{
                window.setTimeout(()=>{
                    that.place_data = data.data.data.data
                }, 500)
                console.log(data.data.data.data)
            })
        },
        load_forecast_model_parameter(){
            let that = this
            this.loading = true
            this.current_model = ""
            this.axios.post('/setting/load_forecast_parameter', {
                type: "GET",
                status: "model",
                name: this.city_select
            }).then(data=>{
                window.setTimeout(()=>{
                    that.model_data = data.data.data.data
                    that.current_model = that.model_data.model_reversion
                    that.loading = false
                }, 500)
                console.log(data.data.data.data)
            })
        },
        update_city(city){
            this.city_select = city
            this.load_forecast_model_parameter()
        },
        update_model(model){
            this.model_select = model
            let that = this
            this.axios.post('/setting/load_forecast_parameter', {
                type: "POST",
                status: "model",
                name: this.city_select,
                model: this.model_select
            }).then(data=>{
            })
        }
        
    },
    mounted(){
        this.load_forecast_place_parameter()
    }
}
</script>