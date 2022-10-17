<template>
    <div>
        <div :class="{'d-lg-flex': $store.state.user_data.pageType == 'taipower'}">
            <div class="complete col-12 col-lg-3 me-lg-2" :class="{'mb-2': $store.state.user_data.pageType != 'taipower', 'mb-3': $store.state.user_data.pageType == 'taipower'}">
                <autocomplete @station-select="station_select" @search-select="search_select" :preSelect="$store.state.user_data.pageType == 'taipower'"></autocomplete>
            </div>
            <div class="selection mb-2 col-lg-3">
                <el-select v-model="value" class="col-12 col-lg-12" size="large">
                    <el-option
                        v-for="item in options"
                        :key="item.value"
                        :label="$t(`report.${item.label}`)"
                        :value="item.value"
                    >
                    </el-option>
                </el-select>
            </div>
        </div>
        <timeRangePickerSimple @setDate="setDate" :class="{'mt-lg-2': $store.state.user_data.pageType != 'taipower'}" />

        <div class="modal fade" id="modal">
            <div class="modal-dialog modal-dialog-centered modal-fullscreen-lg-down modal-dialog-scrollable">
                <div class="modal-content">
                    <div class="modal-header">
                        <h5 class="modal-title">{{$t("預覽")}}</h5>
                        <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
                    </div>
                    <div class="modal-body">
                        <div ref="file"></div>
                    </div>
                    <div class="modal-footer">
                        <button type="button" class="btn btn-secondary me-auto" data-bs-dismiss="modal">{{$t("關閉")}}</button>
                        <button class="btn btn-primary" @click="download_active">{{$t("report.download")}}</button>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>



<script>
import autocomplete from "../autocomplete/all_type.vue"
import TimeRangePickerSimple from "@/components/datepicker/timeRangePickerSimple.vue"
import { ElLoading } from 'element-plus'
import {Modal} from 'bootstrap'
let docx = require("docx-preview")
export default {
    name: "reportRealTime",
    components:{
        TimeRangePickerSimple,
        autocomplete
    },
    data(){
        return {
            date_selection:{},
            options:[
               {
                   value:"year",
                   label:"year"
               },
               {
                   value:"month",
                   label:"month"
               },
               {
                   value:"day",
                   label:"day"
               },
               {
                   value:"hour",
                   label:"hour"
               },
               {
                   value:"15min",
                   label:"15min"
               }
            ],
            value:"day",
            plant_select: {'ID_list': [], 'col_list': []},
            device_id:"",
            search: "",
            response: undefined
        }
    },
    methods:{
        station_select(item) {
			//console.log(item)
			if(item.name == '無資料'){
				return false
			}
            this.plant_select = {
                ID_list: [item.ID],
                col_list: [item.collection]
            }
		},
        search_select(item){
            this.search = item
        },
        async download(){
            let that = this
            const loadingInstance = ElLoading.service()
            let response = await this.axios.post('/word_generator',{
                ID: this.device_id,
                datepicker1: this.date_selection.date_list[0],
                datepicker2: this.date_selection.date_list[1],
                time_interval: this.value
            }, { responseType: 'blob' })
            if (response.status === 200){
                console.log(response)
                this.myModal.show()
                docx.renderAsync(response.data, this.$refs.file)
                this.response = response
                // that.myModal.show()
            }
            else{
                console.log("Bad Request")
            }
            loadingInstance.close()
        },
        async download_active(){
            try{
                this.myModal.hide()
                let contentDisposition = this.response.headers["content-disposition"]
                let matches = contentDisposition.split("filename=")
                let filename = "report.docx"
                if (matches != null && matches[1]) {
                    filename = matches[1].replace(/['"]/g, '')
                    filename = decodeURIComponent(filename)
                }

                let obj = [new Blob([this.response.data], {type: ''}), filename]
                let link = document.createElement("a")
                document.body.appendChild(link)
                link.href = URL.createObjectURL(obj[0], {type: ''})
                link.download = obj[1]
                link.click()
                document.body.removeChild(link)
            }
            catch{
                console.log("no report")
            }
        },
        setDate(date){
            this.date_selection = date
        }
    },
    watch: {
        date_selection(){
            if (this.search != ""){
                var start_time = new Date(this.date_selection.date_list[0].replace(/-/g, "/"))
                var end_time = new Date(this.date_selection.date_list[1].replace(/-/g, "/"))
                var delta_time_s = (end_time.getTime() - start_time.getTime())/1000
                var delta_days = Math.floor(delta_time_s/(24*3600))
                if (this.value == "year" && delta_days > 2192){
                    alert("輸入年區間超過6年! 請重新輸入")
                }
                else if (this.value == "month" && delta_days > 366){
                    alert("輸入月區間超過12個月! 請重新輸入")
                }
                else if (this.value == "day" && delta_days > 14){
                    alert("輸入天數超過14天! 請重新輸入")
                }
                else if (this.value == "hour" && delta_days > 7){
                    alert("輸入時區間超過7天! 請重新輸入")
                }
                else if (this.value == "15min" && delta_days > 2){
                    alert("輸入分區間超過2天! 請重新輸入")
                }
                else{
                    for (var i=0; i<this.plant_select["ID_list"].length; i++){
                        this.device_id = this.plant_select["ID_list"][i]
                        this.download()
                    }
                }
            }
        },
    },
    mounted(){
        this.myModal = new Modal(document.getElementById('modal'), {backdrop: 'static', keyboard: false})
    },
}
</script>

<style scoped>
@media (min-width: 992px){
    .modal-dialog{
        width: 95vw !important;
        max-width: 95vw !important;
    }
}
</style>