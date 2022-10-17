<template>
    <div>
        <div class="esdate_month_pick row g-0">
            <div class="col-12 col-md-12 col-lg-5 text-center me-0 me-lg-3 mt-2">
                <el-date-picker
                    v-model="date"
                    :type="parentPickerType"
                    placeholder="選擇日期"
                    :disabled="parentIsDisabled"
                    :clearable="false"
                    @change="emit_date"
                    size="large"
                    class="w-100"
                ></el-date-picker>
            </div>
            <div class="col-12 col-md-12 col-lg-5 d-flex  align-items-center mt-2"  v-if="$store.state.user_data.pageType != 'taipower'">
                <el-button
                    class="btn_start_date_last_month"
                    @click="selectDateRange('btn_start_date_last_month')"
                    size="large"
                >
                    <i class="el-icon-caret-left"></i>
                </el-button>
                <el-button
                    class="btn_start_date_yday"
                    @click="selectDateRange('btn_start_date_yday')"
                    size="large"
                >
                    <i class="el-icon-caret-left"></i>
                </el-button>
                <el-button
                    class="btn_start_date_tmr"
                    @click="selectDateRange('btn_start_date_tmr')"
                    size="large"
                >
                    <i class="el-icon-caret-right"></i>
                </el-button>
                <el-button
                    class="btn_start_date_next_month"
                    @click="selectDateRange('btn_start_date_next_month')"
                    size="large"
                >
                    <i class="el-icon-caret-right"></i>
                </el-button>
            </div>
        </div>
    </div>
</template>

<script>
export default {
    name: "monthPicker",
    props: {
        parentIsDisabled: {
            type: Boolean,
            required: false,
        },
        parentPickerType: {
            type: String,
            default:'date'
        },
        parentDate: {
            default: new Date()
        }
    },
    data(){
        return {
            date: new Date(),
        }
    },
    mounted(){
        this.emit_date()
    },
    methods: {
        selectDateRange(e) {
            switch (e) {
                case "btn_start_date_last_month":
                    this.date = this.selectLastMonth(this.date);
                    break;
                case "btn_start_date_next_month":
                    this.date = this.selectNextMonth(this.date);
                    break;
                case "btn_start_date_yday":
                    this.date = this.selectLastDay(this.date);
                    break;
                case "btn_start_date_tmr":
                    this.date = this.selectNextDay(this.date);
                    break;
                default:
                    console.log("請重新選擇");
            }
            this.emit_date()
        },
        selectLastMonth(newDate) {
            if(this.parentPickerType == 'month')
                newDate = newDate.getTime() - 3600 * 1000 * 24 * 30 * 12;
            else
                newDate = newDate.getTime() - 3600 * 1000 * 24 * 30;
            newDate = new Date(newDate);
            return newDate;
        },
        selectNextMonth(newDate) {
            if(this.parentPickerType == 'month')
                newDate = newDate.getTime() + 3600 * 1000 * 24 * 30 * 12;
            else
                newDate = newDate.getTime() + 3600 * 1000 * 24 * 30;
            newDate = new Date(newDate);
            return newDate;
        },
        selectLastDay(newDate) {
            if(this.parentPickerType == 'month')
                 newDate = newDate.getTime() - 3600 * 1000 * 24 * 30;
            else
                newDate = newDate.getTime() - 3600 * 1000 * 24;
            newDate = new Date(newDate);
            return newDate;
        },
        selectNextDay(newDate) {
            if(this.parentPickerType == 'month')
                newDate = newDate.getTime() + 3600 * 1000 * 24 * 30;
            else
                newDate = newDate.getTime() + 3600 * 1000 * 24;
            newDate = new Date(newDate);
            return newDate;
        },
        emit_date(){
            const offset = this.date.getTimezoneOffset()
            let sel_date = new Date(this.date.getTime()-(offset*60*1000))
            sel_date = sel_date.toISOString().split('T')[0]
            this.$emit("set-date", sel_date);   //傳遞已選擇的ID到外層
        }
    },
    watch: {
        parentDate(){
            this.date  = this.parentDate
        }
    }
};
</script>