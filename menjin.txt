#导入pymysql
import numpy as np
import pymysql
import requests
import schedule
from datetime import datetime, timedelta, time


##发送短信
def send_dx(sname,mobil):
    url = 'https://gateway.nciae.edu.cn/mp_message_pocket_web-mp-restful-message-send/ProxyService/message_pocket_web-mp-restful-message-sendProxyService?'
    params = {
        "subject": "未归学生反馈",
        "content": f"您的学生{sname}昨晚未返校，请您尽快核实。",
        "tagId": 9007,
        "sendType": 4,
        "wxSendType": "text",
        "receivers": [
            {
                "userId": "ampadmin",
                "mobile": mobil
            }
        ],
        "schoolCode": "11629",
        "sign": "30c59158e556dad6931b4ab6622f0a53"
    }
    header = {
        "appId": "915291970667343872",
        "accessToken": "f9ccfbb02c4bef5129df4d62e82e2e19",
    }
    r = requests.post(url, headers=header, json=params)
    print(r.text)


#与数据库建立连接
# from men.aaa import client

conn = pymysql.connect(user="root", password="123456j", host="10.176.246.189", database="test", port=3306,charset="utf8")
 #建立游标
cursor = conn.cursor()


##查询未归学生
sql = "SELECT sname FROM menjin"
# sql="SELECT fphone FROM fudaoy WHERE fname IN ( SELECT fname FROM banji WHERE sno IN ( SELECT sno FROM menjin WHERE ss=1))"
#执行
cursor.execute(sql)
#执行的结果存放到data_list
data_list = cursor.fetchall()
# print((data_list))

lst1=[]
for i in data_list:
    # print(i[0])
    a=i[0]
    lst1.append(a)
    # print(a)
# print(lst1)

lst2=[]
for l1 in lst1:
    if l1 not in lst2:
        lst2.append(l1)
print('所有进出校门学生姓名：',lst2)
# lst1=sorted(list(set(data_list)))
# # print(list(lst1)[0][0])

lst3=[]
for i in lst2:
    # print(i)
    name=i
    sql1="SELECT * FROM menjin WHERE sname=%s"
    cursor.execute(sql1,i)
    # cursor.execute(sql1)
    # 执行的结果存放到data_list
    a=cursor.fetchall()
    b=list(a)
    # print(b)
    # print(len(b))
    s=list(b[len(b)-1])
    # print(s)
    if s[len(s)-1]==1:
        lst3.append(i)
print('所有未归学生：',lst3)

##查找未归学生所在班级对应的辅导员的电话
##查询未归学生所在班级
sql2="SELECT * FROM menjin WHERE sname=%s"
for i in lst3:
    sql2 = "SELECT sno FROM menjin WHERE sname=%s"
    cursor.execute(sql2, i)
    a = list(cursor.fetchall())
    s=a[0]
    # print('{name}的班级是：{sno}',i,a)
    print('未归学生姓名：',i)
    print('所在班级：',s[0])
    # print(i,s[0])

    ##查询辅导员姓名
    sql3= "SELECT fname FROM banji WHERE sno=%s"
    cursor.execute(sql3, s[0])
    b=list(cursor.fetchall())
    s=b[0][0]
    print('辅导员姓名：',s)

    ##查询辅导员电话
    sql4="SELECT fphone FROM fudaoy WHERE fname=%s"
    cursor.execute(sql4, s)
    c=list(cursor.fetchall())
    d=c[0][0]
    print('辅导员电话',d)

    ##发送短信
    send_dx(i, d)


#关闭游标
cursor.close()
#关闭连接
conn.close()


##定时任务
def job():
    print('working...')

    # ##发送短信
    # params = {}
    # # number:接收者的号码
    # # templateid：短信模板ID，登录用户中心，在"短信管理->短信模板"中创建，并查看
    # params['number'] = 'd'
    # params['templateId'] = '11180'
    # params['templateParams'] = ['s[0]', 'i']
    #
    # print(client.send(params))

# schedule.every().hour.do(job)  ##每小时执行一次
# schedule.every().day.at("10:30").do(job)  ##每天定点执行
# schedule.every().monday.do(job)  ##每周执行一次
# schedule.every().wednesday.at("13:15").do(job)  ##每周三13：15执行一次任务

# while True:
#     schedule.run_pending()

