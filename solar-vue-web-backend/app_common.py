# ES 99M Vue 與 台電 Vue 共用API
# 主程式功能
#-------------------------------------------------------------------------------
# Libiary
from flask import views, Blueprint, request, current_app, jsonify, session, g, make_response, send_file
from flask_login import UserMixin, login_user, logout_user, current_user
import datetime
from dateutil import relativedelta
import pymongo
from bson import ObjectId, json_util
import os
import math
from pymongo import MongoClient
from urllib.parse import quote_plus # For mongodb uri string
import sys
import traceback
import json
import glob # for finding file without extension
import time
import pdf2image
from io import BytesIO
import requests
import base64

# Python Json Web Tokens
import jwt
#-------------------------------------------------------------------------------
# 通用函式與功能
import current as c
import prepareplot as t
import report_gen as r
import docx_produce as d # ==> docx報表製作函式


#======================================================================================================
# application_common is a Blueprint of flask
# Learn More About Blueprint At
# https://flask.palletsprojects.com/en/2.0.x/blueprints/
application_common = Blueprint('application_common', __name__)


#======================================================================================================
# MongoDB Setup
MONGO_HOST = os.getenv('MONGODB_HOSTNAME', 'localhost')
MONGO_PORT = os.getenv('MONGODB_PORT', '27017')
MONGO_USER = os.getenv('MONGODB_USERNAME', 'root')
MONGO_PASS = os.getenv('MONGODB_PASSWORD', 'pc152')
MONGO_RS_NAME = os.getenv('MONGODB_RS_NAME', 'rs0')

host_split = str(MONGO_HOST).split(',')
port_split = str(MONGO_PORT).split(',')
if len(host_split) == 1:
    uri = "mongodb://{}:{}@{}:{}/".format(quote_plus(MONGO_USER), quote_plus(MONGO_PASS), MONGO_HOST, MONGO_PORT)
    conn = MongoClient(uri, connect=False)
elif len(host_split) > 1:
    host_port = []
    for i, host in enumerate(host_split):
        host_port.append('{}:{}'.format(host, port_split[i]))
    host_port = ','.join(host_port)
    uri = "mongodb://{}:{}@{}/?replicaSet={}".format(quote_plus(MONGO_USER), quote_plus(MONGO_PASS) , host_port , MONGO_RS_NAME)
    conn = MongoClient(uri,connect=False)


#-------------------------------------------------------------------------------
# request完成 將資料json string化
def successful_request(data={}):
    return jsonify({
        "data": data, "status": True
    })
#-------------------------------------------------------------------------------
# 錯誤請求 
def bad_request(status, detail="Error."):
    return jsonify({"error":{
        "status": status,   # http status code
        "source": { "pointer": request.base_url },   #API 路徑
        "detail": detail    # 細節
        }, "status": False}), status
#-------------------------------------------------------------------------------
def exception_detail(e):
    error_class = e.__class__.__name__ #取得錯誤類型
    detail = e.args[0] #取得詳細內容
    cl, exc, tb = sys.exc_info() #取得Call Stack
    lastCallStack = traceback.extract_tb(tb)[-1] #取得Call Stack的最後一筆資料
    fileName = lastCallStack[0] #取得發生的檔案名稱
    lineNum = lastCallStack[1] #取得發生的行號
    funcName = lastCallStack[2] #取得發生的函數名稱
    errMsg = "File \"{}\", line {}, in {}: [{}] {}".format(fileName, lineNum, funcName, error_class, detail)
    return errMsg
#======================================================================================================
# 登入設定
LOGIN_ENABLE = True
if os.getenv('web_backend_login_enable', "true") in ["false", False, "False"]:
    LOGIN_ENABLE = False
#-------------------------------------------------------------------------------
#登入相關設定 Session查核
class User(UserMixin):
    pass

#-------------------------------------------------------------------------------
#對照是否有此用戶
def user_list(user_id):
    _user=user_id.split('_', 1)
    db =conn[_user[0]]
    for user_find in db.users.find({'username': _user[1]}):
        return user_find 
#-------------------------------------------------------------------------------
def check_user():
    if LOGIN_ENABLE == False:
        return ['pv', 'pv'], conn['pv']    # For NO Login
    user = current_user.get_id()
    try:
        user = user.split('_', 1)
    except:
        return None,None
    db = conn[user[0]]
    db.users.update_one({'user_id': current_user.get_id()}, {'$set': {'last_access_time': datetime.datetime.now(), 'last_access_ip': request.remote_addr}})
    return user,db
#-------------------------------------------------------------------------------
# 從current_user取得user_id
def find_user_from_current_user():
    if LOGIN_ENABLE == True:
        find_user = current_user.get_id()
    else:
        find_user = 'pv_pv'   # For NO Login
    return find_user
#-------------------------------------------------------------------------------
# element 日期選擇元件 to time filter
def date_range_interval_to_filter(date_obj={}):
    time_filter = {}
    if date_obj == None or date_obj == {}:
        # NoneType
        return True, {'$exists': True}
    elif isinstance(date_obj, str):
        try:
            date_obj = datetime.datetime.strptime(date_obj, '%Y-%m-%d')
            return True, {'$gte': date_obj, '$lt': date_obj + datetime.timedelta(days=1)}
        except Exception as e:
            return  False, bad_request(400, 'Bad Request. Time error. {}'.format(exception_detail(e)))
    if date_obj.get('mode', '') == 'single':
        try:
            start_date = datetime.datetime.strptime(date_obj['start_date'], '%Y-%m-%d')
            end_date = start_date + datetime.timedelta(days=1)
            time_filter = {'$gte': start_date, '$lt': end_date}
        except:
            return False, bad_request(400, 'Time error')
    elif date_obj.get('mode', '') == 'interval':
        try:
            start_date = datetime.datetime.strptime(date_obj['start_date'], '%Y-%m-%d')
            end_date = datetime.datetime.strptime(date_obj['end_date'], '%Y-%m-%d')
            time_filter = {'$gte': start_date, '$lt': end_date+datetime.timedelta(days=1)}
        except:
            return False, bad_request(400, 'Time error')
    elif date_obj.get('mode', '') in ['today', 'week', 'month', 'year']:
        today =datetime.datetime.today()
        if date_obj['mode'] == 'today':
            start_date = datetime.datetime.combine(today, datetime.time.min)
            end_date = start_date + datetime.timedelta(days=1)
        elif date_obj['mode'] == 'week':
            start_date=datetime.datetime.combine(today, datetime.time.min) - datetime.timedelta(days=today.weekday())
            end_date = start_date + datetime.timedelta(days=7)
        elif date_obj['mode'] == 'month':
            start_date = datetime.datetime(year=today.year, month=today.month, day=1)
            end_date = start_date + relativedelta.relativedelta(months=1)
        elif date_obj['mode'] == 'year':
            start_date = datetime.datetime(year=today.year, month=1, day=1)
            end_date = start_date + relativedelta.relativedelta(years=1)
        time_filter = {'$gte': start_date, '$lt': end_date}
    elif date_obj.get('mode', '') == 'all':
        time_filter = {'$exists': True}

    return True, time_filter
#======================================================================================================
# 登入API

#登入登出API
#login
@application_common.route('/login',methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        username = request.form.get('username',type=str, default='')
        password = request.form.get('password',type=str, default='')
        company = request.form.get('company', type=str, default='pv')
        if company == '':
            company = 'pv'
        if username == '' and password == '':
            return bad_request(401, 'Empty login data.')
        user_id = company+'_'+username
        user_info = user_list(user_id)
        #驗證帳號
        if user_info is not None and password == user_info['password']:
            curr_user = User()
            curr_user.id = user_info['user_id']
            #通過flask-login的login_user方法登入用戶
            login_user(curr_user)
            user,db = check_user()
            db.users.update_one({'_id': ObjectId(str(user_info['_id']))}, {'$set': {'last_login_time': datetime.datetime.now()}})
            return successful_request({})
        #Unauthorized
        return bad_request(401, 'Unauthorized.')
    else:   #方法只能為POST
        return bad_request(405, 'Method Not Allowed. Please use POST.')
#-------------------------------------------------------------------------------
#login width oidc
@application_common.route('/oidc', methods=['POST'])
def oidc():
    if request.method == 'POST':
        request_dict = request.form
        oidc_type = request_dict.get("oidc_type", type=str, default='')
        db = conn['pv']
        expire_time = db.parameter_setting.find_one({"method": "oidc_session_lifetime"}).get("expire_time", 1)
        if (oidc_type):
            try:
                if oidc_type == 'github':
                    githubClientId = os.getenv('oidc_github_client_id', '')
                    githubClientSecret = os.getenv('oidc_github_client_secret', '')
                    code = request_dict.get("code", type=str, default='')
                    if githubClientId and githubClientSecret and code:
                        url = f"http://github.com/login/oauth/access_token?client_id={githubClientId}&client_secret={githubClientSecret}&code={code}"
                        res = requests.post(url, headers={'accept': 'application/json'})
                        # print(res)
                        response = res.text
                        # print(response)
                        response = eval(response)
                        access_token = response.get('access_token')
                        userinfo = requests.get(
                            f'https://api.github.com/user?accesstoken={access_token}',
                            headers={
                                'accept': 'application/vnd.github+json',
                                'Authorization': f"token {access_token}",
                                'Keep-Alive': 'timeout=5'
                            }
                        )
                        user = userinfo.text
                        user = user.replace("false", "False")
                        user = user.replace("true", "True")
                        user = user.replace("null", "None")
                        user = eval(user)
                        login_name = user.get('login')

                        for user_find in db.users.find({'oidc': {"$exists": True}}):
                            if login_name in user_find.get("oidc", {}).get("github", []):
                                curr_user = User()
                                curr_user.id = user_find['user_id']
                                #通過flask-login的login_user方法登入用戶
                                login_user(curr_user)
                                user,db = check_user()
                                db.users.update_one({'_id': ObjectId(str(user_find['_id']))}, {'$set': {'last_login_time': datetime.datetime.now()}})
                                oidc_account = jwt.encode({'github': login_name}, '{}_oidc'.format(current_app.secret_key), algorithm="HS256")
                                resp = make_response(successful_request(oidc_account))
                                try:
                                    resp.set_cookie('oidc_account', oidc_account, httponly=True, expires=datetime.datetime.now()+datetime.timedelta(days=expire_time))
                                except Exception as e:
                                    print("set oidc cookie false{}".format(e))
                                print("github login success")
                                return resp
                        return bad_request(401, 'Unauthorized.')
                    else:
                        return bad_request(401, 'Unauthorized.')
                elif oidc_type == 'gmail' or oidc_type == 'gitlab':
                    id_token = request_dict.get("id_token", type=str, default='')
                    id_token = id_token.replace("false", "False")
                    id_token = id_token.replace("true", "True")
                    id_token = id_token.replace("null", "None")
                    id_token = eval(id_token)
                    # print(id_token)
                    id_token = id_token.get("id_token", "")
                    parts = id_token.split(".")
                    if len(parts) == 3:
                        payload = parts[1]
                        padded = payload + "=" * (4 - len(payload)%4)
                        decoded = base64.b64decode(padded)
                        gmail = json.loads(decoded)["email"]
                        for user_find in db.users.find({'oidc': {"$exists": True}}):
                            if gmail in user_find.get("oidc", {}).get(oidc_type, []):
                                curr_user = User()
                                curr_user.id = user_find['user_id']
                                #通過flask-login的login_user方法登入用戶
                                login_user(curr_user)
                                user,db = check_user()
                                db.users.update_one({'_id': ObjectId(str(user_find['_id']))}, {'$set': {'last_login_time': datetime.datetime.now()}})
                                oidc_account = jwt.encode({oidc_type: gmail}, '{}_oidc'.format(current_app.secret_key), algorithm="HS256")
                                resp = make_response(successful_request(oidc_account))
                                try:
                                    resp.set_cookie('oidc_account', oidc_account, httponly=True, expires=datetime.datetime.now()+datetime.timedelta(days=expire_time))
                                except Exception as e:
                                    print("set oidc cookie false{}".format(e))
                                print(f"{oidc_type} login success")
                                return resp
                        return bad_request(401, 'Unauthorized.')
                    else:
                        return bad_request(401, 'Unauthorized.')
            except Exception as e:
                print("oidc error:{}".format(exception_detail(e)))
                return bad_request(401, 'Unauthorized.')
        
    else:
        return bad_request(405, 'Method Not Allowed. Please use POST.')
#-------------------------------------------------------------------------------
@application_common.route('/api_info', methods=['POST', 'GET'])
def api_info():
    info = {
        'env_project_name': os.getenv('web_backend_project_name', None),
        'env_login_authentication': os.getenv('web_backend_login_enable', None),
        'project_name': os.getenv('web_backend_project_name', '99M'),
        'login_authentication': os.getenv('web_backend_login_enable', "false"),
    }
    return successful_request(info)
#-------------------------------------------------------------------------------
#logout
@application_common.route('/logout')
def logout():
    user = current_user
    user.authenticated = False
    session.clear()
    resp = make_response("del oidc_account")
    resp.delete_cookie("oidc_account")
    logout_user()
    return resp
#-------------------------------------------------------------------------------
#login_statue
# using in 99M
class LoginStatus(views.MethodView):
    def get(self):
        user, db = check_user()
        if db == None:
            return logout()
        return successful_request(self.login_status(db))
    def post(self):
        user, db = check_user()
        if db == None:
            return logout()
        return successful_request(self.login_status(db))
    def login_status(self, db):
        find_user = find_user_from_current_user()
        user_c=list(db.users.find({"user_id" : find_user}))[0]
        return {
            'username': user_c.get('username', ''),
            'level': int(user_c.get('level', 1)),
            'main_photo': user_c.get('main_photo', 'solar_static/images/users_photo/default.png'),
            'is_superuser': user_c.get('superuser', False),
            'pageType': user_c.get('pageType', 'pv')}
application_common.add_url_rule('/login_status', view_func=LoginStatus.as_view('login_status'))    
#-------------------------------------------------------------------------------
#Using in Taipower
class LoginStatusNavigationGuard(LoginStatus):
    def get(self):
        user, db = check_user()
        if db == None:
            return logout()
        return self.login_status(db)
    def post(self):
        user, db = check_user()
        if db == None:
            if 'oidc_account' in request.cookies:
                db = conn['pv']
                oidc_account = request.cookies['oidc_account']
                decode_data = jwt.decode(oidc_account, '{}_oidc'.format(current_app.secret_key), algorithms=["HS256"])
                # print(decode_data)
                oidc_key = list(decode_data.keys())[0]
                oidc_type = list(decode_data.values())[0]
                for user_find in db.users.find({'oidc': {"$exists": True}}):
                    if oidc_type in user_find.get("oidc", {}).get(oidc_key, []):
                        curr_user = User()
                        curr_user.id = user_find['user_id']
                        #通過flask-login的login_user方法登入用戶
                        login_user(curr_user)
                        user,db = check_user()
                        expire_time = db.parameter_setting.find_one({"method": "oidc_session_lifetime"}).get("expire_time", 1)
                        db.users.update_one({'_id': ObjectId(str(user_find['_id']))}, {'$set': {'last_login_time': datetime.datetime.now()}})
                        oidc_account = jwt.encode({oidc_key: oidc_type}, '{}_oidc'.format(current_app.secret_key), algorithm="HS256")
                        resp = make_response(self.login_status(db))
                        print(f"{oidc_key} login success")
                        try:
                            resp.set_cookie('oidc_account', oidc_account, httponly=True, expires=datetime.datetime.now()+datetime.timedelta(days=expire_time))
                        except Exception as e:
                            print("set oidc cookie false {}".format(e))
                        return resp
            return logout()
        return self.login_status(db)
    def login_status(self, db):
        return_dict = super().login_status(db)
        try:
            if 'routing_guard' not in request.cookies:
                my_get_navLink = GetNavLink()
                nav_data, route_guard = my_get_navLink.get_data(db)
                routing_guard_encrypt = route_guard
            else:
                routing_guard_encrypt = request.cookies['routing_guard']

            allow_url = jwt.decode(routing_guard_encrypt, '{}_route_guard'.format(current_app.secret_key), algorithms=["HS256"])['data']
            if request.json['to'] not in allow_url:
                return_dict['next'] = allow_url[0]
            else:
                return_dict['next'] = request.json['to']
        except Exception as e:
            return logout()
        return successful_request(return_dict)
application_common.add_url_rule('/login_status_navigation_guard', view_func=LoginStatusNavigationGuard.as_view('login_status_navigation_guard'))    
#-------------------------------------------------------------------------------
@application_common.route('/app_login_get_token',methods=['POST', 'GET'])
def app_login_get_token():
    if request.method == 'POST':
        username = request.form.get('username',type=str, default="")
        password = request.form.get('password',type=str, default="")
        if username == "" and password == "":
            return bad_request(401, 'Empty login data.')
        if '@' in username:
            domain = username.split('@')[1]
            user = username.split('@')[0]
            if '.' in domain:
                company = domain.split('.')[0]
            else:
                company = domain
        else:
            company = "pv"
        user_id = company+'_'+username
        user_info = user_list(user_id)
        #驗證帳號
        if user_info is not None and password == user_info['password']:
            try:
                token_expire_time = conn[company].parameter_setting.find_one({'method': 'app_auth_token_expire_time', 'expire_after_days': {'$exists': True}})
                if token_expire_time != None:
                    token_expire_time = token_expire_time.get('expire_after_days')
                else:
                    token_expire_time = 30
            except:
                token_expire_time = 30
            token_expire_time = token_expire_time * 86400 + time.time()
            encoded_jwt = jwt.encode({"uid": str(user_info['_id']), "company": company, "exp": token_expire_time,
            'uuid': request.form.get('uuid')}, current_app.secret_key, algorithm="HS256")
            #save device
            conn[company].mobile_device.update_one({'ID': str(user_info['_id']), 'uuid': request.form.get('uuid')}, 
            {'$set': {'platform': request.form.get('device_type'), 'name': request.form.get('device_name'),
            'model': request.form.get('device_model'), 'show': 1, 'auth_token': encoded_jwt,
            'enable_push_notify': True, 'last_login_time': datetime.datetime.now(),
            'firebase_token': request.form.get('device_firebase_token')}}, upsert=True)
            widget_access_token = jwt.encode({"uid": str(user_info['_id']), "company": company}, '{}_app_widget_access_key'.format(current_app.secret_key), algorithm="HS256")
            return successful_request({'token': encoded_jwt, "access_token": widget_access_token})
        #Unauthorized
        return bad_request(401, 'Unauthorized.')
    else:   #方法只能為POST
        return bad_request(405, 'Method Not Allowed. Please use POST.')
#-------------------------------------------------------------------------------
class APPTokenLogin(views.MethodView):
    def get(self):
        #print(request.headers)
        access_token = request.headers.get('Authorization', None)
        if access_token == None:
            return successful_request('No_token_maybe_init_1412')
        try:
            my_decode = jwt.decode(access_token, current_app.secret_key, algorithms=["HS256"])
        except:
           return bad_request(401, 'App_login_Unauthorized.')
        user_id = my_decode.get('uid', None)
        device_uuid = my_decode.get('uuid', None)
        company = my_decode.get('company', None)
        if user_id == None or company == None or device_uuid == None:
            return bad_request(401, 'App_login_Unauthorized.') 
        
        user_info = conn[company].users.find_one({'_id': ObjectId(user_id)})
        #驗證帳號
        if user_info is not None and conn[company].mobile_device.count_documents({'ID': user_id,
        'auth_token': access_token, 'show': 1}) > 0:
            curr_user = User()
            curr_user.id = user_info['user_id']
            #通過flask-login的login_user方法登入用戶
            login_user(curr_user)
            user,db = check_user()
            db.mobile_device.update_one({'ID': user_id, 'uuid': device_uuid}, {'$set': {
                'last_login_time': datetime.datetime.now()
            }})
            resp = make_response(successful_request({'login': True, 'msg': 'App_login_successful_1412'}))
            resp.set_cookie('is_app', "true")
            return resp
        #Unauthorized
        return bad_request(401, 'App_login_Unauthorized.')
    def post(self):
        return self.get()
application_common.add_url_rule('/app_login_with_token', view_func=APPTokenLogin.as_view('app_login_with_token'))
#-------------------------------------------------------------------------------
@application_common.route('/get_static_file_auth_token',methods=['POST', 'GET'])
def get_static_file_auth_token():
    if request.method == 'POST' or request.method == 'GET':
        access_token = request.headers.get('Authorization', None)
        if access_token == None:
            return bad_request(401, 'Unauthorized')
        try:
            my_decode = jwt.decode(access_token, current_app.secret_key, algorithms=["HS256"])
        except:
           return bad_request(401, 'Unauthorized')
        user_id = my_decode.get('uid', None)
        company = my_decode.get('company', None)
        if user_id == None or company == None:
            return bad_request(401, 'App_login_Unauthorized.') 
        
        user_info = conn[company].users.find_one({'_id': ObjectId(user_id)})
        #驗證帳號
        if user_info is not None:
            encoded_jwt = jwt.encode({"exp": time.time()+10}, current_app.secret_key, algorithm="HS256")
            return successful_request({'token': encoded_jwt})
        #Unauthorized
        return bad_request(401, 'Unauthorized.')
    else:   #方法只能為POST
        return bad_request(405, 'Method Not Allowed.')
#-------------------------------------------------------------------------------
# authentication for static files at /solar_static
# see README for further information
@application_common.route('/solar_static_auth', methods=['GET'])
def solar_static_auth():
    user, db = check_user()
    if db == None:
        # For mobile authentication
        access_token = request.args.get('auth_token', None)
        try:
            jwt.decode(access_token, current_app.secret_key, algorithms=["HS256"])
            return successful_request()
        except:
           return bad_request(401, 'Unauthorized')
        return logout()
    return successful_request()
#-------------------------------------------------------------------------------
# To determine whether to show registartion button to user at app
@application_common.route('/check_registration_button', methods=['GET', 'POST'])
def check_registration_button():
    db = conn['pv']
    try:
        return successful_request(db.parameter_setting.find_one({'method': 'enable_app_registration'})['enable'])
    except:
        return successful_request(True)
#======================================================================================================
# Get navLink Content
# Implement in Taipower
class GetNavLink(views.MethodView):
    def get(self):
        user, db = check_user()
        if db == None:
            return logout()

        nav_data, route_guard = self.get_data(db)

        return self.response_add_cookie(successful_request(nav_data), route_guard)

    def get_data(self, db):
        find_user = find_user_from_current_user()
        user_c=list(db.users.find({"user_id" : find_user}))[0]
        
        #get NavData
        match = {
            'type': 'navLink', 
            'pageType': {'$in': ['all', user_c.get('pageType')]}, 'show': 1,
            '$or': [{'level': {'$not': {'$type': 'array'}, '$lte': user_c.get('level', 1)}}, {'level': user_c.get('level', 1)}],
            'superuser': {'$ne': True}
        }
        if user_c.get('superuser', False) == True:
            match.pop('superuser', None)
        project = {
            '_id': 0, 'route': 1, 'name': 1, 'name_i18n': 1, 'icon': 1
        }

        nav_data = list(db.web_nav_page.aggregate([
            {'$match': match},
            {'$sort': {'priority': 1 }},
            {'$project': project},
            {'$addFields': {'alert': False}}
        ]))

        match.pop('show', None)
        project = {'_id': 0, 'route': 1}
        group = {'_id': None, 'route': {'$push': '$route'}}

        allow_url_list = list(db.web_nav_page.aggregate([
            {'$match': match},
            {'$sort': {'priority': 1 }},
            {'$project': project},
            {'$group': group}
        ]))
        route_guard = jwt.encode({'data': allow_url_list[0].get('route', [])}, '{}_route_guard'.format(current_app.secret_key), algorithm="HS256")

        return nav_data, route_guard

    def response_add_cookie(self, _response, guard_token:str):
        resp = make_response(_response)
        resp.set_cookie('routing_guard', guard_token, httponly=True)
        return resp
application_common.add_url_rule('/get_navLink', view_func=GetNavLink.as_view('get_navLink'))
#======================================================================================================
#get nav tab
@application_common.route('/get_tab_data', methods=['POST'])
def get_tab_data():
    user, db = check_user()
    if db == None:
        return logout()
    try:
        find_user = find_user_from_current_user()
        user_c=list(db.users.find({"user_id" : find_user}))[0]
        request_dict = request.json
        path = request_dict["path"]
        pageType = user_c.get("pageType", "all")
        level = user_c.get("level", 1)
        match = {
            "type": "tab",
            "route": path,
            "show": 1,
            "$and": [
                {"$or": [{"pageType": {"$in": ["all", pageType]}}, {"pageType": {"$all": [pageType]}}]},
                {"$or": [{"level": {"$lte": level}}, {"level": {"$all": [level]}}, {"level": {"$in": ["all"]}}]}
            ]
        }
        project = {
            '_id': 0, 'name': 1, 'name_i18n': 1, 'value': 1, 'constrain': 1
        }
        if user_c.get("superuser", False) == True:
            tab_data = db.web_nav_page.aggregate([
                {"$match": match},
                {'$sort': {'priority': 1 }},
                {'$project': project}
            ])
        else:
            match["$or"] = [{"superuser": {"$exists": False}}, {"superuser": False}]
            tab_data = db.web_nav_page.aggregate([
                {"$match": match},
                {'$sort': {'priority': 1 }},
                {'$project': project}
            ])
        tab_data = list(tab_data)
        # print(tab_data)
        return successful_request({"data": tab_data})
    except Exception as e:
        print(e)
        return bad_request(400, 'Error Due to {}'.format(e))
#======================================================================================================
# 一般API
#使用位置 /homefunc /stationlist /show
#使用位置 /homefunc /stationlist /show
class StatsAllPVReal(views.MethodView):
    def get(self):
        user, db = check_user()
        if db == None:
            return logout()
        find_user = find_user_from_current_user()
        user_c=list(db.users.find({"user_id" : find_user}))[0]
        today = datetime.datetime.strftime(datetime.datetime.now(), '%Y-%m-%d')
        today = datetime.datetime.strptime(today, '%Y-%m-%d')
        try:
            plant_filter = {}
            if user_c['plant'][0] != 'total':
                for i in user_c['plant']:
                    if 'name' not in plant_filter:
                        plant_filter['name'] = {'$in': []}
                    plant_filter['name']['$in'].append(i)
            stats_data = {'total_station': 0, 'total_capacity': 0, 'total_kwh': 0, 'total_carbon_reduction': 0, 'profit': '---',
            'ID_list': [], 'PV_data': []}
            for plant in db.plant.find(plant_filter):
                stats_data['PV_data'].append({
                    'ID': str(plant['_id']),
                    'name': str(plant.get('name')),
                    'collection': str(plant.get('collection', 'pv_plant'))
                })
                stats_data['ID_list'].append(str(plant['_id']))
                stats_data['total_capacity'] += plant.get('capacity', 0) 
                group_count = db.equipment.count_documents({'PV': plant['name'], 'type': 'pv_group'})
                try:
                    #today_kwh = c.diff_data(db, 'pv_plant', str(plant['_id']), 'kwh', 0)
                    #today_kwh = db.pr_cal.find_one({'ID': str(plant['_id']), 'time_interval': 'day', 'time': today}).get('kwh', None)
                    today_kwh = c.current_data(db, plant.get('collection', 'pv_plant'), str(plant['_id']))
                    if len(today_kwh) > 0:
                        today_kwh = today_kwh[0].get('kwh', None)
                    if isinstance(today_kwh, (int, float)):
                        stats_data['total_kwh'] += today_kwh


                except:
                    pass
                stats_data['total_station'] += group_count
            stats_data['total_capacity'] = round(stats_data['total_capacity']/1000, 3) # convert kW to MW 
            stats_data['total_kwh'] = stats_data['total_kwh']
            stats_data['total_carbon_reduction'] = round(stats_data['total_kwh']*0.502)   # 109 年排碳係數 
            stats_data['total_kwh'] = round(stats_data['total_kwh']/1000, 2)
        except Exception as e:
            print(exception_detail(e))
            return bad_request('Error Due to {}'.format(e))
        return successful_request(stats_data)
    def post(self):
        return self.get()
application_common.add_url_rule('/stats_all_pv_real', view_func=StatsAllPVReal.as_view('stats_all_pv_Real'))
#-------------------------------------------------------------------------------
@application_common.route('/tawian3d_plant_overview')
def tawian3d_plant_overview():
    user, db = check_user()
    if db == None:
        return logout()
    today = datetime.datetime.strftime(datetime.datetime.now(), '%Y-%m-%d')
    today = datetime.datetime.strptime(today, '%Y-%m-%d')
    find_user = find_user_from_current_user()
    user_c=list(db.users.find({"user_id" : find_user}))[0]
    try:
        plant_filter = {}
        if user_c['plant'][0] != 'total':
            for i in user_c['plant']:
                if 'name' not in plant_filter:
                    plant_filter['name'] = {'$in': []}
                plant_filter['name']['$in'].append(i)
        list1 = []
        for plant in db.plant.find(plant_filter):
            weather_data = c.get_weather_forecast(db, plant.get('location', {}).get('city', ''))
            plant_data = {
                'idfor3Dpoint': plant.get('location', {}).get('taiwan3d', {}), 
                'name': plant.get('name', '---'), 'link': {'title': '查看案場','url': '/',}, 
                'ID': str(plant['_id']), 'collection': plant.get('collection', 'pv_plant'),
                'weather': {
                    'imgurl': weather_data.get('imgurl', ''),
                    'temperature': weather_data.get('T', '---'),
                    'status':weather_data.get('Wx', '---'),
                    'rain': '降雨機率{}%'.format(
                        '---' if isinstance(weather_data.get('PoP6h', '---'), str) else int(weather_data['PoP6h']))
				}, 'ttlPower': {
                    'title': '總累計發電量',
                    'numb': '---',
                    'unit': 'kWh'
                },
                'todayPower': {
                    'title': '今日發電量',
                    'numb': '---',
                    'unit': 'kWh'
                },
                'otherInfos': [   #更改時 注意下面程式取用的陣列位置
                    { 'title': '總電站數', 'numb': '---', 'unit': '座' },
                    { 'title': '等效日照', 'numb': '---', 'unit': 'h' },
                    #{ 'title': '今日發電量', 'numb': '---', 'unit': 'kWh' },  # remind to correct index
                    { 'title': '今日減碳量', 'numb': '---', 'unit': 'kg' },
                    { 'title': '累計減碳量', 'numb': '---', 'unit': 'kg' },
                ]
            }
            group_count = db.equipment.count_documents({'PV': plant['name'], 'type': 'pv_group'})
            plant_data['otherInfos'][0]['numb'] = group_count
            try:
                for _data in db[plant.get('collection', 'pv_plant')].find({'ID': str(plant['_id']), '$and': [{'kwh': {'$nin':[None]}}, {'kwh': {'$exists': True}}]}).sort('time', -1).limit(1):
                    plant_data['ttlPower']['numb'] = round(_data.get('kwh', '---'))
                    if plant_data['ttlPower']['numb']  > 10000:
                        plant_data['ttlPower']['numb'] /= 1000
                        plant_data['ttlPower']['unit'] = 'MWh'
                    plant_data['otherInfos'][3]['numb'] = str(round(_data.get('kwh', '---')*0.509))   # 108 年排碳係數
            except Exception as e:
                print(exception_detail(e))
                pass    
            # use meter_cal instead
            gen_stats = db.meter_cal.find_one({'ID': str(plant['_id']), 'time_interval': 'day', 'time': today})
            try:
                #today_kwh = c.diff_data(db, 'pv_plant', str(plant['_id']), 'kwh', 0)
                today_kwh = gen_stats.get('kwh', '---')
                plant_data['todayPower']['numb'] = str(today_kwh if isinstance(today_kwh, str) else round(today_kwh, 2))
                #plant_data['otherInfos'][2]['numb'] = str(today_kwh if isinstance(today_kwh, str) else round(today_kwh, 2))
                plant_data['otherInfos'][2]['numb'] = str(round(today_kwh*0.509))   # 108 年排碳係數
            except:
                pass
            
            try:
                irrh_stats = db.irrh_cal.find_one({'ID': c.plant_group_ID_find_sun_ID(db, plant['_id'], 'pv_plant'), 
                'time_interval': 'day', 'time': today})
                plant_data['otherInfos'][1]['numb']  = round(irrh_stats['irrh'], 3)
            except Exception as e:
                plant_data['otherInfos'][1]['numb'] = '---'


            list1.append(plant_data)
    except Exception as e:
        print(exception_detail(e))
        return bad_request(400, 'Error Due to {}'.format(e))

    return successful_request(list1)
#-------------------------------------------------------------------------------
#使用位置 /selectStation
class GetSelectStation(views.MethodView):
    def get(self):
        user, db = check_user()
        if db == None:
            return logout()
        find_user = find_user_from_current_user()

        user_c=list(db.users.find({"user_id" : find_user}))[0]
        nationOpt_dict = {}
        groupIDLable = {}
        try:
            plant_filter = {}
            if user_c['plant'][0] != 'total':
                for i in user_c['plant']:
                    if 'name' not in plant_filter:
                        plant_filter['name'] = {'$in': []}
                    plant_filter['name']['$in'].append(i)

            for plant in db.plant.find(plant_filter):
                try:
                    city = plant['location']['city'] 
                    district = plant['location']['district']
                    if city not in nationOpt_dict:
                        nationOpt_dict[city] = {}
                    if  district not in nationOpt_dict[city]:
                        nationOpt_dict[city][district] = {}
                    if plant['name'] not in nationOpt_dict[city][district]:
                        nationOpt_dict[city][district][plant['name']] = {'name': plant['name'],
                        'ID': str(plant['_id']), 'lgroup': {}}
                    for lgroup in db.equipment.find({'PV': plant['name'], 'type': 'pv_lgroup'}):
                        if lgroup['name'] not in nationOpt_dict[city][district][plant['name']]['lgroup']:
                            nationOpt_dict[city][district][plant['name']]['lgroup'][lgroup['name']] = {
                                'name': lgroup['name'], 'ID': str(lgroup['_id']), 'group': {}
                            }
                        for group in db.equipment.find({'PV': plant['name'], 'lgroup': lgroup['name'], 'type': 'pv_group'}):
                            #if group['name'] not in nationOpt_dict[city][district][plant['name']]['lgroup'][lgroup['name']]['group']:
                            nationOpt_dict[city][district][plant['name']]['lgroup'][lgroup['name']]['group'][group['name']] = {
                                'name': group['name'], 'ID': str(group['_id'])
                            }
                            groupIDLable[str(group['_id'])] = [city, district, plant['name'], lgroup['name'], group['name']]
                except Exception as e:
                    print(exception_detail(e))
            
            nationOpt = []
            for city in nationOpt_dict:
                district_list = []
                for district in nationOpt_dict[city]:
                    plant_list = []
                    for plant in nationOpt_dict[city][district]:
                        lgroup_list = []
                        for lgroup in nationOpt_dict[city][district][plant]['lgroup']:
                            group_list = []
                            for group in nationOpt_dict[city][district][plant]['lgroup'][lgroup]['group']:
                                group_list.append({'label': group, 'value': nationOpt_dict[city][district][plant]['lgroup'][lgroup]['group'][group]['ID']})
                            lgroup_list.append({'label': lgroup, 
                            'value': nationOpt_dict[city][district][plant]['lgroup'][lgroup]['ID'], 'children': group_list})
                        plant_list.append({'label': plant, 
                        'value': nationOpt_dict[city][district][plant]['ID'], 'children': lgroup_list})
                    district_list.append({'label': district, 'value': district, 'children': plant_list})
                nationOpt.append({'label': city, 'value': city, 'children': district_list})
        except Exception as e:
            print(exception_detail(e))
        return successful_request({'nationOpt':nationOpt, 'groupIDLable':groupIDLable})
    def post(self):
        return self.get()
application_common.add_url_rule('/get_select_station',view_func=GetSelectStation.as_view('get_select_station'))
#-------------------------------------------------------------------------------
#使用位置 /stationlist
#找出子案場
@application_common.route('/station_search_ID', methods=['POST'])
def station_search_ID():
    user, db = check_user()
    if db == None:
        return logout()
    request_dict = request.json
    #print(request_dict)
    return_dict = {'ID_list': [], 'col_list': []}
    try:
        ID = request_dict['ID']
        _type = request_dict['type']
        return_dict['ID_list'].append(ID)
        return_dict['col_list'].append(_type)
    except:
        return bad_request(400, 'Bad Request. No ID and type.')
    search_filter = {}
    if _type == 'pv_plant':
        for plant in db.plant.find({'_id': ObjectId(ID)}):
            search_filter['PV'] = plant.get('name', '')
            search_filter['type'] = 'pv_lgroup'
    else:
        for equip in db.equipment.find({'_id': ObjectId(ID)}):
            search_filter['PV'] = equip.get('PV', '')
            if _type == 'pv_lgroup':
                search_filter['lgroup'] = equip.get('name', '')
                search_filter['type'] = 'pv_group'
    for equip in db.equipment.find(search_filter):
        return_dict['ID_list'].append(str(equip['_id']))
        return_dict['col_list'].append(equip.get('type', ''))
        if search_filter['type'] == 'pv_lgroup':
            for _equip in db.equipment.find({'PV': equip.get('PV'), 'lgroup': equip.get('name'), 'type': 'pv_group'}):
                return_dict['ID_list'].append(str(_equip['_id']))
                return_dict['col_list'].append(_equip.get('type', ''))
    #print(return_dict)
    return successful_request(return_dict)
#-------------------------------------------------------------------------------
#使用位置 /stationData
#找出母案場 資料 name ID
@application_common.route('/ID_get_parent_data', methods=['POST'])
def ID_get_parent_data():
    user, db = check_user()
    if db == None:
        return logout()
    request_dict = request.json
    #print(request_dict)
    return_dict = {}
    try:
        ID = request_dict['ID']
        ObjectId(ID)
    except:
        return bad_request(400, 'Bad Request. ID Error.')
    for plant in db.plant.find({'_id': ObjectId(ID)}):
        return_dict = {
            'ID': str(plant['_id']),
            'name': plant.get('name'),
            'collection': 'pv_plant'
        }
    for equip in db.equipment.find({'_id': ObjectId(ID)}):
        return_dict = {
            'ID': str(equip['_id']),
            'name': equip.get('name'),
            'collection': equip.get('type')
        }
        try:
            plant_data = db.plant.find_one({'name': equip.get('PV')})
            return_dict['PV'] = plant_data['name']
            return_dict['PV_ID'] = str(plant_data['_id'])
            if equip.get('type') == 'pv_group':
                lgroup_data = db.equipment.find_one({'PV': equip['PV'], 'name': equip['lgroup'], 'type': 'pv_lgroup'})
                return_dict['lgroup'] = lgroup_data['name']
                return_dict['lgroup_ID'] = str(lgroup_data['_id'])
        except:
            pass
    return successful_request(return_dict)
#-------------------------------------------------------------------------------
class StationSearchRegex(views.MethodView):
    def __init__(self) -> None:
        super().__init__()
        self.search_level = ['pv_plant', 'pv_lgroup', 'pv_group']
    def get_request_dict(self):
        request_dict = request.json
        return request_dict
    def post(self):
        user, db = check_user()
        if db == None:
            return logout()
        request_dict = self.get_request_dict()
        try:
            query = request_dict['query']
        except:
            return bad_request('Bad Request. No query.')
        try:
            if 'search_level' in request_dict:
                if isinstance(request_dict['search_level'], list):
                    self.search_level = request_dict['search_level']
        except:
            pass

        find_user = find_user_from_current_user()
        user_c=list(db.users.find({"user_id" : find_user}))[0]
        plant_filter = {}
        allow_plant_list = []
        if user_c['plant'][0] != 'total':
            for i in user_c['plant']:
                if 'name' not in plant_filter:
                    plant_filter['name'] = {'$in': []}
                plant_filter['name']['$in'].append(i)

        for plant in db.plant.find(plant_filter):
            allow_plant_list.append(plant.get('name', ""))
        fullquery = ''
        if '/' in query:
            fullquery = query
            query = query.split('/')[-1]
        return_list = []
        return_ID_list = []
        if 'pv_plant' in self.search_level:
            for plant in db.plant.find({'name': {'$regex': query}}):
                # This user has not auth to access 
                if plant.get("name") not in allow_plant_list:
                    continue
                return_list.append({
                    'name': plant.get('name', ''),
                    'realName': plant.get('name', ''),
                    'ID': str(plant['_id']),
                    'collection': plant.get('collection', 'pv_plant'),
                })
                return_ID_list.append(str(plant['_id']))
                # search lgroup or group under it
                for equip in db.equipment.find({'PV': plant.get('name'), 'type': {'$in': ['pv_lgroup', 'pv_group']}}):
                    if equip.get('type') in self.search_level:
                        name_str = '{}/'.format(equip.get('PV'))
                        return_dict = {
                            'realName': equip.get('name', ''),
                            'ID': str(equip['_id']),
                            'collection': equip.get('collection', None),
                            'PV': equip.get('PV')
                        }
                        if equip.get('type', '') == 'pv_lgroup':
                            name_str += '{}'.format(equip.get('name', ''))
                        elif equip.get('type', '') == 'pv_group':
                            name_str += '{}/{}'.format(equip.get('lgroup'),equip.get('name', ''))
                            return_dict['lgroup'] = equip.get('lgroup')
                        return_dict['name'] = name_str
                        return_list.append(return_dict)
                        return_ID_list.append(str(equip['_id']))
        for equip in db.equipment.find({'name': {'$regex': query}, 'type': {'$in': ['pv_lgroup', 'pv_group']}}).sort('_id', 1):
            # This user has not auth to access 
            if equip.get("PV") not in allow_plant_list or equip.get('type') not in self.search_level or str(equip['_id']) in return_ID_list:
                continue
            name_str = '{}/'.format(equip.get('PV'))
            return_dict = {
                'realName': equip.get('name', ''),
                'ID': str(equip['_id']),
                'collection': equip.get('collection', None),
                'PV': equip.get('PV'),
            }
            if equip.get('type', '') == 'pv_lgroup':
                name_str += '{}'.format(equip.get('name', ''))
            elif equip.get('type', '') == 'pv_group':
                name_str += '{}/{}'.format(equip.get('lgroup'),equip.get('name', ''))
                return_dict['lgroup'] = equip.get('lgroup')
            return_dict['name'] = name_str
            return_list.append(return_dict)
            return_ID_list.append(str(equip['_id']))

            if equip.get('type', '') == 'pv_lgroup' and 'pv_group' in self.search_level:
                # search group
                for group in db.equipment.find({'PV': equip.get('PV'), 'lgroup': equip.get('name'), 'type': 'pv_group'}):
                    if str(group['_id']) not in return_ID_list:
                        name_str = '{}/'.format(group.get('PV'))
                        name_str += '{}/{}'.format(group.get('lgroup'), group.get('name', ''))
                        return_list.append({
                            'name': name_str,
                            'realName': group.get('name', ''),
                            'ID': str(group['_id']),
                            'collection': group.get('collection', None),
                            'PV': equip.get('PV'),
                            'lgroup': group.get('lgroup')
                        })  
                        return_ID_list.append(str(group['_id']))
        if fullquery != '':
            _return_list = return_list.copy()
            return_list = []
            for x in _return_list:
                if x['name'] == fullquery:
                    return_list.append(x)
        return successful_request(return_list)
#使用位置 /stationlist
#使用 regex 來找 pv_plant pv_lgroup pv_group
application_common.add_url_rule('/station_search_regex', view_func=StationSearchRegex.as_view('station_search_regex'))
#-------------------------------------------------------------------------------
#使用位置 /stationGraphic
#使用 regex 來找 pv_plant pv_lgroup pv_group
class StationSearchRegexSLD(StationSearchRegex):
    def __init__(self) -> None:
        super().__init__()
        self.search_level = ['pv_lgroup', 'pv_group']
    def get_request_dict(self):
        if 'layout' in request.json:
            try:
                if request.json.get('layout', 0) == 1:
                    self.search_level = ['pv_group']
            except:
                pass
        return super().get_request_dict()
application_common.add_url_rule('/station_search_regex_SLD', view_func=StationSearchRegexSLD.as_view('station_search_regex_SLD'))
#-------------------------------------------------------------------------------
#使用位置 /stationGraphic /chartOverview
# 比較圖表
#使用 regex 來找  pv_group
class StationSearchRegexGroup(StationSearchRegex):
    def __init__(self) -> None:
        super().__init__()
        self.search_level = ['pv_group']
application_common.add_url_rule('/station_search_regex_group', view_func=StationSearchRegexGroup.as_view('station_search_regex_group'))
#-------------------------------------------------------------------------------
#使用位置 taipower /dispatch
#使用 regex 來找  pv_lgroup or pv_plant
class StationSearchRegexLgroup(StationSearchRegex):
    def __init__(self) -> None:
        super().__init__()
        self.search_level = ['pv_lgroup']
    def get_request_dict(self):
        request_dict = super().get_request_dict()
        only_lgroup = request_dict.get('only_lgroup', True)
        if only_lgroup:
            self.search_level = ['pv_lgroup']
        else:
            self.search_level = ['pv_plant', 'pv_lgroup']
        return request_dict
application_common.add_url_rule('/station_search_regex_lgroup', view_func=StationSearchRegexLgroup.as_view('station_search_regex_lgroup'))
#-------------------------------------------------------------------------------
#使用位置 taipower /setting
#使用 regex 來找 pv_plant only
class StationSearchRegexPlant(StationSearchRegex):
    def __init__(self) -> None:
        super().__init__()
        self.search_level = ['pv_plant']
application_common.add_url_rule('/station_search_regex_plant', view_func=StationSearchRegexPlant.as_view('station_search_regex_plant'))
#-------------------------------------------------------------------------------
#使用位置 /stationlist
#取得 儲存 刪除 使用者最愛
@application_common.route('/station_favorite', methods=['POST', 'GET', 'DELETE'])
def station_favorite_save():
    user, db = check_user()
    if db == None:
        return logout()
    find_user = find_user_from_current_user()

    user_c=list(db.users.find({"user_id" : find_user}))[0]
    request_dict = request.json
    if request.method == 'POST':
        try:
            name = request_dict['name']
            data = request_dict['data']
        except Exception as e:
            return bad_request(400, 'Bad Request. {}'.format(e))
        #print(name)
        #print(data)
        # find_user = current_user.get_id()
        db.stationGroup.update_one({'user_id': str(user_c['_id']), 'name': name}, {'$set': {'data': data, 'show': 1}}, upsert=True)
    elif request.method == 'GET':
        allow_ID_list = []
        # 確認案場是使用者能看的
        plant_filter = {}
        if user_c['plant'][0] != 'total':
            for i in user_c['plant']:
                if 'name' not in plant_filter:
                    plant_filter['name'] = {'$in': []}
                plant_filter['name']['$in'].append(i)

        for plant in db.plant.find(plant_filter):
            allow_ID_list.append(str(plant['_id']))
            for equip in db.equipment.find({'PV': plant.get('name', ''), 'type': {'$in': ['pv_lgroup', 'pv_group']}}):
                allow_ID_list.append(str(equip['_id']))
        #print(allow_ID_list)
        user_favorite = list(db.stationGroup.find({'user_id': str(user_c['_id']), 'show': 1}))
        _user_favorite = []
        for d in user_favorite:
            d.pop('_id', None)
            d.pop('user_id', None)
            d_data = []
            for i in d.get('data', []):
                if i.get('ID', None) in allow_ID_list:
                    d_data.append(i)
            d['data'] = d_data
            _user_favorite.append(d)
        default_favorite = None
        for d in db.stationGroup.find({'user_id': str(user_c['_id']), 'default': True}):
            d.pop('_id', None)
            d.pop('user_id', None)
            d_data = []
            for i in d.get('data', []):
                if i.get('ID', None) in allow_ID_list:
                    d_data.append(i)
            d['data'] = d_data
            default_favorite = d
        return successful_request({'favorite_list': _user_favorite, 'default_favorite': default_favorite})
    elif request.method == 'DELETE':
        try:
            name = request_dict['name']
        except Exception as e:
            return bad_request(400, 'Bad Request. {}'.format(e))
        db.stationGroup.update_one({'user_id': find_user, 'name': name}, {'$set': {'show': 0}})
        
    return successful_request()
#-------------------------------------------------------------------------------
#使用位置 /stationlist
#取得 使用者最愛
@application_common.route('/get_station_favorite', methods=['POST', 'GET'])
def get_station_favorite():
    user, db = check_user()
    if db == None:
        return logout()
    find_user = find_user_from_current_user()

    user_c=list(db.users.find({"user_id" : find_user}))[0]

    allow_ID_list = []
    # 確認案場是使用者能看的
    plant_filter = {}
    if user_c['plant'][0] != 'total':
        for i in user_c['plant']:
            if 'name' not in plant_filter:
                plant_filter['name'] = {'$in': []}
            plant_filter['name']['$in'].append(i)

    for plant in db.plant.find(plant_filter):
        allow_ID_list.append(str(plant['_id']))
        for equip in db.equipment.find({'PV': plant.get('name', ''), 'type': {'$in': ['pv_lgroup', 'pv_group']}}):
            allow_ID_list.append(str(equip['_id']))
    #print(allow_ID_list)
    user_favorite = list(db.stationGroup.find({'user_id': str(user_c['_id']), 'show': 1}))
    _user_favorite = []
    for d in user_favorite:
        d.pop('_id', None)
        d.pop('user_id', None)
        d_data = []
        for i in d.get('data', []):
            if i.get('ID', None) in allow_ID_list:
                if i.get('collection', None) == 'pv_plant':
                    d_data.append({
                        'ID': i.get('ID', None),
                        'collection': i.get('collection', None),
                        'name': db.plant.find_one({'_id': ObjectId(i.get('ID', None))}).get('name', '')
                    })
                elif i.get('collection', None) == 'pv_lgroup':
                    equip_data = db.equipment.find_one({'_id': ObjectId(i.get('ID', None))})
                    d_data.append({
                        'ID': i.get('ID', None),
                        'collection': i.get('collection', None),
                        'name': '{}/{}'.format(equip_data.get('PV'), equip_data.get('name'))
                    })
                elif i.get('collection', None) == 'pv_group':
                    equip_data = db.equipment.find_one({'_id': ObjectId(i.get('ID', None))})
                    d_data.append({
                        'ID': i.get('ID', None),
                        'collection': i.get('collection', None),
                        'name': '{}/{}/{}'.format(equip_data.get('PV'), equip_data.get('lgroup'), equip_data.get('name'))
                    })
        d['data'] = d_data
        _user_favorite.append(d)
    default_favorite = None
    d = None
    d = db.stationGroup.find_one({'user_id': str(user_c['_id']), 'default': True})
    if d == None:
        d = db.stationGroup.find_one({'user_id': 'all', 'default': True})
    if d != None:
        d.pop('_id', None)
        d.pop('user_id', None)
        d_data = []
        for i in d.get('data', []):
            if i.get('ID', None) in allow_ID_list:
                if i.get('collection', None) == 'pv_plant':
                    d_data.append({
                        'ID': i.get('ID', None),
                        'collection': i.get('collection', None),
                        'name': db.plant.find_one({'_id': ObjectId(i.get('ID', None))}).get('name', '')
                    })
                elif i.get('collection', None) == 'pv_lgroup':
                    equip_data = db.equipment.find_one({'_id': ObjectId(i.get('ID', None))})
                    d_data.append({
                        'ID': i.get('ID', None),
                        'collection': i.get('collection', None),
                        'name': '{}/{}'.format(equip_data.get('PV'), equip_data.get('name'))
                    })
                elif i.get('collection', None) == 'pv_group':
                    equip_data = db.equipment.find_one({'_id': ObjectId(i.get('ID', None))})
                    d_data.append({
                        'ID': i.get('ID', None),
                        'collection': i.get('collection', None),
                        'name': '{}/{}/{}'.format(equip_data.get('PV'), equip_data.get('lgroup'), equip_data.get('name'))
                    })
        d['data'] = d_data
        default_favorite = d
    return successful_request({'favorite_list': _user_favorite, 'default_favorite': default_favorite})
#-------------------------------------------------------------------------------
#使用位置 /stationlist
#儲存  使用者最愛
@application_common.route('/save_station_favorite', methods=['POST'])
def save_station_favorite():
    user, db = check_user()
    if db == None:
        return logout()
    find_user = find_user_from_current_user()
    user_c=list(db.users.find({"user_id" : find_user}))[0]
    request_dict = request.json
    if request.method == 'POST':
        try:
            name = request_dict['name']
            data = request_dict['data']
        except Exception as e:
            return bad_request(400, 'Bad Request. {}'.format(e))
        for d in data:
            d.pop("name", None)
            d.pop("realName", None)
        #print(name)
        #print(data)
        # find_user = current_user.get_id()
        db.stationGroup.update_one({'user_id': str(user_c['_id']), 'name': name}, {'$set': {'data': data, 'show': 1}}, upsert=True)
    return successful_request()
#-------------------------------------------------------------------------------
#使用位置 /stationlist
#刪除 使用者最愛
@application_common.route('/delete_station_favorite', methods=['POST'])
def delete_station_favorite():
    user, db = check_user()
    if db == None:
        return logout()
    find_user = find_user_from_current_user()
    user_c=list(db.users.find({"user_id" : find_user}))[0]
    request_dict = request.json
    try:
        name = request_dict['name']
    except Exception as e:
        return bad_request(400, 'Bad Request. {}'.format(e))
    db.stationGroup.update_one({'user_id': str(user_c['_id']), 'name': name}, {'$set': {'show': 0}})
    return successful_request()
#-------------------------------------------------------------------------------
#使用位置 /selectStation
class GetSelectStationSystem(views.MethodView):
    def get(self):
        user, db = check_user()
        if db == None:
            return logout()
        find_user = find_user_from_current_user()

        user_c=list(db.users.find({"user_id" : find_user}))[0]
        system_dict = {}
        groupIDLable = {}
        try:
            plant_filter = {}
            if user_c['plant'][0] != 'total':
                for i in user_c['plant']:
                    if 'name' not in plant_filter:
                        plant_filter['name'] = {'$in': []}
                    plant_filter['name']['$in'].append(i)

            for plant in db.plant.find(plant_filter):
                try:
                    system = plant.get('type', None)
                    if system not in system_dict:
                        system_dict[system] = {}
                    if plant['name'] not in system_dict[system]:
                        system_dict[system][plant['name']] = {'name': plant['name'],
                        'ID': str(plant['_id']), 'lgroup': {}}
                    for lgroup in db.equipment.find({'PV': plant['name'], 'type': 'pv_lgroup'}):
                        if lgroup['name'] not in system_dict[system][plant['name']]['lgroup']:
                            system_dict[system][plant['name']]['lgroup'][lgroup['name']] = {
                                'name': lgroup['name'], 'ID': str(lgroup['_id']), 'group': {}
                            }
                        for group in db.equipment.find({'PV': plant['name'], 'lgroup': lgroup['name'], 'type': 'pv_group'}):
                            #if group['name'] not in nationOpt_dict[city][district][plant['name']]['lgroup'][lgroup['name']]['group']:
                            system_dict[system][plant['name']]['lgroup'][lgroup['name']]['group'][group['name']] = {
                                'name': group['name'], 'ID': str(group['_id'])
                            }
                            groupIDLable[str(group['_id'])] = [system, plant['name'], lgroup['name'], group['name']]
                except Exception as e:
                    print(exception_detail(e))
            
            systemList = [{'label': '全部', 'value': 'ALL'}]
            for system in system_dict:
                plant_list = []
                for plant in system_dict[system]:
                    lgroup_list = []
                    for lgroup in system_dict[system][plant]['lgroup']:
                        group_list = []
                        for group in system_dict[system][plant]['lgroup'][lgroup]['group']:
                            group_list.append({'label': group, 'value': system_dict[system][plant]['lgroup'][lgroup]['group'][group]['ID']})
                        lgroup_list.append({'label': lgroup, 
                        'value': system_dict[system][plant]['lgroup'][lgroup]['ID'], 'children': group_list})
                    plant_list.append({'label': plant, 
                    'value': system_dict[system][plant]['ID'], 'children': lgroup_list})
                system_translate = {"DG": "DG","PV": "地面型","BESS": "屋頂型","WT": "水面型"}
                systemList.append({'label': system_translate.get(system, system), 'value': system, 'children': plant_list})
        except Exception as e:
            print(exception_detail(e))
        return successful_request({'system': systemList, 'groupIDLable':groupIDLable})
    def post(self):
        return self.get()
application_common.add_url_rule('/get_select_station_system',view_func=GetSelectStationSystem.as_view('get_select_station_system'))
#-------------------------------------------------------------------------------
#使用位置 /stationlist
class GetCardOverviewReal(views.MethodView):
    def __init__(self) -> None:
        super().__init__()
        self.time = datetime.datetime.strftime(datetime.datetime.now(), '%Y-%m-%d')
        self.time = datetime.datetime.strptime(self.time, '%Y-%m-%d')
    def get(self):
        return self.main_func()
    def post(self):
        return self.main_func()
    def main_func(self):
        self.user, self.db = check_user()
        if self.db == None:
            return logout()
        try:
            dict1 = request.json
            try:
                ID_list = dict1['ID_list']
                if not isinstance(ID_list, list):
                    raise TypeError('type error')
            except Exception as e:
                return bad_request(400, 'Bad Request. ID_list error {}'.format(e))
            try:
                col_list = dict1['col_list']
                if not isinstance(col_list, list):
                    raise TypeError('type error')
            except Exception as e:
                return bad_request(400, 'Bad Request. col_list error {}'.format(e))
            if(len(ID_list) != len(col_list)):
                return bad_request(400, 'Bad Request. Length not equal.')
        except Exception as e:
            return bad_request(400, 'Bad Request. Due to {}'.format(e))

        data_list = []
        for i in range(len(ID_list)):
            try:
                data_list.append(self.get_data(ID_list[i], col_list[i]))
            except Exception as e:
                print(exception_detail(e))
                continue
        return successful_request(data_list)

    def get_data(self, ID, col):
        db = self.db
        equip_col = 'plant' if col == 'pv_plant' else 'equipment'
        data_dict = {}
        find_user = find_user_from_current_user()
        user_c=list(db.users.find({"user_id" : find_user}))[0]
        for x in db[equip_col].find({'_id': ObjectId(ID)}):
            data_dict['led_state'] = x.get('led_state', 0)
            data_dict['work'] = True if  x.get('led_state', 0) == 0 else False
            # establish filter query to find child equip
            child_equip_filter = {}
            if x['type'] == 'PV':
                child_equip_filter['PV'] = x['name']
            if x['type'] == 'pv_lgroup':
                child_equip_filter['PV'] = x['PV']
                child_equip_filter['lgroup'] = x['name']
                data_dict['PV'] = x['PV']
            if x['type'] == 'pv_group':
                child_equip_filter['PV'] = x['PV']
                child_equip_filter['lgroup'] = x['lgroup']
                child_equip_filter['group'] = x['name']
                data_dict['PV'] = x['PV']
                data_dict['lgroup'] = x['lgroup']
            # Get Child equipment
            child_equip_ID_list = [str(x['_id'])]
            for equip in db.equipment.find(child_equip_filter):
                child_equip_ID_list.append(str(equip['_id']))
            # get all alarm_count from both self and childs
            data_dict['alert_count'] = db.alarm.count_documents({'ID': {'$in': child_equip_ID_list}, 'returntime': ''})
            data_dict['no_alert'] = True if data_dict['alert_count'] == 0 else False
            data_dict['name'] = x['name']
            data_dict['ID'] = ID
            today = datetime.datetime.strftime(datetime.datetime.now(), '%Y-%m-%d')
            today = datetime.datetime.strptime(today, '%Y-%m-%d')
            if user_c.get('pageType') == 'taipower':
                data_dict['capacity'] = round(x.get('capacity', '---'))
            else:
                data_dict['capacity'] = round(x.get('capacity', '---'), 3)
            try:
                data_dict['today_kwh'] = round(db.meter_cal.find_one({'ID': ID, 'time_interval': 'day', 'time': today})['kwh'])
            except:
                data_dict['today_kwh'] = '---'
            try:
                this_month = datetime.datetime.strftime(self.time, '%Y-%m')
                this_month = datetime.datetime.strptime(this_month, '%Y-%m')
                data_dict['month_kwh'] = round(db.meter_cal.find_one({'ID': ID, 'time_interval': 'month', 'time': this_month})['kwh'])
            except:
                data_dict['month_kwh'] = '---'
            try:
                this_year = datetime.datetime.strftime(self.time, '%Y')
                this_year = datetime.datetime.strptime(this_year, '%Y')
                data_dict['year_kwh'] = round(db.meter_cal.find_one({'ID': ID, 'time_interval': 'year', 'time': this_year})['kwh'])
            except:
                data_dict['year_kwh'] = '---'
            gen_stats = db.pr_cal.find_one({'ID': ID, 'time_interval': 'day', 'time': today})
            try:
                if 'parameter' in user_c:
                    data_dict['pr'] = round(gen_stats[user_c['parameter'].get('pr', 'pr')], 2)
                else:
                    data_dict['pr'] = round(gen_stats['pr'], 2)
                 
            except:
                data_dict['pr'] = '---'
            try:
                data_dict['dmy'] = round(gen_stats['dmy'], 3)
                 
            except:
                data_dict['dmy'] = '---'
            try:
                data_dict['irrh'] = round(db.irrh_cal.find_one({'ID': c.plant_group_ID_find_sun_ID(db, ID, col), 
                'time_interval': 'day', 'time': today})['irrh'], 2)
            except:
                data_dict['irrh'] = '---'
            try:
                data_dict['p'] = c.current_data(db, x.get("collection"), str(x['_id']))[0]['p']
                data_dict['p'] = round(data_dict['p'])
            except:
                data_dict['p'] = '---'
            # get iot list
            iot_filter = {}
            if x['type'] == 'PV':
                iot_filter = {'PV': x['name']}
            elif x['type'] == 'pv_lgroup':
                iot_filter = {'PV': x['PV'], 'lgroup': x['name']}
            elif x['type'] == 'pv_group':
                iot_filter = {'PV': x['PV'], 'lgroup': x['lgroup'], 'group': x['name']}
            last_connect_time_list = []
            communi_list = []
            for iot in db.iot.find(iot_filter):
                try:
                    last_connect_time_list.append(datetime.datetime.now() - iot.get('last_connect_time'))
                except:
                    last_connect_time_list.append(None)
                try:
                    if iot['check'] == 0 and iot['status'] == 'pushed':
                        # 根據Iotlink_b的程式 alarm 已發送
                        communi_list.append(False)
                    else:
                        # 通訊正常
                        communi_list.append(True)
                except:
                    communi_list.append(None)
            data_dict['lastTime'] = '---' if None in last_connect_time_list or len(last_connect_time_list) == 0 else '0 分鐘前' if max(last_connect_time_list) < datetime.timedelta(minutes=10) else '{} 分鐘前'.format(int(max(last_connect_time_list).seconds/60)) \
            if max(last_connect_time_list) < datetime.timedelta(hours=1) else  '{} 小時前'.format(int(max(last_connect_time_list).seconds/3600)) if max(last_connect_time_list) < datetime.timedelta(days=1) else '超過24小時前'
            data_dict['lastTime_i18n'] = {
                'zh-TW': '---' if None in last_connect_time_list or len(last_connect_time_list) == 0 else '0 分鐘前' if max(last_connect_time_list) < datetime.timedelta(minutes=10) else '{} 分鐘前'.format(int(max(last_connect_time_list).seconds/60)) \
                    if max(last_connect_time_list) < datetime.timedelta(hours=1) else  '{} 小時前'.format(int(max(last_connect_time_list).seconds/3600)) if max(last_connect_time_list) < datetime.timedelta(days=1) else '超過24小時前',
                'en-US': '---' if None in last_connect_time_list or len(last_connect_time_list) == 0 else '0 min ago' if max(last_connect_time_list) < datetime.timedelta(minutes=10) else '{} mins ago'.format(int(max(last_connect_time_list).seconds/60)) \
                    if max(last_connect_time_list) < datetime.timedelta(hours=1) else  '{} hours ago'.format(int(max(last_connect_time_list).seconds/3600)) if max(last_connect_time_list) < datetime.timedelta(days=1) else 'Over 24 hours ago',
            }
            data_dict['communi'] = True if None in communi_list or len(communi_list) == 0 or (not (False in communi_list)) else False
            data_dict['profit'] = '---'
            data_dict['type'] = x['type']
            data_dict['collection'] = x['collection']
            #案場圖片
            data_dict['imgsrc'] = '{}/images/plant_image/{}.*'.format(current_app.config['UPLOAD_FOLDER'], data_dict['ID'])
            find_img = glob.glob(data_dict['imgsrc'])
            try:
                if find_img:
                    data_dict['imgsrc'] = 'solar_static/images/plant_image/{}'.format(find_img[-1].split('/')[-1])
                else: 
                    data_dict['imgsrc'] = 'solar_static/images/plant_image/default.png'
            except:
                data_dict['imgsrc'] = 'solar_static/images/plant_image/default.png'

            # Carbon Reduction
            try:
                data_dict['carbon_reduction'] = round(data_dict['today_kwh']*0.502)   # 109 年排碳係數 
            except:
                data_dict['carbon_reduction'] = '---'

        return data_dict
application_common.add_url_rule('/get_card_overview_real', view_func=GetCardOverviewReal.as_view('get_card_overview_real'))
#-------------------------------------------------------------------------------
#使用位置 電站管理 stationTabBasic 取得資訊頁資料
class GetBasicDataReal(GetCardOverviewReal):
    def get_data(self, ID, col):
        db = self.db
        data_dict = super().get_data(ID, col)
        plant_name = ''
        if data_dict['collection'] != 'pv_plant':
            for equip in db.equipment.find({'_id': ObjectId(data_dict['ID'])}):
                plant_name = equip.get('PV', '')
        else:
            plant_name = data_dict['name']
        for plant in db.plant.find({'name': plant_name}):
            weather_data = c.get_weather_forecast(db, plant.get('location', {}).get('city', {}))
            data_dict['weather'] = {
                'imgurl': weather_data.get('imgurl', ''),
                'temperature': weather_data.get('T', '---'),
                'status':weather_data.get('Wx', '---'),
                'rain': '降雨機率{}%'.format(
                    '---' if isinstance(weather_data.get('PoP6h', '---'), str) else int(weather_data['PoP6h']))
            }
        return data_dict
application_common.add_url_rule('/get_basic_data_real', view_func=GetBasicDataReal.as_view('get_basic_data_real'))
#-------------------------------------------------------------------------------
#使用位置 stationData 電站管理 stationTabBasic 取得資訊頁資料
class GetBasicDataLocale(GetCardOverviewReal):
    def get_data(self, ID, col):
        db = self.db
        data_dict = super().get_data(ID, col)
        plant_name = ''
        if data_dict['collection'] != 'pv_plant':
            for equip in db.equipment.find({'_id': ObjectId(data_dict['ID'])}):
                plant_name = equip.get('PV', '')
        else:
            plant_name = data_dict['name']
        for plant in db.plant.find({'name': plant_name}):
            weather_data = c.get_weather_forecast_by_date(db, plant.get('location', {}).get('city', ''))
            data_dict['weather'] = {
                'imgurl': weather_data.get('imgurl', ''),
                'temperature': weather_data.get('T', '---'),
                'status':weather_data.get('Wx', '---'),
                'rain': '---' if isinstance(weather_data.get('PoP6h', '---'), str) else int(weather_data['PoP6h'])
            }
        return data_dict
    
application_common.add_url_rule('/get_basic_data_locale', view_func=GetBasicDataLocale.as_view('get_basic_data_locale'))
#-------------------------------------------------------------------------------
#使用位置 電站管理 /stationlist  取得plant資料
@application_common.route('/get_plant_detail', methods=['POST'])
def get_plant_detail():
    user,db = check_user()
    if(db == None):
        return logout() 
    request_dict = request.json
    try:
        ID = request_dict['ID']
        ObjectId(ID)
    except Exception as e:
        return bad_request(400, 'Bad Request. ID error.')
    dict1 = {'client_info': {}, 'paets_info': {}}
    for plant in db.plant.find({'_id': ObjectId(ID)}):
        #print(plant)
        try:
            dict1['start_date'] = datetime.datetime.strftime(plant.get('start_date', '---'), '%Y-%m-%d %H:%M')
        except:
            dict1['start_date'] = "---"

        dict1['capacity'] = plant.get('capacity', '---')
        dict1['plant_address'] = plant.get('plant_address', '---')
        dict1['coordinates'] = plant.get('coordinates', '---')
        dict1['typeNumb'] = plant.get('typeNumb', '---')
        dict1['expectedPower'] = plant.get('expectedPower', '---')
        dict1['inverter_model'] = plant.get('inverter_model', '---')
        try:
            if len(plant.get('event', [])) == 0:
                dict1['event'] = ''
            else:
                str1 = ''
                for i, x in enumerate(plant.get('event', [])):
                    str1 += '{}. {}'.format(i+1, x)
                dict1['event'] = str1
        except:
            dict1['event'] = ''
        dict1['client_info']['unit'] = plant.get('client_info', {}).get('unit', '---')
        dict1['client_info']['admin'] = '/'.join(plant.get('client_info', {}).get('admin', []))
        dict1['client_info']['TEL'] = plant.get('client_info', {}).get('TEL', '---')
        try:
            if len(plant.get('client_info', {}).get('event', [])) == 0:
                dict1['client_info']['event'] = ''
            else:
                str1 = ''
                for i, x in enumerate(plant.get('client_info', {}).get('event', [])):
                    str1 += '{}. {}'.format(i+1, x)
                dict1['client_info']['event'] = str1
        except:
            dict1['client_info']['event'] = ''
        dict1['paets_info']['unit'] = plant.get('paets_info', {}).get('unit', '---')
        dict1['paets_info']['TEL'] = plant.get('paets_info', {}).get('TEL', '---')
        dict1['paets_info']['admin'] = '/'.join(plant.get('paets_info', {}).get('admin', []))
        try:
            if len(plant.get('paets_info', {}).get('event', [])) == 0:
                dict1['paets_info']['event'] = ''
            else:
                str1 = ''
                for i, x in enumerate(plant.get('paets_info', {}).get('event', [])):
                    str1 += '{}. {}'.format(i+1, x)
                dict1['paets_info']['event'] = str1
        except:
            dict1['paets_info']['event'] = ''
       # dict1[''] = plant.get('', '---')

    return successful_request(dict1)
#-------------------------------------------------------------------------------
#用在Nav bar顯示
@application_common.route('/alarm_total_count')
def alarm_total_count():
    user, db = check_user()
    if db == None:
        return logout()
    find_user = find_user_from_current_user()

    user_c=list(db.users.find({"user_id" : find_user}))[0]
    plant_filter = {}
    if user_c['plant'][0] != 'total':
        for i in user_c['plant']:
            if 'name' not in plant_filter:
                plant_filter['name'] = {'$in': []}
            plant_filter['name']['$in'].append(i)
    ID_list = []
    for plant in db.plant.find(plant_filter):
        ID_list.append(str(plant['_id']))   # plant
        for equip in db.equipment.find({'PV': plant.get('name', '')}):
            ID_list.append(str(equip['_id']))   # lgroup group inv string meter sensor io, etc
        for iot in db.iot.find({'PV': plant.get('name', '')}):
            ID_list.append(str(iot['_id']))   # iot
    #print(ID_list)
    alarm_count = db.alarm.count_documents({'ID': { '$in': ID_list}, 'returntime': ''})
    #print(alarm_count)
    return successful_request(alarm_count)
#-------------------------------------------------------------------------------
#使用位置 電站管理 stationPop
#用id取得底下未復歸警報
@application_common.route('/unreturn_alarm_count_by_id', methods=['POST'])
def unreturn_alarm_count_by_id():
    user,db = check_user()
    if(db == None):
        return logout() 
    request_dict = request.json
    try:
        ID = request_dict['ID']
        ObjectId(ID)
    except:
        return bad_request(400, 'Bad Request. ID error.')
    equip_filter = {}
    iot_filter = {}
    equip_id_list = []
    # If found, it is plant
    for plant in db.plant.find({'_id': ObjectId(ID)}).limit(1):
        equip_filter = {'PV': plant.get('name')}
        iot_filter =  {'PV': plant.get('name')}
        equip_id_list.append(str(plant['_id']))
    # If found, it is lgroup or group
    for l_group in db.equipment.find({'_id': ObjectId(ID)}).limit(1):
        if l_group.get('type') == 'pv_lgroup':
            equip_filter = {'PV': l_group.get('PV'), 'lgroup': l_group.get('name')}
            iot_filter = {'PV': l_group.get('PV'), 'lgroup': l_group.get('name')}
        else:
            equip_filter = {'PV': l_group.get('PV'), 'lgroup': l_group.get('lgroup'), 'group': l_group.get('name')}
            iot_filter = {'PV': l_group.get('PV'), 'lgroup': l_group.get('lgroup'), 'group': l_group.get('name')} 
    for equip in db.equipment.find(equip_filter):
        equip_id_list.append(str(equip['_id']))
    for iot in db.iot.find(iot_filter):
        equip_id_list.append(str(iot['_id']))
    alarm_count = db.alarm.count_documents({'ID': {'$in': equip_id_list}, 'returntime': ''})
    return successful_request({
        'alarm_count': alarm_count,
        'no_alarm': True if alarm_count == 0 else False
    })
#-------------------------------------------------------------------------------
#使用位置 警報 /alertOverview
class AlarmGet(views.MethodView):
    def __init__(self, alarm_collection="alarm"):
        self.alarm_collection = alarm_collection
    def get(self):
        return bad_request(400, 'Please Use Post')
    def post(self):
        user, db = check_user()
        if db == None:
            return logout()
        #print(request.json)
        request_dict = request.json
        alarm_filter = {}
        try:
            alarm_filter.update(request_dict.get('filter', {}))
        except Exception as e:
            bad_request(400, 'Bad Request. {}'.format(exception_detail(e)))
        alarm_filter['level'] = {'$gte': 0, '$lt': 4}
        if request_dict.get('time', {}).get('mode', '') == 'single':
            try:
                start_date = datetime.datetime.strptime(request_dict['time']['start_date'], '%Y-%m-%d')
                end_date = start_date + datetime.timedelta(days=1)
                alarm_filter['time'] = {'$gte': start_date, '$lt': end_date}
            except:
                return bad_request(400, 'Time error')
        elif request_dict.get('time', {}).get('mode', '') == 'interval':
            try:
                start_date = datetime.datetime.strptime(request_dict['time']['start_date'], '%Y-%m-%d')
                end_date = datetime.datetime.strptime(request_dict['time']['end_date'], '%Y-%m-%d')
                alarm_filter['time'] = {'$gte': start_date, '$lt': end_date+datetime.timedelta(days=1)}
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
            alarm_filter['time'] = {'$gte': start_date, '$lt': end_date}
        equip_filter = {}
        if request_dict.get('equip_type', '') != 'all':
            try:
                if request_dict['equip_type'] != 'iot':
                    equip_filter['type'] = request_dict['equip_type']
                else:
                    equip_filter['true_type'] = request_dict['equip_type']
            except:
                return bad_request(400, 'Bad Request. equip_type must specify.')
        alarm_filter['ID'] = {'$in': []}
        # plant buffer. 警報對應案場資料
        plant_buffer = {}
        for plant in db.plant.find({}):
            plant_buffer[plant.get('name', '')] = plant
        equipment_buffer = {}
        iot_buffer = {}
        if request_dict.get('plant', {}).get('all', True) == False:
            try:
                ID_list = request_dict['plant']['ID']
                col_list = request_dict['plant']['col']
                for i, _ID in enumerate(ID_list):
                    try:
                        if request_dict['equip_type'] == 'all': 
                            alarm_filter['ID']['$in'].append(_ID)
                        _equip_filter = equip_filter 
                        if col_list[i] == 'pv_plant':
                            data = db.plant.find_one({'_id': ObjectId(_ID)})
                            _equip_filter['PV'] = data['name']
                            #_equip_filter['lgroup'] = {'$exists': False}
                        else:
                            data = db.equipment.find_one({'_id': ObjectId(_ID)})
                            equipment_buffer[str(data['_id'])] = data
                            if col_list[i] == 'pv_lgroup':
                                _equip_filter['PV'] = data['PV']
                                _equip_filter['lgroup'] = data['name']
                                #_equip_filter['group'] = {'$exists': False}
                            elif col_list[i] == 'pv_group':
                                _equip_filter['PV'] = data['PV']
                                _equip_filter['lgroup'] = data['lgroup']
                                _equip_filter['group'] = data['name']
                            elif col_list[i] == 'iot':
                                for iot in db.iot.find({'_id': ObjectId(_ID)}):
                                    iot_buffer[str(iot['_id'])] = iot
                                    alarm_filter['ID']['$in'].append(str(iot['_id']))
                            else: # inv, string, sun, wind, etc...
                                _equip_filter['_id'] = ObjectId(_ID)

                        #print(_equip_filter)
                        if col_list[i] == 'pv_group' and (_equip_filter.get('true_type', '') == 'iot' or request_dict['equip_type'] == 'all'):   #要多找iot
                            for iot in db.iot.find(_equip_filter):
                                iot_buffer[str(iot['_id'])] = iot
                                alarm_filter['ID']['$in'].append(str(iot['_id']))
                        for equip in db.equipment.find(_equip_filter):
                            # ref equipment skip
                            if isinstance(equip.get('PV'), list):
                                if 'PV' in _equip_filter and equip.get('PV')[0] != _equip_filter['PV']:
                                    continue
                            equipment_buffer[str(equip['_id'])] = equip
                            alarm_filter['ID']['$in'].append(str(equip['_id']))
                    except:
                        continue
            except:
                return bad_request(400, 'Bad Request. Plant all is false then ID and col must provided')
        else:
            plant_filter = {}
            find_user = find_user_from_current_user()

            user_c=list(db.users.find({"user_id" : find_user}))[0]
            if user_c['plant'][0] != 'total':
                for i in user_c['plant']:
                    if 'name' not in plant_filter:
                        plant_filter['name'] = {'$in': []}
                    plant_filter['name']['$in'].append(i)
            for plant in db.plant.find(plant_filter):
                if request_dict['equip_type'] in ['all','pv_plant']: 
                    alarm_filter['ID']['$in'].append(str(plant['_id']))
                equip_filter['PV'] = plant.get('name', '')
                for equip in db.equipment.find(equip_filter):
                    equipment_buffer[str(equip['_id'])] = equip
                    alarm_filter['ID']['$in'].append(str(equip['_id']))
                    if equip.get('type', None) == 'pv_group' and (equip_filter.get('true_type', '') == 'iot' or request_dict['equip_type'] == 'all'):
                        for iot in db.iot.find({'PV': plant.get('name', ''), 'lgroup': equip['lgroup'], 'group': equip['name']}):
                            iot_buffer[str(iot['_id'])] = iot
                            alarm_filter['ID']['$in'].append(str(iot['_id']))   # iot
        if request_dict.get('alarm_group', '') != 'all':
            try:
                alarm_filter['group'] = request_dict['alarm_group']
            except:
                return bad_request(400, 'Bad Request. The alarm_group must provide')
        if request_dict.get('alarm_type', '') != 'all':
            try:
                if request_dict['alarm_type'] == 'not_returned':
                    alarm_filter['returntime'] = ''
                elif request_dict['alarm_type'] == 'returned':
                    alarm_filter['returntime'] = {'$ne': ''}
                    #alarm_filter['return_state'] = 1
                elif request_dict['alarm_type'] == 'not_archived':
                    alarm_filter['show'] = 1
                elif request_dict['alarm_type'] == 'archived':
                    alarm_filter['show'] = 2
            except:
                return bad_request(400, 'Bad Request. The alarm_type must provide')
        #print(alarm_filter)
        alarm_data = []
        alarm_total = db.alarm.count_documents(alarm_filter)
        documents_per_page = request_dict.get('documents_per_page', 10)
        total_page = math.ceil(alarm_total/documents_per_page)
        page = request_dict.get('page', 1)
        #print(alarm_filter)
        if type(page) != int:
            return bad_request(400, 'Bad Request. Error page. Should be integer.')
        for alarm in db[self.alarm_collection].find(alarm_filter).skip((page-1)*documents_per_page).limit(documents_per_page).sort('time', -1):
            try:
                place_str = ''   # 類型 廠區 分組 分區
                equip_type = ''
                equip_name = ''
                system_translate = {"DG": "DG","PV": "地面型","BESS": "屋頂型","WT": "水面型"}
                type_translate = {"inv": "變流器", "string": "串電流錶", "io": "開關", "sun": "日照計", 
                "temp": "溫度計", "wind": "風速計", "meter": "智慧電錶", "pv_meter": "智慧電錶"}
                if alarm['ID'] not in equipment_buffer and alarm['ID'] not in iot_buffer:   #代表是plant
                    _data = db.plant.find_one({'_id': ObjectId(alarm['ID'])})
                    place_str = system_translate.get(_data.get('type',''),_data.get('type','')) + '-' + _data.get('name', '')
                    equip_type = '案場'
                    equip_name = _data.get('name', '')
                elif alarm['ID'] in iot_buffer:   #代表是iot
                    _data = iot_buffer[alarm['ID']]
                    place_str = '-'.join([system_translate.get(plant_buffer.get(_data.get('PV')).get('type'), ''), _data.get('PV', ''), _data.get('lgroup',''), _data.get('group', '')])
                    equip_type = '資料收集器'
                    equip_name = _data.get('name',  '資料收集器')
                else:   # those in equipment
                    _data = equipment_buffer[alarm['ID']]
                    place_str = '-'.join([
                        system_translate.get(
                            plant_buffer.get(
                                _data.get('PV') if isinstance(_data.get('PV'), str) else _data.get('PV', [''])[0])
                            .get('type'), ''), 
                            _data.get('PV') if isinstance(_data.get('PV'), str) else _data.get('PV', [''])[0], 
                        ''
                    ])
                    equip_name = _data.get('name',  '')
                    if _data.get('type') == 'pv_lgroup':
                        place_str += _data.get('name', '')
                        equip_type = '分區' if _data.get('Devide_type', '') == '' else type_translate.get(_data.get('Device_type', ''), _data.get('Device_type', ''))
                    elif _data.get('type') == 'pv_group':
                        place_str += '-'.join([_data.get('lgroup', ''), _data.get('name', '')])
                        equip_type = '分組' if _data.get('Devide_type', '') == '' else type_translate.get(_data.get('Device_type', ''), _data.get('Device_type', ''))
                    else:
                        place_str += '-'.join([
                            _data.get('lgroup', '') if isinstance(_data.get('lgroup', ''), str) else _data.get('lgroup', [''])[0], 
                            _data.get('group', '') if isinstance(_data.get('group', ''), str) else _data.get('group', [''])[0]
                        ])
                        equip_type = type_translate.get(_data.get('type', ''), _data.get('type', ''))
                # Get Dispatch Name
                try:
                    dispatch_name = None if alarm.get('dispatch_ID', None) == None else db.dispatch.find_one({'_id': ObjectId(alarm.get('dispatch_ID', None))})['name']
                except:
                    dispatch_name = None
                _dict = {
                    '_id': str(alarm['_id']), 'ID': str(alarm['ID']),
                    'alarm_place': place_str,
                    'alarm_group': alarm.get('group', ''), 'alarm_event': alarm.get('event', ''),
                    'equip_type': equip_type, 'equip_name': equip_name,
                    'about': alarm.get('about', None),
                    'level': alarm.get('level', 4),
                    'time': datetime.datetime.strftime(alarm.get('time'), '%Y-%m-%d %H:%M:%S'),
                    'checktime': '' if alarm.get('checktime', '') == '' else datetime.datetime.strftime(alarm.get('checktime'), '%Y-%m-%d %H:%M:%S'),
                    'returntime': '' if alarm.get('returntime', '') == '' else datetime.datetime.strftime(alarm.get('returntime'), '%Y-%m-%d %H:%M:%S'),
                    'dispatchRecord': '',
                    'dispatch_ID': alarm.get('dispatch_ID', None),
                    'dispatch_name': dispatch_name,
                    'tools': {
                        'check': str(alarm['_id']), 'manual': str(alarm['_id']), 'archived': str(alarm['_id'])
                    },
                    'losing_kwh': alarm.get("losing_kwh", 0)
                }
                alarm_data.append(_dict)
            except Exception as e:
                print(exception_detail(e))
                continue
        return successful_request({'data': alarm_data, 'total_page': total_page, 'current_page': page, 'total_count': alarm_total})
application_common.add_url_rule('/alarm_get', view_func=AlarmGet.as_view('alarm_get'))
#-------------------------------------------------------------------------------
class AlarmGetEvent(AlarmGet):
    def __init__(self):
        super().__init__(alarm_collection="event")
application_common.add_url_rule('/alarm_get_event', view_func=AlarmGetEvent.as_view('alarm_get_event'))
#-------------------------------------------------------------------------------
#使用位置 警報 /alertOverview
@application_common.route('/alarm_tools', methods=['POST'])
def alarm_tools():
    user, db = check_user()
    if db == None:
        return logout()
    request_dict = request.json
    #print(request_dict)
    mode = request_dict.get('mode', None)
    ID = request_dict.get('ID', None)
    try:
        if mode == 'check':
            db.alarm.update_one({'_id': ObjectId(ID)}, {'$set':{'checktime': datetime.datetime.now()}})
        elif mode == 'manual_return':
            db.alarm.update_one({'_id': ObjectId(ID)}, {'$set':{'return_state': 1, 'returntime': datetime.datetime.now()}})
        elif mode == 'archived':
            db.alarm.update_one({'_id': ObjectId(ID)}, {'$set':{'show': 2}})
        else:
            return bad_request(400, 'No such mode')
    except Exception as e:
        return bad_request(500, exception_detail(e))
    return successful_request()
#-------------------------------------------------------------------------------
#使用位置 圖表顯示 電站管理 /stationlist
@application_common.route('/history_data_list', methods=['POST'])
def history_data_list():
    user,db = check_user()
    if(db == None):
        return logout() 
    find_user = find_user_from_current_user()
    user_c=list(db.users.find({"user_id" : find_user}))[0]
    request_dict = request.json
    try:
        history_ID = request_dict['history_ID']
        ObjectId(history_ID)
        datacollection = request_dict['datacollection']
        datatype = request_dict['datatype']
    except Exception as e:
        return bad_request(400, 'Bad Request. ID or datacollection or datatype error.')
    #如果時間沒給的話 就抓當日的
    try:
        datepicker1 = request_dict['datepicker1']
    except:
        datepicker1 = datetime.datetime.strftime(datetime.datetime.today(), '%Y-%m-%d')
    try:
        datepicker2 = request_dict['datepicker2']
    except:
        datepicker2 = datetime.datetime.strftime(datetime.datetime.today(), '%Y-%m-%d')
    try:
        date = datetime.datetime.strptime(datepicker1,"%Y-%m-%d")
        date_start = datetime.datetime.strptime(datepicker1,"%Y-%m-%d")
        date_end = datetime.datetime.strptime(datepicker2,"%Y-%m-%d")
    except:
        return bad_request(400, 'Date error. shuold be %Y-%m-%d')
    date_range = request_dict.get('date_range', 0)
    if isinstance(date_range, int) == False:
        return bad_request(400, 'Bad Request. date_range should be int')

    name_list = [] # Use in ProtectiveRelay
    
    if(datacollection=='pv_plant'):
        interval = 60
        coll=db['plant']
        capacity_data = list(coll.find({'_id':ObjectId(history_ID)},{'_id':0}))
        try:
            pv_name=capacity_data[0]['name']
        except:
            pv_name=1
        try:
            capacity=capacity_data[0]['capacity']
        except:
            capacity=1
        if(datatype=='kwh'):
            x_axis = t.fix_x_xis_date(date_start,date_end,date_range)
            y_axis = t.bar_one_cal_col(db, history_ID, 'meter_cal', 'kwh', date_start, date_end, date_range)
            _min,_max,_avg,_total = t.math_index(y_axis)
        elif(datatype=='PR'):
            x_axis = t.fix_x_xis_date(date_start,date_end,date_range)
            y_axis = t.bar_one_cal_col(db, history_ID, 'pr_cal',
                user_c.get('parameter', {}).get('pr', 'pr'),
                date_start, date_end, date_range)
            _min,_max,_avg,_total = t.math_index(y_axis)
            #_avg   = t.bar_one_PR_total(db,'PR',history_ID,capacity,'kwh',1,'IRRh',date_start,date_end,date_range) #20210330_暫時註解
        elif(datatype=='PSH'):
            x_axis = t.fix_x_xis_date(date_start,date_end,date_range)
            y_axis = t.bar_one_cal_col(db, c.plant_group_ID_find_sun_ID(db, history_ID, 'pv_plant'), 
            'irrh_cal', 'irrh', date_start, date_end, date_range)
            _min,_max,_avg,_total = t.math_index(y_axis)
        elif(datatype=='p'):
            interval = 60
            try:
                main_sun_list = list(db.equipment.find({'PV':pv_name, "main_sun" : 1}))
                main_sun_ID=str(main_sun_list[0]['_id'])
            except Exception as e:
                main_sun_ID=''
            find = [
                {'ID':history_ID,'collection':'pv_plant','datatype':datatype,'interval':60},
                {'ID':main_sun_ID,'collection':'sensor','datatype':'value','interval':60}
            ]
            x_axis = t.fix_x_xis_date(date_start,date_end,0)
            y_axis = t.day_multi_line(db,find,date_start,date_end)
            _min,_max,_avg,_total = t.math_index(y_axis,2)
        else:
            x_axis = t.fix_x_xis_date(date_start,date_end,0)
            y_axis = t.dayline_one(db,datacollection,history_ID,datatype,date_start,date_end,interval)
            _min,_max,_avg,_total = t.math_index(y_axis)
    elif(datacollection=='pv_lgroup'or  datacollection=='pv_group'or datacollection=='pv_meter'):
        interval = 60
        equipment_data = db.equipment.find_one({"_id" : ObjectId(history_ID)},{'_id':0},sort=[( '_id', pymongo.DESCENDING )])
        try:
            PV=equipment_data['PV']
        except:
            PV=''  
        try:
            COM=equipment_data['COMport']
        except:
            COM=''
        if COM=='PV':
            pv_data= db.plant.find_one({'name':PV},{'_id':1}) 
            history_ID=str(pv_data['_id'])
            datacollection='pv_plant'
            coll=db['plant']
            capacity_data = list(coll.find({'_id':ObjectId(history_ID)},{'_id':0}))
            try:
                pv_name=capacity_data[0]['name']
            except:
                pv_name=1
            try:
                capacity=capacity_data[0]['capacity']
            except:
                capacity=1
            if(datatype=='kwh'):
                x_axis = t.fix_x_xis_date(date_start,date_end,date_range)
                y_axis = t.bar_one_cal_col(db, history_ID, 'meter_cal', 'kwh', date_start, date_end, date_range)
                _min,_max,_avg,_total = t.math_index(y_axis)
            elif(datatype=='PR'):
                x_axis = t.fix_x_xis_date(date_start,date_end,date_range)
                y_axis = t.bar_one_cal_col(db, history_ID, 'pr_cal', 
                user_c.get('parameter', {}).get('pr', 'pr'), 
                date_start, date_end, date_range)
                _min,_max,_avg,_total = t.math_index(y_axis)
                #_avg   = t.bar_one_PR_total(db,'PR',history_ID,capacity,'kwh',1,'IRRh',date_start,date_end,date_range)
            elif(datatype=='PSH'):
                x_axis = t.fix_x_xis_date(date_start,date_end,date_range)
                y_axis = t.bar_one_cal_col(db, c.plant_group_ID_find_sun_ID(db, history_ID, datacollection), 'irrh_cal',
                'irrh', date_start, date_end, date_range)
                _min,_max,_avg,_total = t.math_index(y_axis)
            elif(datatype=='p'):
                interval = 60
                try:
                    main_sun_list = list(db.equipment.find({'PV':pv_name, "main_sun" : 1}))
                    main_sun_ID=str(main_sun_list[0]['_id'])
                except Exception as e:
                    main_sun_ID=''
                find = [
                    {'ID':history_ID,'collection':'pv_plant','datatype':datatype,'interval':60},
                    {'ID':main_sun_ID,'collection':'sensor','datatype':'value','interval':60}
                ]
                x_axis = t.fix_x_xis_date(date_start,date_end,0)
                y_axis = t.day_multi_line(db,find,date_start,date_end)
                _min,_max,_avg,_total = t.math_index(y_axis,2)
            else:
                x_axis =  t.fix_x_xis_date(date_start,date_end,0)
                y_axis = t.dayline_one(db,datacollection,history_ID,datatype,date_start,date_end,interval)
                _min,_max,_avg,_total = t.math_index(y_axis)
        else:
            interval = 60
            coll=db['equipment']
            capacity_data = list(coll.find({'_id':ObjectId(history_ID)},{'_id':0}))
            try:
                pv_name=capacity_data[0]['name']
            except:
                pv_name=1
            try:
                capacity=capacity_data[0]['capacity']
            except:
                capacity=1
            try:
                datacollection = capacity_data[0]['collection']    #20210424 By YuShan 電表階層相關
            except:
                datacollection = datacollection
            if(datatype=='kwh'):
                x_axis = t.fix_x_xis_date(date_start,date_end,date_range)
                y_axis = t.bar_one_cal_col(db, history_ID, 'meter_cal', 'kwh', date_start, date_end, date_range)
                _min,_max,_avg,_total = t.math_index(y_axis)
            elif(datatype=='PR'):
                x_axis = t.fix_x_xis_date(date_start,date_end,date_range)
                y_axis = t.bar_one_cal_col(db, history_ID, 'pr_cal',
                user_c.get('parameter', {}).get('pr', 'pr'),
                date_start, date_end, date_range)
                _min,_max,_avg,_total = t.math_index(y_axis)
                #_avg   = t.bar_one_PR_total(db,'PR',history_ID,capacity,'kwh',1,'IRRh',date_start,date_end,date_range)
            elif(datatype=='p'):
                interval = 60
                try:
                    main_sun_ID = ''
                    sun_filter = {'type': 'sun'}
                    if equipment_data.get('type') == 'pv_lgroup':
                        sun_filter['PV'] = equipment_data.get('PV')
                        sun_filter['lgroup'] = equipment_data.get('name')
                    elif equipment_data.get('type') == 'pv_group':
                        sun_filter['PV'] = equipment_data.get('PV')
                        sun_filter['lgroup'] = equipment_data.get('lgroup')
                        sun_filter['group'] = equipment_data.get('name')      
                    else:
                        if 'group' in equipment_data:
                            sun_filter['group'] = equipment_data.get('group')
                        if 'lgroup' in equipment_data:
                            sun_filter['lgroup'] = equipment_data.get('lgroup')
                        sun_filter['PV'] = equipment_data.get('PV')
                    sun_filter['PV'] = {'$all': [sun_filter['PV']]}     
                    for sun_equip in db.equipment.find(sun_filter).sort('name', 1).limit(1):
                        main_sun_ID=str(sun_equip['_id'])
                except Exception as e:
                    main_sun_ID = ''
                find = [
                    {'ID':history_ID,'collection':datacollection,'datatype':datatype,'interval':60},
                    {'ID':main_sun_ID,'collection':'sensor','datatype':'value','interval':60}
                ]
                x_axis = t.fix_x_xis_date(date_start,date_end,0)
                y_axis = t.day_multi_line(db,find,date_start,date_end)
                _min,_max,_avg,_total = t.math_index(y_axis,2)
            else:
                x_axis = t.fix_x_xis_date(date_start,date_end,0)
                y_axis = t.dayline_one(db,datacollection,history_ID,datatype,date_start,date_end,interval)
                _min,_max,_avg,_total = t.math_index(y_axis)
    elif(datacollection=='inverter'):
        interval = 60
        inv_ID = history_ID
        try:
            sun_ID = ""
            for inv in db.equipment.find({'_id': ObjectId(inv_ID)}).limit(1):
                filter = {'PV': {'$all': [inv['PV']]}, 'lgroup': inv['lgroup'], 'group': inv['group'], 'type': 'sun'}
                for sun in db.equipment.find(filter).limit(1):
                    sun_ID = str(sun['_id'])
        except:
            sun_ID = ''
        if(datatype=='kwh'):
            x_axis = t.fix_x_xis_date(date_start,date_end,date_range)
            y_axis = t.bar_one_cal_col(db, history_ID, 'inverter_cal', 'kwh', date_start, date_end, date_range)
            _min,_max,_avg,_total = t.math_index(y_axis)
        elif(datatype=='PR' ):
            coll=db['equipment']
            capacity_data = list(coll.find({'_id':ObjectId(inv_ID)},{'_id':0}))
            try:
                capacity=capacity_data[0]['capacity']
            except:
                capacity=1
            x_axis = t.fix_x_xis_date(date_start,date_end,date_range)
            y_axis = t.bar_one_cal_col(db, history_ID, 'pr_cal',
            user_c.get('parameter', {}).get('pr', 'pr'),
            date_start, date_end, date_range)
            _min,_max,_avg,_total = t.math_index(y_axis)
            #_avg   = t.bar_one_PR_total(db,'PR',inv_ID,capacity,'kwh',1,'IRRh',date_start,date_end,date_range)
        elif(datatype=='RA' ):
            coll=db['equipment']
            capacity_data = list(coll.find({'_id':ObjectId(inv_ID)},{'_id':0}))
            try:
                capacity=capacity_data[0]['capacity']
            except:
                capacity=1
            x_axis = t.fix_x_xis_date(date_start,date_end,date_range)
            y_axis = t.bar_one_cal_col(db, history_ID, 'pr_cal', 'ra', date_start, date_end, date_range)
            _min,_max,_avg,_total = t.math_index(y_axis)
        elif(datatype=='p_cell_total' ):
            interval = 60
            find = [
                {'ID':inv_ID,'collection':'inverter','datatype':datatype,'interval':60},
                {'ID':sun_ID,'collection':'sensor','datatype':'value','interval':60}
            ]
            x_axis = t.fix_x_xis_date(date_start,date_end,0)
            y_axis = t.day_multi_line(db,find,date_start,date_end)
            _min,_max,_avg,_total = t.math_index(y_axis,2)
        elif(datatype=='p_bus_total' ):
            interval = 60
            find = [
                {'ID':inv_ID,'collection':'inverter','datatype':datatype,'interval':60},
                {'ID':sun_ID,'collection':'sensor','datatype':'value','interval':60}
            ]
            x_axis = t.fix_x_xis_date(date_start,date_end,0)
            y_axis = t.day_multi_line(db,find,date_start,date_end)
            _min,_max,_avg,_total = t.math_index(y_axis,2)
        else:
            x_axis = t.fix_x_xis_date(date_start,date_end,0)
            y_axis = t.dayline_one(db,datacollection,inv_ID,datatype,date_start,date_end,interval)
            _min,_max,_avg,_total = t.math_index(y_axis)
    elif(datacollection=='string_meter'):
        interval = 60
        x_axis =  t.fix_x_xis_date(date_start,date_end,0)
        if(datatype!='sa'):
            y_axis = t.dayline_one(db,datacollection,history_ID,datatype,date_start,date_end,interval)
            _min,_max,_avg,_total = t.math_index(y_axis)
        else:
            y_axis = t.dayline_sa(db,history_ID,date_start,date_end,interval=60)
            #y_axis = t.dayline_sa_temp(db,history_ID,date_start,date_end,interval=60)
            _min,_max,_avg,_total = t.math_index(y_axis,16)
    elif(datacollection=='sensor'):
        interval = 60
        x_axis = t.fix_x_xis_date(date_start,date_end,0)
        y_axis = t.dayline_one(db,datacollection,history_ID,datatype,date_start,date_end,interval)
        _min,_max,_avg,_total = t.math_index(y_axis)
    elif(datacollection=='meter'):
        if(datatype!='p_sum' and datatype!='q_sum' and datatype!='s_sum'):
            interval = 60
            x_axis = t.fix_x_xis_date(date_start,date_end,0)
            if(datatype=='v' or datatype=='i' or datatype=='p' or datatype=='q' or datatype=='pf' or datatype=='THDI' or datatype=='v_' or datatype=='THDU'):
                datatype1 = datatype+'1'
                datatype2 = datatype+'2'
                datatype3 = datatype+'3'
                y_axis = t.dayline_three(db,datacollection,history_ID,datatype1,datatype2,datatype3,date)
                _min,_max,_avg,_total = t.math_index(y_axis,3)
            else:
                y_axis = t.dayline_one(db,datacollection,history_ID,datatype,date_start,date_end)
                _min,_max,_avg,_total = t.math_index(y_axis)
        else:
            datacollection = 'meter2'
            x_axis = t.fix_x_xis_date(date_start,date_end,0)
            y_axis = t.dayline_one(db,datacollection,history_ID,datatype,date_start,date_end)
            _min,_max,_avg,_total = t.math_index(y_axis)
    elif(datacollection=='pv_io'):
        interval = 60
        x_axis = t.fix_x_xis_date(date_start,date_end,0)
        _min,_max,_avg,_total = (None, None, None, None)
        if(datatype!='DI'):
            y_axis = t.dayline_one(db,datacollection,history_ID,datatype,date_start,date_end,interval)
        else:
            y_axis = t.dayline_io(db,history_ID,date_start,date_end,interval=60)
    elif(datacollection=='ProtectiveRelay'):
        equip_data = db.equipment.find_one({'_id': ObjectId(history_ID)})
        interval = 60
        x_axis = t.fix_x_xis_date(date_start,date_end,0)
        _min,_max,_avg,_total = (None, None, None, None)
        try:
            IEEE_code = str(request_dict.get('IEEE_code', 'total'))
        except:
            return bad_request(400, 'Bad Request. No IEEE_code')
        y_axis, name_list = t.dayline_protective_relay(db,history_ID, equip_data,IEEE_code,datatype,date_start,date_end,interval=60)

    time_year=datetime.datetime.now().year
    month_len = t.month_len(date_start,date_end)
    day_len = t.day_len(date_start,date_end)
    return successful_request({
        'x_axis': x_axis, 'y_axis': y_axis,  'name_list': name_list,
        'month_len': month_len, 'day_len': day_len, 'min': _min, 'max': _max, 'avg': _avg, 'total': _total, 'time_year': time_year
    })
#-------------------------------------------------------------------------------
#使用位置 圖表顯示 電站管理 /stationlist
@application_common.route('/all_plant_history_data_list', methods=['POST'])
def all_plant_history_data_list():
    user,db = check_user()
    if(db == None):
        return logout() 
    find_user = find_user_from_current_user()

    user_c=list(db.users.find({"user_id" : find_user}))[0]

    request_dict = request.json
    #如果時間沒給的話 就抓當日的
    try:
        datepicker1 = request_dict['datepicker1']
    except:
        datepicker1 = datetime.datetime.strftime(datetime.datetime.today(), '%Y-%m-%d')
    try:
        datepicker2 = request_dict['datepicker2']
    except:
        datepicker2 = datetime.datetime.strftime(datetime.datetime.today(), '%Y-%m-%d')
    try:
        date = datetime.datetime.strptime(datepicker1,"%Y-%m-%d")
        date_start = datetime.datetime.strptime(datepicker1,"%Y-%m-%d")
        date_end = datetime.datetime.strptime(datepicker2,"%Y-%m-%d")
    except:
        return bad_request(400, 'Date error. shuold be %Y-%m-%d')
    date_range = request_dict.get('date_range', 0)
    if isinstance(date_range, int) == False:
        return bad_request(400, 'Bad Request. date_range should be int')
    
    x_axis = t.fix_x_xis_date(date_start,date_end,date_range)
    #y_axis = t.bar_one_cal_col(db, history_ID, 'kwh', date_start, date_end, date_range)
    y_axis = []
    plant_filter = {}
    if user_c['plant'][0] != 'total':
        for i in user_c['plant']:
            if 'name' not in plant_filter:
                plant_filter['name'] = {'$in': []}
            plant_filter['name']['$in'].append(i)
    list1 = []
    for plant in db.plant.find(plant_filter):
        try:
            list1.append(t.bar_one_cal_col(db, str(plant['_id']), 'meter_cal', 'kwh', date_start, date_end, date_range))
        except:
            continue
    if len(list1) > 0:
        y_axis = [0]*len(list1[0])
        for i in list1:
            for cursor, ii in enumerate(i):
                try:
                    if isinstance(ii, (int, float)):
                        y_axis[cursor] += ii
                except: 
                    continue
    _min,_max,_avg,_total = t.math_index(y_axis)

    time_year=datetime.datetime.now().year
    month_len = t.month_len(date_start,date_end)
    day_len = t.day_len(date_start,date_end)
    return successful_request({
        'x_axis': x_axis, 'y_axis': y_axis, 'month_len': month_len, 'day_len': day_len, 'min': _min, 'max': _max, 'avg': _avg, 'total': _total, 'time_year': time_year
    })

#-------------------------------------------------------------------------------
#使用位置 /stationGraphic SLD 單線圖與平面圖
@application_common.route('/getIDListData', methods=['POST'])
def getIDListData():
    user,db = check_user()
    if(db == None):
        return logout()
    find_user = find_user_from_current_user()
    user_c=list(db.users.find({"user_id" : find_user}))[0]
    request_dict = request.json
    plant = request_dict.get('plant', None)
    lgroup = request_dict.get('lgroup', None)
    IDList = request_dict.get('IDList', [])
    #if plant == None or lgroup == None:
    #   return bad_request(400, 'plant or lgroup is empty')
    starttime,endtime = c.date_interval(datetime.date.today())
    data = {"plant_inverterNormalNumber":0,"plant_inverterNumber":0,
    "lgroup_inverterNormalNumber":0,"lgroup_inverterNumber":0,
    "inverterNormalNumber":0,"inverterNumber":0}
    try:
        data["plant_inverterNumber"] = db.equipment.count_documents({"PV": plant,"type":"inv"})
        data["plant_inverterNormalNumber"] = db.equipment.count_documents({"PV": plant, "type":"inv", "state":0})
        data["lgroup_inverterNumber"] = db.equipment.count_documents({"PV": plant, "lgroup": lgroup,"type":"inv"})
        data["lgroup_inverterNormalNumber"] = db.equipment.count_documents({"PV": plant, "lgroup": lgroup, "type":"inv", "state":0})
    except:
        pass
    for ID in IDList:
        if ID != "":
            findData = db.equipment.find_one({"_id":ObjectId(ID)})
            if findData == None:
                findData = db.plant.find_one({"_id":ObjectId(ID)})
            if findData == None:
                findData = db.iot.find_one({"_id":ObjectId(ID)})
            if findData != None:
                if findData.get("type",None) == "PV":
                    data[ID] = c.current_data(db,"pv_plant",ID,{"ID":0,"time":0,"data_state":0}) [0]
                    # print(data[ID],db,col,ID)
                    try:
                        gen_stat = db.pr_cal.find_one({'ID': ID, 'time_interval': 'day', 'time': starttime})
                        if 'parameter' in user_c:
                            data[ID]["PR"] = round(gen_stat.get(user_c['parameter'].get('pr', 'pr'), None), 2)
                        else:
                            data[ID]["PR"] = round(gen_stat.get('pr', None), 2)
                        data[ID]["DMY"] = round(gen_stat.get('dmy', None), 2)
                    except:
                        data[ID]["PR"] = None
                        data[ID]["DMY"] = None
                    try:
                        data[ID]["kwh_today"] = round(
                            db.meter_cal.find_one({'ID': ID, 'time_interval': 'day', 'time': starttime})['kwh']
                        )
                    except:
                        data[ID]["kwh_today"] = None
                    try:
                        data[ID]["irrh"] = round(
                            db.irrh_cal.find_one({'ID': c.plant_group_ID_find_sun_ID(db, ID, findData['collection'])
                            , 'time_interval': 'day', 'time': starttime})['irrh']
                        , 2)
                    except:
                        data[ID]["irrh"] = None

                    try:
                        this_month = datetime.datetime.strftime(starttime, '%Y-%m')
                        this_month = datetime.datetime.strptime(this_month, '%Y-%m')
                        data[ID]["kwh_month"]= round(
                            db.meter_cal.find_one({'ID': ID, 'time_interval': 'month', 'time': this_month})['kwh']
                        )
                    except:
                        data[ID]["kwh_month"] = c.diff_data(db,"pv_plant",ID,'kwh',1)
                    try:
                        this_year = datetime.datetime.strftime(starttime, '%Y')
                        this_year = datetime.datetime.strptime(this_year, '%Y')
                        data[ID]["kwh_year"]= round(
                            db.meter_cal.find_one({'ID': ID, 'time_interval': 'year', 'time': this_year})['kwh']
                        )
                    except:
                        data[ID]["kwh_year"]  = c.diff_data(db,"pv_plant",ID,'kwh',2)
                    
                  
                elif findData.get("type",None) == "pv_lgroup":
                    error = False
                    _ID = ""
                    if(findData["COMport"]=="PV"):
                        col = "pv_plant"
                        try:
                            _ID = str(db.plant.find_one({'name':findData[findData["system"]]},{'_id':1}) ["_id"])
                        except:
                            error = True
                    else:
                        col = "pv_lgroup"
                        _ID = ID
                    if(error==False):
                        data[ID] = c.current_data(db,col,_ID,{"ID":0,"time":0,"data_state":0}) [0]
                        # print(data[ID],db,col,_ID)
                        try:
                            gen_stat = db.pr_cal.find_one({'ID': _ID, 'time_interval': 'day', 'time': starttime})
                            if 'parameter' in user_c:
                                data[ID]["PR"] = round(gen_stat.get(user_c['parameter'].get('pr', 'pr'), None), 2)
                            else:
                                data[ID]["PR"] = gen_stat.get('pr', None)
                            data[ID]["DMY"] = gen_stat.get('dmy', None)
                        except:
                            data[ID]["PR"] = None
                            data[ID]["DMY"] = None
                        try:
                            data[ID]["kwh_today"] = round(
                                db.meter_cal.find_one({'ID': _ID, 'time_interval': 'day', 'time': starttime})['kwh']
                            )
                        except:
                            data[ID]["kwh_today"] = None
                        try:
                            data[ID]["irrh"] = round(
                                db.irrh_cal.find_one({'ID': c.plant_group_ID_find_sun_ID(db, _ID, col)
                                , 'time_interval': 'day', 'time': starttime})['irrh']
                            , 2)
                        except:
                            data[ID]["irrh"] = None
                        try:
                            this_month = datetime.datetime.strftime(starttime, '%Y-%m')
                            this_month = datetime.datetime.strptime(this_month, '%Y-%m')
                            data[ID]["kwh_month"]= round(
                                db.meter_cal.find_one({'ID': _ID, 'time_interval': 'month', 'time': this_month})['kwh']
                            )
                        except:
                            data[ID]["kwh_month"] = c.diff_data(db,"pv_plant",_ID,'kwh',1)
                        try:
                            this_year = datetime.datetime.strftime(starttime, '%Y')
                            this_year = datetime.datetime.strptime(this_year, '%Y')
                            data[ID]["kwh_year"]= round(
                                db.meter_cal.find_one({'ID': _ID, 'time_interval': 'year', 'time': this_year})['kwh']
                            )
                        except:
                            data[ID]["kwh_year"]  = c.diff_data(db,"pv_plant",_ID,'kwh',2)

                    else:
                        data[ID] = {}
                elif findData.get("type",None) == "pv_group":
                    error = False
                    _ID = ""
                    if(findData.get("COMport", None)=="PV"):
                        col = "pv_plant"
                        try:
                            _ID = str(db.plant.find_one({'name':findData[findData["system"]]},{'_id':1}) ["_id"])
                        except:
                            error = True
                    else:
                        col = "pv_group"
                        _ID = ID
            
                    if(error==False):
                        data[ID] = c.current_data(db,col,_ID,{"ID":0,"time":0,"data_state":0}) [0]
                        try:
                            gen_stat = db.pr_cal.find_one({'ID': _ID, 'time_interval': 'day', 'time': starttime})
                            if 'parameter' in user_c:
                                data[ID]["PR"] = round(gen_stat.get(user_c['parameter'].get('pr', 'pr'), None), 2)
                            else:
                                data[ID]["PR"] = gen_stat.get('pr', None)
                            data[ID]["DMY"] = gen_stat.get('dmy', None)
                        except:
                            data[ID]["PR"] = None
                            data[ID]["DMY"] = None
                        try:
                            data[ID]["kwh_today"] = round(
                                db.meter_cal.find_one({'ID': _ID, 'time_interval': 'day', 'time': starttime})['kwh']
                            )
                        except:
                            data[ID]["kwh_today"] = None
                        try:
                            data[ID]["irrh"] = round(
                                db.irrh_cal.find_one({'ID': c.plant_group_ID_find_sun_ID(db, _ID, col)
                                , 'time_interval': 'day', 'time': starttime})['irrh']
                            , 2)
                        except:
                            data[ID]["irrh"] = None
                        try:
                            this_month = datetime.datetime.strftime(starttime, '%Y-%m')
                            this_month = datetime.datetime.strptime(this_month, '%Y-%m')
                            data[ID]["kwh_month"]= round(
                                db.meter_cal.find_one({'ID': _ID, 'time_interval': 'month', 'time': this_month})['kwh']
                            )
                        except:
                            data[ID]["kwh_month"] = c.diff_data(db,"pv_plant", _ID,'kwh',1)
                        try:
                            this_year = datetime.datetime.strftime(starttime, '%Y')
                            this_year = datetime.datetime.strptime(this_year, '%Y')
                            data[ID]["kwh_year"]= round(
                                db.meter_cal.find_one({'ID': _ID, 'time_interval': 'year', 'time': this_year})['kwh']
                            )
                        except:
                            data[ID]["kwh_year"]  = c.diff_data(db,"pv_plant", _ID,'kwh',2)

                    else:
                        data[ID] = {}
                # inverter
                elif findData.get("type",None) == "inv" :
                    data[ID] = c.current_data(db,findData["collection"], ID,{"ID":0,"time":0,"data_state":0}) [0]
                    capacity=float(findData['capacity'])
                    try:
                        #data[ID]['PR'] =  c.diff_data_PR(db,'PR',ID,capacity,'kwh',1,'IRRh',0)
                        gen_stat = db.pr_cal.find_one({'ID': ID, 'time_interval': 'day', 'time': starttime})
                        if 'parameter' in user_c:
                            data[ID]["PR"] = round(gen_stat.get(user_c['parameter'].get('pr', 'pr'), None), 2)
                        else:
                            data[ID]["PR"] = gen_stat.get('pr', None)
                        data[ID]["RA"] = gen_stat.get('ra', None)
                    except:
                        data[ID]['PR'] = '---'
                        data[ID]['RA'] = '---'
                # string_meter
                elif  findData.get("type",None) == "string":
                    data[ID] = c.current_data(db,findData["collection"], ID,{"ID":0,"time":0,"data_state":0}) [0]
                    data[ID]["event"] = []
                    data[ID]["alarm"] = []
                    #PVLOF event move to alarm
                    for i in db.alarm.find({"ID":ID,"checktime":"","time":{"$gte":starttime,"$lt":endtime}},{"_id":0},sort=[( 'time', pymongo.ASCENDING )]):
                        i["start"] = datetime.datetime.strftime(i['time'],"%H:%M:%S")
                        try:
                            i["end"] = datetime.datetime.strftime(i['returntime'],"%H:%M:%S")
                        except:
                            pass
                        i["time"] = datetime.datetime.strftime(i['time'],"%H:%M:%S")
                        data[ID]["event"].append(i)
                    
                    for i in db.alarm.find({"ID":ID, "method": {"$exists": False},"returntime":"","time":{"$gte":starttime,"$lt":endtime}},{"_id":0},sort=[( 'time', pymongo.DESCENDING )]):
                        i["time"] = datetime.datetime.strftime(i['time'],"%H:%M:%S")
                        data[ID]["alarm"].append(i)
                        

                    data[ID].update({"serial_num":findData["serial_num"],"module_num":findData["module_num"]})
                
                elif findData.get("true_type",None) == "iot":
                    data[ID] = {"state":(findData["status"] == "pushed") * 3 ,"type":"iot"}
                #state 
                try:
                    data[ID].update({"state":findData["state"]})
                    if findData.get("type",None) == "inv" :
                        if findData["state"] == 0:
                            data["inverterNormalNumber"] = data["inverterNormalNumber"] + 1 
                        data["inverterNumber"] = data["inverterNumber"] + 1 
                except:
                    pass
                #name
                try:
                    data[ID].update({"name":findData["name"]})
                except:
                    pass
                #type
                try:
                    data[ID].update({"type":findData["type"]})
                except:
                    pass
            else:
                pass
    return successful_request(data)
#-------------------------------------------------------------------------------
#使用位置 /stationGraphic SLD 單線圖與平面圖
@application_common.route('/alarmLatest', methods=['POST'])
def alarmLatest():
    user,db = check_user()
    if(db == None):
        return logout() 
    request_dict = request.json
    plant_name = request_dict.get('PV', '')
    lgroup_name = request_dict.get('lgroup', '')
    group_name = request_dict.get('group', None)
    find_filter = {'PV': plant_name}
    if lgroup_name != '':
        find_filter['lgroup'] = lgroup_name
        if group_name != None:
            find_filter['group'] = group_name
    condiction_list = []
    for ii in db.equipment.find(find_filter):
        if type(ii.get('PV', [])) == list:     #由於參照Sensor 所以只會抓第一個案場
            if ii['PV'][0] == plant_name:
                condiction_list.append({'ID':str(ii['_id']),'show':1})
        else:
            condiction_list.append({'ID':str(ii['_id']),'show':1})
    for i in db.iot.find(find_filter):
        condiction_list.append({'ID':str(i['_id']),'show':1})
    if len(condiction_list)> 0 :
        event = db.alarm.find_one({"returntime":"",'$or':condiction_list},{"_id":0},sort=[( 'time', pymongo.DESCENDING )])
        if event != None:
            event['time'] = datetime.datetime.strftime(event['time'],"%Y-%m-%d %H:%M:%S")
            equip = db.equipment.find_one({"_id":ObjectId(event["ID"])},{"_id":0})
            if equip == None:
                equip = db.iot.find_one({"_id":ObjectId(event["ID"])},{"_id":0})
                equip["type"] = "iot"
        else:
            equip = None
    else:
        event = None
        equip = None
    return successful_request({'event': event, 'equip': equip})
#-------------------------------------------------------------------------------
#使用位置 /stationGraphic SLD 單線圖與平面圖
#從儀器資訊得到group data
@application_common.route('/equip_ID_get_group_data', methods=['POST'])
def equip_ID_get_group_data():
    user,db = check_user()
    if(db == None):
        return logout() 
    request_dict = request.json
    try:
        ID = request_dict['ID']
        ObjectId(ID)
    except:
        return bad_request(400, 'Bad Request. ID error.')
    data = {}
    for equip in db.equipment.find({'_id': ObjectId(ID)}):
        parent_filter = {}
        if 'group' in equip:
            if isinstance(equip['group'], str):
                parent_filter = {'PV': equip.get('PV'), 'lgroup': equip.get('lgroup'), 'name': equip.get('group'), 'type': 'pv_group'}
            elif isinstance(equip['group'], list):
                parent_filter = {'PV': equip.get('PV')[0], 'lgroup': equip.get('lgroup')[0], 'name': equip.get('group')[0], 'type': 'pv_group'}
        elif 'lgroup' in equip:
            if isinstance(equip['lgroup'], str):
                parent_filter = {'PV': equip.get('PV'), 'name': equip.get('lgroup'), 'type': 'pv_lgroup'}
            elif isinstance(equip['lgroup'], list):
                parent_filter = {'PV': equip.get('PV')[0], 'name': equip.get('lgroup')[0], 'type': 'pv_lgroup'}
        for parent in db.equipment.find(parent_filter):
            data['name'] = parent.get('name')
            data['ID'] = str(parent['_id'])
            data['collection'] = parent.get('type')
    return successful_request(data)
#-------------------------------------------------------------------------------
#使用位置 /stationList 電站管理 設備資訊
#取得全部簡略的inverter total須顯示資料
@application_common.route('/pv_inv_total_data', methods=['POST'])
def pv_inv_total_data():
    user,db = check_user()
    if(db == None):
        return logout()
    find_user = find_user_from_current_user()
    user_c=list(db.users.find({"user_id" : find_user}))[0]
    request_dict = request.json
    try:
        pv_inv_total_ID_list = request_dict['ID_list']
        for i in pv_inv_total_ID_list:
            ObjectId(i)   # Just check if id vaild
    except:
        return bad_request(400, 'Bad Request. ID_list error.')
    pv_inv_total_data = c.current_data(db,'inverter',pv_inv_total_ID_list)
    starttime,endtime = c.date_interval(datetime.date.today())
    for i,j in enumerate(pv_inv_total_ID_list):
        equipment_data = db.equipment.find_one({"_id" : ObjectId(pv_inv_total_ID_list[i])},{'_id':0}) 
        pv_inv_total_data[i]['name'] = equipment_data.get('name', '')
        pv_inv_total_data[i]['capacity']  = equipment_data['capacity']
        capacity=float(pv_inv_total_data[i]['capacity'])
        try:
            gen_stat = db.pr_cal.find_one({'ID': pv_inv_total_ID_list[i], 'time_interval': 'day', 'time': starttime})
            try:
                pv_inv_total_data[i]['RA'] =  round(gen_stat['ra'], 2)
            except:
                pv_inv_total_data[i]['RA'] = "---"
            try:
                if 'parameter' in user_c:
                    pv_inv_total_data[i]["PR"] = round(gen_stat.get(user_c['parameter'].get('pr', 'pr'), None), 2)
                else:
                    pv_inv_total_data[i]['PR'] = round(gen_stat['pr'], 2)
            except:
                pv_inv_total_data[i]["PR"] = "---"
            try:
                pv_inv_total_data[i]['kwh_today'] = round(
                    db.inverter_cal.find_one({'ID': pv_inv_total_ID_list[i], 'time_interval': 'day', 'time': starttime})['kwh'], 2
                )
            except:
                pv_inv_total_data[i]['kwh_today'] = "---"
        except Exception as e:
            print(exception_detail(e))
            pv_inv_total_data[i]['RA'] = '---'
            pv_inv_total_data[i]['PR'] = '---'
            pv_inv_total_data[i]['kwh_today'] = '---'
    return successful_request(pv_inv_total_data)
#-------------------------------------------------------------------------------
#使用位置  /stationList 電站管理 設備資訊
#取得inv須顯示資料
@application_common.route('/pv_inv_data', methods=['POST'])
def pv_inv_data():
    user,db = check_user()
    if(db == None):
        return logout() 
    find_user = find_user_from_current_user()
    user_c=list(db.users.find({"user_id" : find_user}))[0]
    request_dict = request.json
    try:
        inv_ID = request_dict['inv_ID']
        ObjectId(inv_ID)    # Just check if id vaild
    except:
        return bad_request(400, 'Bad Request. inv_ID error.')
    starttime,endtime = c.date_interval(datetime.date.today())

    device_data = db.equipment.find({'_id':ObjectId(inv_ID)},{'_id':0})[0]
    inv_data = c.current_data(db,'inverter',inv_ID)[0]
    capacity=float(device_data['capacity'])
    gen_stat = db.pr_cal.find_one({'ID': inv_ID, 'time_interval': 'day', 'time': starttime})
    try:
        inv_data['RA'] =  round(gen_stat['ra'], 2)
    except:
        inv_data['RA'] = '---'
    try:
        if 'parameter' in user_c:
            inv_data['PR'] = round(gen_stat[user_c['parameter'].get('pr', 'pr')], 2)
        else:
            inv_data['PR'] = round(gen_stat['pr'], 2)
    except:
        inv_data['PR'] = '---'
    try:
        inv_data['kwh_today'] = round(
            db.inverter_cal.find_one({'ID': inv_ID, 'time_interval': 'day', 'time': starttime})['kwh'], 2
        )
    except:
        inv_data['kwh_today'] = '---'
    try:
        inv_data['mode'] = c.inverter_mode_translation(inv_data['mode'], device_data.get('Device_model', None))
    except:
        inv_data['mode'] = '---'
    try:   #變流器序號
        inv_data['serial_number'] = device_data['replace_data'][-1]['serial_number']
    except:
        inv_data['serial_number'] = '---'
    try:   #變流器型號
        inv_data['Device_model'] = device_data['Device_model']
    except:
        inv_data['Device_model'] = '---'
    try:
        inv_data['temp_sink']
    except:
        inv_data['temp_sink'] = '---'
    try:
        inv_data['temp_inner']
    except:
        inv_data['temp_inner'] = '---'
    try:
        inv_data['temp_Boost_1']
    except:
        inv_data['temp_Boost_1'] = '---'
    # round
    for key in inv_data:
        try:
            if isinstance(inv_data[key], float):
                inv_data[key] = round(inv_data[key], 2)
        except:
            pass
    state_data = c.current_state(db,inv_ID)[0]
    return successful_request({
        'inv_data': inv_data,
        'state_data': state_data,
        'device_data': device_data,
    })
#-------------------------------------------------------------------------------
#使用位置  /stationList 電站管理 設備資訊
#取得string須顯示資料
@application_common.route('/pv_string_data', methods=['POST'])
def pv_string_data():
    user,db = check_user()
    if(db == None):
        return logout() 
    request_dict = request.json
    try:
        string_ID = request_dict['string_ID']
        ObjectId(string_ID)    # Just check if id vaild
    except:
        return bad_request(400, 'Bad Request. string_ID error.')
    
    first = request_dict.get('first', True)
    string_data = c.current_data(db,'string_meter',string_ID)[0]
    state_data = c.current_state(db,string_ID)[0]
    if(first == True):
        equip_data = c.current_equip(db,string_ID)[0]
    #20210508 string meter未用到則顯示---
    for i in db.equipment.find({'_id': ObjectId(string_ID)}):
        if 'wiring' in i.get('string_data',{}):
            for count in range(len(string_data.get('sa', []))):
                if count < len(i['string_data']['wiring']):
                    if i['string_data']['wiring'][count] == 0:
                        string_data['sa'][count] = None
                        if 'sa'+str(count+1) in string_data:
                            string_data['sa'+str(count+1)] = None
                else:
                    string_data['sa'][count] = None
                    if 'sa'+str(count+1) in string_data:
                            string_data['sa'+str(count+1)] = None
        elif 'serial_num' in i:
            for count in range(len(string_data.get('sa', []))):
                if count >= int(i['serial_num']):
                    string_data['sa'][count] = None
                    if 'sa'+str(count+1) in string_data:
                        string_data['sa'+str(count+1)] = None
    return successful_request({
        'string_data': string_data,
        'state_data': state_data,
        'equip_data': equip_data,
    })
#-------------------------------------------------------------------------------
#使用位置  /stationList 電站管理 設備資訊
#取得sensor須顯示的資料
@application_common.route('/pv_sensor_data', methods=['POST'])
def pv_sensor_data():
    user,db = check_user()
    if(db == None):
        return logout() 
    request_dict = request.json
    try:
        sensor_ID_list = request_dict['ID_list']
        for i in sensor_ID_list:
            ObjectId(i)    # Just check if id vaild
    except:
        return bad_request(400, 'Bad Request. ID_list error.')
    sensor_data = []
    sensor_data = c.current_data(db,'sensor',sensor_ID_list)
    state_data = c.current_state(db,sensor_ID_list)
    return_list = []
    for i in range(len(sensor_data)):
        if sensor_data[i] == {}:
            continue
        sensor_data[i]['state'] = state_data[i].get('state', 0)
        return_list.append(sensor_data[i])
    return successful_request(return_list)
#-------------------------------------------------------------------------------
#使用位置  /stationList 電站管理 設備資訊
#取得meter須顯示的資料
@application_common.route('/pv_meter_data', methods=['POST'])
def pv_meter_data():
    user,db = check_user()
    if(db == None):
        return logout() 
    request_dict = request.json
    try:
        meter_ID_list = request_dict['ID_list']
        for i in meter_ID_list:
            ObjectId(i)    # Just check if id vaild
    except:
        return bad_request(400, 'Bad Request. ID_list error.')
    #20210424_by YuShan pv, lgroup, group電表顯示meter階層
    #去equipment抓取所屬collection
    dict1 = {}
    for i in meter_ID_list:
        for data in db.equipment.find({"_id": ObjectId(i)}):
            col = data.get('collection', None) 
            if col not in dict1:
                dict1[col] = []
            dict1[col].append(i)
        for data in db.plant.find({"_id": ObjectId(i)}):
            col = data.get('collection', None) 
            if col not in dict1:
                dict1[col] = []
            dict1[col].append(i)

    meter_ID_dict = dict1
    meter_data = []
    starttime,endtime = c.date_interval(datetime.date.today())
    
    for col in meter_ID_dict:
        meter_ID_list = meter_ID_dict[col]
        _meter_data = c.current_data(db,col,meter_ID_list)
        for i,j in enumerate(meter_ID_list):
            _meter_data[i]['collection'] = col
            try:
                _meter_data[i]['kwh_today'] = round(
                    db.meter_cal.find_one({'ID': j, 'time_interval': 'day', 'time': starttime})['kwh']
                )
            except:
                _meter_data[i]['kwh_today'] = '---'
            try:
                this_month = datetime.datetime.strftime(starttime, '%Y-%m')
                this_month = datetime.datetime.strptime(this_month, '%Y-%m')
                _meter_data[i]['kwh_month'] = round(
                    db.meter_cal.find_one({'ID': j, 'time_interval': 'month', 'time': this_month})['kwh']
                )
            except:
                _meter_data[i]['kwh_month'] = '---'
            try:
                this_year = datetime.datetime.strftime(starttime, '%Y')
                this_year = datetime.datetime.strptime(this_year, '%Y')
                _meter_data[i]['kwh_year'] = round(
                    db.meter_cal.find_one({'ID': j, 'time_interval': 'year', 'time': this_year})['kwh']
                )
            except:
                _meter_data[i]['kwh_year'] = '---'
            # round
            for key in _meter_data[i]:
                try:
                    if isinstance(_meter_data[i][key], float):
                        _meter_data[i][key] = round(_meter_data[i][key], 2)
                except:
                    pass
        meter_data.extend(_meter_data)

    state_data = c.current_state(db,meter_ID_list)
    return_list = []
    for i in range(len(meter_data)):
        meter_data[i]['state'] = state_data[i].get('state', 0)
        return_list.append(meter_data[i])

    """ plant_name= db.equipment.find_one({'_id':ObjectId(meter_ID_list[0])},{'PV':1}) 
    plant_data= db.plant.find_one({'name':plant_name['PV']}) 
    plant_ID=str(plant_data['_id'])
    plant_name=str(plant_data['meter_name'])
    pv_data = c.current_data(db,'pv_plant',[plant_ID])
    for i,j in enumerate([str(plant_data['_id'])]):
        pv_data[i]['kwh_today'] = c.diff_data(db,'pv_plant',j,'kwh',0)
        pv_data[i]['kwh_month'] = c.diff_data(db,'pv_plant',j,'kwh',1)
        pv_data[i]['kwh_year']  = c.diff_data(db,'pv_plant',j,'kwh',2)
    return successful_request({
        'meter_data': return_list,
        'pv_data': pv_data,
        'plant_ID': plant_ID,
        'plant_name': plant_name
    }) """

    return successful_request({
        'meter_data': return_list,
    })
#-------------------------------------------------------------------------------
#使用位置  /stationList 電站管理 設備資訊
#取得Protective Relay需顯示資料
@application_common.route('/pv_protective_relay_data', methods=['POST'])
def pv_protective_relay_data():
    user,db = check_user()
    if(db == None):
        return logout() 
    request_dict = request.json
    try:
        pr_ID = request_dict['ID']
        ObjectId(pr_ID)    # Just check if id vaild
    except:
        return bad_request(400, 'Bad Request. ID error.')
    try:
        IEEE_code = str(request_dict.get('IEEE_code', 'total'))
    except:
        return bad_request(400, 'Bad Request. No IEEE Code.')
    equip_data = db.equipment.find_one({'_id': ObjectId(pr_ID)})
    if equip_data == None:
        return bad_request(400, 'Bad Request. Target device not found.')

    relay_data = c.current_protective_relay_data(db, 'ProtectiveRelay', pr_ID, IEEE_code, equip_data.get('points', {}))
    for i in relay_data:
        try:
            if 'name' in i:
                i['label'] = equip_data.get('points', {}).get(i['name'], i['LN'])
            else:
                i['label'] = i['LN']
        except:
            continue
    

    return successful_request({
        'relay_data': relay_data,
        'state_data': {'state': equip_data.get('state', None)},
    })
#-------------------------------------------------------------------------------
#使用位置  /stationList 電站管理 設備資訊
#取得 plant lgroup 與 group 下的儀器
class GetEquipmentSelection(views.MethodView):
    def get(self):
        return bad_request(400, 'Bad Request. Please use POST.')
    def post(self):
        user,db = check_user()
        if(db == None):
            return logout() 
        request_dict = request.json
        find_filter = self.establish_find_filter(db, request_dict)
        if find_filter[0] == False:
            return find_filter[1]
        find_filter = find_filter[1]
        data_dict = {
            'inv': self.get_inv_data(db, find_filter),
            'sensor': self.get_sensor_data(db, find_filter),
            'meter': self.get_meter_data(db, find_filter, request_dict.get('collection')),
            'io': self.get_io_data(db, find_filter),
            'ProtectiveRelay': self.get_ProtectiveRelay_data(db, find_filter)
        }
        return successful_request(data_dict)
    def establish_find_filter(self, db, request_dict):
        filter = {}
        try:
            ID = request_dict['ID']
            collection = request_dict['collection']
            if collection == 'pv_plant':
                for plant in db.plant.find({'_id': ObjectId(ID)}):
                    filter = {'PV': plant.get('name', None),'lgroup': {'$exists': False}, 'group': {'$exists': False}}
            elif collection == 'pv_lgroup':
                for lgroup in db.equipment.find({'_id': ObjectId(ID)}):
                    filter = {'PV': lgroup.get('PV', None), 'lgroup': lgroup.get('name', None), 'group': {'$exists': False}}
            elif collection == 'pv_group':
                for group in db.equipment.find({'_id': ObjectId(ID)}):
                    filter = {'PV': group.get('PV', None), 'lgroup': group.get('lgroup', None), 'group': group.get('name', None)}
            else:
                return (False, bad_request(400, 'Bad Request. No such type of group.'))
        except Exception as e:
            return (False, bad_request(400, exception_detail(e)))
        return (True, filter)  
    # inv      
    def get_inv_data(self, db, filter):
        _filter = filter.copy()
        _filter['type'] = 'inv'
        list1 = []
        for i in db.equipment.find(_filter).sort('Device_id',pymongo.ASCENDING):
            string = []
            sm_filter = filter.copy()
            sm_filter['type'] = 'string'
            sm_filter['inv'] = i.get('name', '')
            for sm in db.equipment.find(sm_filter).sort('_id',pymongo.ASCENDING):
                string_list = []
                try:
                    string_num = 0
                    for wiring_i, wiring in enumerate(sm['string_data']['wiring']):
                        if wiring == True:
                            string_num += 1
                            string_list.append('#{}'.format(wiring_i+1))
                except:
                    string_num = sm.get('serial_num', 9)
                    string_list = ['#{}'.format(i) for i in range(1, string_num+1)]
                    

                string.append({
                    'ID': str(sm['_id']),
                    'name': sm.get('name', ''),
                    'state': sm.get('state', 0),
                    'string_num': string_num,
                    'string_list': string_list,
                    'collection': sm.get('collection', 'string_meter'),
                    'Device_model': sm.get('Device_model', '---'),
                    "mac": i.get('mac', '---')
                })
            list1.append({
                'ID': str(i['_id']),
                'name': i.get('name', ''),
                'state': i.get('led_state', 0),
                'string': string,
                'model': i.get('module_model', ''),
                'collection': i.get('collection', 'inverter'),
                'Device_model': i.get('Device_model', '---'),
                "mac": i.get('mac', '---')
            })
        return list1
    # sensor
    def get_sensor_data(self, db, filter):
        _filter = filter.copy()
        _filter['PV'] = {'$all': [filter['PV']]}
        _filter['Device_type'] = 'sensor'
        list1 = []
        for i in db.equipment.find(_filter).sort('_id',pymongo.ASCENDING): 
            list1.append({
                'ID': str(i['_id']),
                'name': i.get('name', ''),
                'state': i.get('state', 0),
                'unit': 'W/㎡' if i.get('type') == 'sun' else '°C' if i.get('type') == 'temp' else 'm/s' if i.get('type') == 'wind' else '',
                'collection': i.get('collection', 'sensor'),
                'Device_model': i.get('Device_model', '---'),
                "mac": i.get('mac', '---')
            })
        return list1
    # meter
    def get_meter_data(self, db, filter, collection):
        _filter = filter.copy()
        _filter['type'] = 'meter'
        list1 = []
        for i in db.equipment.find(_filter):
            list1.append({
                'ID': str(i['_id']),
                'name': i.get('name', ''),
                'state': i.get('state', 0),
                'collection': i.get('collection', 'pv_meter'),
                'Device_model': i.get('Device_model', '---'),
                "mac": i.get('mac', '---')
            })

        #搜尋本身是 pv_lgroup or pv_group
        if collection == 'pv_plant':
            _filter = {'name': _filter['PV'], 'COMport': {'$nin': [None, '', 'none', 'PV']} }
            for i in db.plant.find(_filter).sort('_id',pymongo.ASCENDING):
                list1.append({
                    'ID': str(i['_id']),
                    'name': i.get('name', ''),
                    'state': i.get('state', 0),
                    'collection': i.get('collection', ''),
                    'Device_model': i.get('Device_model', '---'),
                    "mac": i.get('mac', '---')
                })
        else:
            _filter['COMport'] = {'$nin': [None, '', 'none', 'PV']}
            if collection == 'pv_lgroup':
                _filter['name'] = _filter['lgroup']
                _filter['type'] = 'pv_lgroup'
                _filter.pop('lgroup')
            elif collection == 'pv_group':
                _filter['name'] = _filter['group']
                _filter['type'] = 'pv_group'
                _filter.pop('group')

            for i in db.equipment.find(_filter):
                list1.append({
                    'ID': str(i['_id']),
                    'name': i.get('name', ''),
                    'state': i.get('state', 0),
                    'collection': i.get('collection', 'pv_meter'),
                    'Device_model': i.get('Device_model', '---'),
                    "mac": i.get('mac', '---')
                })

        return list1
    # io
    def get_io_data(self, db, filter):
        _filter = filter
        _filter['type'] = 'io'
        list1 = []
        for i in db.equipment.find(_filter).sort('_id',pymongo.ASCENDING):
            list1.append({
                'ID': str(i['_id']),
                'name': i.get('name', ''),
                'state': i.get('state', 0),
                'collection': i.get('collection', 'pv_io'),
                'Device_model': i.get('Device_model', '---'),
                "mac": i.get('mac', '---')
            })
        return list1
    def get_ProtectiveRelay_data(self, db, filter):
        _filter = filter
        _filter['type'] = 'ProtectiveRelay'
        list1 = []
        for i in db.equipment.find(_filter).sort('_id',pymongo.ASCENDING):
            list1.append({
                'ID': str(i['_id']),
                'name': i.get('name', ''),
                'state': i.get('state', 0),
                'collection': i.get('collection', 'ProtectiveRelay'),
                'Device_model': i.get('Device_model', '---'),
                "mac": i.get('mac', '---')
            })
        return list1
application_common.add_url_rule('/get_equip_select', view_func=GetEquipmentSelection.as_view('get_equip_select'))
#-------------------------------------------------------------------------------
#使用位置  /chartOverview 比較圖表
#取得 plant lgroup 與 group 下的儀器
class GetEquipmentSelectionCompare(GetEquipmentSelection):
    def post(self):
        user,db = check_user()
        if(db == None):
            return logout() 
        request_dict = request.json
        try:
            ID = request_dict['ID']
            ObjectId(ID)
            self.ID = ID
        except:
            return bad_request(400, 'Bad Request. ID Error')
        find_filter = self.establish_find_filter(db, request_dict)
        if find_filter[0] == False:
            return find_filter[1]
        find_filter = find_filter[1]
        data_dict = {
            'inv': self.get_inv_data(db, find_filter),
            'sensor': self.get_sensor_data(db, find_filter),
            'meter': self.get_meter_data(db, find_filter, request_dict.get('collection')),
            'io': self.get_io_data(db, find_filter)
        }
        # Get Plant Info
        try:
            ID = request_dict['ID']
            collection = request_dict['collection']
            station_info = { 'ID': ID, 'collection': collection}
            if collection == 'pv_plant':
                for plant in db.plant.find({'_id': ObjectId(ID)}):
                    station_info['station_list'] = [plant.get('name', '')]
            elif collection == 'pv_lgroup':
                for lgroup in db.equipment.find({'_id': ObjectId(ID)}):
                    station_info['station_list'] = [lgroup.get('PV', ''), lgroup.get('name', '')]
            elif collection == 'pv_group':
                for group in db.equipment.find({'_id': ObjectId(ID)}):
                    station_info['station_list'] = [group.get('PV', ''), group.get('lgroup', ''), group.get('name')]
            station_info['station_str'] = '/'.join(station_info['station_list']) + '/'
        except Exception as e:
            return bad_request(400, 'Bad Request. {}'.format(exception_detail(e)))

        return successful_request({
            'equip_data': data_dict,
            'station_data': station_info
        })
    def get_inv_data(self, db, filter):
        list1 = super().get_inv_data(db, filter)
        
        for inv in list1:
            inv['point_info'] = [
                {'name': "直流功率(W)", "about": "p_cell_total"},
                {'name': "交流功率(W)", "about": "p_bus_total"},
            ]
            if "string" in inv:
                for sm in inv["string"]:
                    sm['point_info'] = []
                    for sm_i in sm['string_list']:
                        sm['point_info'].append({
                            'name': sm_i, "about": sm_i
                        })
        return list1
    def get_meter_data(self, db, filter, collection):
        list1 = super().get_meter_data(db, filter, collection)
        if len(list1) == 0:   # 虛擬層 無電表
            for i in db['plant' if collection == 'pv_plant' else 'equipment'].find({'_id': ObjectId(self.ID)}):
                list1.append({
                    'ID': str(i['_id']),
                    'name': i.get('name', ''),
                    'state': i.get('state', 0),
                    'collection': i.get('collection', 'pv_meter'),
                    'Device_model': i.get('Device_model', '---'),
                    "mac": i.get('mac', '---')
                })
        for meter in list1:
            meter['point_info'] = [
                {'name': "功率", "about": "p"},
            ]
        return list1
    
application_common.add_url_rule('/get_equip_select_compare', view_func=GetEquipmentSelectionCompare.as_view('get_equip_select_compare'))
#-------------------------------------------------------------------------------
#使用位置  /chartOverview 比較圖表
#取得 比較圖表我的最愛
class CompareGroupTool(views.MethodView):
    def get(self):
        user,db = check_user()
        if(db == None):
            return logout() 
        find_user = find_user_from_current_user()
        user_c=list(db.users.find({"user_id" : find_user}))[0]
        group_list = []
        station_search = {}
        for group in db.compare_group.find({'user_id': str(user_c['_id']), 'show': 1}):
            equip_list = group.get('equip_list', []) 
            for equip in equip_list:
                if '{}_{}'.format(equip['ID'], equip['about']) not in station_search:
                    station_search['{}_{}'.format(equip['ID'], equip['about'])]= self.equip_get_station_str(db, equip['ID'], equip['type'], equip['about'], equip.get('parentID'))
                equip['label'] = station_search['{}_{}'.format(equip['ID'], equip['about'])]
                equip['isActive'] = False
            group_list.append({
                '_id': str(group['_id']),
                'name': group['name'],
                'equip_data': group.get('equip_list', []) 
            })
        return successful_request({
            'group_data': group_list
        })
    def post(self):
        user,db = check_user()
        if(db == None):
            return logout() 
        request_dict = request.json
        find_user = find_user_from_current_user()
        user_c=list(db.users.find({"user_id" : find_user}))[0]
        try:
            name = request_dict['name']
            equip_data = request_dict['equip_data']
        except Exception as e:
            return bad_request(400, 'Bad Request. {}'.format(exception_detail(e)))
        db.compare_group.update_one({'name': name, 'user_id': str(user_c['_id']), 'show': 1}, {
            '$set': {'equip_list': equip_data}
        }, upsert=True)
        return successful_request()
    def delete(self):
        user,db = check_user()
        if(db == None):
            return logout() 
        try:
            group_ID = request.args['ID']
            ObjectId(group_ID)
        except:
            return bad_request(400, 'Bad Request. ID Error')
        db.compare_group.update_one({'_id': ObjectId(group_ID)}, {'$set': {'show': 0}})
        return successful_request()
    def equip_get_station_str(self, db, _id, equip_type, about, parentID=None):
        station_str = ''
        plant_data = db.plant.find_one({'_id': ObjectId(_id)})
        if plant_data != None:
            station_str = '{}'.format(plant_data.get('name'), plant_data.get('name'))
        equip_data = db.equipment.find_one({'_id': ObjectId(_id)})
        if equip_data != None and equip_type != 'sensor':
            if 'group' in equip_data:
                station_str = '{}/{}/{}/{}'.format(equip_data.get('PV'), equip_data.get('lgroup'), equip_data.get('group'), equip_data.get('name'))
            elif 'lgroup' in equip_data:
                station_str = '{}/{}/{}'.format(equip_data.get('PV'), equip_data.get('lgroup'), equip_data.get('name'))
            elif 'PV' in equip_data:
                station_str = '{}/{}'.format(equip_data.get('PV'), equip_data.get('name'))
        else:
            for group in db.equipment.find({'_id': ObjectId(parentID)}):
                station_str = '{}/{}/{}/{}'.format(group.get('PV'), group.get('lgroup'), group.get('name'), equip_data.get('name'))
        point_ref = db.compare_group.find_one({'reference': True})
        try:
            if equip_type in ['inv', 'meter']:
                station_str += '/{}'.format(point_ref[equip_type].get(about, about))
            else:
                pass
        except:
            station_str += '/{}'.format(about)

        return station_str
application_common.add_url_rule('/compare_group_tool', view_func=CompareGroupTool.as_view('compare_group_tool'))
#-------------------------------------------------------------------------------
@application_common.route('/get_compare_data', methods=['POST'])
def get_compare_data():
    user,db = check_user()
    if(db == None):
        return logout()
    request_dict = request.json
    
    #如果時間沒給的話 就抓當日的
    try:
        datepicker1 = request_dict['datepicker1']
    except:
        datepicker1 = datetime.datetime.strftime(datetime.datetime.today(), '%Y-%m-%d')
    try:
        datepicker2 = request_dict['datepicker2']
    except:
        datepicker2 = datetime.datetime.strftime(datetime.datetime.today(), '%Y-%m-%d')
    try:
        date = datetime.datetime.strptime(datepicker1,"%Y-%m-%d")
        date_start = datetime.datetime.strptime(datepicker1,"%Y-%m-%d")
        date_end = datetime.datetime.strptime(datepicker2,"%Y-%m-%d")
    except:
        return bad_request(400, 'Date error. shuold be %Y-%m-%d')
    
    equip_list = request_dict.get('equip_list', [])
    return_dict = {}
    axisdict = {}
    #format
    # strlist _id, type, detail(if inv and meter)
    try:
        for id_type in equip_list:
            equip_id = id_type.split('_', 1)[0]
            equip = db.plant.find_one({'_id': ObjectId(equip_id)})
            if equip == None:
                equip = db.equipment.find_one({'_id': ObjectId(equip_id)})
            if equip == None:
                continue
            x_list = []
            y_list = []
            #取得儀器名稱
            equip_name = ""
            legendgroup = ""
            try:
                equip_name = equip.get('name', '')
                if 'PV' in equip:
                    if type(equip.get('PV', "")) == str:
                        legendgroup = equip.get('PV', "")
                    elif type(equip.get('PV', "")) == list:
                        legendgroup = equip['PV'][0]
                    legendgroup += "/"
                    if 'lgroup' in equip:
                        if type(equip.get('lgroup', "")) == str:
                            legendgroup += equip.get('lgroup', "")
                        elif type(equip.get('lgroup', "")) == list:
                            legendgroup += equip['lgroup'][0]
                        legendgroup += "/"
                        if 'group' in equip:
                            if type(equip.get('group', "")) == str:
                                legendgroup += equip.get('group', "")
                            elif type(equip.get('group', "")) == list:
                                legendgroup += equip['group'][0]
                            legendgroup += "/"
                    equip_name = legendgroup + equip_name
                if equip.get('type') == "string": #串電流
                    equip_name += ('#'+str(id_type.split('_', 1)[1][2:]))
            except:
                print('error')
            my_unit = ''
            meter_unit = {'電壓':'(V)', '電流': '(A)', '功率': '(kW)', '電能': '(kWh)', '虛功': '(kVAR)', '功因': '', '頻率': '(f)', '需量': '(kW)'}
            sensor_name = {'sun': '照度(W/m²)', 'temp': '溫度(℃)', 'wind': '風速', 'string': '電流(A)'}
            #取得項目名稱
            if equip.get('type') in ['inv', 'meter', 'PV', 'pv_lgroup', 'pv_group']: 
                try:
                    equip['type'] = 'meter' if equip['type'] in ['PV', 'pv_lgroup', 'pv_group'] else equip['type'] 
                    for i in db.compare_group.find({'reference': True}):
                        for meter_key in meter_unit:
                            if meter_key in i.get(equip.get('type'), {}).get(id_type.split('_', 1)[1], ''):
                                equip_name += ('-'+ i.get(equip.get('type'), {}).get(id_type.split('_', 1)[1], '')+ meter_unit.get(meter_key))
                                my_unit = meter_key+ meter_unit.get(meter_key)
                        #y title name
                        if my_unit not in axisdict:
                            axisdict[my_unit] = len(axisdict) + 1
                except:
                    print('error1')
            else:
                equip_name += ('-' + sensor_name.get(equip.get('type'), ''))
                my_unit = sensor_name.get(equip.get('type'), '')
                if my_unit not in axisdict:
                    axisdict[my_unit] = len(axisdict) + 1
            x_axis = t.fix_x_xis_date(date_start, date_end,0)
            y_axis = t.dayline_one(db,equip.get('collection'),str(equip['_id']), id_type.split('_', 1)[1], date_start, date_end, 60)
            return_dict[id_type] = {'x': x_axis, 'y': y_axis, 'name': equip_name, 'legendgroup': legendgroup,
                'yaxis': axisdict.get(my_unit, 0), 'hoverlabel': {'namelength' :-1}} 

    except Exception as e:
        return bad_request(400, 'Bad Request. {}'.format(exception_detail(e)))
    return successful_request({
        'return_dict': return_dict,
        'axisdict': axisdict
    })
#-------------------------------------------------------------------------------
#使用位置 /stationGraphic 串電流熱圖
#取得 string_pvlof 熱圖
@application_common.route('/pv_heatmap_string_pvlof_plot', methods=['POST'])
def pv_heatmap_string_pvlof_plot():
    user,db = check_user()
    if(db == None):
        return logout() 
    request_dict = request.json
    try:
        pv_name = request_dict['pv_name']
        pv_lgroup_group = request_dict.get('pv_lgroup_group', None)
        pv_lgroup = request_dict['pv_lgroup']
        pv_group = request_dict['pv_group']
    except Exception as e:
        # Use ID to find group
        try:
            ID = request_dict['ID']
            pv_name = ''
            pv_lgroup_group = ''
            for equip in db.equipment.find({'_id': ObjectId(ID)}):
                pv_name = equip['PV']
                pv_lgroup_group = '{}_{}'.format(equip['lgroup'], equip['name'])
        except Exception as ee:
            print(ee)
            return bad_request(400, 'Bad Request. No name and ID Error')

    try:
        datepicker = request_dict['datepicker']
        date = datetime.datetime.strptime(datepicker, "%Y-%m-%d")
    except Exception as e:
        return bad_request(400, 'Bad Request. date error')

    if(pv_lgroup_group != None):
        pv_lgroup_group = pv_lgroup_group.split("_")
        pv_lgroup = pv_lgroup_group[0]
        pv_group = pv_lgroup_group[1]

    print({"PV" : pv_name, "lgroup" : pv_lgroup, "group" : pv_group, "type":"string"})
    x_axis = t.fix_x_xis(interval=5*60)
    y_axis = []
    z_axis = []
    stringList = []
    for i in db.equipment.find({"PV" : pv_name, "lgroup" : pv_lgroup, "group" : pv_group, "type":"string"}):
        _y_axis = []
        i["_id"] = str(i["_id"])
        stringList.append(i)
        for j in range(int(i["serial_num"])):
            _y_axis.append(i["name"]+"#"+str(j+1))
        _z_axis = t.dayline_heatmap_string_pvlof(db,i["_id"],i["serial_num"],date,date)
        y_axis.append(_y_axis)
        z_axis.append(_z_axis)
    return successful_request({
        'x_axis': x_axis,
        'y_axis': y_axis,
        'z_axis': z_axis,
        'stringList': stringList
    })
#----------------------------------------------------------------------------------------------------
#mongoDB 搜尋檢易API
@application_common.route('/db_find', methods=['POST'])
def db_find():
    user,db = check_user()
    if(db == None):
        return logout() 
    request_dict = request.json
    try:
        collection = request_dict['collection']
        if collection not in ['equipment', 'plant', 'alarm', 'alarm_cause']:
            return bad_request('Bad Request. collection not allowed.')
    except:
        return bad_request(400, 'Bad Request. collection is required.')
    filter = request_dict.get('filter', {})
    if not isinstance(filter, dict):
        return bad_request(400, 'Bad request. filter must be object or dict.')
    time_format = request_dict.get('time_format', '%Y-%m-%d')

    # filter processing
    if '_id' in filter:
        if isinstance(filter['_id'], str):
            filter['_id'] = ObjectId(filter['_id'])
        elif isinstance(filter['_id'], list):
            for i, _id in enumerate(filter['_id']):
                filter['_id'][i] = ObjectId(_id)
            filter['_id'] = {
                '$in': filter['_id']
            }

    return_list = [] 
    for i in db[collection].find(filter):
        for key in i:
            if key == '_id':
                i[key] = str(i[key]) 
            elif isinstance(i[key], datetime.date):
                try:
                    i[key] = datetime.datetime.strftime(i[key], time_format)
                except Exception as e:
                    return bad_request(400, 'Bad Request. Due to {}'.format(e))
        return_list.append(i)  
    return successful_request({
        'data': return_list
    })
#-------------------------------------------------------------------------------
#使用位置 DMY比較圖表
@application_common.route('/ID_get_dmy_irrh_interval', methods=['POST'])
def ID_get_dmy_irrh_interval():
    user,db = check_user()
    if(db == None):
        return logout() 
    request_dict = request.json
    try:
        in_ID_list = request_dict['ID_list']
        if not isinstance(in_ID_list, list):
            return bad_request(400, 'Bad Request typeof ID_list must be array.')
    except Exception as e:
        return bad_request(400, 'Bad Request. No ID_list')
    try:
        datatype_list = request_dict.get('datatype', ['dmy'])
    except:
        pass    

    # ID get info
    ID_list = []
    name_list = []
    collection_list = []
    sensor_dict = {}
    for ID in in_ID_list:
        #print(ID)
        plant_data = db.plant.find_one({'_id': ObjectId(ID)})
        if plant_data != None:
            # Find Its sun sensor
            sun_sensor = db.equipment.find_one({'PV': {'$all': [plant_data['name']]},'type': 'sun', 'main_sun': 1})
            if sun_sensor != None:
                plant_data['sun'] = str(sun_sensor['_id'])
                if str(sun_sensor['_id']) not in sensor_dict:
                    sensor_dict[str(sun_sensor['_id'])] = sun_sensor
            else:
                plant_data['sun'] = None

            ID_list.append(ID)
            name_list.append(plant_data)
            collection_list.append(plant_data.get('collection','pv_plant'))

            continue
        equip_data = db.equipment.find_one({'_id': ObjectId(ID)})
        if equip_data != None:
            # Find Its sun sensor
            # pv_lgroup
            if equip_data['type'] == 'pv_lgroup':
                sun_filter = {'PV': {'$all': [equip_data['PV']]}, 'lgroup': {'$all': [equip_data['name']]},'type': 'sun', 'main_sun': 1}
            # pv_group
            elif equip_data['type'] == 'pv_group':
                sun_filter = {'PV': {'$all': [equip_data['PV']]}, 'lgroup': {'$all': [equip_data['lgroup']]},
                'group': {'$all': [equip_data['name']]},'type': 'sun', 'main_sun': 1}
            # else
            else:
                sun_filter = {'PV': {'$all': [equip_data['PV']]}, 'lgroup': {'$all': [equip_data['lgroup']]},
                'group': {'$all': [equip_data['group']]},'type': 'sun', 'main_sun': 1}
            sun_sensor = db.equipment.find_one(sun_filter)
            if sun_sensor != None:
                equip_data['sun'] = str(sun_sensor['_id'])
                if str(sun_sensor['_id']) not in sensor_dict:
                    sensor_dict[str(sun_sensor['_id'])] = sun_sensor
            else:
                equip_data['sun'] = None


            ID_list.append(ID)
            name_list.append(equip_data)
            collection_list.append(equip_data.get('collection','pv_lgroup'))        

    #print(sensor_dict)

    # daterange 
    try:
        date_range = {1: 'hour', 2: 'day', 3: 'day', 4: 'day'}[request_dict.get('date_range',1)]
        date_format = {1: '%Y-%m-%d %H', 2: '%Y-%m-%d', 3: '%Y-%m', 4: '%Y'}[request_dict.get('date_range',1)]
    except Exception as e:
        return bad_request(400, 'Bad Request. date_range error. It must between 1-4. {}'.format(e))

    # get time
    try:
        starttime, endtime = datetime.datetime.strptime(request_dict['datepicker1'],'%Y-%m-%d'), datetime.datetime.strptime(request_dict['datepicker2'],'%Y-%m-%d')
        x_axis = t.fix_x_xis_date(starttime,endtime,request_dict.get('date_range',1))
        starttime_range = starttime # Trans to datetime object
        endtime_range = endtime + datetime.timedelta(days=1) # Trans to datetime object
    except Exception as e:
        return bad_request(400, 'Bad request. Date Error. {}'.format(e))
    #print(starttime, endtime)

    #print(x_axis)
    #print(collection_list)

    remote_error_msg = ""

    # dmy
    if 'dmy' in datatype_list:
        dmy_list = []
        for i, ID in enumerate(ID_list):
         
            # which collection base on type
            if collection_list[i] == 'inverter':
                col = 'inverter_cal'
            else:
                col = 'meter_cal'

            y_axis = t.bar_one_cal_col(db, ID, col, 'kwh', starttime, endtime, request_dict.get('date_range',1))
            for _i, _y in enumerate(y_axis):
                try:
                    y_axis[_i] = _y / name_list[i]['capacity']
                except:
                    pass
                
            #print(y_axis)
            dmy_list.append({
                'x_axis': x_axis,
                'y_axis': y_axis,
                'ID': ID,
                'collection': collection_list[i],
                'name': name_list[i]['name'],
                'label': name_list[i]['name'] if collection_list[i] == 'pv_plant' 
                    else '{}/{}'.format(name_list[i]['PV'],name_list[i]['name']) if collection_list[i] == 'pv_lgroup'
                    else '{}/{}/{}'.format(name_list[i]['PV'], name_list[i]['lgroup'], name_list[i]['name']) if collection_list[i] == 'pv_group'
                    else '{}/{}/{}/{}'.format(name_list[i]['PV'],name_list[i]['lgroup'],name_list[i]['group'],name_list[i]['name'])
            })
            #print(dmy_list)


        sun_list = []
        # get sun data
        for sun_ID in sensor_dict:
            y_axis_dict = {}
            for _x in x_axis:
                y_axis_dict[_x] = None
            
            try:
                for data in db.irrh_cal.find({'ID': sun_ID, 'time_interval': date_range, 'time': {'$gte': starttime_range, '$lt': endtime_range}}).sort('time', 1):
                    #print(data)
                    try:
                        if y_axis_dict[datetime.datetime.strftime(data['time'], date_format)] == None:
                            y_axis_dict[datetime.datetime.strftime(data['time'], date_format)] = 0
                        y_axis_dict[datetime.datetime.strftime(data['time'], date_format)] += round(data['irrh'], 3)
                    except:
                        pass
            except:
                pass

            y_axis = list(y_axis_dict.values())

            sun_list.append({
                'ID': sun_ID,
                'name': sensor_dict[sun_ID].get('name', ''),
                'x_axis': x_axis,
                'y_axis': y_axis,
                'label': '{}/{}/{}/{}'.format(
                    sensor_dict[sun_ID].get('PV', [''])[0] if isinstance(sensor_dict[sun_ID].get('PV', ['']), list) else sensor_dict[sun_ID]['PV'],
                    sensor_dict[sun_ID].get('lgroup', [''])[0] if isinstance(sensor_dict[sun_ID].get('lgroup', ['']), list) else sensor_dict[sun_ID]['lgroup'],
                    sensor_dict[sun_ID].get('group', [''])[0] if isinstance(sensor_dict[sun_ID].get('group', ['']), list) else sensor_dict[sun_ID]['group'],
                    sensor_dict[sun_ID].get('name', '')
                )
            })

        # 取得盛齊電站發電量 只限date_range >= 2 aka 月搜尋區間以上
        # 茂鴻用
        # For MaoHong billionwatts
        remote_error_msg += t.dmy_irrh_interval_billionwatts(db, dmy_list, sun_list, x_axis, starttime, endtime, request_dict.get('date_range', 1))
        
    # dmy
    if 'pr' in datatype_list:
        pr_list = []
        for i, ID in enumerate(ID_list):
            y_axis = t.bar_one_cal_col(db, ID, 'pr_cal', 'pr', starttime, endtime, request_dict.get('date_range',1))
                
            #print(y_axis)
            pr_list.append({
                'x_axis': x_axis,
                'y_axis': y_axis,
                'ID': ID,
                'collection': collection_list[i],
                'name': name_list[i]['name'],
                'label': name_list[i]['name'] if collection_list[i] == 'pv_plant' 
                    else '{}/{}'.format(name_list[i]['PV'],name_list[i]['name']) if collection_list[i] == 'pv_lgroup'
                    else '{}/{}/{}'.format(name_list[i]['PV'], name_list[i]['lgroup'], name_list[i]['name']) if collection_list[i] == 'pv_group'
                    else '{}/{}/{}/{}'.format(name_list[i]['PV'],name_list[i]['lgroup'],name_list[i]['group'],name_list[i]['name'])
            })
            #print(dmy_list)

        
    return_dict = {
        'remote_error_msg': remote_error_msg
    }
    if 'dmy' in datatype_list:
        return_dict.update({'dmy_list': dmy_list, 'sun_list': sun_list})
    if 'pr' in datatype_list:
        return_dict.update({'pr_list': pr_list})
    
    return successful_request(return_dict)
#-------------------------------------------------------------------------------
#使用位置 DMY比較圖表
# 取得所有group ID /chartOverview
@application_common.route('/get_all_group_ID', methods=['POST'])
def get_all_group_ID():
    user, db = check_user()
    if db == None:
        return logout()
    find_user = find_user_from_current_user()
    user_c=list(db.users.find({"user_id" : find_user}))[0]
    try:
        plant_filter = {}
        if user_c['plant'][0] != 'total':
            for i in user_c['plant']:
                if 'name' not in plant_filter:
                    plant_filter['name'] = {'$in': []}
                plant_filter['name']['$in'].append(i)
        group_data = {'capacity_list': [], 'ID_list': []}
        for plant in db.plant.find(plant_filter):
            for equipment in db.equipment.find({"PV":plant.get("name", ""), "type": "pv_group"}):
                if equipment:
                    group_data['ID_list'].append(str(equipment['_id']))
                    group_data['capacity_list'].append(equipment.get('capacity', 0))
        
    except Exception as e:
        print(exception_detail(e))
        return bad_request('Error Due to {}'.format(e))
    return successful_request(group_data)
#-------------------------------------------------------------------------------
#使用位置 taipower /setting 使用者設定
@application_common.route('/get_all_users_data')
def get_all_users_data():
    user, db = check_user()
    if db == None:
        return logout()
    find_user = find_user_from_current_user()
    user_c=list(db.users.find({"user_id" : find_user}))[0]
    if user_c.get('level', 1) < 3:
        return bad_request(400, 'Bad Request. You can not access.')
    is_superuser = user_c.get('superuser', False)
    user_list = []
    current_page = int(request.args.get('page', 1))
    find_filter = {} if is_superuser else {'superuser': {'$exists': False}}
    per_page = int(request.args.get('per_page', 10))
    if not is_superuser:
        find_filter['pageType'] = user_c.get('pageType')
    for user in db.users.find(find_filter).skip((current_page-1)*per_page).limit(per_page):
        user_list.append({
            '_id': str(user['_id']),
            'username': user.get('username', ''),
            'level': user.get('level', 1),
            'user_data': user.get('user_data', None),
            'plant': user.get('plant'),
        })
        if is_superuser:  # Will not expose to non superuser
            user_list[-1]['pageType'] = user.get('pageType')
            try:
                user_list[-1]['last_access_time'] = datetime.datetime.strftime(user['last_access_time'], '%Y-%m-%d %H:%M:%S')
            except:
                user_list[-1]['last_access_time'] = '---'
            user_list[-1]['last_access_ip'] = user.get('last_access_ip', '---')
            # password
            user_list[-1]['pwd'] = jwt.encode({"password": None if user.get('superuser', False) == True else user.get('password')}, "superuser_edit&view_only_password", algorithm="HS256")
            # That user's mobile_device
            mobile_list = []
            for mobile in db.mobile_device.find({'ID': str(user['_id']), 'show': 1}):
                mobile['_id'] = str(mobile['_id'])
                try:
                    mobile['last_login_time'] = datetime.datetime.strftime(mobile['last_login_time'], '%Y-%m-%d %H:%M:%S')
                except:
                    mobile['last_login_time'] = '---'
                mobile_list.append(mobile)
            user_list[-1]['mobile_list'] = mobile_list
    return successful_request({
        'users_list': user_list,
        'current_page': current_page,
        'total_page': math.ceil(db.users.count_documents(find_filter)/per_page)
    })
#-------------------------------------------------------------------------------
#使用位置 taipower /setting 使用者設定
#新增使用者
@application_common.route('/create_new_user', methods=['POST'])
def create_new_user():
    user, db = check_user()
    if db == None:
        return logout()
    find_user = find_user_from_current_user()
    user_c=list(db.users.find({"user_id" : find_user}))[0]

    request_dict = request.json
    try:
        user_dict = {
            'username': request_dict['username'],
            'password': request_dict['password'],
            'level': request_dict['level'],
            'user_id': '{}_{}'.format(user[0], request_dict['username']),
            'page': 1,
            'plant': request_dict['plant'],
            'user_data': request_dict.get('user_data', {
                'name': '', 'tel': '', 'dispatch_price_per_hour': 0
            }),
            'pageType': user_c.get('pageType', 'pv'),
            'main_photo': '#',
            'parameter': {
                'pr': 'pr'
            },
            'widget': {}
        }
        if db.users.count_documents({'user_id': user_dict['user_id']}) > 0:
            return bad_request(400, 'Bad Request. User Exists')
        db.users.insert_one(user_dict)
    except Exception as e:
        return bad_request(400, 'Bad Request. {}'.format(e))
    return successful_request()
#-------------------------------------------------------------------------------
#使用位置 taipower /setting 使用者設定
#檢查使用者名稱是否重複
@application_common.route('/username_duplicate_check', methods=['POST'])
def username_duplicate_check():
    user, db = check_user()
    if db == None:
        return logout()
    request_dict = request.json
    try:
        username = request_dict['username']
    except:
        return bad_request(400, 'Bad Request. username')
    if db.users.count_documents({'username': username}) > 0:
        return successful_request(False)
    else:
        return successful_request(True)
#-------------------------------------------------------------------------------
#使用位置 taipower /setting 使用者設定
#更新使用者資料
@application_common.route('/update_user_data', methods=['POST'])
def update_user_data():
    user, db = check_user()
    if db == None:
        return logout()
    request_dict = request.json
    find_user = find_user_from_current_user()
    user_c=list(db.users.find({"user_id" : find_user}))[0]
    if user_c.get('level', 1) < 3:
        return bad_request(400, 'Bad Request. You can not access.')
    try:
        ID = request_dict['ID']
        mode = request_dict['mode']
        if mode == 'user_data':
            user_data = request_dict['data']
            if user_c.get('superuser', False) != True:  # Protection Guard
                user_data.pop('pageType', None)
            else:
                db.users.update_one({'_id': ObjectId(ID)}, {'$set': {'pageType': user_data.get('pageType', user_c.get('pageType'))}})
                user_data.pop('pageType', None)
            db.users.update_one({'_id': ObjectId(ID)}, {'$set': {'user_data': user_data}})
        elif mode == 'plant':
            user_data = request_dict['data']
            if len(user_data) == 0 or not isinstance(user_data, list):
                return bad_request(400, 'Bad Request. plant error')
            db.users.update_one({'_id': ObjectId(ID)}, {'$set': {'plant': user_data}})
        elif mode == 'level':
            user_data = request_dict['data']
            if not isinstance(user_data, int) or user_data < 1 or user_data > 3:
                return bad_request(400, 'Bad Request. level error')
            db.users.update_one({'_id': ObjectId(ID)}, {'$set': {'level': user_data}})
        elif mode == 'pwd':
            if user_c.get('superuser', False) != True:  # Protection Guard
                return bad_request(400, 'Bad Request.')
            pwd = request_dict['data']
            db.users.update_one({'_id': ObjectId(ID)}, {'$set': {'password': pwd}})
    except Exception as e:
        return bad_request(400, 'Bad Request. {}'.format(exception_detail(e)))
    return successful_request()
#-------------------------------------------------------------------------------
@application_common.route('/delete_user', methods=['POST'])
def delete_user():
    user, db = check_user()
    if db == None:
        return logout()
    try:
        ID = request.json['ID']
        ObjectId(ID)
    except:
        return bad_request('Bad Request. ID error')
    user_data = db.users.find_one({'_id': ObjectId(ID)})
    if user_data == None:
        return bad_request('Bad Request. user not found')
    db.users_delete.insert_one(user_data)
    db.users.delete_one({'_id': ObjectId(ID)})
    return successful_request()
#-------------------------------------------------------------------------------
#使用位置 taipower /setting 推播通知
#取得 更新 手機裝置資訊
class MyMobileDevice(views.MethodView):
    def get(self):
        user, db = check_user()
        if db == None:
            return logout()
        find_user = find_user_from_current_user()
        user_c=list(db.users.find({"user_id" : find_user}))[0]
        current_page = int(request.args.get('current_page', 1))
        table_data = []
        for mobile in db.mobile_device.find({'ID': str(user_c['_id']), 'show': 1}).skip((current_page-1)*10).limit(10):
            try:
                table_data.append({
                    '_id': str(mobile['_id']),
                    'name': mobile.get('name', ''),
                    'platform': {'ios': 'iOS', 'android': 'Android'}.get(mobile.get('platform', ''), mobile.get('platform', '')),
                    'model': mobile.get('model', ''),
                    'last_login_time': '---' if mobile.get('last_login_time', None) == None \
                        else datetime.datetime.strftime(mobile.get('last_login_time', None), '%Y-%m-%d %H:%M:%S'),
                    'enable_push_notify': mobile.get('enable_push_notify', True)
                })
            except:
                pass
        return successful_request({
            'mobile_list': table_data,
            'total_page': math.ceil(db.mobile_device.count_documents({'ID': str(user_c['_id']), 'show': 1})/10),
            'current_page': current_page
        })
    def post(self):
        user, db = check_user()
        if db == None:
            return logout()
        request_dict = request.json
        find_user = find_user_from_current_user()
        user_c=list(db.users.find({"user_id" : find_user}))[0]
        try:
            ID = request_dict['ID']
            for mobile in db.mobile_device.find({'_id': ObjectId(ID)}):
                if mobile.get('ID') != str(user_c['_id']):
                    continue
                mode = request_dict['mode']
                if mode == 'update_enable_push_notify':
                    data = request_dict['data']
                    if isinstance(data, bool):
                        db.mobile_device.update_one({'_id': mobile['_id']}, {
                            '$set': {'enable_push_notify': data}
                        })
                elif mode == 'delete_device':
                    db.mobile_device.update_one({'_id': mobile['_id']}, {
                        '$set': {'show': 0, 'auth_token': None}
                    })
        except Exception as e:
            return bad_request(400, 'Bad Request. {}'.format(exception_detail(e)))
        return successful_request()
application_common.add_url_rule('/my_mobile_device', view_func=MyMobileDevice.as_view('my_mobile_device'))
#-------------------------------------------------------------------------------
#使用位置 taipower footer for app store and play store badge
#取得 商店連結
@application_common.route('/get_app_store_url')
def get_app_store_url():
    user, db = check_user()
    if db == None:
        return logout()
    data = db.parameter_setting.find_one({'method': 'app_store_url'})
    ios = "#"
    android = "#"
    if data != None:
        ios = data.get('data', {}).get('ios', '#')
        android = data.get('data', {}).get('android', '#')
    return successful_request({
        'ios': ios,
        'android': android
    })
#-------------------------------------------------------------------------------
#使用位置 taipower /setting 更改案場或儀器名稱
@application_common.route('/change_equip_name', methods=['POST'])
def change_equip_name():
    user, db = check_user()
    if db == None:
        return logout()
    request_dict = request.json
    try:
        ID = request_dict['ID']
        rename = request_dict['rename']
    except:
        return bad_request(400, 'Bad Request. ID or rename error')
    find_user = find_user_from_current_user()
    user_c=list(db.users.find({"user_id" : find_user}))[0]
    if user_c.get('level', 1) < 3:
        return bad_request(400, 'Bad Request. Level')
    
    plant = db.plant.find_one({'_id': ObjectId(ID)})
    equip = db.equipment.find_one({'_id': ObjectId(ID)})
    origin_name = None
    if plant != None:
        origin_name = plant.get('name', None)
        result = c.equipment_name_change(db, {
            'name': plant.get('name', None),
            'collection': 'pv_plant',
            'rename': rename
        })
    elif equip != None:
        origin_name = equip.get('name', None)
        equip['rename'] = rename
        result = c.equipment_name_change(db, equip) 
    try:
        if result[0] == True:
            db.setting_log.insert_one({
                'method': 'equip_rename',
                'ID': ID,
                'origin_name': origin_name,
                'rename': rename,
                'time': datetime.datetime.now(),
                'exec_by': str(user_c['_id'])
            })
            return successful_request({'status': True})
        else:
            return successful_request({'status': False, 'result': result[1]})
    except:
        return bad_request(400, 'Bad Request. Err')
#-------------------------------------------------------------------------------
#使用位置 /reportOverview 99M taipower 電費單
class ElectricBillUploadFile(views.MethodView):
    def __init__(self) -> None:
        super().__init__()
        self.allow_file_type = set(['pdf', 'PDF'])
        self.dirPath = current_app.config['UPLOAD_FOLDER']
    def post(self):
        user,db = check_user()
        if db == None:
            return logout()
        self.db = db
        self.file_dict = request.files
        self.request_dict = request.form
        print(request.form)
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
                print(file)
                result.append(self.save_file(file, dirPath))
        return successful_request({
            'result': result
        })
    def create_store_path(self):
        try:
            ID = self.request_dict['ID']
            ObjectId(ID)
            self.ID = ID
            lgroup_data = self.db.equipment.find_one({'_id': ObjectId(ID)})
            PV_ID = str(self.db.plant.find_one({'name': lgroup_data['PV']})['_id'])
        except:
            return False, 'ID error'
        try:
            if 'month' in self.request_dict:
                # For month only
                month = self.request_dict['month']
                month = datetime.datetime.strptime(month, '%Y-%m-%d')
                month = datetime.datetime.strftime(month, '%Y-%m')
                self.date_type = 'month'
                self.month = month
                self.dirPath += '/uploadBill/{}/{}/{}/'.format(PV_ID, ID, month)
            else:
                # For date interval. New MaoHong
                starttime = self.request_dict['starttime']
                endtime = self.request_dict['endtime']
                starttime = datetime.datetime.strptime(starttime, '%Y-%m-%d')
                endtime = datetime.datetime.strptime(endtime, '%Y-%m-%d')
                self.date_type = 'date_interval'
                self.starttime = starttime
                self.endtime = endtime
                self.dirPath += '/uploadBill/{}/{}/'.format(PV_ID, ID)
        except:
            return False, 'Date Error'
        return True, self.dirPath
    def save_file(self, file, dirPath):
        """ filename = secure_filename(file.filename)
        file.save(dirPath+'/'+file.filename) """
        if self.date_type == 'month':
            file.save(dirPath+'bill.pdf')
            # To image
            images = pdf2image.convert_from_path(dirPath + "/bill.pdf")
            for index,image in enumerate(images):
                image.save(dirPath + "/bill." + str(index)+".png")
            self.db.TaipowerBillandPvsyst.update_one({
                'time': datetime.datetime.strptime(self.month, '%Y-%m'),
                'ID': self.ID,
                'method': 'BillPdf',
            }, {'$set': {
                    'show': 1, 'filename': 'bill.pdf', 'image_length': len(images),
                    'upload_time': datetime.datetime.now(),
                }}, upsert=True)
        else: # date_interval
            find_filter = { 'ID': self.ID, 'method': 'BillPdf'}
            find_filter.update({'$or':  [ {'starttime': { '$lte': self.starttime}, 'endtime': { '$gte': self.starttime, '$lte': self.endtime}}, { 'endtime': { '$gte': self.endtime}, 'starttime': { '$gte': self.starttime, '$lte': self.endtime}}, { 'starttime': { '$lte': self.starttime}, 'endtime': { '$gte': self.endtime}}]})
            origin_bill = self.db.TaipowerBillandPvsyst.find_one(find_filter)
            if origin_bill == None:
                update_id = self.db.TaipowerBillandPvsyst.update_one({
                    'time': self.starttime,
                    'starttime': self.starttime,
                    'endtime': self.endtime,
                    'ID': self.ID,
                    'method': 'BillPdf',
                }, {'$set': {
                        'upload_time': datetime.datetime.now(),
                    }}, upsert=True).upserted_id
            else:
                update_id = origin_bill['_id']
            dirPath += '{}/'.format(update_id)
            try:
                os.makedirs(dirPath)
                print("Directory " , dirPath ,  " Created ")    
            except FileExistsError:
                print("Directory " , dirPath ,  " already exists")
            file.save(dirPath+'bill.pdf')
            # To image
            images = pdf2image.convert_from_path(dirPath + "/bill.pdf")
            for index,image in enumerate(images):
                image.save(dirPath + "/bill." + str(index)+".png")
            update_id = self.db.TaipowerBillandPvsyst.update_one({'_id': update_id}, {
                '$set': {
                    'show': 1, 'filename': 'bill.pdf', 'image_length': len(images),
                    'time': self.starttime,
                    'starttime': self.starttime,
                    'endtime': self.endtime,
                    'upload_time': datetime.datetime.now(),
                }
            })
        return True
    def allowed_file(self, filename):
        return '.' in filename and \
            filename.rsplit('.', 1)[1] in self.allow_file_type
application_common.add_url_rule('/electricBill_upload_file', view_func=ElectricBillUploadFile.as_view('electricBill_upload_file'))
#-------------------------------------------------------------------------------
# 使用位置 99M /reportOverview 報表總覽 電費單
@application_common.route('/get_electricBill_data', methods=['POST'])
def get_electricBill_data():
    user,db = check_user()
    if db == None:
        return logout()
    request_dict = request.json
    try:
        ID = request_dict['ID']
        ObjectId(ID)
    except:
        return bad_request(400, 'Bad Request. ID Error.')
    find_filter = {'ID': ID, 'show': 1}
    try:
        if 'month' in request_dict:
                # For month only
                month = request_dict['month']
                month = datetime.datetime.strptime(month, '%Y-%m-%d')
                month = datetime.datetime.strftime(month, '%Y-%m')
                date_type = 'month'
                find_filter.update({'time': month})
        else: # For New MaoHong
            # For date interval. New MaoHong
            starttime = request_dict['starttime']
            endtime = request_dict['endtime']
            starttime = datetime.datetime.strptime(starttime, '%Y-%m-%d')
            endtime = datetime.datetime.strptime(endtime, '%Y-%m-%d')
            date_type = 'date_interval'
            find_filter.update({'$or':  [ {'starttime': { '$lte': starttime}, 'endtime': { '$gte': starttime, '$lte': endtime}}, { 'endtime': { '$gte': endtime}, 'starttime': { '$gte': starttime, '$lte': endtime}}, { 'starttime': { '$lte': starttime}, 'endtime': { '$gte': endtime}}]})
    except:
        return bad_request(400, 'Bad Request. Date Error.')
    bill_pdf = {}
    tableData = []
    tableData_method = []
    print(find_filter)
    for record in db.TaipowerBillandPvsyst.find(find_filter):
        if record.get('method') == 'BillPdf':
            lgroup_data = {}
            for lgroup in db.equipment.find({'_id': ObjectId(ID)}):
                lgroup['ID'] = str(lgroup['_id'])
                lgroup['PV'] = lgroup.get('PV')
                for plant in db.plant.find({'name': lgroup.get('PV')}):
                    lgroup['PV_ID'] = str(plant['_id'])
                lgroup_data = lgroup
            try:
                bill_pdf = {
                    'PV': lgroup_data.get('PV', ''),
                    'PV_ID': lgroup_data.get('PV_ID', ''),
                    'lgroup': lgroup_data.get('name', ''),
                    'ID': lgroup_data['ID'],
                    '_id': str(record['_id']),
                    'filename': record['filename'],
                    'time': datetime.datetime.strftime(record['time'], '%Y-%m'),
                    'upload_time': datetime.datetime.strftime(record['upload_time'], '%Y-%m-%d %H:%M'),
                }
                if date_type == 'date_interval':
                    bill_pdf.update({
                        'starttime': datetime.datetime.strftime(record['starttime'], '%Y-%m-%d'),
                        'endtime': datetime.datetime.strftime(record['endtime'], '%Y-%m-%d')
                    })
            except Exception as e:
                print(e)
                pass
        else:
            record['_id'] = str(record['_id'])
            tableData_method.append(record.get('method'))
            tableData.append(record)
    # add tableData if no record ['TaipowerBill', 'Pvsyst']
    for _method in ['TaipowerBill']:
        if _method not in tableData_method:
            tableData.append({
                'method': _method,
                'ID': ID,
                'kwh': None,
                'fee': None,
                'dmy': None,
                'readonly': False,
            })
    
    return successful_request({
        'bill_pdf': bill_pdf,
        'tableData': tableData
    })
#-------------------------------------------------------------------------------
# 使用位置 99M /reportOverview 報表總覽 電費單
@application_common.route('/update_electricBill_tableData', methods=['POST'])
def update_electricBill_tableData():
    user,db = check_user()
    if db == None:
        return logout()
    find_user = find_user_from_current_user()
    user_c=list(db.users.find({"user_id" : find_user}))[0]

    request_dict = request.json
    try:
        ID = request_dict['ID']
        ObjectId(ID)
    except:
        return bad_request(400, 'Bad Request. ID Error.')
    find_filter = {'ID': ID, 'show': 1}
    try:
        if 'month' in request_dict:
            # For month only
            month = request_dict['month']
            month = datetime.datetime.strptime(month, '%Y-%m-%d')
            month = datetime.datetime.strftime(month, '%Y-%m')
            date_type = 'month'
            find_filter.update({'time': month})
        else: # For New MaoHong
            # For date interval. New MaoHong
            starttime = request_dict['starttime']
            endtime = request_dict['endtime']
            starttime = datetime.datetime.strptime(starttime, '%Y-%m-%d')
            endtime = datetime.datetime.strptime(endtime, '%Y-%m-%d')
            date_type = 'date_interval'
            find_filter.update({'$or':  [ {'starttime': { '$lte': starttime}, 'endtime': { '$gte': starttime, '$lte': endtime}}, { 'endtime': { '$gte': endtime}, 'starttime': { '$gte': starttime, '$lte': endtime}}, { 'starttime': { '$lte': starttime}, 'endtime': { '$gte': endtime}}]})
    except:
        return bad_request(400, 'Bad Request. Date Error.')
    tableData = request_dict.get('tableData', [])

    allowMethod = ['TaipowerBill', 'Pvsyst']
    for _data in tableData:
        try:
            if _data['method'] not in allowMethod:
                continue
            find_filter['method'] = _data['method']
            origin_data = db.TaipowerBillandPvsyst.find_one(find_filter)
            if origin_data != None and origin_data['readonly'] == True:
                continue

            # Type Check
            for point in ['kwh', 'dmy', 'fee']:
                try:
                    if isinstance(_data[point], (int, float)):
                        continue 
                    elif '.' in _data[point]:
                        _data[point] = float(_data[point])
                    else:
                        _data[point] = int(_data[point])
                except:
                    _data[point] = None
                
            if date_type == 'month':
                db.TaipowerBillandPvsyst.update_one({'ID': ID, 'time': month, 'method': _data['method'], 'show': 1, 'readonly': False}, {
                    '$set': {
                        'kwh': _data.get('kwh'),
                        'dmy': _data.get('dmy'),
                        'fee': _data.get('fee'),
                        'updatetime': datetime.datetime.now(),
                        'last_update_user': str(user_c['_id'])
                    }
                }, upsert=True)
            else:
                if origin_data == None: # New
                    db.TaipowerBillandPvsyst.insert_one({
                        'ID': ID, 'time': starttime, 'method': _data['method'], 'show': 1, 'readonly': False,
                        'starttime': starttime, 'endtime': endtime,
                        'kwh': _data.get('kwh'),
                        'dmy': _data.get('dmy'),
                        'fee': _data.get('fee'),
                        'updatetime': datetime.datetime.now(),
                        'last_update_user': str(user_c['_id'])
                    })
                else:
                    db.TaipowerBillandPvsyst.update_one({'_id': origin_data['_id']}, {
                        '$set': {
                            'starttime': starttime, 'endtime': endtime,
                            'kwh': _data.get('kwh'),
                            'dmy': _data.get('dmy'),
                            'fee': _data.get('fee'),
                            'updatetime': datetime.datetime.now(),
                            'last_update_user': str(user_c['_id'])
                        }
                    })
        
        except Exception as e:
            print(e)
            pass

    return successful_request()
#-------------------------------------------------------------------------------
# 使用位置 99M /reportOverview 報表總覽 電費單
@application_common.route('/report_get_electricBill', methods=['POST'])
def report_get_electricBill():
    user,db = check_user()
    if(db == None):
        return logout() 
    find_user = find_user_from_current_user()
    user_c=list(db.users.find({"user_id" : find_user}))[0]
    try:
        plant_filter = {}
        if user_c['plant'][0] != 'total':
            for i in user_c['plant']:
                if 'name' not in plant_filter:
                    plant_filter['name'] = {'$in': []}
                plant_filter['name']['$in'].append(i)
        lgroup_dict = {}
        for plant in db.plant.find(plant_filter):
            for equip in db.equipment.find({"PV":plant.get("name", ""), "type": "pv_lgroup"}):
                equip['PV_ID'] = str(plant['_id'])
                lgroup_dict[str(equip['_id'])] = equip
    except Exception as e:
        print(exception_detail(e))
        return bad_request('Error Due to {}'.format(e))
    request_dict = request.json
    report_filter = {'show': 1, 'method': 'BillPdf'}
    # time filter
    if request_dict.get('time', {}).get('mode', '') == 'single':
        try:
            start_date = datetime.datetime.strptime(request_dict['time']['start_date'], '%Y-%m-%d')
            end_date = start_date + datetime.timedelta(days=1)
            report_filter['time'] = {'$gte': start_date, '$lt': end_date}
        except:
            return bad_request(400, 'Time error')
    elif request_dict.get('time', {}).get('mode', '') == 'interval':
        try:
            start_date = datetime.datetime.strptime(request_dict['time']['start_date'], '%Y-%m-%d')
            end_date = datetime.datetime.strptime(request_dict['time']['end_date'], '%Y-%m-%d')
            report_filter['time'] = {'$gte': start_date, '$lt': end_date+datetime.timedelta(days=1)}
        except:
            return bad_request(400, 'Time error')
    elif request_dict.get('time', {}).get('mode', '') in ['today', 'week', 'month', 'year']:
        today =datetime.datetime.today()
        if request_dict['time']['mode'] in ['today', 'week']:
            start_date = datetime.datetime(year=today.year, month=today.month, day=1)
            end_date = datetime.datetime.now()
        elif request_dict['time']['mode'] == 'year':
            start_date = datetime.datetime(year=today.year, month=1, day=1)
            end_date = datetime.datetime.now()
        report_filter['time'] = {'$gte': start_date, '$lt': end_date}
    # ID_list filter
    try:
        ID_list = request_dict.get('ID_list', [])
        col_list = request_dict.get('col_list', [])
        filter_ID = []
        for i, ID in enumerate(ID_list):
            if col_list[i] == 'pv_plant':
                for plant in db.plant.find({'_id': ObjectId(ID)}):
                    for lgroup in db.equipment.find({'PV': plant.get('name'), 'type': 'pv_lgroup'}):
                        if str(lgroup['_id']) in lgroup_dict:
                            filter_ID.append(str(lgroup['_id']))
            elif col_list[i] == 'pv_group':
                for group in db.equipment.find({'_id': ObjectId(ID)}):
                    for lgroup in db.equipment.find({'PV': group.get('PV'), 'name': group.get('lgroup'), 'type': 'pv_lgroup'}):
                        if str(lgroup['_id']) in lgroup_dict:
                            filter_ID.append(str(lgroup['_id']))
            else:
                if ID in lgroup_dict:
                    filter_ID.append(ID)
        if len(filter_ID) > 0:
            report_filter['ID'] = {'$in': filter_ID}
    except Exception as e:
        print(e)
        pass
    
    return_list = []
    pageType = None
    if 'pageType' in user_c:
        pageType = user_c['pageType']
    current_page =  request_dict.get('page', 1)
    for report in db.TaipowerBillandPvsyst.find(report_filter).skip((current_page - 1)*10).limit(10).sort('time', -1):
        try:
            tableData = db.TaipowerBillandPvsyst.find_one({'ID': report['ID'], 'time': report['time'], 'show': 1,
            'method': 'TaipowerBill'})
            report_data = {
                'PV': lgroup_dict.get(report['ID'], {}).get('PV', ''),
                'PV_ID': lgroup_dict.get(report['ID'], {}).get('PV_ID', ''),
                'lgroup': lgroup_dict.get(report['ID'], {}).get('name', ''),
                'ID': report['ID'],
                '_id': str(report['_id']),
                'filename': report['filename'],
                'time': datetime.datetime.strftime(report['time'], '%Y-%m'),
                'upload_time': datetime.datetime.strftime(report['upload_time'], '%Y-%m-%d %H:%M'),
                'kwh': None if tableData == None else tableData.get('kwh', None),
                'fee': None if tableData == None else tableData.get('fee', None)
            }
            if 'starttime' in report:
                report_data['starttime'] = datetime.datetime.strftime(report['starttime'], '%Y-%m-%d')
                report_data['endtime'] = datetime.datetime.strftime(report['endtime'], '%Y-%m-%d')
            return_list.append(report_data)
        except:
            continue
    return successful_request({
        'data': return_list,
        'total_report': db.TaipowerBillandPvsyst.count_documents(report_filter),
        "total_page": math.ceil(db.TaipowerBillandPvsyst.count_documents(report_filter)/10)
    })
#-------------------------------------------------------------------------------
# 使用位置 99M /reportOverview 報表總覽 電費單
@application_common.route('/delete_electricBill', methods=['POST'])
def delete_electricBill():
    user,db = check_user()
    if(db == None):
        return logout() 
    find_user = find_user_from_current_user()
    user_c=list(db.users.find({"user_id" : find_user}))[0]
    if user_c.get('level', 1) < 3:
        return bad_request(400, 'Bad Request. Level')
    request_dict = request.json
    try:
        ID = request_dict['ID']
        ObjectId(ID)
        find_filter = { 'ID': ID}
    except:
        return bad_request(400, 'Bad Request. ID Error')
    try:
        if 'month' in request_dict:
            # For month only
            month = request_dict['month']
            month = datetime.datetime.strptime(month, '%Y-%m-%d')
            month = datetime.datetime.strftime(month, '%Y-%m')
            date_type = 'month'
            find_filter.update({'time': month})
        else: # For New MaoHong
            # For date interval. New MaoHong
            starttime = request_dict['starttime']
            endtime = request_dict['endtime']
            starttime = datetime.datetime.strptime(starttime, '%Y-%m-%d')
            endtime = datetime.datetime.strptime(endtime, '%Y-%m-%d')
            date_type = 'date_interval'
            find_filter.update({'$or':  [ {'starttime': { '$lte': starttime}, 'endtime': { '$gte': starttime, '$lte': endtime}}, { 'endtime': { '$gte': endtime}, 'starttime': { '$gte': starttime, '$lte': endtime}}, { 'starttime': { '$lte': starttime}, 'endtime': { '$gte': endtime}}]})
    except:
        return bad_request(400, 'Bad Request. Date Error.')

    for record in db.TaipowerBillandPvsyst.find(find_filter):
        db.TaipowerBillandPvsyst.update_one({ '_id': record['_id']}, { '$set': { 'show': 0}})

    return successful_request()
#-------------------------------------------------------------------------------
#警報圓餅圖
@application_common.route('/get_alarm_pie_chart_data', methods=['POST'])
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
                # if alarm["alarm_group"] == "設備" or alarm["alarm_group"] == "軟體":
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
@application_common.route('/get_inverter_temp_power', methods=['POST'])
def get_inverter_temp_power():
    user,db = check_user()
    if(db == None):
        return logout() 
    request_dict = request.json
    today = datetime.datetime.today()
    today = datetime.datetime.strftime(today, '%Y-%m-%d')
    interval = request_dict.get("interval", "day")
    ID = request_dict.get("ID", "")
    collection = request_dict.get("collection", "")
    start_time = request_dict.get("datepicker1", today)
    end_time = request_dict.get("datepicker2", today)
    start_time = datetime.datetime.strptime(start_time, '%Y-%m-%d')
    end_time = datetime.datetime.strptime(end_time, '%Y-%m-%d')
    x_axis = []
    inv_id = []
    name_dict = {}
    name_list = []
    return_dict = {"temp": {}}
    try:
        filter = {"type": "inv"}
        if collection == "pv_plant":
            filter["PV"] = db.plant.find_one({"_id": ObjectId(ID)})["name"]
        elif collection == "pv_lgroup":
            filter["PV"] = db.equipment.find_one({"_id": ObjectId(ID), "type": "pv_lgroup"})["PV"]
            filter["lgroup"] = db.equipment.find_one({"_id": ObjectId(ID), "type": "pv_lgroup"})["name"]
        elif collection == "pv_group":
            filter["PV"] = db.equipment.find_one({"_id": ObjectId(ID), "type": "pv_group"})["PV"]
            filter["lgroup"] = db.equipment.find_one({"_id": ObjectId(ID), "type": "pv_group"})["lgroup"]
            filter["group"] = db.equipment.find_one({"_id": ObjectId(ID), "type": "pv_group"})["name"]
        for equi in db.equipment.find(filter):
            name = equi["PV"] + "-" + equi["lgroup"] + "-" + equi["group"] + "-" + equi["name"]
            name_list.append(name)
            name_dict[str(equi["_id"])] = name
            inv_id.append(str(equi["_id"]))

        date_range = 2
        if interval == "hour":
            date_range = 1
        x_axis = t.fix_x_xis_date(start_time, end_time, date_range)
        axis_30 = t.fix_x_xis_date(start_time, end_time, date_range=0, interval=60*30)
        if interval == "day":
            limit = 48
        else:
            limit = 2
        for id in inv_id:
            counter = 0
            inv_values = []
            temp_values = []
            _temp_values = []
            for time in x_axis:
                inv_value = db.inverter_cal.find_one({
                    "ID": id,
                    "time_interval": interval,
                    "time": datetime.datetime.strptime(time, '%Y-%m-%d') if interval == "day" else datetime.datetime.strptime(time, "%Y-%m-%d %H")
                })
                if inv_value != None:
                    _inv_value = inv_value.get("kwh", None)
                else:
                    inv_value = None
                if _inv_value != None and _inv_value != "":
                    inv_values.append(round(_inv_value, 2))
                else:
                    inv_values.append(None)

            for time_30 in axis_30:
                counter += 1
                temp_value = db.inverter.find_one({
                    "ID": id,
                    "time": datetime.datetime.strptime(time_30, "%Y-%m-%d %H:%M")
                })
                if temp_value != None:
                    _temp_value = temp_value.get("temp_inner", None)
                else:
                    _temp_value = None
                if _temp_value != None and _temp_value != 0 and _temp_value != "":
                    temp_values.append(round(_temp_value, 2))
                if counter == limit:
                    if len(temp_values) > 0:
                        _temp_values.append(sum(temp_values)/len(temp_values))
                    else:
                        _temp_values.append(None)
                    counter = 0
                    temp_values = []
            return_dict["temp"][name_dict[id]] = _temp_values
            return_dict[name_dict[id]] = inv_values
        return successful_request({
            "data": {
                "name_list": name_list,
                "data": return_dict,
                "x_axis": x_axis
            }
        })
    except Exception as e:
        print(exception_detail(e))
        return bad_request(400, "Bad Request. {}".format(e))
#-------------------------------------------------------------------------------
# 使用位置 /reportOverview 報表總覽 旬報表搜尋
@application_common.route('/report_get_Tday', methods=['POST'])
def report_get_Tday():
    user,db = check_user()
    if(db == None):
        return logout() 
    find_user = find_user_from_current_user()
    
    user_c=list(db.users.find({"user_id" : find_user}))[0]
    request_dict = request.json
    ID_list = request_dict.get('ID_list', [])
    col_list = request_dict.get('col_list', [])
    report_filter = {'show': 1}
    # time filter
    if request_dict.get('time', {}).get('mode', '') == 'single':
        try:
            start_date = datetime.datetime.strptime(request_dict['time']['start_date'], '%Y-%m-%d')
            end_date = start_date + datetime.timedelta(days=1)
            report_filter['time'] = {'$gte': start_date, '$lt': end_date}
        except:
            return bad_request(400, 'Time error')
    elif request_dict.get('time', {}).get('mode', '') == 'interval':
        try:
            start_date = datetime.datetime.strptime(request_dict['time']['start_date'], '%Y-%m-%d')
            end_date = datetime.datetime.strptime(request_dict['time']['end_date'], '%Y-%m-%d')
            report_filter['time'] = {'$gte': start_date, '$lt': end_date+datetime.timedelta(days=1)}
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
        report_filter['time'] = {'$gte': start_date, '$lt': end_date}
    # plant filter
    if isinstance(ID_list, list) and len(ID_list) > 0:
        pass
    # Search All
    else:
        plant_filter = {}
        if user_c['plant'][0] != 'total':
            for i in user_c['plant']:
                if 'name' not in plant_filter:
                    plant_filter['name'] = {'$in': []}
                plant_filter['name']['$in'].append(i)
        for plant in db.plant.find(plant_filter):
            ID_list.append(str(plant['_id']))
            col_list.append(str(plant['collection']))
    #print(ID_list, col_list)
    report_filter['ID'] = []
    plant_trans = {}
    try:
        for i, col in enumerate(col_list):
            if col == 'pv_plant':
                for plant in db.plant.find({'_id': ObjectId(ID_list[i])}):
                    excel_level = plant.get('Taipower_excel_level', 'lgroup')
                    if excel_level == 'PV' or excel_level == 'plant':
                        report_filter['ID'].append(str(plant['_id']))
                        plant_trans[str(plant['_id'])] = plant.get('name')
                    elif excel_level == 'lgroup' or excel_level == 'pv_lgroup':
                        for lgroup in db.equipment.find({'PV': plant.get('name'), 'type': 'pv_lgroup'}):
                            report_filter['ID'].append(str(lgroup['_id']))
                            plant_trans[str(lgroup['_id'])] = '{}\\{}'.format(plant.get('name'), lgroup.get('name'))
                    else: # group
                        for group in db.equipment.find({'PV': plant.get('name'), 'type': 'pv_group'}):
                            report_filter['ID'].append(str(group['_id']))
                            plant_trans[str(group['_id'])] = '{}\\{}\\{}'.format(plant.get('name'), group.get('lgroup'), group.get('name'))
            elif col == 'pv_lgroup':
                for lgroup in db.equipment.find({'_id': ObjectId(ID_list[i])}):
                    for plant in db.plant.find({'name': lgroup.get('PV', None)}):
                        excel_level = plant.get('Taipower_excel_level', 'lgroup')
                        if excel_level == 'PV' or excel_level == 'plant':
                            report_filter['ID'].append(str(plant['_id']))
                            plant_trans[str(plant['_id'])] = plant.get('name')
                        elif excel_level == 'lgroup' or excel_level == 'pv_lgroup':
                            report_filter['ID'].append(str(lgroup['_id']))
                            plant_trans[str(lgroup['_id'])] = '{}\\{}'.format(lgroup.get('PV'), lgroup.get('name'))
                        else:
                            for group in db.equipment.find({'PV': group.get('PV'), 'lgroup': lgroup.get('name'), 'type': 'pv_group'}):
                                report_filter['ID'].append(str(group['_id']))
                                plant_trans[str(group['_id'])] = '{}\\{}\\{}'.format(group.get('PV'), group.get('lgroup'), group.get('name'))

            else:  #group
                for group in db.equipment.find({'_id': ObjectId(ID_list[i])}):
                    for plant in db.plant.find({'name': group.get('PV', None)}):
                        excel_level = plant.get('Taipower_excel_level', 'lgroup')
                        if excel_level == 'PV' or excel_level == 'plant' or excel_level == 'pv_plant':
                            report_filter['ID'].append(str(plant['_id']))
                            plant_trans[str(plant['_id'])] = plant.get('name')
                        elif excel_level == 'lgroup' or excel_level == 'pv_lgroup' or excel_level == 'pv_lgroup':
                            for lgroup in db.equipment.find({'PV': group.get('PV'), 'name': group.get('lgroup'), 'type': 'pv_lgroup'}):
                                report_filter['ID'].append(str(lgroup['_id']))
                                plant_trans[str(lgroup['_id'])] = '{}\\{}'.format(lgroup.get('PV'), lgroup.get('name'))
                        else:
                            report_filter['ID'].append(str(group['_id']))
                            plant_trans[str(group['_id'])] = '{}\\{}\\{}'.format(group.get('PV'), group.get('lgroup'), group.get('name'))
    except Exception as e:
        return bad_request('Bad Request. Due to {}'.format(exception_detail(e)))
    report_filter['ID'] = {'$in': report_filter['ID']}
    return_list = []
    pageType = None
    if 'pageType' in user_c:
        pageType = user_c['pageType']
    current_page =  request_dict.get('page', 1)
    for report in db.excel.find(report_filter).skip((current_page - 1)*10).limit(10).sort('time', -1):
        try:
            return_list.append({
                'filename': report['filename'] if pageType in ['pv', None] else '{}/{}'.format(pageType, report['filename']),
                'period': report.get('peroid'),
                'time': datetime.datetime.strftime(report['time'], '%Y-%m-%d'),
                'group': plant_trans[report['ID']],
            })
        except:
            continue
    return successful_request({
        'data': return_list,
        'total_report': db.excel.count_documents(report_filter),
        "total_page": math.ceil(db.excel.count_documents(report_filter)/10)
    })
#-------------------------------------------------------------------------------
# 使用位置 /reportOverview 報表總覽 即時變流器報表製作
@application_common.route('/realtime_inv_excel_generate', methods=['POST'])
def realtime_inv_excel_generate():
    user,db = check_user()
    if(db == None):
        return logout()
    try:
        ID = request.json['ID']
        ObjectId(ID)
        inv_data = db.equipment.find_one({'_id': ObjectId(ID)})
        return r.inv_excel_today(db, ID, inv_data)
    except Exception as e:
        return bad_request(400, 'Bad Request. {}'.format(exception_detail(e)))  
#-------------------------------------------------------------------------------
# 使用位置 /reportOverview 報表總覽 變流器報表搜尋
@application_common.route('/report_get_inverter', methods=['POST'])
def report_get_inverter():
    user,db = check_user()
    if(db == None):
        return logout()
    find_user = find_user_from_current_user()
    
    user_c=list(db.users.find({"user_id" : find_user}))[0]
    request_dict = request.json
    ID_list = request_dict.get('ID_list', [])
    col_list = request_dict.get('col_list', [])
    report_filter = {'show': 1}
    # time filter
    if request_dict.get('time', {}).get('mode', '') == 'single':
        try:
            start_date = datetime.datetime.strptime(request_dict['time']['start_date'], '%Y-%m-%d')
            end_date = start_date + datetime.timedelta(days=1)
            report_filter['time'] = {'$gte': start_date, '$lt': end_date}
        except:
            return bad_request(400, 'Time error')
    elif request_dict.get('time', {}).get('mode', '') == 'interval':
        try:
            start_date = datetime.datetime.strptime(request_dict['time']['start_date'], '%Y-%m-%d')
            end_date = datetime.datetime.strptime(request_dict['time']['end_date'], '%Y-%m-%d')
            report_filter['time'] = {'$gte': start_date, '$lt': end_date+datetime.timedelta(days=1)}
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
        report_filter['time'] = {'$gte': start_date, '$lt': end_date}
    # plant filter
    if isinstance(ID_list, list) and len(ID_list) > 0:
        pass
    # Search All
    else:
        plant_filter = {}
        if user_c['plant'][0] != 'total':
            for i in user_c['plant']:
                if 'name' not in plant_filter:
                    plant_filter['name'] = {'$in': []}
                plant_filter['name']['$in'].append(i)
        for plant in db.plant.find(plant_filter):
            ID_list.append(str(plant['_id']))
            col_list.append(str(plant['collection']))
    #print(ID_list, col_list)
    report_filter['ID'] = []
    plant_trans = {}
    inverter_trans = {}
    def groupID_get_inverter(inv_filter={}):
        inv_ID_list = []
        inv_filter['type'] = 'inv'
        for inverter in db.equipment.find(inv_filter):
            inv_ID = str(inverter['_id'])
            inv_ID_list.append(inv_ID)
            inverter_trans[inv_ID] = inverter.get('name')
        return inv_ID_list
    try:
        for i, col in enumerate(col_list):
            if col == 'pv_plant':
                for plant in db.plant.find({'_id': ObjectId(ID_list[i])}):  
                    for group in db.equipment.find({'PV': plant.get('name'), 'type': 'pv_group'}):
                        inv_ID_list = groupID_get_inverter({'PV': plant.get('name'), 'lgroup': group.get('lgroup'), 'group': group.get('name')})
                        report_filter['ID'].extend(inv_ID_list)
                        plant_trans.update(dict.fromkeys(inv_ID_list, '{}\\{}\\{}'.format(plant.get('name'), group.get('lgroup'), group.get('name'))))
            elif col == 'pv_lgroup':
                for lgroup in db.equipment.find({'_id': ObjectId(ID_list[i])}):
                    for group in db.equipment.find({'PV': lgroup.get('PV'), 'lgroup': lgroup.get('name'), 'type': 'pv_group'}):
                        inv_ID_list = groupID_get_inverter({'PV': group.get('PV'), 'lgroup': group.get('lgroup'), 'group': group.get('name')})
                        report_filter['ID'].extend(inv_ID_list)
                        plant_trans.update(dict.fromkeys(inv_ID_list, '{}\\{}\\{}'.format(group.get('PV'), group.get('lgroup'), group.get('name'))))
            else:  #group
                for group in db.equipment.find({'_id': ObjectId(ID_list[i])}):
                    inv_ID_list = groupID_get_inverter({'PV': group.get('PV'), 'lgroup': group.get('lgroup'), 'group': group.get('name')})
                    report_filter['ID'].extend(inv_ID_list)
                    plant_trans.update(dict.fromkeys(inv_ID_list, '{}\\{}\\{}'.format(group.get('PV'), group.get('lgroup'), group.get('name'))))
    except Exception as e:
        return bad_request('Bad Request. Due to {}'.format(exception_detail(e)))
    report_filter['ID'] = {'$in': report_filter['ID']}
    return_list = []
    pageType = None
    if 'pageType' in user_c:
        pageType = user_c['pageType']
    current_page =  request_dict.get('page', 1)
    realtime_length = 0
    realtime_page = 0
    today = datetime.datetime.combine(datetime.datetime.today(), datetime.time(hour=0, minute=0, second=0, microsecond=0))
    if 'time' not in report_filter or ( today >= report_filter['time']['$gte'] and today <= report_filter['time']['$lt']):
        realtime_page = math.floor(len(report_filter['ID']['$in'])/ 10) + 1
        realtime_length = len(report_filter['ID']['$in'])
        if current_page <= realtime_page:
            c = 0
            for i in range((current_page-1)*10, len(report_filter['ID']['$in'])):
                ID = report_filter['ID']['$in'][i]
                filename = '_____realtime_____{}'.format(ID)
                return_list.append({
                    'filename': filename,
                    'inverter': inverter_trans.get(ID),
                    'time': datetime.datetime.strftime(datetime.datetime.today(), '%Y-%m-%d'),
                    'group': plant_trans[ID],
                    'realtime': False,
                })
                c += 1
                if c == 10:
                    break
    current_page -= realtime_page
    if current_page >= 1:
        for report in db.inverter_excel.find(report_filter).skip((current_page - 1)*10).limit(10).sort('time', -1):
            try:
                return_list.append({
                    'filename': report['filename'] if pageType in ['pv', None] else '{}/{}'.format(pageType, report['filename']),
                    'inverter': inverter_trans.get(report['ID']),
                    'time': datetime.datetime.strftime(report['time'], '%Y-%m-%d'),
                    'group': plant_trans[report['ID']],
                    'realtime': False,
                })
            except:
                continue

    return successful_request({
        'data': return_list,
        'total_report': db.inverter_excel.count_documents(report_filter) + math.ceil(realtime_length/10)*10,
        "total_page": math.ceil((db.inverter_excel.count_documents(report_filter) + math.ceil(realtime_length/10)*10)/10)
    })
#-------------------------------------------------------------------------------
class DocxPrototype(views.MethodView):
    def __init__(self, collection="docx", time_interval="month", default_leval="lgroup"):
        super().__init__()
        self.collection = collection
        self.time_interval = time_interval
        self.default_level = default_leval
    def post(self):
        user,db = check_user()
        if(db == None):
            return logout()
        find_user = find_user_from_current_user()
        
        user_c=list(db.users.find({"user_id" : find_user}))[0]
        request_dict = request.json
        ID_list = request_dict.get('ID_list', [])
        col_list = request_dict.get('col_list', [])
        report_filter = {'show': 1}
        # time filter
        if request_dict.get('time', {}).get('mode', '') == 'single':
            try:
                start_date = datetime.datetime.strptime(request_dict['time']['start_date'], '%Y-%m-%d')
                end_date = start_date + datetime.timedelta(days=1)
                report_filter['time'] = {'$gte': start_date, '$lt': end_date}
            except:
                return bad_request(400, 'Time error')
        elif request_dict.get('time', {}).get('mode', '') == 'interval':
            try:
                start_date = datetime.datetime.strptime(request_dict['time']['start_date'], '%Y-%m-%d')
                end_date = datetime.datetime.strptime(request_dict['time']['end_date'], '%Y-%m-%d')
                report_filter['time'] = {'$gte': start_date, '$lt': end_date+datetime.timedelta(days=1)}
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
            report_filter['time'] = {'$gte': start_date, '$lt': end_date}
        # plant filter
        if isinstance(ID_list, list) and len(ID_list) > 0:
            pass
        # Search All
        else:
            plant_filter = {}
            if user_c['plant'][0] != 'total':
                for i in user_c['plant']:
                    if 'name' not in plant_filter:
                        plant_filter['name'] = {'$in': []}
                    plant_filter['name']['$in'].append(i)
            for plant in db.plant.find(plant_filter):
                ID_list.append(str(plant['_id']))
                col_list.append(str(plant['collection']))
        #print(ID_list, col_list)
        report_filter['ID'] = []
        plant_trans = {}
        try:
            for i, col in enumerate(col_list):
                if col == 'pv_plant':
                    for plant in db.plant.find({'_id': ObjectId(ID_list[i])}):
                        excel_level = self.default_level
                        if excel_level == 'PV' or excel_level == 'plant':
                            report_filter['ID'].append(str(plant['_id']))
                            plant_trans[str(plant['_id'])] = plant.get('name')
                        elif excel_level == 'lgroup' or excel_level == 'pv_lgroup':
                            for lgroup in db.equipment.find({'PV': plant.get('name'), 'type': 'pv_lgroup'}):
                                report_filter['ID'].append(str(lgroup['_id']))
                                plant_trans[str(lgroup['_id'])] = '{}\\{}'.format(plant.get('name'), lgroup.get('name'))
                        else: # group
                            for group in db.equipment.find({'PV': plant.get('name'), 'type': 'pv_group'}):
                                report_filter['ID'].append(str(group['_id']))
                                plant_trans[str(group['_id'])] = '{}\\{}\\{}'.format(plant.get('name'), lgroup.get('name'), group.get('name'))
                elif col == 'pv_lgroup':
                    for lgroup in db.equipment.find({'_id': ObjectId(ID_list[i])}):
                        for plant in db.plant.find({'name': lgroup.get('PV', None)}):
                            excel_level = self.default_level
                            if excel_level == 'PV' or excel_level == 'plant':
                                report_filter['ID'].append(str(plant['_id']))
                                plant_trans[str(plant['_id'])] = plant.get('name')
                            elif excel_level == 'lgroup' or excel_level == 'pv_lgroup':
                                report_filter['ID'].append(str(lgroup['_id']))
                                plant_trans[str(lgroup['_id'])] = '{}\\{}'.format(lgroup.get('PV'), lgroup.get('name'))
                            else:
                                for group in db.equipment.find({'PV': group.get('PV'), 'lgroup': lgroup.get('name'), 'type': 'pv_group'}):
                                    report_filter['ID'].append(str(group['_id']))
                                    plant_trans[str(group['_id'])] = '{}\\{}\\{}'.format(group.get('PV'), group.get('lgroup'), group.get('name'))

                else:  #group
                    for group in db.equipment.find({'_id': ObjectId(ID_list[i])}):
                        for plant in db.plant.find({'name': group.get('PV', None)}):
                            excel_level = self.default_level
                            if excel_level == 'PV' or excel_level == 'plant' or excel_level == 'pv_plant':
                                report_filter['ID'].append(str(plant['_id']))
                                plant_trans[str(plant['_id'])] = plant.get('name')
                            elif excel_level == 'lgroup' or excel_level == 'pv_lgroup' or excel_level == 'pv_lgroup':
                                for lgroup in db.equipment.find({'PV': group.get('PV'), 'name': group.get('lgroup'), 'type': 'pv_lgroup'}):
                                    report_filter['ID'].append(str(lgroup['_id']))
                                    plant_trans[str(lgroup['_id'])] = '{}\\{}'.format(lgroup.get('PV'), lgroup.get('name'))
                            else:
                                report_filter['ID'].append(str(group['_id']))
                                plant_trans[str(group['_id'])] = '{}\\{}\\{}'.format(group.get('PV'), group.get('lgroup'), group.get('name'))
        except Exception as e:
            return bad_request('Bad Request. Due to {}'.format(exception_detail(e)))
        report_filter['ID'] = {'$in': report_filter['ID']}
        return_list = []
        # excel 不用分 pageType
        pageType = None
        if 'pageType' in user_c:
            pageType = user_c['pageType']
        current_page =  request_dict.get('page', 1)
        report_filter['time_interval'] = self.time_interval
        if self.time_interval == 'month':
            _filter = report_filter.copy()
            _filter['time_interval'] = {'$exists': False}
            report_filter = {'$or': [report_filter, _filter]}
        for report in db[self.collection].find(report_filter).skip((current_page - 1)*10).limit(10).sort('time', -1):
            try:
                return_list.append({
                    'filename': report['filename'] if pageType in ['pv', None] else '{}/{}'.format(pageType, report['filename']),
                    'period': report.get('peroid', '---'),
                    'time': datetime.datetime.strftime(report['time'], '%Y-%m-%d'),
                    'group': plant_trans[report['ID']],
                })
            except:
                continue
        print(self.time_interval)
        return successful_request({
            'data': return_list,
            'total_report': db[self.collection].count_documents(report_filter),
            "total_page": math.ceil(db[self.collection].count_documents(report_filter)/10)
        })
class GetDocxWeek(DocxPrototype):
    def __init__(self):
        super().__init__(time_interval="week")
        self.time_interval = 'week'
application_common.add_url_rule('/report_get_week_report', view_func=GetDocxWeek.as_view('report_get_week_report'))

class GetDocx(DocxPrototype):
    pass
application_common.add_url_rule('/report_get_month_report', view_func=GetDocx.as_view('report_get_month_report'))

class GetDocxDay(DocxPrototype):
    def __init__(self):
        super().__init__(time_interval="day")
application_common.add_url_rule('/report_get_day_report', view_func=GetDocxDay.as_view('report_get_day_report'))
#-------------------------------------------------------------------------------
# 使用位置 /reportOverview 報表總覽 週報表-A搜尋
@application_common.route('/report_get_week_report_A', methods=['POST'])
def report_get_week_report_A():
    user,db = check_user()
    if(db == None):
        return logout() 
    find_user = find_user_from_current_user()
    user_c=list(db.users.find({"user_id" : find_user}))[0]
    request_dict = request.json
    report_filter = {'show': 1}
    # time filter
    if request_dict.get('time', {}).get('mode', '') == 'single':
        try:
            start_date = datetime.datetime.strptime(request_dict['time']['start_date'], '%Y-%m-%d')
            end_date = start_date + datetime.timedelta(days=1)
            report_filter['time'] = {'$gte': start_date, '$lt': end_date}
        except:
            return bad_request(400, 'Time error')
    elif request_dict.get('time', {}).get('mode', '') == 'interval':
        try:
            start_date = datetime.datetime.strptime(request_dict['time']['start_date'], '%Y-%m-%d')
            end_date = datetime.datetime.strptime(request_dict['time']['end_date'], '%Y-%m-%d')
            report_filter['time'] = {'$gte': start_date, '$lt': end_date+datetime.timedelta(days=1)}
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
        report_filter['time'] = {'$gte': start_date, '$lt': end_date}
    
    return_list = []
    pageType = None
    if 'pageType' in user_c:
        pageType = user_c['pageType']
    current_page =  request_dict.get('page', 1)
    for report in db.week_docx.find(report_filter).skip((current_page - 1)*10).limit(10).sort('time', -1):
        try:
            return_list.append({
                'filename': report['filename'] if pageType in ['pv', None] else '{}/{}'.format(pageType, report['filename']),
                'time': datetime.datetime.strftime(report['time'], '%Y-%m-%d'),
            })
        except:
            continue
    return successful_request({
        'data': return_list,
        'total_report': db.week_docx.count_documents(report_filter),
        "total_page": math.ceil(db.week_docx.count_documents(report_filter)/10)
    })
#-------------------------------------------------------------------------------
#使用位置 /reportOverview taipower 即時週報表A
@application_common.route('/download_realtime_week_a_excel')
def download_realtime_week_a_excel():
    user,db = check_user()
    if(db == None):
        return logout() 
    import week_A_excel.web_onmac as wa
    file_info, file_binary = wa.week_mainA(db)
    return send_file(file_binary, download_name=file_info.get('filename', 'report.xls'), as_attachment=True)
#-------------------------------------------------------------------------------
#使用位置 /stationGraphic SLD 單線圖與平面圖
@application_common.route('/SLD_path_analysis', methods=['POST'])
def SLD_path_analysis():
    user,db = check_user()
    if(db == None):
        return logout() 
    request_dict = request.json
    plant = request_dict.get('plant', None)
    lgroup = request_dict.get('lgroup', None)
    group = request_dict.get('group', None)
    svg = request_dict.get('svg', None)
    layout = request_dict.get('layout', None)
    if plant == None and svg == None:
        try:
            plant = db.users.find_one({"username":user[1]},{"plant":1})["plant"][0]
        except:
            plant = "total"
       
        if plant == "total":
            try:
                plant = db.plant.find_one()["name"]     
            except:
                plant = "null"
                svg = "null"
    if lgroup == None or (type(lgroup)==str and len(lgroup)==0):
        try:
            lgroup = db.equipment.find_one({'PV':plant, 'type': 'pv_lgroup'})['name']
            # if 平面圖 則回傳group
            group = db.equipment.find({'PV':plant, 'lgroup': lgroup, 'type': 'pv_group'})['name']
        except:
            lgroup = "null"
    if svg == None and group == None:
        svg = lgroup
    elif svg == None and group != None:
        svg = group
    else:
        pass
    if svg[len(svg)-6:len(svg)] == "Layout":
        """ if layout == 0:
            svg = svg[:-6] """
        layout = 1
    elif plant!="null" and layout == 1:   
        svg = svg+"Layout"
    return successful_request({'plant':plant, 'svg':svg,'layout':layout, 'lgroup':lgroup, 'group': group})
#-------------------------------------------------------------------------------
@application_common.route('/get_data_integrity_stats', methods=['POST'])
def get_data_integrity_stats():
    user,db = check_user()
    if(db == None):
        return logout() 
    find_user = find_user_from_current_user()
    user_c=list(db.users.find({"user_id" : find_user}))[0]

    request_dict = request.json
    try:
        ID = request_dict['ID']
        if ID != None:
            ObjectId(ID)
    except:
        return bad_request(400, 'Bad Request. ID Error')
    try:
        start_date = request_dict['start_date']
        end_date = request_dict['end_date']
        date_mode = request_dict.get('date_mode', 'single')
        start_date = datetime.datetime.strptime(start_date, '%Y-%m-%d')
        end_date = datetime.datetime.strptime(end_date, '%Y-%m-%d')
        if date_mode == 'single':
            end_date = start_date
        end_date += datetime.timedelta(days=1)
    except:
        return bad_request(400, 'Bad Request. Date Error')
    ID_list = []
    info_dict = {}
    child_info_dict = {}
    if ID != None:
        for plant in db.plant.find({'_id': ObjectId(ID)}):
            ID_list.append(str(plant['_id']))
            plant['_id'] = str(plant['_id'])
            info_dict = plant
            child_filter = {'PV': plant.get('name'), 'lgroup': {'$exists': False}, 'group': {'$exists': False}} 

        for equip in db.equipment.find({'_id': ObjectId(ID)}):
            ID_list.append(str(equip['_id']))
            equip['_id'] = str(equip['_id'])
            info_dict = equip
            child_filter = {'PV': equip.get('PV')}
            if equip.get('type') == 'pv_lgroup':
                child_filter['lgroup'] = equip.get('name')
                child_filter['group'] = {'$exists': False} 
            elif equip.get('type') == 'pv_group':
                child_filter['lgroup'] = equip.get('lgroup')
                child_filter['group'] = equip.get('name')

        for child in db.equipment.find(child_filter):
            ID_list.append(str(child['_id']))
            child_info_dict[str(child['_id'])] = child
    else:
        plant_filter = {}
        if user_c['plant'][0] != 'total':
            for i in user_c['plant']:
                if 'name' not in plant_filter:
                    plant_filter['name'] = {'$in': []}
                plant_filter['name']['$in'].append(i)
        for plant in db.plant.find(plant_filter):
            ID_list.append(str(plant['_id']))
            child_info_dict[str(plant['_id'])] = plant
    done = True
    self_done_list = []
    self_lost_list = []
    child_lost_list = []
    child_rate_strange_list = []
    for _data in db.data_integrity.find({'ID': {'$in': ID_list}, 'time': {'$gte': start_date, '$lt': end_date}}):
        try:
            done &= _data.get('done', False)
            if _data['ID'] == ID: # plant lgroup group
                if _data.get('done') == True:
                    self_done_list.append({
                        '_id': str(_data['_id']),
                        'time': datetime.datetime.strftime(_data['time'], '%Y-%m-%d' if _data.get('level') == 'day' else '%Y-%m-%d %H:%M'),
                        'time_interval': _data['time_interval'],
                        'level': _data.get('level'),
                        'ID': ID,
                        'rate': _data.get('rate') if not isinstance(_data.get('rate', 0), (int, float)) else round(_data.get('rate', 0), 3),
                        'cal_restart_done': _data.get('cal_restart_done'),
                        'virtual': info_dict.get('virtual', 1)
                    })
                else:
                    self_lost_list.append({
                        '_id': str(_data['_id']),
                        'time': datetime.datetime.strftime(_data['time'], '%Y-%m-%d' if _data.get('level') == 'day' else '%Y-%m-%d %H:%M'),
                        'time_interval': _data['time_interval'],
                        'level': _data.get('level'),
                        'ID': ID,
                        'rate': _data.get('rate') if not isinstance(_data.get('rate', 0), (int, float)) else round(_data.get('rate', 0), 3),
                        'cal_restart_done': _data.get('cal_restart_done'),
                        'virtual': info_dict.get('virtual', 1)
                    })
            else: # Child or other equipment
                if _data.get('done') != True:
                    child_lost_list.append({
                        '_id': str(_data['_id']),
                        'time': datetime.datetime.strftime(_data['time'], '%Y-%m-%d' if _data.get('level') == 'day' else '%Y-%m-%d %H:%M'),
                        'time_interval': _data['time_interval'],
                        'level': _data.get('level'),
                        'ID': _data['ID'],
                        'rate': _data.get('rate') if not isinstance(_data.get('rate', 0), (int, float)) else round(_data.get('rate', 0), 3),
                        'cal_restart_done': _data.get('cal_restart_done'),
                        'name': child_info_dict.get(_data['ID'], {}).get('name', ''),
                        'virtual': child_info_dict.get(_data['ID'], {}).get('virtual', 1)
                    })
                elif not isinstance(_data.get('rate'), (int, float)) or _data.get('rate') < 0 or _data.get('rate') > 1:
                    child_rate_strange_list.append({
                        '_id': str(_data['_id']),
                        'time': datetime.datetime.strftime(_data['time'], '%Y-%m-%d' if _data.get('level') == 'day' else '%Y-%m-%d %H:%M'),
                        'time_interval': _data['time_interval'],
                        'level': _data.get('level'),
                        'ID': _data['ID'],
                        'rate': _data.get('rate') if not isinstance(_data.get('rate', 0), (int, float)) else round(_data.get('rate', 0), 3),
                        'cal_restart_done': _data.get('cal_restart_done'),
                        'name': child_info_dict.get(_data['ID'], {}).get('name', ''),
                        'virtual': child_info_dict.get(_data['ID'], {}).get('virtual', 1)
                    })
        except Exception as e:
            print(e)
            continue

    return_dict = {
        'done': done,
        'self_done': self_done_list,
        'self_lost': self_lost_list,
        'info_dict': info_dict,
        'child_lost': child_lost_list,
        'child_rate_strange': child_rate_strange_list,
    }
    return successful_request(return_dict)
#-------------------------------------------------------------------------------
# deepLearning
# 模板清洗 module_cleaning
# 取得頁面資料
class GetModuleCleaningData(views.MethodView):
    def post(self):
        user,db = check_user()
        if db == None:
            return logout()
        request_dict = request.json
        try:
            # lgroup ID
            ID = request_dict['ID']
            ObjectId(ID)
            lgroup_data = db.equipment.find_one({'_id': ObjectId(ID)})
            plant_data = db.plant.find_one({'name': lgroup_data['PV']})
        except Exception as e:
            return bad_request(400, 'Bad Request. ID Error. {}'.format(e))

        daily_show_information = {}
        for info in db.cleaning.find({'ID': ID, 'type': 'daily_show_information'}).sort('time', -1):
            try:
                info['_id'] = str(info['_id'])
                info['time'] = datetime.datetime.strftime(info['time'], '%Y-%m-%d %H:%M-%S')
                try:
                    info['expected_pr'] = round(info['expected_pr'], 2)
                except:
                    info['expected_pr'] = '---'
                try:
                    info['current_soiling_value'] = round(info['current_soiling_value']*100, 2)
                except:
                    info['current_soiling_value'] = '---'
                try:
                    info['expected_total_loss'] = round(info['expected_total_loss'], 2)
                except:
                    info['expected_total_loss'] = '---'
                try:
                    info['expected_today_loss'] = round(info['expected_today_loss'], 2)
                except:
                    info['expected_today_loss'] = '---'
                daily_show_information = info
                break
            except:
                pass
        return successful_request({
            'weather_data': self.get_three_day_weather(db, plant_data),
            'daily_show_information': daily_show_information
        })
    def get_three_day_weather(self, db, plant_data:dict):
        weather_list = []
        current_date = datetime.datetime.now()
        for i in range(3):
            weather_data = c.get_weather_forecast_by_date(db, plant_data.get('location', {}).get('city', ''), current_date)
            weather_list.append({
                'date': datetime.datetime.strftime(current_date, '%m-%d'),
                'imgurl': weather_data.get('imgurl', ''),
                'temperature': weather_data.get('T', '---'),
                'status':weather_data.get('Wx', '---'),
                'rain': '---' if isinstance(weather_data.get('PoP6h', '---'), str) else int(weather_data['PoP6h'])
            })
            current_date += datetime.timedelta(1)
        return weather_list
application_common.add_url_rule('/get_module_cleaning_data', view_func=GetModuleCleaningData.as_view('get_module_cleaning_data'))
#------------------------------------------------------------------------------------------------------------
# deepLearning
# 模板清洗 module_cleaning
# 取得歷史髒污累積圖
class GetModuleCleaningSoilPlot(views.MethodView):
    def post(self):
        user,db = check_user()
        if db == None:
            return logout()
        request_dict = request.json
        try:
            # lgroup ID
            ID = request_dict['ID']
            ObjectId(ID)
            lgroup_data = db.equipment.find_one({'_id': ObjectId(ID)})
        except Exception as e:
            return bad_request(400, 'Bad Request. ID Error. {}'.format(e))
        today = datetime.datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
        start_date = today - relativedelta.relativedelta(years=1)
        end_date = today - datetime.timedelta(days=1)
        x_axis = t.fix_x_xis_date(start_date, end_date, 2)
        daily_normalized = t.dayline_one(db, 'cleaning', ID, 'value', 
        start_date, end_date, 86400, {'type': 'daily_normalized'})
        perfect_clean =  t.dayline_one(db, 'cleaning', ID, 'value', 
        start_date, end_date, 86400, {'type': 'perfect_clean'})
        for i in range(len(x_axis)):
            if perfect_clean[i] != None and math.isnan(perfect_clean[i]):
                perfect_clean[i] = None
            if daily_normalized[i] != None and math.isnan(daily_normalized[i]):
                daily_normalized[i] = None
        return successful_request({
            'x_axis': x_axis,
            'daily_normalized': daily_normalized,
            'perfect_clean': perfect_clean
        })
application_common.add_url_rule('/get_module_cleaning_soil_plot', view_func=GetModuleCleaningSoilPlot.as_view('get_module_cleaning_soil_plot'))

#------------------------------------------------------------------------------------
@application_common.route('/get_digital_twin_data', methods=['POST'])
def get_digital_twin_data():
    user,db = check_user()
    if(db == None):
        return logout() 
    request_dict = request.json
    try:
        start_time = request_dict["datepicker1"]
        end_time = request_dict["datepicker2"]
        end_time += " 23:00:00"
        start_time += " 00:00:00"
        start_time = datetime.datetime.strptime(start_time, '%Y-%m-%d %H:%M:%S')
        end_time = datetime.datetime.strptime(end_time, '%Y-%m-%d %H:%M:%S')

        x_axis =[]
        real_time_len=0
        if start_time<=end_time:
            start_time = start_time + relativedelta.relativedelta(hour=0,minute=0,second=0)
            end_time = end_time + relativedelta.relativedelta(days=+1,hour=0,minute=0,second=0)
            real_time_len = (end_time - start_time).total_seconds()/(60*15)
        

        real_time_len=int(real_time_len)
        deltatime = datetime.timedelta(minutes=15)
        nexttime = datetime.datetime.combine(start_time, datetime.time.min)

        for i in range(real_time_len):
            x_axis.append(datetime.datetime.strftime(nexttime,"%Y-%m-%d %H:%M:%S"))
            nexttime  = nexttime + deltatime 

        ID = request_dict["ID"]
        return_data = {
            "real_power": [],
            "output_power": [],
            "time": []
        }

        twin_collection = db["digital_twin_output"]
        for time in x_axis:
            data = twin_collection.find_one(
                {
                    "ID": ID,
                    "time": datetime.datetime.strptime(time,"%Y-%m-%d %H:%M:%S")
                }
            )
            if data != None:
                if data.get("real_power", None) != None:
                    return_data["real_power"].append(round(data["real_power"], 2))
                else:
                    return_data["real_power"].append(None)
                if data.get("output_power", None) != None:
                    return_data["output_power"].append(round(data["output_power"], 2))
                else:
                    return_data["output_power"].append(None)
            else:
                return_data["output_power"].append(None)
                return_data["real_power"].append(None)
        return_data["time"] = x_axis
        output_data = {
            "data": return_data
        }
        return successful_request({'data': output_data})
    except Exception as e:
        print(exception_detail(e))
        return bad_request(400, "Bad Request. {}".format(e))
#-------------------------------------------------------------------------------
#使用位置 /setting
# web_nav_page setting
class WebNavPageData(views.MethodView):
    def post(self):
        user,db = check_user()
        if(db == None):
            return logout() 
        request_dict = request.json
        find_user = find_user_from_current_user()
        user_c=list(db.users.find({"user_id" : find_user}))[0]
        if user_c.get('level', 1) < 3 or user_c.get('superuser', False) != True:
            return bad_request(400, 'Bad Request.')
        if request_dict.get('method') == 'update':
            try:
                data = request_dict['data']
                #print(data)
                update_dict = {
                    'icon': data.get('icon'),
                    'level': data['level'],
                    'name': data['name'],
                    'name_i18n': data['name_i18n'],
                    'pageType': data['pageType'],
                    'priority': data['priority'],
                    'route': data['route'],
                    'show': 1,
                    'type': data['type']
                }
                if data['type'] == 'tab':
                    update_dict['value'] = data['value']
                    try:
                        update_dict['constrain'] = json.loads(data.get('constrain'))
                    except:
                        update_dict['constrain'] = None
                elif data['type'] == 'navLink':
                    if data.get('show', False):
                        update_dict['show'] =  1
                    else:
                        update_dict['show'] = 0
                if 'zh-TW' not in data['name_i18n'] or 'en-US' not in data['name_i18n']:
                    return bad_request(400, 'Bad Request. name_i18n')
                if 'superuser' in data and data['superuser'] != True:
                    update_dict['superuser'] = False
                else:
                    update_dict['superuser'] = True
                if data['ID'] != None:
                    ObjectId(data['ID'])
                    db.web_nav_page.update_one({'_id': ObjectId(data['ID'])}, {'$set': update_dict})
                else:
                    db.web_nav_page.insert_one(update_dict)
            except Exception as e:
                return bad_request(400, "Bad Request. {}".format(e))
        return successful_request()
    def get(self):
        user,db = check_user()
        if(db == None):
            return logout() 
        pageType = request.args.get('pageType', None)
        find_filter = {}
        if pageType != None and pageType != '':
            find_filter['pageType'] = {'$in': ['all', pageType]}
        # Get All pageType
        pageType_list = []
        for user in db.users.find({}, {'_id': 0, 'pageType': 1}):
            if 'pageType' in user and user['pageType'] not in pageType_list:
                pageType_list.append(user['pageType'])
        navLink_data = []
        tab_data = []
        navLink_length = 0
        tab_length = 0
        for data in db.web_nav_page.find(find_filter).sort('priority', 1):
            try:
                data['ID'] = str(data['_id']) 
                data.pop('_id', None)
                if isinstance(data['level'], (int, float)):
                    data['level'] = int(data['level'])
                    new_level = []
                    i = 3
                    while i >= data['level']:
                        new_level.append(i)
                        i -= 1
                    data['level'] = new_level
                if data['level'] == 'all':
                    data['all_level'] = True
                else:
                    data['all_level'] = False
                if data['pageType'] == 'all':
                    data['all_pageType'] = True
                else:
                    for p in data['pageType']:
                        if p not in pageType_list:
                            pageType_list.append(p)
                if data.get('show', 0) == 1:
                    data['show'] = True
                else:
                    data['show'] = False
                
                if data['type'] == 'navLink':
                    navLink_data.append(data)
                elif data['type'] == 'tab':
                    try:
                        data['constrain'] = json.dumps(data['constrain'])
                    except:
                        data['constrain'] = None
                    tab_data.append(data)

            except Exception as e:
                print(exception_detail(e))
                pass
        # Sort tab_data
        try:
            tab_data = sorted(tab_data, key=lambda x: x['route'])
        except Exception as e:
            pass
        return successful_request({
            'navLink_data': navLink_data,
            'navLink_length': len(navLink_data),
            'tab_data': tab_data,
            'tab_length': len(tab_data),
            'pageType_list': pageType_list
        })
    def delete(self):
        user,db = check_user()
        if(db == None):
            return logout() 
        try:
            ID = request.args['ID']
            ObjectId(ID)
        except:
            return bad_request(400, 'Bad Request. ID Error.')
        find_user = find_user_from_current_user()
        user_c=list(db.users.find({"user_id" : find_user}))[0]
        if user_c.get('level', 1) < 3 or user_c.get('superuser', False) != True:
            return bad_request(400, 'Bad Request.')
        db.web_nav_page.delete_one({'_id': ObjectId(ID)})
        return successful_request()
application_common.add_url_rule('/web_nav_page_data', view_func=WebNavPageData.as_view('web_nav_page_data'))
#-------------------------------------------------------------------------------
#使用位置 /setting
# web_nav_page setting
# export full collection of web_nav_page
@application_common.route('/web_nav_page_json_export')
def web_nav_page_json_export():
    user,db = check_user()
    if(db == None):
        return logout() 
    file = BytesIO()
    data = json.dumps(json.loads(json_util.dumps(db.web_nav_page.find({}))))
    file.write(data.encode())
    file.seek(0)
    rv = send_file(
        file,
        as_attachment=True,
        download_name="web_nav_page.json"
    )
    return rv
#-------------------------------------------------------------------------------
#使用位置 /setting
# web_nav_page setting
# upload json of web_nav_page
@application_common.route('/web_nav_page_json_upload', methods=['POST'])
def web_nav_page_json_upload():
    user,db = check_user()
    if(db == None):
        return logout() 
    try:
        json_file = request.files
        for file_name in request.files:
            json_file = request.files[file_name]
            web_nav_page_data = json_util.loads(json_file.read())
            for data in web_nav_page_data:
                db.web_nav_page.update_one({'_id': ObjectId(data['_id'])}, {'$set': data}, upsert=True)
    except Exception as e:
        return bad_request(400, 'Bad Request. {}'.format(e))
    return successful_request()
#-------------------------------------------------------------------------------
#使用位置 /setting
# web_nav_page setting
# connect other mongoDB
@application_common.route('/web_nav_page_server_connection', methods=['POST', 'GET'])
def web_nav_page_server_connection():
    user,db = check_user()
    if(db == None):
        return logout() 
    if request.method == 'POST':
        request_dict = request.json
    else:
        request_dict = request.args
    try:
        url = request_dict['url']
        another_db = request_dict['db']
    except Exception as e:
        return bad_request(400, 'Bad Request. {}'.format(e))
    #print(url, another_db)
    try:
        new_conn = MongoClient(url, connectTimeoutMS=2000, serverSelectionTimeoutMS=2000)
        web_data = new_conn[another_db].web_nav_page.find({})
        file = BytesIO()
        data = json.dumps(json.loads(json_util.dumps(web_data)))
        file.write(data.encode())
        file.seek(0)
        rv = send_file(
            file,
            as_attachment=True,
            download_name="web_nav_page.json"
        )
        return rv
    except Exception as e:
        return bad_request(400, 'Bad Request. {}'.format(e))
#-------------------------------------------------------------------------------
#使用位置 /setting
# web_nav_page setting
# site_reidrect_navbar setting
class SiteRedirectNavbar(views.MethodView):
    def get(self):
        user,db = check_user()
        if(db == None):
            return logout() 
        return_dict = {
            'json_data': [],
            'json_string': "[]",
            'enable': False
        }
        urlData = db.parameter_setting.find_one({'method': 'site_redirect_navbar'})
        if urlData != None:
            return_dict['json_data'] = json.loads(urlData.get('data', '[]'))
            return_dict['json_string'] = urlData.get('data', '[]')
            return_dict['enable'] = urlData.get('enable', False)
        return successful_request(return_dict)
    def post(self):
        user,db = check_user()
        if(db == None):
            return logout() 
        find_user = find_user_from_current_user()
        user_c=list(db.users.find({"user_id" : find_user}))[0]
        if user_c.get('level', 1) < 3 or user_c.get('superuser', False) != True:
            return bad_request(400, 'Bad Request.')
        try:
            request_dict = request.json
            mode = request_dict['mode']
            urlData = db.parameter_setting.find_one({'method': 'site_redirect_navbar'})
            if urlData == None:
                db.parameter_setting.insert_one({'method': 'site_redirect_navbar', 'enable': False,
                'data': '[]'
                })
            if mode == 'enable':
                data = request_dict['data']
                if isinstance(data, bool):
                    db.parameter_setting.update_one({'method': 'site_redirect_navbar'}, {
                        '$set': {'enable': data}
                    })
            elif mode == 'data':
                data = request_dict['data']
                data_json = json.loads(data)
                db.parameter_setting.update_one({'method': 'site_redirect_navbar'}, {
                    '$set': {'data': json.dumps(data_json, separators=(',', ':'))}
                })
        except Exception as e:
            return bad_request(400, 'Bad Request. {}'.format(e))
        return successful_request()
application_common.add_url_rule('/site_redirect_navbar', view_func=SiteRedirectNavbar.as_view('site_redirect_navbar'))
#-------------------------------------------------------------------------------
@application_common.route('/get_dispatch_report', methods=['POST'])
def get_dispatch_report():
    user, db = check_user()
    if db == None:
        return logout()
    request_dict = request.json
    try:
        rv = d.report_dispatch_maohong(db, request_dict)
        return rv
    except Exception as e:
        print(exception_detail(e))
        return bad_request(400, 'Bad request. {}'.format(e))

