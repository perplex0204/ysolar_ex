<template>
    <div>
        <!-- Interval Selection is Dropdown On Mobile Device -->
        <div class="row g-0 mt-2 me-2 d-block d-lg-none">
            <div class="dropdown col-12">
                <button class="btn btn-primary dropdown-toggle w-100" type="button" id="interval_dropdown" 
                data-bs-toggle="dropdown" aria-expanded="false" :class="{'active': mode != 'single' && mode != 'interval'}">
                    {{dropdown_text}}
                </button>
                <ul class="dropdown-menu w-100" aria-labelledby="interval_dropdown">
                    <li><a class="dropdown-item" @click="dropdownSelect('all')">{{$t('全部')}}</a></li>
                    <li><a class="dropdown-item" @click="dropdownSelect('today')"  v-if="$store.state.user_data.pageType != 'taipower'">{{$t('本日')}}</a></li>
                    <li><a class="dropdown-item" @click="dropdownSelect('week')">{{$t('本週')}}</a></li>
                    <li><a class="dropdown-item" @click="dropdownSelect('month')">{{$t('本月')}}</a></li>
                    <li><a class="dropdown-item" @click="dropdownSelect('year')">{{$t('本年')}}</a></li>
                </ul>
            </div>
        </div>
        <!-- Interval Selection On Desktop -->
        <div class="row g-0 mt-2 me-2 mb-2 d-none d-lg-flex">
            <button type="button" class="btn btn-primary btn-sm col-12 col-sm-9 col-md-6 col-lg-3 col-xl-1"
                @click="selectAll"
                :class="{ active: mode=='all'}"
            >
                {{$t('全部')}}
            </button>
            <button type="button" class="btn btn-primary btn-sm col-12 col-sm-9 col-md-6 col-lg-3 col-xl-1 ms-lg-2"
                @click="selectToday"
                :class="{ active: mode=='today'}"
                v-if="$store.state.user_data.pageType != 'taipower'"
            >
                {{$t('本日')}}
            </button>
            <button type="button" class="btn btn-primary btn-sm col-12 col-sm-9 col-md-6 col-lg-3 col-xl-1 ms-lg-2"
                @click="selectThisWeek"
                :class="{ active: mode=='week'}"
            >
                {{$t('本週')}}
            </button>
            <button type="button" class="btn btn-primary btn-sm col-12 col-sm-9 col-md-6 col-lg-3 col-xl-1 ms-lg-2"
                @click="selectThisMonth"
                :class="{ active: mode=='month'}"
            >
                {{$t('本月')}}
            </button>
            <button type="button" class="btn btn-primary btn-sm col-12 col-sm-9 col-md-6 col-lg-3 col-xl-1 ms-lg-2"
                @click="selectThisYear"
                :class="{ active: mode=='year'}"
            >
                {{$t('本年')}}
            </button>
        </div>
        <div class="row g-0 me-2">
            <button type="button" class="btn btn-primary btn-sm col-12 col-sm-9 col-md-6 col-lg-3 col-xl-1 auto_date_range mt-2"
                @click="setRangeType($event)"
                :class="{ active: mode=='single' }"
            >
                {{$t('單日')}}
            </button>
            <button type="button" class="btn btn-primary btn-sm col-12 col-sm-9 col-md-6 col-lg-3 col-xl-1 manual_date_range mt-2 ms-lg-2"
                @click="setRangeType($event)"
                :class="{ active: !singleDateRange }"
            >
                {{$t('區間')}}
            </button>
        </div>
        <div class="row g-0 me-2 mb-2">
            <div class="col-12 col-md-6 col-lg-4 col-xl-3 col-xxl-2 text-center mt-2">
                <!-- 起始時間 -->
                <el-date-picker
                    v-model="startDate"
                    placeholder="開始日期"
                    type="date"
                    class="w-100"
                    :disabled="mode != 'single' && mode != 'interval'"
                    size="large"
                ></el-date-picker>
            </div>
            <div class="col-12 col-md-6 col-lg-auto d-flex  align-items-center ms-2 mt-2">
                <el-button
                    class="btn_start_date_last_month"
                    @click="selectDateRange($event)"
                    size="large"
                    :disabled="mode != 'single' && mode != 'interval'"
                    v-if="$store.state.user_data.pageType != 'taipower'"
                >
                    <i class="btn_start_date_last_month el-icon-caret-left"></i>
                </el-button>
                <el-button
                    class="btn_start_date_yday"
                    @click="selectDateRange($event)"
                    size="large"
                    :disabled="mode != 'single' && mode != 'interval'"
                    v-if="$store.state.user_data.pageType != 'taipower'"
                >
                    <i class="btn_start_date_yday el-icon-caret-left"></i>
                </el-button>
                <el-button
                    class="btn_start_date_tmr"
                    @click="selectDateRange($event)"
                    size="large"
                    :disabled="mode != 'single' && mode != 'interval'"
                    v-if="$store.state.user_data.pageType != 'taipower'"
                >
                    <i class="btn_start_date_tmr el-icon-caret-right"></i>
                </el-button>
                <el-button
                    class="btn_start_date_next_month"
                    @click="selectDateRange($event)"
                    size="large"
                    :disabled="mode != 'single' && mode != 'interval'"
                    v-if="$store.state.user_data.pageType != 'taipower'"
                >
                    <i class="btn_start_date_next_month el-icon-caret-right"></i>
                </el-button>
                <label class="ms-2 me-2 fs-5">~</label>
            </div>
            <div class="col-12 col-md-6 col-lg-4 col-xl-3 col-xxl-2 text-center mt-2">
                <!-- 結束時間 -->
                <el-date-picker
                    v-model="endDate"
                    type="date"
                    placeholder="結束日期"
                    class="w-100"
                    :disabled="singleDateRange"
                    size="large"
                ></el-date-picker>
            </div>
            <div class="col-12 col-md-6 col-lg-5 col-xl-4 col-xxl-3 d-flex  align-items-center ms-2 mt-2" v-if="$store.state.user_data.pageType != 'taipower'">
                <el-button
                    class="btn_end_date_last_month"
                    @click="selectDateRange($event)"
                    size="large"
                    :disabled="singleDateRange"
                >
                    <i class="btn_end_date_last_month el-icon-caret-left"></i>
                </el-button>
                <el-button
                    class="btn_end_date_yday"
                    @click="selectDateRange($event)"
                    size="large"
                    :disabled="singleDateRange"
                >
                    <i class="btn_end_date_yday el-icon-caret-left"></i>
                </el-button>
                <el-button
                    class="btn_end_date_tmr"
                    @click="selectDateRange($event)"
                    size="large"
                    :disabled="singleDateRange"
                >
                    <i class="btn_end_date_tm el-icon-caret-right"></i>
                </el-button>
                <el-button
                    class="btn_end_date_next_month"
                    @click="selectDateRange($event)"
                    size="large"
                    :disabled="singleDateRange"
                >
                    <i class="btn_end_date_next_month el-icon-caret-right"></i>
                </el-button>
            </div>
            <div class="col-12 col-md-auto d-flex justify-content-center align-items-end ms-md-2 mt-2 mt-lg-0">
                <el-button size="large"
                    class="col-12 col-md-auto"
                    @click="searchDateRange(dateRange)"
                    :disabled="mode != 'single' && mode != 'interval'"
                >
                    <i class="el-icon-search"></i>
                </el-button>
            </div>
        </div>
    </div>
</template>

<script>
import {Dropdown} from 'bootstrap'

export default {
    name: "dateMonthPicker",
    props:{
        initial_mode:{type: String, default: "all"}
    },
    emits: ['setDate'],
    data() {
        return {
            singleDateRange: true,
            mode: this.initial_mode,    //會有 today week month year single interval
            date: "",
            startDate: "",
            endDate: "",
            dateRange: [null, null],
            dropdown_text: this.$i18n.t('全部'),
        };
    },
    mounted(){
        this.searchDateRange()
    },
    created() {
        this.date = new Date();
        this.startDate = new Date();
        this.endDate = new Date();
    },
    methods: {
        // 選取時間範圍類型：單間 or {{$t('區間')}}
        setRangeType(e) {
            const clsList = e.target.classList;
            if (clsList.contains("auto_date_range")) {
                this.singleDateRange = true;
                this.mode = 'single'
            } else if (clsList.contains("manual_date_range")) {
                this.singleDateRange = false;
                this.mode = 'interval'
            } else {
                console.log("請重新選擇");
            }
        },
        // {{$t('區間')}}選取功能
        selectDateRange(e) {
            const classList = e.target.classList;
            switch (true) {
                case classList.contains("btn_start_date_last_month"):
                    this.startDate = this.selectLastMonth(this.startDate);
                    break;
                case classList.contains("btn_start_date_next_month"):
                    this.startDate = this.selectNextMonth(this.startDate);
                    break;
                case classList.contains("btn_start_date_yday"):
                    this.startDate = this.selectLastDay(this.startDate);
                    break;
                case classList.contains("btn_start_date_tmr"):
                    this.startDate = this.selectNextDay(this.startDate);
                    break;
                case classList.contains("btn_end_date_last_month"):
                    this.endDate = this.selectLastMonth(this.endDate);
                    break;
                case classList.contains("btn_end_date_next_month"):
                    this.endDate = this.selectNextMonth(this.endDate);
                    break;
                case classList.contains("btn_end_date_yday"):
                    this.endDate = this.selectLastDay(this.endDate);
                    break;
                case classList.contains("btn_end_date_tmr"):
                    this.endDate = this.selectNextDay(this.endDate);
                    break;
                default:
                    console.log("請重新選擇");
            }
        },
        selectLastMonth(newDate) {
            newDate = newDate.getTime() - 3600 * 1000 * 24 * 30;
            newDate = new Date(newDate);
            return newDate;
        },
        selectNextMonth(newDate) {
            newDate = newDate.getTime() + 3600 * 1000 * 24 * 30;
            newDate = new Date(newDate);
            return newDate;
        },
        selectLastDay(newDate) {
            newDate = newDate.getTime() - 3600 * 1000 * 24;
            newDate = new Date(newDate);
            return newDate;
        },
        selectNextDay(newDate) {
            newDate = newDate.getTime() + 3600 * 1000 * 24;
            newDate = new Date(newDate);
            return newDate;
        },
        // 單間選取
        selectAll() {
            console.log("選擇從古至今");
            this.singleDateRange = true;
            this.mode = 'all'
            this.searchDateRange()

        },
        selectToday() {
            console.log("選擇今日");
            this.singleDateRange = true;
            this.mode = 'today'
            this.searchDateRange()

        },
        selectThisWeek() {
            console.log("選擇{{$t('本週')}}");
            this.singleDateRange = true;
            this.mode = 'week'
            this.searchDateRange()

        },
        selectThisMonth() {
            console.log("選擇{{$t('本月')}}");
            this.singleDateRange = true;
            this.mode = 'month'
            this.searchDateRange()

        },
        selectThisYear() {
            console.log("選擇{{$t('本年')}}");
            this.singleDateRange = true;
            this.mode = 'year'
            this.searchDateRange()

        },
        dropdownSelect(mode) {
            this.singleDateRange = true;
            switch(mode){
                case 'all':
                    this.mode = 'all'
                    this.dropdown_text = this.$i18n.t('全部')
                    break
                case 'today':
                    this.mode = 'today'
                    this.dropdown_text = this.$i18n.t('本日')
                    break
                case 'week':
                    this.mode = 'week'
                    this.dropdown_text = this.$i18n.t('本週')
                    break
                case 'month':
                    this.mode = 'month'
                    this.dropdown_text = this.$i18n.t('本月')
                    break
                case 'year':
                    this.mode = 'year'
                    this.dropdown_text = this.$i18n.t('本年')
                    break
            }
            const dropdown = new Dropdown(document.getElementById("interval_dropdown"))
            dropdown.hide()
            this.searchDateRange()
        },
        // 送出查詢
        searchDateRange() {
            this.dateRange = [this.startDate, this.endDate];
            const offset = this.dateRange[0].getTimezoneOffset()
            let start_date = new Date(this.dateRange[0].getTime()-(offset*60*1000))
            start_date = start_date.toISOString().split('T')[0]
            let end_date = new Date(this.dateRange[1].getTime()-(offset*60*1000))
            end_date = end_date.toISOString().split('T')[0]
            this.$emit('setDate', {date_list: [start_date, end_date], mode: this.mode});   //傳遞已選擇的ID到外層
        },
    },
};
</script>
