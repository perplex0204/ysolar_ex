<template>
	<div class="card p-4">
		<h5>
			<i
				class="fa-solid fa-screwdriver-wrench text-primary me-2"></i>{{ $t("setting.data_integrity.data_integrity_setup") }}
		</h5>
		<div class="d-flex flex-wrap mt-2 align-items-center">
			<auto-complete @station-select="station_select"></auto-complete>
		</div>
		<div class="d-flex flex-wrap mt-2 align-items-center">
			<!-- <el-select v-model="type" placeholder="請選擇設備種類">
			<el-option
				v-for="item in typeSelect"
				:key="item.value"
				:label="item.label"
				:value="item.value">
			</el-option>
			</el-select> -->
			<input class="me-2" type="checkbox" id="plant" value="plant" v-model="type_checked" />
			<label class="me-4" for="plant">plant</label>
			<input class="me-2" type="checkbox" id="lgroup" value="lgroup" v-model="type_checked" />
			<label class="me-3" for="lgroup">lgroup</label>
			<input class="me-2" type="checkbox" id="group" value="group" v-model="type_checked" />
			<label class="me-2" for="group">group</label>
		</div>
		<div class="d-flex flex-wrap mt-2 align-items-center">
			<input class="me-2" type="checkbox" id="inverter" value="inverter" v-model="type_checked" />
			<label class="me-2" for="inverter">inverter</label>
			<input class="me-2" type="checkbox" id="sensor" value="sensor" v-model="type_checked" />
			<label class="me-2" for="sensor">sensor</label>
			<input class="me-2" type="checkbox" id="meter" value="meter" v-model="type_checked" />
			<label class="me-2" for="meter">meter</label>
		</div>
		<div>
			<time-range-picker-simple v-if="this.name !== ''" @setDate="setDate" />
		</div>
		<div v-if="this.name !== ''" class="d-flex flex-wrap mt-2 align-items-center">
			<el-select v-model="start_time" placeholder="請選擇開始時間">
				<el-option v-for="item in startTimeSelect" :key="item.value" :label="item.label" :value="item.value">
				</el-option>
			</el-select>
			<el-select class="ms-lg-2" v-model="end_time" placeholder="請選擇結束時間">
				<el-option v-for="item in endTimeSelect" :key="item.value" :label="item.label" :value="item.value">
				</el-option>
			</el-select>
		</div>
		<div class="d-flex flex-wrap mt-2 align-items-center">
			<button :disabled="this.start_time == '' || this.end_time == ''" @click="fake_data_integrity" type="button"
				class="btn btn-primary mt-2 btn-sm col-12 col-sm-12 col-md-6 col-lg-3 col-xl-1
        ">
				{{ $t("setting.data_integrity.fake_data_integrity") }}
			</button>
			<button :disabled="this.start_time == '' || this.end_time == ''" @click="pr_calculate" type="button" class=" btn btn-primary mt-2 ms-lg-2 btn-sm col-12 col-sm-12 col-md-6 col-lg-3 col-xl-1
        ">
				{{ $t("setting.data_integrity.pr_calculate") }}
			</button>
		</div>
		<div class="modal" tabindex="-1" ref="change_username_password_modal">
			<div class="modal-dialog modal-dialog-centered">
				<div class="modal-content">
					<div class="modal-header">
						<h5 class="modal-title">
							{{ $t("setting.users.update_username_password") }}
						</h5>
						<button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
					</div>
					<div class="modal-body">
						<label class="col-4 mt-4 text-lg-center">{{ $t("setting.users.password_valid")
						}}</label>
						<div class="col-8 mt-4">
							<el-input v-model="password" type="password" />
						</div>
					</div>
					<div class="modal-footer">
						<button type="button" class="btn btn-success" @click="handleConfirm">
							{{ $t("setting.data_integrity.confirm") }}
						</button>
					</div>
				</div>
			</div>
		</div>
		<!-- 分隔線 -->
		<el-divider class="mt-4 mb-4" />
		<h5 class="mt-2">
			<i
				class="fa-solid fa-screwdriver-wrench text-primary me-2"></i>{{ $t("setting.data_integrity.data_integrity_chart") }}
		</h5>
		<!-- 資料完整度圖表 -->
		<div v-loading="this.loading">
			<!-- stbigimg shadow不知道是啥 -->
			<div class="w-100">
				<div class="stbigimg shadow">
					<div id="plot_div"></div>
				</div>
			</div>
		</div>
	</div>
</template>

<script>
import AutoComplete from "../autocomplete/all_type.vue";
import TimeRangePickerSimple from "@/components/datepicker/timeRangePickerSimple.vue";
import { Modal } from "bootstrap";

export default {
	name: "dataIntegrity",
	components: {
		AutoComplete,
		TimeRangePickerSimple,
	},
	data() {
		return {
			plot_name: "",
			screenWidth: document.body.clientWidth,
			type_checked: [],
			ID: null,
			collection: null,
			name: "",
			loading: false,
			startTimeSelect: [
				{
					value: "0",
					label: "00:00",
				},
				{
					value: "1",
					label: "01:00",
				},
				{
					value: "2",
					label: "02:00",
				},
				{
					value: "3",
					label: "03:00",
				},
				{
					value: "4",
					label: "04:00",
				},
				{
					value: "5",
					label: "05:00",
				},
				{
					value: "6",
					label: "06:00",
				},
				{
					value: "7",
					label: "07:00",
				},
				{
					value: "8",
					label: "08:00",
				},
				{
					value: "9",
					label: "09:00",
				},
				{
					value: "10",
					label: "10:00",
				},
				{
					value: "11",
					label: "11:00",
				},
				{
					value: "12",
					label: "12:00",
				},
				{
					value: "13",
					label: "13:00",
				},
				{
					value: "14",
					label: "14:00",
				},
				{
					value: "15",
					label: "15:00",
				},
				{
					value: "16",
					label: "16:00",
				},
				{
					value: "17",
					label: "17:00",
				},
				{
					value: "18",
					label: "18:00",
				},
				{
					value: "19",
					label: "19:00",
				},
				{
					value: "20",
					label: "20:00",
				},
				{
					value: "21",
					label: "21:00",
				},
				{
					value: "22",
					label: "22:00",
				},
				{
					value: "23",
					label: "23:00",
				},
			],
			endTimeSelect: [
				{
					value: "0",
					label: "00:00",
				},
				{
					value: "1",
					label: "01:00",
				},
				{
					value: "2",
					label: "02:00",
				},
				{
					value: "3",
					label: "03:00",
				},
				{
					value: "4",
					label: "04:00",
				},
				{
					value: "5",
					label: "05:00",
				},
				{
					value: "6",
					label: "06:00",
				},
				{
					value: "7",
					label: "07:00",
				},
				{
					value: "8",
					label: "08:00",
				},
				{
					value: "9",
					label: "09:00",
				},
				{
					value: "10",
					label: "10:00",
				},
				{
					value: "11",
					label: "11:00",
				},
				{
					value: "12",
					label: "12:00",
				},
				{
					value: "13",
					label: "13:00",
				},
				{
					value: "14",
					label: "14:00",
				},
				{
					value: "15",
					label: "15:00",
				},
				{
					value: "16",
					label: "16:00",
				},
				{
					value: "17",
					label: "17:00",
				},
				{
					value: "18",
					label: "18:00",
				},
				{
					value: "19",
					label: "19:00",
				},
				{
					value: "20",
					label: "20:00",
				},
				{
					value: "21",
					label: "21:00",
				},
				{
					value: "22",
					label: "22:00",
				},
				{
					value: "23",
					label: "23:00",
				},
			],
			password: "",
			start_date: "",
			end_date: "",
			start_time: "",
			end_time: "",
			is_fake_or_pr: "",
		};
	},
	mounted() {
		this.change_username_password_modal = new Modal(
			this.$refs.change_username_password_modal
		);
		let that = this;
		window.addEventListener("resize", this.plot_resize);
		window.addEventListener("resize", function () {
			return (() => {
				that.screenWidth = this.document.body.clientWidth;
			})();
		});
		if (this.screenWidth >= 576) {
			this.csvsize = "large";
			console.log("resize large");
		} else {
			this.csvsize = "small";
			console.log("resize small");
		}
	},
	unmounted() {
		window.removeEventListener("resize", this.plot_resize);
	},
	methods: {
		// 圖表的函式
		show_plot() {
			let that = this;
			this.axios
				.post("get_data_integrity_data", {
					station: this.name,
					start_date: this.start_date,
					start_time: this.start_time,
					end_date: this.end_date,
					end_time: this.end_time,
					is_fake_or_pr: this.is_fake_or_pr,
					type_checked: this.type_checked,
					ID: this.ID,
				})
				.then((data) => {
					// print目前丟回來的資料
					// console.log(
					// 	"data.data.data.data.data : ",
					// 	data.data.data.data.data
					// );

					// 獲取data長度
					// const getLengthOfObject = (obj) => {
					// 	let lengthOfObject = Object.keys(obj).length;
					// 	console.log(lengthOfObject);
					// 	console.log(Object.keys(obj))
					// }

					// getLengthOfObject(data.data.data.data.data);
					// plot_data = 後端的output_data['data']內的內容，有三個標籤['output_kwh']、['real_kwh']、['time']
					var plot_data = data.data.data.data.data;
					var plot_time = plot_data["time"]
					delete plot_data.time
					// 如果有收到正確的資料(回傳資料長度>0)，則設定輸出的title名稱 = 案場名_開始時間_結束時間
					if (plot_time.length > 0) {
						this.plot_name =
							this.name +
							"_" +
							plot_time[0].split(" ")[0] +
							"_" +
							plot_time[
								plot_time.length - 1
							].split(" ")[0];
						console.log(that.name);
					}
					that.plot_forecasting(
						plot_time,
						plot_data
					);
					// print去除時間的資料(rate)
					console.log(plot_data)
				});
		},
		plot_forecasting(time, plot_data) {
			const MyPlot = document.getElementById("plot_div");
			MyPlot.innerHTML = "";
			// color如果沒有指定色碼的話就會直接隨機
			var color = [];
			var color_index = 0;
			var data = [];
			for (var equipment in plot_data) {
				console.log("name : ", equipment, " data :", plot_data[equipment])
				data.push({
					type: "scatter",
					mode: "lines",
					x: time,
					y: plot_data[equipment],
					// name: this.$i18n.t("plot.實際輸出功率"),
					name: equipment,
					yaxis: "y",
					line: {
						color: color[color_index],
						shape: "linear",
					},
					marker: {
						size: 8,
					},
				})
				color_index = color_index + 1;
			}
			// data.push({
			// 	type: "scatter",
			// 	mode: "lines",
			// 	x: time,
			// 	y: inverter1_data,
			// 	// name: this.$i18n.t("plot.實際輸出功率"),
			// 	name: "Inverter1",
			// 	yaxis: "y",
			// 	line: {
			// 		color: color[0],
			// 		shape: "linear",
			// 	},
			// 	marker: {
			// 		size: 8,
			// 	},
			// });
			// data.push({
			// 	type: "scatter",
			// 	mode: "lines",
			// 	x: time,
			// 	y: inverter2_data,
			// 	// name: this.$i18n.t("plot.實際輸出功率"),
			// 	name: "Inverter2",
			// 	yaxis: "y",
			// 	line: {
			// 		color: color[1],
			// 		shape: "linear",
			// 	},
			// 	marker: {
			// 		size: 8,
			// 	},
			// });
			// 設定輸出的樣式
			var layout = {
				// title = 上面的that.name
				title: {
					text: this.plot_name,
					font: {
						family: "Courier New, monospace",
						size: this.$store.state.isMobile ? 6 : 25,
					},
				},
				// x軸樣式
				xaxis: {
					// domain: [0.1, 0.94],
					// anchor: "free",
					// position: 0,
				},
				// y軸樣式
				yaxis: {
					title: {
						// text: this.$i18n.t("plot.功率") + "(kWh)",
						text: "Rate",
					},
				},
				// 大小
				margin: {
					l: 70,
					t: 50,
					pad: 10,
				},
				// 長寬
				width: document.getElementById("plot_div").clientWidth,
				height: document.getElementById("plot_div").clientHeight,
				// 手機板
				legend: {
					x: this.$store.state.isMobile ? 0 : 1,
					y: this.$store.state.isMobile ? -0.4 : 1,
				},
				// 不知道
				hovermode: "closest",
				// 顏色
				hoverlabel: {
					// 背景設為#ffffff(白)
					bgcolor: "#FFFFFF",
					// 格線顏色
					bordercolor: "#888888",
					// 字體顏色
					font: {
						color: "#000000",
					},
				},
			};
			// 繪圖的函數，輸入一：MyPlot(應該是要在哪裡繪圖)，輸入二：上面的兩個data.push，輸入三：上面設定的輸出樣式
			this.Plotly.newPlot(MyPlot, data, layout, {
				// 下面這兩個應該是類似參數設定，不太確定
				displaylogo: false,
				modeBarButtonsToRemove: [
					"sendDataToCloud",
					"hoverClosestCartesian",
					"hoverCompareCartesian",
					"toggleSpikelines",
				],
			});
		},
		plot_resize() {
			this.csvsize = "large";
			let update = {
				width: "",
				heigth: "",
			};
			update = {
				width: document.getElementById("plot_div").clientWidth,
				height: document.getElementById("plot_div").clientHeight,
				title: {
					text: this.name,
					font: {
						family: "Courier New, monospace",
						size: this.$store.state.isMobile ? 6 : 25,
					},
				},
				yaxis: {
					title: {
						// text: this.$i18n.t("plot.功率") + "(kWh)",
						text: 'rate'
					},
				},
				legend: {
					x: this.$store.state.isMobile ? 0 : 1,
					y: this.$store.state.isMobile ? -0.4 : 1,
				},
				margin: {
					l: 70,
					t: 50,
					pad: 10,
				},
			};
			let update_style = {
				name: [
					// this.$i18n.t("plot.實際輸出功率"),
					// this.$i18n.t("plot.預測輸出功率"),
				],
			};
			if (document.getElementById("plot_div").clientWidth < 576) {
				this.csvsize = "small";
			}
			try {
				this.Plotly.relayout("plot_div", update);
				// this.Plotly.restyle("plot_div", update_style);
			} catch {
				return false;
			}
		},
		// 按下確定鈕以後所觸發的函式，async、await：api收發
		async handleConfirm() {
			console.log(this.type_checked);

			const typeObj = {
				password: this.password,
				station: this.name,
				start_date: this.start_date,
				start_time: this.start_time,
				end_date: this.end_date,
				end_time: this.end_time,
				is_fake_or_pr: this.is_fake_or_pr,
				type_checked: this.type_checked,
			};
			await this.axios
				.post("/setting/fake_data_integrity", typeObj)
				.then((typeObj) => { })
				.catch((err) => {
					console.log(err);
				});
			console.log(
				this.start_date,
				this.end_date,
				this.type_checked,
				this.name
			);
			this.change_username_password_modal.hide();
		},
		station_select(item) {
			this.ID = item.ID;
			this.collection = item.collection;
			this.name = item.name;
		},
		setDate({ date_list }) {
			this.start_date = date_list[0];
			this.end_date = date_list[1];
			this.show_plot();
		},
		fake_data_integrity() {
			this.change_username_password_modal.show();
			this.is_fake_or_pr = "1";
		},
		pr_calculate() {
			this.change_username_password_modal.show();
			this.is_fake_or_pr = "0";
		},
	},
	watch: {
		// start_date() {
		// 	// place_select確實有收到資料(auto_complete有輸入內容)，則開始依日期區間做搜尋的動作
		// 	if (this.start_date == true) {
		// 		this.show_plot();
		// 	}
		// },
		// 更改大小則重新resize圖
		"$store.state.language": function () {
			this.plot_resize();
		},
		// 如果是手機板則重新resize圖
		"$store.state.navOpen": function () {
			if (!this.$store.state.isMobile) {
				this.plot_resize();
			}
		},
	},
};
</script>

<!-- 設定css的部分(樣式) -->
<style scoped>
#plot_div {
	position: relative;
	padding: 1rem;
	min-height: 500px;
	max-height: 550px;
	width: 95%;
	max-width: 95%;
}

.stbigimg {
	position: relative;
	width: 80vw;
	min-height: 65vh;
	border-radius: 1rem;
	box-shadow: 0 0 15px #dee4ea;
	overflow: hidden;
	background-color: #FFFFFF;
}

@media (max-width: 991px) {
	#plot_div {
		padding: 0rem;
		max-height: 600px;
		width: 100%;
		max-width: 100%;
	}

	.stbigimg {
		width: 100%;
	}
}
</style>
