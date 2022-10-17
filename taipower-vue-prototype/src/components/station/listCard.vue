<template>
    <div class="row">
        <transition-group name="fade">
            <div class="col-12 col-xxl-4 mt-2" :class="{'col-lg-7 me-2': $store.state.user_data.pageType != 'taipower', 'col-lg-3':  $store.state.user_data.pageType == 'taipower',
            'col-xl-5': $store.state.user_data.pageType != 'taipower', 'col-xl-4':  $store.state.user_data.pageType == 'taipower'}"
            v-for="(station, idx) in stationData" :key="idx">

                <div class="card">

                    <div class="card-header d-flex align-items-center" @dblclick="header_dblclick(station.ID,station.collection)"
                        :class="{
                            'card-header-plant': station.collection == 'pv_plant',
                            'card-header-lgroup': station.collection == 'pv_lgroup', 
                            'card-header-group': station.collection == 'pv_group'
                        }"
                    >
                        <h5 class="m-0">{{
                            station.collection == 'pv_plant'?
                            station.name:
                            station.collection == 'pv_lgroup'?
                            `${station.PV}/${station.name}`:
                            `${station.PV}/${station.lgroup}/${station.name}`
                        }}</h5>
                        <h6 class="m-0 ms-auto">{{$t("案場容量")}}:{{station.capacity}}</h6>
                    </div>

                    <div class="card-body p-1">
                        <div class="container ps-0 pe-0" :class="{'mt-2': $store.state.user_data.pageType != 'taipower'}">
                            <div class="row justify-content-center">
                                <div class="col-12 col-md-4 col-lg-3 col-xl-3 ps-0 fw-bold align-items-end text-center">
                                    <i class="fas fa-bolt"></i><i class="far fa-clock fs-7"></i>
                                    <span>{{$t("功率")}}</span>
                                </div>
                                <div class="col-12 col-sm-12 col-md-auto fs-6 ps-0 align-items-end text-center">
                                    <label class="fw-bold">{{station.p}}</label>
                                    <span class="fs-7 ms-1">kW</span>
                                </div>
                                <div class="col-12 col-md-5 col-lg-5 col-xl-4 ps-0 fs-6 fw-bold align-items-end text-center">
                                    <i class="fas fa-charging-station"></i><span style="font-size: 0.25rem;">Day</span>
                                    <span>{{$t("今日發電量")}}</span>
                                </div>
                                <div class="col-12 col-sm-12 col-md-auto fs-6 ps-0 me-0 align-items-end text-center">
                                    <label class="fw-bold">{{station.kwh}}</label>
                                    <span class="fs-7 ms-1">kWh</span>
                                </div>
                            </div>
                        </div>
                        <div class="container ps-0 pe-0" :class="{'mt-2': $store.state.user_data.pageType != 'taipower'}">
                            <div class="row">
                                <div class="col-5 col-lg-5 ms-3" style="display: flex; flex-direction: column; justify-content: space-evenly">
                                    <div class="d-flex fs-6">
                                        <i class="fas fa-check-circle"
                                        :class="{'text-success': station.status.work,
                                        'text-danger': !station.status.work}"></i>
                                        <span style="margin-left: 5px;">{{$t(`stationData.運轉狀態`)}}</span>
                                    </div>
                                    <div class="d-flex fs-6">
                                        <i class="fas fa-check-circle"
                                        :class="{'text-success': station.status.communi,
                                        'text-danger': !station.status.communi}"></i>
                                        <span style="margin-left: 5px;">{{$t(`stationData.通訊狀態`)}}</span>
                                    </div>
                                    <div class="d-flex fs-6">
                                        <i class="fas fa-check-circle"
                                        :class="{'text-success': station.status.alertCount == 0,
                                        'text-danger': station.status.alertCount != 0}"></i>
                                        <span style="margin-left: 5px;">{{$t(`stationData.警報`)}}</span>
                                        <label class="ms-2 fw-bold">{{station.status.alertCount}}</label>
                                    </div>
                                    <div class="d-flex align-items-end fs-6">
                                        <i class="fas fa-location-arrow"></i>
                                        <i class="fas fa-sun fs-7" style="margin-left: -5px;"></i>
                                        <span>{{$t("等效日照小時")}}</span>
                                        <label class="ms-2 fw-bold">{{station.irrh}}</label>
                                        <span class="fs-7 ms-1">h</span>
                                    </div>
                                    <div class="d-flex align-items-end fs-6">
                                        <i class="fas fa-location-arrow"></i>
                                        <i class="fas fa-sun fs-7" style="margin-left: -5px;"></i>
                                        <span>{{$t("等效發電小時")}}</span>
                                        <label class="ms-2 fw-bold">{{station.dmy}}</label>
                                        <span class="fs-7 ms-1">h</span>
                                    </div>
                                </div>
                                <div class="col-6" :class="{'col-lg-6': $store.state.user_data.pageType != 'taipower', 'col-lg-5': $store.state.user_data.pageType == 'taipower'}">
                                    <div class="d-flex justify-content-center">
                                        <div class="sta_circle" :ref="staCircle" :data-per="station.pr"
                                            :class="{
                                                'card-header-plant': station.collection == 'pv_plant',
                                                'card-header-lgroup': station.collection == 'pv_lgroup', 
                                                'card-header-group': station.collection == 'pv_group'
                                            }"
                                        >
                                            <div class="stacir_img">
                                                <figure class="m-0" :style="{ 'background-image': 'url(' + station.imgsrc + ')' }"></figure>
                                                <span class="d-none d-lg-block" :class="{'fs-5': $store.state.user_data.pageType == 'taipower'}"><b :class="{'text-center': $store.state.user_data.pageType == 'taipower'}">PR</b>{{ station.pr }}%</span>
                                                <span class="fs-7 d-lg-none"><b>PR</b>{{ station.pr }}%</span>
                                            </div>
                                            <svg version="1.1" id="Layer_1" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" x="0px" y="0px" viewBox="0 0 20 20" style="enable-background: new 0 0 493.2 493.3;" xml:space="preserve">
                                                <path d="M246.6,10c130.7,0,236.6,105.9,236.6,236.6S377.3,483.3,246.6,483.3S10,377.3,10,246.6S115.9,10,246.6,10" />
                                            </svg>
                                        </div>
                                    </div>
                                </div>
                            </div>
                        </div>

                        <div class="d-flex align-items-end ms-3 mb-2">
                            <i class="fas fa-clock fs-7"></i>
                            <label class="fs-7">{{$t("stationData.overview.最後通訊時間")}}：{{station.lastTime}}</label>
                            <button @click="openStation(station)" class="btn btn-warning ms-auto me-2">{{$t('查看案場')}}</button>
                        </div>
                        
                    </div>
                </div>
            </div>
        </transition-group>
    </div>
</template>

<script>
export default {
    name: "listCard",
    props: {
		stationData: Array,
	},
    data(){
        return {
            circle_refs: [],
        }
    },
    methods:{
        handleScroll(){
			this.circle_refs.forEach( el =>{
				let thisTop = el.offsetTop - window.innerHeight;
				let srcV    = window.scrollY;
				let perc    = 1 - (el.dataset.per / 100);
				let dashOff = el.children[1].children[0];
				if( srcV > thisTop ){
					dashOff.style.strokeDashoffset = this.pathLenth * perc;
				}else{
					dashOff.style.strokeDashoffset = this.pathLenth;
				}
			});
		},
		staCircle(el) {
			if (el) {
				this.circle_refs.push(el)
			}
		},
        openStation(data){
            this.$store.state.stationList_history = {
                ID_list: this.$parent.$data.plant_select.ID_list,
                col_list: this.$parent.$data.plant_select.col_list,
                current_page: this.$parent.$data.current_page
            }
            this.$router.push({path: "stationData", query: {ID: data.ID, collection: data.collection}})
        },
        header_dblclick(ID, type){
			this.$emit("dblclick-jump", {ID: ID, type: type})
		}
    },
    mounted(){
        window.addEventListener('scroll', this.handleScroll)
        if(this.stationData.length > 0){
            this.pathLenth = this.circle_refs[0].children[1].children[0].getTotalLength();
            this.handleScroll()
        }
    },
    beforeUpdate() {
		this.circle_refs = []
	},
	updated(){
		this.pathLenth = this.circle_refs[0].children[1].children[0].getTotalLength();
		this.handleScroll()
	},
    unmounted(){
        window.removeEventListener('scroll', this.handleScroll)
    },
}
</script>