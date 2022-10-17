# Deprecated Func
#======================================================================================================
# preplot.py
def bar_one(db,collection,ID,datatype,date_start=datetime.date.today(),date_end=datetime.date.today(),date_range=1):
    db1 = db['PR']
    db = db[collection]
    starttime,endtimeX = date_interval(date_start)
    starttimeX,endtime = date_interval(date_end)
    #print (date_end-date_start)
    print (date_range)
    if(date_range==1):
        day_len_data=day_len(date_start,date_end)
        y = [None]*day_len_data
        for k in range(0,day_len_data):
            endtime    =  starttime + relativedelta(hours=+1) 
            starttime2 =  starttime + relativedelta(hours=-1) 
            endtime2   =  endtime   + relativedelta(hours=-1)
            '''
            # 子軒
            if starttime<datetime.datetime.now():
                date_buffer_end   = list(db.find({'ID':ID,'time': {'$gte':starttime ,'$lt':endtime },datatype:{'$nin':[0,None]}},{'_id':0,datatype:1}).sort('time',pymongo.DESCENDING).limit(1) )#None
                date_buffer_start = list(db.find({'ID':ID,'time': {'$gte':starttime2,'$lt':endtime2},datatype:{'$nin':[0,None]}},{'_id':0,datatype:1}).sort('time',pymongo.DESCENDING).limit(1) )#None
                #print (date_buffer_end)
                #print (date_buffer_start)
                if (len(date_buffer_end)>0) and (len(date_buffer_start)>0):
                    y[k] = date_buffer_end[0][datatype]-date_buffer_start[0][datatype]
                elif (len(date_buffer_end)==0) and (len(date_buffer_start)>0):
                    y[k] = 0
                elif (len(date_buffer_end)>0) and (len(date_buffer_start)==0):
                    starttime3 =  starttime + relativedelta(days=-7,hour=0,minute=0,second=0) 
                    date_buffer_start = list(db.find({'ID':ID,'time': {'$gte':starttime3,'$lt':endtime2},datatype:{'$nin':[0,None]}},{'_id':0,datatype:1}).sort('time',pymongo.DESCENDING).limit(1) )#None
                    if (len(date_buffer_start)==0):
                        y[k] = 0
                    else:
                        
                        y[k] = date_buffer_end[0][datatype]-date_buffer_start[0][datatype]

                elif (len(date_buffer_end)==0) and (len(date_buffer_start)==0):
                    y[k] = 0
            '''
            # 健誠
            if starttime<datetime.datetime.now():
                date_buffer_end   = list(db.find({'ID':ID,'time': {'$gte':starttime ,'$lt':endtime },datatype:{'$nin':[0,None]}},{'_id':0,datatype:1,'time':1}).sort('time',pymongo.DESCENDING).limit(1) )#None
                date_buffer_start = list(db.find({'ID':ID,'time': {'$gte':starttime2,'$lt':endtime2},datatype:{'$nin':[0,None]}},{'_id':0,datatype:1,'time':1}).sort('time',pymongo.DESCENDING).limit(1) )#None
                #print (date_buffer_end)
                #print (date_buffer_start)
                if (len(date_buffer_end)>0) and (len(date_buffer_start)>0):
                    y[k] = date_buffer_end[0][datatype]-date_buffer_start[0][datatype]
                elif (len(date_buffer_end)==0) and (len(date_buffer_start)>0):
                    y[k] = 0
                elif (len(date_buffer_end)>0) and (len(date_buffer_start)==0):
                    starttime3 =  starttime + relativedelta(days=-7,hour=0,minute=0,second=0) 
                    date_buffer_start1 = list(db.find({'ID':ID,'time': {'$gte':starttime3,'$lt':endtime2},datatype:{'$nin':[0,None]}},{'_id':0,datatype:1,'time':1}).sort('time',pymongo.DESCENDING).limit(1) )#None
                    print('date_buffer_start',date_buffer_start)
                    print('date_buffer_end',date_buffer_end)
                    print('j[k]:',k,day_len_data)
                    
                    if (len(date_buffer_start1)==0):
                        y[k] = 0
                    else:
                        if date_buffer_end[0]['time'].day == date_buffer_start1[0]['time'].day:
                            print("the same day")
                            # sun search
                            # sun_buffer 時間由舊到新
                            sun_buffer = list(db1.find({'ID':ID,'time': {'$gte':date_buffer_start1[0]['time'],'$lt':date_buffer_end[0]['time']},'IRRh':{'$nin':[None]}},{'_id':0,'IRRh':1,'time':1}).sort('time',pymongo.ASCENDING) )#None

                            # sun_buffer = [{'IRRh':800},{'IRRh':700},{'IRRh':600},{'IRRh':500},{'IRRh':400},{'IRRh':300},{'IRRh':200},{'IRRh':100}]                            
                            if len(sun_buffer) == (date_buffer_end[0]['time'].hour-date_buffer_start1[0]['time'].hour): # 日照計沒斷線
                                print('日照計沒斷線')
                                sun_buffer_list = []
                                for yyy in range(len(sun_buffer)):
                                    sun_buffer_list.append(sun_buffer[yyy]['IRRh'])
                                # 日照量總和
                                sun_buffer_list_sum = sum(sun_buffer_list)                         
                                print('日照量總和',sun_buffer_list_sum)
                                # 日照計比例分配
                                for xxx in range(k-(date_buffer_end[0]['time'].hour-date_buffer_start1[0]['time'].hour)+1 , k+1):
                                    print(xxx,sun_buffer_list)
                                    y[xxx] = (date_buffer_end[0][datatype]-date_buffer_start1[0][datatype]) / sun_buffer_list_sum * sun_buffer_list[0]
                                    sun_buffer_list.pop(0) # 將計算完的項目pop
                                    
                                
                            else: # 日照計 斷線 或是沒有日照計
                                # 平均法
                                # for xxx in range(date_buffer_start[0]['time'].hour+1 , date_buffer_end[0]['time'].hour+1):
                                for xxx in range(k-(date_buffer_end[0]['time'].hour-date_buffer_start1[0]['time'].hour)+1 , k+1):
                                    y[xxx] = (date_buffer_end[0][datatype]-date_buffer_start1[0][datatype]) / (date_buffer_end[0]['time'].hour - date_buffer_start1[0]['time'].hour )
                                    print('hours',xxx,'y[xxx]',y[xxx])
                        else:
                            y[k] = date_buffer_end[0][datatype]-date_buffer_start1[0][datatype]

                elif (len(date_buffer_end)==0) and (len(date_buffer_start)==0):
                    y[k] = 0
            starttime = endtime
        #print (y)
    elif(date_range==2):
        _month_len = month_len(date_start,date_end)
        y = [None]*_month_len
        #starttime = datetime.datetime.strptime(str(starttime.year)+'-'+str(starttime.month)+'-01 00:00:00',"%Y-%m-%d %H:%M:%S")
        starttime = date_start
        for k in range(0,_month_len):
            endtime    =  starttime + relativedelta(days=+1) 
            starttime2 =  starttime + relativedelta(days=-1) 
            endtime2   =  endtime   + relativedelta(days=-1) 
            '''
            # 子軒
            if starttime<datetime.datetime.now():
                start_time=datetime.datetime.now()
                date_buffer_end   = list(db.find({'ID':ID,'time': {'$gte':starttime ,'$lt':endtime },datatype:{'$nin':[0,None]}},{'_id':0,datatype:1}).sort('time',pymongo.DESCENDING).limit(1) )#None
                date_buffer_start = list(db.find({'ID':ID,'time': {'$gte':starttime2,'$lt':endtime2},datatype:{'$nin':[0,None]}},{'_id':0,datatype:1}).sort('time',pymongo.DESCENDING).limit(1) )#None
                #print ('xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx')
                #print (datetime.datetime.now()-start_time)
                #print ('xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx')
                
                if (len(date_buffer_end)>0) and (len(date_buffer_start)>0):
                    y[k] = date_buffer_end[0][datatype]-date_buffer_start[0][datatype]
                elif (len(date_buffer_end)==0) and (len(date_buffer_start)>0):
                    y[k] = 0
                elif (len(date_buffer_end)>0) and (len(date_buffer_start)==0):
                    starttime3 =  starttime + relativedelta(day=0,hour=0,minute=0,second=0) 
                    date_buffer_start = list(db.find({'ID':ID,'time': {'$gte':starttime3,'$lt':endtime2},datatype:{'$nin':[0,None]}},{'_id':0,datatype:1}).sort('time',pymongo.DESCENDING).limit(1) )#None
                    if (len(date_buffer_start)==0):
                        y[k] = 0
                    else:
                        y[k] = date_buffer_end[0][datatype]-date_buffer_start[0][datatype]
                elif (len(date_buffer_end)==0) and (len(date_buffer_start)==0):
                    y[k] = 0
            '''
            # 健誠
            if starttime<datetime.datetime.now():
                start_time=datetime.datetime.now()
                date_buffer_end   = list(db.find({'ID':ID,'time': {'$gte':starttime ,'$lt':endtime },datatype:{'$nin':[0,None]}},{'_id':0,datatype:1,'time':1}).sort('time',pymongo.DESCENDING).limit(1) )#None
                date_buffer_start = list(db.find({'ID':ID,'time': {'$gte':starttime2,'$lt':endtime2},datatype:{'$nin':[0,None]}},{'_id':0,datatype:1,'time':1}).sort('time',pymongo.DESCENDING).limit(1) )#None
                #print ('xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx')
                #print (datetime.datetime.now()-start_time)
                #print ('xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx')
                
                if (len(date_buffer_end)>0) and (len(date_buffer_start)>0):
                    y[k] = date_buffer_end[0][datatype]-date_buffer_start[0][datatype]
                elif (len(date_buffer_end)==0) and (len(date_buffer_start)>0):
                    y[k] = 0
                elif (len(date_buffer_end)>0) and (len(date_buffer_start)==0):
                    starttime3 =  starttime + relativedelta(day=0,hour=0,minute=0,second=0) 
                    date_buffer_start1 = list(db.find({'ID':ID,'time': {'$gte':starttime3,'$lt':endtime2},datatype:{'$nin':[0,None]}},{'_id':0,datatype:1,'time':1}).sort('time',pymongo.DESCENDING).limit(1) )#None
                    if (len(date_buffer_start1)==0):
                        y[k] = 0
                    else:
                        if date_buffer_end[0]['time'].month == date_buffer_start1[0]['time'].month:
                            print("the same month")
                            # sun search
                            # sun_buffer 時間由舊到新
                            sun_buffer = list(db1.find({'ID':ID,'time': {'$gte':date_buffer_start1[0]['time'],'$lt':date_buffer_end[0]['time']},'IRRh':{'$nin':[None]}},{'_id':0,'IRRh':1,'time':1}).sort('time',pymongo.ASCENDING) )#None

                            # sun_buffer = [{'IRRh':800},{'IRRh':700},{'IRRh':600},{'IRRh':500},{'IRRh':400},{'IRRh':300},{'IRRh':200},{'IRRh':100}]                            
                            if len(sun_buffer) == (date_buffer_end[0]['time'].month-date_buffer_start1[0]['time'].month): # 日照計沒斷線
                                print('日照計沒斷線')
                                sun_buffer_list = []
                                for yyy in range(len(sun_buffer)):
                                    sun_buffer_list.append(sun_buffer[yyy]['IRRh'])
                                # 日照量總和
                                sun_buffer_list_sum = sum(sun_buffer_list)                         
                                print('日照量總和',sun_buffer_list_sum)
                                # 日照計比例分配
                                for xxx in range(k-(date_buffer_end[0]['time'].month-date_buffer_start1[0]['time'].month)+1 , k+1):
                                    print(xxx,sun_buffer_list)
                                    y[xxx] = (date_buffer_end[0][datatype]-date_buffer_start1[0][datatype]) / sun_buffer_list_sum * sun_buffer_list[0]
                                    sun_buffer_list.pop(0) # 將計算完的項目pop
                                    
                                
                            else: # 日照計 斷線 或是沒有日照計
                                # 平均法
                                # for xxx in range(date_buffer_start[0]['time'].day+1 , date_buffer_end[0]['time'].day+1):
                                for xxx in range(k-(date_buffer_end[0]['time'].day-date_buffer_start1[0]['time'].day)+1 , k+1):
                                    y[xxx] = (date_buffer_end[0][datatype]-date_buffer_start1[0][datatype]) / (date_buffer_end[0]['time'].day - date_buffer_start1[0]['time'].day )
                                    print('days',xxx,'y[xxx]',y[xxx])
                        else:
                            y[k] = date_buffer_end[0][datatype]-date_buffer_start1[0][datatype]
                elif (len(date_buffer_end)==0) and (len(date_buffer_start)==0):
                    y[k] = 0

            starttime = endtime
    elif(date_range==3):
        _year_len = year_len(date_start,date_end)
        y = [None]*_year_len
        #starttime  =  datetime.datetime.strptime(str(starttime.year)+'-01-01 00:00:00',"%Y-%m-%d %H:%M:%S")
        for k in range(0,_year_len):
            starttime = starttime
            endtime = datetime.datetime.strftime(starttime + relativedelta(months=+1), '%Y-%m')
            endtime = datetime.datetime.strptime(endtime, '%Y-%m')
            if k == len(y) - 1:   #最後一個月的搜尋時間應為date_end+1天
                endtime = date_end + datetime.timedelta(days=1)
            starttime2 =  starttime + relativedelta(months=-1) 
            endtime2   =  starttime 
            '''
            # 子軒
            if starttime<datetime.datetime.now():
                date_buffer_end   = list(db.find({'ID':ID,'time': {'$gte':starttime ,'$lt':endtime },datatype:{'$nin':[0,None]}},{'_id':0,datatype:1}).sort('time',pymongo.DESCENDING).limit(1) )#None
                date_buffer_start = list(db.find({'ID':ID,'time': {'$gte':starttime2,'$lt':endtime2},datatype:{'$nin':[0,None]}},{'_id':0,datatype:1}).sort('time',pymongo.DESCENDING).limit(1) )#None
                if (len(date_buffer_end)>0) and (len(date_buffer_start)>0):
                    y[k] = date_buffer_end[0][datatype]-date_buffer_start[0][datatype]
                elif (len(date_buffer_end)==0) and (len(date_buffer_start)>0):
                    y[k] = 0
                elif (len(date_buffer_end)>0) and (len(date_buffer_start)==0):
                    starttime3 =  starttime + relativedelta(month=0,day=0,hour=0,minute=0,second=0) 
                    date_buffer_start = list(db.find({'ID':ID,'time': {'$gte':starttime3,'$lt':endtime2},datatype:{'$nin':[0,None]}},{'_id':0,datatype:1}).sort('time',pymongo.DESCENDING).limit(1) )#None
                    if (len(date_buffer_start)==0):
                        y[k] = 0
                    else:
                        y[k] = date_buffer_end[0][datatype]-date_buffer_start[0][datatype]
                elif (len(date_buffer_end)==0) and (len(date_buffer_start)==0):
                    y[k] = 0
            '''
            # 健誠
            if starttime<datetime.datetime.now():
                date_buffer_end   = list(db.find({'ID':ID,'time': {'$gte':starttime ,'$lt':endtime },datatype:{'$nin':[0,None]}},{'_id':0,datatype:1,'time':1}).sort('time',pymongo.DESCENDING).limit(1) )#None
                date_buffer_start = list(db.find({'ID':ID,'time': {'$gte':starttime2,'$lt':endtime2},datatype:{'$nin':[0,None]}},{'_id':0,datatype:1,'time':1}).sort('time',pymongo.DESCENDING).limit(1) )#None
                if (len(date_buffer_end)>0) and (len(date_buffer_start)>0):
                    y[k] = date_buffer_end[0][datatype]-date_buffer_start[0][datatype]
                elif (len(date_buffer_end)==0) and (len(date_buffer_start)>0):
                    y[k] = 0
                elif (len(date_buffer_end)>0) and (len(date_buffer_start)==0):
                    starttime3 =  starttime + relativedelta(month=0,day=0,hour=0,minute=0,second=0) 
                    date_buffer_start1 = list(db.find({'ID':ID,'time': {'$gte':starttime3,'$lt':endtime2},datatype:{'$nin':[0,None]}},{'_id':0,datatype:1,'time':1}).sort('time',pymongo.DESCENDING).limit(1) )#None
                    if (len(date_buffer_start1)==0):
                        y[k] = 0
                    else:
                        if date_buffer_end[0]['time'].year == date_buffer_start1[0]['time'].year:
                            print("the same year")
                            # sun search
                            # sun_buffer 時間由舊到新
                            sun_buffer = list(db1.find({'ID':ID,'time': {'$gte':date_buffer_start1[0]['time'],'$lt':date_buffer_end[0]['time']},'IRRh':{'$nin':[None]}},{'_id':0,'IRRh':1,'time':1}).sort('time',pymongo.ASCENDING) )#None

                            # sun_buffer = [{'IRRh':800},{'IRRh':700},{'IRRh':600},{'IRRh':500},{'IRRh':400},{'IRRh':300},{'IRRh':200},{'IRRh':100}]                            
                            if len(sun_buffer) == (date_buffer_end[0]['time'].year-date_buffer_start1[0]['time'].year): # 日照計沒斷線
                                print('日照計沒斷線')
                                sun_buffer_list = []
                                for yyy in range(len(sun_buffer)):
                                    sun_buffer_list.append(sun_buffer[yyy]['IRRh'])
                                # 日照量總和
                                sun_buffer_list_sum = sum(sun_buffer_list)                         
                                print('日照量總和',sun_buffer_list_sum)
                                # 日照計比例分配
                                for xxx in range(k-(date_buffer_end[0]['time'].year-date_buffer_start1[0]['time'].year)+1 , k+1):
                                    print(xxx,sun_buffer_list)
                                    y[xxx] = (date_buffer_end[0][datatype]-date_buffer_start1[0][datatype]) / sun_buffer_list_sum * sun_buffer_list[0]
                                    sun_buffer_list.pop(0) # 將計算完的項目pop
                                    
                                
                            else: # 日照計 斷線 或是沒有日照計
                                # 平均法
                                # for xxx in range(date_buffer_start[0]['time'].month+1 , date_buffer_end[0]['time'].month+1):
                                for xxx in range(k-(date_buffer_end[0]['time'].month-date_buffer_start1[0]['time'].month)+1 , k+1):
                                    y[xxx] = (date_buffer_end[0][datatype]-date_buffer_start1[0][datatype]) / (date_buffer_end[0]['time'].month - date_buffer_start1[0]['time'].month )
                                    print('months',xxx,'y[xxx]',y[xxx])
                        else:
                            y[k] = date_buffer_end[0][datatype]-date_buffer_start1[0][datatype]
                elif (len(date_buffer_end)==0) and (len(date_buffer_start)==0):
                    y[k] = 0

            starttime = endtime
    elif(date_range==4):
        """ y = [None]*20
        starttime = datetime.datetime.strptime (str(starttime.year-19)+'-01-01 00:00:00',"%Y-%m-%d %H:%M:%S") """
        y = [None]*int(endtime.year-starttime.year+1)
        for k in range(len(y)):
            starttime  =  starttime
            endtime = datetime.datetime.strftime(starttime + relativedelta(years=1), '%Y')
            endtime = datetime.datetime.strptime(endtime, '%Y')
            if k == len(y) - 1:   #最後一個月的搜尋時間應為date_end+1天
                endtime = date_end + datetime.timedelta(days=1)
            starttime2 =  starttime + relativedelta(years=-1) 
            endtime2   =  starttime
            if starttime<datetime.datetime.now():
                date_buffer_end   = list(db.find({'ID':ID,'time': {'$gte':starttime ,'$lt':endtime },datatype:{'$nin':[0,None]}},{'_id':0,datatype:1}).sort('time',pymongo.DESCENDING).limit(1) )#None
                date_buffer_start = list(db.find({'ID':ID,'time': {'$gte':starttime2,'$lt':endtime2},datatype:{'$nin':[0,None]}},{'_id':0,datatype:1}).sort('time',pymongo.DESCENDING).limit(1) )#None
                #print (date_buffer_end)
                #print (date_buffer_start)
                if (len(date_buffer_end)>0) and (len(date_buffer_start)>0):   #有這年+有上年
                    y[k] = date_buffer_end[0][datatype]-date_buffer_start[0][datatype]
                elif (len(date_buffer_end)==0) and (len(date_buffer_start)>0):#沒這年+有上年
                    y[k] = 0
                elif (len(date_buffer_end)>0) and (len(date_buffer_start)==0):#有這年+沒上年
                    #搜尋從2000年到現在
                    starttime3 =  starttime + relativedelta(year=2000,month=1,day=1,hour=0,minute=0,second=0) 
                    date_buffer_start = list(db.find({'ID':ID,'time': {'$gte':starttime3,'$lt':endtime2},datatype:{'$nin':[0,None]}},{'_id':0,datatype:1}).sort('time',pymongo.DESCENDING).limit(1) )#None
                    if (len(date_buffer_start)==0):
                        #搜尋當年是否有資料
                        date_buffer_start = list(db.find({'ID':ID,'time': {'$gte':starttime ,'$lt':endtime },datatype:{'$nin':[0,None]}},{'_id':0,datatype:1}).sort('time',pymongo.ASCENDING).limit(1) )#None
                        if (len(date_buffer_start)==0):
                            y[k] = 0
                        else:
                            y[k] = date_buffer_end[0][datatype]-date_buffer_start[0][datatype]
                    else:
                        y[k] = date_buffer_end[0][datatype]-date_buffer_start[0][datatype]
                elif (len(date_buffer_end)==0) and (len(date_buffer_start)==0):#沒這年+沒上年
                    y[k] = 0
            starttime = endtime
    #print (y)
    return y
#-----------------------------------------------------------------------
#IRRh Grep
#By YuShan
#Old Method
def bar_one_IRRh(db,collection,ID,IRR,IRRh,date_start=datetime.date.today(),date_end=datetime.date.today(),date_range=1):
    db = db[collection]
    starttime,endtimeX = date_interval(date_start)
    starttimeX,endtime = date_interval(date_end)
    
    IRR=float(IRR)
    if(date_range==1):
        day_len_data=day_len(date_start,date_end)
        y = [None]*day_len_data
        for k in range(0,day_len_data):
            IRRh_buffer=0
            endtime = starttime+ relativedelta(hours=+1) 
            for i in db.find({'ID':ID,'time': {'$gte': starttime,'$lt':endtime},'IRRh':{'$nin':[0,None]}},{'_id':0}).sort('time',pymongo.DESCENDING).limit(1):#None
                IRRh_buffer=IRRh_buffer+i[IRRh]
                y[k]=IRRh_buffer
            
            starttime = endtime
    elif(date_range==2):
        _month_len = month_len(date_start,date_end)
        y = [None]*_month_len
        starttime = date_start
        for k in range(0,_month_len):
            IRRh_buffer=0
            endtime = starttime+ relativedelta(days=+1) 
            

            for i in db.find({'ID':ID,'time': {'$gte': starttime,'$lt':endtime},'IRRh':{'$nin':[0,None]}},{'_id':0}).sort('time',pymongo.DESCENDING).limit(24):#None
                IRRh_buffer=IRRh_buffer+i[IRRh]
                y[k]=IRRh_buffer

            starttime = endtime
    elif(date_range==3):
        _year_len = year_len(date_start,date_end)
        y = [None]*_year_len
        for k in range(len(y)):
            starttime = starttime
            endtime = datetime.datetime.strftime(starttime + relativedelta(months=+1), '%Y-%m')
            endtime = datetime.datetime.strptime(endtime, '%Y-%m')
            if k == len(y) - 1:   #最後一個月的搜尋時間應為date_end+1天
                endtime = date_end + datetime.timedelta(days=1)
            kwh_buffer=0
            IRRh_buffer=0
            
            for i in db.find({'ID':ID,'time': {'$gte': starttime,'$lt':endtime},'IRRh':{'$nin':[0,None]}},{'_id':0}).sort('time',pymongo.DESCENDING).limit(744):#None
                IRRh_buffer=IRRh_buffer+i[IRRh]
                y[k]=IRRh_buffer
            
            starttime = endtime
    elif(date_range==4):
        y = [None]*int(endtime.year-starttime.year+1)
        for k in range(len(y)):
            starttime  =  starttime
            endtime = datetime.datetime.strftime(starttime + relativedelta(years=1), '%Y')
            endtime = datetime.datetime.strptime(endtime, '%Y')
            if k == len(y) - 1:   #最後一個月的搜尋時間應為date_end+1天
                endtime = date_end + datetime.timedelta(days=1)
            kwh_buffer=0
            IRRh_buffer=0

            for i in db.find({'ID':ID,'time': {'$gte': starttime,'$lt':endtime},'IRRh':{'$nin':[0,None]}},{'_id':0}).sort('time',pymongo.DESCENDING).limit(14880):#None
                IRRh_buffer=IRRh_buffer+i[IRRh]
                y[k]=IRRh_buffer
            starttime = endtime
    return y
#----------------------------------------------------------------------------------------------------------

def bar_one_DMY(db,collection,ID,datatype,date_start=datetime.date.today(),date_end=datetime.date.today(),date_range=1):
    db = db[collection]
    starttime,endtimeX = date_interval(date_start)
    starttimeX,endtime = date_interval(date_end)
    #print (date_end-date_start)
    print (date_range)
    if(date_range==1):
        day_len_data=day_len(date_start,date_end)
        y = [None]*day_len_data
        for k in range(0,day_len_data):
            endtime    =  starttime + relativedelta(hours=+1) 
            starttime2 =  starttime + relativedelta(hours=-1) 
            endtime2   =  endtime   + relativedelta(hours=-1)
            if starttime<datetime.datetime.now():
                date_buffer_end   = list(db.find({'ID':ID,'time': {'$gte':starttime ,'$lt':endtime },datatype:{'$nin':[0,None]}},{'_id':0,datatype:1}).sort('time',pymongo.DESCENDING).limit(1) )#None
                date_buffer_start = list(db.find({'ID':ID,'time': {'$gte':starttime2,'$lt':endtime2},datatype:{'$nin':[0,None]}},{'_id':0,datatype:1}).sort('time',pymongo.DESCENDING).limit(1) )#None
                #print (date_buffer_end)
                #print (date_buffer_start)
                if (len(date_buffer_end)>0) and (len(date_buffer_start)>0):
                    y[k] = date_buffer_end[0][datatype]-date_buffer_start[0][datatype]
                elif (len(date_buffer_end)==0) and (len(date_buffer_start)>0):
                    y[k] = 0
                elif (len(date_buffer_end)>0) and (len(date_buffer_start)==0):
                    starttime3 =  starttime + relativedelta(days=-7,hour=0,minute=0,second=0) 
                    date_buffer_start = list(db.find({'ID':ID,'time': {'$gte':starttime3,'$lt':endtime2},datatype:{'$nin':[0,None]}},{'_id':0,datatype:1}).sort('time',pymongo.DESCENDING).limit(1) )#None
                    if (len(date_buffer_start)==0):
                        y[k] = 0
                    else:
                        
                        y[k] = date_buffer_end[0][datatype]-date_buffer_start[0][datatype]

                elif (len(date_buffer_end)==0) and (len(date_buffer_start)==0):
                    y[k] = None
            starttime = endtime
        #print (y)
    elif(date_range==2):
        _month_len = month_len(date_start,date_end)
        y = [None]*_month_len
        #starttime = datetime.datetime.strptime(str(starttime.year)+'-'+str(starttime.month)+'-01 00:00:00',"%Y-%m-%d %H:%M:%S")
        starttime = date_start
        for k in range(0,_month_len):
            endtime    =  starttime + relativedelta(days=+1) 
            starttime2 =  starttime + relativedelta(days=-1) 
            endtime2   =  endtime   + relativedelta(days=-1) 
            
            if starttime<datetime.datetime.now():
                start_time=datetime.datetime.now()
                date_buffer_end   = list(db.find({'ID':ID,'time': {'$gte':starttime ,'$lt':endtime },datatype:{'$nin':[0,None]}},{'_id':0,datatype:1}).sort('time',pymongo.DESCENDING).limit(1) )#None
                date_buffer_start = list(db.find({'ID':ID,'time': {'$gte':starttime2,'$lt':endtime2},datatype:{'$nin':[0,None]}},{'_id':0,datatype:1}).sort('time',pymongo.DESCENDING).limit(1) )#None
                #print ('xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx')
                #print (datetime.datetime.now()-start_time)
                #print ('xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx')
                
                if (len(date_buffer_end)>0) and (len(date_buffer_start)>0):
                    y[k] = date_buffer_end[0][datatype]-date_buffer_start[0][datatype]
                elif (len(date_buffer_end)==0) and (len(date_buffer_start)>0):
                    y[k] = 0
                elif (len(date_buffer_end)>0) and (len(date_buffer_start)==0):
                    starttime3 =  starttime + relativedelta(days=-21,hour=0,minute=0,second=0) 
                    date_buffer_start = list(db.find({'ID':ID,'time': {'$gte':starttime3,'$lt':endtime2},datatype:{'$nin':[0,None]}},{'_id':0,datatype:1}).sort('time',pymongo.DESCENDING).limit(1) )#None
                    if (len(date_buffer_start)==0):
                        y[k] = 0
                    else:
                        y[k] = date_buffer_end[0][datatype]-date_buffer_start[0][datatype]
                elif (len(date_buffer_end)==0) and (len(date_buffer_start)==0):
                    y[k] = None

            

            starttime = endtime
    elif(date_range==3):
        _year_len = year_len(date_start,date_end)
        y = [None]*_year_len
        #starttime  =  datetime.datetime.strptime(str(starttime.year)+'-01-01 00:00:00',"%Y-%m-%d %H:%M:%S")
        for k in range(len(y)):
            starttime = starttime
            endtime = datetime.datetime.strftime(starttime + relativedelta(months=+1), '%Y-%m')
            endtime = datetime.datetime.strptime(endtime, '%Y-%m')
            if k == len(y) - 1:   #最後一個月的搜尋時間應為date_end+1天
                endtime = date_end + datetime.timedelta(days=1)
            starttime2 =  starttime + relativedelta(months=-1) 
            endtime2   =  starttime 

            if starttime<datetime.datetime.now():
                date_buffer_end   = list(db.find({'ID':ID,'time': {'$gte':starttime ,'$lt':endtime },datatype:{'$nin':[0,None]}},{'_id':0,datatype:1}).sort('time',pymongo.DESCENDING).limit(1) )#None
                date_buffer_start = list(db.find({'ID':ID,'time': {'$gte':starttime2,'$lt':endtime2},datatype:{'$nin':[0,None]}},{'_id':0,datatype:1}).sort('time',pymongo.DESCENDING).limit(1) )#None
                if (len(date_buffer_end)>0) and (len(date_buffer_start)>0):
                    y[k] = date_buffer_end[0][datatype]-date_buffer_start[0][datatype]
                elif (len(date_buffer_end)==0) and (len(date_buffer_start)>0):
                    y[k] = 0
                elif (len(date_buffer_end)>0) and (len(date_buffer_start)==0):
                    starttime3 =  starttime + relativedelta(month=0,day=0,hour=0,minute=0,second=0) 
                    date_buffer_start = list(db.find({'ID':ID,'time': {'$gte':starttime3,'$lt':endtime2},datatype:{'$nin':[0,None]}},{'_id':0,datatype:1}).sort('time',pymongo.DESCENDING).limit(1) )#None
                    if (len(date_buffer_start)==0):
                        y[k] = 0
                    else:
                        y[k] = date_buffer_end[0][datatype]-date_buffer_start[0][datatype]
                elif (len(date_buffer_end)==0) and (len(date_buffer_start)==0):
                    y[k] = None
            starttime = endtime
    elif(date_range==4):
        y = [None]*int(endtime.year-starttime.year+1)
        for k in range(len(y)):
            starttime  =  starttime
            endtime = datetime.datetime.strftime(starttime + relativedelta(years=1), '%Y')
            endtime = datetime.datetime.strptime(endtime, '%Y')
            if k == len(y) - 1:   #最後一個月的搜尋時間應為date_end+1天
                endtime = date_end + datetime.timedelta(days=1)
            starttime2 =  starttime + relativedelta(years=-1) 
            endtime2   =  starttime
            if starttime<datetime.datetime.now():
                date_buffer_end   = list(db.find({'ID':ID,'time': {'$gte':starttime ,'$lt':endtime },datatype:{'$nin':[0,None]}},{'_id':0,datatype:1}).sort('time',pymongo.DESCENDING).limit(1) )#None
                date_buffer_start = list(db.find({'ID':ID,'time': {'$gte':starttime2,'$lt':endtime2},datatype:{'$nin':[0,None]}},{'_id':0,datatype:1}).sort('time',pymongo.DESCENDING).limit(1) )#None
                #print (date_buffer_end)
                #print (date_buffer_start)
                if (len(date_buffer_end)>0) and (len(date_buffer_start)>0):   #有這年+有上年
                    y[k] = date_buffer_end[0][datatype]-date_buffer_start[0][datatype]
                elif (len(date_buffer_end)==0) and (len(date_buffer_start)>0):#沒這年+有上年
                    y[k] = 0
                elif (len(date_buffer_end)>0) and (len(date_buffer_start)==0):#有這年+沒上年
                    #搜尋從2000年到現在
                    starttime3 =  starttime + relativedelta(year=2000,month=1,day=1,hour=0,minute=0,second=0) 
                    date_buffer_start = list(db.find({'ID':ID,'time': {'$gte':starttime3,'$lt':endtime2},datatype:{'$nin':[0,None]}},{'_id':0,datatype:1}).sort('time',pymongo.DESCENDING).limit(1) )#None
                    if (len(date_buffer_start)==0):
                        #搜尋當年是否有資料
                        date_buffer_start = list(db.find({'ID':ID,'time': {'$gte':starttime ,'$lt':endtime },datatype:{'$nin':[0,None]}},{'_id':0,datatype:1}).sort('time',pymongo.ASCENDING).limit(1) )#None
                        if (len(date_buffer_start)==0):
                            y[k] = 0
                        else:
                            y[k] = date_buffer_end[0][datatype]-date_buffer_start[0][datatype]
                    else:
                        y[k] = date_buffer_end[0][datatype]-date_buffer_start[0][datatype]
                elif (len(date_buffer_end)==0) and (len(date_buffer_start)==0):#沒這年+沒上年
                    y[k] = None
            starttime = endtime
    #print (y)
    return y
#-----------------------------------------------------------------------
def bar_one_PR(db,collection,ID,kw,kwh,IRR,IRRh,date_start=datetime.date.today(),date_end=datetime.date.today(),date_range=1):
    db = db[collection]
    starttime,endtimeX = date_interval(date_start)
    starttimeX,endtime = date_interval(date_end)
    
    IRR=float(IRR)
    kw=float(kw)
    if(date_range==1):
        day_len_data=day_len(date_start,date_end)
        y = [None]*day_len_data
        for k in range(0,day_len_data):
            kwh_buffer=0
            IRRh_buffer=0
            endtime = starttime+ relativedelta(hours=+1) 
            for i in db.find({'ID':ID,'time': {'$gte': starttime,'$lt':endtime},'kwh':{'$nin':[0,None]}},{'_id':0}).sort('time',pymongo.DESCENDING).limit(1):#None

                kwh_buffer=kwh_buffer+i[kwh]
                IRRh_buffer=IRRh_buffer+i[IRRh]

                
                if (IRRh_buffer!=0) and (kw!=0):
                    if (IRRh_buffer>0.001):
                        y[k]=(kwh_buffer/kw) / (IRRh_buffer/ IRR)*100
                    else:
                        y[k]=0
                else:
                    y[k]=0
            
            starttime = endtime
    elif(date_range==2):
        _month_len = month_len(date_start,date_end)
        y = [None]*_month_len
        #starttime = datetime.datetime.strptime(str(starttime.year)+'-'+str(starttime.month)+'-01 00:00:00',"%Y-%m-%d %H:%M:%S")
        starttime = date_start
        for k in range(0,_month_len):
            kwh_buffer=0
            IRRh_buffer=0
            endtime = starttime+ relativedelta(days=+1) 
            

            for i in db.find({'ID':ID,'time': {'$gte': starttime,'$lt':endtime},'kwh':{'$nin':[0,None]}},{'_id':0}).sort('time',pymongo.DESCENDING).limit(24):#None
                
                kwh_buffer=kwh_buffer+i[kwh]
                IRRh_buffer=IRRh_buffer+i[IRRh]

                #print (i[IRRh])
            if (IRRh_buffer!=0) and (kw!=0):
                if (IRRh_buffer>0.001):
                    y[k]=(kwh_buffer/kw) / (IRRh_buffer/ IRR)*100
                else:
                    y[k]=0
            else:
                y[k]=0

            starttime = endtime
    elif(date_range==3):
        _year_len = year_len(date_start,date_end)
        y = [None]*_year_len
        #starttime  =  datetime.datetime.strptime(str(starttime.year)+'-01-01 00:00:00',"%Y-%m-%d %H:%M:%S")
        for k in range(len(y)):
            starttime = starttime
            endtime = datetime.datetime.strftime(starttime + relativedelta(months=+1), '%Y-%m')
            endtime = datetime.datetime.strptime(endtime, '%Y-%m')
            if k == len(y) - 1:   #最後一個月的搜尋時間應為date_end+1天
                endtime = date_end + datetime.timedelta(days=1)
            kwh_buffer=0
            IRRh_buffer=0
            
            for i in db.find({'ID':ID,'time': {'$gte': starttime,'$lt':endtime},'kwh':{'$nin':[0,None]}},{'_id':0}).sort('time',pymongo.DESCENDING).limit(744):#None
                kwh_buffer=kwh_buffer+i[kwh]
                IRRh_buffer=IRRh_buffer+i[IRRh]
                #print (i[kwh])
            
            if (IRRh_buffer!=0) and (kw!=0):
                if (IRRh_buffer>0.001):
                    y[k]=(kwh_buffer/kw) / (IRRh_buffer/ IRR)*100
                else:
                    y[k]=0
            else:
                y[k]=0
            
            starttime = endtime
    elif(date_range==4):
        #y = [None]*20
        #starttime = datetime.datetime.strptime (str(starttime.year-19)+'-01-01 00:00:00',"%Y-%m-%d %H:%M:%S")
        y = [None]*int(endtime.year-starttime.year+1)
        for k in range(len(y)):
            starttime  =  starttime
            endtime = datetime.datetime.strftime(starttime + relativedelta(years=1), '%Y')
            endtime = datetime.datetime.strptime(endtime, '%Y')
            if k == len(y) - 1:   #最後一個月的搜尋時間應為date_end+1天
                endtime = date_end + datetime.timedelta(days=1)
            kwh_buffer=0
            IRRh_buffer=0
            """ starttime  =  datetime.datetime.strptime (str(starttime.year) +'-01-01 00:00:00',"%Y-%m-%d %H:%M:%S")
            endtime = starttime + relativedelta(years=+1) """
            
            for i in db.find({'ID':ID,'time': {'$gte': starttime,'$lt':endtime},'kwh':{'$nin':[0,None]}},{'_id':0}).sort('time',pymongo.DESCENDING).limit(14880):#None
                kwh_buffer=kwh_buffer+i[kwh]
                IRRh_buffer=IRRh_buffer+i[IRRh]
            
            if (IRRh_buffer!=0) and (kw!=0):
                if (IRRh_buffer>0.001):
                    y[k]=(kwh_buffer/kw) / (IRRh_buffer/ IRR)*100
                else:
                    y[k]=0
            else:
                y[k]=0
            starttime = endtime
    return y
#-----------------------------------------------------------------------
# 光電展用 99M有用
# 未來拿掉時記得一起拿掉~
def plant_kwh_get(db, ID, date=datetime.date.today()):
    not_real_IRRh = [0,0,0,0,0,0,0.03298,0.21866,0.42101,0.61295,0.73565,0.7418,0.73961,0.43778,0.22833,0.16731,0.04046,0.00058,0,0,0,0,0,0]
    random.seed(int(ID, 16))
    gen_data = {'kwh': '---', 'today_kwh': '---', 'irrh': '---', 'today_kwh_list': [None]*24}
    starttime,endtime = date_interval(date)
    """ db.plant_gen.update_one({'ID': ID, 'time': starttime},
    { '$set':{
        'coefficient': 1,
        'base': 100,
        'kwh': [0, 0, 0, 0, 0, 10, 20, 30, 40 , 50 , 60, 70, 60 , 50, 40, 30, 20, 10, 0, 0, 0,0,0,0,0]
    }
    },upsert=True) """
    base_kwh = None
    for data in db.plant_gen.find({'ID': ID, 'time': starttime}):
        base_kwh = data.get('base', None)
        plant_gen_list = data.get('kwh', None)
        coefficient = data.get('coefficient', 1)
        now_time = datetime.datetime.strftime(datetime.datetime.now(), '%Y-%m-%d %H')
        now_time = datetime.datetime.strptime(now_time, '%Y-%m-%d %H')
        time_cursor = starttime
        gen_data['today_kwh'] = 0
        gen_data['irrh'] = 0
        while time_cursor <= now_time:
            gen_data['today_kwh'] +=  plant_gen_list[int((now_time-time_cursor).seconds/3600)]
            gen_data['irrh'] += not_real_IRRh[int((now_time-time_cursor).seconds/3600)]*random.uniform(0.95, 1)
            try:
                gen_data['today_kwh_list'][int((now_time-time_cursor).seconds/3600)]= (plant_gen_list[int((now_time-time_cursor).seconds/3600)])*coefficient
            except:
                pass
            time_cursor += datetime.timedelta(hours=1)
        gen_data['today_kwh'] *= coefficient
        if base_kwh != None:
            gen_data['kwh'] = base_kwh + gen_data['today_kwh']
    
    return gen_data
#-----------------------------------------------------------------------
