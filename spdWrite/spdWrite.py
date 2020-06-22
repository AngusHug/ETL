'''
@Author:ruoyu
@Date:2019/12/06 15:19
@FileName:spdWrite.py
'''
import json
import pandas as pd
import sys
class spdWrite:
    '''
    def __init__(self):
        self.loadPath = sys.argv[0]
        self.writeTable = sys.argv[1]
        self.keyList = sys.argv[2]
        '''
    def __init__(self, loadPath, writeTable, keyList):
        self.loadPath = loadPath
        self.writeTable = writeTable
        self.keyList = keyList
    def readTxt(self):
        with open(self.loadPath, 'r', encoding='utf-8') as f:
            data = f.read()
            data = pd.read_json(data, orient='records', lines=True)
            clomunName = data.columns.values
            
            print(data)
        '''
        read():read all file ,return str
        readline():read one line every time, return str
        readlines():read all file, return list
        
        '''
# if __name__ == "__main__":
#     res = spdWrite()
#     res.readTxt()
loadPath = "D:\python_Course\ETL\PythonHive\spdWrite\highway.json"
writeTable = "tmp.highWay"
keyList = ["name", "belong_highway"]
res = spdWrite(loadPath, writeTable, keyList=keyList)
res.readTxt()