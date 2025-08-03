from data_utils import *
import math
import matplotlib.pyplot as plt

# sensor = read_sensor_file("raw_data/1x_move_yaw_pitch.csv")
# sensor = read_sensor_file("raw_data/1x_roll.csv")
# sensor = read_sensor_file("raw_data/2x_roll.csv")
# sensor = read_sensor_file("raw_data/2x_yaw_pitch.csv")
# sensor_still = read_sensor_file("raw_data/stationary_tilt.csv")
sensor_still = read_sensor_file("raw_data/stationary_3.csv")

sensor = read_sensor_file("raw_data/roll_pitch.csv")
lsm_calib = xyz()
mpu_calib = xyz()
for index,data in enumerate(sensor_still, start=1):
    lsm_calib.x = cumulative_average(data.lsm.gyro.x, lsm_calib.x, index)
    lsm_calib.y = cumulative_average(data.lsm.gyro.y, lsm_calib.y, index)
    lsm_calib.z = cumulative_average(data.lsm.gyro.z, lsm_calib.z, index)

    mpu_calib.x = cumulative_average(data.mpu.gyro.x, mpu_calib.x, index)
    mpu_calib.y = cumulative_average(data.mpu.gyro.y, mpu_calib.y, index)
    mpu_calib.z = cumulative_average(data.mpu.gyro.z, mpu_calib.z, index)

for index,data in enumerate(sensor):
    scale = 1
    sensor[index].lsm.gyro.x -= lsm_calib.x * scale
    sensor[index].lsm.gyro.y -= lsm_calib.y * scale
    sensor[index].lsm.gyro.z -= lsm_calib.z * scale

    sensor[index].mpu.gyro.x -= mpu_calib.x * scale
    sensor[index].mpu.gyro.y -= mpu_calib.y * scale
    sensor[index].mpu.gyro.z -= mpu_calib.z * scale

lsm_sum_of_dev_g = xyz()
mpu_sum_of_dev_g = xyz()
for index,data in enumerate(sensor_still):
    lsm_sum_of_dev_g.x += (data.lsm.gyro.x - lsm_calib.x) ** 2
    lsm_sum_of_dev_g.y += (data.lsm.gyro.y - lsm_calib.y) ** 2
    lsm_sum_of_dev_g.z += (data.lsm.gyro.z - lsm_calib.z) ** 2

    mpu_sum_of_dev_g.x += (data.mpu.gyro.x - mpu_calib.x) ** 2
    mpu_sum_of_dev_g.y += (data.mpu.gyro.y - mpu_calib.y) ** 2
    mpu_sum_of_dev_g.z += (data.mpu.gyro.z - mpu_calib.z) ** 2

std_dev_lsm_gyro = xyz()
std_dev_lsm_gyro.x = math.sqrt(lsm_sum_of_dev_g.x / (len(sensor_still) - 1))
std_dev_lsm_gyro.y = math.sqrt(lsm_sum_of_dev_g.y / (len(sensor_still) - 1))
std_dev_lsm_gyro.z = math.sqrt(lsm_sum_of_dev_g.z / (len(sensor_still) - 1))

std_dev_mpu_gyro = xyz()
std_dev_mpu_gyro.x = math.sqrt(mpu_sum_of_dev_g.x / (len(sensor_still) - 1))
std_dev_mpu_gyro.y = math.sqrt(mpu_sum_of_dev_g.y / (len(sensor_still) - 1))
std_dev_mpu_gyro.z = math.sqrt(mpu_sum_of_dev_g.z / (len(sensor_still) - 1))

print("lsm_x:",std_dev_lsm_gyro.x)
print("lsm_y:",std_dev_lsm_gyro.y)
print("lsm_z:",std_dev_lsm_gyro.z)

print("mpu_x:",std_dev_mpu_gyro.x)
print("mpu_y:",std_dev_mpu_gyro.y)
print("mpu_z:",std_dev_mpu_gyro.z)
ori_lsm = []
ori_mpu = []

for index, data in enumerate(sensor):
    time_dif = 0.01
    last_z_lsm = 0
    last_z_mpu = 0
    if(index != 0):
        last_z_lsm = ori_lsm[-1].z
        last_z_mpu = ori_mpu[-1].z
        
    ori = accel_to_xy(data.lsm.accel)
    ori.time = data.time
    ori.z = last_z_lsm
    gyro = gyro_local_to_global(data.lsm.gyro, deg_to_rad(ori))
    ori.z = last_z_lsm + gyro.z * time_dif
    ori_lsm.append(ori)

    ori = accel_to_xy(data.mpu.accel)
    ori.time = data.time
    ori.z = last_z_mpu
    gyro = gyro_local_to_global(data.mpu.gyro, deg_to_rad(ori))
    ori.z = last_z_mpu + gyro.z * time_dif
    ori_mpu.append(ori)

times = []
x_lsm = []
y_lsm = []
z_lsm = []
x_mpu = []
y_mpu = []
z_mpu = []

for ori in ori_lsm:
    times.append(ori.time)
    x_lsm.append(ori.x)
    y_lsm.append(ori.y)
    z_lsm.append(ori.z)

for ori in ori_mpu:  
    x_mpu.append(ori.x)
    y_mpu.append(ori.y)
    z_mpu.append(ori.z)

plt.figure()
plt.plot(times, x_lsm, color = "r")
plt.plot(times, y_lsm, color = "g")
plt.plot(times, z_lsm, color = "b")

plt.figure()
plt.plot(times, x_mpu, color = "r")
plt.plot(times, y_mpu, color = "g")
plt.plot(times, z_mpu, color = "b")

plt.show()