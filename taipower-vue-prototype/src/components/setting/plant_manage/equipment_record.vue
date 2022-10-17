<template>
    <div class="card p-4 mt-3">
        <h5><i class="fa-solid fa-screwdriver-wrench text-primary me-2"></i>{{$t('setting.plant_manage.設備紀錄')}}</h5>

        <!-- auto complete案場設備 -->
        <div class="d-flex flex-wrap mt-2 align-items-center">
            <div class="col-12 col-lg-5 col-xl-4 col-xxl-3">
                <autocomplete @station-select="station_select"></autocomplete>
            </div>
        </div>

        <!-- 顯示選擇的plant / lgroup / group -->
        <h6 class="text-success mt-2 ms-1">{{name}}</h6>

        <!-- div把接下來選擇設備、更改名字欄位包起來 -->
        <div class="d-flex flex-wrap align-items-top" v-if="ID != null">

            <!-- 選擇設備種類(電站/串列電流表/變流器/環境感測器) -->
            <div class="col-12 col-lg-5 col-xl-4 col-xxl-3">
                <el-select size="large" class="w-100" v-model="equip_type" @change="equip = equip_obj[equip_type][0].ID">
                    <el-option v-for="item, type in equip_obj" :key="type" :label="$t(type)" :value="type" />
                </el-select>
            </div>

            <!-- 選擇設備本身 -->
            <div class="col-12 col-lg-5 ms-lg-2 mt-2 mt-lg-0 col-xl-4 col-xxl-3">
                <el-select size="large" class="w-100" v-model="equip">
                    <el-option v-for="e in equip_obj[equip_type]" :key="e.ID"
                    :label="e.label" :value="e.ID" />
                </el-select>
            </div>

            <!-- 箭頭，如果網頁版箭頭向右，畫面縮放至一定比例(手機板)改為箭頭向下 -->
            <!-- <div class="col-12 col-lg-auto ms-lg-2 mt-2 mt-lg-0 align-self-center text-center">
                <i class="fa-solid fa-arrow-right-long fs-4 text-primary d-none d-lg-block" style="margin-bottom: 22px;"></i>
                <i class="fa-solid fa-arrow-down-long fs-4 text-primary d-lg-none"></i>
            </div> -->

            <!-- 要更改的名字 -->
            <!-- <div class="col-12 col-lg-5 col-xl-4 col-xxl-3 ms-lg-2 mt-2 mt-lg-0">
                <el-form size="large"
                ref="rename_form"
                :model="rename_form"
                :rules="rename_valid">
                    <el-form-item prop="rename">
                        <el-input v-model="rename_form.rename" />
                    </el-form-item>
                </el-form>
            </div> -->
        </div>
        
        <!-- 儲存按鈕 -->
        <!-- <div class="d-flex mt-2" v-if="ID != null">
            <button class="btn btn-success ms-auto" @click="save" :class="{'disabled': loading}">
                <div class="spinner-border" role="status" v-if="loading">
                    <span class="visually-hidden">Loading...</span>
                </div>
                <div v-else>
                    {{$t('儲存')}}
                </div>
            </button>
        </div> -->
        <div class="mt-2" v-if="ID != null">
            <el-date-picker v-model="dateTimePicker"
                        type="datetime"
                        placeholder="請選擇設備更改時間"
                        value-format="YYYY-MM-DD HH:mm:ss">
            </el-date-picker>
        </div>

        <div class="mt-2 col-12 col-lg-5 col-xl-4 col-xxl-3" v-if="ID != null">
            <el-input :disabled="this.equip_type!='inv'" v-model="kwh_key_in" placeholder="請輸入原有之kwh值"/>
            <!-- <el-input :disabled="this.equip_type!='inv' && this.equip_type!='string'" v-model="kwh_key_in" placeholder="請輸入原有之kwh值"/> -->
        </div>
        
        <div class="d-flex" v-if="ID != null">
            <button @click="handleConfirm" type="button" class="btn btn-success ms-auto">{{$t('setting.plant_manage.確定按鈕')}}</button>
        </div>
    </div>
</template>

<script>
import autocomplete from "../../autocomplete/all_type.vue"
// import { ElMessage } from 'element-plus'

export default {
    name: "fastModify",
    components: {
        autocomplete
    },
    data(){
        return {
            ID: null,
            collection: null,
            name: "",
            realName: "",
            equip_obj: {},
            equip_type: null,
            equip: null,
            kwh_key_in:null,
            test:"",
            dateTimePicker:''
            // rename_form: {
            //     rename: null,
            // },
            // rename_valid: {
            //     rename: [
            //         { required: true, message: this.$i18n.t('setting.plant_manage.please_enter_rename'), trigger: 'blur' },
            //     ]
            // },

            // loading: false
        }
    },
    methods: {
        station_select(item){
            this.ID = item.ID
            this.collection = item.collection
            this.name = item.name
            this.realName = item.realName
            // this.rename = null
            this.get_equip_select()
        },
        get_equip_select(){
            this.axios.post('/get_equip_select', {
                ID: this.ID,
                collection: this.collection
            }).then(data=>{
                console.log(data.data.data)
                this.equip_obj = {}
                this.equip_obj['station'] = [{
                    label: this.realName,
                    value: this.collection,
                    ID: this.ID
                }]
                this.equip_type = 'station'
                this.equip = this.ID
                let equip_select = data.data.data

                for(var type in equip_select){
                    if(equip_select[type].length > 0){
                        equip_select[type].forEach(element => {
                            if(type == 'inv'){
                                element.string.forEach(sm => {
                                    if(!('string' in this.equip_obj)){
                                        this.equip_obj['string'] = []
                                    }
                                    this.equip_obj['string'].push({
                                        label: sm.name,
                                        value: 'string',
                                        ID: sm.ID
                                    })
                                })                                
                            }
                            // other equip
                            if(!(type in this.equip_obj)){
                                this.equip_obj[type] = []
                            }
                            this.equip_obj[type].push({
                                label: element.name,
                                value: type,
                                ID: element.ID
                            })
                        })
                    }
                }
            })
        },
        // save(){
        //     this.$refs.rename_form.validate().then(result => {
        //         const answer = confirm(this.$i18n.t('setting.plant_manage.confirm_rename'))
        //         if(!answer)
        //             return false
        //         this.loading = true
        //         this.axios.post('/change_equip_name', {
        //             ID: this.equip,
        //             rename: this.rename_form.rename
        //         }).then(data=>{
        //             if(data.data.data.status == true){
        //                 ElMessage.success(this.$i18n.t('成功'))
        //                 this.reset()
        //             }else{
        //                 if(data.data.data.result == "duplicated"){
        //                     ElMessage.error(this.$i18n.t('setting.plant_manage.名稱重複'))
        //                 }else{
        //                     ElMessage.error(this.$i18n.t('錯誤'))
        //                 }
        //             }
        //             this.loading = false
        //         })
        //     }).catch()
        // },
        reset(){
            this.ID = null
            this.collection = null
            this.name = ""
            this.realName = ""
            // this.rename = null
        },
        async handleConfirm(){
            console.log('================================')
            // 設備所在位置
            console.log('realName : ' + this.realName)
            // 設備所在位置(全路徑)
            console.log('name : ' + this.name)
            // 設備所在位置id
            console.log('ID : ' + this.ID)
            // 設備所在位置(plant/lgroup/group)
            console.log('collection : ' + this.collection)
            // 設備ID
            console.log('equip : ' + this.equip)
            // 輸入的時間
            console.log('time : ' + this.dateTimePicker)
            // 輸入的kwh
            console.log('kwh : ' + this.kwh_key_in)
            // 設備type
            console.log('type : ' + this.equip_type)
			const typeObj = {'realName':this.realName,
                    'name':this.name,
                    'ID':this.ID,
                    'collection':this.collection,
                    'equip':this.equip,
                    'time':this.dateTimePicker,
                    'kwh':this.kwh_key_in,
                    'equip_type':this.equip_type
			};
		await this.axios.post('/setting/equipment_record', typeObj
			).then(typeObj => {
            }).catch(err=>{
				console.log(err)
			})
			// console.log(this.start_date , this.end_date, this.type, this.name)
			// this.change_username_password_modal.hide()
        },
    }
}
</script>