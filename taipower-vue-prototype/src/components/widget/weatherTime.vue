<template>
    <div class="card col-12 col-lg-8 p-0 mt-3 me-2 shadow">
        <div class="row g-0">
            <div class="col-12 col-lg-4  col-xxl-6 d-flex justify-content-center align-items-center flex-wrap pt-2">
                <h5 class="ms-lg-2 mb-0" v-if="$store.state.user_data.pageType != 'taipower'">{{time_data.YY}}/{{time_data.mm}}/{{time_data.dd}}</h5>
                <h4 class="display-3 fs-4 me-2" v-else>{{time_data.YY}}/{{time_data.mm}}/{{time_data.dd}}</h4>
                <div class="d-flex align-items-center">
                    <h4 class="display-3" :class="{'fs-4': $store.state.user_data.pageType == 'taipower'}">{{time_data.HH}}</h4>
                    <h4 class="display-3 text-primary clock_flash ms-1 me-1 mb-3" :class="{'fs-4': $store.state.user_data.pageType == 'taipower'}">:</h4>
                    <h4 class="display-3" :class="{'fs-4': $store.state.user_data.pageType == 'taipower'}">{{time_data.MM}}</h4>
                </div>
            </div>
            <div class="col-12 col-lg-8 col-xxl-6 weather-zone">
                <div class="d-flex">
                    <div class="ms-2">
                        <h4 class="display-3 mt-2 temp-color fw-bold"
                        :class="{'fs-2': $store.state.user_data.pageType == 'taipower'}">{{weather_data.temperature}}  °C</h4>
                        <h6 class="mt-2 text-dark">{{$t('降雨機率')}}：{{weather_data.rain}} %</h6>
                        <h6 class="mt-2 text-dark">{{city}}</h6>
                    </div>
                    <div class="ms-auto me-2" :class="{'col-3': $store.state.user_data.pageType == 'taipower'}">
                        <img class="w-100 weather-icon" :src="weather_data.imgurl">
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>

<script>
export default {
    name: "weatherTime",
    props: {
        city: {
            type: String,
            default: "新北市"
        }
    },
    data(){
        return {
            time_data: {
                YY: '--', mm: '--', dd: '--',
                HH: '--', MM: '--', SS: '--'
            },
            weather_data: {
                temperature: '---',
                rain: '---',
                imgurl: '---'
            }
        }
    },
    mounted(){
        this.clockRun()
        this.get_weather_data()
    },
    methods: {
        clockRun(){
			var date = new Date();
			var h = date.getHours(); // 0 - 23
			var m = date.getMinutes(); // 0 - 59
			var s = date.getSeconds(); // 0 - 59
			if(h == 0){
				h = 12;
			}

			h = (h < 10) ? "0" + h : h;
			m = (m < 10) ? "0" + m : m;
			s = (s < 10) ? "0" + s : s;
			
            this.time_data.HH = h
            this.time_data.MM = m
            this.time_data.SS = s
			
			const offset = date.getTimezoneOffset()
			date = new Date(date.getTime() - (offset*60*1000))
			let curr_date = date.toISOString().split('T')[0].split('-')
			this.time_data.YY = curr_date[0]
            this.time_data.mm = curr_date[1]
            this.time_data.dd = curr_date[2]
            
			setTimeout(this.clockRun, 1000);
		},
        get_weather_data(){
            let that = this
            this.axios.post('/get_weather_data', {
                city: this.city
            }).then(data => {
                console.log(that.weather_data)
                for(var key in that.weather_data){
                    if(data.data.data[key] != undefined){
                        that.weather_data[key] = data.data.data[key]
                    }
                }
            })
        }
    },
}
</script>

<style>
.clock_flash {
   animation-duration: 800ms;
   animation-name: blink;
   animation-iteration-count: infinite;
   animation-direction: alternate;
}
.weather-zone {
    background-color: #edf0f4;
    border-top-right-radius: 8px;
    border-bottom-right-radius: 8px;
}

.weather-icon {
    animation: upDown 2s infinite linear;
}

@media (max-width: 991px){
    .weather-zone {
        border-top-right-radius: 0px;
    }
}
</style>