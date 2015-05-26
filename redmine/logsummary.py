#!/usr/bin/python3
#encoding=UTF-8
#
# git提交日志统计；生成JS，显示到redmine里
#


from datetime import datetime 
from datetime import date
from datetime import timedelta
import cgi
import operator
import psycopg2

 
#配置文件
import config

conn = psycopg2.connect(config.PGURL)

print("Content-type:text/plain")
print("")

def queryData(beginDate):
    cur = conn.cursor()
    if(beginDate == None):
        cur.execute("select commitUser, score, count(*) cnt from git_commit_message where mergeId is null group by commitUser, score")
    else:
        cur.execute("select commitUser, score, count(*) cnt from git_commit_message where commitdate>=%s and mergeId is null group by commitUser, score", [beginDate])
        
    rows = cur.fetchall()
    cur.close()
    
    data = []
    for i in range(len(rows)):
        u = rows[i][0]
        dataRow = None
        for j in range(len(data)):
            if(u == data[j][0]):
                dataRow = data[j]
                break
        if(dataRow == None):
            dataRow = [u, 0, 0]
            data.append(dataRow)
            
        dataRow[1] += rows[i][2]
        if(rows[i][1] >= 3):
            dataRow[2] += rows[i][2]
        
    
    sortedData = sorted(data, key=operator.itemgetter(2), reverse=True)
    return sortedData

def printJSString(dataList, jsVar):
    print('var ', jsVar, '=new Array();')
    for i in range(len(dataList)):
        print(jsVar + '[', i, ']=new Array();');
        print(jsVar + '[', i, '][0]="' + dataList[i][0] + '";')
        print(jsVar + '[', i, '][1]=', dataList[i][1])
        print(jsVar + '[', i, '][2]=', dataList[i][2])

today = date.today()
#近一周
data = queryData(today + timedelta(days=-7))
printJSString(data, 'logSummary7')

#一个月内
data = queryData(today + timedelta(days=-30))
printJSString(data, 'logSummary30')

#所有
data = queryData(None)
printJSString(data, 'logSummaryAll')





conn.close()
