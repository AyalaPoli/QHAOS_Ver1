from dataclasses import dataclass
from main.Configuration_files.AOM_configuration import *
from main.Configuration_files.GPIO_configuration import *
import tkinter as tk
import customtkinter as ctk

import struct



@dataclass
class Function_Settings:
    name: str
    decim_op_code: int
    fields: dict
    control_flag: bool = False

    def set_hex_op_code(self):
        self.hex_op_code = hex(self.decim_op_code)

    def set_control_hack(self):
        # to be determined
        self.control_hack = self.name

    def set_control_flag_on(self):
        self.control_flag = True

    def set_control_flag_off(self):
        self.control_flag = False

    def set_field(self, field_name, field_val):
        self.fields[field_name]=field_val



#connect_fields = dict.fromkeys([connect_time_str, connect_username_str])
#connect_settings = Function_Settings(connect_name, connect_dec_op_code, connect_fields)

"""SET EXPERIMENT STATE"""
set_exp_state_name = "SET EXPERIMENT STATE"
set_exp_state_dec_op_code = 0

experiment_state_field_name = "EXPERIMENT STATE"
start_exp_dec_op_code = 0
start_exp_name = "START EXPERIMENT"
stop_exp_dec_op_code = 1
stop_exp_name = "STOP EXPERIMENT"
reset_exp_dec_op_code = 2
reset_exp_name = "RESET EXPERIMENT"
experiment_state_fields_options_dict = {start_exp_dec_op_code: start_exp_name,
                                        stop_exp_dec_op_code: stop_exp_name,
                                        reset_exp_dec_op_code: reset_exp_name}

dir_path_field_name="DIR PATH"
iterations_num_field_name="ITER NUM"
cycle_time_field_name="CYCLE TIME"
set_exp_state_fields = dict.fromkeys([experiment_state_field_name])

exp_state_set_settings = Function_Settings(set_exp_state_name, set_exp_state_dec_op_code, set_exp_state_fields)

ack_from_server_format="<4s H B B B H B"
struct_from_server = struct.Struct(ack_from_server_format)


"""SET GPIO VALUE"""
set_GPIO_name = "SET GPIO"
set_GPIO_imm_op_code = 1
channel_index_field_name = "CHANNEL INDEX"
channel_value_field_name = "CHANNEL VALUE"
set_GPIO_index_field_options_dict = {range(min_channel_index_GPIO, max_channel_index_GPIO): channel_index_field_name}
set_GPIO_value_fields_options_dict = {on_value: set_function_param_str,
                                      off_value: disactivate_function_param_str}

set_GPIO_fields = dict.fromkeys([channel_index_field_name, channel_value_field_name])
set_GPIO_settings = Function_Settings(set_GPIO_name, set_GPIO_imm_op_code, set_GPIO_fields)
set_GPIO_format='B B'


"""SET AOM VALUE"""
set_AOM_name = "SET AOM"
set_AOM_imm_op_code=2
params_config_field_name="Params_to_configure"
only_amp_to_config=1
only_freq_to_config=2
two_params_to_config=3

first_param_field_name="First_param"
second_param_field_name="Second_param"
set_aom_format='B B f'
set_aom_format_two_params='B B f f'


"""SET AOM FROM EXPERIMENT VALUE"""
set_aom_exp_format_one_params='B B Q B B B f'
set_aom_exp_format_two_params='B B Q B B B f f'
set_aom_exp_op_code = 9

"""ITERATION STRING TO NUMBER CONVERT"""

single_run_txt = "Single Run"
infinite_iteration_txt = "Infinite Execution"
enter_iteration_txt = "Enter Iterations Number: "
#single_iter_val, infinite_iter_val, enter_iter_val = range(1, 4)
iter_str_lst=[single_run_txt,infinite_iteration_txt, enter_iteration_txt]
str_value_iterations_dict={iter_str: val for iter_str, val in zip(iter_str_lst, range(1,4))}

"""SET GPIO FROM EXPERIMENT VALUE"""
set_gpio_exp_format='B B Q B B'
set_gpio_exp_op_code = 10

"""All FUNCTIONS SETTINGS LST"""
functions_settings_lst = [exp_state_set_settings, set_GPIO_settings]

def get_val_by_dict(dict, req_val):
    return [k for k, val in dict.items() if val == req_val][0]

def create_functions_settings_names_dict(functions_settings_lst):
    return {f.name: f for f in functions_settings_lst}

def get_device_channel_tupple(input_file):
    splitted = input_file.split(".")[0].split("_")
    return splitted[0], splitted[1]

def build_listbox_index_dict(input_lst, start_val=1):
    return {curr_input: i for curr_input, i in zip(input_lst, range(start_val,len(input_lst)+start_val))}


class Parameter_Entry():
    def __init__(self, frame, param_name, param_index, sticky, padx, pady, valid_msg_txt, val_type, default_val=0):
        self.frame=frame
        self.param_name=param_name

        if isinstance(val_type, int):
            self.param_intval=tk.IntVar()
        if isinstance(val_type, float):
            self.param_intval=tk.DoubleVar()
        if isinstance(val_type, str):
            self.param_intval=tk.StringVar()

        self.default_val=default_val
        self.param_input_value=None
        self.param_index=param_index
        self.sticky=sticky
        self.padx=padx
        self.pady=pady
        self.valid_msg_txt=valid_msg_txt
        self.build_param_entry()


    def build_param_entry(self):
        #self.frame.grid(row=self.param_index, column=0)
        self.label=ctk.CTkLabel(self.frame, text=self.param_name)
        self.label.grid(row=self.param_index, column=0, sticky=self.sticky, pady=self.pady, padx=self.padx)
        self.label.configure(background="gainsboro")

        self.entry=ctk.CTkEntry(self.frame, textvariable = self.param_intval)
        self.entry.grid(row=self.param_index, column=1, sticky=self.sticky, pady=self.pady, padx=self.padx)

        if self.default_val:
            self.entry.delete(0, tk.END)
            self.entry.insert(0, self.default_val)
        else:
            self.entry.delete(0, tk.END)

        self.params_range_mgs = tk.Label(self.frame, text=self.valid_msg_txt)
        self.params_range_mgs.grid(row=self.param_index + 1, column=1, sticky=self.sticky)
        self.params_range_mgs.configure(background="gainsboro")

        self.visiable_obj_lst=[self.label,self.entry,self.params_range_mgs]


    def is_empty_entry(self):
        return True if len(self.entry.get()) == 0 else False

    def destroy(self):
        self.entry.destroy()