<template>
  <div class="col-12 col-lg-12 responsive_table">
    <div style="overflow-y:scroll">
      <div
        class="w-100 row responsive_table_header fw-bold m-0 d-none d-lg-flex flex-nowrap"
      >
        <div class="col-2 text-center">
          <label class="fs-6">{{$t('setting.iec61850.設備名稱')}}</label>
        </div>
        <div class="col-2 text-center">
          <label class="fs-6">{{$t('setting.iec61850.設備型號')}}</label>
        </div>
        <div class="col-2 text-center">
          <label class="fs-6">{{$t('setting.iec61850.指令地址')}}</label>
        </div>
        <div class="col-2 text-center">
          <label class="fs-6">{{$t('setting.iec61850.目標數值')}}</label>
        </div>
        <div class="col-2 text-center">
          <label class="fs-6">{{$t('setting.iec61850.執行時間')}}</label>
        </div>
        <div class="col-2 text-center">
          <label class="fs-6">{{$t('setting.iec61850.執行指令')}}</label>
        </div>
      </div>
      <div v-loading="this.loading">
        <div class="w-100 pt-2 pb-2 text-center" v-if="tableData.length == 0">
          {{$t('setting.iec61850.無資料')}}
        </div>
        <div class="w-100 responsive_table_body">
          <div
            class="row m-0 responsive_table_content mt-2 mt-lg-0 pt-2 pb-3 p-lg-0"
            v-for="(data, index) in tableData"
            :key="data._id"
          >
            <div class="col-12 col-lg-2 pt-lg-4 pb-lg-4">
              <div class="d-flex d-lg-none">
                <label class="fs-6 fw-bold">{{$t('setting.iec61850.設備名稱')}}:</label>
                <label class="fs-6">{{ data.label }}</label>
              </div>
              <label class="fs-6 w-100 text-center d-none d-lg-block">{{
                data.label
              }}</label>
            </div>

            <div class="col-12 col-lg-2 pt-lg-4 pb-lg-4">
              <div class="d-flex d-lg-none">
                <label class="fs-6 fw-bold">{{$t('setting.iec61850.設備型號')}}:</label>
                <label class="fs-6">{{ data.model }}</label>
              </div>
              <label class="fs-6 w-100 text-center d-none d-lg-block">{{
                data.model
              }}</label>
            </div>

            <div class="col-12 col-lg-2 pt-lg-4 pb-lg-4">
              <label class="fs-6 fw-bold d-lg-none">{{$t('setting.iec61850.指令地址')}}:</label>
              <div
                class="d-flex w-100 algin-items-center justify-content-start justify-content-lg-center"
              >
                <el-select
                  v-model="data.address"
                  size="large"
                  @change="$emit('update_command', data._id, data.address)"
                >
                  <el-option
                    v-for="item in commandList[data.model]"
                    :key="item.address"
                    :value="item.address"
                    :label="item.address + ' ' + item.command"
                  />
                </el-select>
              </div>
            </div>

            <div class="col-12 col-lg-2 pt-lg-4 pb-lg-4">
              <label class="fs-6 fw-bold d-lg-none">{{$t('setting.iec61850.目標數值')}}:</label>
              <div
                class="d-flex w-100 algin-items-center justify-content-start justify-content-lg-center"
              >
                <el-input
                  v-model="data.values"
                  :placeholder="getRange(data.model, data.address)"
                  :disabled="data.address === null"
                />
              </div>
            </div>

            <div class="col-12 col-lg-2 pt-lg-4 pb-lg-4">
              <label class="fs-6 fw-bold d-lg-none">{{$t('setting.iec61850.執行時間')}}:</label>
              <div
                class="d-flex w-100 algin-items-center justify-content-start justify-content-lg-center"
              >
                <el-date-picker
                  :placeholder="$t('setting.iec61850.請選擇執行時間')"
                  type="datetime"
                  class="w-100"
                  v-model="data.start"
                  :disabledDate="disabledDate"
                >
                </el-date-picker>
              </div>
            </div>

            <div class="col-12 col-lg-2 pt-lg-4 pb-lg-4">
              <label class="fs-6 fw-bold d-lg-none">{{$t('setting.iec61850.執行指令')}}:</label>
              <div
                class="d-flex justify-content-center align-items-center w-100"
              >
                <button
                  class="btn btn-success ms-lg-2 mt-2 col-lg-auto col-12"
                  @click="sendCommand(data, index)"
                >
                  {{$t('setting.iec61850.送出')}}
                </button>
              </div>
              <div
                class="d-flex justify-content-center align-items-center w-100"
              >
                <button
                  class="btn btn-success ms-lg-2 mt-2 col-lg-auto col-12"
                  @click="resetCommand(data, index)"
                >
                  {{$t('setting.iec61850.重置')}}
                </button>
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
  name: "informationTable",
  emits: ["update_command"],
  props: {
    tableData: {
      type: Array,
      required: false,
      default() {
        return [];
      },
    },
    commandList: {
      type: Object,
      required: true,
      default() {
        return {};
      },
    },
    loading: {
      type: Boolean,
      required: true,
      default() {
        return false;
      },
    },
  },
  data() {
    return {};
  },
  methods: {
    getRange(model, address) {
      if (address === null) {
        return this.$i18n.t('setting.iec61850.請選擇指令地址');
      }
      let addressList = this.commandList[model];
      for (var data in addressList) {
        if (addressList[data].address === address) {
          return (
            addressList[data].min +
            "~" +
            addressList[data].max +
            " ( " +
            addressList[data].unit +
            " )"
          );
        }
      }
      return this.$i18n.t('setting.iec61850.無資料');
    },
    getMultiplier(data, index) {
      for (var i = 0; i < this.commandList[data.model].length; i++) {
        if (this.commandList[data.model][i].address === data.address) {
          return this.commandList[data.model][i].multiplier;
        }
      }
    },
    disabledDate(date) {
      return date < Date.now();
    },
    getTime() {
      var now = new Date();
      now.getSeconds() < 30 ? now.setSeconds(0) : now.setSeconds(30);
      return now;
    },
    checkValue(data, index) {
      if (isNaN(data.values)) return false;
      let value = parseFloat(data.values);
      console.log(value);
      let values = this.commandList[data.model][index];
      let min = values.min;
      let max = values.max;
      return value >= min && value <= max;
    },
    checkInput(data, index) {
      let address = data.address;
      let start = data.start;
      let value = data.values;
      if (address === null || start === null || value === null) {
        return false;
      }
      if (address === undefined || start === undefined || value === undefined) {
        return false;
      }
      return true;
    },
    checkTime(data, index) {
      console.log(
        data.start.getTime(),
        new Date().getTime() + 30000,
        data.start.getTime() - (new Date().getTime() + 30000)
      );
      console.log(data.start.getTime() < new Date().getTime() + 30000);
      return data.start.getTime() < new Date().getTime() + 30000;
    },
    resetCommand(data, index) {
      for (var i = 0; i < this.commandList[data.model].length; i++) {
        if (this.commandList[data.model][i].address === data.address) {
          data.values = this.commandList[data.model][i].default;
          data.start = new Date(new Date().getTime() + 60000);
          console.log(data.start);
          break;
        }
      }
    },
    sendCommand(data, index) {
      if (!this.checkInput(data, index)) {
        window.alert(this.$i18n.t('setting.iec61850.請填入完整資料'));
        return;
      } else if (!this.checkValue(data, index)) {
        window.alert(this.$i18n.t('setting.iec61850.請輸入正確的數值'));
        return;
      }
      // else if (!this.checkTime(data, index)) {
      //   window.alert("請確認時間");
      //   return;
      // }
      let value = parseFloat(this.tableData[index].values);
      let key = this.tableData[index].ID;
      var equipment = {};
      equipment[key] = false;
      console.log(data);
      let sendObject = {
        equipment: equipment,
        time: parseInt(this.getTime().getTime()),
        address: data.address,
        value: value,
        start: parseInt(data.start.getTime()),
        status: false,
        parity: 1,
        mac: data.mac,
        multiplier: this.getMultiplier(data, index),
      };
      console.log(sendObject);
      // sendCommand
      this.axios
        .post("/setting/send_IEC61850_command", sendObject)
        .then((res) => {
          console.log(res);
          if (res.status === 200) {
            window.alert(this.$i18n.t('setting.iec61850.指令發送成功'));
          } else {
            window.alert(this.$i18n.t('setting.iec61850.指令發送失敗'));
          }
        })
        .catch((err) => {
          console.log(err);
        });
      // reset
      data.address = null;
      data.start = null;
      data.values = null;
    },
  },
};
</script>
