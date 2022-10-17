<template>
    <div>
        <div class="row g-0 mt-2 me-2" v-if="$store.state.user_data.pageType != 'taipower'">
            <button type="button" class="btn btn-primary btn-sm col-12 col-sm-9 col-md-6 col-lg-3 col-xl-1"
                @click="selectToday"
                :class="{ active: mode=='today'}"
            >
                {{$t('本日')}}
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
        <div class="row g-0" :class="{'me-2': $store.state.user_data.pageType != 'taipower', 'me-0': $store.state.user_data.pageType == 'taipower'}">
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
            <div class="col-12 col-md-6 col-lg-5 col-xl-auto d-flex  align-items-center ms-md-2 mt-2
            justify-content-between" v-if="$store.state.user_data.pageType != 'taipower'">
                <el-button
                    class="btn_start_date_last_month"
                    @click="selectDateRange($event)"
                    size="large"
                    :disabled="mode != 'single' && mode != 'interval'"
                >
                    <i class="btn_start_date_last_month el-icon-caret-left"></i>
                </el-button>
                <el-button
                    class="btn_start_date_yday"
                    @click="selectDateRange($event)"
                    size="large"
                    :disabled="mode != 'single' && mode != 'interval'"
                >
                    <i class="btn_start_date_yday el-icon-caret-left"></i>
                </el-button>
                <el-button
                    class="btn_start_date_tmr"
                    @click="selectDateRange($event)"
                    size="large"
                    :disabled="mode != 'single' && mode != 'interval'"
                >
                    <i class="btn_start_date_tmr el-icon-caret-right"></i>
                </el-button>
                <el-button
                    class="btn_start_date_next_month"
                    @click="selectDateRange($event)"
                    size="large"
                    :disabled="mode != 'single' && mode != 'interval'"
                >
                    <i class="btn_start_date_next_month el-icon-caret-right"></i>
                </el-button>
            </div>
            <div class="col-12 col-md-auto d-flex justify-content-center align-items-end">
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
            <div class="col-12 col-md-6 col-lg-5 col-xl-auto d-flex  align-items-center ms-md-2 mt-2
            justify-content-between" v-if="$store.state.user_data.pageType != 'taipower'">
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
            <div class="col-12 col-md-auto d-flex justify-content-center align-items-end ms-md-2 mt-2">
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
export default {
    name: "dateMonthPicker",
    data() {
        return {
            singleDateRange: true,
            mode: this.$store.state.user_data.pageType == 'taipower' ? 'single' : 'today',    //會有 today single interval
            date: "",
            startDate: "",
            endDate: "",
            dateRange: [null, null],
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
            console.log(e)
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
        selectToday() {
            console.log("選擇今日");
            this.singleDateRange = true;
            this.mode = 'today'
            this.searchDateRange()

        },
        // 送出查詢
        searchDateRange() {
            this.dateRange = [this.startDate, this.endDate];
            const offset = this.dateRange[0].getTimezoneOffset()
            let start_date = ""
            if(this.mode == 'today'){
                let today = new Date()
                start_date = new Date(today.getTime()-(offset*60*1000))
                start_date = start_date.toISOString().split('T')[0]
            }
            else{
                start_date = new Date(this.dateRange[0].getTime()-(offset*60*1000))
                start_date = start_date.toISOString().split('T')[0]
            }
            let end_date = ""
            if(this.mode == 'single' || this.mode == 'today'){
                end_date = start_date
            }else{
                end_date = new Date(this.dateRange[1].getTime()-(offset*60*1000))
                end_date = end_date.toISOString().split('T')[0]
            } 
            console.log(start_date, end_date)
            //方便history_data_list api today會在這邊換成等效<<{{$t('單日')}}，日期今天這樣>>
            this.$emit('setDate', {date_list: [start_date, end_date], mode: this.mode == 'today'? 'single':this.mode, mode2: this.mode});   //傳遞已選擇的ID到外層
        },
    },
};
</script>
