<template>
	<div class="card p-4" id="card" v-loading="loading" element-loading-background="rgba(3, 19, 39, 0.8)">
		<div class="container-fluid">
			<br><br><br>
			<div class="row">
				<div class="col-sm-4">
					<div class="box" style="--c:#062d63;--w:10px;--b:3px">
						<div style="background-image: radial-gradient(rgb(12,47,90),rgb(3,19,39))">
							<div class="panel panel-primary">
								<div class="panel-heading"></div>
								<!-- AFC執行率統計 -->
								<div class="panel-body" style="height:300px;">
									<div class="stbigimg shadow">
										<div id="plot_1"></div>
									</div>
								</div>
								<div class="panel-footer"></div>
							</div>
						</div>
					</div>
				</div>
				<div class="col-sm-4">
					<div class="box" style="--c:#062d63;--w:10px;--b:3px">
						<div style="background-image: radial-gradient(rgb(12,47,90),rgb(3,19,39))">
							<div class="panel panel-primary">
								<div class="panel-heading"></div>
								<!-- 昨日輔電 -->
								<div class="panel-body" style="height:300px;">
									<div class="stbigimg shadow">
										<div id="plot_2"></div>
									</div>
								</div>
								<div class="panel-footer"></div>
							</div>
						</div>
					</div>
				</div>
				<div class="col-sm-4">
					<div class="box" style="--c:#062d63;--w:10px;--b:3px">
						<div style="background-image: radial-gradient(rgb(12,47,90),rgb(3,19,39))">
							<div class="panel panel-primary">
								<div class="panel-heading"></div>
								<!-- 昨日輔電 -->
								<div class="panel-body" style="height:300px;">
									<div class="stbigimg shadow">
										<div id="plot_3"></div>
									</div>
								</div>
								<div class="panel-footer"></div>
							</div>
						</div>
					</div>
				</div>
			</div>
			<br><br>
			<el-divider style="--el-border-style:solid;margin-top: 35px;margin-bottom: 39px;" class="divider"></el-divider>
			<br><br>
			<div class="row">
                <div class="col-sm-4">
					<div class="box" style="--c:#062d63;--w:10px;--b:3px">
						<div style="background-image: radial-gradient(rgb(12,47,90),rgb(3,19,39))">
							<div class="panel panel-primary">
								<div class="panel-heading"></div>
								<!-- 各案場運轉資訊1 -->
								<div class="panel-body">
									<div class="row">
										<div class="col-sm-6 align-items-center">
											<div class="text-center" style="padding-top:25px;">
												<p class="fs-4" style="color:white;">天璇 2.1 MW</p>
												<img :src="battery1" style="height:130px; width:150px;" />
												<p class="fs-4" style="color:white;">系統SoC：{{stationData.get_data_done? stationData.TianXuan_info.battery.soc :'none'}}%</p>
											</div>
										</div>
										<div class="col-sm-6">
											<div class="" style="padding-top:12px;">
												<p class="fs-5" style="color:white;">系統平均執行率：{{stationData.get_data_done?stationData.TianXuan_info.system.SBSPM:'none'}}%</p>
												<p class="fs-5" style="color:white;">系統實功：{{stationData.get_data_done?stationData.TianXuan_info.vab_acm.p:'none'}}kW</p>
												<p class="fs-5" style="color:white;">系統虛功：{{stationData.get_data_done?stationData.TianXuan_info.vab_acm.q:'none'}}kVAR</p>
												<p class="fs-5" style="color:white;">最高溫度：{{stationData.get_data_done?stationData.TianXuan_info.env.temp_max:'none'}}°C</p>
												<p class="fs-5" style="color:white;">最高濕度：{{stationData.get_data_done?stationData.TianXuan_info.env.humi_max:'none'}}%</p>
											</div>
										</div>
									</div>
								</div>
								<div class="panel-footer"></div>
							</div>
						</div>
					</div>
				</div>
				<div class="col-sm-4">
					<div class="box" style="--c:#062d63;--w:10px;--b:3px">
						<div style="background-image: radial-gradient(rgb(12,47,90),rgb(3,19,39))">
							<div class="panel panel-primary">
								<div class="panel-heading"></div>
								<!-- 各案場運轉資訊2 -->
								<div class="panel-body">
									<div class="row">
										<div class="col-sm-6 align-items-center">
											<div class="text-center" style="padding-top:25px;">
												<p class="fs-4" style="color:white;">韓暘 2.1 MW</p>
												<img :src="battery2" style="height:130px; width:150px;" />
												<p class="fs-4" style="color:white;">系統SoC：{{stationData.get_data_done?stationData.HanYang_info.battery.soc:'none'}}%</p>
											</div>
										</div>
										<div class="col-sm-6">
											<div class="" style="padding-top:12px;">
												<p class="fs-5" style="color:white;">系統平均執行率：{{stationData.get_data_done?stationData.HanYang_info.system.SBSPM:'none'}}%</p>
												<p class="fs-5" style="color:white;">系統實功：{{stationData.get_data_done?stationData.HanYang_info.vab_acm.p:'none'}}kW</p>
												<p class="fs-5" style="color:white;">系統虛功：{{stationData.get_data_done?stationData.HanYang_info.vab_acm.q:'none'}}kVAR</p>
												<p class="fs-5" style="color:white;">最高溫度：{{stationData.get_data_done?stationData.HanYang_info.env.temp_max:'none'}}°C</p>
												<p class="fs-5" style="color:white;">最高濕度：{{stationData.get_data_done?stationData.HanYang_info.env.humi_max:'none'}}%</p>
											</div>
										</div>
									</div>
								</div>
								<div class="panel-footer"></div>
							</div>
						</div>
					</div>
				</div>
				<div class="col-sm-4">
					<div class="box" style="--c:#062d63;--w:10px;--b:3px">
						<div style="background-image: radial-gradient(rgb(12,47,90),rgb(3,19,39))">
							<div class="panel panel-primary">
								<div class="panel-heading"></div>
								<!-- 各案場運轉資訊3 -->
								<div class="panel-body">
									<div class="row">
										<div class="col-sm-6 align-items-center">
											<div class="text-center" style="padding-top:25px;">
												<p class="fs-4" style="color:white;">天樞 8.4 MW</p>
												<img :src="battery4" style="height:130px; width:150px;" />
												<p class="fs-4" style="color:white;">系統SoC：{{stationData.get_data_done?stationData.TianShu_info.battery.soc:'none'}}%</p>
											</div>
										</div>
										<div class="col-sm-6">
											<div class="" style="padding-top:12px;">
												<p class="fs-5" style="color:white;">系統平均執行率：{{stationData.get_data_done?stationData.TianShu_info.system.SBSPM:'none'}}%</p>
												<p class="fs-5" style="color:white;">系統實功：{{stationData.get_data_done?stationData.TianShu_info.vab_acm.p:'none'}}kW</p>
												<p class="fs-5" style="color:white;">系統虛功：{{stationData.get_data_done?stationData.TianShu_info.vab_acm.q:'none'}}kVAR</p>
												<p class="fs-5" style="color:white;">最高溫度：{{stationData.get_data_done?stationData.TianShu_info.env.temp_max:'none'}}°C</p>
												<p class="fs-5" style="color:white;">最高濕度：{{stationData.get_data_done?stationData.TianShu_info.env.humi_max:'none'}}%</p>
											</div>
										</div>
									</div>
								</div>
								<div class="panel-footer"></div>
							</div>
						</div>
					</div>
				</div>
			</div>
			<br><br><br><br><br>
		</div>
	</div>
</template>

<script>
import * as d3 from 'd3'
import myJson from '../components/ysolar_test/twCounty2010geo.json'
// import $ from 'jquery'

export default {
    name: "ysolarTest04",
	components: {
	},
	data() {
		return {
			loading:true,
			stationData:{get_data_done:false},
			battery1: require('../components/ysolar_test/battery1.svg'),
			battery2: require('../components/ysolar_test/battery2.svg'),
			battery3: require('../components/ysolar_test/battery3.svg'),
			battery4: require('../components/ysolar_test/battery4.svg'),
			CHB_Bill_kwh:[161400,154800,198800,196000,234800,236000,260400,256400,250400,218800,207600,192000]
		};
	},
	methods: {
		plot_panel1() {
			const MyPlot = document.getElementById("plot_1");
			MyPlot.innerHTML = "";
			// color如果沒有指定色碼的話就會直接隨機
			var endData = [];
			endData.push({
				type: "bar",
				x: ['0~70','70~75','75~85','85~95','95~100'],
				y: this.stationData.afc_list,
				// name: this.$i18n.t("plot.實際輸出功率"),
				name: '每小時平均執行率',
				yaxis: "y",
				marker: {
					size: 8,
					color:'#FF8040'
				},
			});

			var initialData=[
			{
				type: "bar",
					x: ['0~70','70~75','75~85','85~95','95~100'],
					y: [0,0,0,0,0],
					name: '每小時平均執行率',
					yaxis: "y",
					marker: {
						size: 8,
						color:'#FF8040'
				},
			}
			]

			var layout = {
				barmode: 'stack',
				// title = 上面的that.name
				title: {
					text: 'AFC執行率統計',
					font: {
						family: " STHeiti,Coppe,Courier New",
						size: 25,
						color:'#ffffff'
					},
				},
				margin: {
					l: 60,
					r: 40,
					b: 60,
					t: 60,
					pad: 4
				},
				height:300,
				// x軸樣式
				xaxis: {
					title: {
						text: "小時平均執行率",
						font:{
							color:'#ffffff',
							family: "STHeiti,Copperplate,Courier New",
						},
					},
					range:[-1,5]
				},
				// y軸樣式
				yaxis: {
					title: {
						text: "案場數量",
						font:{
							color:'#ffffff',
							family: "STHeiti,Copperplate,Courier New",
						},
					},
					gridcolor:"rgba(224,224,224,0.5)",
					range:[0,this.stationData.afc_list[5]]
				},
				automargin: true,
				legend: {
					x: this.$store.state.isMobile ? 0 : 1,
					y: this.$store.state.isMobile ? -0.4 : 1,
					font:{
						color:'#ffffff'
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
				duration: 6000,
				easing: "cubic-in-out"
				},
				frame: {
				duration: 6000
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
			this.Plotly.animate(MyPlot,{data:endData},{animationConfig});
		},
		plot_panel2() {
			const MyPlot = document.getElementById("plot_2");
			MyPlot.innerHTML = "";
			var endData = [];
			endData.push({
					type: "bar",
					x: ['天璇','韓暘','天樞'],
					y: [this.stationData.HanYang_info.vab_acm.tot_kwh,this.stationData.TianShu_info.vab_acm.tot_kwh,this.stationData.TianXuan_info.vab_acm.tot_kwh],
					// name: this.$i18n.t("plot.實際輸出功率"),
					name: '累計充放電能',
					yaxis: "y",
					marker: {
						size: 8,
						color: "rgba(0,255,255,0.8)"
					},
				});

			var initialData=[
			{
				type: "bar",
				x:['天璇','韓暘','天樞'],
				y: [0,0,0],
				// name: this.$i18n.t("plot.實際輸出功率"),
				name: '累計充放電能',
				yaxis: "y",
				marker: {
					size: 8,
					color: "rgba(0,255,255,0.8)"
				},
			}
			]

			var layout = {
				barmode: 'group',
				// title = 上面的that.name
				title: {
					text: '累計充放電能',
					font: {
						family: "Courier New, monospace",
						size: 25,
						color:'#ffffff'
					},
				},
				height:300,
				margin: {
					l: 60,
					r: 40,
					b: 40,
					t: 60,
					pad: 4
				},
				// x軸樣式
				xaxis: {
					title: {
						text: "案場名稱",
						font:{
							color:'#ffffff',
							family: "STHeiti,Copperplate,Courier New",
					},
					},
					range:[-1,this.stationData.afc_list[5]]
				},
				// y軸樣式
				yaxis: {
					title: {
						text: "Kwh",
						font:{
							color:'#ffffff',
							family: "STHeiti,Copperplate,Courier New",
						},
					},
					"gridcolor":"rgba(224,224,224,0.5)",
					// 範圍暫定為天樞+10000kwh
					range:[0,this.stationData.TianShu_info.vab_acm.tot_kwh+10000]
				},
				automargin: true,
				legend: {
					x: this.$store.state.isMobile ? 0 : 1,
					y: this.$store.state.isMobile ? -0.4 : 1,
					font:{
						color:'#ffffff'
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
			this.Plotly.animate(MyPlot,{data:endData},{animationConfig});
		},
		plot_panel3() {
			const MyPlot = document.getElementById("plot_3");
			MyPlot.innerHTML = "";
			// color如果沒有指定色碼的話就會直接隨機
			var endData = [];
			endData.push({
					type: "bar",
					x: ['天璇','韓暘','天樞'],
					y: [this.stationData.HanYang_info.rte,this.stationData.TianShu_info.rte,this.stationData.TianXuan_info.rte],
					// name: this.$i18n.t("plot.實際輸出功率"),
					name: '往返效率',
					yaxis: "y",
					marker: {
						size: 8,
						color: "rgba(0,255,255,0.8)"
					},
				});

			var initialData=[
			{
				type: "bar",
				x: ['天璇','韓暘','天樞'],
				y: [0,0,0],
				// name: this.$i18n.t("plot.實際輸出功率"),
				name: '往返效率',
				yaxis: "y",
				marker: {
					size: 8,
					color: "rgba(0,255,255,0.8)"
				},
			}
			]

			var layout = {
				barmode: 'group',
				// title = 上面的that.name
				title: {
					text: '往返效率',
					font: {
						family: "Courier New, monospace",
						size: 25,
						color:'#ffffff'
					},
				},
				height:300,
				margin: {
					l: 60,
					r: 40,
					b: 40,
					t: 60,
					pad: 4
				},
				// x軸樣式
				xaxis: {
					title: {
						text: "案場名稱",
						font:{
							color:'#ffffff',
							family: "STHeiti,Copperplate,Courier New",
					},
					},
					range:[-1,this.stationData.afc_list[5]]
				},
				// y軸樣式
				yaxis: {
					title: {
						text: "百分比(%)",
						font:{
							color:'#ffffff',
							family: "STHeiti,Copperplate,Courier New",
						},
					},
					"gridcolor":"rgba(224,224,224,0.5)",
					range:[0,1]
				},
				automargin: true,
				legend: {
					x: this.$store.state.isMobile ? 0 : 1,
					y: this.$store.state.isMobile ? -0.4 : 1,
					font:{
						color:'#ffffff'
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
			this.Plotly.animate(MyPlot,{data:endData},{animationConfig});
		},
		async getPostData_normal(){
			this.loading = true
			await this.axios.post('/setting/get_ysolar_energy_storage', {
				// normal、click_TianXuan、click_HanYang、click_TianShu
				'method':'normal'
			}).then(data => {
				console.log(data.data.data)
				this.stationData = data.data.data
				this.plot_panel1();
				this.plot_panel2();
				this.plot_panel3();
				this.loading = false;
			})
		},
		test(){
			console.log('123123')
		}
	},
	watch: {
	},
	mounted() {
		this.getPostData_normal()
	},
	unmounted() {
	}
};
</script>


<!-- 設定css的部分(樣式) -->
<style scoped>
/* card，轉成正式頁面以後要改成總背景 */
.card{
	/* background: rgb(3, 19, 39); */
	background: rgb(5, 30, 61);
}

.box {
	--b: 5px;   /* thickness of the border */
	--c: red;   /* color of the border */
	--w: 20px;  /* width of border */


	border: var(--b) solid #0000; /* space for the border */
	--_g: #0000 90deg,var(--c) 0;
	--_p: var(--w) var(--w) border-box no-repeat;
	background:
	conic-gradient(from 90deg  at top    var(--b) left  var(--b),var(--_g)) 0    0    / var(--_p),
	conic-gradient(from 180deg at top    var(--b) right var(--b),var(--_g)) 100% 0    / var(--_p),
	conic-gradient(from 0deg   at bottom var(--b) left  var(--b),var(--_g)) 0    100% / var(--_p),
	conic-gradient(from -90deg at bottom var(--b) right var(--b),var(--_g)) 100% 100% / var(--_p);
}

/* 分隔線 */
.divider{
	border-color:rgb(66,66,66)
}

body {
  margin: 0;
  padding: 0;
  background: #bbb;
}

.title {
  font-family: Arial;
  margin: 1.5em auto;
  font-size: 2em;
  color: #333;
  text-align: center;
  text-shadow: 1px 1px 0 #ddd;
}

.chart {
  margin: 1.5em auto;
  display: block;
  border: 5px solid #eee;
  box-shadow: 0 0 2px #666, 0 0 150px rgba(0,0,0,.2);
  background-color: #fff;
}

.label-content {
  pointer-events: none;
}
</style>