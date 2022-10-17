<template>
    <div>
        <div class="card p-2">
            <h5>
				<i class="fa-solid fa-link text-primary me-2"></i>
                Web Navigation and Access Permission Setting
			</h5>
            <div class="d-flex flex-wrap align-items-center">
                <div class="col-12 col-lg-auto me-2 mb-2">
                    <i class="fa-solid fa-rotate text-success"></i>
                    Sync With Other Server
                </div>
                <div class="col-12 col-lg-8 me-2 mb-2">
                    <el-input placeholder="MongoDB Connection String" class="w-100" size="large"
                    v-model="mongodb_url"></el-input>
                </div>
                <div class="col-12 col-lg-3 me-2 mb-2">
                    <el-input placeholder="MongoDB DB name" class="w-100" size="large" v-model="mongodb_db"></el-input>
                </div>
                <div class="ms-auto mb-2">
                    <button class="btn btn-success" @click="mongodb_connect">Connect & Download</button>
                </div>
            </div>
            <!-- <p class="mb-0 fw-light">*The connection string will be stored at parameter_setting, method: "web_nav_page_sync_mongoDB"</p> -->
            <p class="fw-light">**Ensure Firewall or VPN is set properly. Or using local network IP.</p>
            <!-- JSON Upload -->
            <el-upload
                class="upload-demo"
                action="api/web_nav_page_json_upload"
                :on-success="get_web_nav_page_data"
                :on-error="upload_error"
                accept="application/JSON"
            >
                <button class="btn btn-primary">Update JSON</button>
                <template #tip>
                    <div class="el-upload__tip">
                        Upload web_nav_link JSON file
                    </div>
                </template>
            </el-upload>
        </div>
        <div class="card p-2 mt-3" v-loading="is_loading">
            <div class="d-flex flex-wrap">
                <el-select v-model="pageType" size="large" @change="get_web_nav_page_data">
                    <el-option label="All pageType" value=""></el-option>
                    <el-option v-for="p in pageType_list" :key="p" :label="p" :value="p"></el-option>
                </el-select>
                <button class="btn btn-warning mb-2  ms-auto" @click="json_export"><i class="fa-solid fa-download"></i>Download .json</button>
            </div>
            <!-- ===================== navlink ============================ -->
            <div class="d-flex align-items-center mb-2">
                <h6 class="mt-2">Nav Link</h6>
                <button class="btn btn-warning ms-auto" @click="show_new_navLink"><i class="fa-solid fa-plus"></i></button>
            </div>
            <div class="table-responsive" style="max-height: 50vh; overflow-y: scroll;">
                <table class="table table-striped">
                    <thead class="table-light">
                        <tr>
                            <th>Route</th>
                            <th>Name</th>
                            <th>i18n</th>
                            <th>pageType</th>
                            <th>Level</th>
                            <th>Show</th>
                            <th>priority</th>
                            <th>Icon</th>
                            <th>Superuser ONLY</th>
                            <th>
                            </th>
                        </tr>
                    </thead>
                    <tbody>
                        <!-- New navlink -->
                        <tr v-if="new_navLink.display" class="bg-success bg-opacity-50">
                            <!-- route -->
                            <td><el-input v-model="new_navLink.route" size="large" placeholder="/dashboard"></el-input></td>
                            <!-- name -->
                            <td><el-input v-model="new_navLink.name" size="large" placeholder="個性化首頁"></el-input></td>
                            <!-- name_i18n -->
                            <td>
                                <el-popover
                                    width="300"
                                    trigger="click"
                                >
                                    <template #reference>
                                        <el-button size="large"><i class="fa-solid fa-globe"></i></el-button>
                                    </template>
                                    <el-form :rules="i18n_rule">
                                        <div v-for="c in Object.keys(new_navLink.name_i18n)" :key="c">
                                            <label>{{c}}</label>
                                            <el-form-item :prop="c">
                                                <el-input  v-model="new_navLink.name_i18n[c]"></el-input>
                                            </el-form-item>
                                        </div>
                                    </el-form>
                                </el-popover>
                            </td>
                            <!-- pageType -->
                            <td>
                                <el-popover 
                                    width="300"
                                    trigger="click"
                                    @hide="update_pageType(new_navLink)"
                                >
                                    <template #reference>
                                        <el-button size="large"><label v-if="new_navLink.all_pageType">All</label><i class="fa-solid fa-file" v-else></i></el-button>
                                    </template>
                                    <el-switch
                                        v-model="new_navLink.all_pageType"
                                        size="large"
                                        active-text="All"
                                        inactive-text="Specify pageType"
                                        @change="(new_val)=>{
                                             new_val ? new_navLink.pageType = 'all' : new_navLink.pageType = []
                                        }"
                                    />
                                    <div v-if="!new_navLink.all_pageType">
                                        <label class="mb-2">pageType</label>
                                        <div class="d-flex align-items-center" v-for="p,i in new_navLink.pageType" :key="i" >
                                            <el-input v-model="new_navLink.pageType[i]"></el-input>
                                            <button class="btn ms-auto text-dark" @click="()=>{
                                                new_navLink.pageType.splice(i, 1)
                                            }"><i class="fa-solid fa-trash"></i></button>
                                        </div>
                                        <el-button class="mt-2" size="large" @click="new_navLink.pageType.push('')"><i class="fa-solid fa-plus"></i></el-button>
                                    </div>
                                 </el-popover>
                            </td>
                            <!-- level -->
                            <td>
                                <el-popover 
                                    width="300"
                                    trigger="click"
                                    @hide="update_level(new_navLink)"
                                >
                                    <template #reference>
                                        <el-button size="large">{{new_navLink.all_level ? "All" : Number.isInteger(new_navLink.level) ? new_navLink.level : new_navLink.level.join(',')}}</el-button>
                                    </template>
                                    <el-switch
                                        v-model="new_navLink.all_level"
                                        size="large"
                                        active-text="All"
                                        inactive-text="Specify level"
                                        @change="(new_val)=>{
                                             new_val ? new_navLink.level = 1 : new_navLink.level = []
                                        }"
                                    />
                                    <el-checkbox-group v-model="new_navLink.level" v-if="!new_navLink.all_level">
                                        <el-checkbox :label="1" />
                                        <el-checkbox :label="2" />
                                        <el-checkbox :label="3" />
                                    </el-checkbox-group>
                                </el-popover>
                            </td>
                            <!-- show -->
                            <td>
                                <el-switch
                                    v-model="new_navLink.show"
                                    size="large"
                                    active-text="Show"
                                    inactive-text="Hide"
                                />
                            </td>
                            <!-- priority -->
                            <td>
                                <el-input-number placeholder="1" v-model="new_navLink.priority"></el-input-number>
                            </td>
                            <!-- icon -->
                            <td>
                                <el-popover 
                                    width="300"
                                    trigger="click"
                                >
                                    <template #reference>
                                        <el-button size="large" class="pt-0 pb-0"><i v-if="new_navLink.icon != ''" :class="new_navLink.icon" class="fs-4"></i></el-button>
                                    </template>
                                    <el-input v-model="new_navLink.icon" placeholder="icon class"></el-input>
                                </el-popover>
                            </td>
                            <!-- superuser -->
                            <td>
                                <el-switch
                                    v-model="new_navLink.superuser"
                                    size="large"
                                    active-text="SU"
                                    inactive-text="No"
                                />
                            </td>
                            <!-- delete -->
                            <td>
                                <button class="btn" @click="save_new_navLink"><i class="fa-solid fa-save"></i></button>
                                <button class="btn" @click="new_navLink.display=false"><i class="fa-solid fa-trash"></i></button>
                            </td>
                        </tr>
                        <tr v-for="data in navLink_data.slice((navLink_page-1)*5, (navLink_page-1)*5+5)" :key="data.ID">
                            <!-- route -->
                            <td><el-input v-model="data.route" size="large" placeholder="/dashboard"
                            @change="update_web_nav_page(data)"></el-input></td>
                            <!-- name -->
                            <td><el-input v-model="data.name" size="large" placeholder="個性化首頁"
                            @change="update_web_nav_page(data)"></el-input></td>
                            <!-- name_i18n -->
                            <td>
                                <el-popover
                                    width="300"
                                    trigger="click"
                                    @hide="update_web_nav_page(data)"
                                >
                                    <template #reference>
                                        <el-button size="large"><i class="fa-solid fa-globe"></i></el-button>
                                    </template>
                                    <el-form :rules="i18n_rule">
                                        <div v-for="c in Object.keys(data.name_i18n)" :key="c">
                                            <label>{{c}}</label>
                                            <el-form-item :prop="c">
                                                <el-input  v-model="data.name_i18n[c]"></el-input>
                                            </el-form-item>
                                        </div>
                                    </el-form>
                                </el-popover>
                            </td>
                            <!-- pageType -->
                            <td>
                                <el-popover 
                                    width="300"
                                    trigger="click"
                                    @hide="update_pageType(data)"
                                >
                                    <template #reference>
                                        <el-button size="large"><label v-if="data.all_pageType">All</label><i class="fa-solid fa-file" v-else></i></el-button>
                                    </template>
                                    <el-switch
                                        v-model="data.all_pageType"
                                        size="large"
                                        active-text="All"
                                        inactive-text="Specify pageType"
                                        @change="(new_val)=>{
                                             new_val ? data.pageType = 'all' : data.pageType = []
                                        }"
                                    />
                                    <div v-if="!data.all_pageType">
                                        <label class="mb-2">pageType</label>
                                        <div class="d-flex align-items-center" v-for="p,i in data.pageType" :key="i" >
                                            <el-input v-model="data.pageType[i]"></el-input>
                                            <button class="btn ms-auto text-dark" @click="()=>{
                                                data.pageType.splice(i, 1)
                                            }"><i class="fa-solid fa-trash"></i></button>
                                        </div>
                                        <el-button class="mt-2" size="large" @click="data.pageType.push('')"><i class="fa-solid fa-plus"></i></el-button>
                                    </div>
                                 </el-popover>
                            </td>
                            <!-- level -->
                            <td>
                                <el-popover 
                                    width="300"
                                    trigger="click"
                                    @hide="update_level(data)"
                                >
                                    <template #reference>
                                        <el-button size="large">{{data.all_level ? "All" : Number.isInteger(data.level) ? data.level : data.level.join(',')}}</el-button>
                                    </template>
                                    <el-switch
                                        v-model="data.all_level"
                                        size="large"
                                        active-text="All"
                                        inactive-text="Specify level"
                                        @change="(new_val)=>{
                                             new_val ? data.level = 1 : data.level = []
                                        }"
                                    />
                                    <el-checkbox-group v-model="data.level" v-if="!data.all_level">
                                        <el-checkbox :label="1" />
                                        <el-checkbox :label="2" />
                                        <el-checkbox :label="3" />
                                    </el-checkbox-group>
                                </el-popover>
                            </td>
                            <!-- show -->
                            <td>
                                <el-switch
                                    v-model="data.show"
                                    size="large"
                                    active-text="Show"
                                    inactive-text="Hide"
                                    @change="update_web_nav_page(data)"
                                />
                            </td>
                            <!-- priority -->
                            <td>
                                <el-input-number placeholder="1" v-model="data.priority"
                                @change="update_web_nav_page(data)"></el-input-number>
                            </td>
                            <!-- icon -->
                            <td>
                                <el-popover 
                                    width="300"
                                    trigger="click"
                                    @hide="update_web_nav_page(data)"
                                >
                                    <template #reference>
                                        <el-button size="large" class="pt-0 pb-0"><i v-if="data.icon != ''" :class="data.icon" class="fs-4"></i></el-button>
                                    </template>
                                    <el-input v-model="data.icon" placeholder="icon class"></el-input>
                                </el-popover>
                            </td>
                            <!-- superuser -->
                            <td>
                                <el-switch
                                    v-model="data.superuser"
                                    size="large"
                                    active-text="SU"
                                    inactive-text="No"
                                    @change="update_web_nav_page(data)"
                                />
                            </td>
                            <!-- delete -->
                            <td>
                                <button class="btn" @click="delete_data(data)"><i class="fa-solid fa-trash"></i></button>
                            </td>
                        </tr>
                    </tbody>
                </table>
            </div>
            <el-pagination
                class="d-flex justify-content-center w-100 mt-2"
                background
                layout="prev, pager, next"
                :total="navLink_length"
                :page-size="5"
                v-model:currentPage="navLink_page"
            >
			</el-pagination>
            <!-- ======================= tab ============================= -->
            <div class="d-flex align-items-center mb-2">
                <h6 class="mt-2">Tabs</h6>
                <button class="btn btn-warning ms-auto" @click="show_new_tab"><i class="fa-solid fa-plus"></i></button>
            </div>
            <div class="table-responsive" style="max-height: 50vh; overflow-y: scroll;">
                <table class="table table-striped">
                    <thead class="table-light">
                        <tr>
                            <th>Route</th>
                            <th>Value</th>
                            <th>Name</th>
                            <th>i18n</th>
                            <th>pageType</th>
                            <th>Level</th>
                            <th>priority</th>
                            <th>
                                Constrain
                                <el-popover
                                    width="90vw"
                                    trigger="hover"
                                >
                                    <template #reference>
                                        <button class="btn d-inline-block"><i class="fa-solid fa-circle-question"></i></button>
                                    </template>
                                    <h5>Usage of Constrain Differs</h5>
                                    <p>Tag: constrain usage differs depending on developers of eash page. You can defined you own and fill the description in the table below. Help everyone understands better!</p>
                                    <p class="fst-italic">Constrain is a JSON String. Enter constrain Properly!!!!</p>
                                    <br/>
                                    List of constrain usage:
                                    <table class="table  table-hover">
                                        <tr>
                                            <th>
                                                Route
                                            </th>
                                            <th>
                                                Description
                                            </th>
                                        </tr>
                                        <tr  v-for="d in constrain_description" :key="d.route">
                                            <td>
                                                {{d.route}}
                                            </td>
                                            <td>
                                                {{d.info}}
                                            </td>
                                        </tr>
                                    </table>
                                </el-popover>
                            </th>
                            <th v-show="false">Icon</th>
                            <th>Superuser ONLY</th>
                            <th>
                            </th>
                        </tr>
                    </thead>
                    <tbody>
                        <tr v-if="new_tab.display" class="bg-success bg-opacity-50">
                            <!-- route -->
                            <td><el-input v-model="new_tab.route" size="large" placeholder="/dashboard"></el-input></td>
                            <!-- value -->
                            <td>
                                <el-input
                                    v-model="new_tab.value"
                                    size="large"
                                />
                            </td>
                           <!-- name -->
                            <td><el-input v-model="new_tab.name" size="large" placeholder="個性化首頁"></el-input></td>
                            <!-- name_i18n -->
                            <td>
                                <el-popover
                                    width="300"
                                    trigger="click"
                                >
                                    <template #reference>
                                        <el-button size="large"><i class="fa-solid fa-globe"></i></el-button>
                                    </template>
                                    <el-form :rules="i18n_rule">
                                        <div v-for="c in Object.keys(new_tab.name_i18n)" :key="c">
                                            <label>{{c}}</label>
                                            <el-form-item :prop="c">
                                                <el-input  v-model="new_tab.name_i18n[c]"></el-input>
                                            </el-form-item>
                                        </div>
                                    </el-form>
                                </el-popover>
                            </td>
                            <!-- pageType -->
                            <td>
                                <el-popover 
                                    width="300"
                                    trigger="click"
                                    @hide="update_pageType(new_tab)"
                                >
                                    <template #reference>
                                        <el-button size="large"><label v-if="new_tab.all_pageType">All</label><i class="fa-solid fa-file" v-else></i></el-button>
                                    </template>
                                    <el-switch
                                        v-model="new_tab.all_pageType"
                                        size="large"
                                        active-text="All"
                                        inactive-text="Specify pageType"
                                        @change="(new_val)=>{
                                             new_val ? new_tab.pageType = 'all' : new_tab.pageType = []
                                        }"
                                    />
                                    <div v-if="!new_tab.all_pageType">
                                        <label class="mb-2">pageType</label>
                                        <div class="d-flex align-items-center" v-for="p,i in new_tab.pageType" :key="i" >
                                            <el-input v-model="new_tab.pageType[i]"></el-input>
                                            <button class="btn ms-auto text-dark" @click="()=>{
                                                new_tab.pageType.splice(i, 1)
                                            }"><i class="fa-solid fa-trash"></i></button>
                                        </div>
                                        <el-button class="mt-2" size="large" @click="new_tab.pageType.push('')"><i class="fa-solid fa-plus"></i></el-button>
                                    </div>
                                 </el-popover>
                            </td>
                            <!-- level -->
                            <td>
                                <el-popover 
                                    width="300"
                                    trigger="click"
                                    @hide="update_level(new_tab)"
                                >
                                    <template #reference>
                                        <el-button size="large">{{new_tab.all_level ? "All" : Number.isInteger(new_tab.level) ? new_tab.level : new_tab.level.join(',')}}</el-button>
                                    </template>
                                    <el-switch
                                        v-model="new_tab.all_level"
                                        size="large"
                                        active-text="All"
                                        inactive-text="Specify level"
                                        @change="(new_val)=>{
                                             new_val ? new_tab.level = 1 : new_tab.level = []
                                        }"
                                    />
                                    <el-checkbox-group v-model="new_tab.level" v-if="!new_tab.all_level">
                                        <el-checkbox :label="1" />
                                        <el-checkbox :label="2" />
                                        <el-checkbox :label="3" />
                                    </el-checkbox-group>
                                </el-popover>
                            </td>
                            <!-- priority -->
                            <td>
                                <el-input-number placeholder="1" v-model="new_tab.priority"></el-input-number>
                            </td>
                            <!-- icon -->
                            <td v-show="false">
                                <el-popover 
                                    width="300"
                                    trigger="click"
                                >
                                    <template #reference>
                                        <el-button size="large" class="pt-0 pb-0"><i v-if="new_tab.icon != ''" :class="new_tab.icon" class="fs-4"></i></el-button>
                                    </template>
                                    <el-input v-model="new_tab.icon" placeholder="icon class"></el-input>
                                </el-popover>
                            </td>
                            <!-- superuser -->
                            <td>
                                <el-switch
                                    v-model="new_tab.superuser"
                                    size="large"
                                    active-text="SU"
                                    inactive-text="No"
                                />
                            </td>
                            <!-- delete -->
                            <td>
                                <button class="btn" @click="save_new_tab"><i class="fa-solid fa-save"></i></button>
                                <button class="btn" @click="new_tab.display=false"><i class="fa-solid fa-trash"></i></button>
                            </td>
                        </tr>
                        <tr v-for="data in tab_data.slice((tab_page-1)*5, (tab_page-1)*5+5)" :key="data.ID">
                            <!-- route -->
                            <td><el-input v-model="data.route" size="large" placeholder="/dashboard"
                            @change="update_web_nav_page(data)"></el-input></td>
                            <!-- value -->
                            <td>
                                <el-input
                                    v-model="data.value"
                                    size="large"
                                    @change="update_web_nav_page(data)"
                                />
                            </td>
                            <!-- name -->
                            <td><el-input v-model="data.name" size="large" placeholder="個性化首頁"
                            @change="update_web_nav_page(data)"></el-input></td>
                            <!-- name_i18n -->
                            <td>
                                <el-popover
                                    width="300"
                                    trigger="click"
                                    @hide="update_web_nav_page(data)"
                                >
                                    <template #reference>
                                        <el-button size="large"><i class="fa-solid fa-globe"></i></el-button>
                                    </template>
                                    <el-form :rules="i18n_rule">
                                        <div v-for="c in Object.keys(data.name_i18n)" :key="c">
                                            <label>{{c}}</label>
                                            <el-form-item :prop="c">
                                                <el-input  v-model="data.name_i18n[c]"></el-input>
                                            </el-form-item>
                                        </div>
                                    </el-form>
                                </el-popover>
                            </td>
                            <!-- pageType -->
                            <td>
                                <el-popover 
                                    width="300"
                                    trigger="click"
                                    @hide="update_pageType(data)"
                                >
                                    <template #reference>
                                        <el-button size="large"><label v-if="data.all_pageType">All</label><i class="fa-solid fa-file" v-else></i></el-button>
                                    </template>
                                    <el-switch
                                        v-model="data.all_pageType"
                                        size="large"
                                        active-text="All"
                                        inactive-text="Specify pageType"
                                        @change="(new_val)=>{
                                             new_val ? data.pageType = 'all' : data.pageType = []
                                        }"
                                    />
                                    <div v-if="!data.all_pageType">
                                        <label class="mb-2">pageType</label>
                                        <div class="d-flex align-items-center" v-for="p,i in data.pageType" :key="i" >
                                            <el-input v-model="data.pageType[i]"></el-input>
                                            <button class="btn ms-auto text-dark" @click="()=>{
                                                data.pageType.splice(i, 1)
                                            }"><i class="fa-solid fa-trash"></i></button>
                                        </div>
                                        <el-button class="mt-2" size="large" @click="data.pageType.push('')"><i class="fa-solid fa-plus"></i></el-button>
                                    </div>
                                 </el-popover>
                            </td>
                            <!-- level -->
                            <td>
                                <el-popover 
                                    width="300"
                                    trigger="click"
                                    @hide="update_level(data)"
                                >
                                    <template #reference>
                                        <el-button size="large">{{data.all_level ? "All" : Number.isInteger(data.level) ? data.level : data.level.join(',')}}</el-button>
                                    </template>
                                    <el-switch
                                        v-model="data.all_level"
                                        size="large"
                                        active-text="All"
                                        inactive-text="Specify level"
                                        @change="(new_val)=>{
                                             new_val ? data.level = 1 : data.level = []
                                        }"
                                    />
                                    <el-checkbox-group v-model="data.level" v-if="!data.all_level">
                                        <el-checkbox :label="1" />
                                        <el-checkbox :label="2" />
                                        <el-checkbox :label="3" />
                                    </el-checkbox-group>
                                </el-popover>
                            </td>
                            <!-- priority -->
                            <td>
                                <el-input-number placeholder="1" v-model="data.priority"
                                @change="update_web_nav_page(data)"></el-input-number>
                            </td>
                            <!-- constrain -->
                            <td  class="constrain_input">
                                <el-input placeholder="JSON String" v-model="data.constrain"
                                @change="update_web_nav_page(data)" :clearable="true">
                                </el-input>
                            </td>
                            <!-- icon -->
                            <td v-show="false">
                                <el-popover 
                                    width="300"
                                    trigger="click"
                                    @hide="update_web_nav_page(data)"
                                >
                                    <template #reference>
                                        <el-button size="large" class="pt-0 pb-0"><i v-if="data.icon != ''" :class="data.icon" class="fs-4"></i></el-button>
                                    </template>
                                    <el-input v-model="data.icon" placeholder="icon class"></el-input>
                                </el-popover>
                            </td>
                            <!-- superuser -->
                            <td>
                                <el-switch
                                    v-model="data.superuser"
                                    size="large"
                                    active-text="SU"
                                    inactive-text="No"
                                    @change="update_web_nav_page(data)"
                                />
                            </td>
                            <!-- delete -->
                            <td>
                                <button class="btn" @click="delete_data(data)"><i class="fa-solid fa-trash"></i></button>
                            </td>
                        </tr>
                    </tbody>
                </table>
            </div>
            <el-pagination
                class="d-flex justify-content-center w-100"
                background
                layout="prev, pager, next"
                :total="tab_length"
                :page-size="5"
                v-model:currentPage="tab_page"
            >
			</el-pagination>
        </div>
    </div>
</template>

<script>
import { ElNotification } from 'element-plus'
import { ElMessage } from 'element-plus'

export default {
    name: "webNavPageCard",
    data(){
        return {
            pageType: "",
            navLink_data: [
            ],
            navLink_length: 0,
            navLink_page: 1,
            tab_data: [
            ],
            tab_length: 0,
            tab_page: 1,
            i18n_rule: {
                /* "zh-TW": [
                    { required: true, message: 'zh-TW Required', trigger: 'blur' },
                ],
                "en-US": [
                    { required: true, message: 'en-US Required', trigger: 'blur'}
                ] */
            },
            pageType_list: [],
            is_loading: false,
            new_navLink: {
                display: false,
                ID: null,
                all_level: true,
                all_pageType: true,
                icon: "",
                level: "all",
                name: "",
                name_i18n: {
                    "en-US": "",
                    "zh-TW": ""
                },
                pageType: "all",
                priority: 1,
                route: "/#",
                show: true,
                type: "navLink",
                superuser: true,
            },
            new_tab: {
                display: false,
                ID: null,
                all_level: true,
                all_pageType: true,
                icon: null,
                level: "all",
                name: "",
                name_i18n: {
                    "en-US": "",
                    "zh-TW": ""
                },
                pageType: "all",
                priority: 1,
                route: "/#",
                show: true,
                type: "tab",
                value: "",
                superuser: true,
                constrain: null,
            },
            mongodb_url: "",
            mongodb_db: "",
            constrain_description: [
                {route: '/stationData', info: 'constrain 在這邊用來控制此tab在pv_plant, pv_lgroup, pv_group階層是否要顯示。為陣列，在此陣列中的階層將會顯示。若為null則開放給所有階層'}
            ]
        }
    },
    methods: {
        update_web_nav_page(data, reload=false){
            this.axios.post('/web_nav_page_data', {
                method: 'update',
                data: data
            }).then(data=>{
                if(reload)
                    this.get_web_nav_page_data()
            }).catch(err=>{
                ElMessage.error("Update Error")
            })
        },
        update_pageType(data){
            if(data.ID != null)
                this.update_web_nav_page(data)
            /* if(data.all_pageType){
            }else if(data.pageType.length == 0){
                ElNotification({
                    title: "Not Updating",
                    message: "pageType is empty",
                    duration: 5000
                })
                console.log('Empty pageType')
            } */
        },
        update_level(data){
            if(data.ID != null)
                this.update_web_nav_page(data)
        },
        get_web_nav_page_data(){
            this.is_loading = true
            this.axios.get(`/web_nav_page_data?pageType=${this.pageType}`).then(data=>{
                console.log(data.data.data)
                this.navLink_data = data.data.data.navLink_data
                this.tab_data = data.data.data.tab_data
                this.navLink_length = data.data.data.navLink_length
                this.tab_length = data.data.data.tab_length
                this.pageType_list = data.data.data.pageType_list
                this.navLink_page = 1
                this.tab_page = 1
                this.is_loading = false
            })
        },
        delete_data(obj){
            const answer = confirm('It Will delete from database PERMANENTLY!!! Confirm?')
            if(answer){
                this.axios.delete(`/web_nav_page_data?ID=${obj.ID}`).then(data=>{
                    ElMessage.success('Success')
                    this.get_web_nav_page_data()
                }).catch(err=>{
                    ElMessage.error('Error')
                })
            }
        },
        json_export(){
            window.location.href = 'api/web_nav_page_json_export'
        },
        upload_error(){
            ElMessage.error('Uploaded Failed')
        },
        show_new_navLink(){
            this.new_navLink =  {
                display: true,
                ID: null,
                all_level: true,
                all_pageType: true,
                icon: "",
                level: "all",
                name: "",
                name_i18n: {
                    "en-US": "",
                    "zh-TW": ""
                },
                pageType: "all",
                priority: 1,
                route: "/#",
                show: true,
                type: "navLink",
                superuser: true,
            }
        },
        save_new_navLink(){
            this.update_web_nav_page(this.new_navLink, true)
            this.new_navLink = false
        },
        show_new_tab(){
            this.new_tab = {
                display: true,
                ID: null,
                all_level: true,
                all_pageType: true,
                icon: null,
                level: "all",
                name: "",
                name_i18n: {
                    "en-US": "",
                    "zh-TW": ""
                },
                pageType: "all",
                priority: 1,
                route: "/#",
                show: true,
                type: "tab",
                value: "",
                superuser: true,
                constrain: null,
            }
        },
        save_new_tab(){
            this.update_web_nav_page(this.new_tab, true)
            this.new_tab = false
        },
        mongodb_connect(){
            console.log(this.mongodb_url)
            window.location.href = `/api/web_nav_page_server_connection?url=${this.mongodb_url}&db=${this.mongodb_db}`
        }
    },
    mounted(){
        this.get_web_nav_page_data()
    }
}
</script>
<style scoped>
.constrain_input .el-input:hover :deep(.el-input__wrapper .el-input__inner),
.constrain_input .el-input :deep(.el-input__wrapper .el-input__inner:focus){
    width: fit-content;
}
</style>