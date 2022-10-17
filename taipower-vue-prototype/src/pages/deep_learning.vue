<template>
    <div>
        <div class="navbar navbar-expand-lg navbar-light mb-2">
            <div class="w-100">
                <button class="w-100 d-lg-none btn btn-primary" type="button" data-bs-toggle="collapse" data-bs-target="#navbarNav" aria-controls="navbarNav" aria-expanded="false" aria-label="Toggle navigation" v-if="tab_datas.length>0">
                    {{button_value()}}
                </button>
                <!-- <div class="collapse navbar-collapse" id="navbarNav">
                    <ul class="navbar-nav col-12 col-lg-9">
                        <li class="nav-item col-12 col-lg-4 text-center">
                            <a class="nav-link text-dark" :class="{'active': pageMode == 'digital_twin'}" @click="changePageMode('digital_twin')">{{$t('AIAnalysis.tabs.digital_twin')}}</a>
                        </li>
                        <li class="nav-item col-12 col-lg-4 text-center">
                            <a class="nav-link text-dark" :class="{'active': pageMode == 'power_forecasting'}" @click="changePageMode('power_forecasting')">{{$t('AIAnalysis.tabs.power_forecasting')}}</a>
                        </li>
                        <li class="nav-item col-12 col-lg-4 text-center">
                            <a class="nav-link text-dark" :class="{'active': pageMode == 'module_cleaning'}" @click="changePageMode('module_cleaning')">{{$t('AIAnalysis.tabs.module_cleaning')}}</a>
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
                <digital-twin v-if="pageMode == 'digital_twin'"></digital-twin>
                <power-forecasting v-if="pageMode == 'power_forecasting'"></power-forecasting>
                <module-cleaning v-if="pageMode == 'module_cleaning'"></module-cleaning>
            </div>
        </transition>
    </div>    
</template>




<script>
import digitalTwin from '@/components/deep_learning/digital_twin.vue'
import powerForecasting from '@/components/deep_learning/power_forecasting.vue'
import moduleCleaning from '@/components/deep_learning/module_cleaning.vue'

export default {
    name: "deepLearning",
    components: {
        digitalTwin,
        powerForecasting,
        moduleCleaning
    },
    data() {
        return {
            pageMode: '',
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