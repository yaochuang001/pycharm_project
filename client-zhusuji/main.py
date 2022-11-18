import string
import sys
import os
import time
import cgitb
import datetime
import requests
import hashlib
# 表格导入
from MainWindow import *
#导入qt相关包
from PyQt5.QtWidgets import QMainWindow, QApplication,QMdiArea, QMdiSubWindow, QTableWidgetItem
from PyQt5.QtCore import QTimer, Qt, QDateTime,QThread,pyqtSignal
from PyQt5.QtGui import QPixmap
cgitb.enable(format='text')
Name = ("A01_86T","A02_110T","A03_110T","A04_120T","A05_120T","A06_160T","A07_200T",
        "A08_230T","A09_470T","A10_408T","A11_360T","A12_360T","A13_470T","A14_200T","A15_380T",
        "A20_250T","B16_800T","B17_530T","B18_700T","B19_700T","UV_line","ultrasonic_1","ultrasonic_2",
        "welding_machine","nut_machine_1","nut_machine_2","nut_machine_3","line_1","line_2","printing_machine_1",
        "printing_machine_2","printing_machine_3","nut_machine_4","Assembly_line"
        )
class MyMainWindow(QMainWindow,Ui_MainWindow):

    def __init__(self, parent=None):
        super(MyMainWindow, self).__init__(parent)
        self.setupUi(self)
        self.setWindowTitle("系统设置软件")
        # 创建线程实例
        self.thread = Data_thr()
        self.thread_get = Get_thr()
        #初始化哈希对象
        self.hash_data = hashlib.sha256()
        #self.textBrowser.setLineWrapMode(QtWidgets.QTextBrowser.NoWrap)

        #初始化定时器
        self.time = QTimer(self)
        #线程发射函数
        self.thread.sinOut.connect(self.post_send)
        self.thread_get.sinOut.connect(self.http_get)
        #创建定时器方法
        self.time.timeout.connect(self.begin_sys)

        # 创建工具栏时间
        self.action_start.triggered.connect(self.sys_start)
        self.action_stop.triggered.connect(self.sys_stop)
        self.action_get.triggered.connect(self.date_get)
        self.action_send.triggered.connect(self.date_send)
        self.action_data.triggered.connect(self.date_set)
        self.action_signature.triggered.connect(self.signature)

    def http_get(self,data_lh,data_sy):
        if data_lh != '' and data_sy !='':
            self.data_lh = eval(data_lh)
            self.data_sy = eval(data_sy)
            self.textBrowser_2.append(time.strftime('%Y--%m--%d  %H:%M:%S', time.localtime(time.time())))
            self.textBrowser_2.append('获取龙华数据：%s' % (data_lh,))
            self.textBrowser_2.append('获取石岩数据：%s' % (data_sy,))
            for i in range(len(self.data_lh)):
                self.data_lh[i]['设备'] = Name[i]
            #获取参数
            self.thread.get_arc(self.url_sed,self.data_lh,self.data_sy,self.timestamp)
            #开启发送线程
            self.thread.start()
        else:
            self.textBrowser_2.append(time.strftime('%Y--%m--%d  %H:%M:%S', time.localtime(time.time())))
            self.textBrowser_2.append('数据获取失败')
    def post_send(self,r,data):
        self.textBrowser_3.append(time.strftime('%Y--%m--%d  %H:%M:%S', time.localtime(time.time())))
        self.textBrowser_3.append(r)
        self.textBrowser.append(time.strftime('%Y--%m--%d  %H:%M:%S', time.localtime(time.time())))
        self.textBrowser.append(data)

    def begin_sys(self):
        print('开启数据采集了')
        self.date_get()

    def sys_start(self):
        print('系统启动了')
        self.signature()
        self.time.start(3000)

    def sys_stop(self):
        print('系统停止了')
        self.time.stop()

    def date_get(self):
        self.textBrowser_4.append(time.strftime('%Y--%m--%d  %H:%M:%S', time.localtime(time.time())))
        self.textBrowser_4.append('开启数据采集')
        self.thread_get.start()




    def date_send(self):
        body = {
            "DeviceId": "SPI001",
            "CollectionTime": int(self.timestamp),
            "PointDataItems": [
                {
                    "PointName": "line",
                    "PointValue": "SMT01"
                },
                {
                    "PointName": "padid",
                    "PointValue": "7"
                }
            ]
        }
        #self.textBrowser.append(self.url_sed)
        #print(r.text)
        print('发送数据完成')

    def date_set(self):
        print('打开设置页面')

    def signature(self):
        self.textBrowser_4.append(time.strftime('%Y--%m--%d  %H:%M:%S', time.localtime(time.time())))
        self.textBrowser_4.append('生成签名数据')
        t = time.time()
        url_L = "https://skydf-app.skyallhere.com/data-collection-api/DeviceDataPush"
        nowTime = lambda: int(round(t * 1000))
        Token = "fdsgfafgr43nkajf3krsdawerfnjc"
        self.timestamp = str(nowTime())
        Action = 'DeviceDataPush'
        data = "action=" + Action + '&' +'token=' + Token + '&' + 'timestamp=' + self.timestamp
        self.hash_data.update(data.encode())
        self.signature_data = self.hash_data.hexdigest()
        #self.textBrowser_4.append(data)
        #self.textBrowser_4.append(self.signature_data)
        self.url_sed = url_L + '?signature=' + self.signature_data + '&timestamp=' + self.timestamp
        self.textBrowser_4.append(self.url_sed)


# 创建一个线程类-数据发送
class Data_thr(QThread):
    sinOut = pyqtSignal(str,str)

    def __init__(self,):
        super(Data_thr, self).__init__()

    def get_arc(self,url,body_lh,body_sy,timestamp):
        self.url = url
        self.body_lh = body_lh
        self.body_sy = body_sy
        self.timestamp = timestamp

    def run(self):
        for body_ly in self.body_lh:
            try:
                body = {
                    "DeviceId": body_ly['设备'],
                    "CollectionTime": int(self.timestamp),
                    "PointDataItems": [
                        {
                            "PointName": 'ser_number',
                            "PointValue": body_ly['序列号']
                        },
                        {
                            "PointName": 'dev_status',
                            "PointValue": body_ly['设备状态']
                        },
                        {
                            "PointName": "SAP_number",
                            "PointValue": body_ly['SAP工单号']
                        },
                        {
                            "PointName": "SKY_number",
                            "PointValue": body_ly['创维编码']
                        },
                        {
                            "PointName": "pro_name",
                            "PointValue": body_ly['产品名称']
                        },
                        {
                            "PointName": "work_order_number",
                            "PointValue": body_ly['工单数']
                        },
                        {
                            "PointName": "outp_total",
                            "PointValue": body_ly['总完工数']
                        },
                        {
                            "PointName": "outp_meter",
                            "PointValue": body_ly['当前周期']
                        },
                        {
                            "PointName": "take_method",
                            "PointValue": body_ly['取件方式']
                        },
                    ]
                }
                r = requests.post(url=self.url, json=body, timeout=0.2)
                # 发出信号
                self.sinOut.emit(r.text,str(body))
            except Exception as e:
                # 发出信号
                print('发送失败')
                self.sinOut.emit(str(e),'')
        for body_sy in self.body_sy:
            try:
                body2 = {
                    "DeviceId": body_sy['机台号'],
                    "CollectionTime": int(self.timestamp),
                    "PointDataItems": [
                        {
                            "PointName": 'WkName',
                            "PointValue": body_sy['WkName']
                        },
                        {
                            "PointName": 'today_worktime',
                            "PointValue": body_sy['今日开机']
                        },
                        {
                            "PointName": "status",
                            "PointValue": body_sy['状态']
                        }
                    ]
                }
                r = requests.post(url=self.url, json=body2, timeout=0.2)
                # 发出信号
                self.sinOut.emit(r.text,str(body2))
            except Exception as e:
                # 发出信号
                print('发送失败')
                self.sinOut.emit(str(e),'')


#创建一个线程类-数据接收
class Get_thr(QThread):
    sinOut = pyqtSignal(str,str)

    def __init__(self,):
        super(Get_thr, self).__init__()

    def run(self):
        try:
            url_lh = "http://172.19.31.247:2232/getkanbandata"
            res_lh = requests.get(url_lh)
            data_lh = res_lh.json()
            url_sy = "http://172.19.31.246:2323/getkanbandata"
            res_sy = requests.get(url_sy)
            data_sy = res_sy.json()
            # 发出信号
            self.sinOut.emit(str(data_lh),str(data_sy))
        except Exception as e:
            # 发出信号
            str1 = ''
            str2 = ''
            self.sinOut.emit(str1,str2)














if __name__ == '__main__':
    app = QApplication(sys.argv)

    w = MyMainWindow()
    w.show()
    sys.exit(app.exec_())