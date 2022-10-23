import queue
import tkinter as tk
import tkinter.filedialog
from tkinter.messagebox import showerror

import threading
import socket
import time

# from main.GUI.GUI_params import icon_file,qs_logo_file
# from main.GUI.GUI_objects import *
from PIL import ImageTk, Image
from main.GUI.Run_New_Experiment_Window import *
from main.GUI.Device_Actions_Window import *
from main.GUI.Vizualization_Window import *
from main.GUI.SNSPD_Window import *
from main.Configuration_files.AOM_configuration import *
from main.Configuration_files.SNSPD_configuration import *
from main.GUI.Session_Window import *
from main.GUI.Help_Window import *
from main.GUI.Base_Window import Base_Window
from main.GUI.Client import Client
from main.GUI.Experiment_class import *

import customtkinter as ctk
import json

# TODO take care of error when closing client and the threading

class ER_Application(Base_Window):
    curr_title = 'QHAOS Software'
    root_message_str = "\nWelcome to the software demo!"
    window_width = 1200
    window_height = 800
    rows_weights_dict = {0: 1, 1: 8}
    columns_weights_dict = {0: 1}
    sent_packets_index = 1
    sent_packet_total_time = 0


    run_new_exp_txt = "Experiment Runner"
    vizualize_exp_txt = "Experiment Viewer"
    device_action_txt= "Device Actions"
    get_file_temp_txt = "Get File Template"
    get_session_info_txt = "Get Session Info"
    terminate_txt = "Terminate session"
    snspds_detection_txt = "SNSPDs detection"
    open_snspds_storage_txt = "SNSPDs storage"
    open_document_txt = "Open Documentation"

    experiment_str = "Experiment"
    device_action_str = "Device Actions"
    session_str = "Session"
    help_str = "Help"

    window_opened_info_title = "The Window is already open."
    window_opened_info_msg = "This Window is already open.\nA window opening is limited to one instance at a time"

    not_connected_client_title = "The socket is not connected"
    not_connected_client_msg = "There is no connected socket"

    dev_action_with_exp_err_title="An experiment is running"

    send_queue=queue.Queue()
    queue_empty_wait_time=10

    experiment=None
    run_exp_win_name='Run New Experiment'
    view_exp_win_name='Experiment Visualization'
    device_action_win_name="Single Device Action"
    snspd_win_name="SNSPD data"
    session_win_name="Session"
    help_win_name="Help"
    windows_names_lst = [run_exp_win_name, device_action_win_name, session_win_name]

    open_windows_dict={}


    def __init__(self, root):
        self.root = root
        self.app=self

        super().__init__(root)
        self.root_configuration()
        self.client = Client(self)

        self.open_window(self.session_win_name, Session_Window(self, connect=True))
        self.get_window_obj(self.session_win_name).window.grab_set()
        root.update()

        #self.test()

    def root_configuration(self):

        self.root.update_idletasks()
        self.root.overrideredirect(True)

        ctk.set_appearance_mode("light")  # Modes: system, light, dark
        ctk.set_default_color_theme("blue")
        root_qs_logo_image = ImageTk.PhotoImage(file=qhaos_logo_file)
        self.root_qs_logo_label = tk.Label(self.window, image=root_qs_logo_image)
        self.root_qs_logo_label.configure(background="black")
        self.root_qs_logo_label.image = root_qs_logo_image  # keep a reference
        self.root_qs_logo_label.pack(expand=True, fill='both')

        self.build_main_menu()

    def get_base_window_superclass(self):
        return self.__class__.__bases__

    def build_main_menu(self):
        self.main_menu_bar = tk.Menu(self.window)
        self.window.config(menu=self.main_menu_bar)

        self.experiment_submenu_dict = {self.run_new_exp_txt: self.open_run_new_experiment_window,
                                        self.vizualize_exp_txt: self.open_vizual_exp_window}
        self.device_actions_submenu_dict = {AOM_str: self.open_AOM_device_action_window,
                                       GPIO_str: self.open_GPIO_device_action_window}
        self.snspd_submenu_dict = {self.snspds_detection_txt: self.open_SNSPD_window,
                                   self.open_snspds_storage_txt: self.open_SNSPD_storage}
        self.session_submenu_dict = {self.get_session_info_txt: self.get_session_info,
                                self.terminate_txt: self.terminate_session}
        self.help_submenu_dict = {self.open_document_txt: self.open_documentation}

        self.labels_submenus_dict = {self.experiment_str: self.experiment_submenu_dict,
                                self.device_action_str: self.device_actions_submenu_dict,
                                SNSPD_str: self.snspd_submenu_dict,
                                self.session_str: self.session_submenu_dict, self.help_str: self.help_submenu_dict}

        self.labels_menus_dict={}
        for submenu_label, submenu_dict in self.labels_submenus_dict.items():
            submenu=tk.Menu(self.main_menu_bar, tearoff=0)
            self.labels_menus_dict[submenu_label]=submenu
            #print(dir(self))
            self.main_menu_bar.add_cascade(label=submenu_label, menu=submenu)

            for option, cmd in submenu_dict.items():
                #added_submenu=tk.Menu(self.main_menu_bar, tearoff=0)
                #setattr(self, submenu_label, )

                submenu.add_command(label=option, command=cmd)


    def open_window(self, window_name, window_obj):
        #if not self.app.client.connect_flag and not window_name==self.session_win_name:
        #    super().show_err_msg(self.not_connected_client_title, self.not_connected_client_msg)
        if not hasattr(self, window_name):
            setattr(self, window_name, window_obj)
            self.open_windows_dict[window_name]=window_obj
        else:
            pass
            #todo implement forcing one instance of window as a time
            super().show_info_msg(self.window_opened_info_title, self.window_opened_info_msg)
        #print(dir(self))

    def open_run_new_experiment_window(self):
        self.open_window(self.run_exp_win_name, Run_New_Experiment(self))

    def get_file_template(self):
        print("get file template")

    def open_vizual_exp_window(self):
        self.open_window(self.view_exp_win_name, Vizualization_Window(self))

    def open_AOM_device_action_window(self):
        # if self.app.experiment:
        #     super().show_info_msg(self.dev_action_with_exp_err_title, self.dev_action_with_exp_err_msg)
        self.open_window(self.device_action_win_name, Device_Actions(self, AOM_str))

        #self.device_action=Device_Actions(self, AOM_str)

    def open_GPIO_device_action_window(self):
        self.open_window(self.device_action_win_name, Device_Actions(self, GPIO_str))

        #self.device_action=Device_Actions(self, GPIO_str)

    def open_SNSPD_window(self):
        self.open_window(self.snspd_win_name, SNSPD_Window(self))

    def open_SNSPD_storage(self):
        webbrowser.open_new(SNSPDs_data_storage)

    def get_session_info(self):
        self.open_window(self.session_win_name, Session_Window(self))

        self.session_window=Session_Window(self)

    def open_documentation(self):
        self.open_window(self.help_win_name, Help_Window(self))

    def report_bug(session_frame):
        print("report_bug")

    def connected_success_func(self):
        connect_flag=True
        self.get_window_obj(self.session_win_name).close_window()

    def connection_failed_func(self, con_error_title, con_error_msg):
        self.get_window_obj(self.session_win_name).window.destroy()
        connect_flag=False
        self.show_err_msg(con_error_title, con_error_msg)
        self.session_window = Session_Window(self, connect=True)

    def terminate_session(self):
        print("***print self.server_messages before terminate***")
        print("sent messages")
        print(self.client.sent_messages)
        print("recieved messages")
        print(self.client.received_messages)
        self.client.close_client()
        self.window.destroy()
        connect_flag=False
        print("session terminated ")

    def insert_to_queue(self, queue_item_obj):
        print(queue_item_obj)
        self.send_queue.put(queue_item_obj)


    def initial_experiment(self,input_dir, iteration_num, cycle_time):
        self.experiment=Experiment(self, input_dir, iteration_num, cycle_time)
        print("in initial experiment  {} {} {}".format(input_dir, iteration_num, cycle_time))

    def insert_stop_experiment_command_to_queue(self):
        print("in stop experiment command")
        current_queue_command = Queue_Item(stop_exp_name, {experiment_state_field_name : stop_exp_dec_op_code})
        self.app.insert_to_queue(current_queue_command)

    def start_experiment(self):
        if self.is_window_open(self.run_exp_win_name):
            self.get_window_obj(self.run_exp_win_name).change_widgets_after_start_exp()

    def stop_experiment(self):
        print("in stop experiment from ER app")

        if self.is_window_open(self.run_exp_win_name):
            print("in window open")
            self.get_window_obj(self.run_exp_win_name).change_widgets_after_stop_exp()

        if self.experiment:
            #self.experiment.stop_experiment_runner()
            delattr(self, 'experiment')
            self.experiment=None


    def is_window_open(self, window_name):
        return True if window_name in self.open_windows_dict.keys() else False

    def get_window_obj(self, win_name):
        return self.open_windows_dict[win_name]

    def restart_client(self):
        self.client.close_client()
        delattr(self, 'client')
        self.client = Client(self)

    def handle_input_cmd(self):
        print("handle input cmd")

    def handle_output_cmd(self):
        print("handle_output_cmd")

    def get_prev_user_selections_dict(self):
        return json.load(open(prev_user_selections_path))

    def update_user_selections_dict(self, new_dict):
        with open(prev_user_selections_path, "w") as jsonFile:
            json.dump(new_dict, jsonFile)


    def destroy_open_child_windows(self):
        print("in destroy open child")
        for window_name in self.windows_names_lst:
            if self.is_window_open(window_name):
                self.get_window_obj(window_name).window.destroy()
        self.windows_names_lst=[]

    def remove_window_obj(self, win_title):
        if win_title in self.windows_names_lst:
            if self.is_window_open(win_title):
                delattr(self, win_title)
                self.open_windows_dict.pop(win_title)

    def restart_app(self):
        if self.experiment:
            self.client.stop_exp_func()
        self.send_queue.queue.clear()
        self.restart_client()
        self.experiment=None
        self.destroy_open_child_windows()
        self.session_window = Session_Window(self, connect=True)

    def terminate_app(self):
        if self.experiment:
            self.client.stop_exp_func()
        self.send_queue.queue.clear()

def set_up_experiment_runner_application(curr_root):
    er_app = ER_Application(curr_root)
    curr_root.after(0, curr_root.withdraw)
    curr_root.mainloop()
    return er_app

def start_application():
    root = ctk.CTk()
    er_app = ER_Application(root)
    root.after(0, er_app.root.withdraw)
    return er_app

if __name__ == '__main__':
    #root = ctk.CTk()
    #set_up_experiment_runner_application(root)
    app=start_application()
    app.root.mainloop()
