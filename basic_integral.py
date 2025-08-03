from data_utils import *
import math
import matplotlib.pyplot as plt

# sensor = read_sensor_file("raw_data/1x_move_yaw_pitch.csv")
sensor = read_sensor_file("raw_data/1x_roll.csv")
# sensor = read_sensor_file("raw_data/2x_roll.csv")
# sensor = read_sensor_file("raw_data/2x_yaw_pitch.csv")
# sensor_still = read_sensor_file("raw_data/stationary_tilt.csv")
sensor_still = read_sensor_file("raw_data/stationary.csv")

def cumulative_average(new_data, old_average, new_data_index):
    n = new_data_index # n starts from 1
    new_data = old_average * (n-1)/n + new_data / n

    return new_data

lsm_calib = xyz()
for index,data in enumerate(sensor_still, start=1):
    lsm_calib.x = cumulative_average(data.lsm.gyro.x, lsm_calib.x, index)
    lsm_calib.y = cumulative_average(data.lsm.gyro.y, lsm_calib.y, index)
    lsm_calib.z = cumulative_average(data.lsm.gyro.z, lsm_calib.z, index)

for index,data in enumerate(sensor):
    scale = 1
    sensor[index].lsm.gyro.x -= lsm_calib.x * scale
    sensor[index].lsm.gyro.y -= lsm_calib.y * scale
    sensor[index].lsm.gyro.z -= lsm_calib.z * scale


ori_lsm = []
ori_mpu = []

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

    ori.x = math.atan2(accel.x, accel.z) * 57.2958
    val = math.sqrt(accel.x**2 + accel.z**2)
    ori.y = math.atan2(accel.y, val) * 57.2958

    return ori

def gyro_local_to_global(gyro: xyz, ori_rad: xyz):
    gy_g = xyz()

    sin_x = math.sin(ori_rad.x)
    sin_y = math.sin(ori_rad.y)
    cos_x = math.cos(ori_rad.x)
    cos_y = math.cos(ori_rad.y)

    gy_g.x = gyro.x * cos_y + gyro.y * (sin_x * sin_y) + gyro.z * cos_x * sin_y
    gy_g.y = gyro.y * cos_x + gyro.z * (-sin_x)
    gy_g.z = gyro.x * (-sin_y) + gyro.y * (sin_x * cos_y) + gyro.z * cos_x * cos_y

    return gy_g

for index, data in enumerate(sensor):
    # print(data.lsm.accel.x)
    # break
    time_dif = 0.01
    last_z_lsm = 0
    last_z_mpu = 0
    if(index != 0):
        last_z_lsm = ori_lsm[-1].z
        last_z_mpu = ori_mpu[-1].z
        
    ori = accel_to_xy(data.lsm.accel)
    ori.time = data.time

    gyro = gyro_local_to_global(data.lsm.gyro, deg_to_rad(ori))
    ori.z = last_z_lsm + gyro.z * time_dif
    # print(ori.z)
    ori_lsm.append(ori)

    ori = accel_to_xy(data.mpu.accel)
    ori.time = data.time
    ori_mpu.append(ori)

times = []
x = []
y = []
z = []

for ori in ori_lsm:
    times.append(ori.time)
    x.append(ori.x)
    y.append(ori.y)
    z.append(ori.z)

plt.plot(times, x, color = "r")
plt.plot(times, y, color = "g")
plt.plot(times, z, color = "b")
plt.show()