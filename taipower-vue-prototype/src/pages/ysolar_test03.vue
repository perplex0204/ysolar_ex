<template>
	<div class="card p-4" id="card" v-loading="loading" element-loading-background="rgba(3, 19, 39, 0.8)">
		<div class="container-fluid">
			<div class="row">
                <div class="col-sm-3">
                    <div class="box" style="--c:#062d63;--w:10px;--b:3px">
						<div style="background-image: radial-gradient(rgb(12,47,90),rgb(3,19,39))">
							<div class="panel panel-primary">
								<div class="panel-heading"></div>
								<div class="panel-body" style="height: 120px;">
                                    <div class="row align-middle justify-content-center" style="height:100%;">
										<div class="row justify-content-center col-sm-4" style="height:100%;">
											<span id="icon" style="color:white;" class="colorIcon fs-1 align-self-center text-center fas fa-charging-station mx-auto"></span>
										</div>
										<div class="row justify-content-center col-sm-8" style="height:100%;">
											<span style="color:white " class="fs-3 align-self-end text-center mx-auto">案場總建置容量<el-divider style="--el-border-style:solid;margin-top: 0px;margin-bottom: 0px;"></el-divider></span>
											<span style="color:white" class="fs-3 align-self-start text-center mx-auto">48.974MW</span>
										</div>
									</div>
								</div>
								<div class="panel-footer"></div>
							</div>
						</div>
					</div>
                </div>
                <div class="col-sm-3">
                    <div class="box" style="--c:#062d63;--w:10px;--b:3px">
						<div style="background-image: radial-gradient(rgb(12,47,90),rgb(3,19,39))">
							<div class="panel panel-primary">
								<div class="panel-heading"></div>
                                <!-- 案場總累計發電量 -->
								<div class="panel-body" style="height: 120px;">
                                    <div class="row align-middle justify-content-center" style="height:100%;">
										<div class="row justify-content-center col-sm-4" style="height:100%;">
											<span id="icon" style="color:white;" class="colorIcon fs-1 align-self-center text-center fa-solid fa-bolt mx-auto"></span>
										</div>
										<div class="row justify-content-center col-sm-8" style="height:100%;">
											<span style="color:white " class="fs-3 align-self-end text-center mx-auto">案場累計發電量<el-divider style="--el-border-style:solid;margin-top: 0px;margin-bottom: 0px;"></el-divider></span>
											<span style="color:white" class="fs-3 align-self-start text-center mx-auto">{{stationData.get_data_done?stationData.kwh_history:'0'}}MW</span>
										</div>
									</div>
								</div>
								<div class="panel-footer"></div>
							</div>
						</div>
					</div>
                </div>
                <div class="col-sm-3">
                    <div class="box" style="--c:#062d63;--w:10px;--b:3px">
						<div style="background-image: radial-gradient(rgb(12,47,90),rgb(3,19,39))">
							<div class="panel panel-primary">
								<div class="panel-heading"></div>
                                <!-- 案場總電站數 -->
								<div class="panel-body" style="height: 120px;">
                                    <div class="row align-middle justify-content-center" style="height:100%;">
										<div class="row justify-content-center col-sm-4" style="height:100%;">
											<span id="icon" style="color:white;" class="colorIcon fs-1 align-self-center text-center fa-solid fa-solar-panel mx-auto"></span>
										</div>
										<div class="row justify-content-center col-sm-8" style="height:100%;">
											<span style="color:white " class="fs-3 align-self-end text-center mx-auto">案場總電站數<el-divider style="--el-border-style:solid;margin-top: 0px;margin-bottom: 0px;"></el-divider></span>
											<span style="color:white" class="fs-3 align-self-start text-center mx-auto">2座</span>
										</div>
									</div>
								</div>
								<div class="panel-footer"></div>
							</div>
						</div>
					</div>
                </div>
                <div class="col-sm-3">
                    <div class="box" style="--c:#062d63;--w:10px;--b:3px">
						<div style="background-image: radial-gradient(rgb(12,47,90),rgb(3,19,39))">
							<div class="panel panel-primary">
								<div class="panel-heading"></div>
                                <!-- 案場總累計減碳量 -->
								<div class="panel-body" style="height: 120px;">
                                    <div class="row align-middle justify-content-center" style="height:100%;">
										<div class="row justify-content-center col-sm-4" style="height:100%;">
											<span id="icon" style="color:white;" class="colorIcon fs-1 align-self-center text-center fa-solid fa-fire-flame-simple mx-auto"></span>
										</div>
										<div class="row justify-content-center col-sm-8" style="height:100%;">
											<span style="color:white " class="fs-3 align-self-end text-center mx-auto">案場累計減碳量<el-divider style="--el-border-style:solid;margin-top: 0px;margin-bottom: 0px;"></el-divider></span>
											<span style="color:white" class="fs-3 align-self-start text-center mx-auto">{{stationData.get_data_done?stationData.co2_reduce:'0'}}KG</span>
										</div>
									</div>
								</div>
								<div class="panel-footer"></div>
							</div>
						</div>
					</div>
                </div>
			</div>
            <el-divider class="divider"></el-divider>
            <div class="row">
                <div class="col-sm-2">
                    <div class="box" style="--c:#062d63;--w:10px;--b:3px">
						<div style="background-image: radial-gradient(rgb(12,47,90),rgb(3,19,39))">
							<div class="panel panel-primary">
								<div class="panel-heading"></div>
                                <!-- 案場發電量/裝置量總覽 -->
								<div class="panel-body" style="overflow-y: auto;">
									<div class="text-center" style="padding-top:12px;">
                                        <span class="fs-3" style="color:white;">案場發電狀態</span>
                                    </div>
                                    <div style="height: 650px;">
										<div class="stbigimg shadow">
											<div id="plot_panel_month01" @click="month01_click"></div>
										</div>
										<div class="stbigimg shadow">
											<div id="plot_panel_month02"></div>
										</div>
                                    </div>
								</div>
								<div class="panel-footer"></div>
							</div>
						</div>
					</div>
                </div>
				<div class="col-sm-6">
                    <div class="box" style="--c:#062d63;--w:10px;--b:3px">
						<div style="background-image: radial-gradient(rgb(12,47,90),rgb(3,19,39))">
							<div class="panel panel-primary">
								<div class="panel-heading"></div>
                                <!-- 台灣地圖兼互動式視窗 -->
								<div class="panel-body">
                                    <div>
										<svg id="map_page_3" style=""></svg>
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
								<div class="panel-heading"></div>
                                <!-- 案場即時總發電曲線 -->
								<div class="panel-body">
                                    <div class="stbigimg shadow">
										<div id="plot_mid_1"></div>
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
                                <!-- DMY區間統計 -->
								<div class="panel-body">
                                    <div class="stbigimg shadow">
										<div id="plot_right_1"></div>
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
								<div class="panel-heading"></div>
                                <!-- PR區間統計 -->
								<div class="panel-body">
                                    <div class="stbigimg shadow">
										<div id="plot_right_2"></div>
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
								<div class="panel-heading"></div>
                                <!-- 各區運轉狀態統計 -->
								<div class="panel-body">
                                    <div style="">
                                        <div class="col-6 col-lg-12 responsive_table">
                                            <div style="height: 180px;overflow-y: scroll;">
                                                <div class="w-100 row responsive_table_header fw-bold m-0 d-none d-lg-flex flex-nowrap">
                                                    <div class="col-3 text-center table_header_style">
                                                        <label class="fs-6">電站名稱</label>
													</div>
                                                    <div class="col-3 text-center table_header_style">
                                                        <label class="fs-6">電站容量</label>
                                                    </div>
                                                    <div class="col-3 text-center table_header_style">
                                                        <label class="fs-6">運轉狀態</label>
                                                    </div>
                                                    <div class="col-3 text-center table_header_style">
                                                        <label class="fs-6">通訊狀態</label>
                                                    </div>
                                                </div>
                                                <div>
                                                    <!-- 設定body -->
                                                    <div class="w-100 responsive_table_body"  v-if="this.stationData.get_data_done">
                                                        <div class="row m-0 responsive_table_content mt-2 mt-lg-0 pt-2 pb-3 p-lg-0 " 
                                                            v-for="(item, key) in this.stationData.data" :key="key">
                                                            <div class="col-12 col-lg-3 pt-lg-4 pb-lg-4 ">
                                                                <div class="d-flex d-lg-none">
                                                                    <label class="fs-6">{{  key  }}</label>
                                                                </div>
                                                                <label class="fs-6 w-100 text-center d-none d-lg-block">{{  key 
                                                                }}</label>
                                                            </div>
                                                            <div class="col-12 col-lg-3 pt-lg-4 pb-lg-4">
                                                                <div class="d-flex d-lg-none">
                                                                    <label class="fs-6">{{  item.capacity  }}</label>
                                                                </div>
                                                                <label class="fs-6 w-100 text-center d-none d-lg-block">{{item.capacity}}MW</label>
                                                            </div>
                                                            <div class="col-12 col-lg-3 pt-lg-4 pb-lg-4">
                                                                <div class="d-flex d-lg-none">
                                                                    <label class="fs-6">{{  item.status  }}</label>
                                                                </div>
                                                                <label class="fs-6 w-100 text-center d-none d-lg-block">{{  item.status }}</label>
                                                            </div>
                                                            <div class="col-12 col-lg-3 pt-lg-4 pb-lg-4">
                                                                <div class="d-flex d-lg-none">
                                                                <label class="fs-6">{{  item.communicate_status  }}</label>
                                                                </div>
                                                                <label class="fs-6 w-100 text-center d-none d-lg-block">{{  item.communicate_status }}</label>
                                                            </div>
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
	</div>
</template>

<script>
import * as d3 from 'd3'
import myJson from '../components/ysolar_test/twCounty2010geo.json'

export default {
    name: "ysolarTest03",
	components: {
	},
	data() {
		return {
			loading:true,
			stationData:{get_data_done:false},
			county_clicked:{'place_click':'space'},
            collectionData:[
                {
                    name:'上萬安段',
                    capacity:1884.18,
                    status:'正常',
                    communication:'正常'
                },
                {
                    name:'上萬安段',
                    capacity:1884.18,
                    status:'正常',
                    communication:'正常'
                },
                {
                    name:'上萬安段',
                    capacity:1884.18,
                    status:'正常',
                    communication:'正常'
                }
            ],
			CHB_Bill_kwh:[161400,154800,198800,196000,234800,236000,260400,256400,250400,218800,207600,192000]
		};
	},
	methods: {
        drawMap(){
			let that = this

            var width = 784.5,
            height = 480,
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
                .scale(6300)
                // Center the Map in Colombia
                // .center([-74, 4.5])
                // Center the Map in Taiwan
                .center([121.2, 23.6])
                // .translate([width / 2, height / 2]);

            var path = d3.geo.path()
                .projection(projection);

            // Set svg width & height
            var svg = d3.select('#map_page_3')
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
				.classed('map-layer', true);
                // .attr({'fill': '#fff','stroke': '#aaa'});

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

			var timer = 0
            // When clicked, zoom in
            function clicked(d) {
				// 判斷選取之縣市
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
		// 電力供需現況
        plot_mid_1() {
			const MyPlot = document.getElementById("plot_mid_1");
			MyPlot.innerHTML = "";
			var endData = [];
			endData.push({
					type: "bar",
					x: ['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec'],
					y: this.stationData.CHB_Bill_kwh,
					name: '用電量1',
					yaxis: "y",
					marker: {
						size: 8,
						color: "rgba(71,179,157,0.8)"

					},
				});
			endData.push({
				type: "bar",
				x: ['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec'],
				y: [0,0,0,0,0,0,0,0,0,0,0,0],
				name: '用電量2',
				yaxis: "y",
				marker: {
					size: 8,
					color: "rgba(153,255,235,0.8)"
				},
			});
			endData.push({
				type: "scatter",
				x: ['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec'],
				y: this.stationData.kwh_whole_year,
				name: '發電量',
				yaxis: "y",
				marker: {
					size: 8,
					color: 'rgba(191,152,238,0.8)'
				},
			});

			var initialData=[
			{
				type: "bar",
				x: ['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec'],
				y: [0,0,0,0,0,0,0,0,0,0,0,0],
				name: '用電量1',
				yaxis: "y",
				marker: {
						size: 8,
						color: "rgba(71,179,157,0.8)"
				},
			},
			{
				type: "bar",
				x: ['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec'],
				y: [0,0,0,0,0,0,0,0,0,0,0,0],
				name: '用電量2',
				yaxis: "y",
				marker: {
					size: 8,
					color: "rgba(153,255,235,0.8)"
				},
			},
			{
				type: "scatter",
				x: ['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec'],
				y: [0,0,0,0,0,0,0,0,0,0,0,0],
				name: '發電量',
				yaxis: "y",
				marker: {
					size: 8,
					color: 'rgba(191,152,238,0.8)'
				},
			}
			]

			var layout = {
				barmode: 'stack',
				// title = 上面的that.name
				title: {
				text: '電力供需現況',
				font: {
					family: " STHeiti,Coppe,Courier New",
					size: 18,
					color:'#ffffff'
				},
				},
				height:180,
				margin: {
					l: 60,
					r: 0,
					b: 60,
					t: 50,
					pad: 10
				},
				// x軸樣式
				xaxis: {
					title: {
						text: "time",
						font:{
							color:'#ffffff',
							family: "STHeiti,Copperplate,Courier New",
						},
					},
					range:[-1,12]
				},
				// y軸樣式
				yaxis: {
					title: {
						text: "kWh",
						font:{
							color:'#ffffff',
							family: "STHeiti,Copperplate,Courier New",
						},
					},
					gridcolor:"rgba(224,224,224,0.5)",
					range:[0,5000000]
				},
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
        plot_right_1() {
			const MyPlot = document.getElementById("plot_right_1");
			MyPlot.innerHTML = "";
			// color如果沒有指定色碼的話就會直接隨機

			var endData = [];
			endData.push({
					type: "bar",
					x: ['0~1','1~2','2~3','3~4','4~5','5~6'],
					y: this.stationData.dmy_list,
					name: '案場數量',
					yaxis: "y",
					marker: {
						size: 8,
						color: "rgba(0,255,255,0.8)"
					},
				});

			var initialData=[
			{
				type: "bar",
				x: ['0~1','1~2','2~3','3~4','4~5','5~6'],
				y: [0,0,0,0,0,0],
				name: '案場數量',
				yaxis: "y",
				marker: {
						size: 8,
						color: "rgba(0,255,255,0.8)"
				},
			}
			]

			var layout = {
				barmode: 'stack',
				// title = 上面的that.name
				title: {
				text: 'DMY區間統計',
				font: {
					family: " STHeiti,Coppe,Courier New",
					size: 18,
					color:'#ffffff'
				},
				},
				height:213,
				margin: {
					l: 60,
					r: 30,
					b: 60,
					t: 50,
					pad: 10
				},
				// x軸樣式
				xaxis: {
					title: {
						text: "DMY區間",
						font:{
							color:'#ffffff',
							family: "STHeiti,Copperplate,Courier New",
						},
					},
					range:[-1,6]
				},
				// y軸樣式
				yaxis: {
					title: {
						text: "案場數量(個)",
						font:{
							color:'#ffffff',
							family: "STHeiti,Copperplate,Courier New",
						},
					},
					gridcolor:"rgba(224,224,224,0.5)",
					range:[0,3]
				},
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
			this.Plotly.newPlot(MyPlot, initialData, layout, config);
			this.Plotly.animate(MyPlot,{data:endData},{animationConfig});
		},
        plot_right_2() {
			const MyPlot = document.getElementById("plot_right_2");
			MyPlot.innerHTML = "";
			// color如果沒有指定色碼的話就會直接隨機

			var endData = [];
			endData.push({
					type: "bar",
					x: ['0~10','11~20','21~30','31~40','41~50','51~60','61~70','71~80','81~90','91~100'],
					y: this.stationData.pr_list,
					name: '用電量1',
					yaxis: "y",
					marker: {
						size: 8,
						color: "rgba(0,255,255,0.8)"
					},
				});

			var initialData=[
			{
				type: "bar",
				x: ['0~10','11~20','21~30','31~40','41~50','51~60','61~70','71~80','81~90','91~100'],
				y: [0,0,0,0,0,0,0,0,0,0],
				name: '用電量1',
				yaxis: "y",
				marker: {
						size: 8,
						color: "rgba(0,255,255,0.8)"
				},
			}
			]

			var layout = {
				barmode: 'stack',
				// title = 上面的that.name
				title: {
				text: 'PR區間統計',
				font: {
					family: " STHeiti,Coppe,Courier New",
					size: 18,
					color:'#ffffff'
				},
				},
				height:213,
				margin: {
					l: 60,
					r: 30,
					b: 60,
					t: 50,
					pad: 10
				},
				// x軸樣式
				xaxis: {
					title: {
						text: "PR區間統計",
						font:{
							color:'#ffffff',
							family: "STHeiti,Copperplate,Courier New",
						},
					},
					range:[-1,12]
				},
				// y軸樣式
				yaxis: {
					title: {
						text: "案場數量(個)",
						font:{
							color:'#ffffff',
							family: "STHeiti,Copperplate,Courier New",
						},
					},
					gridcolor:"rgba(224,224,224,0.5)",
					range:[0,3]
				},
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
			this.Plotly.newPlot(MyPlot, initialData, layout, config);
			this.Plotly.animate(MyPlot,{data:endData},{animationConfig});
		},
		// 天權發電量
		plot_panel_month01() {
			if(this.stationData.get_data_done)
			{
				const MyPlot = document.getElementById("plot_panel_month01");
				MyPlot.innerHTML = "";
				// 取得現在時間，到時候拿hour-1當作index
				var hour = new Date().getHours()
				if (this.stationData.data.天權.kwh[hour-1] == undefined){
					var kwh = 0
				}else{
					var kwh = this.stationData.data.天權.kwh[hour-1].value
				}
				var capacity = this.stationData.data.天權.capacity
				var display_capacity = capacity - kwh
				if (this.stationData.data.天權.dmy[hour-1] == undefined){
					var display_dmy = 0
				}else{
					var display_dmy = Math.round(this.stationData.data.天權.dmy[hour-1].value * 100)/100
				}
				var endData = [];
				endData.push({
						type: "pie",
						values: [kwh,display_capacity],
						// name: this.$i18n.t("plot.實際輸出功率"),
						labels: ['發電量','離最大發電量'],
						marker: {
							size: 8,
							colors: ["rgba(0,255,255,0.8)","rgba(149,156,150,0.8)"]
						},
						text:['test'],
						textinfo: "none",
						textposition: "outside",
						textfont:{
							color:'#ffffff'
						},
						hole:.85
					});

				var layout = {
					// title = 上面的that.name
					annotations: [
					{
						font: {
							size: 20,
							color:'#ffffff'
						},
						showarrow: false,
						text:'天權<br>'+display_dmy+'%',
						x: 0.5,
						y: 0.5
					}],
					height:216,
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
			}
		},
		// 玉衡發電量
		plot_panel_month02() {
			if(this.stationData.get_data_done)
			{
				const MyPlot = document.getElementById("plot_panel_month02");
				MyPlot.innerHTML = "";
				var hour = new Date().getHours()
				if (this.stationData.data.玉衡.kwh[hour-1] == undefined){
					var kwh = 0
				}else{
					var kwh = this.stationData.data.玉衡.kwh[hour-1].value
				}
				var capacity = this.stationData.data.玉衡.capacity
				var display_capacity = capacity - kwh
				if (this.stationData.data.玉衡.dmy[hour-1] == undefined){
					var display_dmy = 0
				}else{
					var display_dmy = Math.round(this.stationData.data.玉衡.dmy[hour-1].value * 100)/100
				}
				var endData = [];
				var endData = [];
				endData.push({
						type: "pie",
						values: [kwh,display_capacity],
						// name: this.$i18n.t("plot.實際輸出功率"),
						labels: ['發電量','容量'],
						marker: {
							size: 8,
							colors: ["rgba(0,255,255,0.8)","rgba(149,156,150,0.8)"]
						},
						textinfo: "none",
						textposition: "outside",
						textfont:{
							color:'#ffffff'
						},
						hole:.85
					});

				var layout = {
					// title = 上面的that.name
					annotations: [
					{
						font: {
							size: 18,
							color:'#ffffff'
						},
						showarrow: false,
						text:'玉衡<br>'+display_dmy+'%',
						x: 0.5,
						y: 0.5
					}],
					height:216,
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
			}
		},
		async getPostData() {
			this.loading = true
			await this.axios.post('/setting/ysolar_test', {
			}).then(data => {
				console.log(data.data.data);
				this.stationData = data.data.data;
				this.draw_plotly();
				this.loading = false;
			}).catch((error)=>{
				console.log(error)
			})
		},
		draw_plotly(){
			this.plot_mid_1();
			this.plot_right_1();
			this.plot_right_2();
			this.plot_panel_month01();
			this.plot_panel_month02();
		},
		month01_click(){
			window.open("https://www.w3schools.com");
		}
	},
	watch: {
		county_clicked:{
			handler:function(){
				var noProxy = this.county_clicked
				var noProxy_json = JSON.parse(JSON.stringify(noProxy))
				console.log('change detected', noProxy_json)
				if (noProxy_json.place_click =='space') {
					this.getPostData()
				} else if (noProxy_json.place_click =='屏東縣'){
					this.getPostData()
				} else {
					this.loading = true;
					this.stationData = {'get_data_done':false};
					this.plot_mid_1();
					this.plot_right_1();
					this.plot_right_2();
					this.Plotly.purge('plot_panel_month01');
					this.Plotly.purge('plot_panel_month02');
					this.loading = false;
				}
		},
		deep: true
	}
	},
	mounted() {
		this.getPostData()
		this.drawMap();
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

.stbigimg {
	position: relative;
	max-width: 100%;
	max-height : 100%;
	border-radius: 1rem;
	/* box-shadow: 0 0 15px #dee4ea; */
	overflow: hidden;
	background-color: rgba(0,0,0,0);
}

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
/* ==============================================================以上為台灣地圖style============================================================== */

.colorIcon{
	background: -webkit-linear-gradient(rgba(255,255,255,1), rgba(49,142,255,1));
	-webkit-background-clip: text;
	-webkit-text-fill-color: transparent;
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