<template>
	<div id="stationChange" class="shadow" :class="{'col-lg-3': $store.state.user_data.pageType == 'taipower'}">
		<div class="hom_station_wrap" :class="{'w-100': $store.state.user_data.pageType == 'taipower'}">
			<div 
			class="hom_station"
			v-for="(station, idx) in cityStations"
			:key="idx">
				<div class="w-100">
					<h2>{{ station.name }}</h2>
				</div>
				
				<div class="homst_btminfo">
					<div 
					class="homst_b_item"
					v-for="( info, idx ) in station.otherInfos"
					:key="idx">
						<h3>{{ info.title }}</h3>
						<i>{{ info.unit }}</i>
						<span>{{ info.numb }}</span>
					</div>
				</div>

			</div>
		</div>
	</div>
</template>

<script>
export default {
	name: 'stationChange',
	props: {
		cityStations: Array
	},
	methods: {
		
	}
}
</script>
<style>
.h1, .h2, .h3, h1, h2, h3{
	margin-top: 0px !important;
}
</style>