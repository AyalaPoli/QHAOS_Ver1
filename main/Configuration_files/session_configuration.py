import socket
from main.Configuration_files.AOM_configuration import *
from main.Configuration_files.GPIO_configuration import *
from main.Configuration_files.paths import *
from main.GUI.Function_Setting import str_value_iterations_dict, infinite_iteration_txt

address_family = socket.AF_INET  # IPv4
socket_type = socket.SOCK_STREAM  # TCP
format = "utf-8"

#For the dummy server
server_host = "127.0.0.1"  # localhost
port = 1062  # The port used by the server

#For the physical box
#server_host = "192.168.1.3"
#port = 2007

BUFFERSIZE = 1024
server_messages = ""
username = "ayala"
password = "ayala"

default_dir_path=default_exp_test_dir
default_cycle_time=500000000
default_iteration_num=str_value_iterations_dict[infinite_iteration_txt]

#TODO define by measure
#user_time_vs_operation_time_diff = 1000000000 #the delta between start experiment time and the time the experiments start to execute
user_time_vs_operation_time_diff = 3000000000
pre_operation_send_time_diff = 3000000000 #delay between send to control and the execution of command


class Function_Definition():
    def __init__(self, func_str,int_index=0,fields=None):
        self.func_str=func_str
        self.int_index=int_index
        self.hex_op_code=hex(self.int_index)
        self.fields=fields

start_experiment_def=Function_Definition("Start experiment",0)
stop_experiment_def_params=Function_Definition("Stop experiment",1)
reset_experiment_def_params=Function_Definition("Reset experiment",2)


AOM_immidiate_fields_range_dict={"Channel index": range(min_channel_index_AOM,max_channel_index_AOM+1),
                       "Params to configure":[hex(0),hex(1),hex(2)],
                       "Amplitude":range(min_AOM_amplitude,max_AOM_amplitude),
                       "Frequency:":range(min_AOM_frequency_MHz, max_AOM_frequency_MHZ)}

GPIO_immidiate_fields_range_dict={"Channel index": range(min_channel_index_GPIO,max_channel_index_GPIO+1),
                                  "Channel value":[0,1]}

set_AOM_immidiate_def=Function_Definition("Set AOM", fields=AOM_immidiate_fields_range_dict)
set_GPIO_immidiate_def=Function_Definition("Set GPIO", fields=GPIO_immidiate_fields_range_dict)


AOM_experiments_fields_range_dict=AOM_immidiate_fields_range_dict.copy()
AOM_experiments_fields_range_dict.update({"Operation condition":[0,1],"Trigger channel":[0,1],"Num of channels":[10]})

min_cycles_time_interval=min_AOM_time_interval_nsec
