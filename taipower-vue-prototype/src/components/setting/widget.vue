<template>
    <div>
        <div v-loading="loading">
            <widget-setting :weatherTime="user_parameters.weatherTime" :compareChart="user_parameters.compareChart"
            :taiwan3dMap="user_parameters.taiwan3dMap" :treeMap="user_parameters.treeMap"
            :totalInformationTable="user_parameters.totalInformationTable" :plantHistory="user_parameters.plantHistory"
            :multipleChart="user_parameters.multipleChart" :equipmentCompareChart="user_parameters.equipmentCompareChart"
            :max_number="widget_max_num" :all_city="all_city" :precity="city" :sequenceChart="user_parameters.sequenceChart"
            :dispatchStats="user_parameters.dispatchStats"
            @update="update_parameters" @city_update="city_update"/>
        </div>
    </div>
</template>
<script>
import widgetSetting from "./widget/widget_setting"

export default {
    name: "widget",
    components: {
        widgetSetting
    },
    data() {
        return {
            user_parameters: {
                weatherTime: true,
                compareChart: true,
                taiwan3dMap: false,
                treeMap: false,
                totalInformationTable: true,
                plantHistory: false,
                multipleChart: true,
                equipmentCompareChart: false,
                sequenceChart: false,
                dispatchStats: false
            },
            widget_max_num: 3,
            loading: false,
            city: "",
            all_city: []
        }
    },
    methods: {
        load_user_widget_parameter(){
            this.loading = true
            let that = this
            this.axios.get('/setting/load_user_widget_parameter').then(data=>{
                // console.log(data.data.data)
                window.setTimeout(()=>{
                    that.user_parameters = data.data.data.widget_data
                }, 500)
                that.widget_max_num = data.data.data.widget_max_num
                // console.log(data.data.data.widget_data.city_select)
                that.city = data.data.data.widget_data.city_select
                console.log(that.city)
                that.loading = false
                that.load_widget_city()
            }).catch(error => {
                console.log(error)
                that.loading = false
            })
        },
        update_parameters(key, data){
            // console.log(key, data)
            this.user_parameters[key] = data
            var number = 0
            var array = Object.values(this.user_parameters)
            for (var i=0; i<array.length; i++){
                if (array[i] == true){
                    number += 1
                }
            }
            // console.log(number)
            // console.log(this.widget_max_num)
            if (number > this.widget_max_num){
                alert(`最多選取${this.widget_max_num}個小工具!`)
                this.over_limit(key)
            }
            // console.log(array)
            // console.log(this.user_parameters)
            else{
                this.axios.post('/setting/load_user_widget_parameter', 
                    {
                        user_parameters: this.user_parameters,
                        city: this.city
                    }).then(data=>{

                    }).catch(error => {
                        console.log(error)
                    })
            }
        },
        over_limit(key) {
            window.setTimeout(()=>{
                this.user_parameters[key] = false
                this.axios.post('/setting/load_user_widget_parameter', 
                    {
                        user_parameters: this.user_parameters,
                        city: this.city
                    }
                    ).then(data=>{

                    }).catch(error => {
                        console.log(error)
                    })
            }, 250)
        },
        city_update(city) {
            this.city = city
            this.axios.post('/setting/load_user_widget_parameter', 
            {
                user_parameters: this.user_parameters,
                city: this.city
            }).then(data=>{

            }).catch(error => {
                console.log(error)
            })
            console.log(this.city)
        },
        load_widget_city() {
            this.loading = true
            let that = this
            this.axios.post('/setting/get_widget_city').then(data=>{
                console.log(data.data.data.data)
                window.setTimeout(()=>{
                    // that.city = data.data.data.data[0]
                    that.all_city = data.data.data.data
                }, 250)
                that.loading = false
            }).catch(error => {
                console.log(error)
                that.loading = false
            })
        }
    },
    mounted(){
        this.load_user_widget_parameter()
    }
}
</script>
