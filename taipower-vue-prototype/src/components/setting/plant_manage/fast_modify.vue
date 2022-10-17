<template>
    <div class="card p-4">
        <h5><i class="fa-solid fa-screwdriver-wrench text-primary me-2"></i>{{$t('setting.plant_manage.名稱更改')}}</h5>
        <div class="d-flex flex-wrap mt-2 align-items-center">
            <div class="col-12 col-lg-5 col-xl-4 col-xxl-3">
                <autocomplete @station-select="station_select"></autocomplete>
            </div>
        </div>
        <h6 class="text-success mt-2 ms-1">{{name}}</h6>
        <div class="d-flex flex-wrap align-items-top" v-if="ID != null">
            <div class="col-12 col-lg-5 col-xl-4 col-xxl-3">
                <el-select size="large" class="w-100" v-model="equip_type"
                @change="equip = equip_obj[equip_type][0].ID">
                    <el-option v-for="item, type in equip_obj" :key="type"
                    :label="$t(type)" :value="type" />
                </el-select>
            </div>
            <div class="col-12 col-lg-5 ms-lg-2 mt-2 mt-lg-0">
                <el-select size="large" class="w-100" v-model="equip">
                    <el-option v-for="e in equip_obj[equip_type]" :key="e.ID"
                    :label="e.label" :value="e.ID" />
                </el-select>
            </div>
            <div class="col-12 col-lg-auto ms-lg-2 mt-2 mt-lg-0 align-self-center text-center">
                <i class="fa-solid fa-arrow-right-long fs-4 text-primary d-none d-lg-block" style="margin-bottom: 22px;"></i>
                <i class="fa-solid fa-arrow-down-long fs-4 text-primary d-lg-none"></i>
            </div>
            <div class="col-12 col-lg-5 col-xl-4 col-xxl-3 ms-lg-2 mt-2 mt-lg-0">
                <el-form size="large"
                ref="rename_form"
                :model="rename_form"
                :rules="rename_valid">
                    <el-form-item prop="rename">
                        <el-input v-model="rename_form.rename" />
                    </el-form-item>
                </el-form>
            </div>
        </div>
        <div class="d-flex mt-2" v-if="ID != null">
            <button class="btn btn-success ms-auto" @click="save" :class="{'disabled': loading}">
                <div class="spinner-border" role="status" v-if="loading">
                    <span class="visually-hidden">Loading...</span>
                </div>
                <div v-else>
                    {{$t('儲存')}}
                </div>
            </button>
        </div>
    </div>
</template>

<script>
import autocomplete from "../../autocomplete/all_type.vue"
import { ElMessage } from 'element-plus'

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
            rename_form: {
                rename: null,
            },
            rename_valid: {
                rename: [
                    { required: true, message: this.$i18n.t('setting.plant_manage.please_enter_rename'), trigger: 'blur' },
                ]
            },
            loading: false
        }
    },
    methods: {
        station_select(item){
            this.ID = item.ID
            this.collection = item.collection
            this.name = item.name
            this.realName = item.realName
            this.rename = null
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
                console.log(this.equip_obj)
            })
        },
        save(){
            this.$refs.rename_form.validate().then(result => {
                const answer = confirm(this.$i18n.t('setting.plant_manage.confirm_rename'))
                if(!answer)
                    return false
                this.loading = true
                this.axios.post('/change_equip_name', {
                    ID: this.equip,
                    rename: this.rename_form.rename
                }).then(data=>{
                    if(data.data.data.status == true){
                        ElMessage.success(this.$i18n.t('成功'))
                        this.reset()
                    }else{
                        if(data.data.data.result == "duplicated"){
                            ElMessage.error(this.$i18n.t('setting.plant_manage.名稱重複'))
                        }else{
                            ElMessage.error(this.$i18n.t('錯誤'))
                        }
                    }
                    this.loading = false
                })
            }).catch()
        },
        reset(){
            this.ID = null
            this.collection = null
            this.name = ""
            this.realName = ""
            this.rename = null
        }
    }
}
</script>
