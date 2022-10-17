<template>
	<div class="card p-4" id="card" v-loading="loading" element-loading-background="rgba(3, 19, 39, 0.8)">
		<div class="container-fluid">
			<div class="row">
				<div class="col-sm-6">
					<!-- 轉供現況 -->
					<div class="box" style="--c:#062d63;--w:10px;--b:3px">
						<div style="background-image: radial-gradient(rgb(12,47,90),rgb(3,19,39))">
							<div class="panel panel-primary">
								<div class="panel-heading"></div>
								<div class="panel-body">
									<div class="stbigimg shadow">
										<div id="plot_1"></div>
									</div>
								</div>
								<div class="panel-footer"></div>
							</div>
						</div>
					</div>
					<!-- 月分別電能轉供量、餘電量、憑證張數、二氧化碳減量 -->
				</div>
				<!--右邊欄位-->
				<div class="col-sm-6">
					<div class="box" style="--c:#062d63;--w:10px;--b:3px">
						<div style="background-image: radial-gradient(rgb(12,47,90),rgb(3,19,39))">
							<div class="panel panel-primary">
								<div class="panel-heading"></div>
								<div class="panel-body">
									<div class="stbigimg shadow">
										<div id="plot_2"></div>
									</div>
								</div>
								<div class="panel-footer"></div>
							</div>
						</div>
					</div>
				</div>
			</div>
			<el-divider class="divider" style="margin-top: 19px;margin-bottom: 19px;"></el-divider>
			<!-- 1~6月 -->
			<div class="row">
				<div class="col-2">
					<div class="box" style="--c:#062d63;--w:10px;--b:3px">
						<div style="background-image: radial-gradient(rgb(12,47,90),rgb(3,19,39))">
							<div class="panel panel-primary">
								<div class="panel-heading"></div>
								<div class="panel-body">
									<div class="stbigimg shadow">
										<div id="plot_month01"></div>
									</div>
								</div>
								<div class="panel-footer"></div>
							</div>
						</div>
					</div>
				</div>
				<div class="col-2">
					<div class="box" style="--c:#062d63;--w:10px;--b:3px">
						<div style="background-image: radial-gradient(rgb(12,47,90),rgb(3,19,39))">
							<div class="panel panel-primary">
								<div class="panel-heading"></div>
								<div class="panel-body">
									<div class="stbigimg shadow">
										<div id="plot_month02"></div>
									</div>
								</div>
								<div class="panel-footer"></div>
							</div>
						</div>
					</div>
				</div>
				<div class="col-2">
					<div class="box" style="--c:#062d63;--w:10px;--b:3px">
						<div style="background-image: radial-gradient(rgb(12,47,90),rgb(3,19,39))">
							<div class="panel panel-primary">
								<div class="panel-heading"></div>
								<div class="panel-body">
									<div class="stbigimg shadow">
										<div id="plot_month03"></div>
									</div>
								</div>
								<div class="panel-footer"></div>
							</div>
						</div>
					</div>
				</div>
				<div class="col-2">
					<div class="box" style="--c:#062d63;--w:10px;--b:3px">
						<div style="background-image: radial-gradient(rgb(12,47,90),rgb(3,19,39))">
							<div class="panel panel-primary">
								<div class="panel-heading"></div>
								<div class="panel-body">
									<div class="stbigimg shadow">
										<div id="plot_month04"></div>
									</div>
								</div>
								<div class="panel-footer"></div>
							</div>
						</div>
					</div>
				</div>
				<div class="col-2">
					<div class="box" style="--c:#062d63;--w:10px;--b:3px">
						<div style="background-image: radial-gradient(rgb(12,47,90),rgb(3,19,39))">
							<div class="panel panel-primary">
								<div class="panel-heading"></div>
								<div class="panel-body">
									<div class="stbigimg shadow">
										<div id="plot_month05"></div>
									</div>
								</div>
								<div class="panel-footer"></div>
							</div>
						</div>
					</div>
				</div>
				<div class="col-2">
					<div class="box" style="--c:#062d63;--w:10px;--b:3px">
						<div style="background-image: radial-gradient(rgb(12,47,90),rgb(3,19,39))">
							<div class="panel panel-primary">
								<div class="panel-heading"></div>
								<div class="panel-body">
									<div class="stbigimg shadow">
										<div id="plot_month06"></div>
									</div>
								</div>
								<div class="panel-footer"></div>
							</div>
						</div>
					</div>
				</div>
			</div>
			<!-- 7~12月 -->
			<el-divider class="divider" style="margin-top: 20px;margin-bottom: 19px;"></el-divider>
			<div class="row">
				<div class="col-2">
					<div class="box" style="--c:#062d63;--w:10px;--b:3px">
						<div style="background-image: radial-gradient(rgb(12,47,90),rgb(3,19,39))">
							<div class="panel panel-primary">
								<div class="panel-heading"></div>
								<div class="panel-body">
									<div class="stbigimg shadow">
										<div id="plot_month07"></div>
									</div>
								</div>
								<div class="panel-footer"></div>
							</div>
						</div>
					</div>
				</div>
				<div class="col-2">
					<div class="box" style="--c:#062d63;--w:10px;--b:3px">
						<div style="background-image: radial-gradient(rgb(12,47,90),rgb(3,19,39))">
							<div class="panel panel-primary">
								<div class="panel-heading"></div>
								<div class="panel-body">
									<div class="stbigimg shadow">
										<div id="plot_month08"></div>
									</div>
								</div>
								<div class="panel-footer"></div>
							</div>
						</div>
					</div>
				</div>
				<div class="col-2">
					<div class="box" style="--c:#062d63;--w:10px;--b:3px">
						<div style="background-image: radial-gradient(rgb(12,47,90),rgb(3,19,39))">
							<div class="panel panel-primary">
								<div class="panel-heading"></div>
								<div class="panel-body">
									<div class="stbigimg shadow">
										<div id="plot_month09"></div>
									</div>
								</div>
								<div class="panel-footer"></div>
							</div>
						</div>
					</div>
				</div>
				<div class="col-2">
					<div class="box" style="--c:#062d63;--w:10px;--b:3px">
						<div style="background-image: radial-gradient(rgb(12,47,90),rgb(3,19,39))">
							<div class="panel panel-primary">
								<div class="panel-heading"></div>
								<div class="panel-body">
									<div class="stbigimg shadow">
										<div id="plot_month10"></div>
									</div>
								</div>
								<div class="panel-footer"></div>
							</div>
						</div>
					</div>
				</div>
				<div class="col-2">
					<div class="box" style="--c:#062d63;--w:10px;--b:3px">
						<div style="background-image: radial-gradient(rgb(12,47,90),rgb(3,19,39))">
							<div class="panel panel-primary">
								<div class="panel-heading"></div>
								<div class="panel-body">
									<div class="stbigimg shadow">
										<div id="plot_month11"></div>
									</div>
								</div>
								<div class="panel-footer"></div>
							</div>
						</div>
					</div>
				</div>
				<div class="col-2">
					<div class="box" style="--c:#062d63;--w:10px;--b:3px">
						<div style="background-image: radial-gradient(rgb(12,47,90),rgb(3,19,39))">
							<div class="panel panel-primary">
								<div class="panel-heading"></div>
								<div class="panel-body">
									<div class="stbigimg shadow">
										<div id="plot_month12"></div>
									</div>
								</div>
								<div class="panel-footer"></div>
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
	name: "ysolarTest01",
	components: {
	},
	data() {
		return {
			loading:true,
			stationData: {},
		};
	},
	methods: {
		plot_panel1() {
			const MyPlot = document.getElementById("plot_1");
			MyPlot.innerHTML = "";
			var endData = [];
			// var generate = [145689,142309,135689,147790,153369,143066,148869,150060,159978,163048,145350,139563]
			var generate = this.stationData.kwh_whole_year
			var use = this.stationData.CHB_Bill_kwh
			var left = this.stationData.CHB_left_kwh
			endData.push({
				type: "bar",
				x: ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'],
				y: use,
				// name: this.$i18n.t("plot.2."),
				name: '餘電量',
				yaxis: "y",
				marker: {
					size: 8,
					color: 'rgba(147,255,147,0.8)'
				},
			});
			endData.push({
				type: "scatter",
				x: ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'],
				y: left,
				// name: this.$i18n.t("plot.實際輸出功率"),
				name: '轉供電量',
				yaxis: "y",
				marker: {
					size: 8,
					color: "#BE77FF"
				},
				fill: 'none'
			});
			endData.push({
				type: "scatter",
				x: ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'],
				y: generate,
				// name: this.$i18n.t("plot.實際輸出功率"),
				name: '發電量',
				yaxis: "y",
				marker: {
					size: 8,
					color: "#00ffff"
				},
			});

			var initialData = [
				{
					type: "bar",
					x: ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'],
					y: [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
					name: '餘電量',
					yaxis: "y",
					marker: {
						size: 8,
						color: 'rgba(147,255,147,0.8)'
					},
				},
				{
					type: "scatter",
					x: ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'],
					y: [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
					name: '發電量',
					yaxis: "y",
					marker: {
						size: 8,
						color: "#00ffff"
					},
				},
				{
					type: "scatter",
					x: ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'],
					y: [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
					name: '轉供電量',
					yaxis: "y",
					marker: {
						size: 8,
						color: "#BE77FF"
					},
					fill: 'tonexty'
				}
			]

			var layout = {
				barmode: 'stack',
				// title = 上面的that.name
				title: {
					text: '全年供需預估',
					font: {
						family: " STHeiti,Coppe,Courier New",
						size: 25,
						color: '#ffffff'
					},
				},
				margin: {
					l: 60,
					r: 40,
					b: 60,
					t: 60,
					pad: 4
				},
				height: 300,
				// x軸樣式
				xaxis: {
					title: {
						text: "time",
						font: {
							color: '#ffffff',
							family: "STHeiti,Copperplate,Courier New",
						},
					},
					range: [-1, 12]
				},
				// y軸樣式
				yaxis: {
					title: {
						text: "kWh",
						font: {
							color: '#ffffff',
							family: "STHeiti,Copperplate,Courier New",
						},
					},
					gridcolor: "rgba(224,224,224,0.5)",
					range: [0, 7000000]
				},
				automargin: true,
				legend: {
					x: this.$store.state.isMobile ? 0 : 1,
					y: this.$store.state.isMobile ? -0.4 : 1,
					font: {
						color: '#ffffff'
					}
				},
				// 不知道
				hovermode: "closest",
				// 懸浮視窗設定
				hoverlabel: {
					// 背景
					bgcolor: "#FFFFFF",
					// 格線
					bordercolor: "#122F5A",
					// 字體
					font: {
						color: "#000000",
					},
				},
				paper_bgcolor: 'rgba(0,0,0,0)',
				plot_bgcolor: 'rgba(0,0,0,0)'
			};

			const animationConfig = {
				transition: {
					duration: 500,
					easing: "cubin-in-out",
				},
				frame: {
					duration: 500
				}
			};

			var config = {
				// 下面這兩個應該是類似參數設定，不太確定
				displaylogo: false,
				modeBarButtonsToRemove: [
					"sendDataToCloud",
					"hoverClosestCartesian",
					"hoverCompareCartesian",
					"toggleSpikelines",
					"pan2d",
					"lasso2d",
					"zoomIn2d",
					"zoomOut2d",
					"autoScale2d"
				],
			}

			// 繪圖的函數，輸入一：MyPlot(應該是要在哪裡繪圖)，輸入二：上面的兩個data.push，輸入三：上面設定的輸出樣式
			this.Plotly.newPlot(MyPlot, initialData, layout, config)
			this.Plotly.animate(MyPlot, { data: endData }, animationConfig);
		},
		plot_panel2() {
			const MyPlot = document.getElementById("plot_2");
			MyPlot.innerHTML = "";
			var endData = [];
			function Sumdata(arr) {
				var sum = 0;
				for (var i = 0; i < arr.length; i++) {
					sum += arr[i];
				}
				return sum;
			}
			var annualTransferVolume = Sumdata(this.stationData.CHB_Bill_kwh)
			var annualLeftKwh = Sumdata(this.stationData.CHB_left_kwh)
			endData.push({
				type: "bar",
				x: ['年度轉供量'],
				y: [annualTransferVolume / 1000],
				// name: this.$i18n.t("plot.實際輸出功率"),
				name: '年度轉供量(M)',
				yaxis: "y",
				marker: {
					size: 8,
					color: "rgba(13,128,255,0.8)"
				},
			});
			endData.push({
				type: "bar",
				x: ['餘電量'],
				y: [annualLeftKwh / 1000],
				// name: this.$i18n.t("plot.實際輸出功率"),
				name: '餘電量(M)',
				yaxis: "y",
				marker: {
					size: 8,
					color: "rgba(12,174,232,0.8)"
				},
			});
			endData.push({
				type: "bar",
				x: ['憑證張數'],
				y: [annualTransferVolume / 1000],
				// name: this.$i18n.t("plot.實際輸出功率"),
				name: '憑證張數(張)',
				yaxis: "y",
				marker: {
					size: 8,
					color: "rgba(0,255,255,0.8)"
				},
			});
			endData.push({
				type: "bar",
				x: ['二氧化碳減量'],
				y: [annualTransferVolume * 0.554 / 1000],
				// name: this.$i18n.t("plot.實際輸出功率"),
				name: '二氧化碳減量(T)',
				yaxis: "y",
				marker: {
					size: 8,
					color: "rgba(12,232,170,0.8)"
				},
			});

			var initialData = [
				{
					type: "bar",
					x: ['年度轉供量'],
					y: [0],
					// name: this.$i18n.t("plot.實際輸出功率"),
					name: '年度轉供量',
					yaxis: "y",
					marker: {
						size: 8,
						color: "rgba(13,128,255,0.8)"
					},
				},
				{
					type: "bar",
					x: ['餘電量'],
					y: [0],
					// name: this.$i18n.t("plot.實際輸出功率"),
					name: '餘電量',
					yaxis: "y",
					marker: {
						size: 8,
						color: "rgba(12,174,232,0.8)"
					},
				},
				{
					type: "bar",
					x: ['憑證張數'],
					y: [0],
					// name: this.$i18n.t("plot.實際輸出功率"),
					name: '憑證張數',
					yaxis: "y",
					marker: {
						size: 8,
						color: "rgba(0,255,255,0.8)"
					},
				},
				{
					type: "bar",
					x: ['二氧化碳減量'],
					y: [0],
					// name: this.$i18n.t("plot.實際輸出功率"),
					name: '二氧化碳減量',
					yaxis: "y",
					marker: {
						size: 8,
						color: "rgba(12,232,170,0.8)"
					},
				}
			]

			var layout = {
				barmode: 'group',
				// title = 上面的that.name
				title: {
					text: '年度轉供量、餘電量、憑證張數、二氧化碳減量',
					font: {
						family: "Courier New, monospace",
						size: 25,
						color: '#ffffff'
					},
				},
				height: 300,
				margin: {
					l: 60,
					r: 40,
					b: 40,
					t: 60,
					pad: 4
				},
				// x軸樣式
				xaxis: {
					// title: {
					// 	text: "time",
					// 	font:{
					// 		color:'#ffffff',
					// 		family: "STHeiti,Copperplate,Courier New",
					// },
					// },
					range: [-1, 4]
				},
				// y軸樣式
				yaxis: {
					// title: {
					// 	text: "Kwh",
					// 	font:{
					// 		color:'#ffffff',
					// 		family: "STHeiti,Copperplate,Courier New",
					// 	},
					// },
					"gridcolor": "rgba(224,224,224,0.5)",
					range: [0, 50000]
				},
				automargin: true,
				legend: {
					x: this.$store.state.isMobile ? 0 : 1,
					y: this.$store.state.isMobile ? -0.4 : 1,
					font: {
						color: '#ffffff'
					}
				},
				// 不知道
				hovermode: "closest",
				// 懸浮視窗設定
				hoverlabel: {
					// 背景
					bgcolor: "#FFFFFF",
					// 格線
					bordercolor: "#122F5A",
					// 字體
					font: {
						color: "#000000",
					},
				},
				paper_bgcolor: 'rgba(0,0,0,0)',
				plot_bgcolor: 'rgba(0,0,0,0)'
			};

			const animationConfig = {
				transition: {
					duration: 3000,
					easing: "cubic-in-out"
				},
				frame: {
					duration: 500
				}
			};

			var config = {
				// 下面這兩個應該是類似參數設定，不太確定
				displaylogo: false,
				modeBarButtonsToRemove: [
					"sendDataToCloud",
					"hoverClosestCartesian",
					"hoverCompareCartesian",
					"toggleSpikelines",
					"pan2d",
					"lasso2d",
					"zoomIn2d",
					"zoomOut2d",
					"autoScale2d"
				],
			}

			// 繪圖的函數，輸入一：MyPlot(應該是要在哪裡繪圖)，輸入二：上面的兩個data.push，輸入三：上面設定的輸出樣式
			this.Plotly.newPlot(MyPlot, initialData, layout, config)
			this.Plotly.animate(MyPlot, { data: endData }, { animationConfig });
		},
		plot_panel_month01() {
			const MyPlot = document.getElementById("plot_month01");
			MyPlot.innerHTML = "";
			// color如果沒有指定色碼的話就會直接隨機
			var color = [];
			var color_index = 0;
			var endData = [];
			endData.push({
				type: "pie",
				// values: [this.stationData.CHB_Bill_kwh[0], this.stationData.CHB_left_kwh[0]],
				values: [this.stationData.CHB_left_kwh[0], this.stationData.CHB_Bill_kwh[0]],
				// name: this.$i18n.t("plot.實際輸出功率"),
				labels: ['轉供電量', '餘電量'],
				marker: {
					size: 8,
					colors: ["rgba(0,128,128,0.8)", "rgba(0,255,255,0.8)"]
				},
				textinfo: "label+percent",
				textposition: "outside",
				textfont: {
					color: '#ffffff'
				},
				hole: .85
			});

			var layout = {
				// title = 上面的that.name
				annotations: [
					{
						font: {
							size: 20,
							color: '#ffffff'
						},
						showarrow: false,
						text: '一月',
						x: 0.5,
						y: 0.5
					}],
				// title: {
				// 	text: '一月',
				// 	font: {
				// 		family: "Courier New, monospace",
				// 		size: 15,
				// 		color:'#ffffff'
				// 	},
				// },
				height: 250,
				margin: {
					l: 30,
					r: 30,
					b: 30,
					t: 30,
				},
				showlegend: false,
				// 不知道
				hovermode: "closest",
				// 懸浮視窗設定
				hoverlabel: {
					// 背景
					bgcolor: "#FFFFFF",
					// 格線
					bordercolor: "#122F5A",
					// 字體
					font: {
						color: "#000000",
					},
				},
				paper_bgcolor: 'rgba(0,0,0,0)',
				plot_bgcolor: 'rgba(0,0,0,0)'
			};

			// const animationConfig = {
			// 	transition: {
			// 	duration: 3000,
			// 	easing: "cubic-in-out"
			// 	},
			// 	frame: {
			// 	duration: 500
			// 	}
			// };

			var config = {
				// 下面這兩個應該是類似參數設定，不太確定
				displaylogo: false,
				modeBarButtonsToRemove: [
					"sendDataToCloud",
					"hoverClosestCartesian",
					"hoverCompareCartesian",
					"toggleSpikelines",
					"pan2d",
					"lasso2d",
					"zoomIn2d",
					"zoomOut2d",
					"autoScale2d"
				],
			}

			// 繪圖的函數(餅狀圖無效)，輸入一：MyPlot(應該是要在哪裡繪圖)，輸入二：上面的兩個data.push，輸入三：上面設定的輸出樣式
			// this.Plotly.newPlot(MyPlot, initialData, layout, config)
			// this.Plotly.animate(MyPlot,{data:endData},{animationConfig});
			this.Plotly.newPlot(MyPlot, endData, layout, config)
		},
		plot_panel_month02() {
			const MyPlot = document.getElementById("plot_month02");
			MyPlot.innerHTML = "";
			// color如果沒有指定色碼的話就會直接隨機
			var color = [];
			var color_index = 0;
			var endData = [];
			endData.push({
				type: "pie",
				values: [this.stationData.CHB_left_kwh[1], this.stationData.CHB_Bill_kwh[1]],
				// name: this.$i18n.t("plot.實際輸出功率"),
				labels: ['轉供電量', '餘電量'],
				marker: {
					size: 8,
					colors: ["rgba(0,128,128,0.8)", "rgba(0,255,255,0.8)"]
				},
				textinfo: "label+percent",
				textposition: "outside",
				textfont: {
					color: '#ffffff'
				},
				hole: .85
			});

			var layout = {
				// title = 上面的that.name
				annotations: [
					{
						font: {
							size: 20,
							color: '#ffffff'
						},
						showarrow: false,
						text: '二月',
						x: 0.5,
						y: 0.5
					}],
				height: 250,
				margin: {
					l: 30,
					r: 30,
					b: 30,
					t: 30,
				},
				showlegend: false,
				// 不知道
				hovermode: "closest",
				// 懸浮視窗設定
				hoverlabel: {
					// 背景
					bgcolor: "#FFFFFF",
					// 格線
					bordercolor: "#122F5A",
					// 字體
					font: {
						color: "#000000",
					},
				},
				paper_bgcolor: 'rgba(0,0,0,0)',
				plot_bgcolor: 'rgba(0,0,0,0)'
			};

			var config = {
				// 下面這兩個應該是類似參數設定，不太確定
				displaylogo: false,
				modeBarButtonsToRemove: [
					"sendDataToCloud",
					"hoverClosestCartesian",
					"hoverCompareCartesian",
					"toggleSpikelines",
					"pan2d",
					"lasso2d",
					"zoomIn2d",
					"zoomOut2d",
					"autoScale2d"
				],
			}

			this.Plotly.newPlot(MyPlot, endData, layout, config)
		},
		plot_panel_month03() {
			const MyPlot = document.getElementById("plot_month03");
			MyPlot.innerHTML = "";
			// color如果沒有指定色碼的話就會直接隨機
			var color = [];
			var color_index = 0;
			var endData = [];
			endData.push({
				type: "pie",
				values: [this.stationData.CHB_left_kwh[2], this.stationData.CHB_Bill_kwh[2]],
				// name: this.$i18n.t("plot.實際輸出功率"),
				labels: ['轉供電量', '餘電量'],
				marker: {
					size: 8,
					colors: ["rgba(0,128,128,0.8)", "rgba(0,255,255,0.8)"]
				},
				textinfo: "label+percent",
				textposition: "outside",
				textfont: {
					color: '#ffffff'
				},
				hole: .85
			});

			var layout = {
				// title = 上面的that.name
				annotations: [
					{
						font: {
							size: 20,
							color: '#ffffff'
						},
						showarrow: false,
						text: '三月',
						x: 0.5,
						y: 0.5
					}],
				height: 250,
				margin: {
					l: 30,
					r: 30,
					b: 30,
					t: 30,
				},
				showlegend: false,
				// 不知道
				hovermode: "closest",
				// 懸浮視窗設定
				hoverlabel: {
					// 背景
					bgcolor: "#FFFFFF",
					// 格線
					bordercolor: "#122F5A",
					// 字體
					font: {
						color: "#000000",
					},
				},
				paper_bgcolor: 'rgba(0,0,0,0)',
				plot_bgcolor: 'rgba(0,0,0,0)'
			};

			var config = {
				// 下面這兩個應該是類似參數設定，不太確定
				displaylogo: false,
				modeBarButtonsToRemove: [
					"sendDataToCloud",
					"hoverClosestCartesian",
					"hoverCompareCartesian",
					"toggleSpikelines",
					"pan2d",
					"lasso2d",
					"zoomIn2d",
					"zoomOut2d",
					"autoScale2d"
				],
			}

			this.Plotly.newPlot(MyPlot, endData, layout, config)
		},
		plot_panel_month04() {
			const MyPlot = document.getElementById("plot_month04");
			MyPlot.innerHTML = "";
			// color如果沒有指定色碼的話就會直接隨機
			var color = [];
			var color_index = 0;
			var endData = [];
			endData.push({
				type: "pie",
				values: [this.stationData.CHB_left_kwh[3], this.stationData.CHB_Bill_kwh[3]],
				// name: this.$i18n.t("plot.實際輸出功率"),
				labels: ['轉供電量', '餘電量'],
				marker: {
					size: 8,
					colors: ["rgba(0,128,128,0.8)", "rgba(0,255,255,0.8)"]
				},
				textinfo: "label+percent",
				textposition: "outside",
				textfont: {
					color: '#ffffff'
				},
				hole: .85
			});

			var layout = {
				// title = 上面的that.name
				annotations: [
					{
						font: {
							size: 20,
							color: '#ffffff'
						},
						showarrow: false,
						text: '四月',
						x: 0.5,
						y: 0.5
					}],
				height: 250,
				margin: {
					l: 30,
					r: 30,
					b: 30,
					t: 30,
				},
				showlegend: false,
				// 不知道
				hovermode: "closest",
				// 懸浮視窗設定
				hoverlabel: {
					// 背景
					bgcolor: "#FFFFFF",
					// 格線
					bordercolor: "#122F5A",
					// 字體
					font: {
						color: "#000000",
					},
				},
				paper_bgcolor: 'rgba(0,0,0,0)',
				plot_bgcolor: 'rgba(0,0,0,0)'
			};

			var config = {
				// 下面這兩個應該是類似參數設定，不太確定
				displaylogo: false,
				modeBarButtonsToRemove: [
					"sendDataToCloud",
					"hoverClosestCartesian",
					"hoverCompareCartesian",
					"toggleSpikelines",
					"pan2d",
					"lasso2d",
					"zoomIn2d",
					"zoomOut2d",
					"autoScale2d"
				],
			}

			this.Plotly.newPlot(MyPlot, endData, layout, config)
		},
		plot_panel_month05() {
			const MyPlot = document.getElementById("plot_month05");
			MyPlot.innerHTML = "";
			// color如果沒有指定色碼的話就會直接隨機
			var color = [];
			var color_index = 0;
			var endData = [];
			endData.push({
				type: "pie",
				values:[this.stationData.CHB_left_kwh[4], this.stationData.CHB_Bill_kwh[4]],
				// name: this.$i18n.t("plot.實際輸出功率"),
				labels: ['轉供電量', '餘電量'],
				marker: {
					size: 8,
					colors: ["rgba(0,128,128,0.8)", "rgba(0,255,255,0.8)"]
				},
				textinfo: "label+percent",
				textposition: "outside",
				textfont: {
					color: '#ffffff'
				},
				hole: .85
			});

			var layout = {
				// title = 上面的that.name
				annotations: [
					{
						font: {
							size: 20,
							color: '#ffffff'
						},
						showarrow: false,
						text: '五月',
						x: 0.5,
						y: 0.5
					}],
				height: 250,
				margin: {
					l: 30,
					r: 30,
					b: 30,
					t: 30,
				},
				showlegend: false,
				// 不知道
				hovermode: "closest",
				// 懸浮視窗設定
				hoverlabel: {
					// 背景
					bgcolor: "#FFFFFF",
					// 格線
					bordercolor: "#122F5A",
					// 字體
					font: {
						color: "#000000",
					},
				},
				paper_bgcolor: 'rgba(0,0,0,0)',
				plot_bgcolor: 'rgba(0,0,0,0)'
			};

			var config = {
				// 下面這兩個應該是類似參數設定，不太確定
				displaylogo: false,
				modeBarButtonsToRemove: [
					"sendDataToCloud",
					"hoverClosestCartesian",
					"hoverCompareCartesian",
					"toggleSpikelines",
					"pan2d",
					"lasso2d",
					"zoomIn2d",
					"zoomOut2d",
					"autoScale2d"
				],
			}

			this.Plotly.newPlot(MyPlot, endData, layout, config)
		},
		plot_panel_month06() {
			const MyPlot = document.getElementById("plot_month06");
			MyPlot.innerHTML = "";
			// color如果沒有指定色碼的話就會直接隨機
			var color = [];
			var color_index = 0;
			var endData = [];
			endData.push({
				type: "pie",
				values: [this.stationData.CHB_left_kwh[5], this.stationData.CHB_Bill_kwh[5]],
				// name: this.$i18n.t("plot.實際輸出功率"),
				labels: ['轉供電量', '餘電量'],
				marker: {
					size: 8,
					colors: ["rgba(0,128,128,0.8)", "rgba(0,255,255,0.8)"]
				},
				textinfo: "label+percent",
				textposition: "outside",
				textfont: {
					color: '#ffffff'
				},
				hole: .85
			});

			var layout = {
				// title = 上面的that.name
				annotations: [
					{
						font: {
							size: 20,
							color: '#ffffff'
						},
						showarrow: false,
						text: '六月',
						x: 0.5,
						y: 0.5
					}],
				height: 250,
				margin: {
					l: 30,
					r: 30,
					b: 30,
					t: 30,
				},
				showlegend: false,
				// 不知道
				hovermode: "closest",
				// 懸浮視窗設定
				hoverlabel: {
					// 背景
					bgcolor: "#FFFFFF",
					// 格線
					bordercolor: "#122F5A",
					// 字體
					font: {
						color: "#000000",
					},
				},
				paper_bgcolor: 'rgba(0,0,0,0)',
				plot_bgcolor: 'rgba(0,0,0,0)'
			};

			var config = {
				// 下面這兩個應該是類似參數設定，不太確定
				displaylogo: false,
				modeBarButtonsToRemove: [
					"sendDataToCloud",
					"hoverClosestCartesian",
					"hoverCompareCartesian",
					"toggleSpikelines",
					"pan2d",
					"lasso2d",
					"zoomIn2d",
					"zoomOut2d",
					"autoScale2d"
				],
			}

			this.Plotly.newPlot(MyPlot, endData, layout, config)
		},
		plot_panel_month07() {
			const MyPlot = document.getElementById("plot_month07");
			MyPlot.innerHTML = "";
			// color如果沒有指定色碼的話就會直接隨機
			var color = [];
			var color_index = 0;
			var endData = [];
			endData.push({
				type: "pie",
				values: [this.stationData.CHB_left_kwh[6], this.stationData.CHB_Bill_kwh[6]],
				// name: this.$i18n.t("plot.實際輸出功率"),
				labels: ['轉供電量', '餘電量'],
				marker: {
					size: 8,
					colors: ["rgba(0,128,128,0.8)", "rgba(0,255,255,0.8)"]
				},
				textinfo: "label+percent",
				textposition: "outside",
				textfont: {
					color: '#ffffff'
				},
				hole: .85
			});

			var layout = {
				// title = 上面的that.name
				annotations: [
					{
						font: {
							size: 20,
							color: '#ffffff'
						},
						showarrow: false,
						text: '七月',
						x: 0.5,
						y: 0.5
					}],
				height: 250,
				margin: {
					l: 30,
					r: 30,
					b: 30,
					t: 30,
				},
				showlegend: false,
				// 不知道
				hovermode: "closest",
				// 懸浮視窗設定
				hoverlabel: {
					// 背景
					bgcolor: "#FFFFFF",
					// 格線
					bordercolor: "#122F5A",
					// 字體
					font: {
						color: "#000000",
					},
				},
				paper_bgcolor: 'rgba(0,0,0,0)',
				plot_bgcolor: 'rgba(0,0,0,0)'
			};

			var config = {
				// 下面這兩個應該是類似參數設定，不太確定
				displaylogo: false,
				modeBarButtonsToRemove: [
					"sendDataToCloud",
					"hoverClosestCartesian",
					"hoverCompareCartesian",
					"toggleSpikelines",
					"pan2d",
					"lasso2d",
					"zoomIn2d",
					"zoomOut2d",
					"autoScale2d"
				],
			}

			this.Plotly.newPlot(MyPlot, endData, layout, config)
		},
		plot_panel_month08() {
			const MyPlot = document.getElementById("plot_month08");
			MyPlot.innerHTML = "";
			// color如果沒有指定色碼的話就會直接隨機
			var color = [];
			var color_index = 0;
			var endData = [];
			endData.push({
				type: "pie",
				values: [this.stationData.CHB_left_kwh[7], this.stationData.CHB_Bill_kwh[7]],
				// name: this.$i18n.t("plot.實際輸出功率"),
				labels: ['轉供電量', '餘電量'],
				marker: {
					size: 8,
					colors: ["rgba(0,128,128,0.8)", "rgba(0,255,255,0.8)"]
				},
				textinfo: "label+percent",
				textposition: "outside",
				textfont: {
					color: '#ffffff'
				},
				hole: .85
			});

			var layout = {
				// title = 上面的that.name
				annotations: [
					{
						font: {
							size: 20,
							color: '#ffffff'
						},
						showarrow: false,
						text: '八月',
						x: 0.5,
						y: 0.5
					}],
				height: 250,
				margin: {
					l: 30,
					r: 30,
					b: 30,
					t: 30,
				},
				showlegend: false,
				// 不知道
				hovermode: "closest",
				// 懸浮視窗設定
				hoverlabel: {
					// 背景
					bgcolor: "#FFFFFF",
					// 格線
					bordercolor: "#122F5A",
					// 字體
					font: {
						color: "#000000",
					},
				},
				paper_bgcolor: 'rgba(0,0,0,0)',
				plot_bgcolor: 'rgba(0,0,0,0)'
			};

			var config = {
				// 下面這兩個應該是類似參數設定，不太確定
				displaylogo: false,
				modeBarButtonsToRemove: [
					"sendDataToCloud",
					"hoverClosestCartesian",
					"hoverCompareCartesian",
					"toggleSpikelines",
					"pan2d",
					"lasso2d",
					"zoomIn2d",
					"zoomOut2d",
					"autoScale2d"
				],
			}

			this.Plotly.newPlot(MyPlot, endData, layout, config)
		},
		plot_panel_month09() {
			const MyPlot = document.getElementById("plot_month09");
			MyPlot.innerHTML = "";
			// color如果沒有指定色碼的話就會直接隨機
			var color = [];
			var color_index = 0;
			var endData = [];
			endData.push({
				type: "pie",
				values: [this.stationData.CHB_left_kwh[8], this.stationData.CHB_Bill_kwh[8]],
				// name: this.$i18n.t("plot.實際輸出功率"),
				labels: ['轉供電量', '餘電量'],
				marker: {
					size: 8,
					colors: ["rgba(0,128,128,0.8)", "rgba(0,255,255,0.8)"]
				},
				textinfo: "label+percent",
				textposition: "outside",
				textfont: {
					color: '#ffffff'
				},
				hole: .85
			});

			var layout = {
				// title = 上面的that.name
				annotations: [
					{
						font: {
							size: 20,
							color: '#ffffff'
						},
						showarrow: false,
						text: '九月',
						x: 0.5,
						y: 0.5
					}],
				height: 250,
				margin: {
					l: 30,
					r: 30,
					b: 30,
					t: 30,
				},
				showlegend: false,
				// 不知道
				hovermode: "closest",
				// 懸浮視窗設定
				hoverlabel: {
					// 背景
					bgcolor: "#FFFFFF",
					// 格線
					bordercolor: "#122F5A",
					// 字體
					font: {
						color: "#000000",
					},
				},
				paper_bgcolor: 'rgba(0,0,0,0)',
				plot_bgcolor: 'rgba(0,0,0,0)'
			};

			var config = {
				// 下面這兩個應該是類似參數設定，不太確定
				displaylogo: false,
				modeBarButtonsToRemove: [
					"sendDataToCloud",
					"hoverClosestCartesian",
					"hoverCompareCartesian",
					"toggleSpikelines",
					"pan2d",
					"lasso2d",
					"zoomIn2d",
					"zoomOut2d",
					"autoScale2d"
				],
			}

			this.Plotly.newPlot(MyPlot, endData, layout, config)
		},
		plot_panel_month10() {
			const MyPlot = document.getElementById("plot_month10");
			MyPlot.innerHTML = "";
			// color如果沒有指定色碼的話就會直接隨機
			var color = [];
			var color_index = 0;
			var endData = [];
			endData.push({
				type: "pie",
				values: [this.stationData.CHB_left_kwh[9], this.stationData.CHB_Bill_kwh[9]],
				// name: this.$i18n.t("plot.實際輸出功率"),
				labels: ['轉供電量', '餘電量'],
				marker: {
					size: 8,
					colors: ["rgba(0,128,128,0.8)", "rgba(0,255,255,0.8)"]
				},
				textinfo: "label+percent",
				textposition: "outside",
				textfont: {
					color: '#ffffff'
				},
				hole: .85
			});

			var layout = {
				// title = 上面的that.name
				annotations: [
					{
						font: {
							size: 20,
							color: '#ffffff'
						},
						showarrow: false,
						text: '十月',
						x: 0.5,
						y: 0.5
					}],
				height: 250,
				margin: {
					l: 30,
					r: 30,
					b: 30,
					t: 30,
				},
				showlegend: false,
				// 不知道
				hovermode: "closest",
				// 懸浮視窗設定
				hoverlabel: {
					// 背景
					bgcolor: "#FFFFFF",
					// 格線
					bordercolor: "#122F5A",
					// 字體
					font: {
						color: "#000000",
					},
				},
				paper_bgcolor: 'rgba(0,0,0,0)',
				plot_bgcolor: 'rgba(0,0,0,0)'
			};

			var config = {
				// 下面這兩個應該是類似參數設定，不太確定
				displaylogo: false,
				modeBarButtonsToRemove: [
					"sendDataToCloud",
					"hoverClosestCartesian",
					"hoverCompareCartesian",
					"toggleSpikelines",
					"pan2d",
					"lasso2d",
					"zoomIn2d",
					"zoomOut2d",
					"autoScale2d"
				],
			}

			this.Plotly.newPlot(MyPlot, endData, layout, config)
		},
		plot_panel_month11() {
			const MyPlot = document.getElementById("plot_month11");
			MyPlot.innerHTML = "";
			// color如果沒有指定色碼的話就會直接隨機
			var color = [];
			var color_index = 0;
			var endData = [];
			endData.push({
				type: "pie",
				values:[this.stationData.CHB_left_kwh[10], this.stationData.CHB_Bill_kwh[10]],
				// name: this.$i18n.t("plot.實際輸出功率"),
				labels: ['轉供電量', '餘電量'],
				marker: {
					size: 8,
					colors: ["rgba(0,128,128,0.8)", "rgba(0,255,255,0.8)"]
				},
				textinfo: "label+percent",
				textposition: "outside",
				textfont: {
					color: '#ffffff'
				},
				hole: .85
			});

			var layout = {
				// title = 上面的that.name
				annotations: [
					{
						font: {
							size: 20,
							color: '#ffffff'
						},
						showarrow: false,
						text: '十一月',
						x: 0.5,
						y: 0.5
					}],
				height: 250,
				margin: {
					l: 30,
					r: 30,
					b: 30,
					t: 30,
				},
				showlegend: false,
				// 不知道
				hovermode: "closest",
				// 懸浮視窗設定
				hoverlabel: {
					// 背景
					bgcolor: "#FFFFFF",
					// 格線
					bordercolor: "#122F5A",
					// 字體
					font: {
						color: "#000000",
					},
				},
				paper_bgcolor: 'rgba(0,0,0,0)',
				plot_bgcolor: 'rgba(0,0,0,0)'
			};

			var config = {
				// 下面這兩個應該是類似參數設定，不太確定
				displaylogo: false,
				modeBarButtonsToRemove: [
					"sendDataToCloud",
					"hoverClosestCartesian",
					"hoverCompareCartesian",
					"toggleSpikelines",
					"pan2d",
					"lasso2d",
					"zoomIn2d",
					"zoomOut2d",
					"autoScale2d"
				],
			}

			this.Plotly.newPlot(MyPlot, endData, layout, config)
		},
		plot_panel_month12() {
			const MyPlot = document.getElementById("plot_month12");
			MyPlot.innerHTML = "";
			// color如果沒有指定色碼的話就會直接隨機
			var color = [];
			var color_index = 0;
			var endData = [];
			endData.push({
				type: "pie",
				values: [this.stationData.CHB_left_kwh[11], this.stationData.CHB_Bill_kwh[11]],
				// name: this.$i18n.t("plot.實際輸出功率"),
				labels: ['轉供電量', '餘電量'],
				marker: {
					size: 8,
					colors: ["rgba(0,128,128,0.8)", "rgba(0,255,255,0.8)"]
				},
				textinfo: "label+percent",
				textposition: "outside",
				textfont: {
					color: '#ffffff'
				},
				hole: .85
			});

			var layout = {
				// title = 上面的that.name
				annotations: [
					{
						font: {
							size: 20,
							color: '#ffffff'
						},
						showarrow: false,
						text: '十二月',
						x: 0.5,
						y: 0.5
					}],
				height: 250,
				margin: {
					l: 30,
					r: 30,
					b: 30,
					t: 30,
				},
				showlegend: false,
				// 不知道
				hovermode: "closest",
				// 懸浮視窗設定
				hoverlabel: {
					// 背景
					bgcolor: "#FFFFFF",
					// 格線
					bordercolor: "#122F5A",
					// 字體
					font: {
						color: "#000000",
					},
				},
				paper_bgcolor: 'rgba(0,0,0,0)',
				plot_bgcolor: 'rgba(0,0,0,0)'
			};

			var config = {
				// 下面這兩個應該是類似參數設定，不太確定
				displaylogo: false,
				modeBarButtonsToRemove: [
					"sendDataToCloud",
					"hoverClosestCartesian",
					"hoverCompareCartesian",
					"toggleSpikelines",
					"pan2d",
					"lasso2d",
					"zoomIn2d",
					"zoomOut2d",
					"autoScale2d"
				],
			}

			this.Plotly.newPlot(MyPlot, endData, layout, config)
		},
		async getPostData() {
			this.loading = true
			await this.axios.post('/setting/ysolar_test', {
			}).then(data => {
				console.log(data.data.data)
				this.stationData = data.data.data
				this.plot_panel1(),
					this.plot_panel2(),
					this.plot_panel_month01(),
					this.plot_panel_month02(),
					this.plot_panel_month03(),
					this.plot_panel_month04(),
					this.plot_panel_month05(),
					this.plot_panel_month06(),
					this.plot_panel_month07(),
					this.plot_panel_month08(),
					this.plot_panel_month09(),
					this.plot_panel_month10(),
					this.plot_panel_month11(),
					this.plot_panel_month12()
			})
			this.loading = false;
		}
	},
	watch: {

	},
	mounted() {
		this.getPostData()
	},
	unmounted() {
	}
};
</script>


<!-- 設定css的部分(樣式) -->
<style scoped>
/* card，轉成正式頁面以後要改成總背景 */
.card {
	/* background: rgb(3, 19, 39); */
	background: rgb(5, 30, 61);
}

/* 面板背景 */
.box {
	--b: 5px;
	/* thickness of the border */
	--c: red;
	/* color of the border */
	--w: 20px;
	/* width of border */


	border: var(--b) solid #0000;
	/* space for the border */
	--_g: #0000 90deg, var(--c) 0;
	--_p: var(--w) var(--w) border-box no-repeat;
	background:
		conic-gradient(from 90deg at top var(--b) left var(--b), var(--_g)) 0 0 / var(--_p),
		conic-gradient(from 180deg at top var(--b) right var(--b), var(--_g)) 100% 0 / var(--_p),
		conic-gradient(from 0deg at bottom var(--b) left var(--b), var(--_g)) 0 100% / var(--_p),
		conic-gradient(from -90deg at bottom var(--b) right var(--b), var(--_g)) 100% 100% / var(--_p);
}

/* 分隔線 */
.divider {
	border-color: rgb(66, 66, 66)
}

/* plot框框 */
.stbigimg {
	position: relative;
	max-width: 100%;
	max-height: 100%;
	border-radius: 1rem;
	/* box-shadow: 0 0 15px #dee4ea; */
	overflow: hidden;
	background-color: rgba(0, 0, 0, 0);
}

.table_header_style {
	background-color: rgba(0, 0, 0, 0);
	color: white
}
</style>