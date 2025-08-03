import csv
import matplotlib.pyplot as plt
import math

class xyz():
    def __init__(self):
        self.time = 0
        self.x = float(0)
        self.y = float(0)
        self.z = float(0)

class sensor_data():
    def __init__(self):
        self.accel = xyz()
        self.gyro = xyz()

class sensor_file_data():
    def __init__(self, data):
        self.time = int(data[0])

        self.lsm = sensor_data()
        self.mpu = sensor_data()
        
        self.lsm.accel.x = float(data[1]) * 0.000061
        self.lsm.accel.y = float(data[2]) * 0.000061
        self.lsm.accel.z = float(data[3]) * 0.000061
        self.lsm.gyro.x = float(data[4]) * 0.00875
        self.lsm.gyro.y = float(data[5]) * 0.00875
        self.lsm.gyro.z = float(data[6]) * 0.00875
        
        self.mpu.accel.x = float(data[7]) * 0.000061036
        self.mpu.accel.y = float(data[8]) * 0.000061036
        self.mpu.accel.z = float(data[9]) * 0.000061036
        self.mpu.gyro.x = float(data[10]) * 0.0076295
        self.mpu.gyro.y = float(data[11]) * 0.0076295
        self.mpu.gyro.z = float(data[12]) * 0.0076295

    # def __str__(self):
    #     return f"time:{self.time}ms, lsm accel({self.lsm_accel_x},{self.lsm_accel_y},{self.lsm_accel_z}),lsm gyro({self.lsm_gyro_x},{self.lsm_gyro_y},{self.lsm_gyro_z})"

class orientation():
    def __init__(self, data = [0,0,0,0]):
        self.time = int(data[0])
        self.x = float(data[1])
        self.y = float(data[2])
        self.z = float(data[3])

def read_sensor_file(filename):
    datas = []
    with open(filename,'r') as fd:
        rd = csv.reader(fd)
        for row in rd:
            datas.append(sensor_file_data(row))
            
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
        
def cumulative_average(new_data, old_average, new_data_index):
    n = new_data_index # n starts from 1
    new_data = old_average * (n-1)/n + new_data / n

    return new_data


def rad_to_deg(ori: xyz):
    ori_rad = xyz()
    ori_rad.x = ori.x * 180.0 * (1/math.pi)
    ori_rad.y = ori.y * 180.0 * (1/math.pi)
    ori_rad.z = ori.z * 180.0 * (1/math.pi)

    return ori_rad

def deg_to_rad(ori: xyz):
    ori_deg = xyz()
    ori_deg.x = ori.x * math.pi * (1/180.0)
    ori_deg.y = ori.y * math.pi * (1/180.0)
    ori_deg.z = ori.z * math.pi * (1/180.0)

    return ori_deg


def accel_to_xy(accel: xyz):
    ori = orientation()

    ori.x = math.atan2(accel.y, accel.z) * 57.2958
    val = math.sqrt(accel.y**2 + accel.z**2)
    ori.y = math.atan2(-accel.x, val) * 57.2958

    return ori

def gyro_local_to_global(gyro: xyz, ori_rad: xyz):
    gy_g = xyz()

    sin_x = math.sin(ori_rad.x)
    sin_y = math.sin(ori_rad.y)
    cos_x = math.cos(ori_rad.x)
    cos_y = math.cos(ori_rad.y)

    gy_g.x = gyro.x * cos_y + gyro.y * sin_x * sin_y + gyro.z * cos_x * sin_y
    gy_g.y = gyro.y * cos_x + gyro.z * (-sin_x)
    gy_g.z = gyro.x * (-sin_y) + gyro.y * sin_x * cos_y + gyro.z * cos_x * cos_y

    return gy_g