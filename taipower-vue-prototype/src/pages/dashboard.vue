<template>
  <div>
    <button class="btn fs-5 ms-auto p-0 float-end" @click="dashboard_export" v-if="!export_mode"><i class="fa-solid fa-print"></i></button>
    <div :class="{'row': !export_mode}" class="widget_row" v-loading="Object.keys(user_parameters).length == 0">
      <export-cover v-if="export_mode"></export-cover>
      <weather-time :city="city" v-if="user_parameters.weatherTime && !export_mode"></weather-time>
      <taiwan3d-map v-if="user_parameters.taiwan3dMap && !export_mode"></taiwan3d-map>
      <total-information-table v-if="user_parameters.totalInformationTable"></total-information-table>
      <multiple-chart v-if="user_parameters.multipleChart"></multiple-chart>
      <compare-chart v-if="user_parameters.compareChart"></compare-chart>
      <plant-history v-if="user_parameters.plantHistory"></plant-history>
      <treeview v-if="user_parameters.treeMap  && !export_mode"></treeview>
      <equipment-compare v-if="user_parameters.equipmentCompareChart"></equipment-compare>
      <sequence-chart v-if="user_parameters.sequenceChart"></sequence-chart>
      <dispatch-stats v-if="user_parameters.dispatchStats"></dispatch-stats> 
    </div>
    <div class="position-fixed top-0 start-0 p-3" style="z-index: 20; width: 100px;" v-if="export_mode">
      <div ref="print_toast" class="card toast print_toast" role="alert" aria-live="assertive" aria-atomic="true" :data-bs-autohide="false">
        <div class="toast-body">
          <button class="btn fs-5" @click="print_page"><i class="fa-solid fa-print"></i></button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import {Toast} from 'bootstrap';

import exportCover from "@/components/widget/export_cover.vue"
import weatherTime from "@/components/widget/weatherTime.vue"
import plantHistory from "@/components/widget/plantHistory.vue"
import taiwan3dMap from '@/components/widget/taiwan3d_map.vue'
import totalInformationTable from '@/components/widget/totalInformationTable.vue'
import compareChart from '@/components/widget/compareChart.vue'
import treeview from '@/components/widget/treeview.vue'
import equipmentCompare from '@/components/widget/equipmentCompare.vue'
import multipleChart from '@/components/widget/multipleChart.vue'
import sequenceChart from '@/components/widget/sequenceChart.vue'
import dispatchStats from '@/components/widget/dispatchStats.vue'

export default {
    name: 'Dashboard',
    components: {
      exportCover,
      weatherTime,
      plantHistory,
      taiwan3dMap,
      equipmentCompare,
      totalInformationTable,
      compareChart,
      multipleChart,
      treeview,
      sequenceChart,
      dispatchStats
    },
    data() {
      return {
        user_parameters:{},
        city: "新北市",
        export_mode: false,
      }
    },
    methods: {
      widget_components() {
        let that = this
        this.axios.get('/setting/load_user_widget_parameter').then(data=>{
            console.log(data.data.data)
            window.setTimeout(()=>{
              that.user_parameters = data.data.data.widget_data
              that.city = data.data.data.widget_data.city_select
            }, 500)
        })
      },
      dashboard_export() {
        window.open('/dashboard_export', this.$i18n.t('匯出報表'), 'width=794,height=1122')
      },
      print_page(){
        print() 
        window.onafterprint = () =>{
          window.close()
        } 
      }
    },
    beforeMount(){
      if(this.$route.path == '/dashboard_export'){
        this.export_mode = true
        document.querySelector('body').classList.add('export_mode')
        if (!window.matchMedia || window.matchMedia('(prefers-color-scheme: light)').matches) {
          document.querySelector('body').style.background = 'white'
        }
      }
    },
    mounted(){
      this.widget_components()
      this.syncdata = window.setInterval(this.widget_components, 5000)
      if(this.export_mode){
        this.print_toast = new Toast(this.$refs.print_toast)
        this.print_toast.show()
      }
    },
    unmounted(){
      window.clearInterval(this.syncdata)
    },
}
</script>
<style scoped>
  body.export_mode #app{
    background: white !important;
  }
  @page { 
    size: auto;
    margin: 0cm !important; 
  }
  @media print {
    header,footer { 
      display: none; 
    }
    *, *:before, *:after {
      /*CSS transitions*/
      -o-transition-property: none !important;
      -moz-transition-property: none !important;
      -ms-transition-property: none !important;
      -webkit-transition-property: none !important;
      transition-property: none !important;
      
      /*CSS transforms*/
      -o-transform: none !important;
      -moz-transform: none !important;
      -ms-transform: none !important;
      -webkit-transform: none !important;
      transform: none !important;
      
      /*CSS animations*/
      -webkit-animation: none !important;
      -moz-animation: none !important;
      -o-animation: none !important;
      -ms-animation: none !important;
      animation: none !important;
    }
    .print_toast{
      visibility: hidden;
    }
    #app > div{
      padding-top: 0 !important;
      padding-bottom: 0 !important;
    }
    .widget_row *{
      padding: 0 !important;
      visibility: visible;
      margin-right: 0px !important;
      margin-left: 0px !important;
    }
    .widget_row > div{
      display: block;
      width: 21cm;
      min-height: 28.2cm !important;
      margin-top: 0px !important;
      margin-right: 0px !important;
      break-inside: avoid;
      break-before: always;
      break-after: always;
      page-break-after: always;
      -webkit-break-after: always;
    }
    .widget_row .card{
      border: 0px;
      box-shadow: unset;
    }
  }
</style>
