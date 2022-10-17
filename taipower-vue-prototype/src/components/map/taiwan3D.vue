<template>
    <div>
        <div class="tw_wrap shadow" :class="{'col-lg-8': $store.state.user_data.pageType == 'taipower'}">
            <div ref="taiwanContainer" id="taiwanContainer" :class="{ drag: switcher }"></div>
            <div class="tw_switch">
                <!-- <el-tooltip placement="bottom">
                    <div slot="content">
                        自動播放時無法操作<br />
                        平移：滑鼠右鍵<br />
                        縮放：滑鼠中間滾輪<br />
                        旋轉：滑鼠左鍵
                    </div>
                    <el-switch v-model="switcher" 
                    active-color="#FF8046" 
                    inactive-color="#FF8046" 
                    active-text="自選模式" 
                    inactive-text="播放模式" 
                    @change="switchMode"> </el-switch>
                </el-tooltip> -->
            </div>
        </div>
    </div>
</template>

<script>
import * as THREE from 'three';
import {GLTFLoader} from 'three/examples/jsm/loaders/GLTFLoader';
import {OrbitControls} from 'three/examples/jsm/controls/OrbitControls';
import { gsap } from "gsap";
// import stationJSON from '../../assets/pinpoint.json';

const GLTFmodel = "./3d/TW3D.glb";
const GLTFtexture = "./3d/texture_shadow.jpg";
const GLTFname = "./3d/twname.png";

const auto_play_transition = 5000; //自動播放轉場間隔
const update_interval = 0.03; //更新間隔秒數
const pin_point_radius = 0.07; //地圖點點半徑大小
const pin_point_effect_scale_max = 5; //編輯狀態的地圖點特效最大倍率
const pin_point_effect_speed = 100; //編輯狀態的地圖點特效的閃爍及擴散速度
const saved_pin_point_color = 0x656d74; //地圖點顏色
const temp_pin_point_color = 0x0a60ab; //編輯中的地圖點顏色
const picked_pin_point_color = 0x0a60ab; //滑鼠指到的地圖點顏色
const selected_city_color = 0x82c2fa;

// const fileLoader = new THREE.FileLoader();
const pin_point_effect_radius = pin_point_radius; //點點擴散最大半徑

// 點位
let targetPoint;
let effectRing;

let container, renderer, scene, camera, raycaster, spotLight, controls;
let mouse, sMouse;
let taiwanObj;
let rayTraceTarget = null;
let clock;
let toggle = 0.0;
let requestId = 0;

let loadedPoints;
let tempPinPoint; //尚未儲存的地圖點
let savedPinPoint = []; //已儲存的地圖點
let collidingPoint = null; //記錄碰撞到的地圖點

export default {
    name: "totalCount",
    props: {
        get3dPoints: Array,
    },
    data() {
        return {
            playIndex: -1,
            stationPoint: [],
            switcher: false,
            isLockPoint: false,
            lockPointData: null,
        };
    },
    mounted() {
        window.cusVueFunc = {};
        this.$emit('tw3d-finish')  //向parent emit
        for (var i = 0; i <= this.get3dPoints.length - 1; i++) {
            this.stationPoint.push(this.get3dPoints[i].idfor3Dpoint);
        }
        loadedPoints = this.stationPoint;
        container = this.$refs.taiwanContainer;
        this.init();
        this.animate();

        //把伸縮大小加到 Global
        window.cusVueFunc.taiwanResize = this.onWindowResize;

        setTimeout(() => {
            this.playInterval();
        }, 2000);
    },
    unmounted() {
        this.reset();
        cancelAnimationFrame(requestId);
    },
    methods: {
        switchMode() {
            this.resetMapCam();
            let twNmae = scene.children.find((el) => el.name == "twnames").material;
            if (this.switcher == false) {//播放模式
                //開始前清除當前點點樣式
                this.hidePointEffect(savedPinPoint[this.playIndex])
                
                controls.enabled = false;
                controls.enableDamping = false;
                controls.enableZoom = false;
                controls.enablePan = false;

                container.removeEventListener("click", this.onClick);

                gsap.to(twNmae, {
                    duration: 2,
                    opacity: 0,
                });
                // container.removeEventListener('pointerup', null)

            } else {//自選模式
                
                this.resetMapCam();
                container.addEventListener("mousemove", this.onMouseMove);
                container.addEventListener("click", this.onClick);
                setTimeout(() => { //動畫跑完才可以動
                    controls.enabled = true;
                    controls.enableDamping = true;
                    controls.enableZoom = true;
                    controls.enablePan = true;
                }, 2000);
                gsap.to(twNmae, {
                    duration: 2,
                    opacity: 0.7,
                });
            }
        },
        poindown() {
            if (this.switcher == true) {
                container.classList.add("dragging");
            }
        },
        poinup() {
            if (this.switcher == true) {
                container.classList.remove("dragging");
            }
        },
        reset() {
            for (var i = 1; i < 99999; i++) {
                window.clearInterval(i);
                window.clearTimeout(i);
            }
            window.removeEventListener("resize", this.onWindowResize);
            container.removeEventListener("click", this.onClick);
            this.playIndex = -1;
            container = null;
            renderer = null;
            scene = null;
            camera = null;
            raycaster = null;
            mouse = null;
            sMouse = null;
            taiwanObj = null;
            spotLight = null;
            controls = null;
            loadedPoints = null;
            rayTraceTarget = null;
            clock = null;
            toggle = 0.0;
            scene = null;
            clock = null;
            camera = null;
            raycaster = null;
            spotLight = null;
            taiwanObj = null;
            tempPinPoint = null;
            savedPinPoint = [];
            collidingPoint = null;
        },
        init() {
            //場景
            if (scene) {
                return;
            }
            container.addEventListener("pointerdown", this.poindown);
            container.addEventListener("pointerup", this.poinup);
            scene = new THREE.Scene();
            scene.background = new THREE.Color(0xcedff0);
            scene.fog = new THREE.Fog(0xcedff0, 1000, 3000); //霧化遠端

            //計時器
            clock = new THREE.Clock();

            //攝影機 (角度, 大小, )
            camera = new THREE.PerspectiveCamera(80, container.offsetWidth / container.offsetHeight, 1, 5000);
            camera.position.set(-20, -20, -20);

            //射線
            raycaster = new THREE.Raycaster();
            mouse = new THREE.Vector2();
            sMouse = new THREE.Vector2();

            //環境光
            const AmLight = new THREE.AmbientLight(0xcedff0); // soft white light
            scene.add(AmLight);

            spotLight = new THREE.SpotLight(0xcedff0, 0.1);
            // const spotLightHelper = new THREE.SpotLightHelper( spotLight );
            // scene.add( spotLightHelper );
            spotLight.position.set(0, 30, 0);
            spotLight.angle = Math.PI / 4;
            spotLight.penumbra = 1.5;
            spotLight.distance = 100;
            spotLight.shadow.camera.near = 10;
            spotLight.shadow.camera.far = 200;
            spotLight.shadow.focus = 1.5; //調整陰影模糊度，但解析度太差了
            scene.add(spotLight);

            //增加底版
            const textureLoader = new THREE.TextureLoader();
            const texttureBG = textureLoader.load(GLTFtexture);
            const groundMesh = new THREE.Mesh(
                new THREE.PlaneGeometry(100, 100),
                new THREE.MeshPhongMaterial({
                    color: 0xffffff,
                    depthWrite: true,
                    map: texttureBG,
                })
            );
            groundMesh.position.y = -2;
            groundMesh.rotation.x = -Math.PI / 2;
            scene.add(groundMesh);

            //增加地點名稱
            const nameBoard = textureLoader.load(GLTFname);
            const nameMesh = new THREE.Mesh(
                new THREE.PlaneGeometry(21, 21),
                new THREE.MeshBasicMaterial({
                    transparent: true,
                    map: nameBoard,
                })
            );
            nameMesh.position.y = 0.35;
            nameMesh.rotation.x = -Math.PI / 2;
            nameMesh.material.opacity = 0;
            nameMesh.name = "twnames";
            scene.add(nameMesh);

            // 引入台灣模型
            const loader = new GLTFLoader();

            loader.load(
                GLTFmodel,
                function(gltf) {
                    scene.add(gltf.scene); //加入台灣島地圖
                    taiwanObj = gltf.scene.children;

                    //個別加入材質
                    taiwanObj.forEach((el) => {
                        el.material = new THREE.MeshPhongMaterial({ color: 0xffffff });
                    });
                    //改外圍島嶼模型
                    taiwanObj.find((el) => (el.name = "island")).scale.y = 0.3;

                    //台灣地圖讀完接著讀取儲存的地圖點
                    loadedPoints.forEach((element) => {
                        //取得對應的縣市地圖物件
                        const _parentObj = scene.getObjectByName(element.parent);
                        if (_parentObj) {
                            //複製地圖點物件並設成黑色
                            let _loadedPoint = targetPoint.clone();
                            _loadedPoint.material = targetPoint.material.clone();
                            _loadedPoint.material.color.set(saved_pin_point_color);
                            //把點綁在縣市地圖物件下
                            _parentObj.attach(_loadedPoint);
                            //綁好之後再設定位置
                            _loadedPoint.position.x = element.position.x;
                            _loadedPoint.position.y = element.position.y;
                            _loadedPoint.position.z = element.position.z;

                            _loadedPoint.name = element.uuid;
                            _loadedPoint.userData = {
                                camPosition: element.camPosition,
                            };

                            //加到陣列中存起來
                            savedPinPoint.push(_loadedPoint);
                        }
                    });
                    document.getElementById("maploader").classList.add("loaded");
                    setTimeout(() => {
                        //增加設定選單開關大小不同
                        if (localStorage.getItem("ysolar_nav_close") == "yes") {
                            window.cusVueFunc.taiwanResize();
                        }
                        gsap.to(camera.position, {
                            duration: 3,
                            ease: "sine.out",
                            x: 0,
                            y: 30,
                            z: 20,
                        });
                    }, 1000);
                },
                // called while loading is progressing
                function(xhr) {
                    console.log((xhr.loaded / xhr.total) * 100 + "% loaded");
                },
                // called when loading has errors
                function(error) {
                    console.warn("沒讀取到 GLTF 模型", error, GLTFmodel);
                }
            );

            //設定地圖點物件資訊，初始設定為編輯中顏色
            const geometry = new THREE.CircleGeometry(pin_point_radius, 32);
            const targetPointMaterial = new THREE.MeshBasicMaterial({
                color: temp_pin_point_color,
            });
            targetPoint = new THREE.Mesh(geometry, targetPointMaterial);
            targetPoint.lookAt(0, 1, 0);
            scene.add(targetPoint);

            //目標地圖點外圈擴散特效物件資訊
            const effectRingGeometry = new THREE.CircleGeometry(pin_point_effect_radius, 32);
            const effectRingMaterial = new THREE.MeshBasicMaterial({
                color: temp_pin_point_color,
                opacity: 0.1,
                transparent: true,
            });

            effectRing = new THREE.Mesh(effectRingGeometry, effectRingMaterial);
            effectRing.lookAt(0, 1, 0);
            scene.add(effectRing);
            effectRing.visible = false;

            //渲染
            renderer = new THREE.WebGLRenderer({
                antialias: true,
            });
            renderer.shadowMap.enabled = true; //打開陰影
            renderer.setPixelRatio(window.devicePixelRatio); //畫質像素分辨率
            this.$emit('map-set-size', {
                width: container.offsetWidth,
                height: container.offsetHeight
            })
            renderer.setSize(container.offsetWidth, container.offsetHeight);
            container.appendChild(renderer.domElement);

            // controls
            controls = new OrbitControls(camera, renderer.domElement);
            // controls.mouseButtons = {
            //     ORBIT: THREE.MOUSE.RIGHT,
            //     PAN: THREE.MOUSE.LEFT
            // }
            controls.enabled = false; //開關user控制
            controls.enableDamping = false; //動畫開啟
            controls.enableZoom = false; //是否開啟縮放
            controls.enablePan = false; //是否開啟右鍵拖曳功能
            controls.dampingFactor = 0.05;
            controls.screenSpacePanning = true;
            controls.minDistance = 7;
            controls.maxDistance = 18;
            window.addEventListener("resize", this.onWindowResize);
        },
        onMouseMove(e) {
            //換算滑鼠座標
            let _leftOffset = window.innerWidth - renderer.domElement.clientWidth;
            sMouse.x = ((e.clientX - _leftOffset) / renderer.domElement.clientWidth) * 2 - 1;
            sMouse.y = -(e.clientY / renderer.domElement.clientHeight) * 2 + 1;

            mouse.x = e.clientX;
            mouse.y = e.clientY;
        },
        onWindowResize() {
            camera.aspect = container.offsetWidth / container.offsetHeight;
            camera.updateProjectionMatrix();
            this.$emit('map-set-size', {
                width: container.offsetWidth,
                height: container.offsetHeight
            })
            renderer.setSize(container.offsetWidth, container.offsetHeight);
        },
        animate() {
            requestId = requestAnimationFrame(this.animate);
            this.render();
        },
        render() {
            controls.update();

            if (this.switcher == true) {
                //自選模式
                raycaster.setFromCamera(sMouse, camera);
                const _intersects = raycaster.intersectObjects(taiwanObj);
                let _isColliding = false;
                if (_intersects.length != 0) {
                    // console.log(_intersects[0].point);
                    for (let i = 0; i < _intersects[0].object.children.length; i++) {
                        const _point = _intersects[0].object.children[i];
                        let _worldPosition = new THREE.Vector3();
                        _point.getWorldPosition(_worldPosition);
                        let _dist = _intersects[0].point.distanceTo(_worldPosition);
                        if (_dist <= pin_point_radius * 2) {
                            _isColliding = true;
                            collidingPoint = _point;
                            break;
                        }
                    }
                }

                if (this.isLockPoint) {
                    //鎖定站點狀態
                    if (!_isColliding) {
                        collidingPoint = null;
                    }
                } else {
                    if (_isColliding) {
                        //mouseover
                        this.showPointEffect(collidingPoint, picked_pin_point_color);
                        container.classList.add("hover");
                    } else {
                        container.classList.remove("hover");
                        if (collidingPoint) {
                            //mouseleave
                            this.hidePointEffect(collidingPoint);
                            collidingPoint.material.color.set(saved_pin_point_color);
                            collidingPoint = null;
                        }
                    }
                }
            }

            if (effectRing.visible) {
                // 擴散效果
                //利用三角函數圖形做特效，取0~90度轉成弧度
                let _d = Math.cos(this.degreeToRadians((clock.elapsedTime * pin_point_effect_speed) % 90));
                //換算縮放變化量
                let _scale = 1 + (pin_point_effect_scale_max - 1) * (1 - _d);
                effectRing.scale.x = _scale;
                effectRing.scale.y = _scale;
                effectRing.scale.z = _scale;
                //透明度變化
                effectRing.material.opacity = 1 - Math.abs(Math.cos(_d));

                if (effectRing.targetPoint) {
                    let _worldPosition = new THREE.Vector3();
                    effectRing.targetPoint.getWorldPosition(_worldPosition);
                    effectRing.position.copy(_worldPosition);
                }
            }

            toggle += clock.getDelta();

            renderer.render(scene, camera);
        },
        degreeToRadians(angle) {
            return angle * (Math.PI / 180);
        },
        showPointEffect(point, color) {
            point.material.color.set(color);
            //設定擴散效果
            effectRing.material.color.set(color);
            effectRing.material.depthTest = false; //避免被其他半透明物件遮住
            effectRing.visible = true;
            effectRing.targetPoint = point;
            // point.attach(effectRing);
        },
        hidePointEffect(point) {
            point.material.color.set(saved_pin_point_color);
            effectRing.visible = false;
        },
        resetMapCam() {
            taiwanObj.forEach((el) => {
                gsap.to(el.position, { duration: 0.5, y: 0 });
                gsap.to(el.material.color, { duration: 0.5, r: 1, g: 1, b: 1 });
            });
            gsap.to(controls.target, { duration: 1.5, ease: "expo.out", x: 0, y: 0, z: 0 });
            gsap.to(controls, { duration: 1.5, ease: "expo.out", maxDistance: 18 });
            gsap.to(camera.position, { duration: 3, ease: "sine.out", x: 0, y: 30, z: 20 });
        },
        //選擇後改顏色升起
        //參數，string、object、cam postiion object
        selectedChange(city, position, rayTrace) {
            const seleTar = taiwanObj.find((el) => el.name === city);
            const color = new THREE.Color(selected_city_color);
            const playTime = 1.5;

            //沒點點時，座標抓縣市
            if (position == undefined) {
                position = seleTar.position;
            }

            gsap.to(seleTar.position, { duration: 1, ease: "expo.out", y: 1 });
            gsap.to(seleTar.material.color, {
                duration: playTime,
                r: color.r,
                g: color.g,
                b: color.b,
            });

            if (rayTrace) {
                rayTraceTarget = seleTar;
                // container.addEventListener("click", AddingPinPoint);
            } else {
                rayTraceTarget = null;
            }

            //攝影機 Distance距離，target 目標座標
            gsap.to(controls, {
                duration: playTime,
                ease: "expo.out",
                maxDistance: 5,
            });
            gsap.to(controls.target, {
                duration: playTime,
                ease: "expo.out",
                x: position.x,
                y: position.y,
                z: position.z,
            });
        },
        playInterval() {
            //轉場時間不可太短
            if (auto_play_transition < 5000) {
                auto_play_transition == 5000;
            }

            setInterval(() => {
                if (!this.switcher) {
                    if (this.playIndex <= this.stationPoint.length - 2) {
                        this.playIndex += 1;
                    } else {
                        this.playIndex = 0;
                    }
                    this.playPostCard(this.playIndex)

                    //換點點
                    this.selectedChange(savedPinPoint[this.playIndex].parent.name, savedPinPoint[this.playIndex].userData.camPosition, false);
                    this.showPointEffect(savedPinPoint[this.playIndex], picked_pin_point_color);

                    //離場動畫
                    setTimeout(() => {
                        this.resetMapCam();
                        this.hidePointEffect(savedPinPoint[this.playIndex]);
                    }, auto_play_transition - 2000);
                }
            }, auto_play_transition);
        },
        //資訊表格動畫
        playPostCard(playIdx){
            let valueChange = document.getElementById("stationChange").children[0];
            let valueChild = valueChange.children;

            valueChange.classList.add("transi");
            //valueChild[playIdx].style.visibility = "visible";
            valueChild[playIdx].classList.add("active")
            //資訊表格進場
            /* setTimeout(() => {
                valueChild.forEach(function(t) {
                    t.style.display = "none";
                });
                valueChild[playIdx].style.display = "block";
            }, 1000); */

            setTimeout(() => {
                valueChange.classList.remove("transi");
                valueChild.forEach(function(t) {
                    valueChild[playIdx].classList.remove("active")
                });
            }, 3000);

        },
        onClick() {
            if (!this.isLockPoint) {
                if (collidingPoint) {
                    console.log("pick!!!");
                    this.isLockPoint = true;
                    this.showPointEffect(collidingPoint, picked_pin_point_color);
                    this.lockPointData = collidingPoint;
                }
            } else {
                if (collidingPoint) {
                    this.lockPointData.material.color.set(saved_pin_point_color);
                    this.showPointEffect(collidingPoint, picked_pin_point_color);
                    this.lockPointData = collidingPoint;
                } else {
                    this.lockPointData.material.color.set(saved_pin_point_color);
                    this.hidePointEffect(this.lockPointData);
                    this.isLockPoint = false;
                    this.lockPointData = null;
                }
            }
            //點擊切換資訊欄位
            if(collidingPoint){
                let newOrder = this.get3dPoints.findIndex(point => 
                        point.idfor3Dpoint.uuid === collidingPoint.name
                    )
                this.playPostCard(newOrder)
                this.playIndex = newOrder;
            }
        },

    },
};
</script>
