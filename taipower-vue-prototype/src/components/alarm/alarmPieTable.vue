<template>
    <div class="col-12 col-lg-12 mx-0 px-0 d-lg-flex justify-content-center">
        <div class="card shadow col-lg-11">
            <div class="responsive_table shadow-none">
                <div style="overflow-y: scroll;">
                    <div class="w-100 row responsive_table_header fw-bold m-0 d-none d-lg-flex flex-nowrap">
                        <div class="col-4 text-center">
                            <label class="fs-6">{{$t('alarm.廠區')}}</label>
                        </div>
                        <div class="col-2 text-center">
                            <label class="fs-6">{{$t('alarm.設備名稱')}}</label>
                        </div>
                        <div class="col-2 text-center">
                            <label class="fs-6">{{$t('alarm.警報名稱')}}</label>
                        </div>
                        <div class="col-2 text-center">
                            <label class="fs-6">{{$t('alarm.發生次數')}}</label>
                        </div>
                        <div class="col-2 text-center">
                            <label class="fs-6">{{$t('alarm.持續時間')}}</label>
                        </div>
                    </div>
                    <div class="w-100 pt-2 pb-2 text-center" v-if="tableData.length == 0">
                        {{$t('無資料')}}
                    </div>
                    <div class="w-100 col-lg-12 responsive_table_body" style="max-height: 400px">
                        <div class="row m-0 responsive_table_content mt-2 mt-lg-0" v-for="data in tableData" :key="data.alarm_place" 
                        >
                            <div class="col-12 d-lg-none mt-2"></div>
                            <div class="col-12 col-lg-4 pt-lg-4 pb-lg-4">
                                <div class="d-flex d-lg-none flex-wrap">
                                    <label class="fs-6 fw-bold">{{$t('alarm.廠區')}}:</label>
                                    <label class="fs-6">{{data.alarm_place}}</label>
                                </div>
                                <label class="fs-6 w-100 text-center d-none d-lg-block">{{data.alarm_place}}</label>
                            </div>
                            <div class="col-12 col-lg-2 pt-lg-4 pb-lg-4">
                                <div class="d-lg-none">
                                    <label class="fs-6 fw-bold d-lg-none">{{$t('alarm.設備名稱')}}:</label>
                                    <label class="fs-6 d-lg-none">{{data.equip_name}}</label>
                                </div>
                                <label class="fs-6 w-100 text-center d-none d-lg-block">{{data.equip_name}}</label>
                            </div>
                            <div class="col-12 d-lg-none mt-2 mb-2" style="border-bottom: 0.25px solid black;"></div>
                            <div class="col-12 col-lg-2 pt-lg-4 pb-lg-4">
                                <div class="d-lg-none">
                                    <label class="fs-6 fw-bold d-lg-none">{{$t('alarm.警報名稱')}}:</label>
                                    <label class="fs-6 d-lg-none">{{data.alarm_event}}</label>
                                </div>
                                <label class="fs-6 w-100 text-center d-none d-lg-block">{{data.alarm_event}}</label>
                            </div>
                            <div class="col-12 col-lg-2 pt-lg-4 pb-lg-4">
                                <div class="d-lg-none">
                                    <label class="fs-6 fw-bold d-lg-none">{{$t('alarm.發生次數')}}:</label>
                                    <label class="fs-6 d-lg-none">{{data.occur_time}}</label>
                                </div>
                                <label class="fs-6 w-100 text-center d-none d-lg-block">{{data.occur_time}}</label>
                            </div>
                            <div class="col-12 d-lg-none mt-2 mb-2" style="border-bottom: 0.25px solid black;"></div>
                            <div class="col-12 col-lg-2 pt-lg-4 pb-lg-4">
                                <div class="d-lg-none">
                                    <label class="fs-6 fw-bold d-lg-none">{{$t('alarm.持續時間')}}:</label>
                                    <label class="fs-6 d-lg-none">{{data.duration}}</label>
                                </div>
                                <label class="fs-6 w-100 text-center d-none d-lg-block">{{data.duration}}</label>
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
    name: "alarmPieTable",
    data() {
        return {
        }
    },
    props: {
        tableData: {type: Array, required: true, default: function(){return []}}
    },
    methods: {
        
    },
}
</script>