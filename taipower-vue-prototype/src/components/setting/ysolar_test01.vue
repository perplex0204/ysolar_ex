<template>
	<div class="card p-4">
		<div class="d-flex flex-wrap mt-2 align-items-center">
			<button @click="show_plot" type="button" class="btn btn-primary mt-2 ms-lg-2 btn-sm col-12 col-sm-12 col-md-6 col-lg-3 col-xl-1">test</button>
		</div>
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
export default {
    name: "ysolarTest",
	components: {
	},
	data() {
		return {
			plot_name: "",
			screenWidth: document.body.clientWidth,
		};
	},
	mounted() {
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
				.post("/setting/ysolar_test", {
				})
				.then((data) => {
					var plot_data = data.data.data.data.data;
					var plot_time = plot_data["time"]
					// print去除時間的資料(rate)
					that.plot_forecasting(plot_time,plot_data)
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
        background-color: #fff;
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
    