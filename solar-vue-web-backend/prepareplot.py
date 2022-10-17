
from os import name
from re import I
import pymongo
import datetime
import time 
from dateutil.relativedelta import relativedelta
from bson.objectid import ObjectId
from statistics import mean
import hashlib
import requests
#----------------------------------------------------------------------------------------
def year_len(date_start,date_end):

    year_len=0
    if date_start<=date_end:
        date_end += relativedelta(months=1)
        #跨年份 ex. 2020/12/01 - 2021/01/31 month直接相減 會變成-10
        year_len = (date_end.year - date_start.year)*12 + date_end.month - date_start.month
    year_len=int(year_len)
    return year_len
#----------------------------------------------------------------------------------------
def month_len(date_start,date_end):

    month_len=0
    if date_start<=date_end:
        date_end += datetime.timedelta(days=1)
        month_len = (date_end - date_start).total_seconds() / 86400
    month_len=int(month_len)
    return month_len
#----------------------------------------------------------------------------------------
def day_len(date_start,date_end):

    day_len=0
    if date_start<=date_end:
        date_start = date_start + relativedelta(hour=0,minute=0,second=0)
        date_end = date_end +  relativedelta(days=+1,hour=0,minute=0,second=0)
        day_len = (date_end - date_start).total_seconds() / (86400/24)
    day_len=int(day_len)
    return day_len
#---------------------------------------------------------------------------------------
def fix_x_xis(date=datetime.date.today(),interval=1):
    x_axis =[]
   
    nexttime = datetime.datetime.combine(date, datetime.time.min)
    deltatime = datetime.timedelta(seconds=interval)

    for i in range(int(86400/interval)):
        x_axis.append(datetime.datetime.strftime(nexttime,"%Y-%m-%d %H:%M:%S"))
        nexttime  = nexttime + deltatime 
    return x_axis
#---------------------------------------------------------------------------------------
def fix_x_xis_date(date_start=datetime.date.today(),date_end=datetime.date.today(),date_range=1, interval=60):
    x_axis =[]
    if date_range==0:
        # interval unit is second, default set to 60 sec
        real_time_len=0
        if date_start<=date_end:
            date_start = date_start + relativedelta(hour=0,minute=0,second=0)
            date_end = date_end + relativedelta(days=+1,hour=0,minute=0,second=0)
            real_time_len = (date_end - date_start).total_seconds()/interval
        

        real_time_len=int(real_time_len)
        deltatime = datetime.timedelta(seconds=interval)

        #print (day_len)
        nexttime = datetime.datetime.combine(date_start, datetime.time.min)

        for i in range(real_time_len):
            #print (i)
            x_axis.append(datetime.datetime.strftime(nexttime,"%Y-%m-%d %H:%M"))
            nexttime  = nexttime + deltatime 
    elif date_range==1:
        day_len=0
        if date_start<=date_end:
            date_start = date_start + relativedelta(hour=0,minute=0,second=0)
            date_end = date_end + relativedelta(days=+1,hour=0,minute=0,second=0)
            day_len = (date_end - date_start).total_seconds() / (86400/24)
        

        day_len=int(day_len)
        deltatime = datetime.timedelta(hours=1)

        #print (day_len)
        nexttime = datetime.datetime.combine(date_start, datetime.time.min)

        for i in range(day_len):
            #print (i)
            x_axis.append(datetime.datetime.strftime(nexttime,"%Y-%m-%d %H"))
            nexttime  = nexttime + deltatime 
    elif date_range==2:
        month_len=0
        if date_start<=date_end:
            date_end = date_end + datetime.timedelta(days=1)
            month_len = (date_end - date_start).total_seconds() / 86400
        month_len=int(month_len)

        deltatime = datetime.timedelta(days=1)

        #print (month_len)
        nexttime = date_start
        for i in range(month_len):
            #print (i)
            x_axis.append(datetime.datetime.strftime(nexttime,"%Y-%m-%d"))
            nexttime  = nexttime + deltatime
    elif date_range==3:
        year_len=0
        if date_start<=date_end:
            date_end = date_end + relativedelta(months=1)
            year_len = (date_end.year - date_start.year)*12 + date_end.month - date_start.month
        #print(date_start)
        #print(date_end)
        year_len=int(year_len)
        deltatime = relativedelta(months=+1)

        #print (year_len)
        nexttime = date_start

        for i in range(year_len):
            #print (i)
            x_axis.append(datetime.datetime.strftime(nexttime,"%Y-%m"))
            nexttime  = nexttime + deltatime
    elif date_range==4:
        allyear_len=0
        if date_start<=date_end:
            date_end = date_end + relativedelta( years=1)
            allyear_len = (date_end.year - date_start.year)

        #print(date_start)
        #print(date_end)
        allyear_len=int(allyear_len)
        deltatime = relativedelta(years=+1)

        #print (year_len)
        nexttime = date_start

        for i in range(allyear_len):
            #print (i)
            x_axis.append(datetime.datetime.strftime(nexttime,"%Y"))
            nexttime  = nexttime + deltatime
    #print (x_axis)
    return x_axis
#------------------------------------------------------------------------------------
def date_interval(date=datetime.date.today()):
    starttime = datetime.datetime.combine(date, datetime.time.min)
    endtime = starttime+datetime.timedelta(days=1)
    return starttime,endtime
#------------------------------------------------------------------------------------
def week_interval(date=datetime.date.today()):
    starttime = datetime.datetime.combine(date, datetime.time.min)
    endtime = starttime+datetime.timedelta(days=7)
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
#------------------------------------------------------------------------------------
def stopn(interval = 1):
    date=datetime.date.today()
    starttime = datetime.datetime.combine(date, datetime.time.min)
    localtime = datetime.datetime.now()
    stop_n = int((localtime - starttime).total_seconds()/interval)
    return stop_n
#---------------------------------------------------------------------------------------
def math_index(y_axis,layer = 1):
    _min = []
    _max = []
    _avg = []
    _total = []
    if(layer==1):
        mi = {}
        ma = {}
        avg = {}
        total={}
        _y_axis = list(filter(Noneor0,y_axis))
        if(_y_axis!=[]):
            mi_num = min(_y_axis)
            mi['value'] = mi_num
            mi['time'] = y_axis.index(mi_num)
            ma_num = max(_y_axis)
            ma['value'] = ma_num
            ma['time'] = y_axis.index(ma_num)
            avg['value'] = mean(_y_axis)
            total['value'] = sum(_y_axis)
            _min.append(mi)
            _max.append(ma)
            _avg.append(avg)
            _total.append(total)
        else:
            mi['value'] = '---'
            mi['time'] = None
            ma['value'] = '---'
            ma['time'] = None
            avg['value'] = '---'
            total['value'] = '---'
            _min.append(mi)
            _max.append(ma)
            _avg.append(avg)
            _total.append(total)
    elif(layer==2):
        for i in range(layer):
            
            mi = {}
            ma = {}
            avg = {}
            total={}
            _y_axis1 = y_axis[i]
            _y_axis = list(filter(Noneor0,_y_axis1))
            if(_y_axis!=[]):
                mi_num = min(_y_axis)
                mi['value'] = mi_num
                mi['time'] = _y_axis1.index(mi_num)
                ma_num = max(_y_axis)
                ma['value'] = ma_num
                ma['time'] = _y_axis1.index(ma_num)
                avg['value'] = mean(_y_axis)
                
                total['value'] = sum(_y_axis)

                _min.append(mi)
                _max.append(ma)
                _avg.append(avg)
                _total.append(total)
            else:
                mi['value'] = '---'
                mi['time'] = None
                ma['value'] = '---'
                ma['time'] = None
                avg['value'] = '---'
                total['value'] = '---'
                _min.append(mi)
                _max.append(ma)
                _avg.append(avg)
                _total.append(total)
    elif(layer==3):
        mi = {}
        ma = {}
        avg = {}
        total={}
        _y_axis = list(filter(Noneor0,y_axis))
        if(_y_axis!=[]):
            mi_num = min(_y_axis)
            mi['value'] = mi_num
            mi['time'] = y_axis.index(mi_num)
            ma_num = max(_y_axis)
            ma['value'] = ma_num
            ma['time'] = y_axis.index(ma_num)
            avg['value'] = mean(_y_axis)
            #print (_y_axis)
            total['value'] = sum(_y_axis)

            _min.append(mi)
            _max.append(ma)
            _avg.append(avg)
            _total.append(total)
        else:
            mi['value'] = '---'
            mi['time'] = None
            ma['value'] = '---'
            ma['time'] = None
            avg['value'] = '---'
            total['value'] = '---'

            _min.append(mi)
            _max.append(ma)
            _avg.append(avg)
            _total.append(total)
    return _min,_max,_avg,_total
#---------------------------------------------------------------------------------------
def math_index_string(y_axis,layer = 1):
    _min = []
    _max = []
    _avg = []
    _total = []
    
    for i in range(layer):
        
        mi = {}
        ma = {}
        avg = {}
        total={}
        _y_axis1 = y_axis[i]
        _y_axis = list(filter(Noneor0,_y_axis1))
        if(_y_axis!=[]):
            mi_num = min(_y_axis)
            mi['value'] = mi_num
            mi['time'] = _y_axis1.index(mi_num)
            ma_num = max(_y_axis)
            ma['value'] = ma_num
            ma['time'] = _y_axis1.index(ma_num)
            avg['value'] = mean(_y_axis)
            
            total['value'] = sum(_y_axis)

            _min.append(mi)
            _max.append(ma)
            _avg.append(avg)
            _total.append(total)
        else:
            mi['value'] = '---'
            mi['time'] = None
            ma['value'] = '---'
            ma['time'] = None
            avg['value'] = '---'
            total['value'] = '---'
            _min.append(mi)
            _max.append(ma)
            _avg.append(avg)
            _total.append(total)
    
    return _min,_max,_avg,_total
#---------------------------------------------------------------------------------------
def Noneor0(x):
    if(x==0 or x==None):
        return False
    else:
        return True
#---------------------------------------------------------------------------------------
def dayline_one(db,collection,ID,datatype,date_start=datetime.date.today(),date_end=datetime.date.today(),interval=1,match=None):
    db = db[collection]
    starttime,endtimeX = date_interval(date_start)
    starttimeX,endtime = date_interval(date_end)

    #print ((date_end-date_start).days)

    num = int((endtime-starttime).total_seconds()/interval)
    y = [None] * num
    #條件
    if match == None:
        match = {}
    match.update({                                
        'ID':ID,
        'time': {
            '$gte': starttime,
            '$lte': endtime,
        },
    datatype:{'$exists':True}
    })
    #群組
    group =  {
        '_id': ID,
        'time': {  '$push': "$time"  },
        datatype : { '$push': "$"+datatype  }
    }  
    #資料
    data = list(db.aggregate(
        [
            {'$match': match},
            {"$project":{"_id":0,'time':1,datatype:1}},  
            { '$limit' : 178560 },
            #{'$sort': {'time':1}}, 
            {'$group': group},
        ]
    ))
    if(data!=[]):
        for i,time in enumerate(data[0]['time']):
            diff = time - starttime 
            n = int(diff.total_seconds()/interval) 
            try: 
                if isinstance(data[0][datatype][i], (int, float)):
                    y[n] = round(data[0][datatype][i],3)
                else:
                    y[n] = data[0][datatype][i]
            except:
                pass
    return y
#--------------------------------------------------------------------------------
def dayline_one_update(db,collection,ID,datatype,date_start=datetime.date.today(),date_end=datetime.date.today(),interval=1):
    db = db[collection]
    starttime,endtimeX = date_interval(date_start)
    starttimeX,endtime = date_interval(date_end)
    num = int((endtime-starttime).total_seconds()/interval)
    #條件
    match = {                                
        'ID':ID,
        'time': {
            '$gte': starttime,
            '$lte': endtime,
        },

    datatype:{'$exists':True}
    }

    #群組
    group =  {
        '_id': ID,
        'time': {  '$push': "$time"  },
        datatype : { '$push': "$"+datatype  }
    }  
    data = list(db.aggregate(
        [
            {'$match': match},         
            {"$project":{"_id":0,'time':1,datatype:1}},
            {'$sort': {'time':-1}}, 
            {'$limit': 30},
            {'$group': group},
        ]
    ))
    y= []
    if(data!=[]):   
        stop_n = 0
        start_n = 0 
        for i,time in enumerate(data[0]['time']):
            diff = time - starttime 
            n = int(diff.total_seconds()/interval) 
            if(i==0):
                stop_n = n
            else:
                start_n = n
            try: 
                y.append( [round(data[0][datatype][i],3),n] )
            except:
                pass
    return y
#----------------------------------------------------------------------
def dayline_three(db,collection,ID,datatype1,datatype2,datatype3,date_start=datetime.date.today(),date_end=datetime.date.today(),interval=1):
    db = db[collection]
    starttime,endtimeX = date_interval(date_start)
    starttimeX,endtime = date_interval(date_end)
    num = int((endtime-starttime).total_seconds()/interval)
    #print(interval)
    y = [ [ None for i in range(num)] for j in range(3)]
    
    #條件
    #print(datatype1,datatype2,datatype3)
    match = {                                
        'ID':ID,
        'time': {
            '$gte': starttime,
            '$lte': endtime,
        },
    datatype:{'$exists':True}
    }
    #群組
    group =  {
        '_id': ID,
        'time': {  '$push': "$time"  },
        datatype1 : { '$push': "$"+datatype1  },
        datatype2 : { '$push': "$"+datatype2  },
        datatype3 : { '$push': "$"+datatype3  },
    }  
    #資料
    data = list(db.aggregate(
        [
            {'$match': match},
            {"$project":{"_id":0,'time':1,datatype1:1,datatype2:1,datatype3:1}},  
            {'$limit': 86000},
            {'$sort': {'time':1}}, 
            {'$group': group},
        ]
    ))
    
    if(data!=[]):
        for i,time in enumerate(data[0]['time']):
            diff = time - starttime 
            n = int(diff.total_seconds()/interval) 
            try: 
                y[0][n] = data[0][datatype1][i]
            except:
                pass
            try: 
                y[1][n] = data[0][datatype2][i]
            except:
                pass
            try: 
                y[2][n] = data[0][datatype3][i]
            except:
                pass
    return y
#----------------------------------------------------------------------
def dayline_three_update(db,collection,ID,datatype1,datatype2,datatype3,date_start=datetime.date.today(),date_end=datetime.date.today(),interval=1):
    db = db[collection]
    starttime,endtimeX = date_interval(date_start)
    starttimeX,endtime = date_interval(date_end)
    num = int((endtime-starttime).total_seconds()/interval)
    y = [ [ None for i in range(num)] for j in range(3)]
    #條件
    match = {                                
        'ID':ID,
        'time': {
            '$gte': starttime,
            '$lte': endtime,
        },
    datatype:{'$exists':True}
    }
    #群組
    group =  {
        '_id': ID,
        'time': {  '$push': "$time"  },
        datatype1 : { '$push': "$"+datatype1  },
        datatype2 : { '$push': "$"+datatype2  },
        datatype3 : { '$push': "$"+datatype3  },
    }  
    #資料
    data = list(db.aggregate(
        [
            {'$match': match},
            {"$project":{"_id":0,'time':1,datatype1:1,datatype2:1,datatype3:1}}, 
            {'$sort': {'time':-1}}, 
            {'$limit': 30}, 
            {'$group': group},
        ]
    ))
    
    if(data!=[]):
        stop_n = 0
        start_n = 0
        for i,time in enumerate(data[0]['time']):
            diff = time - starttime 
            n = int(diff.total_seconds()/interval) 
            if(i==0):
                stop_n = n
            else:
                start_n = n
            try: 
                y[0][n] = [data[0][datatype1][i],n]
            except:
                pass
            try: 
                y[1][n] = [data[0][datatype2][i],n]
            except:
                pass
            try: 
                y[2][n] = [data[0][datatype3][i],n]
            except:
                pass
        y[0] = y[0][start_n:stop_n+1]
        y[1] = y[1][start_n:stop_n+1]
        y[2] = y[2][start_n:stop_n+1]
    return y
#---------------------------------------------------------------------------------------
def day_multi_line(db,find,date_start=datetime.date.today(),date_end=datetime.date.today()):
    y = []
    for index,j in enumerate(find):
        starttime,endtimeX = date_interval(date_start)
        starttimeX,endtime = date_interval(date_end)
        _db = db[j['collection']]
        #print (j['interval'])
        num = int((endtime-starttime).total_seconds()/j['interval'])
        y.append([ None for i in range(num)])
        #print(j['ID'],j['datatype'])
        match = {
            'ID':j['ID'],
            'time': {
                '$gte': starttime,
                '$lte': endtime,
            },
        j['datatype']:{'$exists':True}
        }

        #群組
        group =  {
            '_id': j['ID'],
            'time': {  '$push': "$time"  },
            j['datatype']  : { '$push': "$"+j['datatype']  }
        }  
        #資料
        data = list(_db.aggregate(
            [
                {'$match': match},
                {"$project":{"_id":0,'time':1,j['datatype'] :1}},  
                { '$limit' : 178560 },
                {'$sort': {'time':1}}, 
                {'$group': group},
            ]
        ))
        if(data!=[]):
            for i,time in enumerate(data[0]['time']):
                diff = time - starttime 
                n = int(diff.total_seconds()/j['interval']) 
                try:
                    y[index][n] = round(data[0][j['datatype'] ][i],3)
                except:
                    pass
    #print (y[0])
    #print (len(y[0]))
    #print (y[1])
    #print (len(y[1]))
    return y
#-----------------------------------------------------------------------
def bar_one_cal_col(db,ID, collection,datatype,date_start=datetime.date.today(),date_end=datetime.date.today(),date_range=1, interval=60, time_interval="1min"):
    starttime,endtimeX = date_interval(date_start)
    starttimeX,endtime = date_interval(date_end)
    if(date_range==0):
        interval_len_data=int((date_end - date_start).total_seconds()/interval)
        y = [None]*interval_len_data
        for k in range(0,interval_len_data):
            endtime = starttime+ relativedelta(seconds=interval) 
            try:
                y[k] = db[collection].find_one({'ID':ID,'time': starttime,'time_interval': time_interval})[datatype]
            except:
                y[k]= None
            starttime = endtime
    else:    # update in 2022.06.05
        # An Incredible Performance Improvement by YuShan
        x_axis = fix_x_xis_date(date_start,date_end,date_range)
        _date_range = {1: 'hour', 2: 'day', 3: 'day', 4: 'day'}.get(date_range, 1)
        date_format = {1: '%Y-%m-%d %H', 2: '%Y-%m-%d', 3: '%Y-%m', 4: '%Y'}.get(date_range, 1)
        y_axis_dict = {}
        for _x in x_axis:
            y_axis_dict[_x] = []
        
        duplicate_prevent = []
        i = 0
        for data in db[collection].find({'ID': ID, 'time_interval': _date_range, 'time': {'$gte': starttime, '$lt': endtime}}).sort('time', 1):
            #print(datetime.datetime.strftime(data['time'], date_format), data['kwh'])
            try:
                if data['time'] in duplicate_prevent:    # PR 計算程式可能有錯誤或開了多個在運行, ask 學長
                    print('bar_one_cal_col time duplicate')
                    continue
                duplicate_prevent.append(data['time'])
                y_axis_dict[datetime.datetime.strftime(data['time'], date_format)].append(data[datatype])
            except:
                pass

        y = []
        for _date in y_axis_dict:
            try:
                #print(_date, sum(y_axis_dict[_date]))
                d_sum = None
                for d in y_axis_dict[_date]:
                    try:
                        if d_sum == None and isinstance(d, (int, float)):
                            d_sum = 0
                        d_sum += d
                    except:
                        pass
                if datatype in ['pr', 'ra']:
                    y.append(d_sum/len(y_axis_dict[_date]))
                else:
                    y.append(d_sum)
            except:
                y.append(None)

    return y
#-----------------------------------------------------------------------
# 計算PR _avg
def bar_one_PR_total(db,collection,ID,kw,kwh,IRR,IRRh,date_start=datetime.date.today(),date_end=datetime.date.today(),date_range=1, interval=60, time_interval="1min"):
    db = db[collection]
    starttime,endtimeX = date_interval(date_start)
    starttimeX,endtime = date_interval(date_end)
    
    IRR=float(IRR)
    kw=float(kw)
    if(date_range==0):
        interval_len_data=int((date_end - date_start).total_seconds()/interval)
        y=0
        kwh_buffer=0
        IRRh_buffer=0
        for k in range(0,interval_len_data):
            endtime = starttime+ relativedelta(seconds=interval) 
            for i in db.find({'ID':ID,'time': {'$gte': starttime,'$lt':endtime},'kwh':{'$nin':[0,None]}},{'_id':0}).sort('time',pymongo.DESCENDING).limit(1):#None
                kwh_buffer=kwh_buffer+i[kwh]
                IRRh_buffer=IRRh_buffer+i[IRRh]  
            starttime = endtime
        
        if (IRRh_buffer!=0) and (kw!=0):
            if (IRRh_buffer>0.001):
                y=(kwh_buffer/kw) / (IRRh_buffer/ IRR)*100
            else:
                y=0
        else:
            y=0
    elif(date_range==1):
        day_len_data=day_len(date_start,date_end)
        y=0
        kwh_buffer=0
        IRRh_buffer=0
        for k in range(0,day_len_data):
            endtime = starttime+ relativedelta(hours=+1) 
            for i in db.find({'ID':ID,'time': {'$gte': starttime,'$lt':endtime},'kwh':{'$nin':[0,None]}},{'_id':0}).sort('time',pymongo.DESCENDING).limit(1):#None
                kwh_buffer=kwh_buffer+i[kwh]
                IRRh_buffer=IRRh_buffer+i[IRRh]  
            starttime = endtime
        
        if (IRRh_buffer!=0) and (kw!=0):
            if (IRRh_buffer>0.001):
                y=(kwh_buffer/kw) / (IRRh_buffer/ IRR)*100
            else:
                y=0
        else:
            y=0
        #print(y)
            
    elif(date_range==2):
        _month_len = month_len(date_start,date_end)
        #starttime = datetime.datetime.strptime(str(starttime.year)+'-'+str(starttime.month)+'-01 00:00:00',"%Y-%m-%d %H:%M:%S")
        starttime = date_start
        y=0
        kwh_buffer=0
        IRRh_buffer=0
        for k in range(0,_month_len):
            endtime = starttime+ relativedelta(days=+1) 
            for i in db.find({'ID':ID,'time': {'$gte': starttime,'$lt':endtime},'kwh':{'$nin':[0,None]}},{'_id':0}).sort('time',pymongo.DESCENDING).limit(24):#None   
                kwh_buffer=kwh_buffer+i[kwh]
                IRRh_buffer=IRRh_buffer+i[IRRh]
                #print (i[IRRh])
            starttime = endtime
        if (IRRh_buffer!=0) and (kw!=0):
            if (IRRh_buffer>0.001):
                y=(kwh_buffer/kw) / (IRRh_buffer/ IRR)*100
            else:
                y=0
        else:
            y=0
    elif(date_range==3):
        _year_len = year_len(date_start,date_end)
        #starttime  =  datetime.datetime.strptime(str(starttime.year)+'-01-01 00:00:00',"%Y-%m-%d %H:%M:%S")
        y=0
        kwh_buffer=0
        IRRh_buffer=0
        for k in range(_year_len):
            starttime = starttime
            endtime = datetime.datetime.strftime(starttime + relativedelta(months=+1), '%Y-%m')
            endtime = datetime.datetime.strptime(endtime, '%Y-%m')
            if k == _year_len - 1:   #最後一個月的搜尋時間應為date_end+1天
                endtime = date_end + datetime.timedelta(days=1)
            for i in db.find({'ID':ID,'time': {'$gte': starttime,'$lt':endtime},'kwh':{'$nin':[0,None]}},{'_id':0}).sort('time',pymongo.DESCENDING).limit(744):#None
                kwh_buffer=kwh_buffer+i[kwh]
                IRRh_buffer=IRRh_buffer+i[IRRh]
                #print (i[kwh])
            starttime = endtime
        if (IRRh_buffer!=0) and (kw!=0):
            if (IRRh_buffer>0.001):
                y=(kwh_buffer/kw) / (IRRh_buffer/ IRR)*100
            else:
                y=0
        else:
            y=0
    elif(date_range==4):
        #starttime = datetime.datetime.strptime (str(starttime.year-19)+'-01-01 00:00:00',"%Y-%m-%d %H:%M:%S")
        y=0
        kwh_buffer=0
        IRRh_buffer=0
        for k in range(int(endtime.year-starttime.year+1)):
            starttime  =  starttime
            endtime = datetime.datetime.strftime(starttime + relativedelta(years=1), '%Y')
            endtime = datetime.datetime.strptime(endtime, '%Y')
            if k == int(endtime.year-starttime.year+1) - 1:   #最後一個月的搜尋時間應為date_end+1天
                endtime = date_end + datetime.timedelta(days=1)
            
            """ starttime  =  datetime.datetime.strptime (str(starttime.year) +'-01-01 00:00:00',"%Y-%m-%d %H:%M:%S")
            endtime = starttime + relativedelta(years=+1) """
            
            for i in db.find({'ID':ID,'time': {'$gte': starttime,'$lt':endtime},'kwh':{'$nin':[0,None]}},{'_id':0}).sort('time',pymongo.DESCENDING).limit(14880):#None
                kwh_buffer=kwh_buffer+i[kwh]
                IRRh_buffer=IRRh_buffer+i[IRRh]
            
            starttime = endtime
        if (IRRh_buffer!=0) and (kw!=0):
            if (IRRh_buffer>0.001):
                y=(kwh_buffer/kw) / (IRRh_buffer/ IRR)*100
            else:
                y=0
        else:
            y=0
    output=[{'value':y}]

    return output
#----------------------------------------------------------------------------------------------------------
def dayline_sa_temp(db,ID,date_start=datetime.date.today(),date_end=datetime.date.today(),interval=1):
    db = db['string_meter']
    print (date_start,date_end)
    starttime,endtimeX = date_interval(date_start)
    starttimeX,endtime = date_interval(date_end)
    num = int((endtime-starttime).total_seconds()/interval)
    y = [ [ None for i in range(num)] for j in range(17)]
    
    #條件
    match = {                                
        'ID':ID,
        'time': {
            '$gte': starttime,
            '$lte': endtime,
        },
        "sa":{'$exists':True},
        "temp":{'$exists':True},
    }
    #群組
    group =  {
        '_id': ID,
        'time': {  '$push': "$time"  },
        'sa' : { '$push': "$"+'sa'  },
        'temp' : { '$push': "$"+'temp'  },
    }  
    #資料
    data = list(db.aggregate(
        [
            {'$match': match},
            {"$project":{"_id":0,'time':1,'sa':1,'temp':1}},  
            {'$group': group},
        ]
    ))
    
    if(data!=[]):
        for i,time in enumerate(data[0]['time']):
            diff = time - starttime 
            n = int(diff.total_seconds()/interval) 
            try: 
                for j in range(1,17):
                    y[j][n] = data[0]['sa'][i][j-1]
            except:
                pass
            try: 
                y[0][n] = data[0]['temp'][i]
            except:
                pass
    print (len(y))
    return y
#----------------------------------------------------------------------------------------------------------
def dayline_sa(db,ID,date_start=datetime.date.today(),date_end=datetime.date.today(),interval=1):
    db = db['string_meter']
    # print (ID)
    # print (date_start,date_end)
    starttime,endtimeX = date_interval(date_start)
    starttimeX,endtime = date_interval(date_end)
    num = int((endtime-starttime).total_seconds()/interval)
    y = [ [ None for i in range(num)] for j in range(16)]
    
    #條件
    match = {                                
        'ID':ID,
        'time': {
            '$gte': starttime,
            '$lte': endtime,
        },
        "sa":{'$exists':True},
    }
    #群組
    group =  {
        '_id': ID,
        'time': {  '$push': "$time"  },
        'sa' : { '$push': "$"+'sa'  },
    }  
    #資料
    data = list(db.aggregate(
        [
            {'$match': match},
            {"$project":{"_id":0,'time':1,'sa':1}},  
            {'$group': group},
        ]
    ))
    
    if(data!=[]):
        # print (len(data[0]['sa']))
        for i,time in enumerate(data[0]['time']):
            # print (data[0]['sa'][i])
            diff = time - starttime 
            n = int(diff.total_seconds()/interval) 
            try: 
                for j in range(0,16):
                    y[j][n] = data[0]['sa'][i][j]
            except Exception as e:
                #print (e)
                pass
    return y
#----------------------------------------------------------------------------------------------------------
def dayline_io(db,ID,date_start=datetime.date.today(),date_end=datetime.date.today(),interval=1):
    db = db['pv_io']
    # print (ID)
    # print (date_start,date_end)
    starttime,endtimeX = date_interval(date_start)
    starttimeX,endtime = date_interval(date_end)
    num = int((endtime-starttime).total_seconds()/interval)
    y = [ [ None for i in range(num)] for j in range(8)]
    #條件
    match = {                                
        'ID':ID,
        'time': {
            '$gte': starttime,
            '$lte': endtime,
        },
        "DI":{'$exists':True},
    }
    #群組
    group =  {
        '_id': ID,
        'time': {  '$push': "$time"  },
        'DI' : { '$push': "$DI"  },
    }  
    #資料
    data = list(db.aggregate(
        [
            {'$match': match},
            {"$project":{"_id":0,'time':1,'DI':1}},  
            {'$group': group},
        ]
    ))
    if(data!=[]):
        # print (len(data[0]['sa']))
        for i,time in enumerate(data[0]['time']):
            # print (data[0]['sa'][i])
            diff = time - starttime 
            n = int(diff.total_seconds()/interval) 
            try: 
                for j in range(0,8):
                    y[j][n] = data[0]['DI'][i][j]
            except Exception as e:
                #print (e)
                pass
    return y

#----------------------------------------------------------------------------------------------------------
def dayline_protective_relay(db,ID,equip_data,IEEE_code,datatype,date_start=datetime.date.today(),date_end=datetime.date.today(),interval=1):
    db=db['ProtectiveRelay']
    starttime,endtimeX = date_interval(date_start)
    starttimeX,endtime = date_interval(date_end)
    num = int((endtime-starttime).total_seconds()/interval)

    y = []
    name_list = []
    dict_y = {}
    #條件
    match = {                                
        'ID':ID,
        'time': {
            '$gte': starttime,
            '$lt': endtime,
        },
        "IEEE_code": IEEE_code if IEEE_code != 'total' else {'$exists': True},
        "name": {"$in": list(equip_data.get('points', {}).keys())}
    }
    if datatype != 'total':
        match['LN'] = datatype
    #資料
    data = list(db.aggregate(
        [
            {'$match': match},
            {"$project":{"_id":0,'time':1,'Attribute': 1, 'LN':1, 'name': 1}},  
            
        ]
    ))
    #print(data)
    for i, _data in enumerate(data):
        #print(_data)
        try:
            if _data['name'] not in dict_y:
                dict_y[_data['name']] = [None for i in range(num)]
            diff = _data['time'] - starttime 
            n = int(diff.total_seconds()/interval) 
            dict_y[_data['name']][n] = _data['Attribute']['Op']
        except Exception as e:
            print(e)
            pass
    for key in dict_y:
        y.append(dict_y[key])
        name_list.append(equip_data.get('points', {}).get(key, key))
    return y, name_list
#----------------------------------------------------------------------------------------------------------

import random
def dayline_heatmap_string_pvlof(db,ID,serial_num,date_start=datetime.date.today(),date_end=datetime.date.today(),interval=5*60):
    db = db['heatmap_string_pvlof']
    starttime,endtimeX = date_interval(date_start)
    starttimeX,endtime = date_interval(date_end)
    num = int((endtime-starttime).total_seconds()/interval)
    z = [ [ None for i in range(num)] for j in range(int(serial_num))]

    #條件
    match = {                                
        'ID':ID,
        'time': {
            '$gte': starttime,
            '$lte': endtime,
        },
        "value":{'$exists':True},
    }
    #群組
    group =  {
        '_id': ID,
        'time': {  '$push': "$time"  },
        'value' : { '$push': "$"+'value'  },
    }  
    #資料
    data = list(db.aggregate(
        [
            {'$match': match},
            {"$project":{"_id":0,'time':1,'value':1}},  
            {'$group': group},
        ]
    ))
    
    if(data!=[]):
        for i,time in enumerate(data[0]['time']):
            diff = time - starttime 
            n = int(diff.total_seconds()/interval) 
            try: 
                for j in range(int(serial_num)):
                    z[j][n] = data[0]['value'][i][j]
            except:  
                pass
    return z
def dayline_heatmap_string_pvlof_discrete(db,ID,wiring,date_start=datetime.date.today(),date_end=datetime.date.today(),interval=5*60):
    db = db['heatmap_string_pvlof']
    starttime,endtimeX = date_interval(date_start)
    starttimeX,endtime = date_interval(date_end)
    num = int((endtime-starttime).total_seconds()/interval)
    z = []
    for j in range(len(wiring)):
        if wiring[j]==1:
            z_one=[]
        
            for i in range(num):  
                z_one.append(None)
            z.append(z_one)
            
    print (len(z))
    
    #條件
    match = {                                
        'ID':ID,
        'time': {
            '$gte': starttime,
            '$lte': endtime,
        },
        "value":{'$exists':True},
    }
    #群組
    group =  {
        '_id': ID,
        'time': {  '$push': "$time"  },
        'value' : { '$push': "$"+'value'  },
    }  
    #資料
    data = list(db.aggregate(
        [
            {'$match': match},
            {"$project":{"_id":0,'time':1,'value':1}},  
            {'$group': group},
        ]
    ))
    
    if(data!=[]):
        print (wiring)
        for i,time in enumerate(data[0]['time']):
            diff = time - starttime 
            n = int(diff.total_seconds()/interval) 
            try: 
                # print (wiring)
                count=0
                for j in range( len(wiring) ):
                    if wiring[j]==1:
                        z[count][n] = data[0]['value'][i][j]
                        count=count+1
            except:  
                pass
    return z
#----------------------------------------------------------------------------------------------------------
# dmy irrh for billionwatts
# Using in MaoHong
# dmy_list and sun_list is pointer to origin list
def dmy_irrh_interval_billionwatts(db, dmy_list, sun_list, x_axis, starttime=datetime.datetime.now(), endtime=datetime.datetime.now(), date_range=1):
    remote_error_msg = ''
    if date_range > 1:
        curr_timestamp = time.time()
        param={
            'Content-Type': 'application/json'
        }
        startDate = datetime.datetime.strftime(starttime,'%Y-%m-%d')
        endDate = datetime.datetime.strftime(endtime,'%Y-%m-%d')
        for bw_plant in db.plant_billionwatts.find({}):
            try:
                str1 = '{}{}'.format(bw_plant['password'], curr_timestamp)
                md5_encode = hashlib.md5(str1.encode('utf-8'))
                token = '{}{}'.format(md5_encode.hexdigest(), bw_plant['username'])
                # Get Capacity Data
                result = requests.post('https://solar.billionwatts.com.tw/WsApp/information', headers=param, json={
                    "api":"ctSiteData",
                    "token": token, "langCode":"zh_TW",
                    "sendTimestamp":curr_timestamp,
                    "para":{
                        "siteNo":bw_plant.get('siteNo'),
                    }
                })
                _data = result.json()
                if _data.get('returnStatus') != 'S':
                    remote_error_msg += '{}: {}\n'.format(bw_plant.get('name', ''), _data.get('retrunMessage', ''))
                    continue
                capacity = _data.get('data', [])[0]['siteBuild']
                result = requests.post('https://solar.billionwatts.com.tw/WsApp/information', headers=param, json={
                    "api":"ctSiteDayPowerH",
                    "token": token, "langCode":"zh_TW",
                    "sendTimestamp":curr_timestamp,
                    "para":{
                        "siteNo":bw_plant.get('siteNo'),
                        "startDate": startDate,
                        "endDate": endDate,
                    }
                })
                _data = result.json()
                if _data.get('returnStatus') != 'S':
                    remote_error_msg += '{}: {}\n'.format(bw_plant.get('name', ''), _data.get('retrunMessage', ''))
                    continue
                # 成功取得
                time_dict = {}
                time_dict_sun = {}
                for i in x_axis:
                    time_dict[i] = None
                    time_dict_sun[i] = None
                for i in _data.get('data', []):
                    i_date = datetime.datetime.strptime(i['dateR'], '%Y-%m-%d')
                    if date_range == 2:
                        i_date = datetime.datetime.strftime(i_date, '%Y-%m-%d')
                    elif date_range == 3:
                        i_date = datetime.datetime.strftime(i_date, '%Y-%m')
                    elif date_range == 4:
                        i_date = datetime.datetime.strftime(i_date, '%Y')
                    if time_dict[i_date] == None:
                        time_dict[i_date] = 0
                    time_dict[i_date] += (i['powerH']/ 1000)
                    if bw_plant.get('sun', False) == True:
                        if time_dict_sun[i_date] == None:
                            time_dict_sun[i_date] = 0
                        time_dict_sun[i_date] += (i['sunPowerH']/ 1000)
                #print(time_dict)
                y_axis = []
                sun_y_axis = []
                for i in time_dict:
                    if time_dict[i] == None:
                        remote_error_msg += '{}: {}無數據回傳 \n'.format(bw_plant.get('name'), i)
                        y_axis.append(None)
                    else:
                        y_axis.append(time_dict[i]/capacity)
                    sun_y_axis.append(time_dict_sun[i])
                dmy_list.append({
                    'x_axis': x_axis,
                    'y_axis': y_axis,
                    'ID': bw_plant.get('siteNo'),
                    'collection': 'plant_billionwatts',
                    'name': bw_plant.get('name'),
                    'label': '盛齊_{}'.format(bw_plant.get('name')),
                })
                # 該盛齊案場有日照計
                if bw_plant.get('sun', False) == True:
                    sun_list.append({
                        'ID': 'sun_'+bw_plant.get('siteNo'),
                        'name': '盛齊_{}_日照計'.format(bw_plant.get('name')),
                        'x_axis': x_axis,
                        'y_axis': sun_y_axis,
                        'label': '盛齊_{}_日照計'.format(bw_plant.get('name'))
                    })
            except Exception as e:
                #remote_error_msg += '{}.'.format(e)
                print(e)
    return remote_error_msg