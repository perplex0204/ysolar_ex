<template>
    <el-popover
        placement="bottom"
        :width="300"
        trigger="click"
        title=""
        :disabled="disabled"
        v-if="Object.keys(my_data).length > 0"
        @hide="save_data"      
    >
        <template #reference>
            <el-button class="w-100" size="large" style="height: auto;">
                <div class="d-flex flex-wrap justify-content-center align-items-center">
                    <div v-if="my_data.plant[0] == 'total'">{{$t('全部')}}</div>
                    <div v-if="my_data.plant[0] != 'total'">{{my_data.plant[0]}}</div>
                    <div class="d-flex" v-if="my_data.plant[0] != 'total' && my_data.plant.length > 1">
                        <label>{{$t('setting.users.與其他')}}</label>
                        <label class="ms-1 me-1">{{my_data.plant.length-1}}</label>
                        <label>{{$t('setting.users.個案場')}}</label>
                    </div>
                </div>
            </el-button>
        </template>
        <div class="w-100 text-center">
            <el-switch
            v-model="my_data.plant_total"
            @change="switch_change"
            :active-text="$t('全部')"
            inactive-text="" />
        </div>
        <div v-if="!my_data.plant_total">
            <!-- alert plant can not be empty -->
            <p class="fw-light m-0 text-danger" v-if="my_data.plant.length == 0"
            style="font-size: .75rem;"><i class="fas fa-exclamation-circle"></i>{{$t("setting.users.plant_empty_error")}}</p>
            <div class="col-12">
                <autocomplete @station-select="station_select"></autocomplete>
            </div>
            <div class="col-12 d-flex flex-wrap">
                <div class="card p-2 me-2 mt-2 bg-secondary"
                v-for="plant in my_data.plant"
                :key="plant">
                    <div class="d-flex flex-wrap justify-content-center align-items-center">
                        <button class="btn p-0" style="width: fit-content;" @click="remove_plant(plant)">
                            <i class="fa-solid fa-xmark"></i>
                        </button>
                        <label>{{plant}}</label>
                    </div>
                </div>
            </div>
        </div>
    </el-popover>
</template>
<script>
import autocomplete from '../../autocomplete/plant_only.vue'

export default {
    name: "Plant_access",
    components: {
        autocomplete
    },
    props: {
        userData: {
            type: Object
        },
        disabled: {
            type: Boolean,
            default: false
        }
    },
    data(){
        return {
            my_data: {
                
            }
        }
    },
    emits: ['update_plant'],
    methods: {
        switch_change(){
            if(this.my_data.plant_total == true){
                this.my_data.plant = ['total']
            }
            else{
                this.my_data.plant = []
            }
        },
        station_select(item){
            if(!this.my_data.plant.includes(item.name)){
                this.my_data.plant.push(item.name)
            }
        },
        remove_plant(plant){
            const index = this.my_data.plant.indexOf(plant)
            this.my_data.plant.splice(index, 1)
        },
        save_data(){
            if(this.my_data.plant.length == 0){
                alert(this.$i18n.t("setting.users.plant_empty_error"))
                this.set_my_data()
            }
            else{
                this.$emit('update_plant', this.my_data.plant)
            }
        },
        set_my_data(){
           this.my_data.plant =  this.userData.plant.slice(0)
           this.my_data.level = this.userData.level
            if(this.userData.plant[0] == 'total'){
                this.my_data.plant_total = true
            }else{
                this.my_data.plant_total = false
            }
            //console.log(this.my_data)
        }
    },
    mounted(){
        this.set_my_data()
    },
    watch: {
        userData(){
            this.set_my_data()
        }
    }
}
</script>