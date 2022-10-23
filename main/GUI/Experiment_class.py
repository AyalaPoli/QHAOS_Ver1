import os
import time
import traceback
import sched
import threading
import pandas as pd
from main.GUI.GUI_params import *
from main.Configuration_files.session_configuration import *
from main.GUI.Function_Setting import *
from distutils.dir_util import copy_tree
from main.Configuration_files.paths import working_dir


#user_time_vs_operation_time_diff
from main.Session.Command_Packet import *

class Experiment():

    #send_scheduler = sched.scheduler(timefunc=time.monotonic_ns, delayfunc=time.sleep)

    user_vs_operation_times_diff = user_time_vs_operation_time_diff
    pre_operation_send_time_diff =pre_operation_send_time_diff

    on_val=0
    off_val=1

    trigger_cond_op_code=0
    timestamp_cond_op_code=1
    op_condition=timestamp_cond_op_code

    subset_rows_num=50 #to determine after measurement, This variable determines the regulary checking of queue during experiment

    sorted_df_to_file_path="sorted_df.csv"

    exp_runner_err_title="Error in experiment runner"
    exp_runner_err_msg=exp_runner_err_title+":\n\n{}"

    error_cycle_time_title="Exceeded cycle time"
    error_cycle_time_msg="Exceeded cycle time: time to wait to the end of cycle {} is negative: {}"

    device_col = "Device"
    channel_col = "Channel"

    stop_exp_flag=False

    default_exp_started_title="Default operations sequence has been stopped"
    default_exp_started_txt="Default operations sequence has been started:\n{}".format(default_dir_path)

    default_exp_stopped_title="Default operations sequence has been stopped"
    default_exp_stopped_txt="Default operations sequence has been stopped:\n{}".format(default_dir_path)

    exp_started_title="Experiment started"
    exp_started_msg="The following experiment has been started: \n{}\niteration num: {}\ncycle time: {}"

    sent_op_file="send_op_files.txt"
    f = open(sent_op_file, "w")

    iter_count = 1
    rem = 0

    ns_to_seb_divider=1000000000
    limit_iter = 1000000000

    def __init__(self, app, input_dir_path, iteration_num, cycle_time):
        self.app=app
        self.input_dir_path=input_dir_path
        self.iteration_num = iteration_num
        self.cycle_time=cycle_time
        self.update_last_exp_args()

    def is_default_experiment(self):
        return True if self.input_dir_path==default_dir_path else False

    def update_last_exp_args(self):
        self.app.client.last_dir_path=self.input_dir_path
        self.app.client.last_iteration_num=self.iteration_num
        self.app.client.last_cycle_time=self.cycle_time


    def start_experiment_runner(self):

        try:
            #self.create_experiment_df() moved to upload
            self.exp_df=pd.read_csv(sorted_merged_working_path)
            self.no_iteration_limit = True if self.iteration_num == str_value_iterations_dict[infinite_iteration_txt] else False
            self.start_experiment_time = self.get_current_time_nano_sec()
            self.cycles_intervals=0
            iter_num=self.iteration_num
            while (iter_num > 0 or self.no_iteration_limit) and not self.stop_exp_flag:
                #TODO assert start experienment: current time is cycles time*number of cycles
                if self.iter_count>self.limit_iter:
                    self.iter_count=1
                    self.rem+=1
                if self.app.is_window_open(self.app.run_exp_win_name):

                    self.app.get_window_obj(self.app.run_exp_win_name).update_running_iteration_num_label(self.iter_count, self.rem)
                self.experiment_df_for_change = self.exp_df.copy(deep=True)
                if not self.no_iteration_limit:
                    iter_num -= 1

                while not self.experiment_df_for_change.empty and not self.stop_exp_flag:
                    curr_subset_df_by_rows=self.get_exp_df_subset_by_rows_num()
                    curr_subset_df_by_rows.apply(lambda row: self.send_row_packet(row), axis=1)

                self.cycles_intervals+=self.cycle_time

                self.wait_to_the_end_of_cycle_time()
                self.start_experiment_time += self.cycle_time
                self.iter_count+=1

            if not self.stop_exp_flag: #If we done the iteration without outer stop
                self.app.client.stop_exp_func()


        except Exception as e:
            print(traceback.format_exc())
            self.app.show_err_msg(self.exp_runner_err_title, self.exp_runner_err_msg.format(e))
            self.app.insert_stop_experiment_command_to_queue()



    def wait_to_the_end_of_cycle_time(self):
        wait_time = (self.start_experiment_time + self.user_vs_operation_times_diff - self.pre_operation_send_time_diff) - self.get_current_time_nano_sec()
        curr_time=self.get_current_time_nano_sec()
        relative_curr_time=curr_time - self.start_experiment_time + self.user_vs_operation_times_diff - self.pre_operation_send_time_diff

        if relative_curr_time < (self.cycle_time + self.user_vs_operation_times_diff):
            if((self.cycle_time-relative_curr_time) > 0):
                wait_time_in_sec=float((self.cycle_time-relative_curr_time)/self.ns_to_seb_divider)
                self.app.client.execute_command_from_queue()
                time.sleep(wait_time_in_sec)
        else:
            self.app.show_err_msg(self.error_cycle_time_title, self.error_cycle_time_msg.format(self.iter_count+1, wait_time))
            self.app.insert_stop_experiment_command_to_queue()

    def get_exp_df_subset_by_rows_num(self):
        req_rows_num=min(self.subset_rows_num, len(self.experiment_df_for_change.index))
        exp_df_subset_by_rows_num = self.experiment_df_for_change.iloc[:req_rows_num]
        self.experiment_df_for_change.drop(exp_df_subset_by_rows_num.index, inplace=True)
        return exp_df_subset_by_rows_num


    def send_row_packet(self, row):

        #step_time = int(row[time_str]) + self.cycles_intervals + self.user_vs_operation_times_diff - self.pre_operation_send_time_diff
        #step_time = int(row[time_str]) + self.user_vs_operation_times_diff - self.pre_operation_send_time_diff
        step_time = int(row[time_str])
        #step_time = int(row[time_str]) + self.user_vs_operation_times_diff
        curr_time = self.get_current_time_nano_sec()
        relative_curr_time = curr_time - self.start_experiment_time

        # if (row[time_str] == 0):
        #     print(step_time)
        #     print(self.cycles_intervals)
        #     print(curr_time)
        #     print(relative_curr_time)
        #     print(row[time_str])


        if relative_curr_time < step_time:
            sleep_time=float((step_time - relative_curr_time)/self.ns_to_seb_divider)
            time.sleep(sleep_time)


        if row[self.device_col] == AOM_str:
            self.set_AOM_func_from_experiment(row, (step_time + self.user_vs_operation_times_diff + self.cycles_intervals))
        elif row[self.device_col] == GPIO_str:
            self.set_GPIO_func_from_experiment(row, (step_time + self.user_vs_operation_times_diff + self.cycles_intervals))


        #added_to_op_time = relative_curr_time + self.user_vs_operation_times_diff - self.pre_operation_send_time_diff

        #self.f.write(str(step_time)+"\n")
        #self.f.write(str(float(step_time))+"\n")

        # send_func=self.set_AOM_func_from_experiment if row[self.device_col]==AOM_str else self.set_GPIO_func_from_experiment
        # delta=(curr_time - added_to_op_time) - step_time
        # delay=delta if delta >= 0 else 0
        # self.send_scheduler.enter(delay, 1, send_func, argument=(row, step_time))
        #delta=step_time-(curr_time - added_to_op_time)
        #if delta<0:
        #    print("delta {}".format(delta))
        #    time.sleep(-delta/self.ns_to_seb_divider)
        #if step_time <= curr_time - added_to_op_time:


    def set_AOM_func_from_experiment(self, row, step_time):
        aom_exp_op_code=set_aom_exp_op_code
        opreration_condition=self.op_condition
        trigger_cond=-1 #to implement when trigger channel inserted
        trigger_channel=0 if opreration_condition==self.timestamp_cond_op_code else trigger_cond

        op_time=step_time
        num_channels_to_config=1
        channel_index = int(row[self.channel_col])
        params_lst = [opreration_condition, trigger_channel, op_time, num_channels_to_config, channel_index]


        amplitude=float(row[amplitude_str]) if pd.notnull(row[amplitude_str]) else None
        frequency=float(row[frequency_str]) if pd.notnull(row[frequency_str]) else None
        if frequency and pd.notnull(amplitude):
            params_config_lst=[two_params_to_config, amplitude, frequency]
            curr_format=set_aom_exp_format_two_params
        else:

            params_config_lst = [only_amp_to_config, amplitude] if pd.notnull(amplitude) else [only_freq_to_config, frequency]
            curr_format=set_aom_exp_format_one_params
        params_lst.extend(params_config_lst)
        self.app.client.send_to_control(aom_exp_op_code, curr_format, params_lst)

    def set_GPIO_func_from_experiment(self, row, step_time):

        gpio_exp_op_code=set_gpio_exp_op_code
        opreration_condition=self.op_condition
        trigger_channel=-1 #to implement when trigger channel inserted
        trigger_condition=0 if opreration_condition==self.timestamp_cond_op_code else trigger_channel

        op_time=step_time
        channel_index = int(row[self.channel_col])
        value=int(row[activate_str])
        params_lst=[opreration_condition, trigger_condition, op_time, channel_index, value]
        self.app.client.send_to_control(gpio_exp_op_code, set_gpio_exp_format, params_lst)

    def return_to_initial_state(self):
        if hasattr(self, "initial_state_df"):
            self.start_experiment_time=self.get_current_time_nano_sec()
            self.initial_state_df.apply(lambda row: self.send_row_packet(row), axis=1)


    def get_current_time_nano_sec(self):
        return time.perf_counter_ns()




"""For unifing command in packet

    in start experiment runner():
        self.curr_times_packet = Commands_Packet()
        self.pop_subset_operations_df_based_times()
        self.get_grouped_AOM_commands()
        self.op_in_times_df_subset.apply(lambda row: self.add_internal_cmd_to_packet_by_row(row), axis=1)

    def add_internal_cmd_to_packet_by_row(self, df_row):
        curr_device = df_row[self.device_column]
        op_code = self.get_exp_op_code_from_device(curr_device)
        payload_data = self.get_payload_data_from_row(curr_device, df_row)
        self.curr_times_packet.add_internal_command(op_code, payload_data)

    def get_exp_op_code_from_device(self, curr_device):
        if self.is_aom_device(curr_device):
            return self.AOM_set_exp_op_code
        if self.is_gpio_device(curr_device):
            return self.GPIO_set_exp_op_code

    def get_payload_data_from_row(self, curr_device, row):
        trigger = self.trigger_op_code
        time = int(row[time_str]) + self.user_time_vs_operation_time_dif
        channel = int(row[self.channel_col])
        if self.is_aom_device(curr_device):
            amplitude_val = row[amplitude_str]
            frequency_val = row[frequency_str]

            # return self.AOM_set_exp_op_code
        if self.is_gpio_device(curr_device):
            activate_val = row[self.activate_str]
            # return self.GPIO_set_exp_op_code

    def get_grouped_AOM_commands(self):
        self.op_in_times_df_subset
        #for each group of AOM channel that share a common physical interface
        for aom_lst in common_interface_AOM_lists:
            common_aom_df=self.op_in_times_df_subset[self.op_in_times_df_subset[self.channel_col].isin(aom_lst)]\
                .groupby([time_str, self.device_column])
            if not common_aom_df.empty:
                print("to do implement insert to packet ")

    def is_aom_device(self, curr_device):
        if curr_device == self.AOM_str:
            return True

    def is_gpio_device(self, curr_device):
        if curr_device == self.GPIO_str:
            return True

    def pop_subset_operations_df_based_times(self):
        curr_time = self.get_current_time_nano_sec()
        added_to_op_time = self.start_experiment_time + self.user_vs_operation_times_diff + self.send_delay
        self.op_in_times_df_subset = self.exp_df[self.exp_df[time_str] <= curr_time + added_to_op_time]
        self.exp_df.drop(self.op_in_times_df_subset.index)


    def get_device_channel_tupple(self, input_file):
        splitted = input_file.split("_")
        return splitted[0], splitted[1]

    def get_current_time_nano_sec(self):
        return time.time_ns()



"""