<template>
    <div>
        <div class="navbar navbar-expand-lg navbar-light mb-2">
            <div class="w-100">
                <!-- 不知道這按鈕是啥 -->
                <button class="w-100 d-lg-none btn btn-primary" type="button" data-bs-toggle="collapse" data-bs-target="#navbarNav" aria-controls="navbarNav" aria-expanded="false" aria-label="Toggle navigation" v-if="tab_datas.length>0">
                    <label v-if="pageMode != 'more'">{{button_value()}}</label>
                    <i class="fa-solid fa-ellipsis" v-else></i>
                </button>
                <!-- 上方navbar按鈕 -->
                <div class="collapse navbar-collapse" id="navbarNav">
                    <ul class="navbar-nav col-lg-12 flex-wrap" ref="my_navbar">
                        <li class="nav-item col-12 my-lg-width" v-for="tab_data in tab_first_datas" :key="tab_data.value">
                            <a class="nav-link text-dark h-100 d-flex align-items-center justify-content-center" :class="{'active': pageMode == tab_data.value}" @click="pageMode = tab_data.value"
                            style="text-align: center">
                                {{
                                    tab_data.name_i18n[$store.state.language] == undefined ?
                                    tab_data.name_i18n['zh-TW'] : tab_data.name_i18n[$store.state.language]
                                }}</a>
                        </li>
                        <li class="nav-item col-12 my-lg-width" v-if="tab_datas.length>5">
                            <a class="nav-link text-dark h-100 d-flex align-items-center justify-content-center" :class="{'active': tab_second_datas.filter(t=> t.value == pageMode).length > 0 }">
                                <el-popover
                                    placement="bottom"
                                    :width="$store.state.isMobile? '90%' : 200"
                                    trigger="click"
                                    class="p-0"
                                    popper-class="p-0"
                                >
                                    <template #reference>
                                        <div class="w-100 text-center">
                                            <i class="fa-solid fa-ellipsis"></i>
                                        </div>
                                    </template>
                                    <div class="d-flex flex-column align-items-center" v-for="tab_data in tab_second_datas" :key="tab_data.value">
                                        <button class="btn w-100 p-3" @click="pageMode = tab_data.value"
                                        :class="{'bg-warning': pageMode == tab_data.value, 'text-dark': pageMode == tab_data.value}">
                                            {{
                                                tab_data.name_i18n[$store.state.language] == undefined ?
                                                tab_data.name_i18n['zh-TW'] : tab_data.name_i18n[$store.state.language]
                                            }}
                                        </button>
                                    </div>
                                </el-popover>
                            </a>
                        </li>
                    </ul>
                </div>
            </div>
        </div>

        <transition mode="out-in" name="table_animation_to">
            <div :key="pageMode">
                <ysolar-test01 v-if="pageMode == 'ysolar_test01'"></ysolar-test01>
                <ysolar-test02 v-if="pageMode == 'ysolar_test02'"></ysolar-test02>
            </div>
        </transition>
    </div>
</template>

<script>
import ysolarTest01 from '../components/ysolar_test/ysolar_test01.vue'
import ysolarTest02 from '../components/ysolar_test/ysolar_test02.vue'

export default {
    name: "ysolar_test",
    components: {
        ysolarTest01,
        ysolarTest02
    },
    data(){
        return {
            pageMode: '',
            li_width_lg: '100%',
            tab_datas: [],
            tab_first_datas: [],
            tab_second_datas: []
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
                if(that.tab_datas.length>5){
                    that.tab_first_datas = that.tab_datas.slice(0, 5)
                    that.tab_second_datas = that.tab_datas.slice(5)
                    that.li_width_lg = `${100 / 6}%`
                }
                else{
                    that.tab_first_datas = that.tab_datas
                    that.li_width_lg = `${100 / that.tab_datas.length}%`
                }
                that.pageMode = that.tab_datas[0].value
            }
        })
    },
    mounted(){
        // this.li_width_lg = `${100 / this.$refs.my_navbar.children.length}%`
    },
    methods: {
        button_value(){
            let tab_data = this.tab_datas.find((value) => {
                return (value.value == this.pageMode)
            })
            return tab_data.name_i18n[this.$store.state.language] == undefined ?
            tab_data.name_i18n['zh-TW'] : tab_data.name_i18n[this.$store.state.language]
        }
    }
}
</script>

<style scoped>
@media (min-width: 992px){
    .my-lg-width{
        flex: 0 0 auto !important;
        width: v-bind(li_width_lg);
    }
}
</style>
