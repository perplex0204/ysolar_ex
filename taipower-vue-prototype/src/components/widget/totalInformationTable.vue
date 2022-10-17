<template>
    <div class="col-12 col-lg-8 mt-3 px-0">
        <div class="card shadow">
            <div class="card-header text-center fw-bold fs-4">
                <i class="icon-nav_factory fs-3"></i>
                {{$t('homePage.table.information')}}
            </div>
            <div class="card-body responsive_table shadow-none">
                <div style="overflow-y: scroll;">
                    <div class="w-100 row responsive_table_header  fw-bold m-0 d-none d-lg-flex flex-nowrap">
                        <div class="col-3 text-center">
                            <label class="fs-6">{{$t('homePage.table.station')}}</label>
                        </div>
                        <div class="col-2 text-center">
                            <label class="fs-6">{{$t('homePage.table.todayPower')}}</label>
                        </div>
                        <div class="col-3 text-center">
                            <label class="fs-6">{{$t('homePage.table.weather')}}</label>
                        </div>
                        <div class="col-2 text-center">
                            <label class="fs-6">{{$t('homePage.table.temperature')}}</label>
                        </div>
                        <div class="col-2 text-center">
                            <label class="fs-6">{{$t('homePage.table.carbon_reduction')}}</label>
                        </div>
                    </div>
                    <div class="w-100 pt-2 pb-2 text-center" v-if="information_datas.length == 0">
                        {{$t('無資料')}}
                    </div>
                    <div class="w-100 col-lg-12 responsive_table_body">
                        <div class="row m-0 responsive_table_content mt-2 mt-lg-0" v-for="information_data in information_datas" :key="information_data.name" 
                        >
                            <div class="col-12 d-lg-none mt-2"></div>
                            <div class="col-12 col-lg-3 pt-lg-4 pb-lg-4">
                                <div class="d-flex d-lg-none flex-wrap">
                                    <label class="fs-6 fw-bold">{{$t('homePage.table.station')}}:</label>
                                    <label class="fs-6">{{information_data.name}}</label>
                                </div>
                                <label class="fs-6 w-100 text-center d-none d-lg-block">{{information_data.name}}</label>
                            </div>
                            <div class="col-12 col-lg-2 pt-lg-4 pb-lg-4">
                                <div class="d-lg-none">
                                    <label class="fs-6 fw-bold d-lg-none">{{$t('homePage.table.todayPower')}}:</label>
                                    <label class="fs-6 d-lg-none">{{information_data.todayPower}}</label>
                                </div>
                                <label class="fs-6 w-100 text-center d-none d-lg-block">{{information_data.todayPower}}</label>
                            </div>
                            <div class="col-12 d-lg-none mt-2 mb-2" style="border-bottom: 0.25px solid black;"></div>
                            <div class="col-12 col-lg-3 pt-lg-4 pb-lg-4">
                                <div class="d-lg-none">
                                    <label class="fs-6 fw-bold d-lg-none">{{$t('homePage.table.weather')}}:</label>
                                    <label class="fs-6 d-lg-none">{{information_data.status}}</label>
                                </div>
                                <label class="fs-6 w-100 text-center d-none d-lg-block">{{information_data.status}}</label>
                            </div>
                            <div class="col-12 col-lg-2 pt-lg-4 pb-lg-4">
                                <div class="d-lg-none">
                                    <label class="fs-6 fw-bold d-lg-none">{{$t('homePage.table.temperature')}}:</label>
                                    <label class="fs-6 d-lg-none">{{information_data.temperature}}</label>
                                </div>
                                <label class="fs-6 w-100 text-center d-none d-lg-block">{{information_data.temperature}}</label>
                            </div>
                            <div class="col-12 d-lg-none mt-2 mb-2" style="border-bottom: 0.25px solid black;"></div>
                            <div class="col-12 col-lg-2 pt-lg-4 pb-lg-4">
                                <div class="d-lg-none">
                                    <label class="fs-6 fw-bold d-lg-none">{{$t('homePage.table.carbon_reduction')}}:</label>
                                    <label class="fs-6 d-lg-none">{{information_data.carbon_reduction}}</label>
                                </div>
                                <label class="fs-6 w-100 text-center d-none d-lg-block">{{information_data.carbon_reduction}}</label>
                            </div>
                        </div> 
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>




<script>

export default {
    name: "totalInformationTable",
    data() {
        return {
            information_datas: []
        }
    },
    methods: {
        get_table_data(){
            let that = this
			this.axios.get('/tawian3d_plant_overview').then(function(data){
				//console.log(data.data.data)
                let datas = data.data.data
                var carbon_reduction
                var data_reg = []
                for (var i=0; i<datas.length; i++) {
                    carbon_reduction = datas[i].otherInfos.find(element => (element.title == '今日減碳量' && element.unit == 'kg'))
                    data_reg.push({
                        name: datas[i].name,
                        todayPower: datas[i].todayPower.numb,
                        status: datas[i].weather.status,
                        temperature: datas[i].weather.temperature,
                        carbon_reduction: carbon_reduction.numb
                    })
                }
                that.information_datas = data_reg
                // console.log(that.information_datas)
			})
            // console.log(that.data)
        }
    },
    mounted(){
        this.get_table_data()
        this.syncdata = window.setInterval(this.get_table_data, 5000)
    },
    unmounted(){
        window.clearInterval(this.syncdata)
    },
}
</script>