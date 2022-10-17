<template>
    <div class="p-0 mt-3">
        <div class="home_page" ref="home_page">
            <div id="maploader"></div>
            <taiwan3D :get3d-points="cityStations" v-if="cityStations.length != 0" @tw3d-finish="tw3dFinish"
			@map-set-size="map_set_size" />
            <stationChange :city-stations="cityStations" v-if="cityStations.length != 0 && cityStations.length != 0"
			ref="station_change" />
        </div>
    </div>
</template>

<script>
import taiwan3D from '@/components/map/taiwan3D.vue'
import stationChange from '@/components/map/stationChange.vue'

export default {
	name: 'Taiwan3d_map',	
	components: { 
		taiwan3D, stationChange
	},
	data() {
		return {
			cityStations: [],
            stationData: [],
		}
	},
	mounted() {
		let that = this
        this.syncdata = setInterval(function(){
			that.tawian3d_plant_overview()
		}, 1000)
	},
	unmounted(){
		clearInterval(this.syncdata)
	},
	methods: {
		tw3dFinish(){
			//等待taiwan3D mount 好
			//因為request要時間，所以taiwan3D不能馬上載入
			//等初次request下來，tawian3D才載入
			//這邊把 播放自選案紐關掉的
			document.querySelector('.tw_switch').style.display = 'none'
		},
		map_set_size(data){
			//console.log(data)
			document.querySelector("#stationChange").style.left = `${data.width - document.querySelector("#stationChange").clientWidth}px`
		},
		openStation(){
			this.$refs.stationPop.$el.style.display = 'block';			
			document.body.classList.add('lock');
		},
		tawian3d_plant_overview(){
			let that = this
			this.axios.get('/tawian3d_plant_overview').then(function(data){
				//console.log(data.data.data)
				that.cityStations = data.data.data
			})
		},
	}
}
</script>