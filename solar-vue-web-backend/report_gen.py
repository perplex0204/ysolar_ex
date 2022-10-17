from flask import jsonify, request, send_file
import pandas as pd
import datetime
from io import BytesIO
from urllib.parse import quote
from dateutil.relativedelta import relativedelta
import sys
import traceback
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
#-------------------------------------------------------------------------------

def inv_excel_today(db, ID, inv_data):
    today = datetime.datetime.now() 
    today = today.replace(hour=0,minute=0,second=0,microsecond=0)
    try:
        
        project = {'_id':0,'ID':0}
        # if inverter_id[j]['Device_model'] == 'M30A':
        #     project = {'_id':0,'ID':0,'temp_inner':0,'temp_Boost_1':0,'temp_Boost_2':0,'temp_sink':0,'v_bus_1':0,'i_bus_1':0,'p_bus_1':0,'f_bus_1':0,'v_bus_2':0,'i_bus_2':0,'p_bus_2':0,'f_bus_2':0,'v_bus_3':0,'i_bus_3':0,'p_bus_3':0,'f_bus_3':0}
        # elif inverter_id[j]['Device_model'] == 'M88H':
        #     project = {'_id':0,'ID':0,'temp_inner':0,'temp_Boost_1':0,'temp_Boost_2':0,'temp_sink':0,'v_bus_1':0,'i_bus_1':0,'p_bus_1':0,'f_bus_1':0,'v_bus_2':0,'i_bus_2':0,'p_bus_2':0,'f_bus_2':0,'v_bus_3':0,'i_bus_3':0,'p_bus_3':0,'f_bus_3':0}

        # inverter_data_pandas = db.{ '$match' : { DTime : { '$gte' :ISODate('2019-03-07T16:00:00Z'),'$lte' :ISODate('2019-03-08T16:00:00Z') }, '$expr' : {'$ eq': [ { '$mod': [ { '$second': ' $DTime ' }, 30 ] }, 0 ]} } }
        # inverter_data_pandas = db.PR.aggregate({ '$match' : { 'time' : { '$gte' :ISODate('2019-03-07T16:00:00Z'),'$lte' :ISODate('2019-03-08T16:00:00Z') } } })
        # $mod:[a,b] --> 除A餘B(秒為最小單位)
        inverter_data_pandas = list( db.inverter.aggregate( [ { '$match':{ 'ID':str(ID) , 'time':{'$gte':today + relativedelta(hours=5,minute=1),'$lte':today + relativedelta(hours=19,minute=1)} , '$expr':{'$eq': [ { '$mod':[{'$second':'$time'},60] },0 ] } }  } , {"$project":project} , {'$sort' : { 'time' : 1 }} ] ) )
        #print(inverter_data_pandas)
        inverter_data_pandas = pd.DataFrame(inverter_data_pandas)
        inverter_data_pandas = inverter_data_pandas.reindex(reversed(inverter_data_pandas.columns), axis=1)
        for k in range(inverter_data_pandas.shape[0]):
            inverter_data_pandas.loc[k,'time'] = datetime.datetime( inverter_data_pandas.loc[k,'time'].year,inverter_data_pandas.loc[k,'time'].month,inverter_data_pandas.loc[k,'time'].day,inverter_data_pandas.loc[k,'time'].hour,inverter_data_pandas.loc[k,'time'].minute,0 )
        
        # rename
        # print(inverter_data_pandas.columns)
        inverter_data_pandas_columns = inverter_data_pandas.columns.tolist()
        # print((inverter_data_pandas_columns))            
        for k in range(len(inverter_data_pandas_columns)):
            # if inverter_data_pandas_columns[k] == 'COMport' :
            #     inverter_data_pandas = inverter_data_pandas.drop(columns=['COMport'])
            # if inverter_data_pandas_columns[k] == 'status' :
            #     inverter_data_pandas = inverter_data_pandas.drop(columns=['status'])
            if inverter_data_pandas_columns[k] == 'pf' :
                inverter_data_pandas = inverter_data_pandas.rename(columns={"pf": "功率因素"})
            elif inverter_data_pandas_columns[k] == 'q_bus_total' :
                inverter_data_pandas = inverter_data_pandas.rename(columns={"q_bus_total": "虛功總和"})


            elif inverter_data_pandas_columns[k] == 'time' :
                inverter_data_pandas = inverter_data_pandas.rename(columns={"time": "時間"})
            elif inverter_data_pandas_columns[k] == 'kwh' :
                inverter_data_pandas = inverter_data_pandas.rename(columns={"kwh": "發電量(kwh)"})
            elif inverter_data_pandas_columns[k] == 'temp_sink' :
                inverter_data_pandas = inverter_data_pandas.rename(columns={"temp_sink": "Ambient溫度"})
            elif inverter_data_pandas_columns[k] == 'temp_inner' :
                inverter_data_pandas = inverter_data_pandas.rename(columns={"temp_inner": "Inverter溫度"})
            
            elif 'temp_Boost_' in inverter_data_pandas_columns[k] :
                a = inverter_data_pandas_columns[k].split('_')
                inverter_data_pandas = inverter_data_pandas.rename(columns={"%s"%(inverter_data_pandas_columns[k]): "MPPT%s溫度"%(a[2])})
            elif 'f_bus_' in inverter_data_pandas_columns[k] :
                a = inverter_data_pandas_columns[k].split('_')
                inverter_data_pandas = inverter_data_pandas.rename(columns={"%s"%(inverter_data_pandas_columns[k]): "L%s頻率(Hz)"%(a[2])})                

            elif 'p_bus_total' in inverter_data_pandas_columns[k] :
                inverter_data_pandas = inverter_data_pandas.rename(columns={"%s"%(inverter_data_pandas_columns[k]): "交流功率(kW)"})
            elif 'p_cell_total' in inverter_data_pandas_columns[k] :
                inverter_data_pandas = inverter_data_pandas.rename(columns={"%s"%(inverter_data_pandas_columns[k]): "直流功率(kW)"})
            
            elif 'v_bus_' in inverter_data_pandas_columns[k] :
                a = inverter_data_pandas_columns[k].split('_')
                inverter_data_pandas = inverter_data_pandas.rename(columns={"%s"%(inverter_data_pandas_columns[k]): "L%s電壓(V)"%(a[2])})
            elif 'i_bus_' in inverter_data_pandas_columns[k] :
                a = inverter_data_pandas_columns[k].split('_')
                inverter_data_pandas = inverter_data_pandas.rename(columns={"%s"%(inverter_data_pandas_columns[k]): "L%s電流(A)"%(a[2])})
            elif 'p_bus_' in inverter_data_pandas_columns[k] :
                a = inverter_data_pandas_columns[k].split('_')
                inverter_data_pandas = inverter_data_pandas.rename(columns={"%s"%(inverter_data_pandas_columns[k]): "L%s功率(P)"%(a[2])})
            elif 'v_cell_' in inverter_data_pandas_columns[k] :
                a = inverter_data_pandas_columns[k].split('_')
                inverter_data_pandas = inverter_data_pandas.rename(columns={"%s"%(inverter_data_pandas_columns[k]): "MPPT%s電壓(V)"%(a[2])})
            elif 'i_cell_' in inverter_data_pandas_columns[k] :
                a = inverter_data_pandas_columns[k].split('_')
                inverter_data_pandas = inverter_data_pandas.rename(columns={"%s"%(inverter_data_pandas_columns[k]): "MPPT%s電流(A)"%(a[2])})
            elif 'p_cell_' in inverter_data_pandas_columns[k] :
                a = inverter_data_pandas_columns[k].split('_')
                inverter_data_pandas = inverter_data_pandas.rename(columns={"%s"%(inverter_data_pandas_columns[k]): "MPPT%s功率(P)"%(a[2])})
            elif 'v_pv_' in inverter_data_pandas_columns[k] :
                a = inverter_data_pandas_columns[k].split('_')
                inverter_data_pandas = inverter_data_pandas.rename(columns={"%s"%(inverter_data_pandas_columns[k]): "直流%s電壓(V)"%(a[2])})
            elif 'i_pv_' in inverter_data_pandas_columns[k] :
                a = inverter_data_pandas_columns[k].split('_')
                inverter_data_pandas = inverter_data_pandas.rename(columns={"%s"%(inverter_data_pandas_columns[k]): "直流%s電流(A)"%(a[2])})
            elif 'p_pv_' in inverter_data_pandas_columns[k] :
                a = inverter_data_pandas_columns[k].split('_')
                inverter_data_pandas = inverter_data_pandas.rename(columns={"%s"%(inverter_data_pandas_columns[k]): "直流%s功率(P)"%(a[2])})
            
            else:
                print(inverter_data_pandas_columns[k])
                inverter_data_pandas = inverter_data_pandas.drop(columns=['%s'%(inverter_data_pandas_columns[k])])
        try:
            inverter_data_pandas = inverter_data_pandas.set_index(['時間'])
        except: 
            pass
        # print(inverter_data_pandas.columns)

        output = BytesIO()
        writer = pd.ExcelWriter(output)
        inverter_data_pandas.to_excel(writer)
        writer.save()
        output.seek(0)

        #print(output)
        filename = '{}-{}-{}_{}_{}_{}_{}.xlsx'.format(today.year,today.month,today.day,inv_data['PV'],inv_data['lgroup'],inv_data['group'],inv_data['name'])
        #print(filename)
        
        #print(inverter_data_pandas)
    except Exception as e :
        print(e)
        return bad_request(500, 'Error Occur {}'.format(exception_detail(e)))
    filename = quote(filename)
    rv = send_file(
        output,
        as_attachment=True,
        download_name=filename
    )
    return rv