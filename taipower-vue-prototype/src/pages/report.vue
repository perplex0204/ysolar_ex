<template>
    <div>
        <!-- <div class="complete">
            <el-autocomplete
                v-model="search"
                :fetch-suggestions="querySearchAsync"
                :placeholder="$t('搜尋')"
                value-key="name"
                @select="handleSelect"
            ></el-autocomplete>
        </div> -->
        
        <div class="navbar navbar-expand-lg navbar-light mb-2">
            <div class="w-100">
                <button class="w-100 d-lg-none btn btn-primary" type="button" data-bs-toggle="collapse" data-bs-target="#navbarNav" aria-controls="navbarNav" aria-expanded="false" aria-label="Toggle navigation" v-if="tab_datas.length>0">
                    <!-- {{ {realtime: "$t('report.imformation.realtime')", schedule: '排程' }[pageMode] }} -->
                    {{button_value()}}
                </button>
                <!-- <div class="collapse navbar-collapse" id="navbarNav">
                    <ul class="navbar-nav col-12 col-lg-9">
                        <li class="nav-item col-12 col-lg-4 text-center">
                            <a class="nav-link text-dark" :class="{'active': pageMode == 'realtime'}" @click="changePageMode('realtime')">{{$t('report.imformation.realtime')}}</a>
                        </li>
                        <li class="nav-item col-12 col-lg-4 text-center">
                            <a class="nav-link text-dark" :class="{'active': pageMode == 'schedule'}" @click="changePageMode('schedule')">{{$t('report.imformation.schedule')}}</a>
                        </li>
                        <li class="nav-item col-12 col-lg-4 text-center">
                            <a class="nav-link text-dark" :class="{'active': pageMode == 'tenday'}" @click="changePageMode('tenday')">{{$t('report.imformation.tenday')}}</a>
                        </li>
                    </ul>
                </div> -->
                <div class="collapse navbar-collapse" id="navbarNav" v-if="tab_datas.length>0">
                    <ul class="navbar-nav col-12" :class="'col-lg-'+tab_datas.length*3">
                        <li class="nav-item col-12 text-center" :class="'col-lg-'+li_length"
                        v-for="tab_data in tab_datas" :key="tab_data.value"
                        >
                            <a class="nav-link text-dark" :class="{'active': pageMode == tab_data.value}" @click="changePageMode(tab_data.value)">
                                {{
                                    tab_data.name_i18n[$store.state.language] == undefined ?
                                    tab_data.name_i18n['zh-TW'] : tab_data.name_i18n[$store.state.language]
                                }}</a>
                        </li>
                    </ul>
                </div>
            </div>
        </div>

        <transition mode="out-in" name="table_animation_to">
            <div :key="pageMode">
                <report-real-time v-if="pageMode=='realtime'"></report-real-time>
                <report-schedule v-if="pageMode == 'schedule'"></report-schedule>
                <ten-day-report v-if="pageMode == 'tenday'"></ten-day-report>
            </div>
        </transition>
    </div>
</template>



<script>
// import TimeRangePickerSimple from "@/components/datepicker/timeRangePickerSimple.vue"
import reportRealTime from "@/components/report/reportRealTime"
import reportSchedule from "@/components/report/reportSchedule"
import tenDayReport from "@/components/report/tenDayReport"

export default{
    name: "report",
    components:{
        reportRealTime,
        reportSchedule,
        tenDayReport
    },
    data(){
        return {
            pageMode: "",
            tab_datas: [],
            li_length: 0,
        }
    },
    methods:{
        changePageMode(mode){
            this.pageMode = mode
        },
        button_value(){
            let tab_data = this.tab_datas.find((value) => {
                return (value.value == this.pageMode)
            })
            return tab_data.name_i18n[this.$store.state.language] == undefined ?
            tab_data.name_i18n['zh-TW'] : tab_data.name_i18n[this.$store.state.language]
        }
    },
    watch: {
    },
    beforeMount(){
        console.log(this.$route)
        let that = this
        this.axios.post('get_tab_data', {"path": this.$route.path})
        .then(data => {
            console.log(data.data.data.data)
            that.tab_datas = data.data.data.data
            if(that.tab_datas.length>0){
                that.li_length = 12/that.tab_datas.length
                that.pageMode = that.tab_datas[0].value
            }
        })
    },
}
</script>
<style scoped>
.complete{
    margin-bottom: 1rem;
    width: 200px;
}
.selection{
    margin-bottom: 1rem;
    width: 200px;
}
</style>