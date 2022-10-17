from app_common import successful_request, bad_request, exception_detail, conn
#-------------------------------------------------------------------------------
from flask import Blueprint, current_app, views, request
from bson.objectid import ObjectId
import datetime

# Python Json Web Tokens
import jwt
#-------------------------------------------------------------------------------
import current as c
#======================================================================================================
# application_common is a Blueprint of flask
# Learn More About Blueprint At
# https://flask.palletsprojects.com/en/2.0.x/blueprints/
application_app_widget = Blueprint('application_app_widget', __name__)
#======================================================================================================
def check_user(access_token):
    try:
        my_decode = jwt.decode(access_token, '{}_app_widget_access_key'.format(current_app.secret_key), algorithms=["HS256"])
        user_data = conn[my_decode['company']].users.find_one({'_id': ObjectId(my_decode["uid"])})
        if user_data != None:
            return str(user_data['_id']), conn[my_decode['company']]
        return None, None
    except:
        return None, None
#-------------------------------------------------------------------------------
def no_auth():
    return bad_request(401, 'Unauthorized.')
#======================================================================================================
class StatsAllPV(views.MethodView):
    def get(self):
        user_ID, db = check_user(request.headers.get('Authorization'))
        if db == None:
            return no_auth()
        user_c=list(db.users.find({"_id" : ObjectId(user_ID)}))[0]
        today = datetime.datetime.strftime(datetime.datetime.now(), '%Y-%m-%d')
        today = datetime.datetime.strptime(today, '%Y-%m-%d')
        try:
            plant_filter = {}
            if user_c['plant'][0] != 'total':
                for i in user_c['plant']:
                    if 'name' not in plant_filter:
                        plant_filter['name'] = {'$in': []}
                    plant_filter['name']['$in'].append(i)
            stats_data = {'station_count': 0, 'total_capacity': 0, 'kwh_today': 0, 'alarm_count': 0}
            for plant in db.plant.find(plant_filter):
                stats_data['total_capacity'] += plant.get('capacity', 0) 
                group_count = db.equipment.count_documents({'PV': plant['name'], 'type': 'pv_group'})
                try:
                    #today_kwh = c.diff_data(db, 'pv_plant', str(plant['_id']), 'kwh', 0)
                    today_kwh = db.meter_cal.find_one({'ID': str(plant['_id']), 'time_interval': 'day', 'time': today}).get('kwh', None)
                    print(today_kwh)
                    #today_kwh = c.current_data(db, plant.get('collection', 'pv_plant'), str(plant['_id']))
                    if isinstance(today_kwh, list) and len(today_kwh) > 0:
                        today_kwh = today_kwh[0].get('kwh', None)
                    if isinstance(today_kwh, (int, float)):
                        stats_data['kwh_today'] += today_kwh
                except:
                    pass
                stats_data['station_count'] += group_count
            stats_data['total_capacity'] = round(stats_data['total_capacity']) # convert kW to MW 
            stats_data['kwh_today'] = round(stats_data['kwh_today'])
            stats_data['carbon_reduction_today'] = round(stats_data['kwh_today']*0.502)   # 109 年排碳係數 
            stats_data['alarm_count'] = 0
            for key in stats_data:
                stats_data[key] = str(stats_data[key])
        except Exception as e:
            print(exception_detail(e))
            return bad_request('Error Due to {}'.format(e))
        return successful_request(stats_data)
    def post(self):
        return self.get()
application_app_widget.add_url_rule('/app/stats_all_pv', view_func=StatsAllPV.as_view('stats_all_pv'))
#-------------------------------------------------------------------------------
