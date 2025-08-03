import serial
import csv

ser = serial.Serial("COM11", timeout=1)

def append_csv(data):
    with open('raw_data/data.csv','a', newline='') as fd:
        writer = csv.writer(fd)
        writer.writerow(data)
        # fd.write(str(data))

while(True):
    data = ser.readline()

    if(len(data) == 0): continue

    res_str = data.decode('utf-8')[:-1]
    res_list = res_str.split(',')
    # res_list[-1] = res_list[-1][:-1]
    # print(res)
    append_csv(res_list)
    print(res_list[0])