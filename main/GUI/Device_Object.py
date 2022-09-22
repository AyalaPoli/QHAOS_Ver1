from main.Configuration_files.AOM_configuration import *
from main.Configuration_files.GPIO_configuration import *
import tkinter as tk
from main.GUI.GUI_params import min_str, max_str, time_str


class Device_Object():
    def __init__(self, device_type):
        self.device_type=device_type

        if device_type==AOM_str:
            self.app_to_physical_index_dict = AOM_app_to_physical_index_dict
            self.functions_params_dict= AOM_function_parameters_dict
            self.current_function=set_function_str
            self.function_parameters_range_dict=AOM_function_parameters_range_dict
            self.exper_file_headers=AOM_exper_file_headers
            self.min_time_interval_nsec=min_AOM_time_interval_nsec
            self.val_type=float(1)

        elif device_type==GPIO_str:
            self.app_to_physical_index_dict = GPIO_app_to_physical_index_dict
            self.functions_params_dict= GPIO_function_parameters_dict
            self.current_function=set_function_str
            self.function_parameters_range_dict=GPIO_function_parameters_range_dict
            self.exper_file_headers=GPIO_exper_file_headers
            self.min_time_interval_nsec=min_GPIO_time_interval_nsec
            self.val_type=int(1)

        self.update_current_params_by_function()


    def update_current_params_by_function(self):
        self.current_params_lst=list(self.functions_params_dict[self.current_function])

    def get_params_lst(self):
        return self.current_params_lst

    def is_AOM_device(self):
        return True if self.device_type==AOM_str else False

    def is_GPIO_device(self):
        return True if self.device_type==GPIO_str else False

    def get_param_value_range(self, param, min_or_max):
        range_index=0 if min_or_max==min_str else 1
        return self.function_parameters_range_dict[param][range_index]

    def get_param_min_max_values(self, param):
        return (self.function_parameters_range_dict[param][0],self.function_parameters_range_dict[param][1])


    def get_AOM_param_value_range(self, param_name):
        min_val = self.function_parameters_range_dict[param_name][0]
        max_val = self.function_parameters_range_dict[param_name][1]
        return min_val, max_val

    def get_GPIO_valid_values_lst(self, param_name):
        return self.function_parameters_range_dict[param_name]

