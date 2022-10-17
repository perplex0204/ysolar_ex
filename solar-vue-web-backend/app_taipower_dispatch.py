# 台電 Vue 派工專用API
# 主程式功能
# Flask App 函式
from app_common import exception_detail, successful_request, bad_request, check_user, logout, find_user_from_current_user, date_range_interval_to_filter
#-------------------------------------------------------------------------------
# Libiary
from flask import Blueprint, request, views, current_app
from dateutil import relativedelta
import datetime
import math
from bson import ObjectId
from werkzeug.utils import secure_filename
import os
#-------------------------------------------------------------------------------
# 通用函式與功能
import current as c
#======================================================================================================
# application_dispatch is a Blueprint of flask
# Learn More About Blueprint At
# https://flask.palletsprojects.com/en/2.0.x/blueprints/
application_dispatch = Blueprint('application_dispatch', __name__)
#======================================================================================================
# Dispatch stage 派工單階段
# wait_for_priority
# wait_for_take
# took_wait_date_enter
# merged
# wait_admin_confirm_date
# wait_for_dispatch
# dispatched_wait_for_review
# auto_reviewed_wait_for_manual
# review_failed
# dispatch_finish
#======================================================================================================
class DispatchPushNotification():
    def __init__(self, db, dispatch_ID:str, name: str, station_ID: str) -> None:
        self.db =db
        station_data = db.equipment.find_one({'_id': ObjectId(station_ID)})
        station_name = "案場" if station_data == None or not isinstance(station_data, dict) or ('PV' not in station_data or 'name' not in station_data) else \
        '{}/{}'.format(
            station_data.get('PV', '案場'), station_data.get('name', '群組')
        )
        try:
            self.PV_name = station_data.get('PV', '案場')
        except:
            self.PV_name = ""
        self.stage_user_level_mag = {
            'wait_for_take': {
                1: {
                    'title': '{}派工系統'.format(station_name),
                    'content': '工單{}已產生，可前往接單'.format(name),
                },
                3: {
                    'title': '{}派工系統'.format(station_name),
                    'content': '工單{}已產生'.format(name),
                }
            },
            'transfer_wait_for_take': {
                1: {
                    'title': '{}派工系統'.format(station_name),
                    'content': '工單{}已轉單，可前往接單'.format(name),
                },
                3: {
                    'title': '{}派工系統'.format(station_name),
                    'content': '工單{}維運人員已轉單'.format(name),
                }
            },
            'wait_for_priority': {},
            'took_wait_date_enter': {
                3: {
                    'title': '{}派工系統'.format(station_name),
                    'content': '{}維運人員已接單，等待填入派工日期'.format(name),
                }
            },
            'took_wait_date_enter_failed': {
                1: {
                    'title': '{}派工系統'.format(station_name),
                    'content': '管理人員拒絕{}派工日期'.format(name),
                }
            },
            'wait_admin_confirm_date_success': {
                3: {
                    'title': '{}派工系統'.format(station_name),
                    'content': '管理人員同意{}派工日期，進入等待派工階段'.format(name),
                }
            },
            'merged': {},
            'wait_admin_confirm_date': {
                3: {
                    'title': '{}派工系統'.format(station_name),
                    'content': '請確認{}派工日期'.format(name),
                }
            },
            'take_to_wait_for_dispatch': {
                3: {
                    'title': '{}派工系統'.format(station_name),
                    'content': '{}維運人員已接單'.format(name),
                }
            },
            'wait_for_dispatch': {
            },
            'dispatched_wait_for_review': {
                3: {
                    'title': '{}派工系統'.format(station_name),
                    'content': '工單{}，等待自動驗收中'.format(name),
                }
            },
            'auto_reviewed_wait_for_manual': {
                3: {
                    'title': '{}派工系統'.format(station_name),
                    'content': '請手動驗收工單{}'.format(name),
                }
            },
            'review_failed': {
                1: {
                    'title': '{}派工系統'.format(station_name),
                    'content': '工單{}驗收失敗'.format(name),
                },
            },
            'dispatch_finish': {
                1: {
                    'title': '{}派工系統'.format(station_name),
                    'content': '工單{}已完成'.format(name),
                },
                3: {
                    'title': '{}派工系統'.format(station_name),
                    'content': '工單{}已完成'.format(name),
                }
            }
        }
    def send(self, stage, to_who='all'):
        self.stage = stage
        self.to_who = to_who
        notify = []
        if stage == 'wait_for_take':
            notify = self.from_stage_get_msg('wait_for_take')
        elif stage == 'wait_for_priority':
            pass
        elif stage == 'took_wait_date_enter':
            notify = self.from_stage_get_msg('took_wait_date_enter')
        elif stage == 'merged':
            pass
        elif stage == 'wait_admin_confirm_date':
            notify = self.from_stage_get_msg('wait_admin_confirm_date')
        elif stage == 'wait_for_dispatch':
            pass
        elif stage == 'dispatched_wait_for_review':
            notify = self.from_stage_get_msg('dispatched_wait_for_review')
        elif stage == 'auto_reviewed_wait_for_manual':
            notify = self.from_stage_get_msg('auto_reviewed_wait_for_manual')
        elif stage == 'review_failed':
            notify = self.from_stage_get_msg('review_failed')
        elif stage == 'dispatch_finish':
            notify = self.from_stage_get_msg('dispatch_finish')
        else:
            notify = self.from_stage_get_msg(stage)
        if notify != None and len(notify) > 0:
            self.db.push_notification.insert_many(notify)
    def from_stage_get_msg(self, stage):
        current_time = datetime.datetime.now()
        if stage not in self.stage_user_level_mag:
            return None
        send_list = []
        db = self.db
        for level in self.stage_user_level_mag[stage]:
            #print(level)
            msg_data = {
                'title': self.stage_user_level_mag[stage][level].get('title', None),
                'content': self.stage_user_level_mag[stage][level]['content'],
                'route': '/dispatch' if level > 1 else '/dispatch_work',
                'rule': "user_list",
                'send_to': [],
                'platform': {
                    'android': True,
                    'ios': True
                },
                'send': False,
                'target_time': current_time,
                'expire_at': current_time + datetime.timedelta(days=1),
                'create_time': current_time
            }
            if self.to_who == 'all':
                for user in db.users.find({'level': level, 'plant': {'$elemMatch':{'$in':['total', self.PV_name]}}}):
                    msg_data['send_to'].append(str(user['_id']))
            elif isinstance(self.to_who, str):
                msg_data['send_to'] = [self.to_who]
            send_list.append(msg_data)
        return send_list
#======================================================================================================
#計算排程區間對應日期
def dispatch_schedule_calculation(repeat:str, repeat_interval:int, _starttime=datetime.datetime.now()):
    if repeat == 'none' or repeat == 'temporary':
        return None
    elif repeat == 'week':
        _starttime += datetime.timedelta(days=7*repeat_interval)
    elif repeat == 'month':
        _starttime += relativedelta.relativedelta(months=1*repeat_interval)
    elif repeat == 'quarter':
        _starttime += relativedelta.relativedelta(months=3*repeat_interval)
    elif repeat == 'half_year':
        _starttime += relativedelta.relativedelta(months=6*repeat_interval)
    elif repeat == 'year':
        _starttime += relativedelta.relativedelta(years=1*repeat_interval)
    return _starttime
#-------------------------------------------------------------------------------
#使用位置 /dispatch 用警報_id取得原因 (AI analysis and manual pick)
@application_dispatch.route('/alarm_id_get_reason', methods=['POST'])
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
class ScheduleData(views.MethodView):
    def post(self):
        user, db = check_user()
        if db == None:
            return logout()
        request_dict = request.json
        try:
            schedule_data = request_dict['schedule_data']
            #print(schedule_data)
        except Exception as e:
            return bad_request(400, 'Bad Request. No schedule_data.')
        try:
            group_data = request_dict['group_data']
            group_data = self.group_data_add_number(group_data)
            #print(group_data)
        except Exception as e:
            return bad_request(400, 'Bad Request. No group_data.')

        try:
            _id = schedule_data['_id']
            name = schedule_data['name']
            repeat = schedule_data['repeat']
            ID = schedule_data['ID']
            schedule_type = schedule_data['schedule_type']
            repeat_interval = schedule_data['repeat_interval']
            # check repeat interval
            if not isinstance(repeat_interval, int):
                return bad_request('Bad Request. repeat_interval format error.')
            else:
                if repeat_interval < 1:
                    return bad_request('Bad Request. repeat_interval smaller than 0.')
            starttime = schedule_data['starttime']
            starttime = datetime.datetime.strptime(starttime, '%Y-%m-%d')

            # _id equals to None, schedule should be not exist
            if _id == None:
                if db.dispatch_schedule.count_documents({'name': name, 'repeat': repeat, 'ID': ID, 'show': 1}) != 0:
                    return bad_request(400, 'Bad Request. Already Exists.')
                # Update to dispatch_schedule database
                _id = db.dispatch_schedule.insert_one({'name': name, 'repeat': repeat, 'ID': ID, 'schedule_type': schedule_type,
                'repeat_interval': repeat_interval, 'start_time': starttime, 'show': 1,
                'group_data': group_data}).inserted_id
                _id = str(_id)
                # Set Calendar
                self.update_calendar(db, _id, ID, repeat, repeat_interval, starttime)                

            # old schedule update
            else:
                try:
                    ObjectId(_id)
                    print('Old Schedule Update: {}'.format(_id))
                except:
                    return bad_request(400, 'Bad Request. _id error')
                # Update to dispatch_schedule database
                db.dispatch_schedule.update_one({'_id': ObjectId(_id)},
                    {'$set':
                        {'name': name, 'repeat': repeat, 'ID': ID, 'schedule_type': schedule_type,
                        'repeat_interval': repeat_interval, 'start_time': starttime, 'show': 1,
                        'group_data': group_data}
                    }
                )
                # Set Calendar
                self.update_calendar(db, _id, ID, repeat, repeat_interval, starttime)    

        except Exception as e:
            print(exception_detail(e))
            return bad_request(400, 'Bad Request. {}'.format(e))       
        return successful_request()
    def update_calendar(self, db, schedule_id, station_ID, repeat, repeat_interval, starttime):
        _starttime = starttime
        dispatch_data = {
            'ID': station_ID,
            'type': 'schedule',
            'schedule_ID': schedule_id,
            'dispatch_time': _starttime,
            'show': 1,
        }
        # remove calendar
        db.dispatch_calendar.delete_many({'schedule_ID': schedule_id})
        # NEW FEATURE will also delete dispatch with stage: wait_for_take
        # after the solar-dispatch-program will create a new one
        db.dispatch.delete_many({'schedule_ID': schedule_id, 'stage': 'wait_for_take'})
        insert_list = []
        while _starttime < datetime.datetime.strptime('2030-01-01', '%Y-%m-%d'):
            dispatch_data['dispatch_time'] = _starttime
            insert_list.append(dispatch_data.copy())
            if repeat == 'none' or repeat == 'temporary':
                break
            else:
                _starttime = dispatch_schedule_calculation(repeat, repeat_interval, _starttime)
        #print(insert_list)
        db.dispatch_calendar.insert_many(insert_list)
        return True
    def group_data_add_number(self, group_data:list):
        for i, group in enumerate(group_data):
            group['number'] = i + 1
            group['number_name'] = '{}. {}'.format(i+1, group.get('name'))
            for ii, child in enumerate(group.get('child', [])):
                child['number'] = ii + 1
                child['number_name'] = '{}-{} {}'.format(i+1, ii+1, child.get('name'))

        return group_data
application_dispatch.add_url_rule('/schedule_data', view_func=ScheduleData.as_view('schedule_data'))
#-------------------------------------------------------------------------------
class GetScheduleOverview(views.MethodView):
    def post(self):
        user, db = check_user()
        if db == None:
            return logout()
        request_dict = request.json
        #print(request_dict)
        dispatch_filter = {'show': 1}
        # Time filter
        if request_dict.get('time', {}).get('mode', '') == 'single':
            try:
                start_date = datetime.datetime.strptime(request_dict['time']['start_date'], '%Y-%m-%d')
                end_date = start_date + datetime.timedelta(days=1)
                dispatch_filter['time'] = {'$gte': start_date, '$lt': end_date}
            except:
                return bad_request(400, 'Time error')
        elif request_dict.get('time', {}).get('mode', '') == 'interval':
            try:
                start_date = datetime.datetime.strptime(request_dict['time']['start_date'], '%Y-%m-%d')
                end_date = datetime.datetime.strptime(request_dict['time']['end_date'], '%Y-%m-%d')
                dispatch_filter['time'] = {'$gte': start_date, '$lt': end_date+datetime.timedelta(days=1)}
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
            dispatch_filter['time'] = {'$gte': start_date, '$lt': end_date}

        # Plant filter
        plant_filter = {}
        find_user = find_user_from_current_user()
        ID = request_dict.get('ID', None)
        user_c=list(db.users.find({"user_id" : find_user}))[0]
        station_dict = {}
        if user_c['plant'][0] != 'total':
            for i in user_c['plant']:
                if 'name' not in plant_filter:
                    plant_filter['name'] = {'$in': []}
                plant_filter['name']['$in'].append(i)
        for plant in db.plant.find(plant_filter):
            for lgroup in db.equipment.find({'PV': plant.get('name', ''), 'type': 'pv_lgroup'}):
                lgroup['place'] = '{}/{}'.format(lgroup.get('PV', ''), lgroup.get('name', ''))
                station_dict[str(lgroup['_id'])] = lgroup
                if ID == None:
                    if 'ID' not in dispatch_filter:
                        dispatch_filter['ID'] = {'$in': []}
                    dispatch_filter['ID']['$in'].append(str(lgroup['_id']))
                elif ID == str(lgroup['_id']):
                    dispatch_filter['ID'] = ID
        #print(dispatch_filter)
        # Pagination
        page = request_dict.get('page', 1)
        if not isinstance(page, int):
            return bad_request(400, 'Bad Request. Page must be int.')
        elif page < 1:
            return bad_request(400, 'Bad Request. Page must be >= 1.')
        # schedule repeat filter
        schedule_repeat = request_dict.get('schedule_repeat', 'all')
        if schedule_repeat != 'all':
            dispatch_filter['repeat'] = schedule_repeat
        return_list = []
        for schedule in db.dispatch_schedule.find(dispatch_filter).limit(10).skip((page-1)*10):
            #print(schedule)
            try:
                schedule['_id'] = str(schedule['_id'])
                schedule['repeat_interval_format'] = c.schedule_interval_format(schedule['repeat'], schedule['repeat_interval'])
                schedule['next_dispatch'] = "---"
                schedule['place'] = station_dict.get(schedule['ID'],{})['place']
                schedule['start_time'] = datetime.datetime.strftime(schedule['start_time'], '%Y-%m-%d')
                for next_dispatch in db.dispatch_calendar.find({'schedule_ID': str(schedule['_id']), 'dispatch_time': {'$gte': datetime.datetime.now()}}).sort('time', 1).limit(1):
                    schedule['next_dispatch'] = datetime.datetime.strftime(next_dispatch['dispatch_time'], '%Y-%m-%d')
                #print(schedule)
                return_list.append(schedule)
            except:
                pass
        
        return successful_request({
            'schedule_list': return_list,
            'current_page': page,
            'total_page': math.ceil(db.dispatch_schedule.count_documents(dispatch_filter)/10)
        })
application_dispatch.add_url_rule('/get_schedule_overview', view_func=GetScheduleOverview.as_view('get_schedule_overview'))
#-------------------------------------------------------------------------------
class GetScheduleData(views.MethodView):
    def post(self):
        user, db = check_user()
        if db == None:
            return logout()
        request_dict = request.json
        #print(request_dict)
        
        try:
            schedule_ID = request_dict['ID']
            ObjectId(schedule_ID)
        except:
            return bad_request(400, 'Bad Request. ID error')

        return_data = {}
        for schedule in db.dispatch_schedule.find({'_id': ObjectId(schedule_ID)}):
            #print(schedule)
            try:
                schedule['_id'] = str(schedule['_id'])
                schedule['repeat_interval_format'] = c.schedule_interval_format(schedule['repeat'], schedule['repeat_interval'])
                schedule['next_dispatch'] = "---"
                schedule['start_time'] = datetime.datetime.strftime(schedule['start_time'], '%Y-%m-%d')
                for next_dispatch in db.dispatch_calendar.find({'schedule_ID': str(schedule['_id']), 'dispatch_time': {'$gte': datetime.datetime.now()}}).sort('time', 1).limit(1):
                    schedule['next_dispatch'] = datetime.datetime.strftime(next_dispatch['dispatch_time'], '%Y-%m-%d')
                #place
                for lgroup in db.equipment.find({'_id': ObjectId(schedule['ID'])}):
                    schedule['place'] = '{}/{}'.format(lgroup['PV'], lgroup['name'])

                # schedule number check
                if schedule.get('group_data', []) == None:
                    schedule['group_data'] = []
                for i, group in enumerate(schedule.get('group_data', [])):
                    if 'number' not in group:
                        group['number'] = i + 1
                        group['number_name'] = '{}. {}'.format(i+1, group.get('name'))
                    for ii, child in enumerate(group.get('child', [])):
                        if 'number' not in child:
                            child['number'] = ii + 1
                            child['number_name'] = '{}-{} {}'.format(i+1, ii+1, child.get('name'))
                    
                
                #print(schedule)
                return_data = schedule
            except Exception as e:
                #print(exception_detail(e))
                pass
        
        return successful_request({
            'schedule_data': return_data
        })
application_dispatch.add_url_rule('/get_schedule_data', view_func=GetScheduleData.as_view('get_schedule_data'))
#-------------------------------------------------------------------------------
class ScheduleDataDelete(views.MethodView):
    def post(self):
        user, db = check_user()
        if db == None:
            return logout()
        request_dict = request.json
        print(request_dict)
        ID = request_dict.get('ID', None)
        if ID == None:
            return successful_request()
        try:
            ObjectId(ID)
        except:
            return bad_request(400, 'Bad Request. ID error.')
        db.dispatch_schedule.update_one({'_id': ObjectId(ID)}, {'$set': {'show': 0}})
        db.dispatch_calendar.delete_many({'schedule_ID': ID})
        db.dispatch.delete_many({'schedule_ID': ID, 'stage': 'wait_for_take'})
        return successful_request()
application_dispatch.add_url_rule('/schedule_data_delete', view_func=ScheduleDataDelete.as_view('schedule_data_delete'))
#-------------------------------------------------------------------------------
# cal_schedule_date
@application_dispatch.route('/cal_schedule_date', methods=['POST'])
def cal_schedule_date():
    request_dist = request.json
    next_dispatch_time = None
    try:
        repeat = request_dist['repeat']
        repeat_interval = request_dist['repeat_interval']
        starttime = request_dist['starttime']
        starttime = datetime.datetime.strptime(starttime, '%Y-%m-%d')
    except Exception as e:
        return bad_request(400, 'Bad Request. {}'.format(e))
    next_dispatch_time = dispatch_schedule_calculation(repeat, repeat_interval, starttime)
    if next_dispatch_time != None:
        next_dispatch_time = datetime.datetime.strftime(next_dispatch_time, '%Y-%m-%d')
    return successful_request({
        'next_dispatch_time': next_dispatch_time
    })
#-------------------------------------------------------------------------------
# Use to get dispatch table
class GetDispatchOverview(views.MethodView):
    def __init__(self) -> None:
        super().__init__()
        self.limit_user_level = 2
    def post(self):
        user, db = check_user()
        if db == None:
            return logout()
        request_dict = request.json
        dispatch_filter = {'show': 1}
        find_user = find_user_from_current_user()
        user_c=list(db.users.find({"user_id" : find_user}))[0]
        # filt by station ID
        plant_filter = {}
        ID = request_dict.get('ID', None)
        station_dict = {}
        if user_c['plant'][0] != 'total':
            for i in user_c['plant']:
                if 'name' not in plant_filter:
                    plant_filter['name'] = {'$in': []}
                plant_filter['name']['$in'].append(i)
        for plant in db.plant.find(plant_filter):
            for lgroup in db.equipment.find({'PV': plant.get('name', ''), 'type': 'pv_lgroup'}):
                lgroup['place'] = '{}/{}'.format(lgroup.get('PV', ''), lgroup.get('name', ''))
                station_dict[str(lgroup['_id'])] = lgroup
                if ID == None:
                    if 'ID' not in dispatch_filter:
                        dispatch_filter['ID'] = {'$in': []}
                    dispatch_filter['ID']['$in'].append(str(lgroup['_id']))
                elif ID == str(lgroup['_id']):
                    dispatch_filter['ID'] = ID

        # dispatch_time
        dispatch_time = request_dict.get('dispatch_time', None)
        dispatch_time = date_range_interval_to_filter(dispatch_time)
        if dispatch_time[0] == False:
            return dispatch_time[1]
        dispatch_filter['dispatch_time'] = dispatch_time[1] 
        # no dispatch
        # a dispatch having merge_list can not be merged by other dispatch
        no_merge = request_dict.get('no_merge', False)
        if no_merge:
            dispatch_filter['merge_list'] = []
            dispatch_filter['stage'] = {'$ne': 'merged'}
        # stage filter
        stage_filter = request_dict.get('stage', None)
        if stage_filter != None:
            if isinstance(stage_filter, str):
                dispatch_filter['stage'] = stage_filter
            elif isinstance(stage_filter, list):
                dispatch_filter['stage'] = {'$in': stage_filter}
        #print(dispatch_filter)
        # pagnation
        try:
            page = request_dict.get('page', 1)
            page = int(page)
        except:
            return bad_request(400, 'Bad Request.')
        # user filter
        if user_c['level'] < self.limit_user_level:
            dispatch_filter['maintainer_ID'] = {'$in': [None, str(user_c['_id'])]}
        #sort
        _sort = request_dict.get('sort', None)
        if _sort == None:
            sort = [('dispatch_time', 1)]
        else:
            sort = []
            for key in _sort:
                sort.append((key, _sort[key]))
        #skip dispatch_ID
        try:
            if 'dispatch_ID' in request_dict:
                dispatch_filter['_id'] = {'$nin': [ObjectId(request_dict['dispatch_ID'])]}
        except Exception as e:
            return bad_request(400, 'Bad Request. {}'.format(exception_detail(e)))
        # dispatch_time None also be obtained, when dispatch_time specify 
        #should last in filter
        if request_dict.get('dispatch_time_none') == True:
            _dispatch_filter = dispatch_filter.copy()
            _dispatch_filter['dispatch_time'] = None
            dispatch_filter = {'$or': [dispatch_filter, _dispatch_filter]}
        #return data
        return self.get_dispatch_data(db, dispatch_filter, page, station_dict, sort)
        
    def get_dispatch_data(self, db, dispatch_filter, page, station_dict, sort=[('dispatch_time', 1)]):
        dispatch_list = []
        #print(dispatch_filter)
        for dispatch in db.dispatch.find(dispatch_filter, {
            '_id': 1, 'dispatch_time': 1, 'maintainer_ID': 1, 'ID': 1,
            'type': 1, 'stage': 1, 'name': 1, 'merge_list': 1, 
            'predict_dispatch_cost': 1, 'auto_review_cost': 1
        }).skip((page-1)*10).limit(10).sort(sort):
            try:
                dispatch['_id'] = str(dispatch['_id'])
                dispatch['place'] = station_dict[dispatch['ID']].get('place', '')
                # date strftime
                if dispatch.get('dispatch_time', None):
                    dispatch['dispatch_time'] = datetime.datetime.strftime(dispatch['dispatch_time'], '%Y-%m-%d')
                #maintainer data
                maintainer_ID = dispatch.get('maintainer_ID', None)
                dispatch['maintainer_data'] = {
                    'name': '',
                    'tel': ''
                }
                if maintainer_ID != None:
                    maintainer_data = db.users.find_one({'_id': ObjectId(maintainer_ID)})
                    if isinstance(maintainer_data, dict) and 'user_data' in maintainer_data:
                        dispatch['maintainer_data'] = maintainer_data['user_data']
                #merge_dispatch
                dispatch['type'] = dispatch['type']
                dispatch_list.append(dispatch)
                #print(dispatch)
            except Exception as e:
                print(exception_detail(e))
                pass
        return successful_request({
            'dispatch_list': dispatch_list,
            'total_page': math.ceil(db.dispatch.count_documents(dispatch_filter)/10),
            'current_page': page
        })

application_dispatch.add_url_rule('/get_dispatch_overview', view_func=GetDispatchOverview.as_view('get_dispatch_overview'))
#-------------------------------------------------------------------------------
class GetDispatchOverviewCount(GetDispatchOverview):
    def get_dispatch_data(self, db, dispatch_filter, page, station_dict, sort):
        return successful_request({
            'dispatch_count': db.dispatch.count_documents(dispatch_filter),
        })
application_dispatch.add_url_rule('/get_disaptch_overview_count', view_func=GetDispatchOverviewCount.as_view('get_dispatch_overview_count'))
#-------------------------------------------------------------------------------
#get dispatch for calendar
class GetDispatchOverviewCalendar(views.MethodView):
    def __init__(self) -> None:
        super().__init__()
        self.limit_user_level = 2
    def post(self):
        user, db = check_user()
        if db == None:
            return logout()
        request_dict = request.json
        try:
            month = datetime.datetime.strptime(request_dict['month'], '%Y-%m')
            #print(month)
        except Exception as e:
            return bad_request(400, 'Bad Request. {}'.format(exception_detail(e)))
        find_user = find_user_from_current_user()
        user_c=list(db.users.find({"user_id" : find_user}))[0]
        return_dict = {}
        dispatch_filter = {'stage': {'$nin': ['merged']}, 'dispatch_time': {
            '$gte': month - datetime.timedelta(days=7),
            '$lt': month + datetime.timedelta(days=37),
        }}
        if user_c.get('level', 1) < self.limit_user_level:
            dispatch_filter['maintainer_ID'] = str(user_c.get('_id'))
        #plant_filter
        plant_filter = {}
        if user_c['plant'][0] != 'total':
            for i in user_c['plant']:
                if 'name' not in plant_filter:
                    plant_filter['name'] = {'$in': []}
                plant_filter['name']['$in'].append(i)
        for plant in db.plant.find(plant_filter):
            for lgroup in db.equipment.find({'PV': plant.get('name', ''), 'type': 'pv_lgroup'}):
                lgroup['place'] = '{}/{}'.format(lgroup.get('PV', ''), lgroup.get('name', ''))
                if 'ID' not in dispatch_filter:
                    dispatch_filter['ID'] = {'$in': []}
                dispatch_filter['ID']['$in'].append(str(lgroup['_id']))
        for dispatch in db.dispatch.find(dispatch_filter):
            try:
                if dispatch.get('dispatch_time', None) != None:
                    # dispatch having time
                    #print(dispatch)
                    dispatch['_id'] = str(dispatch['_id'])
                    dispatch['type'] = dispatch['type']
                    """ for merge_ID in dispatch.get('merge_list', []):
                        try:
                            merge_type = db.dispatch.find_one({'_id': ObjectId(merge_ID)})['type']
                            if  merge_type not in dispatch['type']:
                                dispatch['type'].append(merge_type)
                        except:
                            pass """
                    date_fix = datetime.datetime.strftime(dispatch['dispatch_time'], '%m-%d')
                    if date_fix not in return_dict:
                        return_dict[date_fix] = {
                            'date': date_fix,
                            'child': [],
                            'count': {
                                'alarm': 0,
                                'regular': 0,
                                'wash': 0,
                                'schedule': 0
                            }
                        }
                    # station name
                    station_data = db.equipment.find_one({'_id': ObjectId(dispatch['ID'])})
                    # maintainer name
                    maintainer_name = '---'
                    if dispatch['stage'] != 'wait_for_take':
                        try:
                            for u in db.users.find({'_id': ObjectId(dispatch['maintainer_ID'])}):
                                maintainer_name = u['user_data']['name']
                        except:
                            pass
                    return_dict[date_fix]['child'].append({
                        'collection': 'dispatch',
                        'station_name': '{}/{}'.format(station_data['PV'], station_data['name']),
                        '_id': dispatch['_id'],
                        'type': dispatch['type'],
                        'name': dispatch['name'],
                        'stage': dispatch['stage'],
                        'maintainer_name': maintainer_name
                    })
                    for t in return_dict[date_fix]['count']:
                        if t in dispatch['type']:
                            return_dict[date_fix]['count'][t] += 1
            except Exception as e:
                print(exception_detail(e))
        if user_c.get('level', 1) >= self.limit_user_level:
            for schedule in db.dispatch_calendar.find({
                'dispatch_time': {
                    '$gte': month - datetime.timedelta(days=7),
                    '$lt': month + datetime.timedelta(days=37),
                },
                'show': 1,
                'dispatch_create': {'$exists': False}
            }): 
                try:
                    if schedule.get('dispatch_time', None) != None:
                        #print(schedule)
                        schedule['_id'] = str(schedule['_id'])
                        date_fix = datetime.datetime.strftime(schedule['dispatch_time'], '%m-%d')
                        if date_fix not in return_dict:
                            return_dict[date_fix] = {
                                'date': date_fix,
                                'child': [],
                                'count': {
                                    'alarm': 0,
                                    'regular': 0,
                                    'wash': 0,
                                    'schedule': 0
                                }
                            }
                        # station name
                        station_data = db.equipment.find_one({'_id': ObjectId(schedule['ID'])})
                        schedule_data = db.dispatch_schedule.find_one({'_id': ObjectId(schedule['schedule_ID'])})
                        return_dict[date_fix]['child'].append({
                            'collection': 'dispatch_calendar',
                            'station_name': '{}/{}'.format(station_data['PV'], station_data['name']),
                            '_id': schedule['_id'],
                            'schedule_id': str(schedule_data['_id']),
                            'type': [schedule_data['schedule_type']],
                            'name': schedule_data['name']
                        })
                        return_dict[date_fix]['count']['schedule'] += 1
                except Exception as e:
                    print(exception_detail(e))
            
        return successful_request({
            'data': return_dict
        })
application_dispatch.add_url_rule('/get_dispatch_overview_calendar', view_func=GetDispatchOverviewCalendar.as_view('get_dispatch_overview_calendar'))
#-------------------------------------------------------------------------------
# get dispatch data by _id
class GetDispatchData(views.MethodView):
    def post(self):
        user, db = check_user()
        if db == None:
            return logout()
        request_dict = request.json
        try:
            ID = request_dict['ID']
            ObjectId(ID)
        except:
            return bad_request(400, 'Bad Request. ID error.')

        #get dispatch data
        return_dict = {}
        for dispatch in db.dispatch.find({'_id': ObjectId(ID)}):
            dispatch['_id'] = str(dispatch['_id'])
            #get station data
            dispatch['station_data'] = {}
            for equip in db.equipment.find({'_id': ObjectId(dispatch['ID'])}):
                equip['_id'] = str(equip['_id'])
                equip['plant_data'] = {}
                for plant in db.plant.find({'name': equip.get('PV', '')}):
                    plant['_id'] = str(plant['_id'])
                    if plant.get('start_date', None) != None:
                        plant['start_date'] = datetime.datetime.strftime(plant['start_date'], '%Y-%m-%d')
                    equip['plant_data'] = plant
                dispatch['station_data'] = equip
            #time strftime
            if dispatch.get('dispatch_time', None) != None:
                dispatch['dispatch_time'] = datetime.datetime.strftime(dispatch['dispatch_time'], '%Y-%m-%d')
            #maintainer data
            maintainer_ID = dispatch.get('maintainer_ID', None)
            dispatch['maintainer_data'] = {
                'name': '',
                'tel': ''
            }
            if maintainer_ID != None:
                maintainer_data = db.users.find_one({'_id': ObjectId(maintainer_ID)})
                if 'user_data' in maintainer_data:
                    dispatch['maintainer_data'] = maintainer_data['user_data']
            #alarm_data
            if 'alarm' in dispatch['type']:
                dispatch['alarm_list'] = self.get_alarm_cause(db, dispatch['_id'], dispatch.get('alarm_list', []))
            #regular_data
            if 'regular' in  dispatch['type']:
                dispatch['regular_list'] = self.get_regular_wash_list(dispatch['_id'], dispatch.get('regular_list', []))
            #wash_data
            if 'wash' in dispatch['type']:
                dispatch['wash_list'] = self.get_regular_wash_list(dispatch['_id'], dispatch.get('wash_list', []))
            #print(dispatch)
            return_dict = dispatch

        return successful_request({
            'dispatch_data': return_dict
        })
    def get_alarm_cause(self, db, dispatch_ID, alarm_list):
        return_list = []
        for alarm_dict in alarm_list:
            try:
                for alarm in db.alarm.find({'_id': ObjectId(alarm_dict['ID'])}):
                    alarm['dispatch_ID'] = dispatch_ID
                    alarm['_id'] = str(alarm['_id'])
                    #get equip data
                    equip_type = ''
                    equip_name = ''
                    system_translate = {"DG": "DG","PV": "地面型","BESS": "屋頂型","WT": "水面型"}
                    type_translate = {"inv": "變流器", "string": "串電流錶", "io": "開關", "sun": "日照計", 
                    "temp": "溫度計", "wind": "風速計", "meter": "智慧電錶", "pv_meter": "智慧電錶"}
                    _data = db.plant.find_one({'_id': ObjectId(alarm['ID'])})
                    if _data != None:
                        equip_type = '案場'
                        equip_name = _data.get('name', '')
                    else:
                        _data = db.iot.find_one({'_id': ObjectId(alarm['ID'])})
                        if _data != None:
                            equip_type = '資料收集器'
                            equip_name = _data.get('name',  '資料收集器')
                        else:
                            _data = db.equipment.find_one({'_id': ObjectId(alarm['ID'])})
                            equip_name = _data.get('name',  '')
                            if _data.get('type') == 'pv_lgroup':
                                equip_type = '分區' if _data.get('Devide_type', '') == '' else type_translate.get(_data.get('Device_type', ''), _data.get('Device_type', ''))
                            elif _data.get('type') == 'pv_group':
                                equip_type = '分組' if _data.get('Devide_type', '') == '' else type_translate.get(_data.get('Device_type', ''), _data.get('Device_type', ''))
                            else:
                                equip_type = type_translate.get(_data.get('type', ''), _data.get('type', ''))
                    
                    alarm['equip_name'] = equip_name
                    alarm['equip_type'] = equip_type
                    alarm['cause_data'] = {
                        'ai_analysis': [],
                        'user_select': []
                    }
                    for cause_ID in alarm_dict.get('cause', {}):
                        #print(cause_ID)
                        # photo to pathname
                        alarm_dict['cause'][cause_ID]['photo_data'] = []
                        for filename in alarm_dict['cause'][cause_ID].get('photo', []):
                            alarm_dict['cause'][cause_ID]['photo_data'].append({
                                'filename': filename,
                                'filepath': "solar_static/dispatch/{}/{}/{}/{}".format(
                                    dispatch_ID, alarm['_id'], cause_ID, filename
                                ) 
                            })
                        if cause_ID == "else":    #其他事項
                            alarm_dict['cause']['else']['group'] = '其他'
                            alarm_dict['cause']['else']['event'] = '其他'
                            alarm['cause_data']['user_select'].append(alarm_dict['cause']['else'])
                            continue   # Skip for searching db
                        for cause in db.alarm_cause.find({'_id': ObjectId(cause_ID)}):
                            #print(cause)
                            alarm_dict['cause'][cause_ID]['group'] = cause['alarm_group']
                            alarm_dict['cause'][cause_ID]['event'] = cause['event']
                            alarm['cause_data']['user_select'].append(alarm_dict['cause'][cause_ID])
                    # sorting 
                    # place else in last place
                    new_user_select = []
                    for cause in alarm['cause_data']['user_select']:
                        if cause['group'] == '其他':
                            new_user_select.append(cause)
                        else:
                            _new_user_select = [cause]
                            _new_user_select.extend(new_user_select)
                            new_user_select = _new_user_select
                    alarm['cause_data']['user_select'] = new_user_select
                    #print(alarm)
                    #time fix
                    try:
                        alarm['time'] = datetime.datetime.strftime(alarm['time'], '%Y-%m-%d %H:%M:%S')
                    except:
                        pass
                    try:
                        alarm['returntime'] = datetime.datetime.strftime(alarm['returntime'], '%Y-%m-%d %H:%M:%S')
                    except:
                        alarm['returntime'] = '---'
                        pass
                    return_list.append(alarm)
            except Exception as e:
                print(exception_detail(e))
                pass
        return return_list
    def get_regular_wash_list(self, dispatch_ID, group_list):
        for group in group_list:
            try:
                group['dispatch_ID'] = dispatch_ID
                for child_name in group['child']:
                    # photo to pathname
                    group['child'][child_name]['photo_data'] = []
                    for filename in group['child'][child_name].get('photo', []):
                        group['child'][child_name]['photo_data'].append({
                            'filename': filename,
                            'filepath': "solar_static/dispatch/{}/{}/{}/{}".format(
                                dispatch_ID, group['name'], child_name, filename
                            ) 
                        })
            except Exception as e:
                print(exception_detail(e))
        return group_list
application_dispatch.add_url_rule('/get_dispatch_data', view_func=GetDispatchData.as_view('get_dispatch_data'))
#-------------------------------------------------------------------------------
@application_dispatch.route('/get_dispatch_archive_data', methods=['POST'])
def get_dispatch_archive_data():
    user, db = check_user()
    if db == None:
        return logout()
    request_dict = request.json
    dispatch_filter = {'show': 1}
    find_user = find_user_from_current_user()
    user_c=list(db.users.find({"user_id" : find_user}))[0]
    # filt by station ID
    plant_filter = {}
    ID = request_dict.get('ID', None)
    station_dict = {}
    equip_data = {}
    if user_c['plant'][0] != 'total':
        for i in user_c['plant']:
            if 'name' not in plant_filter:
                plant_filter['name'] = {'$in': []}
            plant_filter['name']['$in'].append(i)
    for plant in db.plant.find(plant_filter):
        for lgroup in db.equipment.find({'PV': plant.get('name', ''), 'type': 'pv_lgroup'}):
            lgroup['place'] = '{}/{}'.format(lgroup.get('PV', ''), lgroup.get('name', ''))
            station_dict[str(lgroup['_id'])] = lgroup
            if ID == None:
                if 'ID' not in dispatch_filter:
                    dispatch_filter['ID'] = {'$in': []}
                dispatch_filter['ID']['$in'].append(str(lgroup['_id']))
            elif ID == str(lgroup['_id']):
                dispatch_filter['ID'] = ID
            equip_data[str(lgroup['_id'])] = lgroup
            for equip in db.equipment.find({'PV': lgroup.get('PV'), 'lgroup': lgroup.get('name')}):
                equip_data[str(equip['_id'])] = equip
    # dispatch_time
    dispatch_time = request_dict.get('dispatch_time', None)
    dispatch_time = date_range_interval_to_filter(dispatch_time)
    if dispatch_time[0] == False:
        return dispatch_time[1]
    dispatch_filter['dispatch_time'] = dispatch_time[1]
    sequence_diagram_overview = True
    if '$gte' in dispatch_filter['dispatch_time'] and '$lt' in dispatch_filter['dispatch_time']:
        try:
            if (dispatch_filter['dispatch_time']['$lt'] - dispatch_filter['dispatch_time']['$gte']).days < 32 :
                sequence_diagram_overview = False
        except:
            pass
    dispatch_filter['stage'] = 'dispatch_finish'
    dispatch_data = list(db.dispatch.find(dispatch_filter))
    station_dispatch_count = {}
    dispatch_type_stat = {
        'alarm': 0,
        'regular': 0,
        'wash': 0
    }
    auto_review_cost_total = 0
    sequence_data = []
    alarm_pie_sort = {'非變流器通信異常': 0, '變流器通信異常': 0}
    total_alarm_count = 0
    for dispatch in dispatch_data:
        try:
            if dispatch.get('ID') not in station_dispatch_count:
                station_dispatch_count[dispatch.get('ID')] = {
                    'name': '{}/{}'.format(station_dict.get(dispatch.get('ID'), {}).get('PV'),
                        station_dict.get(dispatch.get('ID'), {}).get('name')),
                    'count': 0
                }
            station_dispatch_count[dispatch.get('ID')]['count'] += 1
            # type stat
            for key in dispatch_type_stat:
                if key in dispatch.get('type', []):
                    dispatch_type_stat[key] += 1
            try:
                auto_review_cost_total += dispatch['auto_review_cost']
            except:
                pass
            #sequence_diagram
            start_time = dispatch.get('dispatch_time')
            end_time = dispatch.get('finish_time')
            try:
                start_time = end_time - datetime.timedelta(hours=dispatch['working_data'][-1]['working_hour'])
            except: 
                pass
            start_time = datetime.datetime.strftime(start_time, '%Y-%m-%d %H:%M')
            end_time = datetime.datetime.strftime(end_time, '%Y-%m-%d %H:%M')
            if not sequence_diagram_overview:
                sequence_data.append({
                    'x': [start_time, end_time],
                    'y': [dispatch['name'], dispatch['name']],
                    'name': dispatch['name'],
                    'overview': False
                })
            else:
                month = start_time[0:7]
                sequence_data.append({
                    'x': [start_time, end_time],
                    'y': ['{}工單總覽'.format(month), '{}工單總覽'.format(month)],
                    'name': dispatch['name'],
                    'overview': True
                })
            #alarm pie
            if 'alarm_list' in dispatch:
                for a in dispatch['alarm_list']:
                    for alarm in db.alarm.find({'_id': ObjectId(a.get('ID'))}):
                        total_alarm_count += 1
                        if (alarm.get('group') == '軟體' and '斷線' in alarm.get('event', '')) or alarm.get('group') == '斷線':
                            if equip_data.get(alarm.get('ID'), {}).get('type', '') == 'inv':
                                alarm_pie_sort['變流器通信異常'] += 1
                            else:
                                alarm_pie_sort['非變流器通信異常'] += 1
                        else:
                            type_translate = {"inv": "變流器", "string": "串電流錶", "io": "開關", "sun": "日照計", 
                            "temp": "溫度計", "wind": "風速計", "meter": "智慧電錶", "pv_meter": "智慧電錶"}
                            equip_type = type_translate.get(
                                equip_data.get(alarm.get('ID'), {}).get('type', ''), 
                                type_translate.get(
                                    equip_data.get(alarm.get('ID'), {}).get('Device_type', ''), ''
                                ))
                            event_name = alarm.get('event', '')
                            if equip_type not in event_name:
                                event_name = '{}{}'.format(equip_type, event_name)
                            if event_name not in alarm_pie_sort:
                                alarm_pie_sort[event_name] = 0
                            alarm_pie_sort[event_name] += 1
        except:
            pass

    #alarm pie process
    alarm_pie_data = {
        'labels': [],
        'values': [],
        'type': 'pie'
    }
    try:
        for key in alarm_pie_sort:
            alarm_pie_data['labels'].append(key)
            alarm_pie_data['values'].append(round(alarm_pie_sort[key]/total_alarm_count*100, 2))
    except:
        pass
    return successful_request({
        'select_station_name': 'all' if ID == None else '{}/{}'.format(station_dict.get(ID, {}).get('PV'),
            station_dict.get(ID, {}).get('name')),
        'station_dispatch_count': station_dispatch_count,
        'dispatch_type_stat': dispatch_type_stat,
        'total_dispatch_count': len(dispatch_data),
        'auto_review_cost_total': auto_review_cost_total,
        'sequence_data': sequence_data,
        'alarm_pie_data': alarm_pie_data,
        'no_alarm': True if total_alarm_count == 0 else False
    })
#-------------------------------------------------------------------------------
class CreateDispatchSave(views.MethodView):
    def post(self):
        user, db = check_user()
        if db == None:
            return logout()
        request_dict = request.json
        #print(request_dict)
        try:
            ID = request_dict['ID']
            alarm_list = request_dict['alarm_data']
            merge_list = []
            dispatch_time = request_dict.get('dispatch_date', None)
            if dispatch_time != None:
                dispatch_time = datetime.datetime.strptime(dispatch_time, '%Y-%m-%d')
            # check merged dispatch also having merge_list
            for merge_ID in request_dict['merge_dispatch']:
                try:
                    merge_list.append(merge_ID)
                    dispatch_data = db.dispatch.find_one({'_id': ObjectId(merge_ID)})
                    if 'merge_list' in dispatch_data:
                        for i in dispatch_data['merge_list']:
                            if i not in merge_list:
                                merge_list.append(i)
                except:
                    pass

            # dispatch_name
            station_data = db.equipment.find_one({'_id': ObjectId(ID)})
            dispatch_name = "{}/{}-".format(station_data.get('PV'), station_data.get('name'))
            this_month = c.month_interval()[0]
            dispatch_name += datetime.datetime.strftime(this_month, '%Y%m')
            dispatch_count = db.dispatch.count_documents({'ID': ID, 'init_time': {'$gte': this_month}})
            dispatch_count += 1
            dispatch_name += '-{}{}'.format(''.join(['0' for i in range(5-len(str(dispatch_count)))]), dispatch_count)
            dispatch = {
                'name': dispatch_name,
                'ID': ID,
                'init_time': datetime.datetime.now(),
                'last_change_time': datetime.datetime.now(),
                'dispatch_time': dispatch_time,
                'type': ['alarm'],
                'alarm_list': alarm_list,
                'merge_list': merge_list,
                'show': 1,
                'stage': 'wait_for_take',
                'working_data': [],
                'maintainer_ID': None
            }

            # set merged dispatch's stage to 'merged'
            for merge_ID in merge_list:
                for merge_dispatch in db.dispatch.find({'_id': ObjectId(merge_ID)}):
                    if merge_dispatch['type'] not in dispatch['type']:
                        dispatch['type'].append(merge_dispatch['type'] )
                    if 'alarm_list' in merge_dispatch:
                        dispatch['alarm_list'].extend(merge_dispatch['alarm_list'])
                    if 'regular_list' in merge_dispatch:
                        if 'regular_list' in dispatch:
                            dispatch['regular_list'].extend(merge_dispatch['regular_list'])
                        else:
                            dispatch['regular_list'] = merge_dispatch['regular_list']
                    if 'wash_list' in merge_dispatch:
                        if 'wash_list' in dispatch:
                            dispatch['wash_list'].extend(merge_dispatch['wash_list'])
                        else:
                            dispatch['wash_list'] = merge_dispatch['wash_list']
                    db.dispatch.update_one({'_id': ObjectId(merge_ID)}, {'$set': {
                        'stage': 'merged', 'dispatch_time': dispatch_time, 'last_change_time': datetime.datetime.now()}})
            dispatch['predict_dispatch_cost'] = 0
            if 'alarm_list' in dispatch:
                repair_equip_ID_list = []
                for alarm in dispatch['alarm_list']:
                    for a in db.alarm.find({'_id': ObjectId(alarm['ID'])}):
                        if 'ID' in a and a['ID'] not in repair_equip_ID_list:
                            repair_equip_ID_list.append(a['ID'])
                            dispatch['predict_dispatch_cost'] += self.get_repair_cost(db, ID, alarm)
            result = db.dispatch.insert_one(dispatch)
            dispatch_ID = result.inserted_id
            # set alarm dispatch_ID
            for alarm in alarm_list:
                db.alarm.update_one({'_id': ObjectId(alarm['ID'])}, {'$set': {'dispatch_ID': str(dispatch_ID)}})
        except Exception as e:
            print(exception_detail(e))
            return bad_request(400, 'Bad Request. Due to {}'.format(exception_detail(e)))
        return successful_request()
    def get_repair_cost(self, db, lgroup_ID, alarm):
        alarm_data = db.alarm.find_one({'_id': ObjectId(alarm.get('ID'))})
        equip_data = db.equipment.find_one({'_id': ObjectId(alarm_data['ID'])})
        iot_data = db.iot.find_one({'_id': ObjectId(alarm_data['ID'])})
        # Get replace data
        equip_type = None
        equip_model = None
        if equip_data != None:
            if 'lgroup' in equip_data:
                equip_type = equip_data.get('type') if equip_data.get('Device_type') != 'sensor' else 'sensor' 
            elif equip_data.get('type') == 'pv_lgroup':
                equip_type = 'meter'
            if 'Device_model' in equip_data:
                equip_model = equip_data.get('Device_model', '---')
        elif iot_data != None:
            equip_type = 'iot'
            equip_model = iot_data.get('Device_model', '---')
        equip_parameter = db.dispatch_parameter.find_one({'ID': lgroup_ID, 'type': equip_type,
        'model': equip_model})
        if equip_parameter != None and 'dispatch_cost' in equip_parameter:
            return equip_parameter.get('dispatch_cost', 0)
        return 0
application_dispatch.add_url_rule('/create_dispatch_save', view_func=CreateDispatchSave.as_view('create_dispatch_save'))
#-------------------------------------------------------------------------------
class DispatchPhotoSave(views.MethodView):
    def post(self):
        user, db = check_user()
        if db == None:
            return logout()
        #print(request.files)
        #print(request.form)
        if request.form['type'] == 'alarm':
            return self.alarm_photo_save(db)
        elif request.form['type'] in ['regular', 'wash']:
            return self.schedule_photo_save(db, request.form['type'])
    def alarm_photo_save(self, db):
        try:
            for i in request.files:
                file = request.files[i]
                #print(file)
                if file and self.allowed_file(file.filename):
                    filename = secure_filename(file.filename)
                    #print(filename)
                    dirPath = current_app.config['UPLOAD_FOLDER'] + "/dispatch/{}/{}/{}".format(
                        request.form['dispatch_ID'], request.form['alarm_ID'], request.form['cause_ID']) 
                    try:
                        os.makedirs(dirPath)
                        print("Directory " , dirPath ,  " Created ")    
                    except FileExistsError:
                        print("Directory " , dirPath ,  " already exists")
                    file.save(dirPath+"/"+filename)
                for dispatch in db.dispatch.find({'_id': ObjectId(request.form['dispatch_ID'])}):
                    for i in dispatch.get('alarm_list', []):
                        if i.get('ID') == request.form['alarm_ID']:
                            try:
                                if 'photo' not in i["cause"][request.form['cause_ID']]:
                                    i["cause"][request.form['cause_ID']]['photo'] = []
                                if filename not in i["cause"][request.form['cause_ID']]['photo']:
                                    i["cause"][request.form['cause_ID']]['photo'].append(filename)
                            except Exception as e:
                                print(exception_detail(e))
                    db.dispatch.update_one({'_id': ObjectId(request.form['dispatch_ID'])}, {'$set': {'alarm_list': dispatch['alarm_list']}})
        except Exception as e:
            print(exception_detail(e))
            return bad_request(400, 'Bad Request. {}'.format(exception_detail(e)))
        return successful_request({
            'filename': filename,
            'filepath': "solar_static/dispatch/{}/{}/{}/{}".format(
                request.form['dispatch_ID'], request.form['alarm_ID'], request.form['cause_ID'], filename) 
        })
    def schedule_photo_save(self, db, dispatch_type):
        try:
            for i in request.files:
                file = request.files[i]
                #print(file)
                if file and self.allowed_file(file.filename):
                    filename = secure_filename(file.filename)
                    #print(filename)
                    dirPath = current_app.config['UPLOAD_FOLDER'] + "/dispatch/{}/{}/{}".format(
                        request.form['dispatch_ID'], request.form['group_name'], request.form['child_name']) 
                    try:
                        os.makedirs(dirPath)
                        print("Directory " , dirPath ,  " Created ")    
                    except FileExistsError:
                        print("Directory " , dirPath ,  " already exists")
                    file.save(dirPath+"/"+filename)
                for dispatch in db.dispatch.find({'_id': ObjectId(request.form['dispatch_ID'])}):
                    for i in dispatch.get('{}_list'.format(dispatch_type), []):
                        if i.get('name') == request.form['group_name']:
                            try:
                                if 'photo' not in i["child"][request.form['child_name']]:
                                    i["child"][request.form['child_name']]['photo'] = []
                                if filename not in i["child"][request.form['child_name']]['photo']:
                                    i["child"][request.form['child_name']]['photo'].append(filename)
                            except Exception as e:
                                print(exception_detail(e))
                    db.dispatch.update_one({'_id': ObjectId(request.form['dispatch_ID'])}, {'$set': {'{}_list'.format(dispatch_type): dispatch['{}_list'.format(dispatch_type)]}})
        except Exception as e:
            print(exception_detail(e))
            return bad_request(400, 'Bad Request. {}'.format(exception_detail(e)))
        return successful_request({
            'filename': filename,
            'filepath': "solar_static/dispatch/{}/{}/{}/{}".format(
                request.form['dispatch_ID'], request.form['group_name'], request.form['child_name'], filename) 
        })
    def allowed_file(self, filename):
        return '.' in filename and \
            filename.rsplit('.', 1)[1] in set(['png', 'PNG', 'jpg', 'JPG', 'jpeg', 'JPEG'])
application_dispatch.add_url_rule('/dispatch_photo_save', view_func=DispatchPhotoSave.as_view('dispatch_photo_save'))
#-------------------------------------------------------------------------------
class DispatchPhotoRemove(views.MethodView):
    def post(self):
        user, db = check_user()
        if db == None:
            return logout()
        request_dict = request.json
        try:
            filename = request_dict['filename']
            dispatch_ID = request_dict['dispatch_ID']
            dispatch_type = request_dict['type']
            print(filename, dispatch_ID, dispatch_type)
            for dispatch in db.dispatch.find({'_id': ObjectId(dispatch_ID)}):
                if dispatch_type == 'alarm' and 'alarm_list' in dispatch:
                    alarm_ID = request_dict['group_ID']
                    cause_ID = request_dict['child_ID']
                    for i in dispatch.get('alarm_list', []):
                        if i.get('ID') == alarm_ID:
                            try:
                                if filename in i["cause"][cause_ID]['photo']:
                                    i["cause"][cause_ID]['photo'].remove(filename)
                            except Exception as e:
                                print(exception_detail(e))
                    db.dispatch.update_one({'_id': ObjectId(dispatch_ID)}, {'$set': {'alarm_list': dispatch['alarm_list']}})
                elif dispatch_type in ['wash', 'regular'] and '{}_list'.format(dispatch_type):
                    group_name = request_dict['group_ID']
                    child_name = request_dict['child_ID']
                    for i in dispatch.get( '{}_list'.format(dispatch_type), []):
                        if i.get('name') == group_name:
                            try:
                                if filename in i["child"][child_name]['photo']:
                                    i["child"][child_name]['photo'].remove(filename)
                            except Exception as e:
                                print(exception_detail(e))
                    db.dispatch.update_one({'_id': ObjectId(dispatch_ID)}, {'$set': {'{}_list'.format(dispatch_type): dispatch['{}_list'.format(dispatch_type)]}})
        except Exception as e:
            print(exception_detail(e))
        return successful_request()
            
        
application_dispatch.add_url_rule('/dispatch_photo_remove', view_func=DispatchPhotoRemove.as_view('dispatch_photo_remove'))
#-------------------------------------------------------------------------------
class DispatchTake(views.MethodView):
    def post(self):
        user, db = check_user()
        if db == None:
            return logout()
        request_dict = request.json
        dispatch_filter = {'show': 1}
        find_user = find_user_from_current_user()
        user_c=list(db.users.find({"user_id" : find_user}))[0]
        request_dict = request.json
        try:
            ID = request_dict['ID']
            ObjectId(ID)
        except:
            return bad_request(400, 'Bad Request. ID error')
        #print(find_user)
        for dispatch in db.dispatch.find({'_id': ObjectId(ID)}):
            if 'working_data' not in dispatch:
                dispatch['working_data'] = []
            dispatch['working_data'].append({
                'maintainer_ID': str(user_c['_id']),
                'take_time': datetime.datetime.now(),
                'transit':{
                    'start_address': None,
                    'position_id': None,
                    'fee': None
                },
                'summary': None,
            })
            db.dispatch.update_one({'_id': ObjectId(ID)}, {'$set': 
                {'maintainer_ID': str(user_c['_id']), 'working_data': dispatch['working_data'],
                'stage': 'took_wait_date_enter' if dispatch['dispatch_time'] == None else 'wait_for_dispatch'}
            })
            if dispatch['dispatch_time'] == None:
                push_notify = DispatchPushNotification(db, ID, dispatch.get('name', ''), dispatch.get('ID', ''))
                push_notify.send('took_wait_date_enter')
            else:
                push_notify = DispatchPushNotification(db, ID, dispatch.get('name', ''), dispatch.get('ID', ''))
                push_notify.send('take_to_wait_for_dispatch')
        return successful_request()
application_dispatch.add_url_rule('/dispatch_take', view_func=DispatchTake.as_view('dispatch_take'))
#-------------------------------------------------------------------------------
class DispatchUpdateStage(views.MethodView):
    def post(self):
        user, db = check_user()
        if db == None:
            return logout()
        request_dict = request.json
        # ID validate
        try:
            ID = request_dict['ID']
            ObjectId(ID)
        except:
            return bad_request(400, 'Bad Request. ID error.')
        # stage validate
        try:
            stage = request_dict.get('stage', None)
            to_stage = request_dict.get('to_stage', None)
        except:
            return bad_request(400, 'Bad Request. stage error.')
        print(ID, stage)
        dispatch = db.dispatch.find_one({'_id': ObjectId(ID)})
        if stage == 'took_wait_date_enter':
            # next stage wait_admin_confirm_date
            try:
                data = request_dict['data']
                db.dispatch.update_one({'_id': ObjectId(ID)}, {'$set': {
                    'dispatch_time': datetime.datetime.strptime(data['dispatch_time'],'%Y-%m-%d'),
                    'stage': 'wait_admin_confirm_date'}})
                push_notify = DispatchPushNotification(db, ID, dispatch.get('name', ''), dispatch.get('ID', ''))
                push_notify.send('wait_admin_confirm_date')
            except Exception as e:
                return bad_request(400, 'Bad Request. {}'.format(exception_detail(e)))
        elif stage == 'wait_admin_confirm_date':
            try:
                if request_dict['data'] == True:
                    db.dispatch.update_one({'_id': ObjectId(ID)}, {'$set': {
                    'stage': 'wait_for_dispatch'}})
                    push_notify = DispatchPushNotification(db, ID, dispatch.get('name', ''), dispatch.get('ID', ''))
                    push_notify.send('wait_admin_confirm_date_success', dispatch.get('maintainer_ID', None))
                elif request_dict['data'] == False:
                    db.dispatch.update_one({'_id': ObjectId(ID)}, {'$set': {
                    'stage': 'took_wait_date_enter'}})
                    push_notify = DispatchPushNotification(db, ID, dispatch.get('name', ''), dispatch.get('ID', ''))
                    push_notify.send('took_wait_date_enter_failed', dispatch.get('maintainer_ID', None))
            except Exception as e:
                return bad_request(400, 'Bad Request. {}'.format(exception_detail(e)))
        elif stage == 'auto_reviewed_wait_for_manual':
            try:
                if request_dict['data'][0] == True:
                    auto_review_cost = 0
                    auto_review_cost_detail = {
                        'predict_dispatch_cost': None,
                        'transit_fee': None,
                        'worker_fee': None
                    }
                    dispatch = db.dispatch.find_one({'_id': ObjectId(ID)})
                    try:
                        auto_review_cost = dispatch.get('predict_dispatch_cost', 0)   #設備維修成本
                        try:
                            transit_fee = dispatch['working_data'][-1]['transit']['fee']
                            if isinstance(transit_fee, (int, float)):
                                auto_review_cost += transit_fee   #交通成本
                        except: # no fee
                            pass
                        worker_fee = None
                        working_hour = dispatch['working_data'][-1].get('working_hour', 0)   #工時
                        for user in db.users.find({'_id': ObjectId(dispatch['maintainer_ID'])}):
                            if 'user_data' in user:
                                if isinstance(user['user_data'].get('dispatch_price_per_hour'), (int, float)):
                                    worker_fee = working_hour * user['user_data'].get('dispatch_price_per_hour')   #工時 * price/hr
                                    auto_review_cost += worker_fee
                        auto_review_cost_detail = {
                            'predict_dispatch_cost': dispatch.get('predict_dispatch_cost', 0),
                            'transit_fee': transit_fee,
                            'worker_fee': worker_fee
                        }
                    except Exception as e:
                        print(exception_detail('auto_review_cost_fail. {}'.format(exception_detail(e))))
                    db.dispatch.update_one({'_id': ObjectId(ID)}, {'$set': {
                        'stage': 'dispatch_finish',
                        'auto_review_cost': auto_review_cost,
                        'auto_review_cost_detail': auto_review_cost_detail,
                    }})
                    push_notify = DispatchPushNotification(db, ID, dispatch.get('name', ''), dispatch.get('ID', ''))
                    push_notify.send('dispatch_finish', dispatch.get('maintainer_ID', None))
                else:
                    db.dispatch.update_one({'_id': ObjectId(ID)}, {'$set': {
                    'stage': 'review_failed', 'review_failed_reason': request_dict['data'][1]}})
                    push_notify = DispatchPushNotification(db, ID, dispatch.get('name', ''), dispatch.get('ID', ''))
                    push_notify.send('review_failed', dispatch.get('maintainer_ID', None))
            except Exception as e:
                return bad_request(400, 'Bad Request. {}'.format(exception_detail(e)))
        elif stage == 'review_failed':
            db.dispatch.update_one({'_id': ObjectId(ID)}, {'$set': {
            'stage': 'wait_for_dispatch'}})
        elif stage == 'wait_for_take' and to_stage == 'wait_for_take':
            try:
                data = request_dict['data']
                db.dispatch.update_one({'_id': ObjectId(ID)}, {'$set': {
                    'dispatch_time': None if data['dispatch_time'] == None else datetime.datetime.strptime(data['dispatch_time'],'%Y-%m-%d'),
                }})
            except Exception as e:
                return bad_request(400, 'Bad Request. {}'.format(exception_detail(e)))
        elif stage == None:
            if to_stage != None:
                if to_stage == 'wait_for_take':
                    db.dispatch.update_one({'_id': ObjectId(ID)}, {'$set':{
                        'stage': to_stage, 'maintainer_ID': None
                        }
                    })
                    push_notify = DispatchPushNotification(db, ID, dispatch.get('name', ''), dispatch.get('ID', ''))
                    push_notify.send('transfer_wait_for_take')
        return successful_request()
application_dispatch.add_url_rule('/dispatch_update_stage', view_func=DispatchUpdateStage.as_view('dispatch_update_stage'))
#-------------------------------------------------------------------------------
class DisaptchUpdateContent(views.MethodView):
    def post(self):
        user, db = check_user()
        if db == None:
            return logout()
        request_dict = request.json
        # dispatch_ID validate
        try:
            dispatch_ID = request_dict['dispatch_ID']
            ObjectId(dispatch_ID)
        except:
            return bad_request(400, 'Bad Request. dispatch_ID error.')
        # ID validate
        try:
            ID = request_dict['ID']
        except:
            return bad_request(400, 'Bad Request. ID error.')
        # dispatch_type validate
        # ID validate
        try:
            dispatch_type = request_dict['type']
        except:
            return bad_request(400, 'Bad Request. dispatch_type error.')
        cause = request_dict.get('cause', {})
        
        for dispatch in db.dispatch.find({'_id': ObjectId(dispatch_ID)}):
            try:
                if dispatch_type == 'alarm':
                    alarm_list = dispatch['alarm_list']
                    for alarm in alarm_list:
                        if alarm['ID'] == ID:
                            if cause['ID'] in alarm['cause']:
                                alarm['cause'][cause['ID']]['fix'] = cause['fix']
                                alarm['cause'][cause['ID']]['info'] = cause['info']
                            else:
                                return bad_request(400, 'Bad Request. Cause not found.')
                    db.dispatch.update_one({'_id': ObjectId(dispatch_ID)}, {'$set': {'alarm_list': alarm_list}})
                elif dispatch_type in ['wash', 'regular']:
                    schedule_list = dispatch['{}_list'.format(dispatch_type)]
                    for group in schedule_list:
                        if group['name'] == ID:
                            if cause['name'] in group['child']:
                                if cause['category'] == 'choice':
                                    group['child'][cause['name']]['choice'] = cause['choice']
                                elif cause['category'] in ['normal_choice_na', 'yes_choice_na']:
                                    group['child'][cause['name']]['choice'] = cause['choice']
                                elif cause['category'] == 'numeric':
                                    group['child'][cause['name']]['value'] = cause['value']
                                group['child'][cause['name']]['info'] = cause['info']
                            else:
                                return bad_request(400, 'Bad Request. Cause not found.')
                    db.dispatch.update_one({'_id': ObjectId(dispatch_ID)}, {'$set': {'{}_list'.format(dispatch_type): schedule_list}})

                #print(dispatch)
            except Exception as e:
                print(exception_detail(e))
                return bad_request(400, 'Bad Request. {}'.format(exception_detail(e)))
        
        return successful_request()

application_dispatch.add_url_rule('/dispatch_update_content', view_func=DisaptchUpdateContent.as_view('dispatch_update_content'))
#-------------------------------------------------------------------------------
class DispatchAutoReview(views.MethodView):
    def post(self):
        user, db = check_user()
        if db == None:
            return logout()
        request_dict = request.json
        try:
            dispatch_ID = request_dict['dispatch_ID']
            ObjectId(dispatch_ID)
        except:
            return bad_request(400, 'Bad Request. dispatch_ID error.')
        dispatch_finish = request_dict.get('dispatch_finish', False)        
        dispatch_error = False
        error_dict = {
            'alarm': {},
            'regular': {},
            'wash': {}
        }
        for dispatch in db.dispatch.find({'_id': ObjectId(dispatch_ID)}):
            #print(dispatch)

            if 'alarm_list' in dispatch:
                result = self.alarm_check(dispatch['alarm_list'])
                if result[0] == False:
                    dispatch_error = True
                    error_dict['alarm'].update(result[1])
            if 'wash_list' in dispatch:
                result = self.regular_wash_check(dispatch['wash_list'])
                if result[0] == False:
                    dispatch_error = True
                    error_dict['wash'].update(result[1]) 
            if 'regular_list' in dispatch:
                result = self.regular_wash_check(dispatch['regular_list'])
                if result[0] == False:
                    dispatch_error = True
                    error_dict['regular'].update(result[1]) 
            if dispatch_finish:
                try:
                    working_hour = float(request_dict['working_hour'])
                except Exception as e:
                    return bad_request(400, 'Bad Request. working_hour error.')
                current_time = datetime.datetime.now()
                dispatch['working_data'][-1]['working_hour'] = working_hour
                dispatch['working_data'][-1]['finish_hour'] = current_time
                db.dispatch.update_one({'_id': ObjectId(dispatch_ID)}, {'$set': {
                    'working_data': dispatch['working_data'], 'finish_time': current_time,
                    'next_review_time': current_time
                }})
                # dispatch contents are looks good
                enable_ai_review = True
                for parameter in db.parameter_setting.find({'method': 'enable_dispatch_ai_review'}):
                    if 'enable' in parameter:
                        enable_ai_review = parameter['enable']
                db.dispatch.update_one({'_id': ObjectId(dispatch_ID)}, {
                    '$set': {'stage': 'dispatched_wait_for_review' if enable_ai_review else 'auto_reviewed_wait_for_manual'}
                })

        return successful_request({
            'error': dispatch_error,
            'error_data': error_dict
        })
    def alarm_check(self, alarm_list):
        #print(alarm_list)
        error_dict = {}
        for alarm in alarm_list:
            for cause in alarm['cause']:
                # if alarm only have default else cause still needs to check
                if cause == 'else' and len(alarm['cause'].keys()) > 1:
                    continue
                if alarm['cause'][cause]['fix'] != True:
                    error_dict[alarm['ID']] = {
                        'type': 'alarm',
                        'ID': alarm['ID'],
                        'child_ID': cause,
                        'error': ['fix']
                    }
        if len(error_dict.keys()) > 0:
            return False, error_dict
        else:
            return True, None
    def regular_wash_check(self, data_list):
        error_dict = {}
        for group in data_list:
            for child_name in group['child']:
                child = group['child'][child_name]
                error_list = []
                if child['category'] in ['choice', 'normal_choice_na', 'yes_choice_na']:
                    if child['choice'] == None:
                        error_list.append('choice')
                elif child['category'] == 'numeric':
                    if child['value'] == None:
                        error_list.append('value')
                if child.get('photo_required', False):
                    if len(child['photo']) == 0:
                        error_list.append('photo')
                if len(error_list) > 0:
                    error_dict[group['name']] = {
                        'type': 'schedule',
                        'group': group['name'],
                        'error': error_list
                    }

        if len(error_dict.keys()) > 0:
            return False, error_dict
        else:
            return True, None
            
application_dispatch.add_url_rule('/dispatch_auto_review', view_func=DispatchAutoReview.as_view('dispatch_auto_review'))
#-------------------------------------------------------------------------------
class DispatchWorkerTransit(views.MethodView):
    def post(self):
        user, db = check_user()
        if db == None:
            return logout()
        request_dict = request.json
        print(request_dict)
        try:
            dispatch_ID = request_dict['dispatch_ID']
            ObjectId(dispatch_ID)
        except:
            return bad_request(400, 'Bad request. dispatch_ID error.')
        
        find_user = find_user_from_current_user()
        user_c=list(db.users.find({"user_id" : find_user}))[0]
        for dispatch in db.dispatch.find({'_id': ObjectId(dispatch_ID)}):
            try:
                address = request_dict['address']
                place_id = request_dict['place_id']
                direction_distance = int(request_dict['distance'])/1000

                km_per_liter = user_c.get('user_data', {}).get('km_per_liter', 12)  # Using Toyota Town Ace Avg.
                try:
                    oil_price = db.parameter_setting.find_one({'method': 'dispatch_transit_oil_price'})['value']   # use parameter_setting
                except:
                    oil_price = 30
                transit_cost = round(direction_distance/km_per_liter*oil_price)
                dispatch['working_data'][-1]['transit']['start_address'] = address
                dispatch['working_data'][-1]['transit']['position_id'] = place_id
                dispatch['working_data'][-1]['transit']['fee'] = transit_cost

                #print(dispatch)
                db.dispatch.update_one({'_id': ObjectId(dispatch_ID)}, {
                    '$set': {'working_data': dispatch['working_data']}
                })
            except Exception as e:
                return bad_request(400, 'Bad Request. {}'.format(exception_detail(e)))
        return successful_request({
            'transit': {
                'total_cost': transit_cost,
            }
        })        
application_dispatch.add_url_rule('/dispatch_worker_transit', view_func=DispatchWorkerTransit.as_view('dispatch_worker_transit'))
#-------------------------------------------------------------------------------
class DispatchEditContent(views.MethodView):
    def post(self):
        user, db = check_user()
        if db == None:
            return logout()
        request_dict = request.json
        try:
            dispatch_ID = request_dict['dispatch_ID']
            ObjectId(dispatch_ID)
        except:
            return bad_request(400, 'Bad Request. dispatch_ID error.')
        try:
            edit_type = request_dict['type']
        except:
            return bad_request(400, 'Bad Request. type error.')
        for dispatch in db.dispatch.find({'_id': ObjectId(dispatch_ID)}):
            if edit_type == 'alarm':
                try:
                    data = request_dict['data']
                    #print(data)
                    ID_list = []
                    # delete alarm
                    alarm_list = []
                    for alarm in dispatch.get('alarm_list', []):
                        if alarm['ID'] in data:
                            alarm_list.append(alarm)
                        else:
                            # remove alarm's dispatch_ID
                            db.alarm.update_one({'_id': ObjectId(alarm['ID'])}, {'$set': {'dispatch_ID': None}})
                    dispatch['alarm_list'] = alarm_list
                    for alarm in dispatch.get('alarm_list', []):
                        ID_list.append(alarm['ID'])
                        #cause update
                        if alarm['ID'] in data.keys():
                            for cause_ID in data[alarm['ID']]:
                                if cause_ID not in alarm['cause']:
                                    alarm['cause'][cause_ID] = {
                                        'ID': cause_ID,
                                        'info': '',
                                        'photo': [],
                                        'fix': False
                                    }
                            # cause remove
                            new_cause = alarm['cause'].copy()
                            for cause_ID in alarm['cause']:  # cause already in db
                                if cause_ID not in data[alarm['ID']].keys():
                                    new_cause.pop(cause_ID)
                            alarm['cause'] = new_cause
                    # alarm add or delete
                    #new_alarm
                    for alarm_ID in data:
                        if alarm_ID not in ID_list:
                            print('xxxxxxxxxx')
                            if 'alarm_list' not in dispatch:
                                dispatch['alarm_list'] = []
                            dispatch['alarm_list'].append({
                                'ID': alarm_ID,
                                'cause': {
                                    'else': {
                                        'ID': 'else',
                                        'info': '',
                                        'photo': [],
                                        'fix': False
                                    }
                                }
                            })
                            for cause_ID in data[alarm_ID]:
                                dispatch['alarm_list'][-1]['cause'][cause_ID] = {
                                    'ID': cause_ID,
                                    'info': '',
                                    'photo': [],
                                    'fix': False
                                }
                            db.alarm.update_one({'_id': ObjectId(alarm_ID)}, {'$set': {'dispatch_ID': str(dispatch['_id'])}})
                    #print(dispatch['alarm_list'])
                    db.dispatch.update_one({'_id': dispatch['_id']}, {'$set': {
                        'alarm_list': dispatch['alarm_list']
                    }})

                except Exception as e:
                    print(exception_detail(e))
                    return bad_request(400, 'Bad Request. {}'.format(exception_detail(e)))
            elif edit_type in ['regular', 'wash']:
                try:
                    data = request_dict['data']
                    group_list = dispatch.get('{}_list'.format(edit_type), [])
                    print(group_list)
                    upload_group = []
                    for group in data:
                        new_group = {
                            'name': group['name'],
                            'child': {}
                        }
                        origin_group = {}
                        for _group in group_list:
                            if _group['name'] == group['name']:
                                origin_group = _group['child']
                        for child in group['child']:
                            print(child)
                            if child['name'] in origin_group and child['category'] ==  origin_group[child['name']]['category']:
                                new_group['child'][child['name']] = origin_group[child['name']]
                                new_group['child'][child['name']]['photo_required'] = child['photo_required']
                            else:
                                new_group['child'][child['name']] = {
                                    'name': child['name'],
                                    'category': child['category'],
                                    'photo_required': child['photo_required'],
                                    'photo': [],
                                    'info': '',
                                }
                                if child['category'] == 'choice':
                                    new_group['child'][child['name']]['choice'] = None
                                elif child['category'] in ['normal_choice_na', 'yes_choice_na']:
                                    new_group['child'][child['name']]['choice'] = None
                                elif child['category'] == 'numeric':
                                    new_group['child'][child['name']]['value'] = None
                                    new_group['child'][child['name']]['suggest_value'] = child.get('suggest_value', None)
                        
                        upload_group.append(new_group)
                    
                    db.dispatch.update_one({'_id': dispatch['_id']}, {
                        '$set': {
                            '{}_list'.format(edit_type): upload_group
                        }
                    })


                except Exception as e:
                    print(exception_detail(e))
                    return bad_request(400, 'Bad Request. {}'.format(exception_detail(e)))
        return successful_request()
application_dispatch.add_url_rule('/dispatch_edit_content', view_func=DispatchEditContent.as_view('dispatch_edit_content'))
#-------------------------------------------------------------------------------
class DispatchMergeDispatch(views.MethodView):
    def post(self):
        user, db = check_user()
        if db == None:
            return logout()
        request_dict = request.json
        try:
            dispatch_ID = request_dict['dispatch_ID']
            ObjectId(dispatch_ID)
        except:
            return bad_request(400, 'Bad Request. dispatch_ID error.')
        try:
            merge_ID = request_dict['merge_ID']
            ObjectId(merge_ID)
        except:
            return bad_request(400, 'Bad Request. merge_ID error.')
        #print(dispatch_ID, merge_ID)
        for dispatch in db.dispatch.find({'_id': ObjectId(dispatch_ID)}):
            for merge_dispatch in db.dispatch.find({'_id': ObjectId(merge_ID)}):
                for i in ['alarm', 'wash', 'regular']:
                    if '{}_list'.format(i) in merge_dispatch:
                        if  '{}_list'.format(i) not in dispatch:
                            dispatch['{}_list'.format(i)] = merge_dispatch[ '{}_list'.format(i)]
                        else:
                            dispatch['{}_list'.format(i)].extend(merge_dispatch['{}_list'.format(i)])
                        # dispatch type
                        if i not in dispatch['type']:
                            dispatch['type'].append(i)

                db.dispatch.update_one({'_id': merge_dispatch['_id']}, {
                    '$set': {
                        'stage': 'merged', 'dispatch_time': dispatch['dispatch_time'], 'last_change_time': datetime.datetime.now()
                    }
                })
                dispatch.pop('_id', None)
                # Re calculate _predictdispatch_cost
                dispatch['predict_dispatch_cost'] = 0
                if 'alarm_list' in dispatch:
                    repair_equip_ID_list = []
                    for alarm in dispatch['alarm_list']:
                        for a in db.alarm.find({'_id': ObjectId(alarm['ID'])}):
                            if 'ID' in a and a['ID'] not in repair_equip_ID_list:
                                repair_equip_ID_list.append(a['ID'])
                                dispatch['predict_dispatch_cost'] += self.get_repair_cost(db, dispatch['ID'], alarm)
                db.dispatch.update_one({
                    '_id': ObjectId(dispatch_ID)
                }, {'$set': dispatch})

        return successful_request()
    def get_repair_cost(self, db, lgroup_ID, alarm):
        alarm_data = db.alarm.find_one({'_id': ObjectId(alarm.get('ID'))})
        equip_data = db.equipment.find_one({'_id': ObjectId(alarm_data['ID'])})
        iot_data = db.iot.find_one({'_id': ObjectId(alarm_data['ID'])})
        # Get replace data
        equip_type = None
        equip_model = None
        if equip_data != None:
            if 'lgroup' in equip_data:
                equip_type = equip_data.get('type') if equip_data.get('Device_type') != 'sensor' else 'sensor' 
            elif equip_data.get('type') == 'pv_lgroup':
                equip_type = 'meter'
            if 'Device_model' in equip_data:
                equip_model = equip_data.get('Device_model', '---')
        elif iot_data != None:
            equip_type = 'iot'
            equip_model = iot_data.get('Device_model', '---')
        equip_parameter = db.dispatch_parameter.find_one({'ID': lgroup_ID, 'type': equip_type,
        'model': equip_model})
        if equip_parameter != None and 'dispatch_cost' in equip_parameter:
            return equip_parameter.get('dispatch_cost', 0)
        return 0
application_dispatch.add_url_rule('/dispatch_merge_dispatch', view_func=DispatchMergeDispatch.as_view('dispatch_merge_dispatch'))
#-------------------------------------------------------------------------------
#使用位置  taipower 台電 /setting
#取得 plant lgroup 與 group 下的儀器
class GetEquipmentSelectionSettingDispatch(views.MethodView):
    def __init__(self) -> None:
        super().__init__()
        self.real_filter =  [None, '', 'none', 'PV']
    def post(self):
        user,db = check_user()
        if(db == None):
            return logout() 
        request_dict = request.json
        print(request_dict)
        try:
            ID = request_dict['ID']
            ObjectId(ID)
        except:
            return bad_request(400, 'Bad Request. ID Error.')
        try:
            collection = request_dict['collection']
        except:
            return bad_request(400, 'Bad Request. ID Error.')
        data_dict = {}
        # Get Plant Info
        try:
            station_info = { 'ID': ID, 'collection': collection}
            equip_filter = {}
            if collection == 'pv_plant':
                for plant in db.plant.find({'_id': ObjectId(ID)}):
                    station_info['station_list'] = [plant.get('name', '')]
                    equip_filter = {'PV': plant.get('name')}
                    if plant.get('COMport') not in self.real_filter:
                        data_dict['meter'][plant.get('model', '---')] = {
                            'ID': str(ID),
                            'model': plant.get('model', '---')
                        }
            elif collection == 'pv_lgroup':
                for lgroup in db.equipment.find({'_id': ObjectId(ID)}):
                    station_info['station_list'] = [lgroup.get('PV', ''), lgroup.get('name', '')]
                    equip_filter = {'PV': lgroup.get('PV'), 'lgroup': lgroup.get('name')}
                    if lgroup.get('COMport') not in self.real_filter:
                        data_dict['meter'][lgroup.get('model', '---')] = {
                            'ID': str(ID),
                            'model': lgroup.get('model', '---')
                        }
            elif collection == 'pv_group':
                for group in db.equipment.find({'_id': ObjectId(ID)}):
                    station_info['station_list'] = [group.get('PV', ''), group.get('lgroup', ''), group.get('name')]
                    equip_filter = {'PV': group.get('PV'), 'lgroup': group.get('lgroup'), 'group': group.get('name')}
                    if group.get('COMport') not in self.real_filter:
                        data_dict['meter'][group.get('model', '---')] = {
                            'ID': str(ID),
                            'model': group.get('model', '---')
                        }
            else:
                return bad_request(400, 'Bad Request. No such collection.')
            
            # find iot
            for iot in db.iot.find(equip_filter):
                if 'iot' not in data_dict:
                    data_dict['iot'] = {}
                if iot.get('Device_model', '---') not in data_dict['iot']:            
                    data_dict['iot'][iot.get('Device_model', '---')] = {
                        'ID': str(ID),   # station's ID should be lgroup
                        'Device_model': iot.get('Device_model', '---')
                    }
            # find equipment
            equip_filter.update({'COMport': {'$nin':self.real_filter}})
            for equip in db.equipment.find(equip_filter):
                try:
                    print(equip)
                    equip['type'] = 'sensor' if equip['type'] in ['sun', 'wind', 'temp'] else equip['type']
                    if equip['type'] not in data_dict:
                        data_dict[equip['type']] = {}
                    if equip.get('Device_model', '---') not in data_dict[equip['type']]:
                        data_dict[equip['type']][equip.get('Device_model', '---')] = {
                            'ID': str(ID),   # station's ID should be lgroup
                            'Device_model': equip.get('Device_model', '---')
                        }
                except:
                    continue
            station_info['station_str'] = '/'.join(station_info['station_list']) + '/'
            print(data_dict)
        except Exception as e:
            return bad_request(400, 'Bad Request. {}'.format(exception_detail(e)))
        # get dispatching fee
        equip_dict = {}
        for key in data_dict:
            equip_dict[key] = []
            for model in data_dict[key]:
                equip = data_dict[key][model]
                param = db.dispatch_parameter.find_one({'ID': ID, 'type': key, 'model': model})
                if param == None:
                    equip['dispatch_cost'] = None
                else:
                    equip['dispatch_cost'] = param.get('dispatch_cost', None)
                equip_dict[key].append(equip)
        return successful_request({
            'equip_data': equip_dict,
            'station_data': station_info
        })
application_dispatch.add_url_rule('/get_equip_select_setting_dispatch', view_func=GetEquipmentSelectionSettingDispatch.as_view('get_equip_select_setting_dispatch'))
#-------------------------------------------------------------------------------
@application_dispatch.route('/setting_dispatch_save_equip_param', methods=['POST'])
def setting_dispatch_save_equip_param():
    user,db = check_user()
    if(db == None):
        return logout() 
    request_dict = request.json
    try:
        ID = request_dict['ID']
        ObjectId(ID)
        equip_type = request_dict['type']
        model = request_dict['model']
    except Exception as e:
        return bad_request(400, 'Bad Request. {}'.format(exception_detail(e)))

    try:
        dispatch_cost = request_dict.get('dispatch_cost', None)
        db.dispatch_parameter.update_one({'ID': ID, 'type': equip_type, 'model': model}, {
            '$set': {'dispatch_cost': dispatch_cost}
        }, upsert=True)

    except Exception as e:
        return bad_request(400, 'Bad Request. {}'.format(exception_detail(e)))

    return successful_request()
#-------------------------------------------------------------------------------
@application_dispatch.route('/setting_dispatch_lgroup_auto_dispatch', methods=['POST', 'GET'])
def setting_dispatch_lgroup_auto_dispatch():
    user,db = check_user()
    if(db == None):
        return logout()
    if request.method == 'POST': 
        request_dict = request.json
        try:
            ID = request_dict['ID']
            ObjectId(ID)
        except:
            return bad_request(400, 'Bad Request. ID Error')

        try:
            auto_dispatch_threshold = request_dict['auto_dispatch_threshold']
            db.dispatch_parameter.update_one({'ID': ID, 'type': 'pv_lgroup'}, {
            '$set': {'auto_dispatch_threshold': auto_dispatch_threshold}
        }, upsert=True)

        except Exception as e:
            return bad_request(400, 'Bad Request. {}'.format(exception_detail(e)))

        return successful_request()
    else:
        try:
            ID = request.args['ID']
            ObjectId(ID)
        except:
            return bad_request(400, 'Bad Request. ID error.')
        try:
            station_data = {}
            param = db.dispatch_parameter.find_one({'ID': ID, 'type': 'pv_lgroup'})
            if param == None:
                station_data['auto_dispatch_threshold'] = None
            else:
                station_data['auto_dispatch_threshold'] = param.get('auto_dispatch_threshold', None)
        except Exception as e:
            return bad_request(400, 'Bad Request. {}'.format(exception_detail(e)))
        return successful_request(station_data)
#-------------------------------------------------------------------------------
@application_dispatch.route('/get_station_pv_module', methods=['POST', 'GET'])
def get_station_pv_module():
    user,db = check_user()
    if(db == None):
        return logout()
    if request.method == 'POST': 
        request_dict = request.json
        try:
            ID = request_dict['ID']
            model = request_dict['model']
            wash_cost = request_dict['wash_cost']
            #print(ID, model, wash_cost)
            param = db.dispatch_parameter.find_one({'ID': ID, 'type': 'pv_lgroup'})
            if param == None:
                module_wash_cost = {}
                module_wash_cost[model] = float(wash_cost)
                db.dispatch_parameter.update_one({'ID': ID, 'type': 'pv_lgroup'}, {
                    '$set': {
                        'module_wash_cost': module_wash_cost
                    }
                }, upsert=True)
            else:
                if 'module_wash_cost' not in param:
                    param['module_wash_cost'] = {}
                param['module_wash_cost'][model] = float(wash_cost)
                db.dispatch_parameter.update_one({'ID': ID, 'type': 'pv_lgroup'}, {
                    '$set': {
                        'module_wash_cost': param['module_wash_cost']
                    }
                })
        except Exception as e:
            return bad_request(400, 'Bad Request. {}'.format(e))
        return successful_request()
    else:
        try:
            ID = request.args['ID']
            ObjectId(ID)
        except:
            return bad_request(400, 'Bad Request. ID error.')
        module_list = []
        station_str = ''
        for lgroup in db.equipment.find({'_id': ObjectId(ID)}):
            station_str = '{}/{}'.format(lgroup.get('PV'), lgroup.get('name'))
            for group in db.equipment.find({'PV': lgroup.get('PV'), 'lgroup': lgroup.get('name'), 'type': 'pv_group'}):
                if isinstance(group.get('module_model'), str) and group.get('module_model') not in module_list:
                    module_list.append(group.get('module_model'))
                elif isinstance(group.get('module_model'), list):
                    for m in group.get('module_model'):
                        if m not in module_list:
                            module_list.append(m)
        try:
            param = db.dispatch_parameter.find_one({'ID': ID, 'type': 'pv_lgroup'})
            if param == None or 'module_wash_cost' not in param:
                return_list = []
                for m in module_list:
                    return_list.append({
                        'place': station_str,
                        'model': m,
                        'wash_cost': None
                    })
            else:
                return_list = []
                for m in module_list:
                    if m in param['module_wash_cost']:
                        return_list.append({
                            'place': station_str,
                            'model': m,
                            'wash_cost': param['module_wash_cost'][m]
                        })
                    else:
                        return_list.append({
                            'place': station_str,
                            'model': m,
                            'wash_cost': None
                        })
            return successful_request({
                'module_list': return_list
            })
        except Exception as e:
            return bad_request(400, 'Bad Request. {}'.format(exception_detail(e)))
#-------------------------------------------------------------------------------
@application_dispatch.route('/dispatch/update_dispatch_summary', methods=['POST'])
def update_dispatch_summary():
    user,db = check_user()
    if(db == None):
        return logout()
    request_dict = request.json
    try:
        ID = request_dict['ID']
        ObjectId(ID)
    except:
        return bad_request(400, 'Bad Request. ID error.')
    try:
        summary = request_dict['summary']
    except:
        return bad_request(400, 'Bad Request. summary')
    for dispatch in db.dispatch.find({'_id': ObjectId(ID)}):
        if "working_data" in dispatch and isinstance(dispatch["working_data"], list) and len(dispatch["working_data"]) > 0:
            dispatch["working_data"][-1]["summary"] = summary
        db.dispatch.update_one({'_id': dispatch['_id']}, { '$set': { 'working_data': dispatch['working_data']}})
    return successful_request()