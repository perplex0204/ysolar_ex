<template>
    <div class="card p-4" v-loading="loading">
		<h5>
			<i class="fa-solid fa-chart-bar text-primary"></i>
            {{$t("setting.data_integrity.統計資料")}}
		</h5>
        <div class="mb-3 d-flex flex-column">
            <label><i class="fa-solid fa-industry"></i> {{ $t("setting.data_integrity.案場選擇") }}：{{id == null ? $t('全部') : name}}</label>
            <label><i class="fa-solid fa-clock"></i> {{ $t("setting.data_integrity.時間篩選") }}：{{dateMode == 'single' ? startDate : `${startDate}~${endDate}`}}</label>
        </div>
        <!-- Done For All -->
        <div class="w-100 text-center mb-3" v-if="total_done">
            <h1><i class="fa-solid fa-circle-check text-success"></i></h1>
            <h6>{{$t("setting.data_integrity.all_done")}}</h6>
        </div>
        <div class="w-100 text-center mb-3" v-else>
            <h1><i class="fa-solid fa-triangle-exclamation text-danger"></i></h1>
            <h6>{{$t("setting.data_integrity.all_done_false")}}</h6>
        </div>
        <!-- Self 資料 -->
        <div v-if="id != null">
            <h6><i class="fa-solid fa-solar-panel me-1"></i>{{$t('setting.data_integrity.案場資訊')}}</h6>
            <div class="d-flex flex-column">
                <label>{{$t('setting.data_integrity.案場名稱')}}：{{info_dict.name}}
                    <el-popover
                        placement="top-start"
                        :width="200"
                        trigger="hover"
                        :content="info_dict._id"
                    >
                        <template #reference>
                            <button class="btn d-inline-block"><i class="fa-solid fa-circle-info"></i></button>
                        </template>
                    </el-popover>
                </label>
                <label>Collection：{{info_dict.collection}}</label>
                <label>{{$t('setting.data_integrity.是否為虛擬層')}}：
                    <i class="fa-solid fa-check" v-if="info_dict.virtual != 0"></i>
                    <i class="fa-solid fa-xmark" v-else></i>
                </label>
            </div>
            <!-- self, done false -->
            <p class="fst-italic mt-2 mb-0">{{$t('setting.data_integrity.尚未補遺完成')}}</p>
            <div class="table-responsive" style="max-height: 50vh; overflow-y: scroll;" v-if="self_lost.length > 0">
                <table class="table table-striped">
                    <thead class="table-light">
                        <tr>
                            <th>{{$t('setting.data_integrity.時間')}}</th>
                            <th>{{$t('setting.data_integrity.區間')}}</th>
                            <th>{{$t('setting.data_integrity.目前完整度')}}</th>
                        </tr>
                    </thead>
                    <tbody>
                        <tr v-for="data in self_lost" :key="data._id">
                            <td>{{data.time}}</td>
                            <td>{{data.time_interval}}</td>
                            <td>{{data.rate}}</td>
                        </tr>
                    </tbody>
                </table>
            </div>
            <label class="w-100 text-center" v-else>{{$t('無資料')}}</label>
            <!-- self, done true -->
            <p class="fst-italic mt-2 mb-0">{{$t('setting.data_integrity.已上傳補遺完成')}}</p>
            <div class="table-responsive" style="max-height: 50vh; overflow-y: scroll;" v-if="self_done.length > 0">
                <table class="table table-striped">
                    <thead class="table-light">
                        <tr>
                            <th>{{$t('setting.data_integrity.時間')}}</th>
                            <th>{{$t('setting.data_integrity.區間')}}</th>
                            <th>{{$t('setting.data_integrity.完整度')}}</th>
                            <th>{{$t('setting.data_integrity.補算完成')}}</th>
                        </tr>
                    </thead>
                    <tbody>
                        <tr v-for="data in self_done" :key="data._id">
                            <td>{{data.time}}</td>
                            <td>{{data.time_interval}}</td>
                            <td>{{data.rate}}</td>
                            <td>{{data.cal_restart_done}}</td>
                        </tr>
                    </tbody>
                </table>
            </div>
            <label class="w-100 text-center" v-else>{{$t('無資料')}}</label>
        </div>
        <!-- Child and all not done -->
        <h6 class="mt-3"><i class="fa-solid fa-triangle-exclamation me-1"></i>{{$t('setting.data_integrity.子項目未完成補遺項目')}}</h6>
        <div class="table-responsive mt-2" style="max-height: 50vh; overflow-y: scroll;" v-if="child_lost.length > 0">
            <table class="table table-striped">
                <thead class="table-light">
                    <tr>
                        <th>{{$t('setting.data_integrity.名稱')}}</th>
                        <th>{{$t('setting.data_integrity.時間')}}</th>
                        <th>{{$t('setting.data_integrity.區間')}}</th>
                        <th>{{$t('setting.data_integrity.階層')}}</th>
                        <th>{{$t('setting.data_integrity.是否為虛擬層')}}</th>
                        <th>{{$t('setting.data_integrity.目前完整度')}}</th>
                    </tr>
                </thead>
                <tbody>
                    <tr v-for="data in child_lost" :key="data._id">
                        <td>
                            <div class="d-flex align-items-center">
                                {{data.name}}
                                <el-popover
                                    placement="top-start"
                                    :width="200"
                                    trigger="hover"
                                    :content="data.ID"
                                >
                                    <template #reference>
                                        <button class="btn d-inline-block"><i class="fa-solid fa-circle-info"></i></button>
                                    </template>
                                </el-popover>
                            </div>
                        </td>
                        <td>{{data.time}}</td>
                        <td>{{data.time_interval}}</td>
                        <td>{{data.level}}</td>
                        <td><i class="fa-solid fa-check" v-if="data.virtual != 0"></i></td>
                        <td>{{data.rate}}</td>
                    </tr>
                </tbody>
            </table>
        </div>
        <label class="w-100 text-center" v-else>{{$t('無資料')}}</label>
        <!-- Child and all rate error -->
        <h6 class="mt-3"><i class="fa-solid fa-exclamation me-1"></i>{{$t('setting.data_integrity.child_done_but_rate_not_1')}}</h6>
        <div class="table-responsive mt-2" style="max-height: 50vh; overflow-y: scroll;" v-if="child_rate_strange.length > 0">
            <table class="table table-striped">
                <thead class="table-light">
                    <tr>
                        <th>{{$t('setting.data_integrity.名稱')}}</th>
                        <th>{{$t('setting.data_integrity.時間')}}</th>
                        <th>{{$t('setting.data_integrity.區間')}}</th>
                        <th>{{$t('setting.data_integrity.階層')}}</th>
                        <th>{{$t('setting.data_integrity.是否為虛擬層')}}</th>
                        <th>{{$t('setting.data_integrity.完整度')}}</th>
                    </tr>
                </thead>
                <tbody>
                    <tr v-for="data in child_rate_strange" :key="data._id">
                        <td>
                            <div class="d-flex align-items-center">
                                {{data.name}}
                                <el-popover
                                    placement="top-start"
                                    :width="200"
                                    trigger="hover"
                                    :content="data.ID"
                                >
                                    <template #reference>
                                        <button class="btn d-inline-block"><i class="fa-solid fa-circle-info"></i></button>
                                    </template>
                                </el-popover>
                            </div>
                        </td>
                        <td>{{data.time}}</td>
                        <td>{{data.time_interval}}</td>
                        <td>{{data.level}}</td>
                        <td><i class="fa-solid fa-check" v-if="data.virtual != 0"></i></td>
                        <td>{{data.rate}}</td>
                    </tr>
                </tbody>
            </table>
        </div>
        <label class="w-100 text-center" v-else>{{$t('無資料')}}</label>
	</div>
</template>

<script>
import c from "assets/js/common.js"

export default {
    name: "stats",
    props: {
        id: {
            default: null
        },
        collection: {
            default: null
        },
        name: {
            default: ""
        },
        startDate: {
            dafault: c.formatDate(new Date),
        },
        endDate: {
            default: c.formatDate(new Date),
        },
        dateMode: {
            default: 'single'
        }
    },
    data(){
        return {
            child_lost: [],
            child_rate_strange: [],
            info_dict: {},
            self_lost: [],
            self_done: [],
            total_done: false,
            loading: false,
        }
    },
    methods: {
        get_data_integrity_stats(){
            this.loading = true
            this.axios.post('/get_data_integrity_stats', {
                ID: this.id,
                start_date: this.startDate,
                end_date: this.endDate,
                date_mode: this.dateMode
            }).then(data=>{
                console.log(data.data.data)
                this.child_lost = data.data.data.child_lost
                this.info_dict = data.data.data.info_dict
                this.total_done = data.data.data.done
                this.self_lost = data.data.data.self_lost
                this.self_done = data.data.data.self_done
                this.child_rate_strange = data.data.data.child_rate_strange
                this.loading = false
            })
        }
    },
    watch: {
        id(){
            this.get_data_integrity_stats()
        },
        startDate(){
            this.get_data_integrity_stats()
        },
        endDate(){
            this.get_data_integrity_stats()
        },
        date_mode(){
            this.get_data_integrity_stats()
        }
    }
}
</script>