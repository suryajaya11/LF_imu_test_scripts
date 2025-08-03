from data_utils import *

sensor = read_sensor_file("raw_data/1x_move_yaw_pitch.csv")
ori = orientation([0,0,0,0])

for data in sensor:
    print(data.lsm_accel_x)