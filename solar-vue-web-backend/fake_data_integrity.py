from pymongo import MongoClient
import datetime
from dateutil.relativedelta import relativedelta
import os

# 使用:打印資訊
# data:要打印資訊
# select:選擇哪種方式呈現 0.不處理 1.直接打印 2.寫入資料庫 3.寫入筆記本
# funcation_name:方程式名稱
# error_code:錯誤訊息
# level:資訊重要等級  0.正常打印 1.錯誤仍可運行 2.錯誤程序結束 3.錯誤影響其他程式運行 4.線呈出錯仍可重新執行 5.線呈終止 6.資料遺失


def print_function(data, select, funcation_name, error_code, level):
    try:
        now_time = datetime.datetime.now()
        if select == 0:
            pass
        elif select == 1:
            print(str(data)+'  / '+str(funcation_name) +
                  ' /  level :'+str(level)+' / '+str(now_time))
            if error_code != None:
                print(error_code)

        elif select == 3:
            if level >= 1:
                try:
                    with open('SystemList.txt', 'a+') as file:
                        file.write(str(data)+'  / '+str(funcation_name) +
                                   ' /  level :'+str(level)+' / '+str(now_time)+"\n")
                        if error_code != None:
                            file.write(str(error_code)+"\n")
                except Exception as e:
                    print('print txt error')

        else:
            print('dont select data print type')

        if level >= 1 and select != 1 and select != 0:
            print(str(data)+'  / '+str(funcation_name) +
                  ' /  level :'+str(level)+' / '+str(now_time))
            if error_code != None:
                print(error_code)
    except Exception as e:
        print(str(e)+" / print_function / end")

# 使用:修改mongo資料
# mongodbData=[{'host':MONGO_HOST,'port':MONGO_PORT,'db':MONGO_DB,'user':MONGO_USER,'pass':MONGO_PASS}]
# collection:需要修改的資料表
# data:需要修改所搜尋的資料 資料為List 多筆需淤要修改的資料[{},{},{}]
# change_data:搜尋的資料要改成的資料


def mongo_update(mongodbData, collection, data, change_data):
    try:
        select = 1
        # print (data)
        # print (change_data)
        collect = mongodbData[collection]
        try:
            collect.update_one(data, {'$set': change_data}, upsert=True)
            return True
        except Exception as e:
            print_function('dont upload point', select, 'mongo_update', e, 1)
            return False
    except Exception as e:
        print_function('unknow error', select, 'mongo_update', e, 1)
        return False


def fake_data_integrity(start, end, macname, equipment_json, member_number, db):
    try:
        ### parameter setting ###
        start_time = start
        end_time = end
        try:
            total_hour = int((end_time - start_time).total_seconds()/60/60)
            if total_hour <= 0:
                total_hour = 0
        except:
            total_hour = 0

        # mac = ['天權6']
        # mac = ['瑤光19']
        # mac = ['水車頭段629一期','水車頭段629二期']
        mac = macname

        try:
            plant_function = equipment_json['plant']
            lgroup_function = equipment_json['lgroup']
            group_function = equipment_json['group']
            inverter_function = equipment_json['inverter']
            sensor_function = equipment_json['sensor']
            meter_function = equipment_json['meter']
        except:
            plant_function = 0
            lgroup_function = 0
            group_function = 0
            inverter_function = 0
            sensor_function = 0
            meter_function = 0

        try:
            member = member_number
        except:
            member = '1'

        ### main code ###
        plant_ID = []
        lgroup_ID = []
        group_ID = []
        inverter_ID = []
        sensor_ID = []
        meter_ID = []
        for macs in range(len(mac)):
            print(mac[macs])
            if plant_function == 1:
                plant_equipment = list(db['plant'].find({'mac': mac[macs]}))
                if len(plant_equipment):
                    for plant_equipments in range(len(plant_equipment)):
                        # print(inverter_equipment[inverter_equipments])
                        plant_ID.append(
                            str(plant_equipment[plant_equipments]['_id']))
                else:
                    group_name = list(db['equipment'].find(
                        {'mac': mac[macs], 'collection': 'inverter'}).limit(1))
                    try:
                        plant_equipment = list(db['plant'].find(
                            {'name': group_name[0]['PV']}))
                        plant_ID.append(str(plant_equipment[0]['_id']))
                    except Exception as e:
                        pass

            if lgroup_function == 1:
                lgroup_equipment = list(db['equipment'].find(
                    {'mac': mac[macs], 'type': 'pv_lgroup'}))
                if len(lgroup_equipment):
                    for lgroup_equipments in range(len(lgroup_equipment)):
                        # print(inverter_equipment[inverter_equipments])
                        lgroup_ID.append(
                            str(lgroup_equipment[lgroup_equipments]['_id']))
                else:
                    group_name = list(db['equipment'].find(
                        {'mac': mac[macs], 'collection': 'inverter'}).limit(1))
                    try:
                        lgroup_equipment = list(db['equipment'].find(
                            {'PV': group_name[0]['PV'], 'name': group_name[0]['lgroup']}))
                        lgroup_ID.append(str(lgroup_equipment[0]['_id']))
                    except Exception as e:
                        pass

            if group_function == 1:
                group_equipment = list(db['equipment'].find(
                    {'mac': mac[macs], 'type': 'pv_group'}))
                if len(group_equipment):
                    for group_equipments in range(len(group_equipment)):
                        # print(inverter_equipment[inverter_equipments])
                        group_ID.append(
                            str(group_equipment[group_equipments]['_id']))
                else:
                    group_name = list(db['equipment'].find(
                        {'mac': mac[macs], 'collection': 'inverter'}).limit(1))
                    try:
                        group_equipment = list(db['equipment'].find(
                            {'PV': group_name[0]['PV'], 'lgroup': group_name[0]['lgroup'], 'name': group_name[0]['group']}))
                        group_ID.append(str(group_equipment[0]['_id']))
                    except Exception as e:
                        pass

            if inverter_function == 1:
                inverter_equipment = list(db['equipment'].find(
                    {'mac': mac[macs], 'type': 'inv'}))
                for inverter_equipments in range(len(inverter_equipment)):
                    # print(inverter_equipment[inverter_equipments])
                    inverter_ID.append(
                        str(inverter_equipment[inverter_equipments]['_id']))

            if sensor_function == 1:
                sensor_equipment = list(db['equipment'].find(
                    {'mac': mac[macs], "main_sun": 1, 'type': 'sun'}))
                for sensor_equipments in range(len(sensor_equipment)):
                    # print(inverter_equipment[inverter_equipments])
                    sensor_ID.append(
                        str(sensor_equipment[sensor_equipments]['_id']))

            if meter_function == 1:
                print('mac:', mac[macs])
                meter_equipment = list(db['equipment'].find(
                    {'mac': mac[macs], 'type': 'meter'}))
                for meter_equipments in range(len(meter_equipment)):
                    # print(inverter_equipment[inverter_equipments])
                    meter_ID.append(
                        str(meter_equipment[meter_equipments]['_id']))
        # print(plant_ID)
        # print(lgroup_ID)
        # print(group_ID)
        # print(inverter_ID)
        # print(sensor_ID)
        # print(meter_ID)

        # all_types = ['inv','meter','pv_group','pv_lgroup','PV','sun','pv_plant']
        for hours in range(total_hour):
            print(start_time + relativedelta(hours=hours))
            now_time = start_time + relativedelta(hours=hours)

            print('---------------------------------------------')
            print('pv_plant')
            if len(plant_ID):
                for plant_IDs in range(len(plant_ID)):
                    condition = {'ID': plant_ID[plant_IDs], 'time': now_time}
                    set_condition = {'ID': plant_ID[plant_IDs], 'time': now_time, 'level': 'pv_plant', "done": True, "lost_restart": True,
                                     "cal_restart_done": False, 'rate': 0.9, "time_interval": 'hour', 'fake': True, 'member': member}
                    print(condition, set_condition)
                    mongo_update(db, 'data_integrity',
                                 condition, set_condition)
            print('---------------------------------------------')
            print('pv_lgroup')
            if len(lgroup_ID):
                for lgroup_IDs in range(len(lgroup_ID)):
                    condition = {'ID': lgroup_ID[lgroup_IDs], 'time': now_time}
                    set_condition = {'ID': lgroup_ID[lgroup_IDs], 'time': now_time, 'level': 'pv_lgroup', "done": True,
                                     "lost_restart": True, "cal_restart_done": False, 'rate': 0.9, "time_interval": 'hour', 'fake': True, 'member': member}
                    print(condition, set_condition)
                    mongo_update(db, 'data_integrity',
                                 condition, set_condition)
            print('---------------------------------------------')
            print('pv_group')
            if len(group_ID):
                for group_IDs in range(len(group_ID)):
                    condition = {'ID': group_ID[group_IDs], 'time': now_time}
                    set_condition = {'ID': group_ID[group_IDs], 'time': now_time, 'level': 'pv_group', "done": True, "lost_restart": True,
                                     "cal_restart_done": False, 'rate': 0.9, "time_interval": 'hour', 'fake': True, 'member': member}
                    print(condition, set_condition)
                    mongo_update(db, 'data_integrity',
                                 condition, set_condition)
            print('---------------------------------------------')
            print('inverter')
            if len(inverter_ID):
                for inverter_IDs in range(len(inverter_ID)):
                    condition = {
                        'ID': inverter_ID[inverter_IDs], 'time': now_time}
                    set_condition = {'ID': inverter_ID[inverter_IDs], 'time': now_time, 'level': 'inv', "done": True, "lost_restart": True,
                                     "cal_restart_done": False, 'rate': 0.9, "time_interval": 'hour', 'fake': True, 'member': member}
                    print(condition, set_condition)
                    mongo_update(db, 'data_integrity',
                                 condition, set_condition)
            print('---------------------------------------------')
            print('sun')
            if len(sensor_ID):
                for sensor_IDS in range(len(sensor_ID)):
                    condition = {'ID': sensor_ID[sensor_IDS], 'time': now_time}
                    set_condition = {'ID': sensor_ID[sensor_IDS], 'time': now_time, 'level': 'sun', "done": True, "lost_restart": True,
                                     "cal_restart_done": False, 'rate': 0.9, "time_interval": 'hour', 'fake': True, 'member': member}
                    print(condition, set_condition)
                    mongo_update(db, 'data_integrity',
                                 condition, set_condition)
            print('---------------------------------------------')
            print('meter')
            if len(meter_ID):
                for meter_IDs in range(len(meter_ID)):
                    condition = {'ID': meter_ID[meter_IDs], 'time': now_time}
                    set_condition = {'ID': meter_ID[meter_IDs], 'time': now_time, 'level': 'meter', "done": True, "lost_restart": True,
                                     "cal_restart_done": False, 'rate': 0.9, "time_interval": 'hour', 'fake': True, 'member': member}
                    print(condition, set_condition)
                    mongo_update(db, 'data_integrity',
                                 condition, set_condition)

        print(start_time, end_time, total_hour)
        return True
    except:
        return False


def main_function(import_data):
    MONGO_HOST = os.getenv('MONGODB_HOSTNAME', 'localhost')
    MONGO_PORT = os.getenv('MONGODB_PORT', '27017')
    MONGO_USER = os.getenv('MONGODB_USERNAME', 'root')
    MONGO_PASS = os.getenv('MONGODB_PASSWORD', 'pc152')
    print(MONGO_HOST, MONGO_PASS, MONGO_USER, MONGO_PORT)
    uri = "mongodb://{}:{}@{}:{}/".format(MONGO_USER,
                                          MONGO_PASS, MONGO_HOST, MONGO_PORT)
    conn = MongoClient(uri, connect=False)
    db = conn['pv']  # connect database
    print(import_data)

    a = fake_data_integrity(
        import_data[0], import_data[1], import_data[2], import_data[3], import_data[4], db)
    # a = fake_data_integrity(datetime.datetime(2022, 5, 17, 0), datetime.datetime(2022, 5, 17, 1), [
    #                         '建華保養廠第二區停車格'], {'plant': 0, 'lgroup': 0, 'group': 0, 'inverter': 0, 'sensor': 0, 'meter': 0}, '1', db)
    # print(a)
