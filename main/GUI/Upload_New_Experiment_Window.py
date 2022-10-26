import tkinter as tk
import customtkinter as ctk
import pandas as pd
import numpy as np

from main.Configuration_files.paths import *
#from main.GUI.GUI_params import icon_file,qs_logo_file
from tkinter.messagebox import askokcancel
from main.GUI.Base_Window import Base_Window
from main.GUI.GUI_params import device_types_lst
from main.GUI.Device_Object import Device_Object
from main.GUI.GUI_params import min_str,max_str,time_str
from main.GUI.Function_Setting import *
from main.Configuration_files.paths import working_dir
from distutils.dir_util import copy_tree
from distutils.dir_util import remove_tree
from main.Configuration_files.session_configuration import *


class Upload_New_Experiment(Base_Window):

    #buttons_font_size=10

    #run_new_experiment_title = 'Upload_New_Experiment'
    window_width = 750
    window_height = 900
    sticky="nsew"

    #upload_experiment_padx = 10
    #upload_experiment_pady = 10

    curr_title = 'Upload New Experiment'
    upload_dir_button_txt = "Upload Experiment Directory"
    upload_file_dir = experiments_files_dir
    ask_filename_title = "Please Choose Directory to upload"
    upload_dir_label_txt = "Experiment Directory:"
    validate_experiment_button_str = "Validate Experiment"
    valid_message_str = "Valid Experiment File"
    invalid_message_str = "\n".join(["Error: in line number {}: invalid something".format(i) for i in range(30)])
    input_dir_path=""
    valid_file_types_lst=[".csv"]
    validation_message_str = ""
    device_col = "Device"
    channel_col = "Channel"

    iteration_label_txt="Please choose experiment iteration:"

    #device_configuration_experiment_txt = "Device Configuration"

    select_upload_experiment_title="Select Experiment"

    default_iteration_num=0
    iteration_num=default_iteration_num
    apply_experiment_title = "Apply Experiment"
    apply_experiment_msg = "Your action request was accepted"

    wait_for_validation_text="Please wait while the format of the experiment directory is being validated ...\n\n"
    no_input_iterations_title = "Number of Iterations Missing"
    no_input_iterations_msg = "Please select number of iterations to the experiment"

    no_input_file_title = "Experiment Directory Missing"
    no_input_file_msg = "Please select experiment directory"

    no_cycle_time_title = "Cycle Time Missing"
    no_cycle_time_msg = "Please select total cycle time"

    invalid_file_title = "Uploaded file format is invalid"
    invalid_file_msg = "Uploaded file format is invalid.\nPlease fix the errors and try again"

    apply_button_txt="Apply Experiment File"
    apply_experiment_format="Selected Directory: {}\n\nIterations: {}\n\nCycle time: {}\n\nContinue?"
    rows_weights_dict={0:1, 1:1, 2:1, 3:1, 4:1}
    columns_weights_dict={0:1}

    invalid_filename_error="\nError in the file name: {}:"
    invalid_device_filename_format="\nDevice: {} doesn't found in the devices list: {}\n"
    invalid_channel_filename_format="\nDevice channel index: {} doesn't found in the {} channels list: \n{}\n"
    invalid_suffix_filename_format="\nThe extension: {} doesn't found in valid file types list: {}\n"
    invalid_filename_format="\nThe file name format should be: [DeviceName]_[Channel].csv\n"

    invalid_csv_format="\nError in input csv file: {}\n"
    invalid_headers_line_format="\nThe headers line: {} should be: {}\n"
    invalid_line_length_format="\nThe length of line: {} {} is not the required length: {}\n"
    invalid_range_param_format="\nThe {} value In lines [{}] is out of range: [{} - {}]\n"
    invalid_value_param_format="\nThe values In lines [{}] are not one of the valid values: {}\n"

    invalid_times_format="\nError in times intervals: {}\n"
    invalid_time_intervals_format="\nTime interval of the times in steps [{}] and their previous steps must be greater than {} nsec\n"

    total_cycles_time_txt="Total time of each experiment iteration (ns):"
    total_cycles_valid_msg="\nThe cycle time should be at least the time of latest step {} + "+str(min_cycles_time_interval)+"ns"
    #total_cycles_valid_msg="\nThe cycle time should be at least the time of latest step  + {} ".format(min_cycles_time_interval)
    invalid_cycle_time_title = "\nError in total time of cycles"
    invalid_cycle_time_msg = "The total cycle time {}ns is too short. \nTotal cycle time must be at " \
                             "least the time of latest step + the minimal time between experiment cycles:\n{} + "\
                             + str(min_cycles_time_interval)+"ns"

    parsing_file_exception_msg="\nParsing the file raised exception\n"

    max_err_index_lst=10
    empty_str=""



    def __init__(self, run_exp_window_obj, default_flag=False, restart_flag=False, external_uploaded_path=None):
        print(" in init upload new experiment window")
        super().__init__(run_exp_window_obj.window)
        self.run_exp_window=run_exp_window_obj
        if default_flag:
            self.window.withdraw()
            self.initial_window_params_by_default_exp()
        if restart_flag:
            self.window.withdraw()
            self.initial_window_params_by_restart_exp()
        if external_uploaded_path:
            self.window.withdraw()
            self.initial_window_params_by_external_uploaded_exp(external_uploaded_path)
        else:
            self.build_upload_file_frame()
            self.build_validation_file_frame()
            self.build_total_cycles_times_frame()
            self.build_iteration_num_frame()
            self.build_apply_frame()


    def initial_window_params_by_default_exp(self):
        self.input_dir_path = default_dir_path
        self.iteration_num = default_iteration_num
        self.cycles_total_time = default_cycle_time

    def initial_window_params_by_restart_exp(self):
        self.input_dir_path = self.run_exp_window.app.client.last_dir_path
        self.iteration_num = self.run_exp_window.app.client.last_iteration_num
        self.cycles_total_time = self.run_exp_window.app.client.last_cycle_time

    def initial_window_params_by_external_uploaded_exp(self, inserted_path):
        self.input_dir_path = inserted_path

    def build_upload_file_frame(self):
        self.upload_file_dir_frame=super().build_frame(self.window, 0, 0, sticky="nsew")
        self.upload_file_button=super().build_button(self.upload_file_dir_frame, self.upload_dir_button_txt,
                                                self.upload_experiment_dir_command, 0, 0, sticky="W")

        self.filename_label=super().build_label(self.upload_file_dir_frame, self.input_dir_path, 0, 1, sticky="W")


    def build_validation_file_frame(self):

        self.validation_frame=super().build_frame(self.window,1,0, sticky="nsew")
        #self.validation_frame.grid(columnspan=2)
        self.file_validation_text=ctk.CTkTextbox(self.validation_frame, bg='white', cursor='circle', wrap=tk.WORD)
        self.file_validation_text.pack(expand = True, fill='both')

        valid_scrollbar = ctk.CTkScrollbar(self.validation_frame, orientation='vertical',
                                       command=self.file_validation_text.yview)
        self.file_validation_text['yscrollcommand'] = valid_scrollbar.set

        #valid_scrollbar.grid(row=0, column=1, sticky='ns',padx=2)
        #valid_scrollbar.pack()
        #yscrollbar.config(command=self.file_validation_text.yview)

    def upload_experiment_dir_command(self):
        with open(last_running_path_file, 'r') as f:
            last_running_path=f.read().rstrip()
        self.input_dir_path = tk.filedialog.askdirectory(initialdir=last_running_path, title=self.ask_filename_title)
        with open(last_running_path_file, 'w') as f:
            f.write(self.input_dir_path)
        if not self.input_dir_path:
            return
        #self.file_validation_text.insert(tk.INSERT, self.wait_for_validation_text)

        validation_message = self.get_validatation_message_of_dir_format()
        self.is_valid_file=True if validation_message == self.valid_message_str else False
        validation_label_bg = 'palegreen' if self.is_valid_file else 'darksalmon'
        self.file_validation_text.configure(bg=validation_label_bg)
        self.file_validation_text.insert("1.0", "")
        self.file_validation_text.insert(tk.INSERT, validation_message)
        self.file_validation_text.configure(state='disabled')
        if self.is_valid_file:
            self.filename_label.configure(text=self.input_dir_path)
            self.save_experiment_merged_sorted_df()

            self.latest_time_point=self.get_latest_time_point()
            self.total_cycles_time_entry.param_intval.set(self.latest_time_point+min_cycles_time_interval)
            self.total_cycles_valid_msg.format("")
            self.total_cycles_time_entry.params_range_mgs.configure(text=self.total_cycles_valid_msg.format(self.latest_time_point))

    def save_experiment_merged_sorted_df(self):
        dfs_lst = []
        if os.path.exists(working_dir):
            remove_tree(working_dir)
        copy_tree(self.input_dir_path, working_dir)

        for input_file in os.listdir(working_dir):
            if input_file in external_experiment_files_list:
                continue
            df = pd.read_csv(add_to_path(self.input_dir_path, input_file), keep_default_na=False)
            device, channel = get_device_channel_tupple(input_file)
            df[self.device_col] = device
            df[self.channel_col] = channel
            dfs_lst.append(df)

        self.exp_df = pd.concat(dfs_lst, ignore_index=True, axis=0)
        self.exp_df.sort_values(by=[time_str, self.device_col], inplace=True)
        self.exp_df.to_csv(sorted_merged_working_path, index=False)

    def get_validatation_message_of_dir_format(self):
        # validation_message=invalid_message_str

        for self.curr_file in os.listdir(self.input_dir_path):

            if self.curr_file==events_time_filename:
                print("curr file {}".format(self.curr_file))
                print("events_time_filename {}".format(events_time_filename))
                self.run_exp_window.includes_visualization=True

                continue

            if self.curr_file==snspd_timing_filename:
                print("curr file {}".format(self.curr_file))
                print("events_time_filename {}".format(events_time_filename))
                self.run_exp_window.includes_SNSPD=True
                continue

            print("curr_file")
            print(self.curr_file)
            self.curr_file_full_path=os.path.join(self.input_dir_path, self.curr_file)

            filename_msg=self.get_filename_validation_msg()
            if filename_msg:
                return self.invalid_filename_error.format(self.curr_file)+filename_msg

            file_params_range_msg=self.get_file_format_validation_msg()
            if file_params_range_msg:
                return self.invalid_csv_format.format(self.curr_file)+file_params_range_msg

        return self.valid_message_str

    def get_filename_validation_msg(self):
        try:
            base_name, suffix=os.path.splitext(self.curr_file)
            device_name=base_name.split("_")[0]
            device_index=base_name.split("_")[1]
            if device_name not in device_types_lst:
                return self.invalid_device_filename_format.format(device_name, device_types_lst)

            self.curr_device_obj=Device_Object(device_name)
            valid_app_channels=self.curr_device_obj.app_to_physical_index_dict.keys()
            if int(device_index) not in valid_app_channels:
                return self.invalid_channel_filename_format.format(device_index, device_name, valid_app_channels)

            if suffix not in self.valid_file_types_lst:
                return self.invalid_suffix_filename_format.format(suffix,  self.valid_file_types_lst)

            return self.empty_str

        except Exception as e:
            return self.invalid_filename_format+str(e)

    def get_file_format_validation_msg(self):
        msg=""
        df = pd.read_csv(add_to_path(self.input_dir_path, self.curr_file), keep_default_na=False)
        msg += self.is_valid_time_column(df)
        if self.curr_device_obj.is_AOM_device():
            return self.is_valid_AOM_file(df)
        if self.curr_device_obj.is_GPIO_device():
            return self.is_valid_GPIO_file(df)

    def is_valid_AOM_file(self, df):
        file_msg=""
        file_msg+=self.is_valid_param_column(df, amplitude_str)
        file_msg+=self.is_valid_param_column(df, frequency_str)
        return file_msg

    def is_valid_time_column(self, df):
        times_arr=df[time_str].to_numpy().astype(np.int64)
        min_time_interval = self.curr_device_obj.min_time_interval_nsec
        invalid_time_index=[]
        for i in range(1, len(times_arr)):
            if times_arr[i]-times_arr[i-1]<=min_time_interval:
                invalid_time_index.append(i)
        if invalid_time_index:
            return self.invalid_time_intervals_format.format(self.get_lst_str(invalid_time_index), min_time_interval)
        return ""

    def get_lst_str(self, lst):
        return str(lst[:self.max_err_index_lst])+"... " if len(lst)>self.max_err_index_lst else str(lst)


    def is_valid_param_column(self, df, param):
        self.min_val, self.max_val=self.curr_device_obj.get_param_min_max_values(param)
        invalid_param_index=df[df[param].apply(self.is_val_not_in_range)].index.tolist()
        if invalid_param_index:
            return self.invalid_range_param_format.format(param, self.get_lst_str(invalid_param_index), self.min_val, self.max_val)
        return ""

    def is_val_not_in_range(self, curr_val):
        if not curr_val:
            return False
        return False if float(curr_val)>=self.min_val and float(curr_val)<=self.max_val else True

    def is_valid_GPIO_file(self, df):
        file_msg=""
        file_msg+=self.is_valid_time_column(df)
        file_msg+=self.is_valid_activate_column(df)
        return file_msg

    def is_valid_activate_column(self, df):
        self.valid_values_lst = [on_value, off_value]
        invalid_param_index=df[df[set_function_param_str].apply(self.is_valid_activate_val)].index.tolist()
        if invalid_param_index:
            return self.invalid_value_param_format.format(self.get_lst_str(invalid_param_index), self.valid_values_lst)
        return ""

    def is_valid_activate_val(self, val):
        return False if int(val) in self.valid_values_lst else True

    def build_iteration_num_frame(self):
        iteration_frame=super().build_frame(self.window, 2, 0)
        #iteration_frame.grid(columnspan=2)
        super().build_label(iteration_frame, self.iteration_label_txt, 0, 0)

        self.experiment_iteration = tk.StringVar()

        for iter_str, iter_val in str_value_iterations_dict.items():
            super().build_radiobutton(iteration_frame, iter_str, iter_val-1, 1, self.experiment_iteration, iter_val,
                                            self.num_iter_entry_state, padx=0, sticky="W")

        self.iteration_num_intval=tk.IntVar()
        self.iteration_num_entry=super().build_entry(iteration_frame, self.iteration_num_intval,
                                                self.get_experiment_iteration_value, 2, 2, sticky="nsew")

        #super().change_widget_config(self.iteration_num_entry, "state", tk.DISABLED)

        super().change_widget_state(self.iteration_num_entry, activate=False)

    def num_iter_entry_state(self):

        if int(self.experiment_iteration.get())==int(str_value_iterations_dict[enter_iteration_txt]):
            #super().change_widget_config(self.iteration_num_entry,"state",tk.NORMAL)
            super().change_widget_state(self.iteration_num_entry)

        else:
            #super().change_widget_config(self.iteration_num_entry,"state",tk.DISABLED)
            super().change_widget_state(self.iteration_num_entry, activate=False)

    def get_experiment_iteration_value(self):
        self.iteration_num=self.iteration_num_intval.get()

    def build_total_cycles_times_frame(self):
        self.total_cycles_time_frame=super().build_frame(self.window, 3, 0, sticky="nsew")
        self.total_cycles_time_entry = Parameter_Entry(self.total_cycles_time_frame, self.total_cycles_time_txt, 0,
                                                    self.sticky, super().label_padx, super().label_pady, self.total_cycles_valid_msg.format(""),
                                                       "str", default_val=0)
        self.total_cycles_time_entry.build_param_entry()
        self.total_cycles_time_entry.entry.bind("<Return>", self.get_total_cycles_time_value)


    def get_total_cycles_time_value(self):
          self.cycles_total_time=self.total_cycles_time_entry.param_intval.get()

    def apply_upload_dir(self):
        print("in apply_upload_dir")
        self.run_exp_window.change_experiment_info_details_after_upload(self.input_dir_path, self.iteration_num, self.cycles_total_time)
        self.window.destroy()

    def build_apply_frame(self):
        apply_frame=super().build_frame(self.window, 4, 0, sticky="nsew")
        #apply_frame.grid(columnspan=2)
        self.apply_experiment_button=super().build_button(apply_frame, self.apply_button_txt,
                                                     self.select_action_msgbox_cmd, 0, 0, sticky="nsew")


    def create_experiment_df(self):
        print("in create experiment dataframe")
        dfs_lst = []
        initial_state_dfs_lst= []
        if os.path.exists(working_dir):
            for file in os.listdir(working_dir):
                os.remove(add_to_path(working_dir, file))
        copy_tree(self.input_dir_path, working_dir)

        for input_file in os.listdir(working_dir):
            if input_file in external_experiment_files_list:
                continue
            df = pd.read_csv(add_to_path(self.input_dir_path, input_file), keep_default_na=False)
            device, channel = get_device_channel_tupple(input_file)
            print(device)
            print(channel)
            df[self.device_col] = device
            df[self.channel_col] = channel
            dfs_lst.append(df)
            initial_state_dfs_lst.append(df.head(1))

        self.exp_df = pd.concat(dfs_lst, ignore_index=True, axis=0)
        self.initial_state_df=pd.concat(initial_state_dfs_lst, ignore_index=True,axis=0)
        self.exp_df.sort_values(by=[time_str, self.device_col], inplace=True)
        self.exp_df.to_csv(sorted_merged_working_path, index=False)
        print("after to csv")


    def get_latest_time_point(self):
        return int(self.exp_df.iloc[-1:][time_str])

    def select_action_msgbox_cmd(self):
        if not self.experiment_iteration.get():
            tk.messagebox.showwarning(title=self.no_input_iterations_title, message=self.no_input_iterations_msg)
        elif not self.input_dir_path:
            tk.messagebox.showwarning(title=self.no_input_file_title, message=self.no_input_file_msg)
        elif not self.is_valid_file:
            tk.messagebox.showwarning(title=self.invalid_file_title, message=self.invalid_file_msg)
        elif not self.total_cycles_time_entry.param_intval.get():
            tk.messagebox.showwarning(title=self.no_cycle_time_title, message=self.no_cycle_time_msg)
        else:
            self.cycles_total_time=int(self.total_cycles_time_entry.param_intval.get())
            #latest_time_point = self.get_latest_time_point()

            if self.cycles_total_time - self.latest_time_point < min_cycles_time_interval:
                super().show_err_msg(self.invalid_cycle_time_title,
                                     self.invalid_cycle_time_msg.format(self.cycles_total_time, self.latest_time_point))
            else:
                self.iteration_num = int(self.experiment_iteration.get())
                iter_str=get_val_by_dict(str_value_iterations_dict, self.iteration_num)
                select_upload_experiment_txt=self.apply_experiment_format.format(self.input_dir_path, iter_str,self.cycles_total_time)

                select_action_flag=askokcancel(title=self.select_upload_experiment_title, message=select_upload_experiment_txt)
                if select_action_flag:
                    self.create_experiment_df()
                    self.apply_upload_dir()