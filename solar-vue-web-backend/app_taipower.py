# 台電 Vue 專用API
# 主程式功能
# Flask App 函式
from time import time
from app_common import successful_request, bad_request, check_user, logout, exception_detail, date_range_interval_to_filter, find_user_from_current_user
#-------------------------------------------------------------------------------
# Libiary
from flask import Blueprint, request, current_app, views
import datetime
from dateutil import relativedelta
import math
from bson import json_util,ObjectId
from werkzeug.utils import secure_filename
import os
import glob
import requests
import json
import pymongo
import datetime
#-------------------------------------------------------------------------------
# 通用函式與功能
import current as c
import prepareplot as t
import docx_produce as d # ==> docx報表製作函式
import cv2
#======================================================================================================
# application_taipower is a Blueprint of flask
# Learn More About Blueprint At
# https://flask.palletsprojects.com/en/2.0.x/blueprints/
application_taipower = Blueprint('application_taipower', __name__)
#======================================================================================================
#使用位置 /dashboard taipower 取得天氣資料 weather
@application_taipower.route('/get_weather_data', methods=['POST'])
def get_weather_data():
    user, db = check_user()
    if db == None:
        return logout()
    request_dict = request.json
    if 'city' not in request_dict:
        return bad_request(400, 'Bad Request. No city.')
    city = request_dict['city']
    weather_data = c.get_weather_forecast_by_date(db, city)
    weather = {
        'imgurl': weather_data.get('imgurl', ''),
        'temperature': weather_data.get('T', '---'),
        'status':weather_data.get('Wx', '---'),
        'rain': '---' if isinstance(weather_data.get('PoP6h', '---'), str) else int(weather_data['PoP6h'])
    }
    return successful_request(weather)
#-------------------------------------------------------------------------------
#使用位置 /dispatch 用警報_id取得原因 (AI analysis and manual pick)
@application_taipower.route('/alarm_id_get_reason', methods=['POST'])
def alarm_id_get_reason():
    user, db = check_user()
    if db == None:
        return logout()
    request_dict = request.json
    try:
        ID_list = request_dict['ID_list']
    except:
        return bad_request(400, 'Bad Request. No ID_list')
    print(ID_list)
    return_dict = {}
    cause_dict = {}
    for cause in db.alarm_cause.find({'show': 1}):
        if cause.get('alarm_group', '') not in cause_dict:
            cause_dict[cause.get('alarm_group', '')] = {}
        cause_dict[cause.get('alarm_group', '')][str(cause['_id'])] ={'event': str(cause.get('event', ''))}

    for _id in ID_list:
        return_dict[_id] = {
            'user_select': cause_dict,
            'ai_analysis': {}
        }
    return successful_request({'data': return_dict})
#-------------------------------------------------------------------------------
#docx製作
#By 鈞紘 
@application_taipower.route('/word_generator', methods=['POST'])
def word_generator():
    user,db = check_user()
    if(db == None):
        return logout() 
    request_dict = request.json

    try:
        equipment_ID = request_dict["ID"]
        start_time = request_dict["datepicker1"]
        start_time = datetime.datetime.strptime(start_time, '%Y-%m-%d')
        end_time = request_dict["datepicker2"]
        end_time = datetime.datetime.strptime(end_time, '%Y-%m-%d')
        time_interval = request_dict["time_interval"]
        plant_id, solar_ID, meter_ID, pr_ID, collection = d.id_identify(db, equipment_ID)
        name, field_position, capacity = d.field_imformation(db, plant_id)
        # 所有需要的時間
        time_list = d.set_time_interval(start_time, end_time, time_interval)

        #日照計資料
        irrh_data = d.irrh_cal(db, solar_ID, time_list, time_interval)
        #meter資料
        meter_data = d.meter_cal(db, meter_ID, time_list, time_interval)
        #pr資料
        pr_data = d.pr_cal(db, pr_ID, time_list, time_interval)
        #平均及最大值
        #無平均值
        max_val = d.avg_max_value(db, pr_ID, collection, time_list[0], end_time, avg_status=False)
        #有平均值
        # max_val, avg_val = d.avg_max_value(db, pr_ID, collection, time_list[0], end_time, avg_status=True)

        #頁首資訊
        header_data = d.company_imformation(db, plant_id)

        #頁尾資訊
        footer_info = d.company_imformation_footer(db, plant_id)

        #專案名稱
        name = d.project_name(db, pr_ID, time_list[0], time_list[-1], time_interval)
        date = str(time_list[0]) + "~" + str(time_list[-1])
        #案場資訊表格
        #有平均值
        # imformation_dict = d.imformation_data(name, date, field_position, str(capacity), str(max_val), str(avg_val))
        #無平均值
        imformation_dict = d.imformation_data(name, date, field_position, str(capacity), str(max_val))
        table_head_datas = ["時間", "日照量", "發電量(kWh)", "PR"]
        data = d.table_data(time_list, irrh_data, meter_data, pr_data)

        rv = d.report(name, header_data, imformation_dict, table_head_datas, data, current_app.config['UPLOAD_FOLDER'], time_interval, footer_info)
    except Exception as e:
        print(exception_detail(e))
        return bad_request(400, "Bad Request. {}".format(e))

    return rv
#-------------------------------------------------------------------------------
#schedule表格資訊
#By 鈞紘 
@application_taipower.route('/get_word_table_data', methods=['POST'])
def get_word_table_data():
    user,db = check_user()
    if(db == None):
        return logout() 
    request_dict = request.json

    try:
        ID_interval_word = db["ID_interval_word"]
        equipment_ID = request_dict.get("ID", "")
        col = request_dict.get("col", "")
        start_time = request_dict["datepicker1"]
        # start_time = datetime.strptime(start_time, '%Y-%m-%d')
        end_time = request_dict["datepicker2"]
        # end_time = datetime.strptime(end_time, '%Y-%m-%d')
        time_interval = request_dict["time_interval"]
        current_page = request_dict.get("current_page", 1)
        number_per_page = request_dict.get("number_per_page", 10)

        all_col_id = []
        all_filter = {}
        if len(col)>0:
            if col == 'pv_plant':
                all_col_id.append(equipment_ID)
                all_filter["PV"] = db.plant.find_one({"_id": ObjectId(equipment_ID)})["name"]
                all_filter["type"] = "pv_lgroup"
                for lgroup_c in db.equipment.find(all_filter):
                    all_col_id.append(str(lgroup_c["_id"]))
                all_filter["type"] = "pv_group"
                for group_c in db.equipment.find(all_filter):
                    all_col_id.append(str(group_c["_id"]))
            elif col == "pv_lgroup":
                pv = db.equipment.find_one({"_id": ObjectId(equipment_ID)})
                all_col_id.append(str(db.plant.find_one({"name":pv["PV"]})["_id"]))
                all_col_id.append(equipment_ID)
                all_filter["PV"] = pv["PV"]
                all_filter["lgroup"] = pv["name"]
                all_filter["type"] = "pv_group"
                for group_c in db.equipment.find(all_filter):
                    all_col_id.append(str(group_c["_id"]))
            elif col == "pv_group":
                pv = db.equipment.find_one({"_id": ObjectId(equipment_ID)})
                all_col_id.append(str(db.plant.find_one({"name": pv["PV"]})["_id"]))
                all_col_id.append(str(db.equipment.find_one({"PV": pv["PV"], "name": pv["lgroup"], "type": "pv_lgroup"})["_id"]))
                all_col_id.append(equipment_ID)

        find_user = find_user_from_current_user()
        user_c=list(db.users.find({"user_id" : find_user}))[0]

        equipment_filter = {}
        plant_filter = {}
        search_id = []
        if user_c['plant'][0] != 'total':
            for i in user_c['plant']:
                if 'PV' not in equipment_filter:
                    equipment_filter['PV'] = {'$in': []}
                if 'name' not in plant_filter:
                    plant_filter['name'] = {'$in': []}
                plant_filter['name']['$in'].append(i)
                equipment_filter['PV']['$in'].append(i)

            for plant in db.plant.find(plant_filter):
                search_id.append(str(plant['_id']))

            equipment_filter["type"] = "pv_lgroup"
            for lgroup in db.equipment.find(equipment_filter):
                search_id.append(str(lgroup["_id"]))
            
            equipment_filter["type"] = "pv_group"
            for group in db.equipment.find(equipment_filter):
                search_id.append(str(group["_id"]))

        if time_interval == "15min" or time_interval == "hour":
            check = start_time
        elif time_interval == "day":
            check = start_time.split("-")[0] + "-" + start_time.split("-")[1]
        elif time_interval == "month":
            check = start_time.split("-")[0]
        elif time_interval == "year":
            check = "year"

        if equipment_ID:
            datas = ID_interval_word.find(
                {
                    "ID": {"$in": all_col_id},
                    "time_interval": time_interval,
                    "show": 1,
                    "filename": {"$regex": check}
                }
            ).skip((current_page-1)*number_per_page).limit(number_per_page)
            total_page = ID_interval_word.count_documents(
                {
                    "ID":  {"$in": all_col_id},
                    "time_interval": time_interval,
                    "show": 1,
                    "filename": {"$regex": check}
                }
            )
            total_page = math.ceil(total_page/number_per_page)
        else:
            datas = ID_interval_word.find(
                {
                    "ID": {"$in": search_id} if user_c['plant'][0] != 'total' else {"$nin": []},
                    "time_interval": time_interval,
                    "show": 1,
                    "filename": {"$regex": check}
                }
            ).skip((current_page-1)*number_per_page).limit(number_per_page)
            total_page = ID_interval_word.count_documents(
                {
                    "ID": {"$in": search_id} if user_c['plant'][0] != 'total' else {"$nin": []},
                    "time_interval": time_interval,
                    "show": 1,
                    "filename": {"$regex": check}
                }
            )
            total_page = math.ceil(total_page/number_per_page)
        
        searchData = []
        for data in datas:
            # print(data)
            if time_interval == "15min" or time_interval == "hour":
                if data["filename"].split("_")[1] == start_time:
                    searchData.append(data)
            elif time_interval == "day":
                checkDate = data["filename"].split("_")[1]
                if checkDate.split("-")[0] == start_time.split("-")[0] and checkDate.split("-")[1].split(".")[0] == start_time.split("-")[1]:
                    searchData.append(data)
            elif time_interval == "month":
                checkDate = data["filename"].split("_")[1]
                if checkDate.split(".")[0] == start_time.split("-")[0]:
                    searchData.append(data)
            elif time_interval == "year":
                searchData.append(data)
            
        # place = []
        # interval = []
        # time = []
        return_data = []
        for data in searchData:
            place_name = data["filename"]
            return_data.append({
                "place": place_name.split("_")[0],
                "interval": time_interval,
                "time": place_name.split("_")[1].split(".")[0] if time_interval != "year" else "all",
                "filename": data["filename"],
                "ID": data["ID"]
            })
            # place.append(place_name.split("_")[0])
            # interval.append(time_interval)
            # time.append(place_name.split("_")[1].split(".")[0])
        data = {
            "data": return_data,
            "total_page": total_page
        }
        # print(data)
        return data
    except Exception as e:
        print(exception_detail(e))
        return bad_request(400, "Bad Request. {}".format(e))
#-------------------------------------------------------------------------------
#使用位置 /Analysis 短路電流熱圖資料
@application_taipower.route('/get_heat_map_data', methods=['POST'])
def get_heat_map_data():
    user,db = check_user()
    if(db == None):
        return logout() 
    request_dict = request.json

    try:
        group_ID = request_dict["ID"]
        start_time = request_dict["datepicker"]
        equipment = db["equipment"]
        string_meter_collection = db["string_meter"]
        setting = db["parameter_setting"]
        method = setting.find_one({
            "method": "shortCurrentHeatMap"
        })
        if method:
            time_interval = int(method["interval"])
        else:
            time_interval = 300
        group = equipment.find_one({
            "_id": ObjectId(group_ID)
        })

        x = t.fix_x_xis(date=datetime.datetime.strptime(start_time, '%Y-%m-%d'), interval=time_interval)
        x = x[108:193]
        x_length = len(x)
        x_axis = []
        for i in range(x_length):
            x_axis.append(datetime.datetime.strptime(x[i],"%Y-%m-%d %H:%M:%S"))
        if group:
            y_axis = []
            z_axis = []
            start = x_axis[0]
            end = x_axis[-1]
            PV = group["PV"]
            lgroup = group["lgroup"]
            name = group["name"]

            string_meters = equipment.find(
                {
                    "PV": PV,
                    "lgroup": lgroup,
                    "group": name,
                    "type": "string"
                }
            )
            for string_meter in string_meters:
                y = []
                meter_ID = str(string_meter["_id"])
                meter_name = string_meter["name"]
                wiring = string_meter["string_data"]["wiring"]
                for index in range(len(wiring)):
                    if wiring[index] == 1:
                        y.append(meter_name+"#"+str(index+1))
                y_axis.append(y)
                z = [[None for i in range(x_length)] for j in range(len(y))]
                meter_vals = string_meter_collection.find(
                    {
                        "ID": meter_ID,
                        "time": {"$gte": start, "$lte": end}
                    }
                ).sort("time")
                for meter_val in meter_vals:
                    for x_index, x_data in enumerate(x_axis):
                        if meter_val["time"] < x_data:
                            break
                        if meter_val["time"] == x_data:
                            for y_index in range(len(y)):
                                if meter_val["sa"][y_index] != None:
                                    z[y_index][x_index] = round(meter_val["sa"][y_index]/10.02, 2)
                z_axis.append(z)

            # for string_meter in string_meters:
            #     data_dict = {}
            #     w = []
            #     w_all = []
            #     y = []
            #     z = []
            #     data_list = []
            #     meter_ID = str(string_meter["_id"])
            #     meter_name = string_meter["name"]
            #     wiring = string_meter["string_data"]["wiring"]
            #     for index in range(len(wiring)):
            #         if wiring[index] == 1:
            #             w.append(index+1)
            #             y.append(meter_name+"#"+str(index+1))
            #             data_dict[meter_name+"#"+str(index+1)] = []
            #         w_all.append(index+1)
            #     y_axis.append(y)
            #     # old_time = time.time()
            #     meter_vals = string_meter_collection.find(
            #         {
            #             "ID": meter_ID,
            #             "time": {"$gte": start, "$lte": end}
            #         }
            #     ).sort("time")
            #     # print(time.time()-old_time)
            #     for meter_val in meter_vals:
            #         if meter_val["time"] in x_axis:
            #             data_list.append(meter_val)
            #     data_list.append(1)
            #     for x_index in range(x_length):
            #         for data_index in range(len(data_list)):
            #             if data_list[data_index] == 1:
            #                 for i in range(len(w_all)):
            #                     if w_all[i] in w:
            #                         data_dict[meter_name+"#"+str(w_all[i])].append(None)
            #                 break
            #             elif x_axis[x_index] == data_list[data_index]["time"]:
            #                 if len(data_list[data_index]["sa"]) == len(w):
            #                     for i, sa in enumerate(data_list[data_index]["sa"]):
            #                         if sa != None:
            #                             data_dict[meter_name+"#"+str(w[i])].append(round(sa/10.02, 2))
            #                         else:
            #                             data_dict[meter_name+"#"+str(w[i])].append(None)
            #                 elif len(data_list[data_index]["sa"]) > len(w):
            #                     counter = 0
            #                     for i in range(len(w_all)):
            #                         if w_all[i] in w:
            #                             value = data_list[data_index]["sa"][counter]
            #                             if value != None:
            #                                 data_dict[meter_name+"#"+str(w_all[i])].append(round(value/10.02, 2))
            #                             else:
            #                                 data_dict[meter_name+"#"+str(w_all[i])].append(None)
            #                             counter += 1
            #                 data_list = data_list[data_index+1:]
            #                 break
            #             elif x_axis[x_index] < data_list[data_index]["time"]:
            #                 for i in range(len(w)):
            #                     data_dict[meter_name+"#"+str(w[i])].append(None)
            #                 break
            #             elif x_axis[x_index] > data_list[data_index]["time"]:
            #                 continue
            #     for i in range(len(y)):
            #         z.append(data_dict[meter_name+"#"+str(i+1)])
            #     z_axis.append(z)
        x = []    
        for i in range(x_length):
            x.append(datetime.datetime.strftime(x_axis[i],"%Y-%m-%d %H:%M:%S"))
        return_data = {
            "x_axis": x,
            "y_axis": y_axis,
            "z_axis": z_axis
        }
        if len(x_axis) > 0 and len(y_axis) > 0 and len(z_axis) > 0:
            outdata = {
                "data": return_data
            }
            return successful_request({'data': outdata})
        else:
            return_data["z_axis"] = []
            outdata = {
                "data": return_data
            }
            return successful_request({'data': outdata})
    except Exception as e:
        print(exception_detail(e))
        return bad_request(400, "Bad Request. {}".format(e))
#-------------------------------------------------------------------------------
#使用位置 /documents
#Prototype 
class DocumentsUploadFile(views.MethodView):
    def __init__(self) -> None:
        super().__init__()
        self.allow_file_type = set(['png', 'PNG', 'jpg', 'JPG', 'jpeg', 'JPEG', 'HEIC', 'heic',
        'webp', 'WebP'])
        self.dirPath = current_app.config['UPLOAD_FOLDER']
    def post(self):
        user,db = check_user()
        if db == None:
            return logout()
        self.db = db 
        self.file_dict = request.files
        self.request_dict = request.form
        return self.processing()
    def processing(self):
        dirPath = self.create_store_path()
        if dirPath[0] == False:
            return bad_request(400, 'Bad Request. {}'.format(dirPath[1]))
        else:
            dirPath = dirPath[1]
        try:
            os.makedirs(dirPath)
            print("Directory " , dirPath ,  " Created ")    
        except FileExistsError:
            print("Directory " , dirPath ,  " already exists")
        result = []
        for i in self.file_dict:
            file = self.file_dict[i]
            if file and self.allowed_file(file.filename):
                #print(file)
                result.append(self.save_file(file, dirPath))
        return successful_request({
            'result': result
        })
    def create_store_path(self):
        return True, self.dirPath
    def save_file(self, file, dirPath):
        """ filename = secure_filename(file.filename)
        file.save(dirPath+'/'+file.filename) """
        pass
    def allowed_file(self, filename):
        return '.' in filename and \
            filename.rsplit('.', 1)[1] in self.allow_file_type
#-------------------------------------------------------------------------------
class UploadMainPhoto(DocumentsUploadFile):
    def create_store_path(self):
        try:
            return True, self.dirPath + '/images/plant_image'
        except Exception as e:
            return False, exception_detail(e)
    def save_file(self, file, dirPath):
        dirPath = dirPath + '/{}'.format(secure_filename('{}.{}'.format(
            self.request_dict['ID'], file.filename.rsplit('.', 1)[1]
        )))
        find_origin_img = glob.glob(
            '{}/images/plant_image/{}.*'.format(current_app.config['UPLOAD_FOLDER'], self.request_dict['ID'])
        )
        if find_origin_img:
            for origin_file in find_origin_img:
                trash_dir = '{}/trash'.format(origin_file.rsplit('/', 1)[0])
                try:
                    os.makedirs(trash_dir)
                except FileExistsError:
                    pass
                trash_dir += '/{}'.format(origin_file.split('/')[-1])
                os.replace(origin_file, trash_dir)
        file.save(dirPath)
        return True
        
application_taipower.add_url_rule('/documents/upload_main_photo', view_func=UploadMainPhoto.as_view('upload_main_photo'))
#-------------------------------------------------------------------------------
#上傳使用者的相片
class UploadUserPhoto(DocumentsUploadFile):
    def create_store_path(self):
        try:
            return True, self.dirPath + '/images/users_photo'
        except Exception as e:
            return False, exception_detail(e)
    def save_file(self, file, dirPath):
        db = self.db
        find_user = find_user_from_current_user()
        user_c=list(db.users.find({"user_id" : find_user}))[0]
        dirPath = dirPath + '/{}'.format(secure_filename('{}.{}'.format(
            str(user_c.get('_id')), file.filename.rsplit('.', 1)[1]
        )))
        find_origin_img = glob.glob(
            '{}/images/users_photo/{}.*'.format(current_app.config['UPLOAD_FOLDER'], str(user_c.get('_id')))
        )
        if find_origin_img:
            for origin_file in find_origin_img:
                trash_dir = '{}/trash'.format(origin_file.rsplit('/', 1)[0])
                try:
                    os.makedirs(trash_dir)
                except FileExistsError:
                    pass
                trash_dir += '/{}'.format(origin_file.split('/')[-1])
                os.replace(origin_file, trash_dir)
        file.save(dirPath)
        db.users.update_one({'_id': ObjectId(str(user_c.get('_id')))}, {'$set': { 
            'main_photo': 'solar_static/images/users_photo/{}.{}'.format(str(user_c.get('_id')), file.filename.rsplit('.', 1)[1])}})
        return True
        
application_taipower.add_url_rule('/setting/upload_user_photo', view_func=UploadUserPhoto.as_view('upload_user_photo'))
#-------------------------------------------------------------------------------
class UploadDocumentsPhoto(DocumentsUploadFile):
    def create_store_path(self):
        try:
            return True, self.dirPath + '/documents/{}/{}'.format(self.request_dict['ID'], 'photo')
        except Exception as e:
            return False, exception_detail(e)
    def save_file(self, file, dirPath):
        db = self.db
        #print(dirPath)
        #rename 
        file_count = db.documents_upload.count_documents({
            'ID': self.request_dict['ID'],
            'type': 'photo',
        })
        new_name = '{}.{}'.format(
            file_count + 1, file.filename.rsplit('.', 1)[1]
        )
        dirPath += '/{}'.format(secure_filename(new_name))
        file.save(dirPath)
        return str(db.documents_upload.insert_one({
            'ID': self.request_dict['ID'],
            'type': 'photo',
            'filename': new_name,
            'origin_filename': file.filename,
            'upload_time': datetime.datetime.now(),
            'show': 1}).inserted_id)
application_taipower.add_url_rule('/documents/upload_photo', view_func=UploadDocumentsPhoto.as_view('upload_documents_photo'))
#-------------------------------------------------------------------------------
class UploadDocumentsSld(DocumentsUploadFile):
    def __init__(self) -> None:
        super().__init__()
        self.allow_file_type.add('svg')
    def create_store_path(self):
        try:
            return True, self.dirPath + '/documents/{}/{}'.format(self.request_dict['ID'], 'sld')
        except Exception as e:
            return False, exception_detail(e)
    def save_file(self, file, dirPath):
        db = self.db
        #print(dirPath)
        #rename 
        file_count = db.documents_upload.count_documents({
            'ID': self.request_dict['ID'],
            'type': 'sld',
        })
        new_name = '{}.{}'.format(
            file_count + 1, file.filename.rsplit('.', 1)[1]
        )
        dirPath += '/{}'.format(secure_filename(new_name))
        file.save(dirPath)
        return str(db.documents_upload.insert_one({
            'ID': self.request_dict['ID'],
            'type': 'sld',
            'filename': new_name,
            'origin_filename': file.filename,
            'upload_time': datetime.datetime.now(),
            'show': 1}).inserted_id)
application_taipower.add_url_rule('/documents/upload_sld', view_func=UploadDocumentsSld.as_view('upload_documents_sld'))
#-------------------------------------------------------------------------------
class UploadDocumentsDrone(DocumentsUploadFile):
    def __init__(self) -> None:
        super().__init__()
        self.allow_file_type.add('tiff')
        self.allow_file_type.add('TIFF')
        self.allow_file_type.add('tif')
        self.allow_file_type.add('TIF')
    def create_store_path(self):
        try:
            return True, self.dirPath + '/documents/{}/{}'.format(self.request_dict['ID'], 'drone')
        except Exception as e:
            return False, exception_detail(e)
    def save_file(self, file, dirPath):
        db = self.db
        #print(dirPath)
        #rename 
        file_count = db.documents_upload.count_documents({
            'ID': self.request_dict['ID'],
            'type': 'drone',
        })
        new_name = '{}.{}'.format(
            file_count + 1, file.filename.rsplit('.', 1)[1]
        )
        dirPath += '/{}'.format(secure_filename(new_name))
        file.save(dirPath)
        return str(db.documents_upload.insert_one({
            'ID': self.request_dict['ID'],
            'type': 'drone',
            'filename': new_name,
            'origin_filename': file.filename,
            'upload_time': datetime.datetime.now(),
            'show': 1}).inserted_id)
application_taipower.add_url_rule('/documents/upload_drone', view_func=UploadDocumentsDrone.as_view('upload_documents_drone'))
#-------------------------------------------------------------------------------
class UploadDocumentsPhotoGet(views.MethodView):
    def __init__(self) -> None:
        super().__init__()
        self.file_type = 'photo'
    def post(self):
        user,db = check_user()
        if db == None:
            return logout()
        self.db = db
        self.request_dict = request.json
        try:
            ID = self.request_dict['ID']
            ObjectId(ID)
        except:
            return bad_request(400, 'Bad Request. ID Error')
        return self.get_data(ID)
    def get_data(self, ID):
        db = self.db
        request_dict = self.request_dict
        try:
            date_obj = request_dict.get('time', None)
            #print(date_obj)
            time_filter = date_range_interval_to_filter(date_obj)
            if time_filter[0] == False:
                return bad_request(400, time_filter[1])
            time_filter = time_filter[1]
            file_filter = {'show': 1, 'ID': ID, 'upload_time': time_filter,
            'type': self.file_type}
            
            current_page = request_dict.get('current_page', 1)
            file_list = []
            for _file in db.documents_upload.find(file_filter).sort('upload_time', -1).limit(20).skip((current_page-1)*10):
                try:
                    _file['_id'] = str(_file['_id'])
                    _file['filepath'] = 'solar_static/documents/{}/{}/{}'.format(ID, self.file_type, _file['filename'])
                    _file['upload_time_simple'] = datetime.datetime.strftime(_file['upload_time'], '%Y-%m-%d')
                    _file['upload_time'] = datetime.datetime.strftime(_file['upload_time'], '%Y-%m-%d %H:%M:%S')
                    file_list.append(_file)
                except:
                    pass
        except Exception as e:
            return bad_request(400, 'Bad Request. {}'.format(exception_detail(e)))

        total_file = db.documents_upload.count_documents(file_filter)
        return successful_request({
            'file_list': file_list,
            'current_page': current_page,
            'total_page': math.ceil(total_file/10),
            'total_file': total_file
        })
application_taipower.add_url_rule('/documents/upload_documents_photo_get', view_func=UploadDocumentsPhotoGet.as_view('upload_documents_photo_get'))
#-------------------------------------------------------------------------------
class UploadDocumentsSldGet(UploadDocumentsPhotoGet):
    def __init__(self) -> None:
        super().__init__()
        self.file_type = 'sld'
application_taipower.add_url_rule('/documents/upload_documents_sld_get', view_func=UploadDocumentsSldGet.as_view('upload_documents_sld_get'))
#-------------------------------------------------------------------------------
class UploadDocumentsDroneGet(UploadDocumentsPhotoGet):
    def __init__(self) -> None:
        super().__init__()
        self.file_type = 'drone'
application_taipower.add_url_rule('/documents/upload_documents_drone_get', view_func=UploadDocumentsDroneGet.as_view('upload_documents_drone_get'))
#-------------------------------------------------------------------------------
@application_taipower.route('/documents/upload_documents_photo_delete', methods=['POST'])
def upload_documents_photo_delete():
    user,db = check_user()
    if db == None:
        return logout()
    request_dict = request.json
    try:
        ID = request_dict['ID']
        ObjectId(ID)
    except:
        return bad_request(400, 'Bad Request. ID Error.')
    db.documents_upload.update_one({
        '_id': ObjectId(ID)
    }, {'$set': {'show': 0}})
    return successful_request()
#-------------------------------------------------------------------------------
@application_taipower.route('/documents/upload_documents_sld_delete', methods=['POST'])
def upload_documents_sld_delete():
    user,db = check_user()
    if db == None:
        return logout()
    request_dict = request.json
    try:
        ID = request_dict['ID']
        ObjectId(ID)
    except:
        return bad_request(400, 'Bad Request. ID Error.')
    db.documents_upload.update_one({
        '_id': ObjectId(ID)
    }, {'$set': {'show': 0}})
    return successful_request()
#-------------------------------------------------------------------------------
@application_taipower.route('/documents/upload_documents_drone_delete', methods=['POST'])
def upload_documents_drone_delete():
    user,db = check_user()
    if db == None:
        return logout()
    request_dict = request.json
    try:
        ID = request_dict['ID']
        ObjectId(ID)
    except:
        return bad_request(400, 'Bad Request. ID Error.')
    db.documents_upload.update_one({
        '_id': ObjectId(ID)
    }, {'$set': {'show': 0}})
    return successful_request()
#-------------------------------------------------------------------------------
class UploadDocumentsVideo(DocumentsUploadFile):
    def __init__(self) -> None:
        super().__init__()
        self.allow_file_type = set(['mp4', 'MP4', 'mov', 'MOV'])
    def create_store_path(self):
        try:
            return True, self.dirPath + '/documents/{}/{}'.format(self.request_dict['ID'], 'video')
        except Exception as e:
            return False, exception_detail(e)
    def save_file(self, file, dirPath):
        db = self.db
        #print(dirPath)
        #rename 
        file_count = db.documents_upload.count_documents({
            'ID': self.request_dict['ID'],
            'type': 'video',
        })
        new_name = '{}.{}'.format(
            file_count + 1, file.filename.rsplit('.', 1)[1]
        )
        floder_path = dirPath
        dirPath += '/{}'.format(secure_filename(new_name))
        file.save(dirPath)
        #create thumbnail
        vidcap = cv2.VideoCapture(dirPath)
        success,image = vidcap.read()
        while success:
            floder_path += '/{}.png'.format(file_count + 1)
            cv2.imwrite(floder_path, image)     # save frame as PNG file      
            break
        result = db.documents_upload.insert_one({
            'ID': self.request_dict['ID'],
            'type': 'video',
            'filename': new_name,
            'origin_filename': file.filename,
            'upload_time': datetime.datetime.now(),
            'count': file_count + 1,
            'thumbnail_path': 'solar_static/documents/{}/{}/{}.png'.format(self.request_dict['ID'], 'video', file_count + 1),
            'show': 1})
        return {
            '_id': str(result.inserted_id),
            'count': file_count + 1,
            'filename': new_name,
        }
application_taipower.add_url_rule('/documents/upload_video', view_func=UploadDocumentsVideo.as_view('upload_documents_video'))
#-------------------------------------------------------------------------------
class UploadDocumentsVideoGet(UploadDocumentsPhotoGet):
    def __init__(self) -> None:
        super().__init__()
        self.file_type = 'video'
application_taipower.add_url_rule('/documents/upload_documents_video_get', view_func=UploadDocumentsVideoGet.as_view('upload_documents_video_get'))
#-------------------------------------------------------------------------------
@application_taipower.route('/documents/upload_documents_video_delete', methods=['POST'])
def upload_documents_video_delete():
    user,db = check_user()
    if db == None:
        return logout()
    request_dict = request.json
    try:
        ID = request_dict['ID']
        ObjectId(ID)
    except:
        return bad_request(400, 'Bad Request. ID Error.')
    db.documents_upload.update_one({
        '_id': ObjectId(ID)
    }, {'$set': {'show': 0}})
    return successful_request()
#-------------------------------------------------------------------------------
#treeview 樹狀圖
#by 善淜
class GetTreeEquipment(views.MethodView):
    def post(self):
        user,db = check_user()
        if(db == None):
            return logout() 
        request_dict = request.json
        try:
            plant_id = request_dict.get("plant_id","None")
            collection = request_dict.get("collection", "None")
            temp = self.getTree(plant_id,collection,db)
            if temp == None:
                return bad_request(400, "Bad Request. - No Data")
            return successful_request(temp)
        except Exception as e:
            print(exception_detail(e))
            return bad_request(400, "Bad Request. {}".format(e))
        
    def getSensor(self, _id:str,db):
        group = db['equipment'].find_one({"_id":ObjectId(_id)})
        filter = {
            "PV":group['PV'],
            "lgroup":group['lgroup'],
            "group":group['name'],
            "collection":"sensor"
        }
        sensor = []
        data = db['equipment'].find(filter)
        for i in data:
            temp = {
                "ID":str(i['_id']),
                "name":i['name'],
                "type":i['type'],
                "value":None
            }
            try:
                temp['value'] = round(db['sensor'].find_one({"ID":str(i['_id'])})['value'],2)
            except:
                pass
            sensor.append(temp)
        return sensor

    def getInverterbyGroup(self, _id:str,db):
        group = db['equipment'].find_one({"_id":ObjectId(_id)})
        filter = {
            "PV":group['PV'],
            "lgroup":group['lgroup'],
            "group":group['name'],
            "type":"inv"
        }
        inverter = []
        data = db['equipment'].find(filter)
        for i in data:
            temp = {
                "ID":str(i['_id']),
                "name":i['name'],
                "type":"inv",
                "kwh":None,
                "pr":None
            }
            try:
                temp["pr"]=round(db['pr_cal'].find_one({"ID":str(i['_id'])})['pr'],2)
            except:
                pass
            try:
                temp["kwh"]=round(db['inverter'].find_one({"ID":str(i['_id'])})['kwh'],2)
            except:
                pass
            inverter.append(temp)
        return inverter

    def getGroup(self, _id:str,db):
        group = db['equipment'].find_one({"_id":ObjectId(_id)})
        if group == None:
            return []
        data = {
            "ID":str(group['_id']),
            "name":group['name'],
            "type":"group",
            "kwh":None,
            "pr":None
        }
        
        try:
            data["pr"]=round(db['pr_cal'].find_one({"ID":str(group['_id'])})['pr'],2)
        except:
            pass
        try:
            data["kwh"]=round(db[group['collection']].find_one({"ID":str(group['_id'])})['kwh'],2)
        except:
            pass
        inverter = self.getInverterbyGroup(_id,db)
        sensor = self.getSensor(_id,db)
        if len(sensor) + len(inverter):
            data['children'] =  inverter + sensor
        return data
        
    def getlgroup(self, _id:str,db):
        lgroup = db['equipment'].find_one({"_id":ObjectId(_id)})
        data = {
            "ID":str(lgroup['_id']),
            "name":lgroup['name'],
            "type":"lgroup",
            "kwh":None,
            "pr":None
        }
        
        try:
            data["pr"]=round(db['pr_cal'].find_one({"ID":str(lgroup['_id'])})['pr'],2)
        except:
            pass
        try:
            data["kwh"]=round(db[lgroup['collection']].find_one({"ID":str(lgroup['_id'])})['kwh'],2)
        except:
            pass
        
        filter = {
            "PV":lgroup['PV'],
            "lgroup":lgroup['name'],
            "type":"pv_group",
        }
        groups = db['equipment'].find(filter)
        if groups:
            data['children'] = []
        for group in groups:
            data['children'].append(self.getGroup(str(group["_id"]),db))
        return data
    
    def getplant(self, _id:str,db):
        plant = db['plant'].find_one({"_id":ObjectId(_id)})
        data = {
            "ID":str(plant['_id']),
            "name":plant['name'],
            "type":"plant",
            "kwh":None,
            "pr":None
        }
        
        try:
            data["pr"]=round(db['pr_cal'].find_one({"ID":str(plant['_id'])})['pr'],2)
        except:
            pass
        try:
            data["kwh"]=round(db[plant['collection']].find_one({"ID":str(plant['_id'])})['kwh'],2)
        except:
            pass
        
        filter = {
            "PV":plant['name'],
            "type":"pv_lgroup"
        }
        groups = db['equipment'].find(filter)
        if groups:
            data['children'] = []
        for group in groups:
            data['children'].append(self.getlgroup(str(group["_id"]),db))
        return data

    def getTree(self, _id:str,collection:str,db):
        data = {
            "ds" : None
        }
        print(collection)
        if collection == "pv_plant":
            data['ds'] = self.getplant(_id,db)
        elif collection =="pv_lgroup":
            data['ds'] = self.getlgroup(_id,db)
        elif collection == "pv_group":
            data['ds'] = self.getGroup(_id,db)
        else:
            return None
        return data
application_taipower.add_url_rule('/get_tree_equipment', view_func=GetTreeEquipment.as_view('get_tree_equipment'))
#-------------------------------------------------------------------------------
#使用位置 /setting
# push notification 手動發送推播
class ManualSendPushNotification(views.MethodView):
    def post(self):
        user,db = check_user()
        if(db == None):
            return logout() 
        find_user = find_user_from_current_user()
        user_c=list(db.users.find({"user_id" : find_user}))[0]
        if user_c.get('level', 0) < 3:
            return bad_request(400, 'Bad Request. Auth fail.')
        request_dict = request.json
        #print(request_dict)
        try:
            push_dict = {
                'title': request_dict['title'],
                'content': request_dict['content'],
                'route': request_dict['route'],
                'rule': request_dict['rule'],
                'send_to': request_dict.get('send_to', []),
                'platform': {
                    'android': request_dict['platform']['android'],
                    'ios': request_dict['platform']['ios']
                },
                'send': False,
                'target_time': datetime.datetime.now(),
                'expire_at': datetime.datetime.now() + datetime.timedelta(days=1),
                'create_time': datetime.datetime.now() 
            }
            if request_dict['rule'] == 'user_list':
                user_list = request_dict.get('send_to', '')
                user_list = list(user_list.split(','))
                push_dict['send_to'] = []
                for user in db.users.find({'username': {'$in': user_list}}):
                    push_dict['send_to'].append(str(user['_id']))
            db.push_notification.insert_one(push_dict)
        except Exception as e:
            return bad_request(400, 'Bad Request. {}'.format(e))
        return successful_request()
application_taipower.add_url_rule('/manual_send_push_notification', view_func=ManualSendPushNotification.as_view('manual_send_push_notification'))
#-------------------------------------------------------------------------------
# 發電量預測
# by 鈞紘
@application_taipower.route('/get_power_forecasting_data', methods=['POST'])
def get_power_forecasting_data():
    user,db = check_user()
    if(db == None):
        return logout() 
    request_dict = request.json

    try:
        start_time = request_dict["datepicker1"]
        end_time = request_dict["datepicker2"]
        ID = request_dict["ID"]
        mode = request_dict["mode"]
        print(request_dict)
        if start_time == end_time:
            end_time += " 23:59:59"
            start_time += " 00:00:00"
            start_time = datetime.datetime.strptime(start_time, '%Y-%m-%d %H:%M:%S')
            end_time = datetime.datetime.strptime(end_time, '%Y-%m-%d %H:%M:%S')
            if mode != "single":
                start_time -= datetime.timedelta(days=2)
                end_time += datetime.timedelta(days=3)
        else:
            end_time += " 23:00:00"
            start_time += " 00:00:00"
            start_time = datetime.datetime.strptime(start_time, '%Y-%m-%d %H:%M:%S')
            end_time = datetime.datetime.strptime(end_time, '%Y-%m-%d %H:%M:%S')
        return_data = {
            "output_kwh": [],
            "real_kwh": [],
            "time": []
        }

        return_data["time"] = t.fix_x_xis_date(start_time, end_time)
        forecasting_collection = db["generation_forecast"]
        for time in return_data["time"]:
            data = forecasting_collection.find_one(
                {
                    "ID": ID,
                    "time": datetime.datetime.strptime(time, '%Y-%m-%d %H') + relativedelta.relativedelta(minutes=0, seconds=0)
                }
            )
            if data != None:
                if data["output_kwh"] != None:
                    # print(data["output_kwh"])
                    return_data["output_kwh"].append(round(data["output_kwh"], 2))
                else:
                    return_data["output_kwh"].append(None)
                if data["real_kwh"] != None:
                    # print(data["real_kwh"])
                    return_data["real_kwh"].append(round(data["real_kwh"], 2))
                else:
                    return_data["real_kwh"].append(None)
            else:
                return_data["real_kwh"].append(None)
                return_data["output_kwh"].append(None)
        output_data = {
            "data": return_data
        }
        return successful_request({'data': output_data})
    except Exception as e:
        print(exception_detail(e))
        return bad_request(400, "Bad Request. {}".format(e))

#-------------------------------------------------------------------------------
# 使用位置 alarm
# 警報圓餅圖 
# by 鈞紘
@application_taipower.route('/get_alarm_pie_chart_data', methods=['POST'])
def get_alarm_pie_chart_data():
    user,db = check_user()
    if(db == None):
        return logout() 
    request_dict = request.json

    try:
        alarm_option = request_dict["alarm_option"]
        alarms = request_dict["alarms"]

        return_data = {"losing":{}}
        table_dict = {}
        return_list = []
        nowtime = datetime.datetime.now()
        if(alarm_option == "設備" or alarm_option == "軟體"):
            for alarm in alarms:
                if alarm["alarm_group"] == alarm_option:
                    if alarm["alarm_event"] not in return_data:
                        return_data[alarm["alarm_event"]] = 0
                        return_data["losing"][alarm["alarm_event"]] = 0
                    return_data[alarm["alarm_event"]] += 1
                    return_data["losing"][alarm["alarm_event"]] += round(alarm.get("losing_kwh", 0), 2)


                    table_key_name = alarm.get("alarm_place", "") + "_" + alarm.get("equip_name", "") + "_" + alarm.get("alarm_event")
                    if table_key_name not in table_dict:
                        table_dict[table_key_name] = {
                            "alarm_place": alarm.get("alarm_place", "---"),
                            "equip_name" : alarm.get("equip_name", "---"),
                            "alarm_event": alarm.get("alarm_event", "---"),
                            "occur_time": 0,
                            "duration": datetime.timedelta(seconds=0)
                        }
                    
                    return_time = alarm.get("returntime", "")
                    time = alarm.get("time", nowtime)
                    duration = "---"
                    time = datetime.datetime.strptime(time, '%Y-%m-%d %H:%M:%S')
                    if len(return_time) > 0:
                        return_time = datetime.datetime.strptime(return_time, '%Y-%m-%d %H:%M:%S')
                        if return_time < time:
                            duration = time - return_time
                        else:
                            duration = return_time - time
                    else:
                        duration = nowtime - time
                    table_dict[table_key_name]["occur_time"] += 1
                    if duration != "---":
                        table_dict[table_key_name]["duration"] += duration

        elif alarm_option == "all":
            for alarm in alarms:
                if alarm["alarm_group"] == "設備" or alarm["alarm_group"] == "軟體":
                    if alarm["alarm_event"] not in return_data:
                        return_data[alarm["alarm_event"]] = 0
                        return_data["losing"][alarm["alarm_event"]] = 0
                    return_data[alarm["alarm_event"]] += 1
                    return_data["losing"][alarm["alarm_event"]] += round(alarm.get("losing_kwh", 0), 2)

                    table_key_name = alarm.get("alarm_place", "") + "_" + alarm.get("equip_name", "") + "_" + alarm.get("alarm_event")
                    if table_key_name not in table_dict:
                        table_dict[table_key_name] = {
                            "alarm_place": alarm.get("alarm_place", "---"),
                            "equip_name" : alarm.get("equip_name", "---"),
                            "alarm_event": alarm.get("alarm_event", "---"),
                            "occur_time": 0,
                            "duration": datetime.timedelta(seconds=0)
                        }
                    
                    return_time = alarm.get("returntime", "")
                    time = alarm.get("time", nowtime)
                    duration = "---"
                    time = datetime.datetime.strptime(time, '%Y-%m-%d %H:%M:%S')
                    if len(return_time) > 0:
                        return_time = datetime.datetime.strptime(return_time, '%Y-%m-%d %H:%M:%S')
                        if return_time < time:
                            duration = time - return_time
                        else:
                            duration = return_time - time
                    else:
                        duration = nowtime - time
                    table_dict[table_key_name]["occur_time"] += 1
                    if duration != "---":
                        table_dict[table_key_name]["duration"] += duration
        for data in table_dict.values():
            data["duration"] = round(data["duration"].total_seconds()/(60*60), 1)
            return_list.append(data)
        output_data = {
            "data": return_data,
            "table_data": return_list
        }
        return successful_request({'data': output_data})
    except Exception as e:
        print(exception_detail(e))
        return bad_request(400, "Bad Request. {}".format(e))
#-------------------------------------------------------------------------------
# 使用位置 setting
# 使用者設定 更改帳號密碼
@application_taipower.route('/change_username_password', methods=['POST'])
def change_username_password():
    user,db = check_user()
    if(db == None):
        return logout() 
    request_dict = request.json
    find_user = find_user_from_current_user()
    user_c=list(db.users.find({"user_id" : find_user}))[0]
    try:
        old_password = request_dict['old_password']
        if old_password != user_c['password']:
            return successful_request({
                'status': False,
                'reason': 'not_equal'
            })
        else:
            if request_dict['new_password'] != request_dict['password_valid']:
                return successful_request({
                    'status': False,
                    'reason': 'valid_error'
                })
            db.users.update_one({
                '_id': user_c['_id']
            }, {
                '$set': {
                    'password': request_dict['new_password']
                }
            })
    except Exception as e:
        return bad_request(400, 'Bad Request. {}'.format(exception_detail(e)))
    return successful_request({
        'status': True
    })
#-------------------------------------------------------------------------------
# 使用位置 setting
# 取得使用者相關參數
# 在app_common create_new_user 需要新增
@application_taipower.route('/setting/load_user_parameter', methods=['POST', 'GET'])
def load_user_parameter():
    user,db = check_user()
    if db == None:
        return logout()
    find_user = find_user_from_current_user()
    user_c=list(db.users.find({"user_id" : find_user}))[0]

    if request.method == 'POST':
        request_dict = request.json
        #print(request_dict)
        db.users.update_one({'_id': user_c['_id']}, {
            '$set': {
                'parameter': request_dict
            }
        })
        return successful_request()
    else:
        return_dict = {}
        if 'parameter' not in user_c:
            user_c['parameter'] = {}
        return_dict = {
            'pr': user_c['parameter'].get('pr', 'pr')
        }
        return successful_request(return_dict)
#-------------------------------------------------------------------------------
# 使用位置 stationData
#取得變流器顯示表格
@application_taipower.route('/get_inv_table_data', methods=['POST'])
def get_inv_table_data():
    user,db = check_user()
    if db == None:
        return logout()
    request_dict = request.json
    try:
        ID = request_dict['inv_ID']
        Device_model = db.equipment.find_one({'_id': ObjectId(ID)}).get('Device_model')
    except:
        return bad_request(400, 'Bad Request. ID Error')
    table_list = []
    try:
        table_list = db.inverter_table.find_one({'Device_model': Device_model})['table']
    except:
        pass
    return successful_request({
        'table_data': table_list,
        'Device_model': Device_model
    })
#-------------------------------------------------------------------------------
#首頁比較圖表
@application_taipower.route('/get_home_page_compare_data', methods=['POST'])
def get_home_page_compare_data():
    user,db = check_user()
    if db == None:
        return logout()
    request_dict = request.json
    try:
        date_range = request_dict["date_range"]

        find_user = find_user_from_current_user()
        user_c=list(db.users.find({"user_id" : find_user}))[0]

        start_time = datetime.date.today()
        end_time = datetime.date.today()
        year = start_time.year
        month = start_time.month
        # print(user_c)
        if date_range == 2:
            start_time = datetime.date(year, month, 1)
            end_time = datetime.date(year, month+1, 1) - datetime.timedelta(days=1)
        elif date_range == 3:
            start_time = datetime.date(year, 1, 1)
            end_time = datetime.date(year, 12, 1)
        elif date_range == 4:
            start_time = datetime.date(2022, 1, 1)
            end_time = datetime.date(year, 1, 1)
        start_time = datetime.datetime.combine(start_time, datetime.time.min)
        end_time = datetime.datetime.combine(end_time, datetime.time.min)
        # print(type(start_time))
        # print(type(end_time))
        equipment_filter = {}
        if user_c['plant'][0] != 'total':
            for i in user_c['plant']:
                if 'PV' not in equipment_filter:
                    equipment_filter['PV'] = {'$in': []}
                equipment_filter['PV']['$in'].append(i)
        equipment_filter["type"] = "pv_lgroup"

        ID_list = []
        name_list = []
        for equipment in db.equipment.find(equipment_filter):
            ID_list.append(str(equipment["_id"]))
            name = equipment.get("PV", "") + "_" + equipment.get("name", "")
            name_list.append(name)
        
        y_axis = {}
        for i, ID in enumerate(ID_list):
            y_axis[name_list[i]] = t.bar_one_cal_col(db, ID, "meter_cal", "kwh", start_time, end_time, date_range)

        x_axis = t.fix_x_xis_date(start_time, end_time, date_range)
        # print(y_axis[name_list[0]])
        return successful_request({
            "data": {
                "x_axis": x_axis,
                "y_axis": y_axis,
                "name_list": name_list
            }
        })
    except Exception as e:
        print(exception_detail(e))
        return bad_request(400, "Bad Request. {}".format(e))
#-------------------------------------------------------------------------------
#首頁多種圖表
@application_taipower.route('/get_home_page_multiple_data', methods=['POST'])
def get_home_page_multiple_data():
    user,db = check_user()
    if db == None:
        return logout()
    request_dict = request.json
    try:
        date_range = request_dict["date_range"]
        ID = request_dict["ID"]
        plot_type = request_dict["plot_type"]

        plant_collection = db["plant"]
        equipment_collection = db["equipment"]
        inverter_collection = db["inverter"]

        start_time = datetime.date.today()
        end_time = datetime.date.today()
        year = start_time.year
        month = start_time.month
        if date_range == 2:
            start_time = datetime.date(year, month, 1)
            end_time = datetime.date(year, month+1, 1) - datetime.timedelta(days=1)
        start_time = datetime.datetime.combine(start_time, datetime.time.min)
        end_time = datetime.datetime.combine(end_time, datetime.time.min)

        y_axis = {}
        page_data = 5
        total_page = 5
        if plot_type == 3 or plot_type == 4:
            plant = plant_collection.find_one({"_id": ObjectId(ID)})
            name = plant["name"]
            inverters = equipment_collection.find(
                {
                    "PV": name,
                    "type": "inv"
                }
            )
            name_list = []
            if plot_type == 3:
                for inverter in inverters:
                    inv_id = str(inverter["_id"])
                    name_list.append(inverter["lgroup"]+"_"+inverter["name"])
                    y_axis[inverter["lgroup"]+"_"+inverter["name"]] = t.bar_one_cal_col(db, inv_id, "inverter_cal", "kwh", start_time, end_time, date_range)
            elif plot_type == 4:
                for inverter in inverters:
                    inv_id = str(inverter["_id"])
                    name_list.append(inverter["lgroup"]+"_"+inverter["name"])
                    y_axis[inverter["lgroup"]+"_"+inverter["name"]] = t.bar_one_cal_col(db, inv_id, "pr_cal", "pr", start_time, end_time, date_range)
        elif plot_type == 5:
            plant = plant_collection.find_one({"_id": ObjectId(ID)})
            name = plant["name"]
            inverters = equipment_collection.find(
                {
                    "PV": name,
                    "type": "inv"
                }
            )
            name_list = []
            for inverter in inverters:
                inv_id = str(inverter["_id"])
                name_list.append(inverter["lgroup"]+"_"+inverter["name"])
                end_time += relativedelta.relativedelta(hour=23,minute=59,second=59)
                for target in inverter_collection.find({"ID": inv_id,"time": {"$gte": start_time, "$lte": end_time}}).sort("p_bus_total", -1).limit(1):
                    y_axis[inverter["lgroup"]+"_"+inverter["name"]] = target["p_bus_total"]

            parameter_collection = db["parameter_setting"]
            page_data = parameter_collection.find_one({"method": "widget_table_num"}).get("num", 5)

            y_reg = [[]]
            index = 0
            for key, value in y_axis.items():
                if len(y_reg[index]) < page_data:
                    y_reg[index].append({"name": key, "value": value})
                elif len(y_reg[index]) == page_data:
                    index += 1
                    y_reg.append([])
                    y_reg[index].append({"name": key, "value": value})
            y_axis = y_reg
            total_page = len(y_axis)
        x_axis = t.fix_x_xis_date(start_time, end_time, date_range)

        return successful_request({
            "data": {
                "x_axis": x_axis,
                "y_axis": y_axis,
                "name_list": name_list,
                "page_data": page_data,
                "total_page": total_page
            }
        })
    except Exception as e:
        print(exception_detail(e))
        return bad_request(400, "Bad Request. {}".format(e))
#-------------------------------------------------------------------------------
# 使用位置 setting/widget
# 取得使用者相關參數
# 在app_common create_new_user 需要新增
@application_taipower.route('/setting/load_user_widget_parameter', methods=['POST', 'GET'])
def load_user_widget_parameter():
    user,db = check_user()
    if db == None:
        return logout()
    find_user = find_user_from_current_user()
    user_c=list(db.users.find({"user_id" : find_user}))[0]
    parameter_collection = db["parameter_setting"]
    target = parameter_collection.find_one({"method": "widget_max_num"})

    if request.method == 'POST':
        request_dict = request.json
        widget_set = request_dict["user_parameters"]
        city = request_dict["city"]
        widget_set["city_select"] = city
        #print(request_dict)
        db.users.update_one({'_id': user_c['_id']}, {
            '$set': {
                'widget': widget_set
            },
            # '$unset':{"widget":""}
        })
        return successful_request()
    else:
        return_dict = {}
        if 'widget' not in user_c:
            user_c['widget'] = {}
        return_dict = {
            "widget_data": {
                'weatherTime': user_c['widget'].get('weatherTime', True),
                'compareChart': user_c['widget'].get('compareChart', True),
                'taiwan3dMap': user_c['widget'].get('taiwan3dMap', False),
                'treeMap': user_c['widget'].get('treeMap', False),
                'totalInformationTable': user_c['widget'].get('totalInformationTable', True),
                'plantHistory': user_c['widget'].get('plantHistory', False),
                'multipleChart': user_c['widget'].get('multipleChart', True),
                'equipmentCompareChart': user_c['widget'].get('equipmentCompareChart', False),
                'sequenceChart': user_c['widget'].get('sequenceChart', False),
                'city_select': user_c['widget'].get('city_select', ""),
                'dispatchStats': user_c['widget'].get('dispatchStats', False)
            },
            'widget_max_num': target.get('num', 3),
        }
        return successful_request(return_dict)

@application_taipower.route('/setting/get_widget_city', methods=['POST'])
def get_widget_city():
    user,db = check_user()
    if db == None:
        return logout()
    plant_collection = db["plant"]
    find_user = find_user_from_current_user()
    user_c=list(db.users.find({"user_id" : find_user}))[0]
    user_plants = user_c.get("plant", [])
    return_list = []
    reg = []
    try:
        if user_plants[0] == "total":
            for plant in plant_collection.find():
                if plant["location"]["city"] not in reg:
                    reg.append(plant["location"]["city"])
                    return_list.append({"value":plant["location"]["city"], "label":plant["location"]["city"]})
        else:
            for plant_name in user_plants:
                city = plant_collection.find_one({"name": plant_name})["location"]["city"]
                if city not in reg:
                    reg.append(city)
                    return_list.append({"value":city, "label":city})
        return_dict = {"data": return_list}
        return successful_request(return_dict)
    except Exception as e:
        print(exception_detail(e))
        return bad_request(400, "Bad Request. {}".format(e))
#-------------------------------------------------------------------------------
#電站管理/總覽圖表
@application_taipower.route('/overview_get_today_power', methods=['POST'])
def overview_get_today_power():
    user,db = check_user()
    if db == None:
        return logout()
    request_dict = request.json
    ID = request_dict["ID"]
    try:
        start_time = datetime.date.today()
        end_time = datetime.date.today()
        start_time = datetime.datetime.combine(start_time, datetime.time.min)
        end_time = datetime.datetime.combine(end_time, datetime.time.min)

        x_axis = []
        y_axis = []

        x_axis = t.fix_x_xis_date(start_time, end_time, 1)
        y_axis = t.bar_one_cal_col(db, ID, "meter_cal", "kwh", start_time, end_time, 1)

        return successful_request({
            "data": {
                "x_axis": x_axis,
                "y_axis": y_axis
            }
        })
    except Exception as e:
        print(exception_detail(e))
        return bad_request(400, "Bad Request. {}".format(e))
#-----------------------------------------------------------------------------
#alarm時序圖
@application_taipower.route('/get_alarm_sequence_diagram', methods=['POST'])
def get_alarm_sequence_diagram():
    user,db = check_user()
    if db == None:
        return logout()
    request_dict = request.json

    try:
        dispatch_collection = db["dispatch"]
        dispatch_filter = {}
        plant = request_dict["plant"]
        if plant["ID"] != None:
            dispatch_filter["ID"] = {"$in": []}
        if plant["col"] == "pv_lgroup":
            dispatch_filter["ID"] = plant["ID"]
        elif plant["col"] == "pv_plant":
            ID_list = []
            plant_name = db["plant"].find_one({"_id": ObjectId(plant["ID"])})["name"]
            for lgroup in db["equipment"].find({"PV": plant_name, "type":"pv_lgroup"}):
                ID_list.append(str(lgroup["_id"]))
            dispatch_filter["ID"]["$in"] = ID_list
        elif plant["col"] == "pv_group":
            ID_list = []
            group = db["equipment"].find_one({"_id": ObjectId(plant["ID"])})
            for lgroup in db["equipment"].find({"PV": group["PV"], "name": group["lgroup"], "type": "pv_lgroup"}):
                ID_list.append(str(lgroup["_id"]))
            dispatch_filter["ID"]["$in"] = ID_list


        if request_dict.get('time', {}).get('mode', '') == 'single':
            try:
                start_date = datetime.datetime.strptime(request_dict['time']['start_date'], '%Y-%m-%d')
                end_date = start_date + datetime.timedelta(days=1)
                dispatch_filter['dispatch_time'] = {'$gte': start_date, '$lt': end_date}
            except:
                return bad_request(400, 'Time error')
        elif request_dict.get('time', {}).get('mode', '') == 'interval':
            try:
                start_date = datetime.datetime.strptime(request_dict['time']['start_date'], '%Y-%m-%d')
                end_date = datetime.datetime.strptime(request_dict['time']['end_date'], '%Y-%m-%d')
                dispatch_filter['dispatch_time'] = {'$gte': start_date, '$lt': end_date+datetime.timedelta(days=1)}
            except:
                return bad_request(400, 'Time error')
        elif request_dict.get('time', {}).get('mode', '') in ['today', 'week', 'month', 'year']:
            today = datetime.datetime.today()
            if request_dict['time']['mode'] == 'today':
                start_date = datetime.datetime.combine(today, datetime.time.min)
                end_date = start_date + datetime.timedelta(days=1)
            elif request_dict['time']['mode'] == 'week':
                start_date=datetime.datetime.combine(today, datetime.time.min) - datetime.timedelta(days=today.weekday())
                end_date = datetime.datetime.now()
            elif request_dict['time']['mode'] == 'month':
                start_date = datetime.datetime(year=today.year, month=today.month, day=1)
                end_date = datetime.datetime.now()
            elif request_dict['time']['mode'] == 'year':
                start_date = datetime.datetime(year=today.year, month=1, day=1)
                end_date = datetime.datetime.now()
            dispatch_filter['dispatch_time'] = {'$gte': start_date, '$lt': end_date}

        all_time = []

        now = datetime.datetime.now()
        dispatch_names = []
        dispatch_dict = {}
        time_list = []
        for dispatch_data in dispatch_collection.find(dispatch_filter):
            time_list = []
            dispatch_name = dispatch_data["name"]
            if dispatch_name not in dispatch_names:
                dispatch_names.append(dispatch_name)
            if dispatch_name not in dispatch_dict:
                dispatch_dict[dispatch_name] = []
            if dispatch_data.get("finish_time", None) != None:
                finish_time = dispatch_data.get("finish_time", now)
                working_time = dispatch_data["working_data"][-1]["working_hour"]
                start_time = finish_time - relativedelta.relativedelta(hours=working_time)
                start_time = datetime.datetime.strftime(start_time, '%Y-%m-%d %H:%M:%S')
                finish_time = datetime.datetime.strftime(finish_time, '%Y-%m-%d %H:%M:%S')

                time_list.append(start_time)
                if start_time not in all_time:
                    all_time.append(start_time)
                time_list.append(finish_time)
                if finish_time not in all_time:
                    all_time.append(finish_time)
                dispatch_dict[dispatch_name].append(time_list)
            else:
                dispatch_time = dispatch_data.get("dispatch_time", now) if dispatch_data.get("dispatch_time", now) != None and dispatch_data.get("dispatch_time", now) != "" else now
                now_time = datetime.datetime.strftime(now, '%Y-%m-%d %H:%M:%S')
                _dispatch_time = datetime.datetime.strftime(dispatch_time, '%Y-%m-%d %H:%M:%S')

                time_list.append(_dispatch_time)
                if _dispatch_time not in all_time:
                    all_time.append(_dispatch_time)
                time_list.append(now_time)
                if now_time not in all_time:
                    all_time.append(now_time)
                dispatch_dict[dispatch_name].append(time_list)


        alarm_array = request_dict["alarms"]
        alarm_names = []
        alarm_dict = {}
        x_axis = []
        y_axis = []
        time_list = []
        if alarm_array != []:
            for alarm in alarm_array:
                alarm_name = alarm.get("alarm_place", "")+"_"+alarm.get("equip_name", "")+"_"+alarm.get("alarm_event", "")
                if alarm_name not in alarm_names:
                    alarm_names.append(alarm_name)
                if alarm_name not in alarm_dict:
                    alarm_dict[alarm_name] = []
                time = alarm["time"]
                return_time = alarm["returntime"]

                time_list = []
                time_list.append(time)
                if time not in all_time:
                    all_time.append(time)
                if return_time != "" :
                    time_list.append(return_time)
                    if return_time not in all_time:
                        all_time.append(return_time)
                        # __time = datetime.datetime.strptime(return_time, '%Y-%m-%d %H:%M:%S')
                        # __time += relativedelta.relativedelta(seconds=1)
                        # __time = datetime.datetime.strftime(__time, '%Y-%m-%d %H:%M:%S')
                        # all_time.append(__time)
                else:
                    time_list.append(now_time)
                    if now_time not in all_time:
                        all_time.append(now_time)
                time_list.sort()
                alarm_dict[alarm_name].append(time_list)

        alarm_dict.update(dispatch_dict)
        # print(alarm_dict)
        x_axis = sorted(all_time)
        y_axis = [[j+1 for i in range(len(x_axis))] for j in range(len(alarm_dict.keys()))]
        index = 0
        counter = 0
        for x_index, _alarm in enumerate(alarm_dict.keys()):
            alarm_dict[_alarm].sort()
            print(alarm_dict[_alarm])
            for y_index, _time in enumerate(x_axis):
                if index == len(alarm_dict[_alarm]):
                    y_axis[x_index][y_index] = None
                    continue
                if _time == alarm_dict[_alarm][index][0] and _time == alarm_dict[_alarm][index][1]:
                    counter = 0
                    index += 1
                    continue
                if _time == alarm_dict[_alarm][index][0] or _time == alarm_dict[_alarm][index][1]:
                    counter += 1
                if counter == 2:
                    index += 1
                    counter = 0
                    continue
                if _time < alarm_dict[_alarm][index][0] or _time > alarm_dict[_alarm][index][1]:
                    y_axis[x_index][y_index] = None
            index = 0

        return successful_request({
            "data": {
                "x_axis": x_axis,
                "y_axis": y_axis,
                "names": alarm_names+dispatch_names
            }
        })
    except Exception as e:
        print(exception_detail(e))
        return bad_request(400, "Bad Request. {}".format(e))
#------------------------------------------------------------------------------------------------------
#使用位置setting/generation forecast model version
@application_taipower.route('/setting/load_forecast_parameter', methods=['POST'])
def load_forecast_parameter():
    user,db = check_user()
    if db == None:
        return logout()
    request_dict = request.json
    forecast_collection = db['generation_forecast_std&mean']
    status = request_dict.get("status", "")
    request_type = request_dict["type"]
    return_dict = {}
    try:
        #post更新資料
        if request_type == 'POST':
            place_name = request_dict["name"]
            model = request_dict.get("model", "")
            if model:
                forecast_collection.update_one({"name": place_name}, {
                    '$set': {
                        'model_reversion': model
                    },
                })
                return successful_request()
        #get取得資料
        else:
            if status == "place":
                equipment_filter = {}
                search_id = []
                find_user = find_user_from_current_user()
                user_c=list(db.users.find({"user_id" : find_user}))[0]
                user_plants = user_c.get("plant", [])
                if len(user_plants)>0 and user_plants[0] != 'total':
                    for plant in db.plant.find({"name": {"$in": user_plants}}):
                        search_id.append(str(plant["_id"]))
                    for i in user_plants:
                        if 'PV' not in equipment_filter:
                            equipment_filter['PV'] = {'$in': []}
                        equipment_filter['PV']['$in'].append(i)
                    equipment_filter["type"] = "pv_lgroup"
                    for lgroup in db.equipment.find(equipment_filter):
                        search_id.append(str(lgroup["_id"]))
                elif len(user_plants)>0 and user_plants[0] == 'total':
                    for plant in db.plant.find():
                        search_id.append(str(plant["_id"]))
                    for i in db.plant.find():
                        if 'PV' not in equipment_filter:
                            equipment_filter['PV'] = {'$in': []}
                        equipment_filter['PV']['$in'].append(i["name"])
                    equipment_filter["type"] = "pv_lgroup"
                    for lgroup in db.equipment.find(equipment_filter):
                        search_id.append(str(lgroup["_id"]))

                all_place = []
                for place in forecast_collection.find({"ID": {"$in": search_id}}):
                    if place.get("name", "") != "":
                        all_place.append({"label": place["name"], "value": place["name"]})
                return_dict = {"data":all_place}
                return successful_request(return_dict)
            elif status == "model":
                place_name = request_dict["name"]
                place = forecast_collection.find_one({"name":place_name})
                if place:
                    return_dict = {
                        "data":{
                            "model_reversion": place.get("model_reversion", ""),
                            "model_history": []
                        }
                    }
                    for history in place.get("model_history", []):
                        return_dict["data"]["model_history"].append({"label": history, "value": history})
                    return successful_request(return_dict)
        return successful_request(return_dict)
    except Exception as e:
        print(exception_detail(e))
        return bad_request(400, "Bad Request. {}".format(e))
#-------------------------------------------------------------------------------------------------------
@application_taipower.route('/get_report_tenday', methods=['POST'])
def get_report_tenday():
    user,db = check_user()
    if(db == None):
        return logout() 
    request_dict = request.json

    try:
        excel = db["excel"]
        equipment = db["equipment"]
        equipment_ID = request_dict.get("ID", "")
        start_time = request_dict["datepicker1"]
        start_time = datetime.datetime.strptime(start_time, '%Y-%m-%d')
        end_time = request_dict["datepicker2"]
        end_time = datetime.datetime.strptime(end_time, '%Y-%m-%d')
        current_page = request_dict.get("current_page", 1)
        number_per_page = request_dict.get("number_per_page", 10)

        find_user = find_user_from_current_user()
        user_c=list(db.users.find({"user_id" : find_user}))[0]
        pageType = user_c["pageType"]

        all_col_id = []
        all_filter = {}
        if len(equipment_ID)>0:
            pv = db.equipment.find_one({"_id": ObjectId(equipment_ID)})
            all_col_id.append(str(db.plant.find_one({"name":pv["PV"]})["_id"]))
            all_col_id.append(equipment_ID)
            all_filter["PV"] = pv["PV"]
            all_filter["lgroup"] = pv["name"]
            all_filter["type"] = "pv_group"
            for group_c in db.equipment.find(all_filter):
                all_col_id.append(str(group_c["_id"]))

        equipment_filter = {}
        search_id = []
        if user_c['plant'][0] != 'total':
            for i in user_c['plant']:
                if 'PV' not in equipment_filter:
                    equipment_filter['PV'] = {'$in': []}
                search_id.append(str(db.plant.find_one({"name": i})["_id"]))
                equipment_filter['PV']['$in'].append(i)

            equipment_filter["type"] = "pv_lgroup"
            for lgroup in db.equipment.find(equipment_filter):
                search_id.append(str(lgroup["_id"]))
            equipment_filter["type"] = "pv_group"
            for group in db.equipment.find(equipment_filter):
                search_id.append(str(group["_id"]))
        else:
            for i in db["plant"].find():
                if 'PV' not in equipment_filter:
                    equipment_filter['PV'] = {'$in': []}
                equipment_filter['PV']['$in'].append(i["name"])

            equipment_filter["type"] = "pv_lgroup"
            for lgroup in db.equipment.find(equipment_filter):
                search_id.append(str(lgroup["_id"]))
            
        if equipment_ID:
            datas = excel.find(
                {
                    "ID": {"$in": all_col_id},
                    "show": 1,
                    "time": {'$gte': start_time, '$lte': end_time}
                }
            ).skip((current_page-1)*number_per_page).limit(number_per_page)
            total_page = excel.count_documents(
                {
                    "ID": {"$in": all_col_id},
                    "show": 1,
                    "time": {'$gte': start_time, '$lte': end_time}
                }
            )
            total_page = math.ceil(total_page/number_per_page)
        else:
            datas = excel.find(
                {
                    "ID": {"$in": search_id},
                    "show": 1,
                    "time": {'$gte': start_time, '$lte': end_time}
                }
            ).skip((current_page-1)*number_per_page).limit(number_per_page)
            total_page = excel.count_documents(
                {
                    "ID": {"$in": search_id},
                    "show": 1,
                    "time": {'$gte': start_time, '$lte': end_time}
                }
            )
            total_page = math.ceil(total_page/number_per_page)
        
        return_data = []
        for data in datas:
            lgroup_id = data["ID"]
            target = equipment.find_one({"_id": ObjectId(lgroup_id)})
            PV = target["PV"]
            name = target["name"]
            return_data.append({
                "station": PV+"-"+name,
                "time": datetime.datetime.strftime(data["time"], '%Y-%m-%d'),
                "period": data.get("peroid", "---"),
                "filename": data["filename"],
            })
            
            
        data = {
            "data": return_data,
            "total_page": total_page,
            "pageType": pageType
        }
        return successful_request(data)
    except Exception as e:
        print(exception_detail(e))
        return bad_request(400, "Bad Request. {}".format(e))

#-------------------------------------------------------------------------------
# 使用位置 setting/IEC61850
# IEC61850 設定參數及指令發送
# 新增 by.善淜
@application_taipower.route('/setting/get_IEC61850_parameter', methods=['POST'])
def get_IEC61850_parameter():
    user,db = check_user()
    if(db == None):
        return logout()
    request_dict = request.json
    request_type = request_dict.get("type", "")
    try:
        if request_type == "GET":
            return_dict = db.IEC61850_parameter.find_one()
            del return_dict["_id"]
            return successful_request(return_dict)
        return bad_request(400,"Bad Request. {}".format(e))
    except Exception as e:
        print(exception_detail(e))
        return bad_request(400, "Bad Request. {}".format(e))

@application_taipower.route('/setting/send_IEC61850_command', methods=['POST'])
def send_IEC61850_command():
    user,db = check_user()
    if(db == None):
        return logout()
    request_dict = request.json
    try:
        command_dict = {
            "time":datetime.datetime.fromtimestamp(request_dict['time']/1000),
            "address":request_dict['address'],
            "value":request_dict['value'],
            "start":datetime.datetime.fromtimestamp(request_dict['start']/1000),
            "status":request_dict['status'],
            "parity":request_dict['parity'],
            "equipment":request_dict['equipment'],
            "mac":request_dict['mac'],
            "multiplier":request_dict['multiplier'],
            "check":False
        }
        if db.IEC61850.count_documents({"start":command_dict["start"],"equipment":command_dict['equipment']}) > 0:
            return bad_request(400, 'Bad Request. This command has been sent.')
        db.IEC61850.insert_one(command_dict)
    except Exception as e:
        return bad_request(400,"Bad Request. {}".format(e))
    return successful_request()

@application_taipower.route('/get_IEC61850_command', methods=['POST'])
def get_IEC61850_command():
    user,db = check_user()
    if db == None:
        return logout()
    try:
        request_dict = request.json
        mac = request_dict['mac']
        return_dict = [i for i in db['IEC61850'].find({"mac":mac,"check":False})]
        for i in return_dict:
            i['_id'] = str(i['_id'])
        return successful_request(return_dict)
    except Exception as e:
        print(exception_detail(e))
        return bad_request(400, "Bad Request. {}".format(e))
    
@application_taipower.route('/delete_IEC61850_command', methods=['POST'])
def delete_IEC61850_command():
    user,db = check_user()
    if db == None:
        return logout()
    try:
        check = []
        request_dict = request.json
        _id = request_dict['_id']
        if type(_id) == str:
            db['IEC61850'].delete_one({"_id":ObjectId(_id)})
            check.append(_id)
        elif type(_id) == list:
            for i in _id:
                db['IEC61850'].delete_one({"_id":ObjectId(i)})
                check.append(i)
        return successful_request({"check":check})
    except Exception as e:
        print(exception_detail(e))
        return bad_request(400, "Bad Request. {}".format(e))
#-------------------------------------------------------------------------------
# 使用位置 setting
# 資料完整度補遺 by碩庭
@application_taipower.route('/setting/fake_data_integrity', methods=['POST', 'GET'])
def fake_data_integrity():
    user, db = check_user()
    if db == None:
        return logout()
    find_user = find_user_from_current_user()
    user_c = list(db.users.find({"user_id": find_user}))[0]
    request_dict = request.json
    try:
        if request_dict['password'] == user_c['password']:
            if request_dict['is_fake_or_pr'] == '1':
                # 模擬資料計算，整理資料至指定型式[start_date,end_date,['mac'],{type.json}]
                start_time_buffer = request_dict['start_date'].split('-')
                start_time = datetime.datetime(int(start_time_buffer[0]), int(
                    start_time_buffer[1]), int(start_time_buffer[2]), int(request_dict['start_time']))

                end_time_buffer = request_dict['end_date'].split('-')
                end_time = datetime.datetime(int(end_time_buffer[0]), int(
                    end_time_buffer[1]), int(end_time_buffer[2]), int(request_dict['end_time']))

                mac_search_index = request_dict['station'].split('/')[0]
                mac_search = db.equipment.find_one({'PV': mac_search_index})
                mac = [mac_search['mac']]

                type_json = {
                    'plant': 0,
                    'lgroup': 0,
                    'group': 0,
                    'inverter': 0,
                    'sensor': 0,
                    'meter': 0
                }

                for type_checked in request_dict['type_checked']:
                    type_json[type_checked] = 1

                import_data = [start_time, end_time,
                               mac, type_json, user_c['username']]

                print(import_data)

                import fake_data_integrity
                fake_data_integrity.main_function(import_data)

            elif request_dict['is_fake_or_pr'] == '0':
                # PR值計算，call建誠學長寫好的.py
                os.system('')
            else:
                return bad_request(400, 'Bad request. API not valid.')
        else:
            print('password not correct')
            return bad_request(400, 'Bad request. User password not correct.')
    except Exception as e:
        print(exception_detail(e))
        return bad_request(400, 'Bad request. {}'.format(e))

    return successful_request()
#-------------------------------------------------------------------------------
# 使用位置 setting
# 設備更新紀錄 by碩庭 20220709v01
# 未補上iot api使設備重啟的功能

@application_taipower.route('/setting/equipment_record', methods=['POST', 'GET'])
def equipment_record():
    user, db = check_user()
    if db == None:
        return logout()
    find_user = find_user_from_current_user()
    user_c = list(db.users.find({"user_id": find_user}))[0]
    request_dict = request.json
    try:
        actual_time = request_dict['time']
        browser_time = datetime.datetime.now()
        equip_id = request_dict['equip']

        # print('actual time : ', actual_time)
        # print('browser time : ', browser_time)
        # print('user : ', user_c['username'])
        # print('kwh : ', request_dict['kwh'])
        # print(db['equipment'].find_one({'_id': ObjectId(equip_id)}))

        equip_data = db['equipment'].find_one({'_id': ObjectId(equip_id)})

        # 如果有要更新kwh的情況
        if db['equipment'].find_one({'_id': ObjectId(equip_id), 'integratingMeter': {'$exists': True}}):
            try:
                original_kwh = equip_data['integratingMeter']
                # 更新equipments內的 integratingMeter 值
                new_kwh = int(request_dict['kwh']) + original_kwh
                update = db['equipment'].update_one({'_id': ObjectId(equip_id)}, {
                                                    '$set': {'integratingMeter': float(request_dict['kwh']) + original_kwh}})
                print('kwh upload done')
            except Exception as e:
                original_kwh = 0
                new_kwh = original_kwh
                print('error')
        else:
            new_kwh = None
            print('there is no original kwh')

        # 要上傳到設備專用的collection的
        upload_data = {
            # 設備ID
            'ID': equip_id,
            # 設備name
            'name': equip_data['name'],
            # 設備位置
            'location': request_dict['name'],
            # 網站時間
            'browser_time': browser_time,
            # 實際時間(人員手動輸入)
            'actual_time': actual_time,
            # 舊kwh(人員手動輸入)
            'old_kwh': int(request_dict['kwh']),
            # 新kwh(舊kwh+原本設備的kwh)
            'new_kwh': new_kwh,
            # user
            'username': user_c['username']
        }
        print('upload data : ', upload_data)

        # 上傳至資料庫
        upload = db['equipment_record'].insert_one(upload_data)
        print('data upload status : ', upload.acknowledged)

        equip_data = db['equipment'].find_one({'_id': ObjectId(equip_id)})
    except Exception as e:
        print(exception_detail(e))
        return bad_request(400, 'Bad request. {}'.format(e))
    return successful_request()
# ------------------------------------------------------------------------------- 20220917更新
# 使用位置 setting
# 資料完整度圖表 by碩庭 20220709v01


@application_taipower.route('/get_data_integrity_data', methods=['POST'])
def get_data_integrity_data():
    user, db = check_user()
    if(db == None):
        return logout()
    request_dict = request.json
    try:
        # print(db.command('collstats', 'AI_alarm'))
        # 設定要回傳的變數
        return_data = {}

        # 把request_dict的資料分到變數內
        start_time = request_dict["start_date"]
        end_time = request_dict["end_date"]

        # 如果搜尋範圍為一天，資料查詢範圍設定為2天前的00:00~3天後的23:59
        if start_time == end_time:
            end_time += " 23:59:59"
            start_time += " 00:00:00"

            start_time = datetime.datetime.strptime(
                start_time, '%Y-%m-%d %H:%M:%S')
            end_time = datetime.datetime.strptime(
                end_time, '%Y-%m-%d %H:%M:%S')

        # 不然就設定為區間開始的00:00~區間結束的23:59
        else:
            end_time += " 23:00:00"
            start_time += " 00:00:00"
            start_time = datetime.datetime.strptime(
                start_time, '%Y-%m-%d %H:%M:%S')
            end_time = datetime.datetime.strptime(
                end_time, '%Y-%m-%d %H:%M:%S')

        # t.fix_x_xis_date的功能是自動把開始時間跟結束時間切成可以拿去當搜尋索引的List
        return_data["time"] = t.fix_x_xis_date(start_time, end_time)

        search_index = request_dict['station'].split('/')

        # 需要進行搜尋的設備列表
        PV_dict = {}
        lgroup_dict = {}
        group_dict = {}
        inverter_dict = {}
        sensor_dict = {}
        meter_dict = {}

        # plant 的情況
        if len(search_index) == 1:
            search_type = 'plant'
            search_index_split = {
                'PV': search_index[0],
                'lgroup': None,
                'group': None
            }
            search_index_equipment = db['plant'].find_one(
                {'_id': ObjectId(request_dict['ID'])})

        # lgroup的情況
        elif len(search_index) == 2:
            search_type = 'lgroup'
            search_index_split = {
                'PV': search_index[0],
                'lgroup': search_index[1],
                'group': None
            }
            search_index_equipment = db['equipment'].find_one(
                {'_id': ObjectId(request_dict['ID'])})

        # group的情況
        elif len(search_index) == 3:
            search_type = 'group'
            search_index_split = {
                'PV': search_index[0],
                'lgroup': search_index[1],
                'group': search_index[2]
            }
            search_index_equipment = db['equipment'].find_one(
                {'_id': ObjectId(request_dict['ID'])})
        else:
            return bad_request(400, 'Bad request. {}'.format(e))

        print(search_index_split)

        # 有打勾要搜尋的類別(一~六種)
        type_to_search = request_dict['type_checked']

        # 在return_data內新增項目
        # plant的搜尋
        if 'plant' in type_to_search:
            PV_search = db['plant'].find_one(
                {'name': search_index_split['PV']})
            PV_dict[str(PV_search['_id'])] = PV_search['name']
            return_data['plant : ' + PV_search['name']] = []

        # lgroup的搜尋
        if 'lgroup' in type_to_search:
            if search_type == 'plant':
                for lgroup in db['equipment'].find({'collection': 'pv_lgroup', 'PV': search_index_split['PV']}):
                    lgroup_dict[str(lgroup['_id'])] = lgroup['name']
                    return_data['lgroup : ' + lgroup['name']] = []
            else:
                for lgroup in db['equipment'].find({'collection': 'pv_lgroup', 'PV': search_index_split['PV'], 'name': search_index_split['lgroup']}):
                    lgroup_dict[str(lgroup['_id'])] = lgroup['name']
                    return_data['lgroup : ' + lgroup['name']] = []

        # 在return_data內新增項目
        # group的搜尋
        # group_data['plant_name'] + ' - ' + group_data['lgroup_name'] + ' : ' + 'group' + ' - ' + group_data['name']
        if 'group' in type_to_search:
            if search_type == 'plant':
                for group in db['equipment'].find({'collection': 'pv_group', 'PV': search_index_split['PV']}):
                    group_dict[str(group['_id'])] = {
                        'lgroup_name': group['lgroup'],
                        'name': group['name']
                    }
                    return_data['group : ' + group_dict[str(
                        group['_id'])]['name'] + ' @ ' + group_dict[str(group['_id'])]['lgroup_name']] = []
            elif search_type == 'lgroup':
                for group in db['equipment'].find({'collection': 'pv_group', 'PV': search_index_split['PV'], 'lgroup': search_index_split['lgroup']}):
                    group_dict[str(group['_id'])] = {
                        'lgroup_name': group['lgroup'],
                        'name': group['name']
                    }
                    return_data['group : ' + group_dict[str(
                        group['_id'])]['name'] + ' @ ' + group_dict[str(group['_id'])]['lgroup_name']] = []
            elif search_type == 'group':
                for group in db['equipment'].find({'collection': 'pv_group', 'PV': search_index_split['PV'], 'lgroup': search_index_split['lgroup'], 'name': search_index_split['group']}):
                    group_dict[str(group['_id'])] = {
                        'lgroup_name': group['lgroup'],
                        'name': group['name']
                    }
                    return_data['group : ' + group_dict[str(
                        group['_id'])]['name'] + ' @ ' + group_dict[str(group['_id'])]['lgroup_name']] = []

        # 在return_data內新增項目
        # inverter的搜尋
        if 'inverter' in type_to_search:
            if search_type == 'plant':
                for inverter in db['equipment'].find({'collection': 'inverter', 'PV': search_index_split['PV']}):
                    inverter_dict[str(inverter['_id'])] = {
                        'lgroup_name': inverter['lgroup'],
                        'group_name': inverter['group'],
                        'name': inverter['name']
                    }
                    return_data['inverter : ' + inverter_dict[str(inverter['_id'])]['name'] + ' @ ' + inverter_dict[str(
                        inverter['_id'])]['lgroup_name'] + ' - ' + inverter_dict[str(inverter['_id'])]['group_name']] = []
            elif search_type == 'lgroup':
                for inverter in db['equipment'].find({'collection': 'inverter', 'PV': search_index_split['PV'], 'lgroup': search_index_split['lgroup']}):
                    inverter_dict[str(inverter['_id'])] = {
                        'lgroup_name': inverter['lgroup'],
                        'group_name': inverter['group'],
                        'name': inverter['name']
                    }
                    return_data['inverter : ' + inverter_dict[str(inverter['_id'])]['name'] + ' @ ' + inverter_dict[str(
                        inverter['_id'])]['lgroup_name'] + ' - ' + inverter_dict[str(inverter['_id'])]['group_name']] = []
            elif search_type == 'group':
                for inverter in db['equipment'].find({'collection': 'inverter', 'PV': search_index_split['PV'], 'lgroup': search_index_split['lgroup'], 'group': search_index_split['group']}):
                    inverter_dict[str(inverter['_id'])] = {
                        'lgroup_name': inverter['lgroup'],
                        'group_name': inverter['group'],
                        'name': inverter['name']
                    }
                    return_data['inverter : ' + inverter_dict[str(inverter['_id'])]['name'] + ' @ ' + inverter_dict[str(
                        inverter['_id'])]['lgroup_name'] + ' - ' + inverter_dict[str(inverter['_id'])]['group_name']] = []

        # 在return_data內新增項目
        # sensor有案場共用的問題，所以先暫時把它直接設成順位第一的地方
        # sensor的搜尋
        if 'sensor' in type_to_search:
            if search_type == 'plant':
                for sensor in db['equipment'].find({'collection': 'sensor', 'PV': search_index_split['PV']}):
                    if type(sensor['lgroup']) == type([]):
                        sensor_dict[str(sensor['_id'])] = {
                            'lgroup_name': sensor['lgroup'][0],
                            'group_name': sensor['group'][0],
                            'name': sensor['name']
                        }
                    else:
                        sensor_dict[str(sensor['_id'])] = {
                            'lgroup_name': sensor['lgroup'],
                            'group_name': sensor['group'],
                            'name': sensor['name']
                        }
                    return_data['sensor : ' + sensor_dict[str(sensor['_id'])]['name'] + ' @ ' +
                                sensor_dict[str(sensor['_id'])]['lgroup_name'] + ' - ' + sensor_dict[str(sensor['_id'])]['group_name']] = []
            elif search_type == 'lgroup':
                for sensor in db['equipment'].find({'collection': 'sensor', 'PV': search_index_split['PV'], 'lgroup': search_index_split['lgroup']}):
                    if type(sensor['lgroup']) == type([]):
                        sensor_dict[str(sensor['_id'])] = {
                            'lgroup_name': sensor['lgroup'][0],
                            'group_name': sensor['group'][0],
                            'name': sensor['name']
                        }
                    else:
                        sensor_dict[str(sensor['_id'])] = {
                            'lgroup_name': sensor['lgroup'],
                            'group_name': sensor['group'],
                            'name': sensor['name']
                        }
                    return_data['sensor : ' + sensor_dict[str(sensor['_id'])]['name'] + ' @ ' +
                                sensor_dict[str(sensor['_id'])]['lgroup_name'] + ' - ' + sensor_dict[str(sensor['_id'])]['group_name']] = []
            elif search_type == 'group':
                for sensor in db['equipment'].find({'collection': 'sensor', 'PV': search_index_split['PV'], 'lgroup': search_index_split['lgroup'], 'group': search_index_split['group']}):
                    if type(sensor['lgroup']) == type([]):
                        sensor_dict[str(sensor['_id'])] = {
                            'lgroup_name': sensor['lgroup'][0],
                            'group_name': sensor['group'][0],
                            'name': sensor['name']
                        }
                    else:
                        sensor_dict[str(sensor['_id'])] = {
                            'lgroup_name': sensor['lgroup'],
                            'group_name': sensor['group'],
                            'name': sensor['name']
                        }
                    return_data['sensor : ' + sensor_dict[str(sensor['_id'])]['name'] + ' @ ' +
                                sensor_dict[str(sensor['_id'])]['lgroup_name'] + ' - ' + sensor_dict[str(sensor['_id'])]['group_name']] = []

        # 在return_data內新增項目
        # meter的搜尋
        if 'meter' in type_to_search:
            if search_type == 'plant':
                for meter in db['equipment'].find({'collection': 'pv_meter', 'PV': search_index_split['PV']}):
                    meter_dict[str(meter['_id'])] = {
                        'lgroup_name': str(meter['lgroup']),
                        'name': meter['name']
                    }
                    return_data['meter : ' + meter_dict[str(
                        meter['_id'])]['name'] + ' @ ' + meter_dict[str(meter['_id'])]['lgroup_name']] = []
            elif search_type == 'lgroup':
                for meter in db['equipment'].find({'collection': 'pv_meter', 'PV': search_index_split['PV'], 'lgroup': search_index_split['lgroup']}):
                    meter_dict[str(meter['_id'])] = {
                        'lgroup_name': str(meter['lgroup']),
                        'name': meter['name']
                    }
                    return_data['meter : ' + meter_dict[str(
                        meter['_id'])]['name'] + ' @ ' + meter_dict[str(meter['_id'])]['lgroup_name']] = []
            elif search_type == 'group':
                for meter in db['equipment'].find({'collection': 'pv_meter', 'PV': search_index_split['PV'], 'lgroup': search_index_split['lgroup'], 'group': search_index_split['group']}):
                    meter_dict[str(meter['_id'])] = {
                        'lgroup_name': str(meter['lgroup']),
                        'name': meter['name']
                    }
                    return_data['meter : ' + meter_dict[str(
                        meter['_id'])]['name'] + ' @ ' + meter_dict[str(meter['_id'])]['lgroup_name']] = []

        for time in return_data["time"]:
            for type_index in type_to_search:
                # lgroup
                if type_index == 'lgroup':
                    for lgroup_id, lgroup_name in lgroup_dict.items():
                        search_data = db['data_integrity'].find_one({'ID': lgroup_id, "time": datetime.datetime.strptime(
                            time, '%Y-%m-%d %H') + relativedelta.relativedelta(minutes=0, seconds=0)})
                        if search_data != None:
                            return_data['lgroup : ' + lgroup_name].append(
                                search_data['rate'])
                        else:
                            return_data['lgroup : ' + lgroup_name].append(None)
                # plant
                elif type_index == 'plant':
                    for PV_id, PV_name in PV_dict.items():
                        search_data = db['data_integrity'].find_one({'ID': PV_id, "time": datetime.datetime.strptime(
                            time, '%Y-%m-%d %H') + relativedelta.relativedelta(minutes=0, seconds=0)})

                        if search_data != None:
                            return_data['plant : ' +
                                        PV_name].append(search_data['rate'])
                        else:
                            return_data['plant : ' + PV_name].append(None)
                    # inverter
                elif type_index == 'inverter':
                    for inverter_id, inverter_data in inverter_dict.items():
                        search_data = db['data_integrity'].find_one({'ID': inverter_id, "time": datetime.datetime.strptime(
                            time, '%Y-%m-%d %H') + relativedelta.relativedelta(minutes=0, seconds=0)})
                        if search_data != None:
                            return_data['inverter : ' + inverter_data['name'] + ' @ ' + inverter_data['lgroup_name'] + ' - ' + inverter_data['group_name']].append(
                                search_data['rate'])
                        else:
                            return_data['inverter : ' + inverter_data['name'] + ' @ ' +
                                        inverter_data['lgroup_name'] + ' - ' + inverter_data['group_name']].append(None)
                    # meter
                elif type_index == 'meter':
                    for meter_id, meter_data in meter_dict.items():
                        search_data = db['data_integrity'].find_one({'ID': meter_id, "time": datetime.datetime.strptime(
                            time, '%Y-%m-%d %H') + relativedelta.relativedelta(minutes=0, seconds=0)})
                        if search_data != None:
                            return_data['meter : ' + meter_data['name'] + ' @ ' +
                                        meter_data['lgroup_name']].append(search_data['rate'])
                        else:
                            return_data['meter : ' + meter_data['name'] +
                                        ' @ ' + meter_data['lgroup_name']].append(None)
                    # group
                elif type_index == 'group':
                    for group_id, group_data in group_dict.items():
                        search_data = db['data_integrity'].find_one({'ID': group_id, "time": datetime.datetime.strptime(
                            time, '%Y-%m-%d %H') + relativedelta.relativedelta(minutes=0, seconds=0)})
                        if search_data != None:
                            return_data['group : ' + group_data['name'] + ' @ ' +
                                        group_data['lgroup_name']].append(search_data['rate'])
                        else:
                            return_data['group : ' + group_data['name'] +
                                        ' @ ' + group_data['lgroup_name']].append(None)
                # sensor
                elif type_index == 'sensor':
                    for sensor_id, sensor_data in sensor_dict.items():
                        search_data = db['data_integrity'].find_one({'ID': sensor_id, "time": datetime.datetime.strptime(
                            time, '%Y-%m-%d %H') + relativedelta.relativedelta(minutes=0, seconds=0)})
                        if search_data != None:
                            return_data['sensor : ' + sensor_data['name'] + ' @ ' + sensor_data['lgroup_name'] + ' - ' + sensor_data['group_name']].append(
                                search_data['rate'])
                        else:
                            return_data['sensor : ' + sensor_data['name'] + ' @ ' +
                                        sensor_data['lgroup_name'] + ' - ' + sensor_data['group_name']].append(None)
                else:
                    return bad_request(400, 'Bad request. {}'.format(e))

                output_data = {
                    "data": return_data
                }
        # print(return_data)
        return successful_request({'data': output_data})
    except Exception as e:
        print(exception_detail(e))
        return bad_request(400, 'Bad request. {}'.format(e))

# -------------------------------------------------------------------------------
# 使用位置 setting
# 資料庫優化 by碩庭 20220806


@application_taipower.route('/setting/database_optimize', methods=['POST'])
def database_optimize():
    user, db = check_user()
    if(db == None):
        return logout()
    request_dict = request.json
    try:
        # 設定要優化的collection
        collection_to_optimize = [
            'inverter',
            'inverter_cal',
            'inverter_training',
            'irrh_cal',
            'meter_cal',
            'pv_plant',
            'pv_lgroup',
            'pv_group',
            'pr_cal',
            'sensor',
            'string_meter',
            'sun_forcast',
            'temp_cal',
            'alarm',
            'digital_twin_output',
            'generation_forecast'
        ]
        collection_data = []

        # 第一次加載網頁的動作(跟refresh一樣)
        if request_dict['function_type'] == 'first_load':
            db_storage_size_kb = db.command('dbstats')['storageSize']
            db_storage_size_mb = int(db_storage_size_kb / 1048576)

            for col in collection_to_optimize:
                for i in db[col].find().sort([('time', 1)]).limit(1):
                    Oldest_data = i

                collection_data.append({
                    'name': col,
                    'Size': int(db.command('collstats', col)['storageSize'] / 1024 / 1024),
                    'Oldest_data': Oldest_data['time'],
                    'Count': db.command('collstats', col)['count']
                })

            return_data = {
                'host': os.getenv('MONGODB_HOSTNAME'),
                'port': os.getenv('MONGODB_PORT'),
                'space_usage': db_storage_size_mb,
                'collection_data': collection_data,
                'max_usage_to_show': db['users'].find_one({'username': user[0]})['max_usage']
            }

            # print(return_data)

            # 暫時加入的插入用來模擬刪除的資料的功能
            # for i in range(500):
            #     db['delete_test_col'].insert_one({
            #         'test value': i,
            #         'time': datetime.datetime(2017, 1, 1) + datetime.timedelta(i)
            #     })
            return successful_request(return_data)

        # 按下refresh的動作
        elif request_dict['function_type'] == 'refresh':
            db_storage_size_kb = db.command('dbstats')['storageSize']
            db_storage_size_mb = int(db_storage_size_kb / 1048576)

            for col in collection_to_optimize:
                for i in db[col].find().sort([('time', 1)]).limit(1):
                    Oldest_data = i

                collection_data.append({
                    'name': col,
                    'Size': int(db.command('collstats', col)['storageSize'] / 1024 / 1024),
                    'Oldest_data': Oldest_data['time'],
                    'Count': db.command('collstats', col)['count']
                })

            return_data = {
                'host': os.getenv('MONGODB_HOSTNAME'),
                'port': os.getenv('MONGODB_PORT'),
                'space_usage': db_storage_size_mb,
                'collection_data': collection_data,
                'max_usage_to_show': db['users'].find_one({'username': user[0]})['max_usage']
            }

            # print(return_data)

            # 暫時加入的插入用來模擬刪除的資料的功能
            # for i in range(500):
            #     db['delete_test_col'].insert_one({
            #         'test value': i,
            #         'time': datetime.datetime(2017, 1, 1) + datetime.timedelta(i)
            #     })

            return successful_request(return_data)

        # 按下優化的動作
        elif request_dict['function_type'] == 'optimize':
            # !!優化條件!!
            delete_query = {
                'time': {'$lt': datetime.datetime.today() - datetime.timedelta(365*5)}
            }
            for col in collection_to_optimize:
                delete_data = db[col].delete_many(delete_query)
                # print刪除筆數
                # print(delete_data.deleted_count)
            return successful_request()

        # 按下設定最大容量的動作
        elif request_dict['function_type'] == 'set_max_usage':
            update_query = {
                'username': user[0]
            }
            update_data = {
                '$set': {
                    'max_usage': int(request_dict['max_usage'])
                }
            }
            update = db['users'].update_one(
                update_query, update_data)

            # print(update.acknowledged)

            return successful_request()

    except Exception as e:
        print(exception_detail(e))
        return bad_request(400, 'Bad request. {}'.format(e))

# -------------------------------------------------------------------------------
# 使用位置 setting
# 設備新增 by碩庭 20220830


@application_taipower.route('/setting/equipment_manage', methods=['POST', 'GET'])
def equipment_manage():
    user, db = check_user()
    if db == None:
        return logout()
    find_user = find_user_from_current_user()
    user_c = list(db.users.find({"user_id": find_user}))[0]
    request_dict = request.json
    try:
        print(request_dict)
        equipment_data = []
        for equipment in db['equipment'].aggregate([{'$match': {'PV': request_dict['station']['name'],'collection':{'$in':request_dict['type_checked']}}}, {'$sort': {'collection': 1, 'name': 1}}]):
            equipment['ID'] = str(equipment['_id'])
            del equipment['_id']
            equipment_data.append(equipment)

        return_data = {
            'data': equipment_data
        }
        return successful_request(return_data)
    except Exception as e:
        print(exception_detail(e))
        return bad_request(400, 'Bad request. {}'.format(e))

# -------------------------------------------------------------------------------
# 使用位置 setting
# 設備新增 - 刪除指定設備 by碩庭 20220831


@application_taipower.route('/setting/equipment_manage/delete', methods=['POST', 'GET'])
def equipment_manage_delete():
    user, db = check_user()
    if db == None:
        return logout()
    find_user = find_user_from_current_user()
    user_c = list(db.users.find({"user_id": find_user}))[0]
    request_dict = request.json
    try:
        del_data = db['equipment'].find_one(
            {'_id': ObjectId(request_dict['id'])})
        del_data['del_time'] = datetime.datetime.now()
        if del_data != None:
            if db['equipment_del_backup'].find_one({'_id': ObjectId(request_dict['id'])}) == None:
                db['equipment_del_backup'].insert_one(del_data)
            else:
                db['equipment_del_backup'].delete_one(
                    {'_id': ObjectId(request_dict['id'])})
                db['equipment_del_backup'].insert_one(del_data)
            db['equipment'].delete_one({'_id': ObjectId(request_dict['id'])})
        else:
            return bad_request(400, 'Bad request. {}'.format('did not find del_data'))
        return successful_request()
    except Exception as e:
        print(exception_detail(e))
        return bad_request(400, 'Bad request. {}'.format(e))

# -------------------------------------------------------------------------------
# 使用位置 setting
# 力暘能源展測試程式 by碩庭 20220919

@application_taipower.route('/setting/ysolar_test', methods=['POST', 'GET'])
def ysolar_test():
    user, db = check_user()
    if db == None:
        return logout()
    find_user = find_user_from_current_user()
    user_c = list(db.users.find({"user_id": find_user}))[0]
    request_dict = request.json
    try:
        url = "https://www.jiadong.solar.paets.com.tw/ysolarreq_api/get_station_day_data"
        payload = json.dumps({
        "name_list": [
            "天權",
            "玉衡",
            "開陽",
            "瑤光"
        ]
        })
        headers = {
            'Authorization': 'Bearer eyJhbGciOiJIUzUxMiIsImlhdCI6MTY2NTM4NDM0OSwiZXhwIjoxNjk2OTIwMzQ5fQ.eyJkYiI6InB2IiwidXNlcm5hbWUiOiJwdiJ9.eWlsV9u7404aMu6Y5YHCSuqbGNR8Yh73LdsT_OCmE03jlX-5tP7ndnQmtR1lQZCUSl87CGEH4J9AVyBb1ui4cA',
            'Access-Control-Allow-Origin': '*',
            'Content-Type': 'application/json'
        }
        response = requests.request("POST", url, headers=headers, data=payload)
        response_decode = json.loads(response.text)
        response_decode['date'] = str(datetime.date.today())
        # 計算plot用的發電量list
        plot_today_kwh_dict = {}
        for station in response_decode['data']:
            kwh_time_list = []
            kwh_kwh_list = []
            for data in response_decode['data'][station]['kwh']:
                # print(datetime.datetime.fromtimestamp(data['time']).strftime('%Y-%m-%d %H:%M:%S'))
                kwh_time_list.append(datetime.datetime.fromtimestamp(data['time']).strftime('%Y-%m-%d %H:%M:%S'))
                kwh_kwh_list.append(data['value'])
            plot_today_kwh_dict[station] = {
                'time':kwh_time_list,
                'kwh':kwh_kwh_list
            }
        response_decode['plot_today_kwh_dict'] = plot_today_kwh_dict
        db['ysolar_data'].update_one({'date':str(datetime.date.today())},{'$set':response_decode} ,upsert = True)
        last_day_data = db['ysolar_data'].find_one({'date':str(datetime.date.today() - datetime.timedelta(days=1))})
        # 兩個案場的日總和發電量，計算全年發電量用
        kwh_station_total = 0
        for station in last_day_data['data']:
            for need_caculate in last_day_data['data'][station]:
                # 確定要計算的地方
                if need_caculate == 'kwh':
                    kwh_total = 0
                    for kwh in  last_day_data['data'][station]['kwh']:
                        if kwh['value'] == None:
                            kwh_total = kwh_total + 0
                        else:
                            kwh_total = kwh_total + float(kwh['value'])
                    kwh_station_total = kwh_station_total + kwh_total
                    
        # 計算年發電量
        kwh_threshold = [0.913,0.939,0.943,0.976,0.913,0.827,0.974,0.894,0.923,1,0.936,0.874]
        kwh_whole_year = []
        for value in kwh_threshold:
            kwh_whole_year.append(value * kwh_station_total * 30)
        # response_decode['kwh_whole_year'] = kwh_whole_year
        kwh_whole_year = [4156000,4749500,5813500,6216500,5305500,5389000,6972000,6237500,5069500,5034000,4553000,3937000]
        response_decode['kwh_whole_year'] = kwh_whole_year
        
        
        # 計算案場歷史總發電量、減碳量
        kwh_history = response_decode['data']['天權']['kwh_total'] + response_decode['data']['玉衡']['kwh_total']
        co2_reduce = round(kwh_history*0.554,2)
        kwh_history = round((kwh_history/1000),2)
        response_decode['kwh_history'] = kwh_history
        response_decode['co2_reduce'] = co2_reduce
        
        #設定要抓哪個小時的資料
        hour = datetime.datetime.now().hour
        
        # 設定顯示昨日DMY統計之LIST
        dmy_list = [0,0,0,0,0,0]
        station_dmy_list = []
        station_dmy_total_list = [last_day_data['data']['天權']['dmy'],last_day_data['data']['玉衡']['dmy']]
        for station_dmy in station_dmy_total_list:
            sum = 0
            for data in station_dmy:
                if data['value'] != None:
                    sum = sum + data['value']
            station_dmy_list.append(sum)
        for dmy in station_dmy_list:
            if dmy >0 and dmy<=1:
                dmy_list[0] = dmy_list[0] + 1
            elif dmy > 1 and dmy <=2:
                dmy_list[1] = dmy_list[1] + 1
            elif dmy > 2 and dmy <=3:
                dmy_list[2] = dmy_list[2] + 1
            elif dmy > 3 and dmy <=4:
                dmy_list[3] = dmy_list[3] + 1
            elif dmy > 4 and dmy <=5:
                dmy_list[4] = dmy_list[4] + 1
            elif dmy > 5 and dmy <=6:
                dmy_list[5] = dmy_list[5] + 1
            else:
                dmy_list[0] = dmy_list[0] + 1
        response_decode['dmy_list'] = dmy_list
        
        # 設定顯示PR統計之LIST 
        pr_list = [0,0,0,0,0,0,0,0,0,0]
        station_pr_list = []
        station_pr_total_list = [last_day_data['data']['天權']['pr'][hour-1],last_day_data['data']['玉衡']['pr'][hour-1]]
        for pr in station_pr_total_list:
            if pr['value'] == None:
                pr_list[0] = pr_list[0] + 1
            elif pr['value'] >0 and pr['value']<=10:
                pr_list[0] = pr_list[0] + 1
            elif pr['value'] > 10 and pr['value'] <=20:
                pr_list[1] = pr_list[1] + 1
            elif pr['value'] > 20 and pr['value'] <=30:
                pr_list[2] = pr_list[2] + 1
            elif pr ['value']> 30 and pr['value'] <=40:
                pr_list[3] = pr_list[3] + 1
            elif pr['value'] > 40 and pr['value'] <=50:
                pr_list[4] = pr_list[4] + 1
            elif pr['value'] > 50 and pr['value'] <=60:
                pr_list[5] = pr_list[5] + 1
            elif pr['value'] > 60 and pr['value'] <=70:
                pr_list[6] = pr_list[6] + 1
            elif pr['value'] > 70 and pr['value'] <=80:
                pr_list[7] = pr_list[7] + 1
            elif pr['value'] > 80 and pr['value'] <=90:
                pr_list[8] = pr_list[8] + 1
            elif pr['value'] > 90 and pr['value'] <=100:
                pr_list[9] = pr_list[9] + 1
            else:
                pr_list[9] = pr_list[9] + 1
        response_decode['pr_list'] = pr_list
        
        # 彰化銀行之月分別用電量
        CHB_Bill_kwh = [161400,154800,198800,196000,234800,236000,260400,256400,250400,218800,207600,192000]
        response_decode['CHB_Bill_kwh'] = CHB_Bill_kwh
        
        # 彰化銀行之餘電量
        CHB_left_kwh = [kwh_whole_year[i] - CHB_Bill_kwh[i] for i in range(len(kwh_whole_year))]
        response_decode['CHB_left_kwh'] = CHB_left_kwh
        
        #設定已回傳之boolean
        response_decode['get_data_done'] = True
        # 檢查資料
        # for key in response_decode:
        #     print(key,':',response_decode[key])
        return successful_request(response_decode)
    except Exception as e:
        print(exception_detail(e))
        return bad_request(400, 'Bad request. {}'.format(e))
    
# -------------------------------------------------------------------------------
# 使用位置 setting
# 力暘能源展測試程式 by碩庭 20220919

@application_taipower.route('/setting/get_ysolar_energy_storage', methods=['POST', 'GET'])
def get_ysolar_energy_storage():
    user, db = check_user()
    if db == None:
        return logout()
    find_user = find_user_from_current_user()
    user_c = list(db.users.find({"user_id": find_user}))[0]
    request_dict = request.json
    try:
        client = pymongo.MongoClient('mongodb://140.118.171.30:22217')
        database = client['AFC']
        col_info = database['info']
        col_SPM = database['SPM']
        stationID_HanYang = "Ysolar_HanYang"
        stationID_TianShu = "Ysolar_TianShu"
        stationID_TianXuan =  "Ysolar_TianXuan"
        timeflag_today = datetime.datetime.now()
        timeflag_last24hour = timeflag_today - datetime.timedelta(days=1)

        return_data = {}
        # 設定已回傳boolean
        return_data['get_data_done'] = True
        
        # 頁面切換時，需要1：各案場最近一筆info、最近一筆SPM
        if request_dict['method'] == 'normal':
            # 韓暘info、計算RTE
            HanYang_info = col_info.find({'ID':stationID_HanYang}).sort('time',-1).limit(1)
            for data in HanYang_info:
                rte = data['vab_acm']['exp_kwh'] / data['vab_acm']['imp_kwh']
                data['rte'] = rte
                del data['_id']
                return_data['HanYang_info'] = data
            # 天樞info、計算RTE
            TianShu_info = col_info.find({'ID':stationID_TianShu}).sort('time',-1).limit(1)
            for data in TianShu_info:
                rte = data['vab_acm']['exp_kwh'] / data['vab_acm']['imp_kwh']
                data['rte'] = rte
                del data['_id']
                return_data['TianShu_info'] = data
            # 天璇info、計算RTE
            TianXuan_info = col_info.find({'ID':stationID_TianXuan}).sort('time',-1).limit(1)
            for data in TianXuan_info:
                rte = data['vab_acm']['exp_kwh'] / data['vab_acm']['imp_kwh']
                data['rte'] = rte
                del data['_id']
                return_data['TianXuan_info'] = data
            # 韓暘SPM
            HanYang_SPM = col_SPM.find({'ID':stationID_HanYang}).sort('time',-1).limit(1)
            for data in HanYang_SPM:
                del data['_id']
                return_data['HanYang_info']['SPM'] = data['SPM']
            # 天樞SPM
            TianShu_SPM = col_SPM.find({'ID':stationID_TianShu}).sort('time',-1).limit(1)
            for data in TianShu_SPM:
                del data['_id']
                return_data['TianShu_info']['SPM'] = data['SPM']
            # 天璇SPM
            TianXuan_SPM = col_SPM.find({'ID':stationID_TianXuan}).sort('time',-1).limit(1)
            for data in TianXuan_SPM:
                del data['_id']
                return_data['TianXuan_info']['SPM'] = data['SPM']
            # 計算每小時AFC執行率之LIST
            # 0~70、70~75、75~85、85~95、95~100、sum_of_station
            spm_list = [return_data['HanYang_info']['SPM'],return_data['TianShu_info']['SPM'],return_data['TianXuan_info']['SPM']]
            afc_list = [0,0,0,0,0,0]
            for spm in spm_list:
                if spm < 0.7 or spm == None:
                    afc_list[0] = afc_list[0] + 1
                    afc_list[5] = afc_list[5] + 1
                elif spm < 0.75 and spm >= 0.7:
                    afc_list[1] = afc_list[1] + 1
                    afc_list[5] = afc_list[5] + 1
                elif spm < 0.85 and spm >= 0.75:
                    afc_list[2] = afc_list[2] + 1
                    afc_list[5] = afc_list[5] + 1
                elif spm < 0.95 and spm >= 0.85:
                    afc_list[3] = afc_list[3] + 1
                    afc_list[5] = afc_list[5] + 1
                elif spm < 1 and spm >= 0.95:
                    afc_list[4] = afc_list[4] + 1
                    afc_list[5] = afc_list[5] + 1
                else:
                    print('spm value error, let it equal 1 afc')
                    afc_list[4] = afc_list[4] + 1
                    afc_list[5] = afc_list[5] + 1
            return_data['afc_list'] = afc_list
            # 檢查資料
            for data in return_data:
                print(return_data[data])
            # 打過去前端
            return successful_request(return_data)
        
        
        # 各案場之SBSPM
        elif request_dict['method'] == 'click_TianXuan':
            find_data_TianXuan = col_info.find({'ID':stationID_TianXuan , 'time':{'$gte':timeflag_last24hour}})
            station_sbspm = []
            station_sbspm_time = []
            for data in find_data_TianXuan:
                station_sbspm.append(data['system']['SBSPM'])
                station_sbspm_time.append(data['time'])
            return_data['station_sbspm'] = station_sbspm
            return_data['station_sbspm_time'] = station_sbspm_time
            return successful_request(return_data)
        elif request_dict['method'] == 'click_TianXuan':
            find_data_HanYang = col_info.find({'ID':stationID_HanYang , 'time':{'$gte':timeflag_last24hour}})
            station_sbspm = []
            station_sbspm_time = []
            for data in find_data_HanYang:
                station_sbspm.append(data['system']['SBSPM'])
                station_sbspm_time.append(data['time'])
            return_data['station_sbspm'] = station_sbspm
            return_data['station_sbspm_time'] = station_sbspm_time
            return successful_request(return_data)
        elif request_dict['method'] == 'click_TianXuan':
            find_data_TianShu = col_info.find({'ID':stationID_TianShu , 'time':{'$gte':timeflag_last24hour}})
            station_sbspm = []
            station_sbspm_time = []
            for data in find_data_TianShu:
                station_sbspm.append(data['system']['SBSPM'])
                station_sbspm_time.append(data['time'])
            return_data['station_sbspm'] = station_sbspm
            return_data['station_sbspm_time'] = station_sbspm_time
            
            
            return successful_request(return_data)
        else:
            return bad_request(400, 'Bad request. {}'.format(e))
    except Exception as e:
        print(exception_detail(e))
        return bad_request(400, 'Bad request. {}'.format(e))