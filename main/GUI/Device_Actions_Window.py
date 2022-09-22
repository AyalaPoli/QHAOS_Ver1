import tkinter as tk
from tkinter import font
import customtkinter as ctk
from tkinter.messagebox import askokcancel
from main.GUI.GUI_params import *
from main.GUI.Device_Object import *

from main.GUI.Base_Window import Base_Window
from main.GUI.Queue_Item import *
from main.GUI.Function_Setting import Parameter_Entry


class Device_Actions(Base_Window):
    curr_title = "Single Device Action"
    window_width = 1100
    window_height = 400
    device_actions_window_msg = "This window execute single and immediate command on the device"
    running_exp_note="\nNote: an experiment is currently running - actions may be overridden"


    rows_weights_dict = {0: 1, 1: 15}
    columns_weights_dict = {0: 1, 1: 1, 2: 1, 3: 1, 4: 1}

    label_font_size = 10

    change_device_button_txt = "Change Device"

    choose_device_type_txt = "Device"
    choose_device_index_txt = "Device Index"
    choose_function_txt = "Function To Execute"
    choose_parameters_txt = "Function Parameters"

    params_range_msg_format_AOM = "Valid values are in range [{}-{}]"
    params_range_msg_format_GPIO = "Valid values are 0 or 1"
    invalid_msg_within_entry = "Invalid value, try again"

    apply_action_title = "Apply Action"
    apply_action_txt = "Your action request was accepted"
    initial_action_label_txt=""

    select_button_txt = "Apply"
    select_action_msgbox_title = "Select Device Action Parameters"
    select_action_label_format = "The action was sent: \nDevice: {}\nChannels: {}\nFunction: {}\n{}" \

    invalid_param_title = "Invalid Parameter Value\n"
    invalid_param_msg = "The following parameters values are invalid\n\n"
    invalid_device_type_format = "Invalid device type: {}\n"
    invalid_channels_format = "Invalid channel\\s: {}\nAll channel should be in {}\n"
    invalid_AOM_param_format = "Invalid parameter value: {}={}, should be in range: {}-{}\n"
    invalid_GPIO_parameter_range_format = "Invalid parameter value:\n{}={}. \nShould be one of the values: {}\n"
    invalid_empty_entry_title = "Value has not been specified"
    invalid_empty_entry_msg = "Value has not been specified for non of the parameters: {}"

    first_window_build = True
    selected_indexes_lst = []

    set_GPIO_name = "SET_GPIO"
    set_AOM_name = "SET_AOM"

    def __init__(self, app, device_type):
        self.app = app
        super().__init__(app.root)
        self.device_obj = Device_Object(device_type)

        if self.app.experiment:
            self.device_actions_window_msg+=self.running_exp_note

        dev_action_label = super().build_label(self.window, self.device_actions_window_msg, 0, 0, sticky="N")
        dev_action_label.grid(columnspan=5)

        self.build_choose_device_type_frame()
        self.build_choose_device_index_frame()
        self.build_choose_function_frame()
        self.build_enter_parameters_frame()
        self.build_buttons_frame()

    def build_choose_device_type_frame(self):

        self.choose_device_type_frame = super().build_frame(self.window, 1, 0)
        super().change_widget_config(self.choose_device_type_frame, "borderwidth", 1)

        self.choose_device_type_label = super().build_label(self.choose_device_type_frame, self.choose_device_type_txt,
                                                            0, 0, 0, 0)
        # self.choose_device_type_label=tk.Label(self.choose_device_type_frame, self.choose_device_type_txt, 0, 0)
        super().change_widget_config(self.choose_device_type_label, "font", (default_font, self.label_font_size))

        self.devices_types_listbox_index_dict = build_listbox_index_dict(device_types_lst)
        selected = self.devices_types_listbox_index_dict[self.device_obj.device_type]-1
        self.devices_listbox = super().build_listbox(self.choose_device_type_frame, device_types_lst, 1, 0,
                                                     selected, self.handle_choose_device_type_listbox)

        #self.devices_listbox.bind("<<ListboxSelect>>", self.device_listbox_cmd)

        #self.change_device_button = super().build_button(self.choose_device_type_frame, self.change_device_button_txt,
        #                                                 self.change_device_button_cmd, 2, 0, sticky="N")

    def handle_choose_device_type_listbox(self, event):

        if self.first_window_build:

            print("in self.first_window_build")
            #self.prev_dev_type = self.inserterd_device_type
            #self.inserterd_device_type = self.devices_listbox.get(tk.ACTIVE)
            self.inserterd_device_type = self.devices_listbox.get(tk.ACTIVE)
            self.first_window_build = False


        else:
            print("in else")
            self.prev_dev_type=self.inserterd_device_type
            self.inserterd_device_type = self.devices_listbox.get(tk.ACTIVE)
            self.device_obj = Device_Object(self.inserterd_device_type)

            if self.prev_dev_type!=self.inserterd_device_type:
                self.selected_indexes_lst = []
                self.index_listbox.selection_clear(0, 'end')
                self.functions_listbox.selection_clear(0, 'end')
                for widget in self.parameters_entries_obj_lst:
                    widget.destroy()
                # for widget in self.enter_parameters_frame.winfo_children():
                #     widget.destroy()
                self.enter_parameters_frame.destroy()
                parameters_entries_obj_lst=[]

                self.device_obj = Device_Object(self.inserterd_device_type)
                self.build_choose_device_index_frame()
                self.build_choose_function_frame()
                self.build_enter_parameters_frame()
                self.action_label.configure(text=self.initial_action_label_txt)

    #def device_listbox_cmd(self, event):

    def change_device_button_cmd(self):
        self.inserterd_device_type = self.devices_listbox.get(tk.ACTIVE)

        if self.first_window_build:
            self.first_window_build = False

        else:
            self.selected_indexes_lst = []
            self.index_listbox.selection_clear(0, 'end')
            self.functions_listbox.selection_clear(0, 'end')
            self.parameters_entries_obj_lst = []
        for widget in self.enter_parameters_frame.winfo_children():
            widget.destroy()
        self.enter_parameters_frame.destroy()

        self.device_obj = Device_Object(self.inserterd_device_type)
        self.build_choose_device_index_frame()
        self.build_choose_function_frame()
        self.build_enter_parameters_frame()
        #self.build_buttons_frame()

    def build_choose_device_index_frame(self):
        self.devices_index_listbox_index_dict = \
            build_listbox_index_dict(self.device_obj.app_to_physical_index_dict.keys())
        print("devices_index_listbox_index_dict")
        print(self.devices_index_listbox_index_dict)
        self.choose_device_index_frame = super().build_frame(self.window, 1, 1)
        super().change_widget_config(self.choose_device_type_frame, "borderwidth", 1)

        self.choose_device_index_label = super().build_label(self.choose_device_index_frame,
                                                             self.choose_device_index_txt, 0, 0, 0, 0)
        super().change_widget_config(self.choose_device_index_label, "font", (default_font, self.label_font_size))

        self.build_device_index_listbox()

    def build_device_index_listbox(self):

        index_lst = list(self.devices_index_listbox_index_dict.keys())
        # if not len(self.selected_indexes_lst):
        #     default_device_index = self.get_default_device_index()
        #     self.selected_indexes_lst = [self.devices_index_listbox_index_dict[default_device_index]]

        #self.selected_indexes_lst=[]

        self.index_listbox = super().build_listbox(self.choose_device_index_frame, index_lst, 1, 0,
                                                   [i-1 for i in self.selected_indexes_lst],
                                                   self.handle_choose_device_index_event, selected=False)

        index_scrollbar = ctk.CTkScrollbar(self.choose_device_index_frame, orientation='vertical',
                                       command=self.index_listbox.yview)
        index_scrollbar.grid(row=1, column=1, sticky='ns')
        self.index_listbox['yscrollcommand'] = index_scrollbar.set

        selected_curselection = self.index_listbox.curselection()
        self.selected_indexes_lst = [i + 1 for i in selected_curselection]
        super().change_widget_config(self.index_listbox, "selectmode", "multiple")



    def handle_choose_device_index_event(self, event):
        selected_curselection = self.index_listbox.curselection()
        self.selected_indexes_lst = [i+1 for i in selected_curselection]

    def get_default_device_index(self):
        return min(self.devices_index_listbox_index_dict.keys())

    def build_choose_function_frame(self):
        self.choose_function_frame = super().build_frame(self.window, 1, 2)
        super().change_widget_config(self.choose_function_frame, "borderwidth", 1)

        self.choose_func_index_label = super().build_label(self.choose_function_frame, self.choose_function_txt, 0, 0, 0, 0)
        super().change_widget_config(self.choose_func_index_label, "font", (default_font, self.label_font_size))

        self.build_function_listbox()

    def build_function_listbox(self):
        self.functions_listbox_index_dict = build_listbox_index_dict(self.device_obj.functions_params_dict.keys())

        func_lst = list(self.functions_listbox_index_dict.keys())
        selected = self.functions_listbox_index_dict[self.device_obj.current_function]
        self.functions_listbox = super().build_listbox(self.choose_function_frame, func_lst, 1, 0,
                                                       selected, self.handle_choose_function_event)
        #Todo: check if -1 is needed

    def handle_choose_function_event(self, event):
        self.device_obj.current_function = self.functions_listbox.get(tk.ACTIVE)
        self.device_obj.update_current_params_by_function()
        self.build_enter_parameters_frame()

    def build_enter_parameters_frame(self):
        self.enter_parameters_frame = super().build_frame(self.window, 1, 3)
        super().change_widget_config(self.choose_function_frame, "borderwidth", 1)

        choose_parameter_label = super().build_label(self.enter_parameters_frame, self.choose_parameters_txt, 0, 0, 0, 0)
        super().change_widget_config(choose_parameter_label, "font", (default_font, self.label_font_size))

        self.parameters_entries_obj_lst = []

        curr_params_list = self.device_obj.get_params_lst()
        index_lst = range(1, len(self.device_obj.get_params_lst()) * 2, 2)

        for self.param, index in zip(curr_params_list, index_lst):
            validation_msg = self.get_parameters_validation_msg()
            self.curr_param_entry_obj = Parameter_Entry(self.enter_parameters_frame, self.param, index, self.sticky,
                                                        super().label_padx, super().label_pady, validation_msg, self.device_obj.val_type,
                                                        default_val="")
            self.parameters_entries_obj_lst.append(self.curr_param_entry_obj)
            self.curr_param_entry_obj.entry.bind("<Return>", self.get_parameter_value)

    def get_parameters_validation_msg(self):
        if self.device_obj.is_AOM_device():
            self.curr_param_min_val, self.curr_param_max_val = self.device_obj.get_AOM_param_value_range(self.param)
            print("self.curr_param_min_val, self.curr_param_max_val")
            print(self.curr_param_min_val, self.curr_param_max_val)
            return self.params_range_msg_format_AOM.format(self.curr_param_min_val, self.curr_param_max_val)
        elif self.device_obj.is_GPIO_device():
            return self.params_range_msg_format_GPIO

    def get_parameter_valid_range(self):
        min_val = self.device_obj.function_parameters_range_dict[self.param][0]
        max_val = self.device_obj.function_parameters_range_dict[self.param][1]
        return min_val, max_val

    def get_parameter_value(self):

        param_input_value = self.curr_param_entry_obj.param_intval.get()

        self.curr_param_entry_obj.param_input_value = param_input_value

        # if all of the parameters were filled
        if len(self.parameters_entries_obj_lst) == len(self.device_obj.current_params_lst):
            self.select_button["state"] = tk.NORMAL

    def build_buttons_frame(self):
        self.buttons_frame = super().build_frame(self.window, 1, 4)
        super().change_widget_config(self.buttons_frame, "borderwidth", 1)

        self.select_button = super().build_button(self.buttons_frame, self.select_button_txt,
                                                  self.select_action_cmd, 1, 0)
        self.action_label = super().build_label(self.buttons_frame, self.initial_action_label_txt, 2, 0, sticky="W")

    def get_values_from_params_entries(self):
        msg=""
        empty_params_count=0
        for entry_obj in self.parameters_entries_obj_lst:
            if entry_obj.is_empty_entry():
            #if not entry_obj.param_intval.get():
                empty_params_count+=1
            else:
                entry_obj.param_input_value = entry_obj.param_intval.get()
        if empty_params_count==len(self.parameters_entries_obj_lst):
            msg += self.invalid_empty_entry_msg.format(", ".join([e.param_name for e in self.parameters_entries_obj_lst]))
        return msg

    def get_func_params_as_str(self):
        params_str = ""

        for entry_obj in self.parameters_entries_obj_lst:
            params_str += "\n{}: {}".format(entry_obj.param_name, entry_obj.param_input_value)
        return params_str

    def get_channel_as_str(self):
        str = ""
        print("selected_indexes_lst")
        print(self.selected_indexes_lst)
        for selected_index in self.selected_indexes_lst:
            for app_chan, index_chan in self.devices_index_listbox_index_dict.items():
                if selected_index == index_chan:
                    str += " {} ".format(app_chan)
        return str

    def select_action_cmd(self):
        if invalid_str := self.get_values_from_params_entries():
            self.action_label.configure(text=invalid_str)
            return
        if invalid_str := self.invalid_parameters_values():
            self.action_label.configure(text=invalid_str)
        else:
            dev_type = self.device_obj.device_type
            channels_str = self.get_channel_as_str()
            func = self.device_obj.current_function
            params_str = self.get_func_params_as_str()
            select_action_txt = self.select_action_label_format.format(dev_type, channels_str, func, params_str)
            self.action_label.configure(text=select_action_txt)
            self.apply_device_action()

    def select_action_cmd_old(self):
        if invalid_str := self.get_values_from_params_entries():
            askokcancel(title=self.invalid_empty_entry_title,message=invalid_str)
            return

        if invalid_str := self.invalid_parameters_values():
            askokcancel(title=self.invalid_param_title, message=invalid_str)
            return

        else:
            dev_type = self.device_obj.device_type
            channels_str = self.get_channel_as_str()
            func = self.device_obj.current_function
            params_str = self.get_func_params_as_str()
            select_action_msgbox_txt = self.select_action_label_format.format(dev_type, channels_str, func, params_str)
            select_action_flag = askokcancel(title=self.select_action_msgbox_title, message=select_action_msgbox_txt)
            if select_action_flag:
                tk.messagebox.askokcancel(title=self.apply_action_title, message=self.apply_action_txt)
                self.apply_device_action()

    def invalid_parameters_values(self):
        invalid_values_str = ""
        if self.device_obj.device_type not in [AOM_str, GPIO_str]:
            invalid_values_str += self.invalid_device_type_format.format(self.device_obj.device_type)
        if not all(elem in self.device_obj.app_to_physical_index_dict.keys() for elem in self.selected_indexes_lst):
            invalid_values_str += self.invalid_channels_format.format(self.selected_indexes_lst,
                                                                      self.device_obj.app_to_physical_index_dict.keys())
        for entry_obj in self.parameters_entries_obj_lst:
            print(" entry_obj.param_input_value")
            print(entry_obj.param_input_value)
            if entry_obj.param_input_value:
                curr_val = entry_obj.param_input_value
                if self.device_obj.is_AOM_device():
                    min_val, max_val = self.device_obj.get_AOM_param_value_range(entry_obj.param_name)
                    if curr_val < min_val or curr_val > max_val:
                        invalid_values_str += self.invalid_AOM_param_format.format(entry_obj.param_name, curr_val, min_val,
                                                                                   max_val)
                if self.device_obj.is_GPIO_device():
                    valid_values_lst = self.device_obj.get_GPIO_valid_values_lst(entry_obj.param_name)
                    if curr_val not in valid_values_lst:
                        invalid_values_str += self.invalid_GPIO_parameter_range_format.format(entry_obj.param_name,
                                                                                              curr_val, valid_values_lst)
        return invalid_values_str

    def initial_to_empty_entry_values(self):
        for entry_obj in self.parameters_entries_obj_lst:
            entry_obj.param_input_value=None

    def apply_device_action(self):

        cmd_name = self.set_AOM_name if self.device_obj.device_type == AOM_str else self.set_GPIO_name

        for sel_chanel in self.selected_indexes_lst:
            print(sel_chanel)
            cmd_dict = {channel_index_field_name: int(sel_chanel)}
            parames_names_val_dict = {entry_obj.param_name: entry_obj.param_input_value for entry_obj in
                                      self.parameters_entries_obj_lst if not entry_obj.is_empty_entry()}
            if cmd_name == self.set_GPIO_name:
                print("in set GPIO")
                print("in parames_names_val_dict")
                print(parames_names_val_dict)
                cmd_dict[set_function_param_str] = int(parames_names_val_dict[set_function_param_str])
            else:
                amplitude_flag, frequency_flag = 0, 0
                print("parames_names_val_dict")
                print(parames_names_val_dict)
                if amplitude_str in parames_names_val_dict.keys():
                    cmd_dict[first_param_field_name] = float(parames_names_val_dict[amplitude_str])
                    amplitude_flag = only_amp_to_config
                    if frequency_str in parames_names_val_dict.keys():
                        cmd_dict[second_param_field_name] = float(parames_names_val_dict[frequency_str])
                        frequency_flag = only_freq_to_config
                else:
                    cmd_dict[first_param_field_name] = float(parames_names_val_dict[frequency_str])
                    frequency_flag = only_freq_to_config
                print("amplitude_flag {} frequency_flag {} ".format(amplitude_flag,frequency_flag))
                cmd_dict[params_config_field_name] = amplitude_flag + frequency_flag

            current_queue_command = Queue_Item(cmd_name, cmd_dict)
            self.app.insert_to_queue(current_queue_command)
        self.window.update()
            #self.app.client.execute_command_from_queue()
        #self.initial_to_empty_entry_values()
