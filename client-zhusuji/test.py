import requests
url_lh = "http://172.19.31.247:2232/getkanbandata"
res_lh = requests.get(url_lh)
data_lh = res_lh.json()
url_sy = "http://172.19.31.246:2323/getkanbandata"
res_sy = requests.get(url_sy)
data_sy = res_sy.json()
name = ("A01_86T","A02_110T","A03_110T","A04_120T","A05_120T","A06_160T","A07_200T",
        "A08_230T","A09_470T","A10_408T","A11_360T","A12_360T","A13_470T","A14_200T","A15_380T",
        "A20_250T","B16_800T","B17_530T","B18_700T","B19_700T","UV_line","ultrasonic_1","ultrasonic_2",
        "welding_machine","nut_machine_1","nut_machine_2","nut_machine_3","line_1","line_2","printing_machine_1",
        "printing_machine_2","printing_machine_3","nut_machine_4","Assembly_line"
        )

for i in range(len(data_lh)):
    data_lh[i]['设备'] = name[i]
for body in data_lh:
    print(body)