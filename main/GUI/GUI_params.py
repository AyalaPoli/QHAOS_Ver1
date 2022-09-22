#import easygui
#from main.Configuration_files.files_params import *
from main.Configuration_files.paths import *

default_font="lucida"

root_width=600
root_height=400
icon_file=add_to_path(config_dir,"qs_bullet.ico")
qs_logo_file=add_to_path(config_dir,"qs_logo.png")
qhaos_logo_file=add_to_path(config_dir,"qhaos_logo.png")

big_font_size=10

root_title = 'Software Demo'
root_message_str = "\nWelcome to the software demo!\n Please select your action from the menu"

run_new_experiment_title='Run New Experiment'
run_experiment_window_width=1200
run_experiment_window_height=600
new_experiment_window_txt="This window controls the experiment run"

#maybe not relevan
upload_exp_file_window_width= 800
upload_exp_file_window_height=500

upload_file_dir=experiments_files_dir
askfilenametitle="Please choose file to upload"
upload_file_label_txt="Experiment File:"

buttons_experiment_padx=10
buttons_experiment_pady=10

frames_experiment_padx=10
frames_experiment_pady=10

#upload_file_frame
upload_file_button_txt="Upload Experiment File"
upload_experiment_file_window_title="Upload Experiment File"
validate_experiment_button_str="Validate Experiment"
valid_message_str="Valid Experiment File"
invalid_message_str= "\n".join(["Error: in line number {}: invalid something".format(i) for i in range(30)])

#vizualize_file_frame
visualize_file_button_txt="File Visualization"

#Experiment buttons
start_experiment_txt="Start Experiment"
stop_experiment_txt="Stop Experiment"
device_configuration_experiment_txt="Device Configuration"


#choose_file_message
select_file_title="Choose Experiment file"
connection_message="Client connected to server\ntime: {}\nhost: {}\nport: {}"
conncetion_title="Connected to server"
connection_button="Continue"
select_file_message="Please choose an Experiment file:"
demo_option='Use demo test_files'
upload_option='upload file'
upload_message="Please choose an Experiment file"
select_output_file_message="Please choose an output log file:"
select_output_file_title="Choose output file"
savebox_message="Please choose an output log file"
automatic_str="create_automatically by file name"
choose_dest="choose destination"
overwrite_message="The file is already exists. Do you want to replace it?"
Yes_str="Yes"
No_str="No"


#Validation Experiment file message
validation_file_msg="Done to validate format of the input file {} "
min_str="minimum"
max_str="maximum"
#choose device
device_message="Please choose one of the following Experiment device"
device_title="Choose Experiment device"
AOM_str="AOM"
GPIO_str="GPIO"
time_str="Time"
activate_str="Activate"
device_choices=[AOM_str,GPIO_str]

#experiments number
experiment_num_msg="Please fill number of times to run the Experiment: "
experiment_num_title="Experiment loop"

#iteration_number - duplicated to delete
single_run_txt = "Single Run"
single_iter_val = 1
infinite_iteration_txt = "Infinite Execution"
infinite_iter_val = 2
enter_iteration_txt = "Enter Iterations Number: "
enter_iter_val = 3
experiment_num_choices=[single_run_txt, infinite_iteration_txt, enter_iteration_txt]

#show configuration
show_config_file_message="Please check the following device configuration.\n If you want to change parameters please update the file: {}"


#start Experiment
start_experiment_message="Server received the following request:\nExperiment file: {}\nDevice: {}\nRepeat: {}\n\n. Start Experiment?"
start_experiment_title="Start Experiment"
start_experiment_button="Start Experiment"

#sent Experiment
sent_experiment_message="Server received the following request:\nExperiment file: {}\nDevice: {}\nRepeat: {}\n at time: {}\n\n. For other command move to terminal"
sent_experiment_title="Experiment received"
Done_button= "Done"

#Device Actions
device_types_lst=[AOM_str, GPIO_str]

