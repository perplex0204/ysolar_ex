<template>
    <div>
        <div class="d-flex flex-wrap mb-2">
			<div class="col-7 col-lg-6 col-xl-4 col-xxl-3 me-2">
				<autocomplete @station-select="station_select" @empty-select="plant_empty_select"> </autocomplete>
			</div>
			<div class="col-4 ms-auto ms-lg-2 col-lg-1 d-flex flex-nowrap me-lg-4 station_change">
				<!-- <el-button-group> -->
					<el-button 
					:class="{active: showcard}" 
					@click="switchDisplay"
					size="large"
					style="border-top-right-radius:0 !important; border-bottom-right-radius:0 !important;"
					class="col-6 col-lg-6 station_btn"><i class="fas fa-th-large" /></el-button>

					<el-button 
					:class="{active: !showcard}" 
					@click="switchDisplay"
					size="large"
					style="margin-left:0 !important; border-top-left-radius:0 !important; border-bottom-left-radius:0 !important;"
					class="col-6 col-lg-6 station_btn"><i class="fas fa-bars"/></el-button>
				<!-- </el-button-group> -->
			</div>

			<el-popover
			ref="favoritePop"
			placement="bottom"
			width="250px"
			trigger="click">
				<template #reference>
					<el-button size="large" class="col-12 col-lg-2 mt-3 mt-lg-0">
						<i class="el-icon-star-off"></i><label class="d-none d-lg-block">{{
							myfavoriteSelect != null ? myfavoriteSelect : $t('stationList.我的最愛')}}</label>
					</el-button>
				</template>
				<div class="d-flex flex-column align-items-center justify-content-center">
					<div class="favorite-row pt-2 pb-2 w-100" v-for="group in favoriteData" :key="group.name"
					@click="selectFavorite(group)">
						<label :class="{'text-primary': myfavoriteSelect == group.name}">{{group.name}}</label>
						<button class="btn p-0 float-end" @click.stop="open_favoriteModal(group); $refs.favoritePop.hide();"><i class="el-icon-s-tools text-dark"></i></button>
					</div>
					<el-button class="mt-2" size="default" @click="reset_favoriteModal(); favoriteModal.show()">
						<i class="el-icon-plus"></i>
					</el-button>
				</div>
			</el-popover>
        </div>
        <div class="row mb-4" v-if="$store.state.user_data.pageType != 'taipower'">
            <div class="col-12 col-md-5 col-lg-2-4 ps-4 pe-4" v-for="i in ttlData" :key="i.title">
                <div class="d-flex align-items-center" style="min-height: 38px;">
                    <h6 class="m-0">{{$t(i.title)}}</h6> <i class="ms-auto text-success" :class="'icon-'+i.icon"></i>
                </div>
                <div class="w-100 d-flex align-items-end  align-self-end">
                    <label class="fs-3 fw-bold stats_numb">{{i.numb}}</label>
                    <label class="ms-auto">{{$t(`unit.${i.unit}`)}}</label>
                </div>
            </div>
        </div>
        
		<list-card 
			v-if="stationList.length > 0 && showcard" 
			:station-data="stationList"
			@dblclick-jump="dblclick_jump"	
		></list-card>

		<list-table
			v-if="stationList.length>0 && !showcard"
			:station-data="stationList"
			@dblclick-jump="dblclick_jump"
		></list-table>

		<div class="ms-2 mt-2">
			<el-pagination
			class="d-flex justify-content-center w-100"
			background
			layout="prev, pager, next"
			:total="plant_select['ID_list'].length"
			v-model:currentPage="current_page"
			:page-size="number_per_page"
			@current-change="get_card_overview()">
			</el-pagination>
		</div>

		<!-- 我的最愛編輯modal -->
		<div class="modal fade" ref="favoriteModal" tabindex="-1" aria-labelledby="exampleModalLabel" aria-hidden="true"
		:data-bs-backdrop="false">
			<div class="modal-dialog modal-dialog-centered">
				<div class="modal-content">
					<div class="modal-header">
						<div class="w-100">
							<el-input
								type="text"
								:placeholder="$t('stationList.我的最愛名稱')"
								maxlength="20"
								show-word-limit
								autofocus
								class="favoriteName fs-5"
								v-model="favoriteModal_data.name"
							></el-input>
							<p class="fs-7 text-danger ms-2 mb-0"
							v-if="[null, undefined, ''].includes(favoriteModal_data.name)">{{$t('stationList.請輸入我的最愛名稱')}}</p>
						</div>
						<button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"
						@click="reset_favoriteModal"></button>
					</div>
					<div class="modal-body">
						<div class="col-12 col-lg-8">
							<autocomplete
								@station-select=" data => favoriteModal_data.station_list.push(data) "
							></autocomplete>
						</div>
						<table class="table mt-2 table-striped">
							<thead>
								<tr>
									<th scope="col"><i class="fa-solid fa-table text-primary me-2"></i>{{$t('stationList.已選取清單')}}</th>
								</tr>
							</thead>
							<tbody>
								<tr v-for="data, i in favoriteModal_data.station_list" :key="data.ID">
									<div class="w-100 d-flex p-2 align-items-center">
										{{data.name}}
										<button class="btn p-0 ms-auto text-secondary"
											@click="favoriteModal_data.station_list.splice(i, 1)"
										><i class="fa-solid fa-circle-xmark"></i></button>
									</div>
								</tr>
							</tbody>
						</table>
					</div>
					<div class="modal-footer">
						<button type="button" class="btn btn-danger"
						@click="delete_favorite">{{$t('刪除')}}</button>
						<button type="button" class="btn btn-success ms-auto"
						@click="save_favorite">{{$t('儲存')}}</button>
					</div>
				</div>
			</div>
		</div>
    </div>
</template>

<script>
import { Modal } from 'bootstrap'
import { ElMessage } from 'element-plus'
import autocomplete from '@/components/autocomplete/stationList.vue'
import listCard from "@/components/station/listCard.vue"
import listTable from "@/components/station/listTable.vue"

export default {
    name: 'Plantinfo',
	components: { listCard, autocomplete, listTable},
    data(){
        return {
            plant_img: require('@/assets/logo.png'),
            plant_search: "",
            ttlData: [
				{ title: '全國總電站數', numb: '---', icon: 'ttl_sunboard', unit: '座'},
				{ title: '全國總建置容量', numb: '---', icon: 'ttl_drive', unit: 'MW'},
				{ title: '全國累計發電量', numb: '---', icon: 'ttl_thunder', unit: 'MWh'},
				{ title: '全國總累計減碳量', numb: '---', icon: 'ttl_leaf', unit: 'kg'},
				{ title: '累計躉售', numb: '---', icon: 'ttl_money', unit: '元'}
			],
			plant_select: {'ID_list': [], 'col_list': []},
			stationList:[
			],
            PV_data: [

			],
			current_page: 1,
			myfavoriteSelect: null,
			favoriteData: [],
			favoriteModal_data: {
				name: null,
				station_list: []
			},
			number_per_page: this.$store.state.user_data.pageType == 'taipower' ? 6 : 10,
			showcard: localStorage.getItem('solar_vue_stationList_display') == 'table' ? false : true
        }
    },
    methods: {
		station_select(item){
			if(item.collection == 'pv_plant' || item.collection == 'pv_lgroup'){
				this.dblclick_jump({
					ID: item.ID, type: item.collection
				})
			}
			else if(item.collection == 'pv_group'){
				this.plant_select.ID_list = [item.ID]
				this.plant_select.col_list = [item.collection]
			}
		},
		plant_empty_select(){
			this.stats_all_pv(true)
		},
		ID_list_is_equal(a, b){
			return a.length === b.length &&
			a.every((v, i) => v === b[i])
		},
        async get_card_overview(){
			let that = this
			//假如 request過慢 要求的案場資料 不等於使用者現在選的
			//拋棄request結果
			let old_ID_list = this.plant_select['ID_list'].slice((this.current_page-1)*this.number_per_page, this.current_page*this.number_per_page)
			await this.axios.post('/get_card_overview_real',{  // Send ID only in pagination range
				ID_list: this.plant_select['ID_list'].slice((this.current_page-1)*this.number_per_page, this.current_page*this.number_per_page), 
				col_list: this.plant_select['col_list'].slice((this.current_page-1)*this.number_per_page, this.current_page*this.number_per_page)
			}).then(function(data){
				if(!that.ID_list_is_equal(old_ID_list, that.plant_select['ID_list'].slice((that.current_page-1)*that.number_per_page, that.current_page*that.number_per_page))){
					//假如 request過慢 要求的案場資料 不等於使用者現在選的
					//拋棄request結果
					console.log('Expire loading data!')
					return false
				}
				let station_data = data.data.data
				that.stationList = []
				for(var i in station_data){
					let d = station_data[i]
					that.stationList.push({
						status:{ work: d['work'], communi: d['communi'], no_alert: d['no_alert'], alertCount: d['alert_count'] },
						name: d['name'], pr: d['pr'], pr_num: d['pr'] == "---" ? 0 : d['pr'], capacity: d['capacity']+' kW', capacity_num: d['capacity'],
						kwh: d['today_kwh'], kwh_num: d['today_kwh'] == "---" ? 0 : d['today_kwh'], p: d['p'], p_num: d['p'] == "---" ? 0 : d['p'], dmy_num: d['dmy'] == "---" ? 0 : d['dmy'], irrh_num: d['irrh'] == "---" ? 0 : d['irrh'],
						dmy: d['dmy'], irrh: d['irrh'], profit: d['profit'], lastTime: d['lastTime_i18n'][that.$store.state.language], url: '/',
						imgsrc: d['imgsrc'], type: d['type'], ID: d['ID'], collection: d['collection'],
						PV: d['PV'], lgroup: d['lgroup'], name_total: d["collection"] == 'pv_plant' ? d["name"] :  d["collection"] == 'pv_lgroup' ? (d["PV"]+"/"+d["name"]) : (d["PV"]+"/"+d["lgroup"]+"/"+d["name"])
					})
				}
			})
		},
        stats_all_pv(page_init=false){
			let that = this
			this.axios.get('/stats_all_pv_real').then(function(data){
				const stats_data = data.data.data
				that.ttlData[0].numb = stats_data['total_station']
				that.ttlData[1].numb = stats_data['total_capacity']
				that.ttlData[2].numb = stats_data['total_kwh']
				that.ttlData[3].numb = stats_data['total_carbon_reduction']
				that.ttlData[4].numb = stats_data['profit']
				if(page_init){
					if(Object.keys(that.$store.state.stationList_history).length > 0){
						// go back from stationData
						// load previous plant_select and page
						that.plant_select['ID_list'] = that.$store.state.stationList_history.ID_list,
						that.plant_select['col_list'] = that.$store.state.stationList_history.col_list,
						that.current_page = that.$store.state.stationList_history.current_page
					}else{
						that.plant_select['ID_list'] = stats_data['ID_list']
						that.plant_select['col_list'] = new Array(stats_data['ID_list'].length).fill('pv_plant')
					}
					that.PV_data = stats_data['PV_data']
					that.get_card_overview()
					page_init = false
				}
			})
		},
        //Station Search
        dblclick_jump(data){
			//alert(`${data.ID} ${data.type}`)
			let that = this
			if(data.type == 'pv_group')
				return false
			this.axios.post('/station_search_ID', {
				name: null,
				ID: data.ID,
				type: data.type
			}).then((data)=>{
				that.plant_select = {ID_list: data.data.data.ID_list, col_list: data.data.data.col_list}
			})
		},
		get_favorite(select=null){
			//取得我的最愛群組
			this.axios.get("/get_station_favorite").then(data => {
				this.favoriteData = data.data.data.favorite_list
				if(select !== null){
					for(var i in this.favoriteData){
						if(select == this.favoriteData[i].name)
							this.selectFavorite(this.favoriteData[i], true)
					}
				}else{
					// 預設顯示案場
					if(data.data.data.default_favorite != null){
						this.plant_select.ID_list = []
						this.plant_select.col_list = []
						data.data.data.default_favorite.data.forEach(d=>{
							this.plant_select.ID_list.push(d.ID)
							this.plant_select.col_list.push(d.collection)
						})
						this.stats_all_pv()
						this.get_card_overview()
					}else{
						this.stats_all_pv(true)
					}
				}
			})	
		},
		save_favorite(){
			if(this.favoriteModal_data.name == "" || this.favoriteModal_data.name == null){
				return false
			}
			this.axios.post("/save_station_favorite", {
				name: this.favoriteModal_data.name,
				data: this.favoriteModal_data.station_list
			}).then(data => {
				//console.log(data.data.data)
				this.get_favorite(this.favoriteModal_data.name)
				this.favoriteModal.hide()
				ElMessage.success(this.$i18n.t('成功'))
			})
		},
		delete_favorite(){
			if(this.favoriteModal_data.name == "" || this.favoriteModal_data.name == null){
				return false
			}
			this.axios.post("/delete_station_favorite", {
				name: this.favoriteModal_data.name
			}).then(data => {
				this.favoriteModal.hide()
				this.reset_favoriteModal()
				this.myfavoriteSelect = null
				this.get_favorite()
				ElMessage.success(this.$i18n.t('成功'))
			})
		},
		reset_favoriteModal(){
			this.get_favorite()
			this.favoriteModal_data = {
				name: null,
				station_list: []
			}
		},
		open_favoriteModal(data){
			this.favoriteModal_data = {
				name: data.name,
				station_list: data.data
			}
			this.favoriteModal.show()
		},
		selectFavorite(data, no_cancel=false){
			if(this.myfavoriteSelect == data.name && !no_cancel){
				this.myfavoriteSelect = null
				this.stats_all_pv(true)
			}else{
				this.myfavoriteSelect = data.name
				this.plant_select.ID_list = []
				this.plant_select.col_list = []
				for(var i in data.data){
					this.plant_select.ID_list.push(data.data[i].ID)
					this.plant_select.col_list.push(data.data[i].collection)
				}
				console.log(this.plant_select)
				this.get_card_overview()
			}
		},
		switchDisplay(){
			this.showcard = !this.showcard
			localStorage.setItem('solar_vue_stationList_display', this.showcard ? 'card':'table')
		}
    },
	mounted(){
		let that = this
		//this.get_favorite()
        this.get_favorite()
		this.favoriteModal = new Modal(this.$refs.favoriteModal)
        this.syncdata = setInterval(function(){
			that.stats_all_pv()
			that.get_card_overview()
		}, 5000)
		//this.plant_search_mount()		
	},
	watch:{
		plant_select: async function(data){
			this.current_page = 1
			await this.get_card_overview()
		},
	},
	unmounted(){
		clearInterval(this.syncdata)
	},
}
</script>
<style scoped>
.carousel-content{
    min-height: 200px;
    background-color: white;
    border-radius: .5rem;
}
.favoriteName:deep(.el-input__inner){
	border: 0px;
	padding-bottom: 0px;
	background-color: transparent;
	color: var(--bs-body-color);
}
.favoriteName:deep(.el-input__suffix .el-input__count-inner){
	background-color: transparent;
}
.favorite-row:hover{
	font-weight: bold;
}
.stats_numb{
	color: var(--bs-primary);
}
@media (prefers-color-scheme: dark) {
	.stats_numb{
		color: rgb(86, 148, 205);
	}
}
</style>