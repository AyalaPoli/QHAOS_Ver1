AOM_str="AOM"
frequency_str="Frequency"
amplitude_str="Amplitude"

min_AOM_time_interval_nsec=2000 #The minimal time between two actions on the same AOM device

min_channel_index_AOM=1 #The minimal application channel index
max_channel_index_AOM=20  #The maximal application channel index

#The conversion between the appliaction channel and the physical channels
AOM_app_to_physical_index_dict={i:i for i in range(min_channel_index_AOM,max_channel_index_AOM+1)}

#Groups of AOM channel that share a common physical interface
common_interface_AOM_lists=[range(1, 4), range(5, 8), range(9, 12)]

set_function_str="Set"

AOM_function_parameters_dict={set_function_str:[frequency_str, amplitude_str]}
min_AOM_frequency_MHz=1 #Frequencey minimal value (MHz)
max_AOM_frequency_MHZ=250 #Frequiency maximal value (MHz)
min_AOM_amplitude=0 #amplitude minimal value (MHz)
max_AOM_amplitude=100 #amplitude maximal value (MHz)

AOM_function_parameters_range_dict={amplitude_str:[min_AOM_amplitude, max_AOM_amplitude],
                                        frequency_str:[min_AOM_frequency_MHz, max_AOM_frequency_MHZ]}

time_str="Time"
AOM_exper_file_headers=[time_str,amplitude_str,frequency_str]