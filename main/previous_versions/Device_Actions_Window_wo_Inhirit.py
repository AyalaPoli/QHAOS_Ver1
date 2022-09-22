import tkinter as tk
from tkinter import font
from tkinter.messagebox import askokcancel
from main.GUI.GUI_params import *
from main.GUI.Device_Object import *

class Device_Actions_Old():

    device_actions_title = "Single Device Action"
    window_width = 1200
    window_height = 400
    device_actions_window_msg = "This window execute single and immediate command on the device"
    device_actions_frames_padx = 10
    device_actions_frames_pady = 10
    buttons_font_size=10

    change_device_button_txt="Change Device"

    choose_device_type_txt = "Device"
    choose_device_index_txt = "Device Index"
    choose_function_txt = "Function To Execute"
    choose_parameters_txt= "Function Parameters"

    params_range_msg_format_AOM="Valid values are in range [{}-{}]"
    params_range_msg_format_GPIO="Valid values are 0 or 1"
    invalid_msg_within_entry="Invalid value, try again"

    apply_action_title = "Apply Action"
    apply_action_txt = "Your action request was accepted"

    select_button_txt="Select"
    select_action_msgbox_title="Select Device Action Parameters"
    select_action_msgbox_format="The following parameters were selected:\nDevice: {}\nChannels: {}\nFunction: {}\nParameters:{}" \
                             "\nDo you want to continue?"


    sticky="nw"

    first_window_build=True
    selected_indexes_lst=[]

    label_font_size=10


    def __init__(self, root, device_type):
        self.root=root
        self.window=tk.Toplevel(self.root)
        self.title = self.device_actions_title
        self.buttons_font = tk.font.Font(size=self.buttons_font_size)

        self.define_window_position()

        self.window.iconbitmap(icon_file)
        self.buttons_font = tk.font.Font(size=self.buttons_font_size)
        self.configure_grid_weights()
        self.device_obj=Device_Object(device_type)

        # Top frame of information message
        new_experiment_label=tk.Label(self.window, text=self.device_actions_window_msg, bg='white')
        new_experiment_label.grid(row=0, column=0, sticky="N", columnspan=5)

        device_actions_frames_padx = 10
        device_actions_frames_pady = 10

        self.build_choose_device_type_frame()
        self.build_choose_device_index_frame()
        self.build_choose_function_frame()
        self.build_enter_parameters_frame()
        self.build_buttons_frame()

    def build_listbox_index_dict(self,input_lst):
        return {curr_input:i for curr_input,i in zip(input_lst, range(len(input_lst)))}

    def define_window_position(self):
        screen_width=self.window.winfo_screenwidth()
        screen_height=self.window.winfo_screenheight()
        center_x = int(screen_width / 2 - self.window_width / 2)
        center_y = int(screen_height / 2 - self.window_height / 2)
        self.window.geometry(f'{self.window_width}x{self.window_height}+{center_x}+{center_y}')

    def configure_grid_weights(self):
        self.window.columnconfigure(0, weight=1)
        self.window.columnconfigure(1, weight=1)
        self.window.columnconfigure(2, weight=1)
        self.window.columnconfigure(3, weight=1)
        self.window.columnconfigure(4, weight=1)
        self.window.rowconfigure(0, weight=1)
        self.window.rowconfigure(1, weight=15)

    def build_choose_device_type_frame(self):
        self.devices_types_listbox_index_dict = self.build_listbox_index_dict(device_types_lst)
        # {AOM_str:0, GPIO_str:1}
        print("self.devices_types_listbox_index_dict")
        print(self.devices_types_listbox_index_dict)
        self.choose_device_type_frame = tk.Frame(self.window, borderwidth=1)
        self.choose_device_type_frame.grid(row=1, column=0, sticky=self.sticky,
                             padx=self.device_actions_frames_padx, pady=self.device_actions_frames_pady)

        choose_device_type_label=tk.Label(self.choose_device_type_frame, text=self.choose_device_type_txt,
                                          font=(default_font, self.label_font_size))

        choose_device_type_label.grid(row=0, column=0, sticky=self.sticky,
                                      padx=self.device_actions_frames_padx, pady=self.device_actions_frames_pady)


        devices_list_items = tk.StringVar(value = device_types_lst)
        self.devices_listbox=tk.Listbox(master=self.choose_device_type_frame, listvariable=devices_list_items, exportselection=False)
        self.devices_listbox.grid(row=1, column=0, sticky=self.sticky,
                                      padx=self.device_actions_frames_padx, pady=self.device_actions_frames_pady)
        print("(self.devices_types_listbox_index_dict[self.device_obj.device_type]")
        print(self.devices_types_listbox_index_dict[self.device_obj.device_type])
        self.devices_listbox.select_set(self.devices_types_listbox_index_dict[self.device_obj.device_type])
        #self.devices_listbox.activate(self.devices_types_listbox_index_dict[self.device_obj.device_type])
        #self.devices_listbox.select_set(self.devices_types_listbox_index_dict[self.device_obj.device_type])

        self.devices_listbox.bind('<<ListboxSelect>>', self.handle_choose_device_type_frame)

        self.change_device_button=tk.Button(self.choose_device_type_frame, text=self.change_device_button_txt,
                                            command=self.change_device_button_cmd)
        self.change_device_button['font'] = self.buttons_font
        self.change_device_button.grid(row=2, column=0, sticky="N",
                                     padx=self.device_actions_frames_padx, pady=self.device_actions_frames_pady)


    def handle_choose_device_type_frame(self, event):
        self.inserterd_device_type = self.devices_listbox.get(tk.ACTIVE)
        print("nothing is done here handle_choose_device_type_frame")
        #print("inserterd_device_type")
        #print(inserterd_device_type)
        #if inserterd_device_type!=self.device_obj.device_type:
        #    self.build_device_index_listbox()

    def change_device_button_cmd(self):
        self.inserterd_device_type = self.devices_listbox.get(tk.ACTIVE)

        if self.first_window_build:
            self.first_window_build=False

        else:
            self.selected_indexes_lst=[]
            self.index_listbox.selection_clear(0, 'end')
            self.functions_listbox.selection_clear(0, 'end')
            self.parameters_entries_obj_lst=[]

        self.device_obj=Device_Object(self.inserterd_device_type)
        self.build_choose_device_index_frame()
        self.build_choose_function_frame()
        self.enter_parameters_frame.destroy()
        self.build_enter_parameters_frame()

    def build_choose_device_index_frame(self):
        self.devices_index_listbox_index_dict = self.build_listbox_index_dict(self.device_obj.app_to_physical_index_dict.keys())

        self.choose_device_index_frame = tk.Frame(self.window, borderwidth=1)
        self.choose_device_index_frame.grid(row=1, column=1, sticky=self.sticky,
                             padx=self.device_actions_frames_padx, pady=self.device_actions_frames_pady)


        choose_device_index_label=tk.Label(self.choose_device_index_frame, text=self.choose_device_index_txt, font=(default_font, self.label_font_size))

        choose_device_index_label.grid(row=0, column=0, sticky=self.sticky,
                                      padx=self.device_actions_frames_padx, pady=self.device_actions_frames_pady)

        self.build_device_index_listbox()

    def build_device_index_listbox(self):

        devices_index_items=tk.StringVar(value=list(self.devices_index_listbox_index_dict.keys()))
        self.index_listbox=tk.Listbox(master=self.choose_device_index_frame, listvariable=devices_index_items,
                                        selectmode="multiple", exportselection=False)
        self.index_listbox.grid(row=1, column=0, sticky=self.sticky,
                                      padx=self.device_actions_frames_padx, pady=self.device_actions_frames_pady)
        print(self.selected_indexes_lst)
        if not len(self.selected_indexes_lst):
            default_device_index=self.get_default_device_index()
            self.selected_indexes_lst=[self.devices_index_listbox_index_dict[default_device_index]]
            self.index_listbox.select_set(self.devices_index_listbox_index_dict[default_device_index])
        index_scrollbar= tk.Scrollbar(self.choose_device_index_frame, orient='vertical',
                     command=self.index_listbox.yview)
        self.index_listbox['yscrollcommand'] = index_scrollbar.set

        self.index_listbox.bind('<<ListboxSelect>>', self.handle_choose_device_index_event)
        index_scrollbar.grid(row=1, column=1, sticky='ns')

    def handle_choose_device_index_event(self, event):
        selected_curselection = self.index_listbox.curselection()
        self.selected_indexes_lst=[i for i in selected_curselection]
        print(self.selected_indexes_lst)
        print("self.selected_indexes_lst")

    def get_default_device_index(self):
        return min(self.devices_index_listbox_index_dict.keys())

    def build_choose_function_frame(self):
        self.choose_function_frame = tk.Frame(self.window, borderwidth=1)
        self.choose_function_frame.grid(row=1, column=2, sticky=self.sticky,
                             padx=self.device_actions_frames_padx, pady=self.device_actions_frames_pady)


        choose_function_index_label=tk.Label(self.choose_function_frame, text=self.choose_function_txt, font=(default_font, self.label_font_size))

        choose_function_index_label.grid(row=0, column=0, sticky=self.sticky,
                                      padx=self.device_actions_frames_padx, pady=self.device_actions_frames_pady)


        self.build_function_listbox()

    def build_function_listbox(self):
        self.functions_listbox_index_dict = self.build_listbox_index_dict(self.device_obj.functions_params_dict.keys())

        functions_items=tk.StringVar(value=list(self.functions_listbox_index_dict.keys()))

        self.functions_listbox=tk.Listbox(self.choose_function_frame, listvariable=functions_items, exportselection=False)

        self.functions_listbox.grid(row=1, column=0,  sticky=self.sticky,
                                      padx=self.device_actions_frames_padx, pady=self.device_actions_frames_pady)
        print("self.functions_listbox_index_dict[self.device_obj.current_function]")
        self.functions_listbox.select_set(self.functions_listbox_index_dict[self.device_obj.current_function])

        self.functions_listbox.bind('<<ListboxSelect>>', self.handle_choose_function_event)

    def handle_choose_function_event(self, event):
        self.device_obj.current_function=self.functions_listbox.get(tk.ACTIVE)
        self.device_obj.update_current_params_by_function()
        self.build_enter_parameters_frame()

        #if curr_selected_func!=self.device_obj.default_function:
        #    self.build_function_listbox()


    def build_enter_parameters_frame(self):

        self.enter_parameters_frame = tk.Frame(self.window, borderwidth=1)
        self.enter_parameters_frame.grid(row=1, column=3, sticky=self.sticky,
                             padx=self.device_actions_frames_padx, pady=self.device_actions_frames_pady)

        choose_parameter_label=tk.Label(self.enter_parameters_frame, text=self.choose_parameters_txt, font=(default_font, self.label_font_size))
        choose_parameter_label.grid(row=0, column=0, sticky=self.sticky,
                                      pady=self.device_actions_frames_pady)

        #self.param_labels_dict = {} to delete
        self.parameters_entries_obj_lst=[]

        curr_params_list=self.device_obj.get_params_lst()
        index_lst=range(1, len(self.device_obj.get_params_lst())*2,2)

        for self.param, index in zip(curr_params_list, index_lst):
            validation_msg=self.get_parameters_validation_msg()
            self.curr_param_entry_obj=Parameter_Entry(self.enter_parameters_frame, self.param, index, self.sticky,
                                                      self.device_actions_frames_pady, validation_msg)
            self.parameters_entries_obj_lst.append(self.curr_param_entry_obj)
            self.curr_param_entry_obj.entry.bind("<Return>", self.get_parameter_value)

    def get_parameters_validation_msg(self):
        if self.device_obj.is_AOM_device():
            self.curr_param_min_val, self.curr_param_max_val=self.get_parameter_valid_range()
            print(self.curr_param_min_val, self.curr_param_max_val)
            return self.params_range_msg_format_AOM.format(self.curr_param_min_val, self.curr_param_max_val)
        elif self.device_obj.is_GPIO_device():
            return self.params_range_msg_format_GPIO

    def get_parameter_valid_range(self):
        min_val=self.device_obj.function_parameters_range_dict[self.param][0]
        max_val=self.device_obj.function_parameters_range_dict[self.param][1]
        return min_val,max_val

    def get_parameter_value(self):
        #input_param_val=self.curr_param_entry_obj.param_value.get()
        input_param_val=self.curr_param_entry_obj.param_intval.get()
        if (input_param_val<self.curr_param_min_val) and (input_param_val>self.curr_param_max_val):
            #self.inserted_params_values_dict[self.param]=self.curr_param_val.get()
            self.curr_param_entry_obj.param_value.set(self.invalid_msg_within_entry)

        #if all of the parameters were filled
        if len(self.parameters_entries_obj_lst)==len(self.device_obj.current_params_lst):
            self.select_button["state"] = tk.NORMAL

    def build_buttons_frame(self):
        self.buttons_frame = tk.Frame(self.window, borderwidth=1)
        self.buttons_frame.grid(row=1, column=4, sticky=self.sticky,
                             padx=self.device_actions_frames_padx, pady=self.device_actions_frames_pady)

        self.select_button=tk.Button(self.buttons_frame, text=self.select_button_txt,
                                            command=self.select_action_msgbox_cmd)
        self.select_button['font'] = self.buttons_font
        self.select_button.grid(row=1, column=0, sticky=self.sticky,
                                     padx=self.device_actions_frames_padx, pady=self.device_actions_frames_pady)

        #self.cancel_button=tk.Button(self.buttons_frame, text=self.cancel_button_txt,
#                                            command=self.cancel_device_action)
        #self.cancel_button['font'] = self.buttons_font
        #self.cancel_button.grid(row=1, column=0, sticky=self.sticky,
#                                     padx=self.run_experiment_frames_padx, pady=self.run_experiment_frames_pady)


    def get_values_from_params_entries(self):
        for entry_obj in self.parameters_entries_obj_lst:
            entry_obj.param_input_value=entry_obj.param_intval.get()


    def get_func_params_as_str(self):
        params_str=""

        for entry_obj in self.parameters_entries_obj_lst:
                    params_str+="\n\t{}: {}".format(entry_obj.param_name, entry_obj.param_input_value)
        return params_str

    def get_channel_as_str(self):
        str=""
        print("selected_indexes_lst")
        print(self.selected_indexes_lst)
        for selected_index in self.selected_indexes_lst:
            for app_chan, index_chan in self.devices_index_listbox_index_dict.items():
                if selected_index==index_chan:
                    str+=" {} ".format(app_chan)
        return str

    def select_action_msgbox_cmd(self):
        dev_type=self.device_obj.device_type
        channels_str=self.get_channel_as_str()
        func=self.device_obj.current_function
        self.get_values_from_params_entries()

        params_str=self.get_func_params_as_str()

        print(channels_str)
        print(self.get_func_params_as_str)
        select_action_msgbox_txt=self.select_action_msgbox_format.format(dev_type, self.get_channel_as_str(),
                                                                         func, params_str)
        print(select_action_msgbox_txt)
        select_action_flag=askokcancel(title=self.select_action_msgbox_title, message=select_action_msgbox_txt)
        if select_action_flag:
            tk.messagebox.showinfo(title=self.apply_action_title, message=self.apply_action_txt)
            self.apply_device_action()

    def apply_device_action(self):
        dev_type=self.device_obj.device_type
        dev_channel=self.selected_indexes_lst
        func=self.device_obj.current_function
        #params_names_values=self.inserted_params_values_dict

        #send_device_action_to_control(self.device_obj.device_type, self.selected_indexes, self.selected_function,
        #                              self.inserted_params_values_dict)
        #def send_device_action_to_control(device_type, device_index_lst, func_str, params_vals_dict): for dev_i in device_index_lst

        set_GPIO_name = "SET_GPIO"
        set_AOM_name = "SET_AOM"

        cmd_name=set_AOM_name if self.dev_type==AOM_str else GPIO_str
        for sel_chanel in self.selected_indexes_lst:
            parames_names_val_dict = {entry_obj.name: entry_obj.val for entry_obj in self.parameters_entries_obj_lst}

    #def cancel_device_action(self):
    #    self.window.destroy()
