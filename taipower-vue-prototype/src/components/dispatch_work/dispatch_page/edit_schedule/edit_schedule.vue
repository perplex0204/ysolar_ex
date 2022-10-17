<template>
    <div>
        <div>
            <div class="d-flex">
                <button class="btn btn-warning"
                @click="finish">
                    <i class="fa-solid fa-angle-left"></i>
                </button>
            </div>
            <div class="col-12 mt-3">
                <div class="card p-2 pt-4">
                    <div class="d-flex align-items-center">
                        <h5 class="mb-0"><i class="icon-wrench text-primary"></i>{{$t('dispatch.排程')}}</h5>
                    </div>
                    <div class="mt-3">
                        <div class="row ps-2 pe-2 mb-2">
                            <div class="col-12 mt-2 mt-lg-0">
                                <div class="d-flex mb-2 align-items-center">
                                    {{$t('dispatch.工作內容')}}
                                    <button class="btn btn-warning ms-auto"
                                    @click="group_edit.enable = true" v-if="!group_delete.enable">
                                        <i class="fas fa-plus"></i>
                                    </button>
                                    <button class="btn"
                                    @click="group_delete.enable = true" v-if="!group_delete.enable">
                                        <i class="fas fa-minus"></i>
                                    </button>
                                    <button class="btn btn-danger ms-auto" v-if="group_delete.enable"
                                    @click="group_delete_save">{{$t('完成')}}</button>
                                </div>
                                <div class="card m-2 p-2" v-if="group_delete.enable">
                                    <label class="mb-2 fs-7" v-if="group_delete.enable">{{$t('dispatch.請點選來刪除')}}</label>
                                    <div class="d-flex flex-wrap">
                                        <div class="check_content p-2 ms-2 shaking_div"
                                        v-for="group in schedule_group" :key="group.name"
                                        :class="{'alert-danger': group_delete.delete_list.includes(group.name), 
                                        }"
                                        @click="group_click_prepare_delete(group.name)"
                                        >
                                            <i class="fas fa-times-circle text-danger"
                                            v-if="group_delete.delete_list.includes(group.name)"></i>
                                            {{group.name}}
                                        </div>
                                    </div>
                                </div>
                                <div class="card p-2 me-4 mb-4" v-if="group_edit.enable">
                                    <div class="d-flex align-items-center flex-wrap p-2">
                                        <button class="btn"
                                        @click="group_edit.enable=false"><i class="fas fa-times-circle text-danger"></i></button> 
                                        <label>{{$t('dispatch.群組名稱')}}：</label>
                                        <div class="col-12 col-lg-4">
                                            <el-input v-model="group_edit.name" />
                                        </div>
                                        <button class="btn btn-success ms-lg-auto" @click="group_edit_save">{{$t('儲存')}}</button>
                                    </div>
                                </div>
                                <el-collapse class="w-100">
                                    <el-collapse-item v-for="group in schedule_group" :key="group.name">
                                        <template #title>
                                            <div class="w-100 d-flex">
                                                <div class="ms-2" v-if="!group.name_edit.enable">
                                                    {{group.name}}
                                                </div>
                                                <div class="col-12 col-lg-5 col-xl-4 col-xxl-3 d-flex align-items-center" v-if="group.name_edit.enable">
                                                    <el-input size="default" class="mt-2 mb-2" v-model="group.name_edit.name"  />
                                                </div>
                                                <button class="btn btn-success mt-2 mb-2 ms-auto" v-if="group.name_edit.enable"
                                                @click.stop="group_name_edit_save(group)">{{$t('儲存')}}</button>
                                                <button class="ms-auto btn" v-if="!group.name_edit.enable"
                                                @click.stop="group.name_edit.enable=true">
                                                    <i class="fa-solid fa-gear"></i>
                                                </button>
                                            </div>
                                        </template>
                                        <div class="d-flex w-100 pe-2">
                                            <label v-if="group.child_delete.enable">{{$t('dispatch.請點選來刪除')}}</label>
                                            <button class="btn btn-primary ms-auto"
                                            v-if="!group.child_delete.enable"
                                            @click="group.child_edit.enable=true">
                                                <i class="fas fa-plus"></i>
                                            </button>
                                            <button class="btn" @click="group.child_delete.enable=true">
                                                <i class="fas fa-minus"
                                                v-if="!group.child_delete.enable"></i></button>
                                            <button class="btn btn-danger ms-auto" v-if="group.child_delete.enable"
                                            @click="child_delete_save(group)">{{$t('儲存')}}</button>
                                        </div>
                                        <div class="d-flex flex-wrap">
                                            <div class="check_content p-2 ms-2"
                                            v-for="child in group.child" :key="child.name"
                                            :class="{'alert-danger': group.child_delete.delete_list.includes(child.name), 
                                            'shaking_div': group.child_delete.enable}" @click="group_click(group, child)">
                                                <i class="fas fa-times-circle text-danger"
                                                v-if="group.child_delete.delete_list.includes(child.name)"></i>
                                                {{child.name}}
                                            </div>
                                        </div>
                                        <div class="card p-2 me-4 mt-2" v-if="group.child_edit.enable==true">
                                        <div class="d-flex align-items-center flex-wrap">
                                            <button class="btn mt-2"
                                            @click="reset_child_edit(group)">
                                                <i class="fas fa-times-circle text-danger"></i>
                                            </button> 
                                            <label class="mt-2">{{$t('dispatch.項目名稱')}}：</label>
                                            <div class="col-12 col-lg-4 col-xl-5 col-xxl-3">
                                                <input class="form-control mt-2 " v-model="group.child_edit.name" />
                                            </div>
                                            <label class="mt-2 ms-lg-2">{{$t('dispatch.項目類別')}}：</label>
                                            <div class="col-12 col-lg-4">
                                                <select class="form-control mt-2" v-model="group.child_edit.category">
                                                    <option value="none" selected>{{$t('dispatch.請選擇類別')}}</option>
                                                    <option value="choice">{{$t('dispatch.正常/異常')}}</option>
                                                    <option value="numeric">{{$t('dispatch.數值')}}</option>
                                                    <option value="normal_choice_na" v-if="!['taipower'].includes($store.state.user_data.pageType)">{{$t('dispatch.正常/異常/NA')}}</option>
                                                    <option value="yes_choice_na" v-if="!['taipower'].includes($store.state.user_data.pageType)">{{$t('dispatch.是/否/NA')}}</option>
                                                </select>
                                            </div>
                                            <label class="mt-2 ms-lg-2" v-if="group.child_edit.category == 'numeric'">{{$t('dispatch.建議數值')}}：</label>
                                            <div class="col-12 col-lg-5 col-xl-4 col-xxl-3" v-if="group.child_edit.category == 'numeric'">
                                                <input class="form-control mt-2 " type="number" v-model="group.child_edit.suggest_value" />
                                            </div>
                                            <div class="d-flex ms-lg-2 col-lg-5 col-xl-4 col-xxl-3 mt-2
                                            align-items-center">
                                                <input class="form-check-input mt-0" type="checkbox" value="" v-model="group.child_edit.photo_required" />
                                                <label>{{$t('dispatch.需要照片上傳')}}</label>
                                            </div>
                                            <button class="btn btn-success ms-auto mt-2" @click="child_edit_save(group)">{{$t('儲存')}}</button>
                                        </div>
                                    </div>
                                    </el-collapse-item>
                                </el-collapse>
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
    name: "EditSchedule",
    emits: ['dispatch-edit-finish'],
    props:{
        scheduleData: {
            type: Array,
            default: ()=>{
                return []
            }
        },
        dispatchData: {
            type: Object,
            required: true
        },
        scheduleType: {
            type: String,
            required: true
        }
    },
    data(){
        return {
            schedule_group: [
            ],
            group_edit: {
                name: null,
                enable: false
            },
            group_delete:{
                enable: false,
                delete_list: []
            },
        }
    },
    methods: {
        finish(){
            const answer = confirm("是否儲存？")
            if(answer){
                this.axios.post('/dispatch_edit_content', {
                    dispatch_ID: this.dispatchData._id,
                    type: this.scheduleType,
                    data: this.schedule_group
                }).then(data=>{
                    this.$emit('dispatch-edit-finish')
                })
                
            }else{
                this.$emit('dispatch-edit-finish')
            }
        },
        //-----------------------------------------------------------------------------
        child_delete_save(group){
            let _new_child_list = []
            group.child.forEach(child => {
                if(!(group.child_delete.delete_list.includes(child.name))){
                    _new_child_list.push(child)
                }
            })
            group.child = _new_child_list
            group.child_delete.delete_list = []
            group.child_delete.enable = false
        },
        group_click(group, child){
            if(group.child_delete.enable){
                if(group.child_delete.delete_list.includes(child.name)){
                    const index = group.child_delete.delete_list.indexOf(child.name)
                    group.child_delete.delete_list.splice(index,1)
                }else{
                    group.child_delete.delete_list.push(child.name)
                }
            }else{
                group.child_edit.enable = true
                group.child_edit.name = child.name
                group.child_edit.origin_name = child.name
                group.child_edit.category = child.category
                group.child_edit.suggest_value = child.suggest_value
                group.child_edit.photo_required = child.photo_required
            }
        },
        child_edit_save(group){
            let error_str = ""
            // Error Alert
            if(group.child_edit.name == '' || group.child_edit.name == null){
                error_str += this.$i18n.t('dispatch["name_blank"]')
            }
            if(group.child_edit.category == '' || group.child_edit.category == null || group.child_edit.category == 'none'){
                error_str += `\n${this.$i18n.t('dispatch["category_blank"]')}`
            }
            if(error_str != ""){
                alert(error_str)
                return false
            }
            // Reset 
            group.child_edit.enable = false
            // Delete Original if name_change
            for(var i in group.child){
                if(group.child_edit.origin_name != null && group.child_edit.origin_name != group.child_edit.name){
                    group.child.splice(i,1)
                    break
                }
            }
            // Overide if already exist
            for(var i in group.child){
                let child = group.child[i]
                if(child.name == group.child_edit.name){
                    child.category = group.child_edit.category
                    child.suggest_value = group.child_edit.suggest_value
                    child.photo_required = group.child_edit.photo_required
                    // Reset 
                    group.child_edit.name = null
                    group.child_edit.category = "none"
                    group.child_edit.suggest_value = null
                    group.child_edit.photo_required = false
                    return true
                }
            }
            // push new one
            group.child.push({
                name: group.child_edit.name,
                category: group.child_edit.category,
                suggest_value: group.child_edit.suggest_value,
                photo_required: group.child_edit.photo_required
            })
            // Reset 
            group.child_edit.name = null
            group.child_edit.category = "none"
            group.child_edit.suggest_value = null
            group.child_edit.photo_required = false

        },
        reset_child_edit(group){
            group.child_edit = {
                name: null,
                origin_name: null,
                category: "none",
                suggest_value: null,
                photo_required: false,
                enable: false,
            }
        },
        group_edit_save(){
            if(this.group_edit.name == null || this.group_edit.name == ""){
                alert(this.$i18n.t('dispatch["name_blank"]'))
                return false
            }
            for(var i in this.schedule_group){
                if(this.schedule_group[i].name == this.group_edit.name){
                    alert(this.$i18n.t('dispatch["name_duplicate"]'))
                    return false
                }
            }
            this.schedule_group.push(
                {
                    name: this.group_edit.name, 
                    child: [],
                    child_delete: {
                        enable: false,
                        delete_list: [],
                    },
                    child_edit: {
                        name: null,
                        origin_name: null,
                        category: "none",
                        suggest_value: null,
                        photo_required: false,
                        enable: false,
                    },
                    name_edit:{
                        name: this.group_edit.name,
                        enable: false
                    },
                }
            )
            this.group_edit.enable = false
            this.group_edit.name = null
        },
        group_click_prepare_delete(name){
            if(this.group_delete.delete_list.includes(name)){
                let index = this.group_delete.delete_list.indexOf(name)
                this.group_delete.delete_list.splice(index, 1)
            }else{
                this.group_delete.delete_list.push(name)
            }
        },
        group_delete_save(){
            this.group_delete.delete_list.forEach(name => {
                let index = -1
                for(var i in this.schedule_group){
                    if(this.schedule_group.name == name){
                        index = i
                    }
                }
                this.schedule_group.splice(index, 1)
            })
            this.group_delete.enable = false
        },
        group_name_edit_save(group){
            if(group.name_edit.name == null || group.name_edit.name == ""){
                alert(this.$i18n.t('dispatch["name_blank"]'))
                return false
            }
            group.name_edit.enable = false
            group.name = group.name_edit.name
        },
    },
    mounted(){
        console.log(this.scheduleData)
        this.schedule_group = [
        ]
        this.scheduleData.forEach(group => {
            let _group = {}
            Object.assign(_group, group)
            //child dict to list
            _group.child = []
            for(var group_name in group.child){
                _group.child.push({
                    name: group.child[group_name].name,
                    origin_name: group.child[group_name].origin_name,
                    category: group.child[group_name].category,
                    suggest_value: group.child[group_name].suggest_value,
                    photo_required: group.child[group_name].photo_required,
                    enable: false

                })
            }

            _group.child_delete = {
                enable: false,
                delete_list: [],
            }
            _group.child_edit = {
                name: null,
                origin_name: null,
                category: "none",
                suggest_value: null,
                photo_required: false,
                enable: false,
            }
            _group.name_edit = {
                name: _group.name,
                enable: false
            }
            this.schedule_group.push(_group)
        })
        console.log(this.schedule_group)
    }
}
</script>