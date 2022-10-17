# 台電 Vue 專用API
# 主程式功能
# Flask App 函式
from app_common import successful_request, bad_request, exception_detail, check_user, logout, find_user_from_current_user
#-------------------------------------------------------------------------------
# Libiary
from flask import Blueprint, request, jsonify, views, current_app
from bson import ObjectId
from werkzeug.utils import secure_filename
import datetime
import os
import shutil # ziping
import math
#-------------------------------------------------------------------------------
# 通用函式與功能
import current as c
import report_gen as r
import prepareplot as t
#======================================================================================================
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'PNG', 'jpg', 'JPG', 'jpeg', 'JPEG', 'html', 'HTML',
'jgw', 'JGW', 'tfw', 'TFW', 'shp', 'SHP', 'dbf', 'DBF', 'dxf', 'DXF', 'tiff', 'TIFF', 'tif', 'TIF'])
#-------------------------------------------------------------------------------
# IR Image Processing Server IP
IR_image_server = os.getenv('ir_image_server_ip', 'http://140.118.172.245:5000')
#======================================================================================================
# application_99M is a Blueprint of flask
# Learn More About Blueprint At
# https://flask.palletsprojects.com/en/2.0.x/blueprints/
application_99M = Blueprint('application_99M', __name__)
#======================================================================================================
#使用位置 派工 /dispatch
@application_99M.route('/ID_get_alarm_data', methods=['POST'])
def ID_get_alarm_data():
    user, db = check_user()
    if db == None:
        return logout()
    request_dict = request.json
    print(request_dict)
    try:
        alarmIDList = request_dict['alarmIDList']
        if not isinstance(alarmIDList, list):
            return bad_request(400, 'Bad Request. alarmIDLIst must be list.')
    except:
        return bad_request(400, 'Bad Request. No alarmIDList')
    equip_dict = {}
    for plant in db.plant.find({}):
        equip_dict[str(plant['_id'])] = plant
    for equip in db.equipment.find({}):
        equip_dict[str(equip['_id'])] = equip
    for iot in db.iot.find({}):
        iot['type'] = 'iot'
        equip_dict[str(iot['_id'])] = iot
    #print(equip_dict)
    return_list = []
    error_list = []
    # Get alarm_cause
    alarm_cause_list = []
    group_dict = {}
    for alarm_cause in db.alarm_cause.find({'show': 1}):
        try:
            if alarm_cause['alarm_group'] not in group_dict:
                group_dict[alarm_cause['alarm_group']] = []
            group_dict[alarm_cause['alarm_group']].append({
                'ID': str(alarm_cause['_id']),
                'name': alarm_cause['event'],
                'select': False
            })
        except:
            pass
    for key in group_dict:
        alarm_cause_list.append({
            'name': key,
            'check': False,
            'children': group_dict[key]
        })
    for alarm_ID in alarmIDList:
        try:
            alarm_data = db.alarm.find_one({'_id': ObjectId(alarm_ID)})
            alarm_data['ID_data'] = {
                'name': equip_dict[alarm_data['ID']]['name'],
                'type': equip_dict[alarm_data['ID']]['type'],
                'station': None,
            }
            if 'PV' not in  equip_dict[alarm_data['ID']]:
                alarm_data['ID_data']['station'] = equip_dict[alarm_data['ID']]['name']
            else:
                alarm_data['ID_data']['station'] = equip_dict[alarm_data['ID']]['PV']
                if 'lgroup' not in equip_dict[alarm_data['ID']] and  equip_dict[alarm_data['ID']]['type'] == 'pv_lgroup':
                    alarm_data['ID_data']['station'] += '/{}'.format(equip_dict[alarm_data['ID']]['name'])
                elif 'lgroup' in equip_dict[alarm_data['ID']]:
                    alarm_data['ID_data']['station'] += '/{}'.format(equip_dict[alarm_data['ID']]['lgroup'][0] if isinstance(equip_dict[alarm_data['ID']]['lgroup'][0], list) else equip_dict[alarm_data['ID']]['lgroup'])
                    if 'group' not in equip_dict[alarm_data['ID']] and  equip_dict[alarm_data['ID']]['type'] == 'pv_group':
                        alarm_data['ID_data']['station'] += '/{}'.format(equip_dict[alarm_data['ID']]['name'])
                    elif 'group' in equip_dict[alarm_data['ID']]:
                        alarm_data['ID_data']['station'] += '/{}'.format(equip_dict[alarm_data['ID']]['group'][0] if isinstance(equip_dict[alarm_data['ID']]['group'][0], list) else equip_dict[alarm_data['ID']]['group'])
            # transform data
            for key in alarm_data:
                if key == '_id':
                    alarm_data[key] = str(alarm_data[key]) 
                elif isinstance(alarm_data[key], datetime.date):
                    alarm_data[key] = datetime.datetime.strftime(alarm_data[key], '%Y-%m-%d %H:%M:%S') 
            alarm_data['alarm_cause'] = alarm_cause_list  
            return_list.append(alarm_data)
            
        except Exception as e:
            error_list.append({'_id': alarm_ID, 'error': str(exception_detail(e))})
    return successful_request({
        'data': return_list,
        'error': error_list
    })
#-------------------------------------------------------------------------------
#使用位置 派工 /dispatch
@application_99M.route('/save_dispatch', methods=['POST'])
def save_dispatch():
    user, db = check_user()
    if db == None:
        return logout()
    request_dict = request.json
    print(request_dict)
    try:
        infos = request_dict['infos']
        ID = request_dict['ID']
        dispatch_type = request_dict.get("type", "A")
        show = request_dict.get('show', 1)
        alarmData = []
        for alarm in request_dict['alarmData']:
            alarmData.append({
                'ID': alarm['ID'],
                'alarm_cause': alarm['alarm_cause_selected_ID'],
                'repair_data': [],
            })
        if '_id' not in infos or infos['_id'] == None:    # New Dispatch
            today = datetime.datetime.today()
            dispatch_count = db.dispatch.count_documents({'ID': ID, 'time': {'$gte': datetime.datetime.strptime(datetime.datetime.strftime(today, '%Y-%m'),'%Y-%m')}})
            lgroup_data = db.equipment.find_one({'_id': ObjectId(ID)})
            name = '{}_{}_A_{}_{}'.format(lgroup_data['PV'], lgroup_data['name'], datetime.datetime.strftime(today, '%Y-%m'), dispatch_count + 1)  
            result = db.dispatch.insert_one({
                'ID': ID, 'time': datetime.datetime.now(), 'dispatch_time': datetime.datetime.strptime(infos['date'][:10],'%Y-%m-%d') + datetime.timedelta(days=1) if show == 1 else None,
                'name': name, 'alarmData': alarmData, 'show': show,
                'worker_contact': {'name': request_dict.get('worker_contact', {}).get('name', ''), 'TEL': request_dict.get('worker_contact', {}).get('TEL', '')},
                'client_contact': {'name': request_dict.get('client_contact', {}).get('name', ''), 'TEL': request_dict.get('client_contact', {}).get('TEL', '')},
                'type': dispatch_type
            })
    except Exception as e:
        print(exception_detail(e))
        return bad_request(400, 'Bad Request. {}'.format(exception_detail(e)))
    return successful_request({'_id': str(result.inserted_id)})
#-------------------------------------------------------------------------------
#使用位置 派工 /dispatch
@application_99M.route('/dispatch_get', methods=['POST'])
def dispatch_get():
    user, db = check_user()
    if db == None:
        return logout()
    find_user = find_user_from_current_user()
    user_c=list(db.users.find({"user_id" : find_user}))[0]

    request_dict = request.json
    #print(request_dict)
    show = request_dict.get('show', 1)
    dispatch_filter = {'show': show}
    ID_list = request_dict.get('ID_list', [])
    col_list = request_dict.get('col_list', [])

    if request_dict.get('time', {}).get('mode', '') == 'single':
        try:
            start_date = datetime.datetime.strptime(request_dict['time']['start_date'], '%Y-%m-%d')
            end_date = start_date + datetime.timedelta(days=1)
            dispatch_filter['dispatch_time'] = {'$gte': start_date, '$lt': end_date}
        except Exception as e:
            return bad_request(400, 'Time error. {}'.format(exception_detail(e)))
    elif request_dict.get('time', {}).get('mode', '') == 'interval':
        try:
            start_date = datetime.datetime.strptime(request_dict['time']['start_date'], '%Y-%m-%d')
            end_date = datetime.datetime.strptime(request_dict['time']['end_date'], '%Y-%m-%d')
            dispatch_filter['dispatch_time'] = {'$gte': start_date, '$lt': end_date+datetime.timedelta(days=1)}
        except:
            return bad_request(400, 'Time error')
    elif request_dict.get('time', {}).get('mode', '') in ['today', 'week', 'month', 'year']:
        today =datetime.datetime.today()
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
        
    if show == 2 and 'dispatch_time' in dispatch_filter: # 暫存
        dispatch_filter['time'] = dispatch_filter['dispatch_time']
        dispatch_filter.pop('dispatch_time', None)
    plant_filter = {}
    if user_c['plant'][0] != 'total':
        for i in user_c['plant']:
            if 'name' not in plant_filter:
                plant_filter['name'] = {'$in': []}
            plant_filter['name']['$in'].append(i)
    for plant in db.plant.find(plant_filter):
        ID_list.append(str(plant['_id']))
        col_list.append(str(plant['collection']))
    
    dispatch_filter['ID'] = []
    plant_trans = {}
    dispatch_level = "pv_lgroup"
    try:
        for i, col in enumerate(col_list):
            if col == 'pv_plant':
                for plant in db.plant.find({'_id': ObjectId(ID_list[i])}):
                    if dispatch_level == 'PV' or dispatch_level == 'plant':
                        dispatch_filter['ID'].append(str(plant['_id']))
                        plant_trans[str(plant['_id'])] = plant.get('name')
                    elif dispatch_level == 'lgroup' or dispatch_level == 'pv_lgroup':
                        for lgroup in db.equipment.find({'PV': plant.get('name'), 'type': 'pv_lgroup'}):
                            dispatch_filter['ID'].append(str(lgroup['_id']))
                            plant_trans[str(lgroup['_id'])] = '{}\\{}'.format(plant.get('name'), lgroup.get('name'))
                    else: # group
                        for group in db.equipment.find({'PV': plant.get('name'), 'type': 'pv_group'}):
                            dispatch_filter['ID'].append(str(group['_id']))
                            plant_trans[str(group['_id'])] = '{}\\{}\\{}'.format(plant.get('name'), group.get('lgroup'), group.get('name'))
            elif col == 'pv_lgroup':
                for lgroup in db.equipment.find({'_id': ObjectId(ID_list[i])}):
                    for plant in db.plant.find({'name': lgroup.get('PV', None)}):
                        if dispatch_level == 'PV' or dispatch_level == 'plant':
                            dispatch_filter['ID'].append(str(plant['_id']))
                            plant_trans[str(plant['_id'])] = plant.get('name')
                        elif dispatch_level == 'lgroup' or dispatch_level == 'pv_lgroup':
                            dispatch_filter['ID'].append(str(lgroup['_id']))
                            plant_trans[str(lgroup['_id'])] = '{}\\{}'.format(lgroup.get('PV'), lgroup.get('name'))
                        else:
                            for group in db.equipment.find({'PV': group.get('PV'), 'lgroup': lgroup.get('name'), 'type': 'pv_group'}):
                                dispatch_filter['ID'].append(str(group['_id']))
                                plant_trans[str(group['_id'])] = '{}\\{}\\{}'.format(group.get('PV'), group.get('lgroup'), group.get('name'))

            else:  #group
                for group in db.equipment.find({'_id': ObjectId(ID_list[i])}):
                    for plant in db.plant.find({'name': group.get('PV', None)}):
                        if dispatch_level == 'PV' or dispatch_level == 'plant' or dispatch_level == 'pv_plant':
                            dispatch_filter['ID'].append(str(plant['_id']))
                            plant_trans[str(plant['_id'])] = plant.get('name')
                        elif dispatch_level == 'lgroup' or dispatch_level == 'pv_lgroup' or dispatch_level == 'pv_lgroup':
                            for lgroup in db.equipment.find({'PV': group.get('PV'), 'name': group.get('lgroup'), 'type': 'pv_lgroup'}):
                                dispatch_filter['ID'].append(str(lgroup['_id']))
                                plant_trans[str(lgroup['_id'])] = '{}\\{}'.format(lgroup.get('PV'), lgroup.get('name'))
                        else:
                            dispatch_filter['ID'].append(str(group['_id']))
                            plant_trans[str(group['_id'])] = '{}\\{}\\{}'.format(group.get('PV'), group.get('lgroup'), group.get('name'))
        dispatch_filter['ID'] = {'$in': dispatch_filter['ID']}
    except Exception as e:
        return bad_request(500, 'Internal Server Error. {}'.format(exception_detail(e)))


    dispatch_list = []
    print(dispatch_filter)
    for dispatch in db.dispatch.find(dispatch_filter):
        try:
            dispatch['_id'] = str(dispatch['_id'])
            dispatch['station_name'] = plant_trans[dispatch['ID']]
            dispatch['time'] = datetime.datetime.strftime(dispatch['time'], '%Y-%m-%d %H:%M:%S')
            try:
                dispatch['dispatch_time'] = datetime.datetime.strftime(dispatch['dispatch_time'], '%Y-%m-%d %H:%M:%S')
            except:
                pass
            dispatch['type'] = {'A': '警報檢修', 'B': '定檢', 'C': '清洗'}.get(dispatch.get('type', 'A'), 'A')
            dispatch_list.append(dispatch)
        except:
            continue
    return successful_request({'dispatch_list': dispatch_list})
#-------------------------------------------------------------------------------
#使用位置  /stationList 電站管理 設備資訊
#取得io須顯示資料
@application_99M.route('/pv_io_data', methods=['POST'])
def pv_io_data():
    user,db = check_user()
    if(db == None):
        return logout() 
    request_dict = request.json
    try:
        io_ID = request_dict['io_ID']
        ObjectId(io_ID)    # Just check if id vaild
    except:
        return bad_request(400, 'Bad Request. io_ID error.')
    
    first = request_dict.get('first', True)
    io_data = c.current_data(db,'pv_io',io_ID)[0]
    state_data = c.current_state(db,io_ID)[0].get('state')
    io_data['state'] = state_data
    if(first == True):
        equip_data = c.current_equip(db,io_ID)[0]

    return successful_request({
        'io_data': io_data,
        'equip_data': equip_data,
    })
#-------------------------------------------------------------------------------
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS
#-------------------------------------------------------------------------------
#使用位置 /stationGraphic
# 紅外線熱影像 使用者upload
@application_99M.route('/thermalImage_upload_file', methods=['POST'])
def thermalImage_upload_file():
    user,db = check_user()
    if(db == None):
        return logout()
    if request.method == 'POST':
        fileLength = int(request.form.get("fileLength"))
        plantName = request.form.get("plantName", default="")
        groupName = request.form.get("groupName", default="")
        filming_time = request.form.get("filming_time", default="")
        search_filming_time =datetime.datetime.strptime(filming_time[:10], "%Y-%m-%d") 
        filming_time = datetime.datetime.strptime(filming_time, "%Y-%m-%d %H:%M") 
        groupName = groupName.split('_')
        plant_ID = ""
        lgroup_ID = ""
        group_ID = ""
        #rewind your stream 
        send_Files = {}
        for i in range(fileLength):
            try:
                file = request.files["file"+str(i)]
                send_Files["file"+str(i)] = (file.filename, file.stream, file.mimetype)
            except:
                pass
        for plant in db.plant.find({"name":plantName}):
            plant_ID = str(plant['_id'])
            for lgroup in db.equipment.find({'PV': plantName, "name": groupName[0], 'type': 'pv_lgroup'}):
                lgroup_ID = str(lgroup['_id'])
                for group in db.equipment.find({'PV': plantName, "lgroup": groupName[0], "name": groupName[1], 'type': 'pv_group'}):
                    group_ID = str(group['_id'])
                    pathName = group_ID + '/' + filming_time.strftime("%Y-%m-%d") + '/Image/'
                    #post to IR image processing server
                    """ try:
                        r = requests.post(IR_image_server+'/save_images', data={'pathName': pathName, 'fileLength': fileLength}
                        , files=send_Files)
                        r = r.json()
                        if r.get('ok', 0) == 0:
                            return bad_request(400, 'Bad Request. Remote Server Report Error')
                    except Exception as e:
                        print(e)
                        return bad_request(400, 'Bad Request. Remote Server Disconnect') """
                    #check if day duplicate
                    time_dict = {
                        '$gte': search_filming_time,
                        '$lt': search_filming_time + datetime.timedelta(days=1)
                    }
                    if db.IR_image.count_documents({
                        'method': 'step1',
                        'PV': plant_ID,
                        'lgroup': lgroup_ID,
                        'ID': group_ID,
                        'filming_time': time_dict
                    }) > 0:
                        #Updte Info at mongoDB
                        db.IR_image.update_one({
                            'method': 'step1',
                            'PV': plant_ID,
                            'lgroup': lgroup_ID,
                            'ID': group_ID,
                            'filming_time': time_dict,
                        }, {'$set':{
                            'flag': 0,
                            'time': datetime.datetime.now(),
                            'progress_rate': ''
                        }})
                    else:
                        #Upload Info to mongoDB
                        db.IR_image.insert_one({
                            'method': 'step1',
                            'PV': plant_ID,
                            'lgroup': lgroup_ID,
                            'ID': group_ID,
                            'flag': 0,
                            'time': datetime.datetime.now(),
                            'filming_time': filming_time,
                            'progress_rate': ''
                        })
                    dirPath = current_app.config['UPLOAD_FOLDER'] + "/uploadThermalImage/" + pathName
                    print(dirPath)
                    try:
                        os.makedirs(dirPath)
                        print("Directory " , dirPath ,  " Created ")    
                    except FileExistsError:
                        print("Directory " , dirPath ,  " already exists")             
                    print(request.files)
                    for i in range(fileLength):
                        try:
                            file = request.files["file"+str(i)]
                            if file and allowed_file(file.filename):
                                filename = secure_filename(file.filename)
                                filename = os.path.basename(file.filename)
                                file.seek(0)
                                file.save(dirPath+"/"+filename)
                        except Exception as e:
                            print(e)
                    return successful_request({
                        'ok': 1,
                        'pathName': pathName
                    })

    return bad_request(400, 'Bad Request.')
#-------------------------------------------------------------------------------
#使用位置 /stationGraphic
# 紅外線熱影像 廠商上傳區
@application_99M.route('/thermalImage_upload_file_company', methods=['POST'])
def thermalImage_upload_file_company():
    user,db = check_user()
    if(db == None):
        return logout()
    if request.method == 'POST':
        fileLength = int(request.form.get("fileLength"))
        plantName = request.form.get("plantName", default="")
        groupName = request.form.get("groupName", default="")
        filming_time = request.form.get("filming_time", default="")
        filming_time = datetime.datetime.strptime(filming_time, "%Y-%m-%d  %H:%M")
        groupName = groupName.split('_')
        plant_ID = ""
        lgroup_ID = ""
        group_ID = ""
        #rewind your stream 
        send_Files = {}
        for i in range(fileLength):
            try:
                file = request.files["file"+str(i)]
                send_Files["file"+str(i)] = (file.filename, file.stream, file.mimetype)
            except:
                pass
        for plant in db.plant.find({"name":plantName}):
            plant_ID = str(plant['_id'])
            for lgroup in db.equipment.find({'PV': plantName, "name": groupName[0], 'type': 'pv_lgroup'}):
                lgroup_ID = str(lgroup['_id'])
                for group in db.equipment.find({'PV': plantName, "lgroup": groupName[0], "name": groupName[1], 'type': 'pv_group'}):
                    group_ID = str(group['_id'])
                    pathName = group_ID + '/' + filming_time.strftime("%Y-%m-%d") + '/'
                    #post to IR image processing server
                    """ try:
                        r = requests.post(IR_image_server+'/save_files_company', 
                        data={'pathName': pathName, 'fileLength': fileLength, "ID": group_ID, "filming_time": request.form.get("filming_time", default="")}
                        , files=send_Files)
                        r = r.json()
                        if r.get('ok', 0) == 0:
                            return bad_request(400, 'Bad Request. Remote Server Report Error')
                    except Exception as e:
                        return bad_request(400, 'Bad Request. Remote Server Disconnect') """
                    #Upload Info to mongoDB
                    db.IR_image.insert_one({
                        'method': 'step2',
                        'PV': plant_ID,
                        'lgroup': lgroup_ID,
                        'ID': group_ID,
                        'flag': 0,
                        'time': datetime.datetime.now(),
                        'progress_rate': ''
                    })
                    dirPath = current_app.config['UPLOAD_FOLDER'] + "/uploadThermalImage/" + pathName
                    print(dirPath)
                    try:
                        os.makedirs(dirPath)
                        print("Directory " , dirPath ,  " Created ")    
                    except FileExistsError:
                        print("Directory " , dirPath ,  " already exists")
                    for i in range(fileLength):
                        try:
                            file = request.files["file"+str(i)]
                            if file and allowed_file(file.filename):
                                filename = secure_filename(file.filename)
                                filename = os.path.basename(file.filename)
                                file.seek(0)
                                file.save(dirPath+"/"+filename)
                        except:
                            pass
                    return successful_request({
                        'ok': 1,
                        'pathName': pathName,
                        'group_ID': group_ID,
                    })

    return bad_request(400, 'Bad Request.')
#-------------------------------------------------------------------------------
#使用位置 /stationGraphic
# 紅外線熱影像
#接收從IR_image_server 回傳的檔案們
@application_99M.route('/save_IR_return_files', methods=['POST'])
def save_IR_return_files():
    print('save_IR_return_files')
    pathName = request.form.get("pathName", default="")
    fileLength = int(request.form.get("fileLength"))
    print(pathName, fileLength)
    print(request.files)
    if pathName != "":
        for i in range(fileLength):
            try:
                file = request.files["file"+str(i)]
                if file and allowed_file(file.filename):
                    filename = secure_filename(file.filename)
                    filename = os.path.basename(file.filename)
                    dirPath = current_app.config['UPLOAD_FOLDER'] + "/uploadThermalImage/" + pathName
                    try:
                        os.makedirs(dirPath)
                        print("Directory " , dirPath ,  " Created ")    
                    except FileExistsError:
                        print("Directory " , dirPath ,  " already exists")
                    file.save(dirPath+"/"+filename)
            except Exception as e:
                print(exception_detail(e))
                return jsonify(ok=0)
        print('save_IR_return_files  finish')
        return jsonify(ok=1)
    return jsonify(ok=0)
#-------------------------------------------------------------------------------
#使用位置 /stationGraphic
# 紅外線熱影像 回傳使用者要觀看的路徑
@application_99M.route('/get_thermalImage_timepath', methods=['POST'])
def get_thermalImage_timepath():
    user,db = check_user()
    if(db == None):
        return logout() 
    request_dict = request.json
    dict1 = {}
    try:
        plantName = request_dict['plantName']
        groupName = request_dict['groupName']
        groupName = groupName.split('_')
    except Exception as e:
        return bad_request(400, 'Bad Request. Due to {}'.format(e))

    for plant in db.plant.find({"name":plantName}):
        plant_ID = str(plant['_id'])
        for lgroup in db.equipment.find({'PV': plantName, "name": groupName[0], 'type': 'pv_lgroup'}):
            lgroup_ID = str(lgroup['_id'])
            for group in db.equipment.find({'PV': plantName, "lgroup": groupName[0], "name": groupName[1], 'type': 'pv_group'}):
                group_ID = str(group['_id'])
                for IR_image in db.IR_image.find({'PV': plant_ID, 'lgroup': lgroup_ID, 'ID': group_ID, 'method': 'step1'}):
                    filming_time = IR_image.get('filming_time', datetime.datetime.now()).strftime('%Y-%m-%d %H:%M')
                    pathName =  group_ID + '/' + filming_time[:10] + '/'
                    dirPath = current_app.config['UPLOAD_FOLDER'] + "/uploadThermalImage/" + pathName
                    print(dirPath)
                    if os.path.isdir(dirPath):
                        dict1[filming_time] = {'time': filming_time, 'htmlpath': pathName}
                        print('exist')
    return successful_request(dict1)
#-------------------------------------------------------------------------------
#使用位置 /stationGraphic
# 紅外線熱影像 打包下載
@application_99M.route('/IR_image_downloadzip', methods=['GET','POST'])
def IR_image_downloadzip():
    user,db = check_user()
    if(db == None):
        return logout() 
    request_dict = request.json
    try:
        pathName = request_dict['pathName']
    except:
        return bad_request(400, 'Bad Request. pathName')
    filePath = current_app.config['UPLOAD_FOLDER'] + "/uploadThermalImage/" + pathName
    zipPath = current_app.config['UPLOAD_FOLDER'] + "/uploadThermalImage/zip/" + pathName
    try:
        shutil.make_archive(zipPath+'download', 'zip', filePath)
    except Exception as e:
        print(e)
    return successful_request('/solar_static/uploadThermalImage/zip/'+pathName+'download.zip')
#-------------------------------------------------------------------------------
#使用位置 jump_station
@application_99M.route('/jump_station_get_data', methods=['POST'])
def jump_station():
    user,db = check_user()
    if(db == None):
        return logout() 
    request_dict = request.json
    try:
        name = request_dict['name']
    except:
        return bad_request(400, 'Bad Request. Name Error')
    if '補' in name:
        old_name = name
        name = ''
        for plant in db.plant.find({'name': {'$regex': old_name[0]}}):
            name = plant.get('name', '')
        name += '補{}'.format(old_name.split('_')[1])
    elif '_' in name:
        name = ''.join(name.split('_'))
    return_data = {}
    for plant in db.plant.find({'name': name}):
        # 只輸入上萬安段 改抓地號...的group
        for equip in db.equipment.find({'PV': plant.get('name'), 'type': 'pv_group'}).limit(1).sort('_id', 1):
            name = equip.get('name')
    for equip in db.equipment.find({'name': name, 'type': {'$in': ['pv_lgroup', 'pv_group']}}):
        return_data['lgroup'] = equip.get('lgroup')
        return_data['PV'] = equip.get('PV')
        return_data['name'] = equip.get('name')
        return_data['ID'] = str(equip['_id'])
        return_data['collection'] = equip.get('type')
        #案場圖片
        return_data['imgsrc'] = '{}/images/plant_image/{}.png'.format(current_app.config['UPLOAD_FOLDER'], return_data['ID'])
        if not os.path.isfile(return_data['imgsrc']):
            return_data['imgsrc'] = 'solar_static/images/plant_image/default.png'
        else:
            return_data['imgsrc'] = 'solar_static/images/plant_image/{}.png'.format(return_data['ID'])
            
        """ plant_data = db.plant.find_one({'name': equip['PV']})
        weather_data = c.get_weather_forecast(db, plant_data.get('location', {}).get('city', ''))
        return_data['weather'] = {
            'imgurl': weather_data.get('imgurl', ''),
            'temperature': weather_data.get('T', '---'),
            'status':weather_data.get('Wx', '---'),
            'rain': '降雨機率{}%'.format(
                '---' if isinstance(weather_data.get('PoP6h', '---'), str) else int(weather_data['PoP6h']))
        } """
    return successful_request(return_data)
#-------------------------------------------------------------------------------
# 使用位置 stationlist
#取得變流器顯示表格 99M專用
# taipower please go to app_taipower.vue
@application_99M.route('/get_inv_table_data', methods=['POST'])
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
        table_list = db.inverter_table.find_one({'Device_model': Device_model})['table_99m']
    except:
        pass
    return successful_request({
        'table_data': table_list,
        'Device_model': Device_model
    })
#-------------------------------------------------------------------------------