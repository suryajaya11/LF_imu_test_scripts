import csv
import matplotlib.pyplot as plt

class sensor_data():
    def __init__(self, data):
        self.time = int(data[0])
        self.lsm_accel_x = float(data[1]) * 0.000061
        self.lsm_accel_y = float(data[2]) * 0.000061
        self.lsm_accel_z = float(data[3]) * 0.000061
        self.lsm_gyro_x = float(data[4]) * 0.00875
        self.lsm_gyro_y = float(data[5]) * 0.00875
        self.lsm_gyro_z = float(data[6]) * 0.00875
        
        self.mpu_accel_x = float(data[7]) * 0.000061036
        self.mpu_accel_y = float(data[8]) * 0.000061036
        self.mpu_accel_z = float(data[9]) * 0.000061036
        self.mpu_gyro_x = float(data[10]) * 0.0076295
        self.mpu_gyro_y = float(data[11]) * 0.0076295
        self.mpu_gyro_z = float(data[12]) * 0.0076295

    # def __str__(self):
    #     return f"time:{self.time}ms, lsm accel({self.lsm_accel_x},{self.lsm_accel_y},{self.lsm_accel_z}),lsm gyro({self.lsm_gyro_x},{self.lsm_gyro_y},{self.lsm_gyro_z})"

class orientation():
    def __init__(self, data):
        self.time = int(data[0])
        self.x = float(data[1])
        self.y = float(data[2])
        self.y = float(data[3])

def read_sensor_file(filename):
    datas = []
    with open(filename,'r') as fd:
        rd = csv.reader(fd)
        for row in rd:
            datas.append(sensor_data(row))
            
    return datas

def read_result_file(filename):
    datas = []
    with open(filename,'r') as fd:
        rd = csv.reader(fd)
        for row in rd:
            datas.append(orientation(row))
            
    return datas

def append_result_file(filename: str, orientation: orientation):
    datas = []
    datas.append(str(orientation.time))
    datas.append(str(orientation.x))
    datas.append(str(orientation.y))
    datas.append(str(orientation.z))
    
    with open(filename,'a', newline='') as fd:
        writer = csv.writer(fd)
        writer.writerow(datas)