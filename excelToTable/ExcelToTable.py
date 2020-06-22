'''
@class:用于固定格式的excel文件读取拼接成hive建表语句
@function:
    1.表头重复校验(用于做表备注)
    2.表名称校验(不同行为分类表名一致，提示修改)
    3.字段名与字段备注一一映射校验(确保同一备注在同一文件内只有一个对应的字段名,减少歧义发生)
    4.拼接sql 写入对应表格列
@author:huangdh
'''
import pandas as pd
import xlrd
class ExcelToTable:
    def __init__(self,ExcelPath, SheetName):
        self.ExcelPath = ExcelPath
        self.SheetName = SheetName
        
    # 读取文件
    def ReadExcel(self, excel_path, sheet_name):
        try:
            data = pd.read_excel(excel_path, sheet_name=sheet_name, header=None)
            return data
        except:
            print("文件不存在哦!")
            
    # 校验表头(用做表备注), 表名, 字段名备注是否有重复/缺失
    def TableKeyInfo(self, data, parition_name):
        tab_dict = {}
        tab_comment_dict = {}
        TableCommonCol = \
            "row_key string comment 'row key',\r\n  app_name string comment '平台名称',\r\n"\
            + " phone_id string comment '手机号ID',\r\n"\
            + "event_time string comment '事件时间',\r\n msg string COMMENT '短文本',\r\n"\
            + "main_call_no string comment '主叫号码ID',\r\n category string comment '分类名称',\r\n"\
            + "prob		string	comment'分类概率值',\r\n ext_info string comment'扩展字段' ,"
        for row_num in range(len(data)):
            # 构建表名及索引构成的字典
            row_data = data.ix[row_num].values
            if(row_data[0] == "表名"):
                tab_dict[row_num] = row_data[1]
                tab_comment_dict[row_data[1]] = data.ix[row_num-1].values[0]
        
        # 拼接建表语句
        tab_index = list(tab_dict.keys())
        tab_name = list(tab_dict.values())
        tab_comment = list(tab_comment_dict.values())
       
        # 相邻两个表名间索引
        row_index = 0
        '''
        ###待解决问题###
        for tab_num in range(len(table_dict)):
            print("这是第",tab_num, "次循环")
            sql_str = "create table if not exists " + tab_name[tab_num] + '(' + TableCommonCol
            while row_index < tab_index[tab_num+1] - 2:
                if (row_index > tab_index[tab_num]+1 and row_index < tab_index[tab_num+1]-2):
                    col_str = data.ix[row_index][1] + '\t' + data.ix[row_index][2] + '\t' \
                              + data.ix[row_index][3] + ',' + '\r\n'
                    sql_str = sql_str + col_str
                row_index += 1
        '''
        tab_num = 0
        sql_str = "create table if not exists " + tab_name[tab_num] + '(' + TableCommonCol + '\r\n'
        tab_comment_str = ")" + "comment'" + tab_comment_dict[tab_name[tab_num]] + "'\r\npartition by" + parition_name + ";"
        for row_index in range(len(data)):
            if row_index > tab_index[tab_num]+1:
                if data.iloc[row_index].isnull().sum() != 6:
                    #print(data.ix[row_index][1], '***********',data.ix[row_index][2], '******', data.ix[row_index][3])
                    col_str = data.ix[row_index][1] + "\t" + data.ix[row_index][2] + "\t" \
                      + "comment'" + data.ix[row_index][3] + "'" + ",\r\n"
                    sql_str = sql_str + col_str
                    row_index += 1
                else:
                    sql_str = sql_str + tab_comment_str
                    data.ix[tab_index[tab_num]+1][5] = sql_str
                    #print(sql_str)
                    #print(data.ix[tab_index[tab_num]+1][5])
                    tab_num += 1
                    row_index += 1
                    sql_str = "create table if not exists " + tab_name[tab_num] + '(' + TableCommonCol + '\r\n'
        return data
        '''
        ***知识点***
        # * 每行遍历输出每行的col_name:value对应值
        # * 用列名访问每一列元素
        for row in data.iterrows():
            print(row)
            
        # * 按列遍历 输出col_name以及 index value对应的series
        for row in data.iteritems():
            print(row)
            
        # * 返回元组 输出每一行col_name = value所组成的元组
        for row in data.itertuples():
            print(row)
        '''
    def WriteExcel(self, data, excel_path, sheet_name):
        data.to_excel(excel_path, sheet_name='sheet_name')
ReadExcelPath = 'C:/Users/Administrator/Desktop/DWB表结构设计1114.xlsx'
ExcelPath = "D:\python_Course\ETL\PythonHive\DWB表结构设计1114.xlsx"
SheetName = "交通出行"
PartitionName = "(pt string comment'数据处理日期',\r\n the_date comment '业务日期')"
res = ExcelToTable(ReadExcelPath, SheetName)
#res.ReadExcel(ExcelPath, SheetName)
#res.TableKeyInfo(res.ReadExcel(ReadExcelPath, SheetName), PartitionName)
res.WriteExcel(res.TableKeyInfo(res.ReadExcel(ReadExcelPath, SheetName), PartitionName), ExcelPath, 'new_traffic')
