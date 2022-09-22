from main.Configuration_files.paths import default_exp_test_dir, add_to_path

import pandas as pd
import os
import time

working_dir=default_exp_test_dir
device_col = "Device"
channel_col = "Channel"
time_str="Time"

user_vs_operation_times_diff=0
send_delay=0

def get_device_channel_tupple(input_file):
    splitted = input_file.split(".")[0].split("_")
    return splitted[0], splitted[1]

def get_diff_arr(arr):
    diff_lst = []
    for i in range(1, len(times_arr)):
        diff_lst.append(times_arr[i] - times_arr[i - 1])
    print(set(diff_lst))

if __name__ == '__main__':
    start_experiment_time=time.time_ns()
    print(working_dir)
    for input_file in os.listdir(working_dir):
        print("current file: {}".format(input_file))
        df = pd.read_csv(add_to_path(working_dir, input_file), keep_default_na=False)
        device, channel = get_device_channel_tupple(input_file)
        print("Current device: {} channel: {}".format(device, channel))
        added_to_op_time = start_experiment_time + user_vs_operation_times_diff + send_delay

        times_arr=df[time_str].to_numpy().astype(int)
        get_diff_arr(times_arr)

        added_time_arr=[]
        for i in times_arr:
            added_time_arr.append(i+added_to_op_time)
        get_diff_arr(added_time_arr)
        get_diff_arr(added_time_arr)
        #times_arr.count(list(times_arr))

