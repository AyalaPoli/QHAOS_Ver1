GPIO_str="GPIO"


min_GPIO_time_interval_nsec=8 #The minimal time between two actions on the same GPIO device

min_channel_index_GPIO=1 #The minimal application channel index
max_channel_index_GPIO=16 #The maximal application channel index
#The conversion between the appliaction channel and the physical channels
GPIO_app_to_physical_index_dict={i:i for i in range(min_channel_index_GPIO, max_channel_index_GPIO+1)}

on_value=1 #Activate value
off_value=0 #Deactivate


min_channel_index_GPIO=min(GPIO_app_to_physical_index_dict.keys())
max_channel_index_GPIO=max(GPIO_app_to_physical_index_dict.keys())

set_function_str="Set"
set_function_param_str="Activate"
disactivate_function_param_str="Deactivate"

GPIO_function_parameters_dict={set_function_str:[set_function_param_str]}
GPIO_function_parameters_range_dict={set_function_param_str:[off_value,on_value]}

time_str="Time"
GPIO_exper_file_headers=[time_str, set_function_param_str]