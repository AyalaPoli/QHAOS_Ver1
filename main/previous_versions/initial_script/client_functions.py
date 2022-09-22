from main.GUI.GUI_params import *
from main.previous_versions.run_params import *


#GUI
def show_connection_message(host, port, curr_time):
    output=easygui.msgbox(connection_message.format(curr_time,host,port), conncetion_title, connection_button)
    return output

def get_automatic_output(input_file, host, time_str):

    basename = os.path.splitext(os.path.basename(input_file))[0]
    output_file = add_to_path(received_from_server_dir, "{}_{}_{}.txt".
                              format(basename, host.replace(".","_") ,time_str.replace("-","_")))
    return output_file

def get_client_files_from_GUI(host, timestr):
    selected_input_option=easygui.ynbox(select_file_message, select_file_title, (demo_option, upload_option))
    select_str="selected demofile" if selected_input_option else "selected upload file"
    print(select_str)
    input_file=demo_file if selected_input_option \
        else easygui.fileopenbox(msg=upload_message)

    selected_output_option = easygui.ynbox(savebox_message, select_file_title, (automatic_str, choose_dest))
    output_file=None
    while not output_file:
        output_file=get_automatic_output(input_file, host, timestr) if selected_output_option \
            else easygui.filesavebox(msg=savebox_message)
        print(output_file)
        if os.path.exists(output_file):
            overwrite_flag = easygui.buttonbox(msg=overwrite_message, choices=(Yes_str, No_str))
            if overwrite_flag == No_str:
                output_file=None

    return input_file, output_file

def get_req_device_from_GUI():
    choice = easygui.choicebox(device_message, device_title, device_choices)
    return choice

def device_choose_flow():
    choice=get_req_device_from_GUI()
    filename=config_AOM if choice==AOM_str else choice==GPIO_str
    f = open(filename, "r")
    config_txt = f.readlines()
    f.close()
    easygui.codebox(show_config_file_message.format(filename), "Show File Contents", config_txt)
    return choice

def show_file_validation_message(input_file):
    msg=is_valid_experiment_file(input_file)
    easygui.codebox(validation_file_msg.format(input_file), "Show File Contents", msg)


def get_expeiment_num_from_GUI():
    choice = easygui.choicebox(experiment_num_msg, experiment_num_title, experiment_num_choices)
    return choice

def show_experiment_start_message(file, device, num):
    output=easygui.msgbox(start_experiment_message.format(file, device, num), start_experiment_title, start_experiment_button)
    return output

def show_experiment_sent_message(file, device, num, curr_time):
    output = easygui.msgbox(sent_experiment_message.format(file, device, num, curr_time), sent_experiment_title, Done_button)
    return output


#VALIDATE Experiment file

def is_valid_file_type(file_type):
    return True if file_type in [AOM_str, GPIO_str] else False

def get_file_type_from_file_name(filename):
    basename=os.path.basename(filename)
    return basename.split("_")[0]

def is_valid_headers_raw(input_headers_raw, file_type):
    #msg=valid_message
    if file_type==AOM_str:
        req_headers=AOM_headers_raw
    elif file_type==GPIO_str:
        req_headers=GPIO_headers_raw
    for (i, j) in zip(input_headers_raw, req_headers):
        if i!=j:
            print("msg")



def is_valid_experiment_file(input_file):
    msg=valid_message
    file_type=get_file_type_from_file_name(input_file)
    valid_file_type=is_valid_file_type(file_type)
    if not valid_file_type:
        return "{} File type is invalid".format(file_type)
    infile=open(input_file, 'r')
    headers_raw=infile.readline()
    headers_msg=is_valid_headers_raw(headers_raw, file_type)
    row_index=2
    for raw in infile.readlines():
        row_index+=1

    return msg

