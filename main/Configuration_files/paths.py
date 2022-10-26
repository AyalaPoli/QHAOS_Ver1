import os

from pathlib import Path

def add_to_path(prefix, suffix):
    return os.path.join(prefix, suffix)

import sys,os
#sys.path.append(os.getcwd())

project_dir= os.path.dirname(Path(os.path.dirname(os.path.abspath(__file__))).parent.absolute())
root_dir=add_to_path(project_dir, "main")


config_dir=add_to_path(root_dir, "Configuration_files")
config_files_dir=add_to_path(config_dir, "files_params")
config_locations_dir=add_to_path(config_dir, "locations")
config_AOM=add_to_path(config_dir, "AOM_configuration.py")
config_GPIO=add_to_path(config_dir, "GPIO_configuration.py")
config_SNSPD=add_to_path(config_dir, "SNSPD_configuration.py")

experiments_files_dir=add_to_path(root_dir, "Experiment Files")
tests_dir=add_to_path(root_dir,"Tests")
widgets_photos_dir=add_to_path(tests_dir, "widgets_photos")

config_run_dir=add_to_path(config_dir, "run")
config_session_dir=add_to_path(config_dir, "Session")
files_dir=add_to_path(root_dir, "test_files")

client_dir=add_to_path(files_dir, "client")
valid_files_dir=add_to_path(experiments_files_dir, "valid_files")
invalid_files_dir=add_to_path(experiments_files_dir, "invalid_files")
received_from_server_dir=add_to_path(client_dir, "received_from_server")

server_dir=add_to_path(files_dir, "server")
sent_from_server_dir=add_to_path(server_dir, "sent")
received_from_client_dir=add_to_path(server_dir, "received")

experiments_directories=add_to_path(root_dir, "Experiments_Directories")
working_dir = add_to_path(experiments_directories, "experiment_temp_working_dir")
default_exp_test_dir=add_to_path(experiments_directories,"default_experiment_dir")

sorted_merged_working_path = "sorted_df.csv"
last_running_path_file=add_to_path(config_dir, "last_running_path.txt")
events_time_filename="events.txt"
last_view_path_file=add_to_path(config_dir, "last_visualization_path.txt")

prev_user_selections_path=add_to_path(config_dir, "previous_user_selections.json")
exp_runner_key="Experiment Runner"
exp_run_last_path="last running path"
exp_viewer_key="Experiment Viewer"
exp_view_last_path="last viewer path"
exp_view_last_AOMs="AOM channels"
exp_view_last_GPIOs="GPIO channels"

snspd_timing_filename="SNSPD_timing.csv"

SNSPDs_data_storage=add_to_path(root_dir, "dummy_data_storage")
external_experiment_files_list=[events_time_filename, snspd_timing_filename]