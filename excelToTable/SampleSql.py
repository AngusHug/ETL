import  os
'''
@class:随机抽样数据demo
@function:
    1.输入标签名称以及对应的字段名，表名 生成建表语句
        * 固定字段
        * 分区字段
        * 生成建表语句
    2.SampleSqlCmd():生成抽样数据的sql
    2.创建分类对应的.sql文件
    3.将sql写入对应的.sql文件

@author:huangdh
'''
class NerConcat:
    def SampleSqlCmd(self,tabNer_dic, tabClassify_dic,splitChar):
        nullNer = []
        outList = {}
        for key in tabClassify_dic:
            sql_str = ""
            trafficNer_list = trafficNer_dic 
            nerNum = len(tabNer_dic)-1
            for ner in trafficNer_list:
                if trafficNer_list.index(ner) != nerNum:
                    sql_str = sql_str + 'concat(' + ner + ',' +splitChar + '),' + '\r'
                else:
                    sql_str = sql_str + ner
            sql_str = "select " + sql_str + " \rfrom " + key + "\rwhere pt = '${pt}' \rorder by rand() limit 500; "
            outList[tabClassify_dic[key]] = sql_str
        print(outList)
        return  outList
    def sqlDocCreate(self, tabClassify_dic):
        # sqlPath = r"F:\工作\述职\01.行业结构化\\"
        failTab = []
        fileName_dic = {}
        for key in tabClassify_dic:
            try:
                sqlPath = r"F:\工作\述职\01.行业结构化\交通出行抽样数据\\"
                Path = sqlPath +  tabClassify_dic[key] + ".sql"
                file = open(Path, 'w')
            except:
                print(tabClassify_dic[key], "创建文件失败")
                failTab.append(tabClassify_dic[key])
        return failTab
    def sqlWriter(self, sqlStr_dic, tabClassify_dic):
        for key in tabClassify_dic:
            print(sqlStr_dic[tabClassify_dic[key]])
            filePath = r"F:\工作\述职\01.行业结构化\交通出行抽样数据\\" + tabClassify_dic[key] + ".sql"
            if os.path.exists(filePath):
                file = open(filePath, 'w')
                file.write(sqlStr_dic[tabClassify_dic[key]])
                file.close()
            '''
            try:
                if os.path.exists(filePath):
                    with open(filePath) as file:
                        file.write(sqlStr_dic[tabClassify_dic[key]])
            except:
                print("数据写入失败")
            '''
trafficNer_dic = ['row_key' ,'app_name'  ,'phone_id'  ,'event_time' ,'msg','main_call_no'  ,'category','prob','ext_info'  ,'dentify_id','order_id','dept_station','dest_station',\
    'train_number','status','general_date','general_time','name','money','address','airline_company','traffic_violations','seat','net_car','car_number','deduction','vehicle_type','ticket_amount','mobile_id_txt']
carNer_dic = ['row_key','app_name','phone_id','event_time','msg','main_call_no','category','prob','ext_info','dentify_id','general_date','general_time',\
    'status','name','mobile_id_txt','address','car_number','license_id','brand','car_model','vehicle_type','driving_subjects','car_status','shop_name']
CartabClassify_dic=\
    {
    'nlp_dev.car_txt_license_exam_fdt':'汽车_驾照_考试'
    ,'nlp_dev.car_txt_license_check_fdt':'汽车_驾照_审验'
    ,'nlp_dev.car_txt_license_record_fdt':'汽车_驾照_记分'
    ,'nlp_dev.car_txt_license_renewal_fdt':'汽车_驾照_办证'
    ,'nlp_dev.car_txt_license_course_fdt':'汽车_学车'
    ,'nlp_dev.car_txt_deal_buycar_fdt':'汽车_买车'
    ,'nlp_dev.car_txt_deal_plate_fdt':'汽车_车牌号预选'
    ,'nlp_dev.car_txt_charge_fdt':'汽车_充电'
    ,'nlp_dev.car_txt_gas_recharge_fdt':'汽车_加油_充值'
    ,'nlp_dev.car_txt_gas_consu_fdt':'汽车_加油_消费'
    ,'nlp_dev.car_txt_reference_fdt':'汽车_备案'
    ,'nlp_dev.car_txt_check_inspect_fdt':'汽车_车检_年检'
    ,'nlp_dev.car_txt_check_annual_audit_fdt':'汽车_车检_年审'
    ,'nlp_dev.car_txt_washcar_fdt':'汽车_洗车'
    ,'nlp_dev.car_txt_maintain_fdt':'汽车_保养'
    ,'nlp_dev.car_txt_other_fdt':'汽车-其他'
    ,'nlp_dev.car_txt_marketing_fdt':'汽车-营销'
    ,'nlp_dev.car_txt_verification_code_fdt':'汽车_验证码'
    
    }

TraffictabClassify_dic = \
    {
    'nlp_dev.traffic_txt_railway_tick_buy_fdt':'交通出行_铁路交通_购票'
    ,'nlp_dev.traffic_txt_railway_tick_change_fdt':'交通出行_铁路交通_改签'
    ,'nlp_dev.traffic_txt_railway_tick_refund_fdt':'交通出行_铁路交通_退票'
    ,'nlp_dev.traffic_txt_railway_tick_abnormal_fdt':'交通出行_铁路交通_异常'
    ,'nlp_dev.traffic_txt_airway_tick_buy_fdt':'交通出行_航空交通_购票'
    ,'nlp_dev.traffic_txt_airway_tick_change_fdt':'交通出行_航空交通_改签'
    ,'nlp_dev.traffic_txt_tairway_tick_refund_fdt':'交通出行_航空交通_退票'
    ,'nlp_dev.traffic_txt_airway_tick_abnormal_fdt':'交通出行_航空交通_异常'
    ,'nlp_dev.traffic_txt_airway_airport_service_fdt':'交通出行_航空交通_接送机'
    ,'nlp_dev.traffic_txt_airway_checkin_fdt':'交通出行_航空交通_值机'
    ,'nlp_dev.traffic_txt_airway_tick_delivery_fdt':'交通出行_航空交通_机票配送'
    ,'nlp_dev.traffic_txt_airway_other_fdt':'交通出行_航空交通_其他'
    ,'nlp_dev.traffic_txt_waterway_tick_buy_refund_fdt':'交通出行_水路交通'
    ,'nlp_dev.traffic_txt_bus_tick_buy_refund_fdt':'交通出行_客车'
    ,'nlp_dev.traffic_txt_netcar_self_fdt':'交通出行_网约车_自己出行'
    ,'nlp_dev.traffic_txt_netcar_me2other_fdt':'交通出行_网约车_好友出行'
    ,'nlp_dev.traffic_txt_netcar_other_fdt':'交通出行_网约车_其他'
    ,'nlp_dev.traffic_txt_designdrive_order_fdt':'交通出行_代驾_订单'
    ,'nlp_dev.traffic_txt_publicway_order_fdt':'交通出行_共享单车_订单'
    ,'nlp_dev.traffic_txt_publicway_unlaw_fdt':'交通出行_共享单车_平台违规'
    ,'nlp_dev.traffic_txt_publicway_other_fdt':'交通出行_共享单车_其他'
    ,'nlp_dev.traffic_txt_rentcar_order_fdt':'交通出行_租车_订单'
    ,'nlp_dev.traffic_txt_rentcar_unlaw_fdt':'交通出行_租车_违章处理'
    ,'nlp_dev.traffic_txt_rentcar_other_fdt':'交通出行_租车_其他'
    ,'nlp_dev.traffic_txt_inform_notice_fdt':'交通出行_机构通知_交通提醒'
    ,'nlp_dev.traffic_txt_inform_movecar_fdt':'交通出行_机构通知_移车'
    ,'nlp_dev.traffic_txt_inform_unlaw_fdt':'交通出行_机构通知_违章'
    ,'nlp_dev.traffic_txt_inform_parking_fdt':'交通出行_机构通知_停车'
    ,'nlp_dev.traffic_txt_inform_restriction_fdt':'交通出行_机构通知_限行'
    ,'nlp_dev.traffic_txt_inform_expressway_consu_fdt':'交通出行_机构通知_高速收费'
    ,'nlp_dev.traffic_txt_inform_appeal_fdt':'交通出行_机构通知_申诉'
    ,'nlp_dev.traffic_txt_inform_park_book_fdt':'交通出行_机构通知_车位预订'
    ,'nlp_dev.traffic_txt_inform_monitor_fdt':'交通出行_机构通知_车辆监控'
    ,'nlp_dev.traffic_txt_etc_fdt':'交通出行_ETC'
    ,'nlp_dev.traffic_txt_other_fdt':'交通出行_其他'
    ,'nlp_dev.traffic_txt_marketing_fdt':'交通出行_营销'
    ,'nlp_dev.traffic_txt_verification_code_fdt':'交通出行_验证码'
}
res = NerConcat()
sql_cmd = res.SampleSqlCmd(trafficNer_dic, TraffictabClassify_dic, "'#ALGO_COL_SEP#'")
res.sqlDocCreate(TraffictabClassify_dic)
res.sqlWriter(sql_cmd, TraffictabClassify_dic)