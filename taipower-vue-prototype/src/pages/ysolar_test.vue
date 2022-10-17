<template>
	<div class="card border-transparent p-4" id="card" v-loading="loading" element-loading-background="rgba(3, 19, 39, 0.8)">
		<div class="container-fluid">
			<div class="row">
				<div class="col-sm-5">
					<!-- 案場發電概況 -->
					<div class="box" style="--c:#062d63;--w:10px;--b:3px">
						<div style="background-image: radial-gradient(rgb(12,47,90),rgb(3,19,39))">
							<div class="panel panel-primary">
								<div class="panel-heading"></div>
								<div class="panel-body">
									<!-- OVERVIEW -->
									<div class="ms-2 me-2 mt-2 ms-lg-2 me-lg-2 mb-4 mb-lg-0 mt-lg-0 ps-3 ps-lg-4 pt-3 me-lg-0">
										<el-select v-model="station_selected" class="mb-4">
											<el-option
												v-for="item in station_select"
												:key="item.station_selected"
												:label="item.label"
												:value="item.station_selected">
											</el-option>
										</el-select>
										<div class="d-flex flex-wrap">
											<div class="col-12 col-lg-6 mb-4 mb-lg-4" v-if="Object.keys(weather_data).length > 0">
												<!--天氣-->
												<div class="col-12 col-lg-12 d-flex pe-4 pe-lg-0 mb-lg-4">
													<div class="card col-12 col-lg-12 weather_card">
														<div class="d-flex flex-wrap align-items-center">

															<!--天氣 if taipower-->
															<div class="col-12 col-lg-12 p-2 pb-0 p-lg-2" v-if="$store.state.user_data.pageType == 'taipower' && !$store.state.isMobile">
																<div class="d-flex flex-wrap justify-content-start">
																	<img class="col-5 col-sm-3 col-md-2 col-lg-1 weather-icon" :src="weather_data.imgurl" />
																	<!-- 溫度 -->
																	<div class="d-flex flex-column">
																		<label class="fs-5 mt-1 temp-color" :style="weatherStyleTaipower">
																			<!-- 溫度 -->
																			溫度：{{weather_data.temperature}}°C
																		</label>
																	</div>

																	<!-- 晴陰雨 -->
																	<div class="fs-5 ms-lg-auto mt-1">
																		{{
																			weather_data.status[$store.state.language] == undefined ?
																			weather_data.status['zh-TW'] : weather_data.status[$store.state.language]
																		}}
																	</div>

																	<!-- 降雨機率 -->
																	<div class="d-flex align-top ms-lg-auto mt-1">
																		<label class="me-2 fs-5 text-center" :class="{'water-color':  weather_data.rain > 0}">
																			<label class="text-danger">
																				{{$t("降雨機率")}}：
																			</label>
																			{{weather_data.rain}}%
																		</label>
																	</div>
																	
																</div>
															</div>
														</div>
													</div>
												</div>

												<!--狀態欄 taipower-->
												<div class="card statab_status col-11 col-lg-12 d-flex flex-wrap text-center">
													<div class="col-12 col-lg-6 py-2" v-for="(item, index) in status_data" :key="index">
														<!-- title -->
														<div class="fs-6">
															<i :class="['icon-'+item.icon, text_colors[index]]"></i>{{$t(`stationData.overview.${item.title}`)}}
														</div>
														<!-- 中間綠色大字1、2 -->
														<div class="fs-6 py-0 text-center" :class="text_colors[index]" v-if="index<2">{{$t(`stationData.overview.${item.text}`)}}</div>
														<!-- 中間綠色大字3、4 -->
														<div class="fs-6 py-0 text-center" :class="text_colors[index]" v-if="index>1">{{item.text}}</div>
													</div>
												</div>
											</div>

											<div class="col-12 col-lg-6">
												<div style="position:relative; bottom:30px" id="plot_today"></div>  
											</div>
										</div>
									</div>
									<!-- OVERVIEW -->
								</div>
								<div class="panel-footer"></div>
							</div>
						</div>
					</div>
					<!-- 月分別電能轉供量、餘電量、憑證張數、二氧化碳減量 -->
					<el-divider class="divider"></el-divider>
					<div class="box" style="--c:#062d63;--w:10px;--b:3px">
						<div style="background-image: radial-gradient(rgb(12,47,90),rgb(3,19,39))">
							<div class="panel panel-primary">
								<div class="panel-heading"></div>
								<div class="panel-body">
									<div class="stbigimg shadow">
										<div id="plot_3"></div>
									</div>
								</div>
								<div class="panel-footer"></div>
							</div>
						</div>
					</div>
				</div>
				<!--右邊欄位-->
				<div class="col-sm-7">
					<div class="box" style="--c:#062d63;--w:10px;--b:3px">
						<div style="background-image: radial-gradient(rgb(12,47,90),rgb(3,19,39))">
							<div class="panel panel-primary">
								<div class="panel-heading"></div>
                                <!-- 台灣地圖兼互動式視窗 -->
								<div class="panel-body">
									<div>
										<svg id="map_page_1" style=""></svg>
                                    </div>
								</div>
								<div class="panel-footer"></div>
							</div>
						</div>
					</div>
					<el-divider class="divider"></el-divider>
					<div class="box" style="--c:#062d63;--w:10px;--b:3px">
						<div style="background-image: radial-gradient(rgb(12,47,90),rgb(3,19,39))">
						<div class="panel panel-primary">
							<div class="panel-heading d-flex justify-content-center">
								<h3 class="mt-2" style="color:white">合約內容</h3>
							</div>
							<div class="panel-body">
								<div class="col-6 col-lg-12 responsive_table">
									<div style="height:260px; overflow-y: auto;">
										<div class="w-100 row responsive_table_header fw-bold m-0 d-none d-lg-flex flex-nowrap">
											<div class="col-3 text-center table_header_style">
												<label class="fs-6">用戶名稱</label>
											</div>
											<div class="col-3 text-center table_header_style">
												<label class="fs-6">用電單位地點</label>
											</div>
											<div class="col-3 text-center table_header_style">
												<label class="fs-6">契約轉供度數</label>
											</div>
											<div class="col-3 text-center table_header_style">
												<label class="fs-6">合約期長</label>
											</div>
										</div>
										<div>
											<!-- 設定body -->
											<div class="w-100 responsive_table_body">
												<div class="row m-0 responsive_table_content mt-2 mt-lg-0 pt-2 pb-3 p-lg-0 " 
													v-for="data in this.collectionData" :key="data.name">
													<div class="col-12 col-lg-3 pt-lg-4 pb-lg-4 ">
														<div class="d-flex d-lg-none">
															<label class="fs-6">{{  data.name  }}</label>
														</div>
														<label class="fs-6 w-100 text-center d-none d-lg-block">{{  data.name 
														}}</label>
													</div>
													<div class="col-12 col-lg-3 pt-lg-4 pb-lg-4">
														<div class="d-flex d-lg-none">
															<label class="fs-6">{{  data.location  }}</label>
														</div>
														<label class="fs-6 w-100 text-center d-none d-lg-block">{{data.location}}</label>
													</div>
													<div class="col-12 col-lg-3 pt-lg-4 pb-lg-4">
														<div class="d-flex d-lg-none">
															<label class="fs-6">{{  data.kwh  }}</label>
														</div>
														<label class="fs-6 w-100 text-center d-none d-lg-block">{{  data.kwh }}度</label>
													</div>
													<div class="col-12 col-lg-3 pt-lg-4 pb-lg-4">
														<div class="d-flex d-lg-none">
															<label class="fs-6">{{  data.date  }}</label>
														</div>
														<label class="fs-6 w-100 text-center d-none d-lg-block">{{  data.date }}</label>
													</div>
												</div>
											</div>
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
		</div>
		<br>
	</div>
</template>

<script>
import * as d3 from 'd3'
import myJson from '../components/ysolar_test/twCounty2010geo.json'

export default {
    name: "ysolarTest01",
	components: {
	},
	data() {
		return {
			county_clicked:{'place_click':'space'},
			station_select:[
				{
					station_selected:'天權',
					label:'天權'
				},
				{
					station_selected:'玉衡',
					label:'玉衡'
				}
			],
			station_selected:'天權',
			text_colors:['text-success','text-success','text-success','text-success'],
			loading:true,
			stationData:{},
			taiwanCountry: [],
			collectionData:[
				{
					name:'XXX機房',
					location:'台北市大安區愛國東路.......',
					kwh:'XXX',
					date:'20220901 - 20270831'
				},
				{
					name:'XXX機房',
					location:'台北市信義區松德路......',
					kwh:'XXX',
					date:'20220901 - 20270831'
				},
				{
					name:'...',
					location:'...',
					kwh:'...',
					date:'...'
				},
				{
					name:'XXX機房',
					location:'新北市新莊區中正路......',
					kwh:'XXX',
					date:'20220901 - 20270831'
				}
			],
			weather_data:{
				'imgurl':'',
				'status':'---',
				'temperature':'25',
				'rain':'30'
			},
			status_data : [
                    {
                        error: false,
                        title: "發電狀態",
                        icon: "ttl_thunder",
                        text: "發電正常",
                    },
                    {
                        error: false,
                        title: "4G通訊",
                        icon: "ttl_mail",
                        text: "正常",
                    },
                    {
                        error: false,
                        title: "DMY",
                        icon: "ttl_time",
						// 輸入dmy
                        text: 0
                    },
                    {
                        error: false,
                        title: "警報數",
                        icon: "ttl_alert",
                        text: 0
                    },
                ],
			CHB_Bill_kwh:[161400,154800,198800,196000,234800,236000,260400,256400,250400,218800,207600,192000]
		};
	},
	methods: {
		drawMap(){
			let that = this
            var width = 930.16,
            height = 530,
            centered;

            // Define color scale
            // 判斷各個行政區域顏色，從#ffffff~#409a99的漸層
            var color = d3.scale.linear()
                .domain([1, 20])
                .clamp(true)
                .range(['#ffffff', '#409A99']);

            // 決定使用的投影法(mercator麥卡托投影法，用來表達正確的方位)
            // center:決定地圖中心點與放大中心的座標
            // scale:縮放倍數

            var projection = d3.geo.mercator()
                // .scale(1500)
                .scale(6000)
                // Center the Map in Colombia
                // .center([-74, 4.5])
                // Center the Map in Taiwan
                .center([121.5, 23.7])
                // .translate([width / 2, height / 2]);

            var path = d3.geo.path()
                .projection(projection);

            // Set svg width & height
            var svg = d3.select('#map_page_1')
                .attr('width', width)
                .attr('height', height);

            // Add background
            svg.append('rect')
                .attr({'fill': 'rgba(0,0,0,0)','pointer-events': 'all'})
                // .attr('class', 'background')
                .attr('width', width)
                .attr('height', height)
                .on('click', clicked);

            var g = svg.append('g');

            var effectLayer = g.append('g')
                .classed('effect-layer', true);
                // .attr({'pointer-events':'none'});

            var mapLayer = g.append('g')
				// .classed('map-layer', true);
                .attr({'fill': '#fff','stroke': '#aaa'});

            var dummyText = g.append('text')
                .classed('dummy-text', true)
                .attr({'font-size': '30px'})
                .attr('x', 0)
                .attr('y', 70)
                .style('opacity', 0);

            var bigText = g.append('text')
                // .classed('big-text', true)
                .attr({'stroke-width':'2','stroke':'#000','fill':'white','font-size': '40px', 'font-weight': '600'})
                .attr('x', 30)
                .attr('y', 60);

            // .attr("d", path) 相當於 .attr("d", function(d){return path(d);})

            // Load map data
            // Update color scale domain based on data
            // color.domain([0, d3.max(myJson.features, nameLength)]);
            // Draw each province as a path
            mapLayer.selectAll('path')//
                .data(myJson.features)//
                .enter()//
                .append('path')//
                .attr('d', path)//
                .attr('vector-effect', 'non-scaling-stroke')
                .style('fill', fillFn)
                .on('mouseover', mouseover)
                .on('mouseout', mouseout)
                .on('click', clicked);
            // Get province name
            // condition ? exprIfTrue : exprIfFalse
            // if d && d.properties, 如果true 執行前面，如果false執行後面
            // 只有11 = 1
            function nameFn(d){
                // console.log(d && d.properties ? d.properties.NOMBRE_DPT : null)
                return d && d.properties ? d.properties.NOMBRE_DPT : null;
            }

            // Get province name length
            function nameLength(d){
                var n = nameFn(d);
                return n ? n.length : 0;
            }

            // Get province color
            function fillFn(d){
				if (d.properties.NOMBRE_DPT =='屏東縣'){
					return color(30);
				}
                return color(nameLength(d));
            }

            // When clicked, zoom in
            function clicked(d) {
				var target = that.county_clicked
				var target_json = JSON.parse(JSON.stringify(target))
				if (d == undefined){
					that.county_clicked = {'place_click':'space'}
				} else{
					if (target_json.place_click == 'space'){
						d['place_click'] = d.properties.NOMBRE_DPT
						that.county_clicked = d
					} else if (target_json.properties.NOMBRE_DPT == d.properties.NOMBRE_DPT){
						that.county_clicked = {'place_click':'space'}
					} else if (target_json.properties.NOMBRE_DPT != d.properties.NOMBRE_DPT){
						d['place_click'] = d.properties.NOMBRE_DPT
						that.county_clicked = d
					}
				}
                var x, y, k;

            // Compute centroid of the selected path
                if (d && centered !== d) {
                    var centroid = path.centroid(d);
                    x = centroid[0];
                    y = centroid[1];
                    k = 4;
                    centered = d;
                } else {
                    x = width / 2;
                    y = height / 2;
                    k = 1;
                    centered = null;
                }

            // Highlight the clicked province
			mapLayer.selectAll('path')
                    .style('fill', function(d){return centered && d===centered ? 'rgba(210,160,255,0.8)' : fillFn(d);});

            // Zoom
                g.transition()
                    .duration(750)
                    .attr('transform', 'translate(' + width / 2 + ',' + height / 2 + ')scale(' + k + ')translate(' + -x + ',' + -y + ')');
            }

            function mouseover(d){
            // Highlight hovered province
                d3.select(this).style('fill', 'rgba(158,120,191,0.8)');

            // Draw effects
                textArt(nameFn(d));
            }

            function mouseout(d){
            // Reset province color
                mapLayer.selectAll('path')
                    .style('fill', function(d){return centered && d===centered ? 'rgba(210,160,255,0.8)' : fillFn(d);});

            // Remove effect text
                effectLayer.selectAll('text').transition()
                    .style('opacity', 0)
                    .remove();

            // Clear province name
                bigText.text('');
            }

            // Gimmick
            // Just me playing around.
            // You won't need this for a regular map.

            var BASE_FONT = "'Helvetica Neue', Helvetica, Arial, sans-serif";

            var FONTS = [
                "Open Sans",
                "Josefin Slab",
                "Arvo",
                "Lato",
                "Vollkorn",
                "Abril Fatface",
                "Old StandardTT",
                "Droid+Sans",
                "Lobster",
                "Inconsolata",
                "Montserrat",
                "Playfair Display",
                "Karla",
                "Alegreya",
                "Libre Baskerville",
                "Merriweather",
                "Lora",
                "Archivo Narrow",
                "Neuton",
                "Signika",
                "Questrial",
                "Fjalla One",
                "Bitter",
                "Varela Round"
            ];

            function textArt(text){
            // Use random font
                var fontIndex = Math.round(Math.random() * FONTS.length);
                var fontFamily = FONTS[fontIndex] + ', ' + BASE_FONT;

                bigText
                    .style('font-family', fontFamily)
                    .text(text);

            // Use dummy text to compute actual width of the text
            // getBBox() will return bounding box
                dummyText
                    .style('font-family', fontFamily)
                    .text(text);
                var bbox = dummyText.node().getBBox();

                var textWidth = bbox.width;
                var textHeight = bbox.height;
                var xGap = 3;
                var yGap = 1;

            // Generate the positions of the text in the background
                var xPtr = 0;
                var yPtr = 0;
                var positions = [];
                var rowCount = 0;
                while(yPtr < height){
                    while(xPtr < width){
                    var point = {
                        text: text,
                        index: positions.length,
                        x: xPtr,
                        y: yPtr
                    };
                    var dx = point.x - width/2 + textWidth/2;
                    var dy = point.y - height/2;
                    point.distance = dx*dx + dy*dy;

                    positions.push(point);
                    xPtr += textWidth + xGap;
                    }
                    rowCount++;
                    xPtr = rowCount%2===0 ? 0 : -textWidth/2;
                    xPtr += Math.random() * 10;
                    yPtr += textHeight + yGap;
                }

                var selection = effectLayer.selectAll('text')
                    .data(positions, function(d){return d.text+'/'+d.index;});

            // Clear old ones
                selection.exit().transition()
                    .style('opacity', 0)
                    .remove();

            // Create text but set opacity to 0
                selection.enter().append('text')
                    .text(function(d){return d.text;})
                    .attr('x', function(d){return d.x;})
                    .attr('y', function(d){return d.y;})
                    .style('font-family', fontFamily)
                    .style('fill', '#777')
                    .style('opacity', 0);

                selection
                    .style('font-family', fontFamily)
                    .attr('x', function(d){return d.x;})
                    .attr('y', function(d){return d.y;});

            // Create transtion to increase opacity from 0 to 0.1-0.5
            // Add delay based on distance from the center of the <svg> and a bit more randomness.
                selection.transition()
                    .delay(function(d){
                    return d.distance * 0.01 + Math.random()*1000;
                    })
                    .style('opacity', function(d){
                    return 0.1 + Math.random()*0.4;
                    });
            }
        },
		plot_panel3() {
			const MyPlot = document.getElementById("plot_3");
			MyPlot.innerHTML = "";
			function Sumdata(arr) {
				var sum = 0;
				for (var i = 0; i < arr.length; i++) {
					sum += arr[i];
				}
				return sum;
			}
			var annualTransferVolume = Sumdata(this.stationData.CHB_Bill_kwh)
			var annualLeftKwh = Sumdata(this.stationData.CHB_left_kwh)
			var endData = [];
			
			// trace of 憑證數量
			var trace1 = {
				x:['憑證數量'],
				y:[this.stationData.CHB_Bill_kwh[9] / 1000],
				type:'bar',
				name:'憑證數量',
				xaxis: 'x1',
				yaxis: 'y1',
				marker: {
					size: 8,
					color: "rgba(0,255,255,0.8)"
				},
				width:0.2
			}
			// trace of co2減量
			var trace2 = {
				x:['CO2減量'],
				y:[this.stationData.CHB_Bill_kwh[9] * 0.554],
				type:'bar',
				name:'CO2減量',
				xaxis: 'x2',
				yaxis: 'y2',
				marker: {
					size: 8,
					color: "rgba(12,232,170,0.8)"
				},
				width:0.2
			}
			// trace of 轉供電量、餘電量、月發電量
			var trace32 = {
				x:['轉供電量'],
				y:[this.stationData.CHB_left_kwh[9]],
				// y:[this.stationData.CHB_Bill_kwh[9]],
				type:'bar',
				name:'轉供電量',
				xaxis: 'x3',
				yaxis: 'y3',
				marker: {
					size: 8,
					color: "rgba(13,128,255,0.8)"
				},
				width:0.2
			}
			var trace33 = {
				x:['餘電量'],
				// y:[this.stationData.CHB_left_kwh[9]],
				y:[this.stationData.CHB_Bill_kwh[9]],
				type:'bar',
				name:'餘電量',
				xaxis: 'x3',
				yaxis: 'y3',
				marker: {
					size: 8,
					color: "rgba(12,174,232,0.8)"
				},
				width:0.2
			}
			var trace31 = {
				x:['月發電量'],
				y:[this.stationData.kwh_whole_year[9]],
				type:'bar',
				name:'月發電量',
				xaxis: 'x3',
				yaxis: 'y3',
				marker: {
					size: 8,
					color: "rgba(12,174,232,0.8)"
				},
				width:0.2
			}

			var data = [trace1, trace2, trace31, trace32, trace33]

			var layout = {
				title: {
					text: '發電量、轉供電量、餘電量、憑證、CO2減量',
					font: {
						family: "Courier New, monospace",
						size: 24,
						color:'#ffffff'
					},
				},
				xaxis: {
					domain: [0, 0.45],
					anchor: 'y1'
				},
				yaxis: {
					domain: [0, 0.45],
					anchor: 'x1',
					"gridcolor":"rgba(224,224,224,0.5)"
				},
				xaxis2: {
					domain: [0.55, 1],
					anchor: 'y2',
				},
				yaxis2: {
					domain: [0, 0.45],
					anchor: 'x2',
					"gridcolor":"rgba(224,224,224,0.5)"
				},
				xaxis3: {
					domain: [0, 1],
					anchor: 'y3'
				},
				yaxis3: {
					domain: [0.5, 1],
					anchor: 'x3',
					"gridcolor":"rgba(224,224,224,0.5)"
				},
				width:648.75,
				height:540,
				margin: {
					l: 60,
					r: 20,
					b: 40,
					t: 70,
					pad: 10
				},
				bargap:0.1,
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
			this.Plotly.newPlot(MyPlot, data, layout, config)
			// 繪圖的函數，輸入一：MyPlot(應該是要在哪裡繪圖)，輸入二：上面的兩個data.push，輸入三：上面設定的輸出樣式
			// this.Plotly.newPlot(MyPlot, initialData, layout, config)
			// this.Plotly.animate(MyPlot,{data:endData},{animationConfig});
		},
		plot_today() {
            const MyPlot = document.getElementById('plot_today')
            MyPlot.innerHTML = ""
            // 力暘展示用
			if(this.station_selected == '天權'){
				console.log('plot 天權')
				var kwh = this.stationData.plot_today_kwh_dict.天權.kwh
				var time = this.stationData.plot_today_kwh_dict.天權.time
			}else if(this.station_selected == '玉衡'){
				console.log('plot 玉衡')
				var kwh = this.stationData.plot_today_kwh_dict.玉衡.kwh
				var time = this.stationData.plot_today_kwh_dict.天權.time
			}
            var data = []
            data.push({
                x:time,
                y:kwh,
                type:'bar',
                marker: {
					size: 8,
					color: '#93FF93'
				},
            })
            
            var layout = {
                paper_bgcolor: 'rgba(0,0,0,0)',
				plot_bgcolor: 'rgba(0,0,0,0)',
                width:308.38,
				height:230,
                margin: {
					l: 60,
					r: 20,
					b: 40,
					t: 25,
					pad: 10
				},
                title: {
                    text: this.$i18n.t("plot.今日發電量"),
                    font: {
						family: " STHeiti,Copperplate,Courier New",
						size: 15,
						color:'#ffffff'
					},
                },
                yaxis: {
                    title: {
                        text: this.$i18n.t("plot.發電量")+"(kWh)",
                        font:{
							color:'#ffffff',
							family: "STHeiti,Copperplate,Courier New",
					},
                    },
                    "gridcolor":"rgba(224,224,224,0.5)",
                    rangemode: 'nonnegative',
                },
                autoMargin: true,
            }
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
            this.Plotly.newPlot(MyPlot, data, layout, config)
            this.loading = false
        },
		async getPostData(){
			this.loading = true
			await this.axios.post('/setting/ysolar_test', {
				'test':'test'
            }).then(data => {
				this.stationData = data.data.data
				console.log(this.stationData)
				this.drawMap();
				this.plot_panel3();
				this.plot_today();
            })
			this.loading = false
		}	
	},
	watch: {
		station_selected:{
			handler:function(){
				this.loading = true;
				console.log(this.station_selected);
				this.Plotly.purge('plot_today');
				this.plot_today();
				this.loading = false;
			}
		},
		county_clicked:{
			handler:function(){
				var noProxy = this.county_clicked
				var noProxy_json = JSON.parse(JSON.stringify(noProxy))
				console.log('change detected', noProxy_json)
				if (noProxy_json.place_click =='space') {
					console.log('space')
				} else if (noProxy_json.place_click =='屏東縣'){
					console.log('屏東縣')
				} else {
					console.log('other county')
				}
		},
		deep: true
		}
	},
	mounted() {
		this.getPostData();
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

/* 面板背景 */
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

/* plot框框 */
.stbigimg {
	position: relative;
	max-width: 100%;
	max-height : 100%;
	border-radius: 1rem;
	/* box-shadow: 0 0 15px #dee4ea; */
	overflow: hidden;
	background-color: rgba(0,0,0,0);
}

.table_header_style{
	background-color: rgba(0,0,0,0);
	color: white
}

.table_content_style{
	background-color: rgba(0,0,0,0);
	color: white
}

.counties {
	fill:#33474e;
}
.counties :hover {
	fill: #7f9ca7;
	transition: 0.5s;
}
.county-borders {
	fill: none;
	stroke: #fff;
	stroke-width: 0.5px;
}
/* ==============================================================以下為台灣地圖style============================================================== */
@import url(https://fonts.googleapis.com/css?family=Open+Sans+Condensed:300|Josefin+Slab|Arvo|Lato|Vollkorn|Abril+Fatface|Old+Standard+TT|Droid+Sans|Lobster|Inconsolata|Montserrat|Playfair+Display|Karla|Alegreya|Libre+Baskerville|Merriweather|Lora|Archivo+Narrow|Neuton|Signika|Questrial|Fjalla+One|Bitter|Varela+Round);

.background {
  fill: rgba(0,0,0,0);
  pointer-events: all;
}

.map-layer {
  fill: #fff;
  stroke: #aaa;
  stroke-width: '1px';
}

.effect-layer{
  pointer-events:none;
}

text{
  font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif;
  font-weight: 300;
}

text.big-text{
  font-size: 30px;
  font-weight: 400;
}

.effect-layer text, text.dummy-text{
  font-size: 12px;
}
/* ==============================================================以下為overview style============================================================== */
.statab_status{
    flex-direction: row;
	background-color: #ffffff;
}
.statab_status>div{
    position: relative;
    border-right: 1px solid #555657;
    border-bottom: 1px solid #4e5052;
}
.statab_status>div:nth-child(2){
    border-right: 0;
}
.statab_status>div:nth-child(3){
    border-bottom: 0;
}
.statab_status>div:nth-child(4){
    border-right: 0;
    border-bottom: 0;
}
.weather_card{
	background-color: #ffffff;
}
/* ==============================================================scroll bar style============================================================== */
/* width */
::-webkit-scrollbar {
	width: 5px;
	height: 5px;
	border-radius:5px;
}
/* Track */
::-webkit-scrollbar-track {
	background: rgb(17, 18, 114);
}

/* Handle */
::-webkit-scrollbar-thumb {
	background: rgb(50, 94, 218);
}

/* Handle on hover */
::-webkit-scrollbar-thumb:hover {
	background: #1e4972;
}
</style>