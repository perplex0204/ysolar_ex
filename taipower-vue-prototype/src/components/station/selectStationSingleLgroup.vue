<template>
	<div class="col-12 col-lg-3 col-xl-2">
		<el-popover placement="bottom-start" trigger="click" popper-class="select_station_popover">
			<template #reference>
				<el-button
					size="large"
					class="w-100"
					:disabled="disable">
					<div v-if="selectedValue.length == 0">
						<i class="icon-nav_home"></i>{{$t('選擇縣市／區域')}}
					</div>
					<div v-else>
						{{selectedValue[1]}}/{{selectedValue[2]}}
					</div>
				</el-button>
			</template>
			<div class="select_s_wrap">
				<div class="select_city">
					<div class="sels_wrap">
						<el-radio-group v-model="selectedCity">
							<el-radio 
							v-for="(item, idx) in nationOpt"
							:key="idx"
							:label="item.value"
							@change="selectCity(item, $event)"></el-radio>
						</el-radio-group>
					</div>
				</div>

				<el-cascader-panel 
				ref="cascaSelect"
				popper-class="select_station_cascader"
				v-model="selectedValue"
				:options="selectedOpt"
				:props="{ multiple: false, value: 'label'}"
				v-show="selectedCity != ''"
				></el-cascader-panel>

			</div>
		</el-popover>
		
	</div>
</template>
<script>
export default {
	name: 'selectStation',
	props: {
		disable: {
			type: Boolean,
			default: false
		}},
	data(){
		return{
			selectedValue: [],
			selectedCity: '',
			selectedOpt: [],
			groupIDLable:{},
			nationOpt: [],
		}
	},
	methods: {
		selectCity(val, e){
			this.selectedValue = [];
			this.selectedOpt = val.children;
			this.$refs['cascaSelect'].$el.style.display = 'flex';
		}
	},
	beforeMount(){
		let that = this
		this.axios.get('/get_select_station').then(function(data){
			that.nationOpt = data.data.data['nationOpt']
			for(var i in that.nationOpt){
				for(var ii in that.nationOpt[i]['children']){
					for(var iii in that.nationOpt[i]['children'][ii]['children']){
						for(var iiii in that.nationOpt[i]['children'][ii]['children'][iii]['children']){
							delete that.nationOpt[i]['children'][ii]['children'][iii]['children'][iiii].children
							//這邊不用選到 group, 所以delete掉
						}
					}
				}
			}
			that.groupIDLable = data.data.data['groupIDLable']
		})
	},
	watch:{
		selectedValue: function(val){
			let ID_select = null
			if(this.$refs['cascaSelect'].getCheckedNodes().length > 0){
				this.$emit("get-ID", this.$refs['cascaSelect'].getCheckedNodes()[0].data.value)
			}
			this.$emit('plant-select', this.selectedValue);   //傳遞已選擇的ID到外層
		}
	}
}
</script>

