#coding=utf-8
# from docx import Document
# from docx.shared import Inches # 處理圖片大小
# from docx.enum.text import WD_PARAGRAPH_ALIGNMENT # 處理段落的置中
# # WD_ALIGN_PARAGRAPH, WD_TAB_ALIGNMENT, WD_TAB_LEADER  # 會有紅色下劃線報異常，不過可以正常使用
# from docx.enum.table import WD_ALIGN_VERTICAL # 處理表格中的字的置中
# from docx.enum.text import WD_ALIGN_PARAGRAPH # 表格內文字致中
# # from docx.enum.table import WD_ALIGN_PARAGRAPH
# from docx.enum.table import WD_TABLE_ALIGNMENT # 處理表格的置中
# from docx.shared import Cm, Pt  #加入可調整的 word 單位
# from docx.shared import RGBColor #調整顏色
# from docx.oxml.ns import qn # 字體轉為標楷體
import xlrd
import xlwt
from xlutils.copy import copy

import pymongo
from pymongo import MongoClient
import datetime
from dateutil.relativedelta import relativedelta, MO
import pandas as pd
import calendar
from bson.objectid import ObjectId

import os
from urllib.parse import quote_plus

import sys
import logging 
from logging.handlers import RotatingFileHandler

from io import BytesIO

import time


def ExcelKeyinData(db,time_info,data_info,basic_info,style_all):
    try:
        # =======================================================================
        # =======================================================================
        # =======================================================================
        today = time_info.get('today','')
        this_monday = time_info.get('this_monday','')
        save_time = time_info.get('save_time','')

        total_plant_num = basic_info.get('total_plant_num','')
        total_capacity = basic_info.get('total_capacity','')
        total_fee = basic_info.get('total_fee','')
        pageType = basic_info.get('pageType','')
        # =======================================================================
        # =======================================================================
        # =======================================================================
        # 開啟想要更改的excel檔案
        # old_excel = xlrd.open_workbook('/var/www/solar-system-tw/static/excel/2020.xls', formatting_info=True)
        try:
            file_path = os.getenv('FILE_PATH', 'init_config')
            old_excel = xlrd.open_workbook('./{}/SPS-week-A.xls'.format(file_path), formatting_info=True)
        except: # Use Default
            old_excel = xlrd.open_workbook('./week_A_excel/SPS-week-A.xls'.format(file_path), formatting_info=True)
        # 將操作檔案物件拷貝，變成可寫的workbook物件
        new_excel = copy(old_excel)
        # 獲得第一個sheet的物件
        ws = new_excel.get_sheet(0)
        # =======================================================================
        # ws.write       寫入標題(0,0)-->(123,ABC)
        # ws.write_merge 合併(X1,X2 ,Y1,Y2)
        # =======================================================================
        # 標題
        ws.write_merge(0,0, 0,5, "統計日期：{},總併網案場:{}個,累積裝置量:{} kWp".format(this_monday.date(),total_plant_num,total_capacity),style_all[0].ttt()) # 合併並置中
        ws.write_merge(1,1, 0,5, "累計電費收入{}元".format(total_fee),style_all[0].ttt()) # 合併並置中
        print('total_fee:',total_fee)
        
        for total_plant_nums in range(int(total_plant_num)):
            # 案場代號
            ws.write(2, 2+total_plant_nums, str(data_info.loc[total_plant_nums,'plant_code']),style_all[1].ttt()) # 調整數值
            # 案場名稱
            ws.write(3, 2+total_plant_nums, str(data_info.loc[total_plant_nums,'plant_name']),style_all[1].ttt()) # 調整數值
            # 裝置容量
            ws.write(4, 2+total_plant_nums, str(data_info.loc[total_plant_nums,'plant_capacity']),style_all[1].ttt()) # 調整數值
            # 模組
            ws.write(5, 2+total_plant_nums, str(data_info.loc[total_plant_nums,'plant_module']),style_all[1].ttt()) # 調整數值
            # 模組數量
            ws.write(6, 2+total_plant_nums, str(data_info.loc[total_plant_nums,'plant_module_number']),style_all[1].ttt()) # 調整數值
            # 變流器型號
            ws.write(7, 2+total_plant_nums, str(data_info.loc[total_plant_nums,'plant_inverter']),style_all[1].ttt()) # 調整數值
            # 模板角度
            ws.write(8, 2+total_plant_nums, str(data_info.loc[total_plant_nums,'plant_angle']),style_all[1].ttt()) # 調整數值
            # PVSYST
            ws.write(9, 2+total_plant_nums, str(data_info.loc[total_plant_nums,'plant_pvsyst']),style_all[1].ttt()) # 調整數值
            # 案場掛表日期
            ws.write(10, 2+total_plant_nums, str(data_info.loc[total_plant_nums,'plant_start_date']),style_all[1].ttt()) # 調整數值
            # 台電電費單 最新一期日期
            ws.write(11, 2+total_plant_nums, str(data_info.loc[total_plant_nums,'plant_taipower_fee']),style_all[1].ttt()) # 調整數值
            # 本期DMY
            ws.write(12, 2+total_plant_nums, str(data_info.loc[total_plant_nums,'plant_taipowerBill_DMY_this']),style_all[1].ttt()) # 調整數值
            # 上期DMY
            ws.write(13, 2+total_plant_nums, str(data_info.loc[total_plant_nums,'plant_taipowerBill_DMY_last']),style_all[1].ttt()) # 調整數值
            # 總累計天數
            ws.write(14, 2+total_plant_nums, str(data_info.loc[total_plant_nums,'plant_accumulation_date']),style_all[1].ttt()) # 調整數值
            # 平均累計DMY
            ws.write(15, 2+total_plant_nums, str(data_info.loc[total_plant_nums,'plant_average_DMY']),style_all[1].ttt()) # 調整數值
            # DMY gain
            try:
                print('data_info.loc[total_plant_nums,plant_gain_num]:',data_info.loc[total_plant_nums,'plant_gain_num'])
                if 5 <= data_info.loc[total_plant_nums,'plant_gain_num']:
                    ws.write(16, 2+total_plant_nums, str(data_info.loc[total_plant_nums,'plant_gain']),style_all[2].ttt()) # 調整數值
                elif 0 <= data_info.loc[total_plant_nums,'plant_gain_num'] < 5:
                    ws.write(16, 2+total_plant_nums, str(data_info.loc[total_plant_nums,'plant_gain']),style_all[3].ttt()) # 調整數值
                elif data_info.loc[total_plant_nums,'plant_gain_num'] < 0:
                    ws.write(16, 2+total_plant_nums, str(data_info.loc[total_plant_nums,'plant_gain']),style_all[4].ttt()) # 調整數值
            except:
                ws.write(16, 2+total_plant_nums, str(data_info.loc[total_plant_nums,'plant_gain']),style_all[2].ttt()) # 調整數值
        # =======================================================================
        # =======================================================================
        # =======================================================================
        # 存檔
        filename = ''
        if len(pageType) == 0:
            filename = '{}-{}_週報表A.xls'.format(today.year,'pv_lgroup_name')
            # save_path = ('week_report/{}'.format(filename))
            #new_excel.save('./week_report/{}'.format(filename)  )
        
            
        else:
            """ if os.path.isdir('week_report/{}'.format(pageType[0]['pageType'])):
                pass
            else:
                os.makedirs('week_report/{}'.format(pageType[0]['pageType'])) """
            filename = '{}-{}-{}_週報表A.xls'.format(this_monday.year,this_monday.month,this_monday.day)
            #new_excel.save('./week_report/{}/{}'.format(pageType[0]['pageType'],filename)  )

        output = BytesIO()
        new_excel.save(output)
        output.seek(0)

        print('word_day save_time',save_time)

        week_docx_data = db['week_docx'].update_one({'time':this_monday},{'$set':{'time':this_monday,'filename':filename,'show':1}},upsert=True)
        if week_docx_data:
            print('upsert to mongo') 
        else:
            week_wordA_error.error('{}: {}'.format('upsert to mongo',e))
        
        return { 'filename':  '{}-{}-{}_週報表A.xls'.format(this_monday.year,this_monday.month,this_monday.day) }, output
    except Exception as e:
        print(datetime.datetime.now(),'ExcelKeyinData',e)
        week_wordA_error.error('{}: {}'.format('ExcelKeyinData',e))

class AllStyle():
    def __init__(self,top,bottom,left,right,font_name,font_height,font_bold,pattern_fore_colour,alignment_horz): 
        
        self.style = xlwt.XFStyle()
        self.top = top
        self.bottom = bottom
        self.left = left
        self.right = right

        self.font = xlwt.Font()
        self.font_height = font_height
        self.font_name = font_name
        self.font_bold = font_bold

        self.pattern = xlwt.Pattern()
        self.pattern.pattern = xlwt.Pattern.SOLID_PATTERN
        self.pattern_fore_colour = pattern_fore_colour

        self.alignment = xlwt.Alignment()
        self.alignment_horz = alignment_horz
        pass
    def ttt(self):
        # 邊框呈現
        if type(self.left) == int:
            self.style.borders.left = self.left
        if type(self.right) == int:
            self.style.borders.right = self.right
        if type(self.top) == int:
            self.style.borders.top = self.top
        if type(self.bottom) == int:
            self.style.borders.bottom = self.bottom
        # 字體呈現
        self.font.name = self.font_name
        self.font.height = self.font_height
        self.font.bold = self.font_bold
        # 背景顏色呈現
        self.style.font = self.font
        self.pattern.pattern_fore_colour = self.pattern_fore_colour
        self.style.pattern = self.pattern
        # 對齊呈現
        self.alignment.horz = self.alignment_horz
        self.style.alignment = self.alignment

        # print('pass')       
    
        return self.style

def week_mainA(db=None):
    try:
        print('GOGOGO')
        if db == None: # Manual Connection
            # connect to mongodb  DESCENDING降序 ASCENDING升序
            MONGO_HOST = os.getenv('MONGODB_HOSTNAME', 'localhost')
            MONGO_PORT = os.getenv('MONGODB_PORT', '27017')
            MONGO_USER = os.getenv('MONGODB_USERNAME', 'root')
            MONGO_PASS = os.getenv('MONGODB_PASSWORD', 'pc152')
            MONGO_HOST = '210.242.178.151'
            MONGO_PORT = '27017'
            MONGO_USER = 'root'
            MONGO_PASS = 'pc152'
            MONGO_RS_NAME = os.getenv('MONGO_RS_NAME','rs0')
            # uri = "mongodb://{}:{}@{}:{}/".format(MONGO_USER, MONGO_PASS, MONGO_HOST, MONGO_PORT)
            # conn = MongoClient(uri, connect=False)
            host_split = str(MONGO_HOST).split(',')
            port_split = str(MONGO_PORT).split(',')
            if len(host_split) == 1:
                uri = "mongodb://{}:{}@{}:{}/".format(quote_plus(MONGO_USER), quote_plus(MONGO_PASS), MONGO_HOST, MONGO_PORT )
                conn = MongoClient(uri, connect=False)
            if len(host_split) != 1:
                host_port = ''
                for hosts in range(len(host_split)):
                    host_port += host_split[hosts] + ':' + port_split[hosts]
                    if hosts != len(host_split) -1:
                        host_port += ','
                uri = "mongodb://{}:{}@{}/?replicaSet={}".format(quote_plus(MONGO_USER), quote_plus(MONGO_PASS) , host_port , MONGO_RS_NAME)
                conn = MongoClient(uri,connect=False)
            db = conn['pv'] # connect database

        pageType = list(db['users'].find({ 'pageType':{'$exists':True} }))
        
        today = datetime.datetime.now().replace(hour=0,minute=0,second=0,microsecond=0)
        # today = datetime.datetime(2021,7,20)
        last4_monday = today.replace(hour=0,minute=0,second=0,microsecond=0) + datetime.timedelta(days=-today.weekday(), weeks=-4)
        this_monday  = today.replace(hour=0,minute=0,second=0,microsecond=0) + datetime.timedelta(days=-today.weekday(), weeks=-0)
        save_time = today
        print(save_time,' ',today,' ',last4_monday,' ',this_monday)
        
        # =======================================================================
        # =======================================================================
        # =======================================================================
        pandas_column = ['plant_code', 'plant_name', 'plant_capacity',
                         'plant_module','plant_module_number','plant_inverter',
                         'plant_angle','plant_pvsyst','plant_start_date',
                         'plant_taipower_fee','plant_accumulation_date','plant_average_DMY',
                         'plant_gain','plant_accumulation_income','plant_last4week_average_DMY',
                         'plant_difference',
                         'plant_taipowerBill_acc_date_this','plant_taipowerBill_DMY_this','plant_taipowerBill_DMY_last','plant_taipowerBill_DMY_total']
        total_information =pd.DataFrame(columns=pandas_column)        
        # 這邊放撈資料的東西
        plant_search = list(db['plant'].find({'used':1}))
        for i in range(len(plant_search)):
            try:
                if plant_search[i]['start_date'] >= today:
                    break
                print('==============================================')
                try:
                    error_point = 0
                    ############
                    # TaipowerBillandPvsyst
                    ############
                    plant_taipower_fee_time = ''
                    plant_taipower_fee_accumulation_data = ''
                    plant_average_DMY_data = ''
                    try:
                        # 判斷要取甚麼階層的電費單
                        try:
                            find_data = {'method':'TaipowerBillandPvsyst_level'}
                            level_setting = list(db['parameter_setting'].find(find_data).limit(1))[0].get('LEVEL', 'pv_plant')#.get('LEVEL', 'pv_plant')
                            print('level_setting:',level_setting)
                        except:
                            level_setting = 'pv_plant'
                        print('level_setting:',level_setting)

                        if level_setting == 'pv_plant':
                            find_data = {'ID':str(plant_search[i]['_id']),"method" : "TaipowerBill",'time':{'$lte':today} }
                        if level_setting == 'pv_lgroup':
                            find_data = {'PV': list(db['plant'].find({'_id':ObjectId(str(plant_search[i]['_id']))}))[0]['name'] ,'collection':'pv_lgroup' }
                            pv_ID = str(list(db['equipment'].find(find_data).limit(1))[0].get('_id', ''))
                            # print('pv_lgroup_ID:',pv_ID,type(pv_ID))
                            find_data = {'ID':str(pv_ID),"method" : "TaipowerBill",'time':{'$lte':today} }
                        if level_setting == 'pv_group':
                            find_data = {'PV': list(db['plant'].find({'_id':ObjectId(str(plant_search[i]['_id']))}))[0]['name'] ,'collection':'pv_group' }
                            pv_ID = str(list(db['equipment'].find(find_data).limit(1))[0].get('_id', ''))
                            # print('pv_group_ID:',pv_ID,type(pv_ID))
                            find_data = {'ID':str(pv_ID),"method" : "TaipowerBill",'time':{'$lte':today} }
                        
                        # 撈資料
                        find_data['show'] = 1 # Non-deleted data
                        print('find_data:',find_data)
                        plant_taipower_fee_scratch = []
                        plant_taipower_fee_scratch = list( db['TaipowerBillandPvsyst'].find(find_data).sort('time',pymongo.DESCENDING).limit(1) )
                        # print('plant_taipower_fee_scratch:',plant_taipower_fee_scratch)
                        for history_bill in range(len(plant_taipower_fee_scratch)):
                            try:
                                plant_taipower_fee_time = plant_taipower_fee_scratch[0]['time']
                            except Exception as e:
                                week_wordA_error.error('{}: {}'.format('plant_taipower_fee_time',e))
                            
                            try:
                                plant_taipower_fee_accumulation_data = (plant_taipower_fee_scratch[0]['endtime'] - plant_search[i]['start_date']).days
                                print('plant_taipower_fee_accumulation_data:',plant_taipower_fee_accumulation_data)

                                find_data = {'ID':find_data['ID'],'time':{'$lte':plant_taipower_fee_scratch[0]['endtime']}}
                                last_kwh = list( db['{}'.format(level_setting)].find(find_data).sort('time',pymongo.DESCENDING).limit(1) )
                                print('last_kwh:',last_kwh)
                                try:
                                    plant_average_DMY_data = round( float(last_kwh[0]['kwh'])/ float(plant_taipower_fee_accumulation_data) / float(plant_search[i]['capacity']),2)
                                except Exception as e:
                                    week_wordA_error.error('{}: {}'.format('plant_average_DMY_data',e))
                            except Exception as e:
                                week_wordA_error.error('{}: {}'.format('plant_taipower_fee_accumulation_data',e))
                            
                            # first_kwh = list( db['pv_plant'].find({'kwh':{'$nin':[0,None]},'ID':str(plant_search[i]['_id']),'time':{'$gte':plant_search[i]['start_date'],'$lte':plant_taipower_fee_time}}).sort('time',pymongo.ASCENDING).limit(1) )
                            # last_kwh  = list( db['pv_plant'].find({'kwh':{'$nin':[0,None]},'ID':str(plant_search[i]['_id']),'time':{'$gte':plant_search[i]['start_date'],'$lte':plant_taipower_fee_time}}).sort('time',pymongo.DESCENDING).limit(1) )
                            # print('first_kwh:',first_kwh[0]['kwh'],'last_kwh:',last_kwh[0]['kwh'])
                            # try:
                            #     plant_average_DMY_data = round((last_kwh[0]['kwh'] - first_kwh[0]['kwh'])/plant_taipower_fee_accumulation_data/plant_search[i]['capacity'],2)
                            # except Exception as e:
                            #     week_wordA_error.error('{}: {}'.format('plant_average_DMY_data',e))

                            
                    except Exception as e:
                        week_wordA_error.error('{}: {}'.format('plant_taipower_fee_scratch',e))
                    
                    ############
                    # Pvsyst
                    ############
                    plant_taipower_pvsyst_kwh = ''
                    plant_taipower_pvsyst_DMY = ''
                    plant_gain_data = ''
                    try:
                        # 判斷要取甚麼階層的電費單
                        try:
                            find_data = {'method':'TaipowerBillandPvsyst_level'}
                            level_setting = list(db['parameter_setting'].find(find_data).limit(1))[0].get('LEVEL', 'pv_plant')#.get('LEVEL', 'pv_plant')
                            print('level_setting:',level_setting)
                        except:
                            level_setting = 'pv_plant'
                        print('level_setting:',level_setting)

                        if level_setting == 'pv_plant':
                            find_data = {'ID':str(plant_search[i]['_id']),"method" : "TaipowerBill",'time':{'$lte':today} }
                        if level_setting == 'pv_lgroup':
                            find_data = {'PV': list(db['plant'].find({'_id':ObjectId(str(plant_search[i]['_id']))}))[0]['name'] ,'collection':'pv_lgroup' }
                            pv_ID = str(list(db['equipment'].find(find_data).limit(1))[0].get('_id', ''))
                            # print('pv_lgroup_ID:',pv_ID,type(pv_ID))
                            find_data = {'ID':str(pv_ID),"method" : "TaipowerBill",'time':{'$lte':today} }
                        if level_setting == 'pv_group':
                            find_data = {'PV': list(db['plant'].find({'_id':ObjectId(str(plant_search[i]['_id']))}))[0]['name'] ,'collection':'pv_group' }
                            pv_ID = str(list(db['equipment'].find(find_data).limit(1))[0].get('_id', ''))
                            # print('pv_group_ID:',pv_ID,type(pv_ID))
                            find_data = {'ID':str(pv_ID),"method" : "TaipowerBill",'time':{'$lte':today} }

                        # 撈資料
                        plant_taipower_pvsyst = []
                        find_data['show'] = 1 # Non-deleted data
                        print('find_data:',find_data)
                        plant_taipower_pvsyst = list( db['TaipowerBillandPvsyst'].find(find_data).sort('time',pymongo.DESCENDING).limit(1) )
                        print('plant_taipower_pvsyst:',plant_taipower_pvsyst)
                        if len(plant_taipower_pvsyst) != 0:
                            try:
                                plant_taipower_pvsyst_kwh = round(plant_taipower_pvsyst[0]['dmy'] * plant_search[i]['capacity'],2)
                            except Exception as e:
                                week_wordA_error.error('{}: {}'.format('plant_taipower_pvsyst_kwh',e))
                            
                            try:
                                plant_taipower_pvsyst_DMY = plant_taipower_pvsyst[0]['dmy']
                                print('plant_taipower_pvsyst_DMY:',plant_taipower_pvsyst_DMY,'plant_average_DMY_data:',plant_average_DMY_data)
                                plant_gain_data = round((plant_average_DMY_data - plant_taipower_pvsyst_DMY) / plant_taipower_pvsyst_DMY * 100,2)
                                print('plant_gain_data:',plant_gain_data)
                            except Exception as e:
                                plant_gain_data = ''
                                week_wordA_error.error('{}: {}'.format('plant_taipower_pvsyst_DMY',e))
                    except Exception as e:
                        week_wordA_error.error('{}: {}'.format('plant_taipower_pvsyst',e))
                    print('plant_gain_data:',plant_gain_data,type(plant_gain_data))
                    
                    ############
                    # pv income
                    ############
                    plant_accumulation_income_data = 0
                    plant_taipowerBill_acc_date_this = 0
                    plant_taipowerBill_DMY_this = 0
                    plant_taipowerBill_DMY_last = 0
                    plant_taipowerBill_DMY_total = 0
                    try:
                        # 判斷要取甚麼階層的電費單
                        try:
                            find_data = {'method':'TaipowerBillandPvsyst_level'}
                            level_setting = list(db['parameter_setting'].find(find_data).limit(1))[0].get('LEVEL', 'pv_plant')#.get('LEVEL', 'pv_plant')
                            print('level_setting:',level_setting)
                        except:
                            level_setting = 'pv_plant'
                        print('level_setting:',level_setting)

                        if level_setting == 'pv_plant':
                            find_data = {'ID':str(plant_search[i]['_id']),"method" : "TaipowerBill",'time':{'$lte':today} }
                        if level_setting == 'pv_lgroup':
                            find_data = {'PV': list(db['plant'].find({'_id':ObjectId(str(plant_search[i]['_id']))}))[0]['name'] ,'collection':'pv_lgroup' }
                            pv_ID = str(list(db['equipment'].find(find_data).limit(1))[0].get('_id', ''))
                            # print('pv_lgroup_ID:',pv_ID,type(pv_ID))
                            find_data = {'ID':str(pv_ID),"method" : "TaipowerBill",'time':{'$lte':today} }
                        if level_setting == 'pv_group':
                            find_data = {'PV': list(db['plant'].find({'_id':ObjectId(str(plant_search[i]['_id']))}))[0]['name'] ,'collection':'pv_group' }
                            pv_ID = str(list(db['equipment'].find(find_data).limit(1))[0].get('_id', ''))
                            # print('pv_group_ID:',pv_ID,type(pv_ID))
                            find_data = {'ID':str(pv_ID),"method" : "TaipowerBill",'time':{'$lte':today} }

                        # 撈資料
                        find_data['show'] = 1 # Non-deleted data
                        plant_taipower_fee_all = []
                        plant_taipower_fee_all = list( db['TaipowerBillandPvsyst'].find(find_data).sort('time',pymongo.DESCENDING) )
                        if len(plant_taipower_fee_all) != 0:
                            for bills in range(len(plant_taipower_fee_all)):
                                try:
                                    plant_accumulation_income_data = plant_accumulation_income_data + plant_taipower_fee_all[bills]['fee']
                                except:
                                    print('plant_accumulation_income_data:',e)
                                try:
                                    if bills == 0:
                                        bill_start = plant_taipower_fee_all[bills]['time']
                                        bill_end   = plant_taipower_fee_all[bills]['endtime']
                                        plant_taipowerBill_acc_date_this = (bill_end - bill_start).days + 1
                                        plant_taipowerBill_DMY_this = round(plant_taipower_fee_all[bills]['kwh']/plant_taipowerBill_acc_date_this/plant_search[i]['capacity'],4)
                                        print('plant_taipowerBill_acc_date_this:',plant_taipowerBill_acc_date_this)
                                except Exception as e:
                                    print('plant_taipowerBill_acc_date_this:',e)
                                try:
                                    if bills == 1:
                                        bill_start = plant_taipower_fee_all[bills]['time']
                                        bill_end   = plant_taipower_fee_all[bills]['endtime']
                                        plant_taipowerBill_acc_date_last = (bill_end - bill_start).days + 1
                                        plant_taipowerBill_DMY_last = round(plant_taipower_fee_all[bills]['kwh']/plant_taipowerBill_acc_date_last/plant_search[i]['capacity'],4)
                                        print('plant_taipowerBill_DMY_last:',plant_taipowerBill_DMY_last)
                                except Exception as e:
                                    plant_taipowerBill_DMY_last = ''
                                    print('plant_taipowerBill_DMY_last:',e)
                    except Exception as e:
                        week_wordA_error.error('{}: {}'.format('plant_taipower_fee_all',e))
                    if plant_accumulation_income_data == 0:
                        plant_accumulation_income_data = ''
                    else:
                        plant_accumulation_income_data = round(plant_accumulation_income_data,2)

                    ############
                    # module inverter type 模板型號
                    # print('module inverter type 模板型號')
                    ############
                    plant_module_device   = ''
                    plant_inverter_device = ''
                    try:
                        find_data = {'PV':plant_search[i]['name'],'collection':'inverter'}
                        plant_inverter_search = list( db['equipment'].find(find_data) )

                        plant_module_type_list = []
                        for inverters in range(len(plant_inverter_search)):
                            if ('AUO' not in plant_inverter_search[inverters]['module_model']) and ('PM' in plant_inverter_search[inverters]['module_model']):
                                plant_module_type = 'AUO '+plant_inverter_search[inverters]['module_model']                            
                            elif ('URE' not in plant_inverter_search[inverters]['module_model']) and ('D' in plant_inverter_search[inverters]['module_model']):
                                plant_module_type = 'URE '+plant_inverter_search[inverters]['module_model']
                            if (plant_module_type not in plant_module_type_list) and plant_module_type != '':
                                plant_module_type_list.append(plant_module_type)
                        for inverters in range(len(plant_module_type_list)):                        
                            plant_module_device = plant_module_device + plant_module_type_list[inverters]
                            if inverters != len(plant_module_type_list)-1:
                                plant_module_device = plant_module_device + ','
                        # print('plant_module_type_list:',plant_module_type_list)

                        plant_inverter_type_list = []
                        plant_inverter_number = []
                        for inverters in range(len(plant_inverter_search)):
                            # print('Device_model:',plant_inverter_search[inverters]['Device_model'])
                            if ('Delta' not in plant_inverter_search[inverters]['Device_model']) and ('M' in plant_inverter_search[inverters]['Device_model']):
                                plant_inverter_type = 'Delta '+plant_inverter_search[inverters]['Device_model']                            
                            elif ('HUAWEI' not in plant_inverter_search[inverters]['Device_model']) and ('sun' in plant_inverter_search[inverters]['Device_model']):
                                plant_inverter_type = 'HUAWEI '+plant_inverter_search[inverters]['Device_model']
                            elif ('SUNGROW' not in plant_inverter_search[inverters]['Device_model']) and ('SG' in plant_inverter_search[inverters]['Device_model']):
                                plant_inverter_type = 'SUNGROW '+plant_inverter_search[inverters]['Device_model']
                            # print(plant_inverter_type)
                            if (plant_inverter_type not in plant_inverter_type_list) and plant_inverter_type != '':
                                plant_inverter_type_list.append(plant_inverter_type)
                        for inverters in range(len(plant_inverter_type_list)):                        
                            plant_inverter_device = plant_inverter_device + plant_inverter_type_list[inverters]
                            if inverters != len(plant_inverter_type_list)-1:
                                plant_inverter_device = plant_inverter_device + ','
                        # print('plant_inverter_type_list:',plant_inverter_type_list)
                    except Exception as e:
                        week_wordA_error.error('{}: {}'.format('module inverter type 模板型號',e))
                    
                    ############
                    # 監控數據 近4周DMY
                    ############
                    plant_last4_week_DMY = 0
                    try:
                        first_kwh = list( db['pv_plant'].find({'kwh':{'$nin':[0,None]},'ID':str(plant_search[i]['_id']),'time':{'$gte':last4_monday,'$lt':this_monday}}).sort('time',pymongo.ASCENDING).limit(1) )
                        last_kwh  = list( db['pv_plant'].find({'kwh':{'$nin':[0,None]},'ID':str(plant_search[i]['_id']),'time':{'$gte':last4_monday,'$lt':this_monday}}).sort('time',pymongo.DESCENDING).limit(1) )
                        try:
                            plant_last4_week_DMY = round((last_kwh[0]['kwh'] - first_kwh[0]['kwh'])/((last_kwh[0]['time']-first_kwh[0]['time']).days+1)/plant_search[i]['capacity'],2)
                        except Exception as e:
                            week_wordA_error.error('{}: {}'.format('last 4 week DMY cal',e))
                        pass
                    except Exception as e:
                        week_wordA_error.error('{}: {}'.format('last 4 week DMY',e))
                    print('plant_last4_week_DMY:',plant_last4_week_DMY)

                    print('plant_search[i][name]:',plant_search[i]['name'])
                    try:
                        plant_code = '{}'.format(plant_search[i]['pv_plant_client_code']) # 廠商對案場的代碼
                    except:
                        plant_code = ''
                    plant_name = '{}'.format(plant_search[i]['name']) #案場名字
                    plant_capacity = '{}'.format(plant_search[i]['capacity']) # 案場容量
                    plant_module = '{}'.format(plant_module_device) # 案場採用模板型號
                    plant_module_number = '{}'.format(plant_search[i]['module']) # 模組數量
                    plant_inverter = '{}'.format(plant_inverter_device) # INV型號
                    try:
                        plant_angle = '{}'.format(plant_search[i]['angle']) # 模板角度等                
                    except:
                        plant_angle = ''
                    plant_pvsyst = '{}({})'.format(plant_taipower_pvsyst_kwh,plant_taipower_pvsyst_DMY) # PVSYST估計值
                    
                    plant_start_date = '{}'.format(plant_search[i]['start_date'].date()) # 案場掛表日期
                    if plant_taipower_fee_time != '':
                        plant_taipower_fee = '{}'.format(plant_taipower_fee_time.date()) # 台電電費單總金額
                    else:
                        plant_taipower_fee = ''
                    if plant_taipower_fee_accumulation_data != '':
                        plant_accumulation_date = '{}'.format(plant_taipower_fee_accumulation_data) # 案場建置至今的總日期
                    else:
                        plant_accumulation_date = ''
                    if plant_average_DMY_data != '':
                        plant_average_DMY = '{}'.format(plant_average_DMY_data) # 案場建置至上期台電電費單的平均DMY
                    else:
                        plant_average_DMY = ''
                    if plant_gain_data != '':
                        plant_gain = '{}%'.format(plant_gain_data) # 
                    else:
                        plant_gain = ''
                    plant_accumulation_income = '{}'.format(plant_accumulation_income_data)
                    plant_last4week_average_DMY = '{}'.format(plant_last4_week_DMY)
                    plant_difference = ''
                    
                    total_information.loc[i,'plant_code'] = plant_code
                    total_information.loc[i,'plant_name'] = plant_name
                    total_information.loc[i,'plant_capacity'] = plant_capacity
                    total_information.loc[i,'plant_module'] = plant_module
                    total_information.loc[i,'plant_module_number'] = plant_module_number
                    total_information.loc[i,'plant_inverter'] = plant_inverter
                    total_information.loc[i,'plant_angle'] = plant_angle
                    total_information.loc[i,'plant_pvsyst'] = plant_pvsyst
                    total_information.loc[i,'plant_start_date'] = plant_start_date
                    total_information.loc[i,'plant_taipower_fee'] = plant_taipower_fee
                    total_information.loc[i,'plant_accumulation_date'] = plant_accumulation_date
                    total_information.loc[i,'plant_average_DMY'] = plant_average_DMY
                    total_information.loc[i,'plant_gain'] = plant_gain
                    total_information.loc[i,'plant_gain_num'] = plant_gain_data
                    total_information.loc[i,'plant_accumulation_income'] = plant_accumulation_income
                    total_information.loc[i,'plant_last4week_average_DMY'] = plant_last4week_average_DMY                    
                    total_information.loc[i,'plant_taipowerBill_acc_date_this'] = plant_taipowerBill_acc_date_this
                    total_information.loc[i,'plant_taipowerBill_DMY_this'] = plant_taipowerBill_DMY_this
                    total_information.loc[i,'plant_taipowerBill_DMY_last'] = plant_taipowerBill_DMY_last
                    
                    # # 把PV改成lgroup資訊
                    # if plant_search[i]['plant_report_level'] != 'lgroup':
                    #     pass
                    # # 把PV改成group資訊
                    # elif plant_search[i]['plant_report_level'] != 'group':
                    #     pass
                    # else:
                    #     pass                
                except Exception as e:
                    week_wordA_error.error('{}: {}'.format('GetPlantProblem:',e))
            except Exception as e:
                week_wordA_error.error('{}: {}'.format('plant_content_setting_error',e))

        print(total_information)
        total_information = total_information.reset_index()
        print('total_information:')
        print(total_information)
        print(total_information.shape)
        print(total_information.loc[0,'plant_gain_num'],type(total_information.loc[0,'plant_gain_num']))
        print(total_information.loc[1,'plant_gain_num'],type(total_information.loc[1,'plant_gain_num']))
        # =======================================================================
        # =======================================================================
        # =======================================================================
        # last 4 week DMY sum and difference
        plant_last4week_DMY_max = ''
        plant_last4week_DMY_max = total_information['plant_last4week_average_DMY'].max()
        print('plant_last4week_DMY_max:',plant_last4week_DMY_max)
        if plant_last4week_DMY_max != '':
            for i in range(total_information.shape[0]):
                try:
                    # print(total_information.loc[i,'plant_last4week_average_DMY'])
                    # print(total_information.loc[i,'plant_last4week_average_DMY'],' ',type(total_information.loc[i,'plant_last4week_average_DMY']))
                    # print('plant_last4week_DMY_max:',plant_last4week_DMY_max,type(plant_last4week_DMY_max))
                    aa = float(total_information.loc[i,'plant_last4week_average_DMY'])
                    bb = float(plant_last4week_DMY_max)
                    total_information.loc[i,'plant_difference'] = '{}%'.format( str( round((aa / bb)*100,2) ) )
                except Exception as e:
                    print('plant_difference',e)
                    week_wordA_error.error('{}: {}'.format('plant_difference',e))
                # total_information.loc[i,'plant_difference'] = '1'
        # =======================================================================
        # =======================================================================
        # =======================================================================
        total_fee = 0
        try:
            # total_fee = total_information['plant_accumulation_income'].sum(axis = 1, skipna = True)
            for fees in range(total_information.shape[0]):
                try:
                    total_fee = total_fee + float(total_information.loc[fees,'plant_accumulation_income'])
                except Exception as e:
                    week_wordA_error.error('{}: {}'.format('total_fee',e))
            print('total_fee:',total_fee)
        except Exception as e :
            week_wordA_error.error('{}: {}'.format('total_fee',e))
        # =======================================================================
        # =======================================================================
        # =======================================================================
        total_plant_num = ''
        total_capacity  = 0
        try:
            total_plant_num = str(total_information.shape[0])
            for total_capacitys in range(total_information.shape[0]):
                try:
                    #total_capacity = round(total_capacity,2)
                    total_capacity = round(total_capacity + float(total_information.loc[total_capacitys,'plant_capacity']), 2)
                except Exception as e:
                    week_wordA_error.error('{}: {}'.format('total_capacity add',e))
        except Exception as e:
            print('total_plant_num & total_capacity',e)
            week_wordA_error.error('{}: {}'.format('total_plant_num & total_capacity',e))
        total_capacity = str(total_capacity)
        print('total_capacity:',total_capacity,'  total_plant_num:',total_plant_num)
        
        # =======================================================================
        # style_all setting
        # region 欄位屬性
            # AllStyle 參數說明(top,bottom,left,right,font_name,font_height,font_bold,pattern_fore_colour,alignment_horz)
            # -----------------------------------------------------------------------
            # 設置邊框 top bottom right left ：
            # borders = xlwt.Borders()
            # 細實線:1，小粗實線:2，細虛線:3，中細虛線:4，大粗實線:5，雙線:6，細點虛線:7
            # 大粗虛線:8，細點劃線:9，粗點劃線:10，細雙點劃線:11，粗雙點劃線:12，斜點劃線:13
            # borders.left = 6
            # borders.right = 1
            # borders.top = 3
            # borders.bottom = 4
            # borders.left_colour = 10
            # borders.right_colour = 11
            # borders.top_colour = 1
            # borders.bottom_colour = 2
            # -----------------------------------------------------------------------
            # 字體  font = xlwt.Font()
            # font.name = 'Times New Roman' , '標楷體'
            # font.height = 20*16 -->字體大小
            # font.bold = True --> 是否為粗體字
            # -----------------------------------------------------------------------
            # 設置背景顏色 pattern = xlwt.Pattern()
            # pattern.pattern = xlwt.Pattern.SOLID_PATTERN
            # pattern.pattern_fore_colour = 0x0A --> 背景顏色 0 黑色 1 白色 2 红色 3 绿色 4 蓝色 5 黄色 6 紫红色等等
            # -----------------------------------------------------------------------
            # 設置單元格對齊方式
            # alignment = xlwt.Alignment()
            # 0x01(左端對齊)、0x02(水平方向上居中對齊)、0x03(右端對齊)
            # alignment.horz = 0x03
            # 0x00(上端對齊)、 0x01(垂直方向上居中對齊)、0x02(底端對齊)
            # alignment.vert = 0x01
            # 設置自動換行
            # alignment.wrap = 1
        # =======================================================================
        # title 
        style0 = AllStyle(1,1,1,1,'Times New Roman',20*16,False,1,0x01)
        # content background white
        style1 = AllStyle(1,1,1,1,'Times New Roman',20*10,False,1,0x01)
        # content background green
        style2 = AllStyle(1,1,1,1,'Times New Roman',20*10,False,3,0x01)
        # content background yellow
        style3 = AllStyle(1,1,1,1,'Times New Roman',20*10,False,5,0x01)
        # content background red
        style4 = AllStyle(1,1,1,1,'Times New Roman',20*10,False,2,0x01)
        style_all = [style0,style1,style2,style3,style4]
        # =======================================================================
        # filling the excel
        # =======================================================================
        time_info = {'today': today,'this_monday': this_monday,'save_time': save_time}
        basic_info = {'total_plant_num': total_plant_num,'total_capacity': total_capacity,'total_fee': total_fee,'pageType': pageType}  
        data_info = total_information
        return ExcelKeyinData(db,time_info,data_info,basic_info,style_all)  
        
    except Exception as e:
        print(datetime.datetime.now(),'week_main',e)
        week_wordA_error.error('{}: {}'.format('week_main',e))

formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s',"%Y-%m-%d %H:%M:%S")
def setup_logger(name, level):
    """To setup as many loggers as you want"""
    if os.path.isdir('log'):
        pass
    else:
        os.makedirs('log')
    log_file = 'log/' + name + '.log'
    handler = logging.FileHandler(log_file)
    handler = RotatingFileHandler(log_file, mode='a', maxBytes=100*1024*1024, backupCount=5, encoding=None, delay=0) # 5*1024*1024
    handler.setFormatter(formatter)

    logger = logging.getLogger(name)
    logger.setLevel(level)
    logger.addHandler(handler)

    return logger


# file logger
week_wordA_error = setup_logger('week_word_errorA',logging.WARNING)
a = time.time()
try:
    week_mainA()
    pass
except Exception as e:
    week_wordA_error.error('{}: {}'.format('week_mainA first running',e))

print(time.time()-a)
# scheduler = BackgroundScheduler(job_defaults={'misfire_grace_time': 15*60})
# scheduler.add_job(week_mainA,'cron',day_of_week ='mon-sun',hour = 1,minute = 30,second = 0,id='week_everydayA') # 定時每天 00:30:00秒執行

# scheduler.start()

# while(1):
#     threadstart = 1
#     time.sleep(1000)