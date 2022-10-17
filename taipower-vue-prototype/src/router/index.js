import { createWebHistory, createRouter } from "vue-router";
import { h } from "vue"; 

//Page Components
import login from '@/pages/login.vue'
import Layout from '@/layout/body.vue'
import dashboard from '@/pages/dashboard.vue'
import stationList from '@/pages/stationList.vue'
import Alarm from '@/pages/Alarm.vue'
import stationData from '@/pages/stationData.vue'
import dispatch from "@/pages/dispatch.vue"
import dispatch_work from "@/pages/dispatch_work.vue"
import report from "@/pages/report.vue"
import reportOverview from "@/pages/reportOverview.vue"
import Analysis from "@/pages/Analysis.vue"
import setting from "@/pages/setting.vue"
import deepLearning from "@/pages/deep_learning.vue"
import documents from "@/pages/documents.vue"
import stationGraphic from "@/pages/stationGraphic.vue"
import openid_connect from "@/pages/openid_connect.vue"
import ysolar_test from "@/pages/ysolar_test.vue"
import ysolar_test02 from "@/pages/ysolar_test02.vue"
import ysolar_test03 from "@/pages/ysolar_test03.vue"
import ysolar_test04 from "@/pages/ysolar_test04.vue"

//css
import '@/assets/css/main.css' //es樣式
import '@/assets/css/ele_index.css' //修改es框架樣式
import '@/assets/css/ani.css' //animation css

//scss
import '@/assets/scss/main.scss'


// Axios
import axios from 'axios';

const VUE_VERSION = require("../../package.json").version;

const router = createRouter({
  routes: [
    {
      path: '/',
      name: 'Layout',
      component: Layout,
      children:[
        {
          path: 'dashboard',
          name: '個性化首頁',
          component: dashboard
        },
        {
          path: 'stationList',
          name: '電站管理',
          component: stationList
        },
        {
          path: 'alarm',
          name: '告警資訊',
          component: Alarm
        },
        {
          path: 'stationData',
          name: '案場資訊',
          component: stationData
        },
        {
          path: 'deepLearning',
          name: 'AI檢知',
          component: deepLearning
        },
        {
          path: 'dispatch',
          name: 'AI派工',
          component: dispatch
        },
        {
          path: 'dispatch_work',
          name: '維運系統',
          component: dispatch_work
        },
        {
          path: 'report',
          name: '資訊報表',
          component: report
        },
        {
          path: 'Analysis',
          name: '統計資訊',
          component: Analysis
        },
        {
          path: 'setting',
          name: '設定',
          component: setting
        },
        {
          path: 'ysolar_test',
          name: '能源展測試01',
          component: ysolar_test
        },
        {
          path: 'ysolar_test02',
          name: '能源展測試02',
          component: ysolar_test02
        },
        {
          path: 'ysolar_test03',
          name: '能源展測試03',
          component: ysolar_test03
        },
        {
          path: 'ysolar_test04',
          name: '能源展測試04',
          component: ysolar_test04
        },
        {
          path: 'documents',
          name: '文件',
          component: documents
        },
        {
          path: 'reportOverview',
          name: "報表",
          component: reportOverview
        },
        {
          path: 'stationGraphic',
          name: '電站圖面',
          component: stationGraphic
        }
      ]
    },
    {
      path: '/login',
      name: 'login',
      component: login
    },
    {
      path: '/openid_connect',
      name: 'openid_connect',
      component: openid_connect
    },
    {
      path: "/logout",
      component: {
        render(c) {
            axios.get("/logout").
            finally(
              function(){
                window.location.href = "/login"
              }
            )
        }
      }
    },
    {
      path: "/dashboard_export",
      component: dashboard
    },
    {
      path: "/WEBINFO",
      component: h('div',[
        h('h1', `Vue Version: ${VUE_VERSION}`),
        h('h4', {class: ["w-100", "text-center"]}, `© Smart Power System`),
        h('label', {class: ["w-100", "text-center"], style: {"font-size": "1px"}}, `天大地大台科大 NTUST`)
      ])
    }
  ],
  history: createWebHistory(),
  scrollBehavior() {
    return new Promise((resolve, reject) => {
      setTimeout(() => {
        resolve({ left: 0, top: 0 })
      }, 250)
    })
  },
})

export default router
