import pymongo
import datetime
import time 
from dateutil.relativedelta import relativedelta
from bson.objectid import ObjectId
import urllib3
import json
import random

http = urllib3.PoolManager()
#---------------------------------------------------------------------------------------
def beftime(interval = 1):
    localtime = datetime.datetime.now()
    beforetime  = localtime - datetime.timedelta(seconds=interval)    
    return beforetime
#------------------------------------------------------------------------------------
def date_interval(date=datetime.date.today()):
    starttime = datetime.datetime.combine(date, datetime.time.min)
    endtime = starttime+datetime.timedelta(days=1)
    return starttime,endtime
#------------------------------------------------------------------------------------
def month_interval(date=datetime.date.today()):
    starttime = datetime.datetime.combine(date + relativedelta(day=1), datetime.time.min)
    endtime = starttime+relativedelta(months=+1)
    return starttime,endtime
#------------------------------------------------------------------------------------
def year_interval(date=datetime.date.today()):
    starttime = datetime.datetime.combine(date + relativedelta(month=1,day=1), datetime.time.min)
    endtime = starttime+relativedelta(years=1)
    return starttime,endtime

#--------------------------------------------------------------------------------------
def current_data(db,collection,ID,project={},errortime=500):
    #beforetime = beftime(errortime)
    db = db[collection]
    if(type(ID)==str):
        ID = ID.split(',')

    project = {**{'_id':0},**project}
    data = []
    
    for i in ID:
        #_data = db.find_one({'ID':i,'time': {'$gte': beforetime}},project,sort=[( 'time', pymongo.DESCENDING )])
        _data = db.find_one({'ID':i},project,sort=[( 'time', pymongo.DESCENDING )])
        if(_data!=None):
            #print(_data)
            data.append(_data)
        else:
            data.append({})
    return data
#--------------------------------------------------------------------------------------
def current_protective_relay_data(db,collection,ID,IEEE_code,points,project={},errortime=500):
    #beforetime = beftime(errortime)
    db = db[collection]
    
    project = {**{'_id':0},**project}
    data = []
    
    #_data = db.find_one({'ID':i,'time': {'$gte': beforetime}},project,sort=[( 'time', pymongo.DESCENDING )])
    name_list = list(set(db.distinct('name')).intersection(list(points.keys())))
    for name in name_list:
        for _data in db.find({'ID':ID,'name': name}, project).sort('time', -1).limit(1):
            try:
                if IEEE_code != 'total' and IEEE_code != _data['IEEE_code']:
                    continue
                data.append(_data)
            except:
                continue
    return data
#----------------------------------------------------------------------------------------
def diff_data(db,collection,ID,datatype,date_range=0):
    db = db[collection]
    if(type(ID)==str):
        ID = ID.split(',')
    diff = 0

    if(date_range==3):
        time = {}
    else:
        if(date_range==0):
            starttime,endtime = date_interval(datetime.date.today())
            starttime2 =  starttime + relativedelta(days=-1)
            endtime2   =  endtime   + relativedelta(days=-1)
        if(date_range==1):
            starttime,endtime = month_interval(datetime.date.today())
            starttime2 =  starttime + relativedelta(months=-1)
            endtime2   =  endtime   + relativedelta(months=-1)
        elif(date_range==2):
            starttime,endtime = year_interval(datetime.date.today())
            starttime2 =  starttime + relativedelta(years=-1)
            endtime2   =  endtime   + relativedelta(years=-1)
        time = {'time': {'$gte': starttime,'$lte':endtime}}

    for i in ID:
        #print(i)
        
        for j in db.find( {'ID':i   ,'time': {'$gte':starttime,'$lt':endtime} ,datatype:{'$nin':[0,None]}   } ,{'_id':0,datatype:1}).sort('time',pymongo.DESCENDING).limit(1):   #,**{'kwh':{'$gt':0,'$lt':100000}} 
            try:
                diff = diff + j[datatype]
            except:
                pass
        #print (starttime2)
        #print (endtime2)
        for j in db.find( {'ID':i    ,'time': {'$gte':starttime2,'$lt':endtime2} ,datatype:{'$nin':[0,None]}   } ,{'_id':0,datatype:1}).sort('time',pymongo.DESCENDING).limit(1):#for j in db.find( {**{'ID':i }   ,**time  } ,{'_id':0,datatype:1}).sort('time',pymongo.ASCENDING).limit(1):
            try:
                diff = diff - j[datatype]
            except:
                pass
    diff = round(diff,3)
    diff = diff if diff >= 0 else '---' #20210331 斷線收集器緊急處理
    return diff
#----------------------------------------------------------------------------------------
#取到前一小時的
#EX. 現在9:31 則取到9:00之前 aka 8:59:59:9999
# DMY用 
def diff_data_past_hour(db,collection,ID,datatype,date_range=0):
    db = db[collection]
    if(type(ID)==str):
        ID = ID.split(',')
    diff = 0

    if(date_range==3):
        time = {}
    else:
        if(date_range==0):
            starttime,endtime = date_interval(datetime.date.today())
            starttime2 =  starttime + relativedelta(days=-1)
            endtime2   =  endtime   + relativedelta(days=-1)
        if(date_range==1):
            starttime,endtime = month_interval(datetime.date.today())
            starttime2 =  starttime + relativedelta(months=-1)
            endtime2   =  endtime   + relativedelta(months=-1)
        elif(date_range==2):
            starttime,endtime = year_interval(datetime.date.today())
            starttime2 =  starttime + relativedelta(years=-1)
            endtime2   =  endtime   + relativedelta(years=-1)
        endtime = datetime.datetime.now().replace(minute=0, second=0, microsecond=0)
        time = {'time': {'$gte': starttime,'$lte':endtime}}
    for i in ID:
        #print(i)
        
        for j in db.find( {'ID':i   ,'time': {'$gte':starttime,'$lt':endtime} ,datatype:{'$nin':[0,None]}   } ,{'_id':0,datatype:1}).sort('time',pymongo.DESCENDING).limit(1):   #,**{'kwh':{'$gt':0,'$lt':100000}} 
            try:
                diff = diff + j[datatype]
            except:
                pass
        #print (starttime2)
        #print (endtime2)
        for j in db.find( {'ID':i    ,'time': {'$gte':starttime2,'$lt':endtime2} ,datatype:{'$nin':[0,None]}   } ,{'_id':0,datatype:1}).sort('time',pymongo.DESCENDING).limit(1):#for j in db.find( {**{'ID':i }   ,**time  } ,{'_id':0,datatype:1}).sort('time',pymongo.ASCENDING).limit(1):
            try:
                diff = diff - j[datatype]
            except:
                pass
    diff = round(diff,3)
    diff = diff if diff >= 0 else '---' #20210331 斷線收集器緊急處理
    return diff
#----------------------------------------------------------------------------------------

def diff_data_PR(db,collection,ID,kw,kwh,IRR,IRRh,date_range=0):
    db = db[collection]
    if(type(ID)==str):
        ID = ID.split(',')
    kwh_total = 0
    IRRh_total=0
    diff=0
    IRR=float(IRR)
    kw=float(kw)
    if(date_range==3):
        time = {}
    else:
        if(date_range==0):
            starttime,endtime = date_interval(datetime.date.today())
        if(date_range==1):
            starttime,endtime = month_interval(datetime.date.today())
        elif(date_range==2):
            starttime,endtime = year_interval(datetime.date.today())
        time = {'time': {'$gte': starttime,'$lt':endtime}}

    for i in ID:
        #print(i)
        
        for j in db.find( {'ID':i   ,'time': {'$gte':starttime,'$lt':endtime}  ,'kwh':{'$nin':[0,None]} } ,{'_id':0}).sort('time',pymongo.DESCENDING):   #,**{'kwh':{'$gt':0,'$lt':100000}} 
            #if j["kwh"]>kw*0.2:
            try:
                #print (j[kwh])
                kwh_total = kwh_total + round(j[kwh],3)
                #print ('kwh')
                #print (j["kwh"])
            except:
                pass
            
            try:
                #print (j[IRRh])
                IRRh_total = IRRh_total +round(j[IRRh],20)
                #print ('IRRh')
                #print (j["IRRh"])
            except:
                pass
        #print (kwh_total)
        #print (IRRh_total)
        
        diff=(kwh_total/kw)/(IRRh_total/IRR)*100
        #print (diff)
        #diff='---'
    diff = round(diff,3)
    diff = diff if float(diff) <= 100 else 100 #20210323 PR大於100皆為100
    return diff

#----------------------------------------------------------------------------------------
def diff_data_PSH(db,collection,ID,IRR,IRRh,date_range=0):
    db = db[collection]
    if(type(ID)==str):
        ID = ID.split(',')
    IRRh_total=0
    diff=0
    IRR=float(IRR)
    if(date_range==3):
        time = {}
    else:
        if(date_range==0):
            starttime,endtime = date_interval(datetime.date.today())
        if(date_range==1):
            starttime,endtime = month_interval(datetime.date.today())
        elif(date_range==2):
            starttime,endtime = year_interval(datetime.date.today())
        time = {'time': {'$gte': starttime,'$lt':endtime}}
    for i in ID:
        for j in db.find( {'ID':i   ,'time': {'$gte':starttime,'$lt':endtime}  ,'IRRh':{'$nin':[0,None]} } ,{'_id':0}).sort('time',pymongo.DESCENDING):   #,**{'kwh':{'$gt':0,'$lt':100000}} 
            
            try:
                IRRh_total = IRRh_total +round(j[IRRh],20)
        
            except:
                pass
   
        
        diff=(IRRh_total/IRR)
        #print (diff)
        #diff='---'
    diff = round(diff,3)
    return diff

#--------------------------------------------------------------------------------------------------------------
def current_state(db,ID):
    db = db['equipment']
    if(type(ID)==str):
        ID = ID.split(',')
    state_data = []
    for i in ID:
        state = db.find_one({'_id':ObjectId(i)},{'_id':0,'state':1})
        if(state=={} or state==None):
            state = {'state':3}
        state_data.append(state)
    return state_data
#--------------------------------------------------------------------------------------------------------------
def schedule_data(db,ID,starttime,endtime):
    schedule_data = []
    for i in range((endtime-starttime).days):
        endtime = starttime+relativedelta(days=1)
        weekday = starttime.weekday()+1
        
        weekday_dict = { "1":"Mon","2":"Tue","3":"Wed","4":"Thu","5":"Fri","6":"Sat","7":"Sun"}
        mode_name_dict = { "0":"Stop","1":"Watt/VAR Control","2":"Stable Output","3":"Smoothing","4":"Freq-Watt (Hys)","5":"Freq-Watt","6":"Voltage-VAR","7":"Volt-Watt","8":"Volt-Watt/VAR","9":"Anti-reverse","10":"Demand"}
        _db = db[weekday_dict[str(weekday)]]

        for i in _db.find({"ID":ID,"start_time": {'$gte': starttime,'$lte':endtime}}):
            i['_id'] = str(i['_id'])
            i['start'] = datetime.datetime.strftime(i['start_time'],"%Y-%m-%d %H:%M:%S")
            i['end'] = datetime.datetime.strftime(i['end_time'],"%Y-%m-%d %H:%M:%S")
            if(i['check']==0):
                i['color'] ='gray'
            elif(i['check']==1):
                i['color'] ='orange'
            elif(i['check']==2):
                i['color'] ='green'  
            i['content'] = ''
            if(i['schedule_mode']==1):
                i['title'] = 'Watt/VAR Control'
                i['content'] += 'mode:Watt/VAR Control<br>'
                i['content'] += 'PQ_p_ref:'+str(i['PQ_p_ref'])+'<br>'
                i['content'] += 'PQ_q_ref:'+str(i['PQ_q_ref'])+'<br>'
            elif(i['schedule_mode']==2):
                i['title'] = 'Stable Output'
                i['content'] += 'mode:Stable Output<br>'
                i['content'] += 'Stable_p_tr_new:'+str(i['Stable_p_tr_new'])+'<br>'
                i['content'] += 'Stable_ramp_up:'+str(i['Stable_ramp_up'])+'<br>'
                i['content'] += 'Stable_ramp_down:'+str(i['Stable_ramp_down'])+'<br>'     
            elif(i['schedule_mode']==3):
                i['title'] = 'Smoothing'
                i['content'] += 'mode:Smoothing<br>'
                i['content'] += 'Smooth_p_variance:'+str(i['Smooth_p_variance'])+'<br>'
            elif(i['schedule_mode']==4):
                i['title'] = 'Freq-Watt (Hys)'
                i['content'] += 'mode:Freq-Watt (Hys)<br>'
                i['content'] += 'FP_Hys_p_base:'+str(i['FP_Hys_p_base'])+'<br>'
                i['content'] += 'f1:'+str(i['f1_Hys_set'])+' p1:'+str(i['p1_Hys_set'])+'<br>'
                i['content'] += 'f2:'+str(i['f2_Hys_set'])+' p2:'+str(i['p2_Hys_set'])+'<br>'
                i['content'] += 'f3:'+str(i['f3_Hys_set'])+' p3:'+str(i['p3_Hys_set'])+'<br>'
                i['content'] += 'f4:'+str(i['f4_Hys_set'])+' p4:'+str(i['p4_Hys_set'])+'<br>'
                i['content'] += 'f5:'+str(i['f5_Hys_set'])+' p5:'+str(i['p5_Hys_set'])+'<br>'
                i['content'] += 'f6:'+str(i['f6_Hys_set'])+' p6:'+str(i['p6_Hys_set'])+'<br>'
            elif(i['schedule_mode']==5):
                i['title'] = 'Freq-Watt'
                i['content'] += 'mode:Freq-Watt<br>'
                i['content'] += 'FP_line_p_base:'+str(i['FP_line_p_base'])+'<br>'
                i['content'] += 'f1:'+str(i['f1_line_set'])+' p1:'+str(i['p1_line_set'])+'<br>'
                i['content'] += 'f2:'+str(i['f2_line_set'])+' p2:'+str(i['p2_line_set'])+'<br>'
                i['content'] += 'f3:'+str(i['f3_line_set'])+' p3:'+str(i['p3_line_set'])+'<br>'
                i['content'] += 'f4:'+str(i['f4_line_set'])+' p4:'+str(i['p4_line_set'])+'<br>'
                i['content'] += 'f5:'+str(i['f5_line_set'])+' p5:'+str(i['p5_line_set'])+'<br>'
                i['content'] += 'f6:'+str(i['f6_line_set'])+' p6:'+str(i['p6_line_set'])+'<br>'
            elif(i['schedule_mode']==6):
                i['title'] = 'Voltage-VAR'
                i['content'] += 'mode:Voltage-VAR<br>'
                i['content'] += 'Vq_q_base:'+str(i['Vq_q_base'])+'<br>'
                i['content'] += 'Vpq_v_base:'+str(i['Vpq_v_base'])+'<br>'
                i['content'] += 'v1:'+str(i['Vq_v1_set'])+' q1:'+str(i['Vq_q1_set'])+'<br>'
                i['content'] += 'v2:'+str(i['Vq_v2_set'])+' q2:'+str(i['Vq_q2_set'])+'<br>'
                i['content'] += 'v3:'+str(i['Vq_v3_set'])+' q3:'+str(i['Vq_q3_set'])+'<br>'
                i['content'] += 'v4:'+str(i['Vq_v4_set'])+' q4:'+str(i['Vq_q4_set'])+'<br>'
                i['content'] += 'v5:'+str(i['Vq_v5_set'])+' q5:'+str(i['Vq_q5_set'])+'<br>'
                i['content'] += 'v6:'+str(i['Vq_v6_set'])+' q6:'+str(i['Vq_q6_set'])+'<br>'
            if(i['schedule_mode']!=0):
                i['content'] += 'SOC_Max:'+str(i['soc_max'])+'<br>'
                i['content'] += 'soc_min :'+str(i['soc_min'])+'<br>'
                i['content'] += 'back_limit :'+str(i['back_limit'])+'<br>'
                i['content'] += 'C_Rate_Limit :'+str(i['C_Rate_Limit'])+'<br>'
                scale_str  = ''
                for j in i['scale']:
                    scale_str = scale_str + i['scale'][j]+','
                i['content'] += 'scale:'+'('+scale_str[0:len(scale_str)-1]+')'+'<br>'
            else:
                i['title'] = 'Stop'
                i['content'] += 'mode:Stop<br>'
            i.pop('start_time', None)
            i.pop('end_time', None)

            schedule_data.append(i)
        starttime = endtime

    return schedule_data
#--------------------------------------------------------------------------------------------------------------
def history_pcs_mode_list(db,ID,starttime,endtime):
    schedule_data = []
    mode_name_dict = { "0":"Stop","1":"Watt/VAR Control","2":"Stable Output","3":"Smoothing","4":"Freq-Watt (Hys)","5":"Freq-Watt","6":"Voltage-VAR","7":"Volt-Watt","8":"Volt-Watt/VAR","9":"Anti-reverse","10":"Demand"}
    _db = db['pcs_mode']
    #print(ID,starttime,endtime)
    for i in _db.find({"ID":ID,"time": {'$gte': starttime,'$lte':endtime}}):
        #print(i)
        i['_id'] = str(i['_id'])
        i['start'] = datetime.datetime.strftime(i['time'],"%Y-%m-%d %H:%M:%S")
        #i['end'] = datetime.datetime.strftime(i['end_time'],"%Y-%m-%d %H:%M:%S")
        i['content'] = ''
        if(i['mode']==1):
            i['title'] = 'Watt/VAR Control'
            i['content'] += 'mode:Watt/VAR Control<br>'
            i['content'] += 'PQ_p_ref:'+str(i['PQ_p_ref'])+'<br>'
            i['content'] += 'PQ_q_ref:'+str(i['PQ_q_ref'])+'<br>'
        elif(i['mode']==2):
            i['title'] = 'Stable Output'
            i['content'] += 'mode:Stable Output<br>'
            i['content'] += 'Stable_p_tr_new:'+str(i['Stable_p_tr_new'])+'<br>'
            i['content'] += 'Stable_ramp_up:'+str(i['Stable_ramp_up'])+'<br>'
            i['content'] += 'Stable_ramp_down:'+str(i['Stable_ramp_down'])+'<br>'     
        elif(i['mode']==3):
            i['title'] = 'Smoothing'
            i['content'] += 'mode:Smoothing<br>'
            i['content'] += 'Smooth_p_variance:'+str(i['Smooth_p_variance'])+'<br>'
        elif(i['mode']==4):
            i['title'] = 'Freq-Watt (Hys)'
            i['content'] += 'mode:Freq-Watt (Hys)<br>'
            i['content'] += 'FP_Hys_p_base:'+str(i['FP_Hys_p_base'])+'<br>'
            i['content'] += 'f1:'+str(i['f1_Hys_set'])+' p1:'+str(i['p1_Hys_set'])+'<br>'
            i['content'] += 'f2:'+str(i['f2_Hys_set'])+' p2:'+str(i['p2_Hys_set'])+'<br>'
            i['content'] += 'f3:'+str(i['f3_Hys_set'])+' p3:'+str(i['p3_Hys_set'])+'<br>'
            i['content'] += 'f4:'+str(i['f4_Hys_set'])+' p4:'+str(i['p4_Hys_set'])+'<br>'
            i['content'] += 'f5:'+str(i['f5_Hys_set'])+' p5:'+str(i['p5_Hys_set'])+'<br>'
            i['content'] += 'f6:'+str(i['f6_Hys_set'])+' p6:'+str(i['p6_Hys_set'])+'<br>'
        elif(i['mode']==5):
            i['title'] = 'Freq-Watt'
            i['content'] += 'mode:Freq-Watt<br>'
            i['content'] += 'FP_line_p_base:'+str(i['FP_line_p_base'])+'<br>'
            i['content'] += 'f1:'+str(i['f1_line_set'])+' p1:'+str(i['p1_line_set'])+'<br>'
            i['content'] += 'f2:'+str(i['f2_line_set'])+' p2:'+str(i['p2_line_set'])+'<br>'
            i['content'] += 'f3:'+str(i['f3_line_set'])+' p3:'+str(i['p3_line_set'])+'<br>'
            i['content'] += 'f4:'+str(i['f4_line_set'])+' p4:'+str(i['p4_line_set'])+'<br>'
            i['content'] += 'f5:'+str(i['f5_line_set'])+' p5:'+str(i['p5_line_set'])+'<br>'
            i['content'] += 'f6:'+str(i['f6_line_set'])+' p6:'+str(i['p6_line_set'])+'<br>'
        elif(i['mode']==6):
            i['title'] = 'Voltage-VAR'
            i['content'] += 'mode:Voltage-VAR<br>'
            i['content'] += 'Vq_q_base:'+str(i['Vq_q_base'])+'<br>'
            i['content'] += 'Vpq_v_base:'+str(i['Vpq_v_base'])+'<br>'
            i['content'] += 'v1:'+str(i['Vq_v1_set'])+' q1:'+str(i['Vq_q1_set'])+'<br>'
            i['content'] += 'v2:'+str(i['Vq_v2_set'])+' q2:'+str(i['Vq_q2_set'])+'<br>'
            i['content'] += 'v3:'+str(i['Vq_v3_set'])+' q3:'+str(i['Vq_q3_set'])+'<br>'
            i['content'] += 'v4:'+str(i['Vq_v4_set'])+' q4:'+str(i['Vq_q4_set'])+'<br>'
            i['content'] += 'v5:'+str(i['Vq_v5_set'])+' q5:'+str(i['Vq_q5_set'])+'<br>'
            i['content'] += 'v6:'+str(i['Vq_v6_set'])+' q6:'+str(i['Vq_q6_set'])+'<br>'
        if(i['mode']!=0):
            i['content'] += 'SOC_Max:'+str(i['soc_max'])+'<br>'
            i['content'] += 'soc_min :'+str(i['soc_min'])+'<br>'
            i['content'] += 'back_limit :'+str(i['back_limit'])+'<br>'
            i['content'] += 'C_Rate_Limit :'+str(i['C_Rate_Limit'])+'<br>'
            scale_str  = ''
            for j in i['scale']:
                scale_str = scale_str + i['scale'][j]+','
            i['content'] += 'scale:'+'('+scale_str[0:len(scale_str)-1]+')'+'<br>'
        else:
            i['title'] = 'Stop'
            i['content'] += 'mode:Stop<br>'
        i.pop('start_time', None)
        i.pop('end_time', None)

        schedule_data.append(i)
    starttime = endtime

    return schedule_data
#--------------------------------------------------------------------------------------------------------------
def current_equip(db,ID):
    db = db['equipment']
    if(type(ID)==str):
        ID = ID.split(',')
    equip_data = []
    for i in ID:
        equip_data.append(db.find_one({'_id':ObjectId(i)},{'_id':0}))
    return equip_data
#--------------------------------------------------------------------------------------------------------------------
def tonum(num):
    try:
        return float(num)
    except:
        return 0
#--------------------------------------------------------------------------------------------------------------------
def inverter_mode_translation(mode, model):
    dict1 = {
        'M70A': {
            'Standby': '待機',
            'Countdown': 'Countdown',
            'On': '運轉',
            'No DC': '無DC',
            'Alarm': '警報',
            'CHECK_PV_POWER': '檢查PV電源'
        },
        'SG110CX': {
            'Run': '運轉',
            'Stop': '停止',
            'Initial standby': '待機：初始化',
            'Key stop': 'Key stop',
            'Standby': '待機',
            'Emergency Stop': '緊急停機',
            'Starting': '啟動',
            'Fault': '錯誤',
            'Alarm run': 'Alarm run',
            'Derating run': '降額運轉',
            'Dispatch run': '調度運轉',
            'Communicate fault': '通訊異常'
        },
        'sun2000-100ktl': {
            '0': '待機：初始化',
            '1': '待機：絕緣阻抗檢測',
            '2': '待機：光照檢測',
            '3': '待機：電網檢測',
            '256': '啟動',
            '512': '運轉',
            '513': '功率限制運轉',
            '514': '降額運轉',
            '768': '關機：異常指令',
            '769': '關機：指令關機',
            '770': '關機：OVGR',
            '771': '關機：通信中斷',
            '772': '關機：功率限制',
            '773': '關機：需手動開機',
            '774': '關機：直流開關斷開',
            '1025': 'cos曲線調度運轉',
            '1026': 'Q-U曲線調度運轉',
            '40960': '待機：無光照', 
            '1280': '點檢就緒',
            '1281': '點檢中',
            '1536': '巡檢中', 
            '1792': 'AFCI自我檢測',
            '2048': 'IV掃描中',
            '2304': '直流輸入檢測'
        }
    }
    if model not in dict1:   #無對應翻譯 回傳原始上傳資料
        return mode
    tran_dict = dict1[model]
    try:
        if mode in tran_dict:   #有翻譯回傳翻譯
            return tran_dict[mode]
        #無翻譯
        if len(mode) >= 7 and mode[:7] == 'Unknown':
            if mode == 'Unknown':
                return '未知狀態(無代碼)'
            try:
                code = mode.split('_', 1)[1]
                return '未知狀態代碼:'+str(code)
            except:    
                return '未知狀態'+str(mode[7:])
    except:
        return mode
    return mode
#--------------------------------------------------------------------------------------------------------------------
def get_weather_forecast(db, city):
    try:
        data = get_weather_forecast_by_date(db, city)
        data['Wx'] = data["Wx"]['zh-TW']
        return data
    except:
        return {}
#--------------------------------------------------------------------------------------------------------------------
# New Func
# Wx corresponds to more images
def get_weather_forecast_by_date(db, city, date=None):
    try:
        find_filter = {}
        # today
        if date == None or date < datetime.datetime.now() + datetime.timedelta(minutes=1):
            date = datetime.datetime.now()
            find_filter = {'ID': city, 'time': {'$gte': date}, 'PoP6h': {'$exists': True}}
        else:
            # 搜尋早上的天氣
            date  = date.replace(hour=5, minute=0, second=0, microsecond=0)
            find_filter = {'ID': city, 'time': {'$gte': date}, 'PoP12h': {'$exists': True}}
        data = {}
        for _data in db.weather_forecast.find(find_filter).sort('time', 1).limit(1):
            data = _data

            # Wx to image
            Wx_to_image = db.parameter_setting.find_one({'method': 'weather_image'})
            if Wx_to_image != None and Wx_to_image.get("Wx_to_image", {}).get( _data["Wx"], None) != None:
                data['imgurl'] = './imgs/weather/{}'.format(Wx_to_image.get("Wx_to_image", {}).get( _data["Wx"], None))
            else: # Not in database
                # Will use simplify condition
                Wx = _data["Wx"]
                if '雨' in Wx or '雪' in Wx:
                   data['imgurl'] = './imgs/weather/rainy.svg'
                elif '陰' in Wx:
                    data['imgurl'] = './imgs/weather/cloudy.svg'
                elif '晴' in Wx and '雲'  in Wx:
                    data['imgurl'] = './imgs/weather/partly_cloudy.svg'
                elif '晴' in Wx and '雲' not in Wx and '雨' not in Wx:
                    data['imgurl'] = './imgs/weather/sunny.svg'
                else:
                    data['imgurl'] = './imgs/weather/mostly_clear.svg'

            # translate Wx_i18n
            Wx_i18n = db.parameter_setting.find_one({'method': 'weather_Wx_i18n'})
            if Wx_i18n != None and "Wx" in _data:
                data["Wx"] = Wx_i18n.get('Wx_i18n', {}).get(_data["Wx"], {'zh-TW': _data["Wx"]})
            else:
                data["Wx"] = {'zh-TW': _data["Wx"]}
            
            #print(_data)
    except Exception as e:
        print(e)
        data = {}
    return data
#--------------------------------------------------------------------------------------------------------------------
def schedule_interval_format(repeat, repeat_interval, lang='zh-tw'):
    if repeat == 'none':
        return {'zh-tw': '不重複', 'en-us': 'No Repeat'}.get(lang, '不重複')
    elif repeat == 'temporary':
        return {'zh-tw': '臨時', 'en-us': 'Temporary'}.get(lang, '臨時')
    else:
        format_str = '{}{}'.format({'zh-tw': '每', 'en-us': 'Every '}.get(lang, '每'), repeat_interval)
        if repeat == 'week':
            format_str += {'zh-tw': '週', 'en-us': ' Week'}.get(lang, '週')
        elif repeat == 'month':
            format_str += {'zh-tw': '月', 'en-us': ' Month'}.get(lang, '月')
        elif repeat == 'quarter':
            format_str += {'zh-tw': '季', 'en-us': ' Quarter'}.get(lang, '季')
        elif repeat == 'half_year':
            format_str += {'zh-tw': '半年', 'en-us': ' Half Year'}.get(lang, '半年')
        elif repeat == 'year':
            format_str += {'zh-tw': '年', 'en-us': ' Year'}.get(lang, '年')
    return format_str
#--------------------------------------------------------------------------------------------------------------------
def plant_group_ID_find_sun_ID(db, ID, col):
    ID = str(ID)
    sun = None
    if col in ['pv_plant', 'plant']:
        for plant in db.plant.find({'_id': ObjectId(ID)}).limit(1):
            sun = db.equipment.find_one({
                'PV': {'$all': [plant.get('name', None)]}, 'type': 'sun', 'main_sun': 1})
    elif col in ['pv_lgroup', 'pv_group']:
        for equip in db.equipment.find({'_id': ObjectId(ID)}).limit(1):
            if col == 'pv_lgroup':
                sun = db.equipment.find_one({
                    'PV': {'$all': [equip.get('PV', None)]}, 'lgroup': equip.get('name'), 
                    'type': 'sun', 'main_sun': 1
                })
            else:
                for sensor in db.equipment.find({
                    'PV': {'$all': [equip.get('PV', None)]}, 'lgroup': equip.get('lgroup'), 'group': equip.get('name'),
                    'type': 'sun', 'main_sun': 1
                }):
                    try:
                        if type(sensor['lgroup']) == list and type(sensor['group']) == list:
                            for i in range(len(sensor['lgroup'])):
                                if sensor['lgroup'][i] == equip.get('lgroup') and sensor['group'][i] == equip.get('name'):
                                    sun = sensor
                        else:
                            sun = sensor
                    except:
                        continue
    try:
        return str(sun['_id'])
    except:
        return None
#--------------------------------------------------------------------------------------------------------------------
# Migrated from Ryan's Code
def equipment_name_change(db, get_json: dict, update_button=1):
    if 'collection' not in get_json:
        return False, 'collection'
    if get_json['collection'] == 'pv_plant':
        name = get_json['name']
        rename = get_json['rename']
        # check whether name duplicated
        check_name_condition = {'name':rename }
        check_name_list = list( db['plant'].find(check_name_condition) )
        if len(check_name_list) == 0:

            # plant
            condition = {'name':name }
            equipment = list( db['plant'].find(condition) )
            for i in range(len(equipment)):
                print(equipment[i])
                condition1 = {'_id':equipment[i]['_id']}
                set_condition1 = {'name':rename}
                print(condition1,set_condition1)
                if update_button == 1:
                    db['plant'].update_one(condition1,{'$set':set_condition1})
                    # user plant rename
                    for user in db.users.find({'plant': name}):
                        try:
                            index = user.get('plant', []).index(name)
                            user.get('plant', [])[index] = rename
                            db.users.update_one({'_id': user['_id']}, {'$set': {'plant': user['plant']}})
                        except:
                            pass

                print('===========================================')
            print(len( equipment ))

            # group & inverter & string meter & sensor & pv_meter
            condition = {'PV': name }
            equipment = list( db['equipment'].find(condition) )
            for i in range(len(equipment)):
                if type(equipment[i]['PV']) != list:
                    print(equipment[i])
                    condition1 = {'_id':equipment[i]['_id']}
                    if 'treeview' in equipment[i]:
                        set_condition1 = {'PV':rename}

                        name_list = equipment[i]['treeview']
                        name_list['PV'] = rename
                        set_condition1['treeview'] = name_list
                    else:
                        set_condition1 = {'PV':rename}
                    print(condition1,set_condition1)
                    if update_button == 1:
                        db['equipment'].update_one(condition1,{'$set':set_condition1})
                else:
                    print(equipment[i])
                    name_list = equipment[i]['PV']
                    for name_lists in range(len(name_list)):
                        if name_list[name_lists] == name:
                            name_list[name_lists] = rename
                    condition1 = {'_id':equipment[i]['_id']}
                    set_condition1 = {'PV':name_list}
                    print(condition1,set_condition1)
                    if update_button == 1:
                        db['equipment'].update_one(condition1,{'$set':set_condition1})
                print('===========================================')
            print(len( equipment ))
            return True, None
        else:
            print('{} name deplicated.'.format(get_json['collection']))
            return False, "duplicated"
    elif get_json['collection'] == 'pv_lgroup':
        pv_name  = get_json['PV']
        name = get_json['name']
        rename = get_json['rename']

        # check whether name duplicated
        check_name_condition = {'PV': pv_name,'name':rename }
        check_name_list = list( db['equipment'].find(check_name_condition) )
        if len(check_name_list) == 0:
            # lgroup
            condition = {'PV': pv_name,'name':name }
            equipment = list( db['equipment'].find(condition) )
            for i in range(len(equipment)):
                print(equipment[i])
                condition1 = {'_id':equipment[i]['_id']}
                set_condition1 = {'name':rename}
                print(condition1,set_condition1)
                if update_button == 1:
                    db['equipment'].update_one(condition1,{'$set':set_condition1})
                print('===========================================')
            print(len( equipment ))

            # group & inverter & string meter & sensor & pv_meter
            condition = {'PV': pv_name,'lgroup':name }
            equipment = list( db['equipment'].find(condition) )
            for i in range(len(equipment)):
                if type(equipment[i]['lgroup']) != list:
                    print(equipment[i])
                    condition1 = {'_id':equipment[i]['_id']}
                    if 'treeview' in equipment[i]:
                        set_condition1 = {'lgroup':rename}

                        name_list = equipment[i]['treeview']
                        name_list['lgroup'] = rename
                        set_condition1['treeview'] = name_list
                    else:
                        set_condition1 = {'lgroup':rename}
                    print(condition1,set_condition1)
                    if update_button == 1:
                        db['equipment'].update_one(condition1,{'$set':set_condition1})
                else:
                    print(equipment[i])
                    name_list = equipment[i]['lgroup']
                    for name_lists in range(len(name_list)):
                        if name_list[name_lists] == name:
                            name_list[name_lists] = rename
                    condition1 = {'_id':equipment[i]['_id']}
                    set_condition1 = {'lgroup':name_list}
                    print(condition1,set_condition1)
                    if update_button == 1:
                        db['equipment'].update_one(condition1,{'$set':set_condition1})
                print('===========================================')
            print(len( equipment ))
            return True, None
        else:
            print('{} name deplicated.'.format(get_json['collection']))
            return False, "duplicated"
    elif get_json['collection'] == 'pv_group':
        pv_name = get_json['PV']
        lgroup_name = get_json['lgroup']
        name = get_json['name']
        rename = get_json['rename']

        # check whether name duplicated
        check_name_condition = {'PV': pv_name, 'lgroup': lgroup_name,'name':rename }
        check_name_list = list( db['equipment'].find(check_name_condition) )
        if len(check_name_list) == 0:

            # group
            condition = {'PV': pv_name, 'lgroup': lgroup_name,'name':name }
            equipment = list( db['equipment'].find(condition) )
            for i in range(len(equipment)):
                print(equipment[i])
                condition1 = {'_id':equipment[i]['_id']}
                set_condition1 = {'name':rename}
                print(condition1,set_condition1)
                if update_button == 1:
                    db['equipment'].update_one(condition1,{'$set':set_condition1})
                print('===========================================')
            print(len( equipment ))

            # inverter & string meter & sensor & pv_meter
            condition = {'PV': pv_name, 'lgroup': lgroup_name,'group':name }
            equipment = list( db['equipment'].find(condition) )
            for i in range(len(equipment)):
                if type(equipment[i]['group']) != list:
                    print(equipment[i])
                    condition1 = {'_id':equipment[i]['_id']}
                    if 'treeview' in equipment[i]:
                        set_condition1 = {'group':rename}

                        name_list = equipment[i]['treeview']
                        name_list['group'] = rename
                        set_condition1['treeview'] = name_list
                    else:
                        set_condition1 = {'group':rename}
                    print(condition1,set_condition1)
                    if update_button == 1:
                        db['equipment'].update_one(condition1,{'$set':set_condition1})
                else:
                    print(equipment[i])
                    name_list = equipment[i]['group']
                    for name_lists in range(len(name_list)):
                        if name_list[name_lists] == name:
                            name_list[name_lists] = rename
                    condition1 = {'_id':equipment[i]['_id']}
                    set_condition1 = {'group':name_list}
                    print(condition1,set_condition1)
                    if update_button == 1:
                        db['equipment'].update_one(condition1,{'$set':set_condition1})
                print('===========================================')
            print(len( equipment ))
            return True, None
        else:
            print('{} name deplicated.'.format(get_json['collection']))
            return False, "duplicated"
    elif get_json['collection'] == 'inverter':
        pv_name = get_json['PV']
        lgroup_name = get_json['lgroup']
        group_name = get_json['group']
        name = get_json['name']
        rename = get_json['rename']

        # check whether name duplicated
        check_name_condition = {'PV': pv_name, 'lgroup': lgroup_name,'group' : group_name,'name':rename }
        check_name_list = list( db['equipment'].find(check_name_condition) )
        if len(check_name_list) == 0: 

            # inverter
            condition = {'PV': pv_name, 'lgroup': lgroup_name,'group' : group_name,'name':name }
            equipment = list( db['equipment'].find(condition) )
            for i in range(len(equipment)):
                print(equipment[i])
                condition1 = {'_id':equipment[i]['_id']}
                set_condition1 = {'name':rename}
                print(condition1,set_condition1)
                if update_button == 1:
                    db['equipment'].update_one(condition1,{'$set':set_condition1})
                print('===========================================')
            print(len( equipment ))

            # string meter
            condition = {'PV': pv_name, 'lgroup': lgroup_name,'group' : group_name,'inv':name }
            equipment = list( db['equipment'].find(condition) )
            for i in range(len(equipment)):
                print(equipment[i])
                condition1 = {'_id':equipment[i]['_id']}
                set_condition1 = {'inv':rename}
                print(condition1,set_condition1)
                if update_button == 1:
                    db['equipment'].update_one(condition1,{'$set':set_condition1})
                print('===========================================')
            print(len( equipment ))
            return True, None
        else:
            print('{} name deplicated.'.format(get_json['collection']))
            return False, "duplicated"
    elif get_json['collection'] == 'string_meter':
        pv_name = get_json['PV']
        lgroup_name = get_json['lgroup']
        group_name = get_json['group']
        inv_name = get_json['inv']
        name = get_json['name']
        rename = get_json['rename']

        # check whether name duplicated
        check_name_condition = {'PV': pv_name, 'lgroup': lgroup_name,'group' : group_name,'inv':inv_name,'name':rename }
        check_name_list = list( db['equipment'].find(check_name_condition) )
        if len(check_name_list) == 0:        
            
            # string meter
            condition = {'PV': pv_name, 'lgroup': lgroup_name,'group' : group_name,'inv':inv_name,'name':name }
            equipment = list( db['equipment'].find(condition) )
            for i in range(len(equipment)):
                print(equipment[i])
                condition1 = {'_id':equipment[i]['_id']}
                set_condition1 = {'name':rename}
                print(condition1,set_condition1)
                if update_button == 1:
                    db['equipment'].update_one(condition1,{'$set':set_condition1})
                print('===========================================')
            print(len( equipment ))
            return True, None
        else:
            print('{} name deplicated.'.format(get_json['collection']))
            return False, "duplicated"
    elif get_json['collection'] == 'sensor':
        pv_name = get_json['PV']
        lgroup_name = get_json['lgroup']
        group_name = get_json['group']
        name = get_json['name']
        rename = get_json['rename']

        # check whether name duplicated
        check_name_condition = {'PV': pv_name, 'lgroup': lgroup_name,'group' : group_name,'name':rename }
        check_name_list = list( db['equipment'].find(check_name_condition) )
        if len(check_name_list) == 0:        
            
            # string meter
            condition = {'PV': pv_name, 'lgroup': lgroup_name,'group' : group_name,'name':name }
            equipment = list( db['equipment'].find(condition) )
            for i in range(len(equipment)):
                print(equipment[i])
                condition1 = {'_id':equipment[i]['_id']}
                set_condition1 = {'name':rename}
                print(condition1,set_condition1)
                if update_button == 1:
                    db['equipment'].update_one(condition1,{'$set':set_condition1})
                print('===========================================')
            print(len( equipment ))
            return True, None
        else:
            print('{} name deplicated.'.format(get_json['collection']))
            return False, "duplicated"







