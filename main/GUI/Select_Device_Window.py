from main.GUI.Base_Window import *
from main.GUI.Function_Setting import build_listbox_index_dict
class Select_Devices_Window(Base_Window):

    window_width = 500
    window_height = 400
    sticky="nsew"

    select_devices_label = "This window is used to select the required devices from the uploaded experiment"
    choose_AOM_txt="Choose AOM devices:"
    choose_GPIO_txt="Choose GPIO devices:"
    curr_title = 'Select Devices to View'
    select_button_txt='Select'

    no_selected_devices_err_msg="No devices were selected for view"
    selected_AOM_devices=[]
    selected_GPIO_devices=[]

    rows_weights_dict = {0: 1, 1: 1, 2: 1}
    columns_weights_dict = {0: 1, 1: 1}


    def __init__(self, vizual_exp_window_obj):
        print(" in init upload new experiment window")
        super().__init__(vizual_exp_window_obj.window)
        self.vizual_exp_window_obj = vizual_exp_window_obj

        window_label=super().build_label(self.window, self.select_devices_label, 0, 0, sticky="N")
        window_label.grid(columnspan=2)

        self.build_AOM_frame()
        self.build_GPIO_listbox()

        self.select_button = super().build_button(self.window, self.select_button_txt,
                                                            self.select_action_cmd, 3, 0, sticky="nsew")
        self.select_button.grid(columnspan=2)

    def build_AOM_frame(self):
        self.AOM_frame=super().build_frame(self.window, 1, 0)
        super().build_label(self.AOM_frame, self.choose_AOM_txt, 0, 0, padx=2, pady=2)
        index_lst=self.vizual_exp_window_obj.available_exp_devices_dict[AOM_str]
        print(self.vizual_exp_window_obj.available_exp_devices_dict[AOM_str])
        print("self.vizual_exp_window_obj.available_exp_devices_dict[AOM_str]")


        self.AOM_index_dict=build_listbox_index_dict(index_lst, start_val=0)

        self.AOM_index_listbox = super().build_listbox(self.AOM_frame, index_lst, 1, 0,  [i-1 for i in self.selected_AOM_devices],
                                                   self.handle_choose_AOM_index_event, selected=False)


        AOM_index_scrollbar = ctk.CTkScrollbar(self.AOM_frame, orientation='vertical',
                                       command=self.AOM_index_listbox.yview)
        AOM_index_scrollbar.grid(row=1, column=1, sticky='ns')
        AOM_index_scrollbar['yscrollcommand'] = AOM_index_scrollbar.set

        selected_curselection = self.AOM_index_listbox.curselection()
        print("selected_curselection")
        print(selected_curselection)
        self.selected_AOM_index_lst = self.get_dict_keys_by_val_lst(self.AOM_index_dict, selected_curselection)
        print("self.selected_AOM_index_lst")
        print( self.selected_AOM_index_lst)
        super().change_widget_config(self.AOM_index_listbox, "selectmode", "multiple")

    def handle_choose_AOM_index_event(self, event):
        selected_curselection = self.AOM_index_listbox.curselection()
        self.selected_AOM_index_lst = self.get_dict_keys_by_val_lst(self.AOM_index_dict, selected_curselection)

    def get_dict_keys_by_val_lst(self, dict, vals_list):
        print("get dict keys by val lst")
        print("dict")
        print(dict)
        print("vals_list")
        print(vals_list)
        return [k for k, v in dict.items() if v in vals_list]

    def build_GPIO_listbox(self):

        self.GPIO_frame = super().build_frame(self.window, 1, 1)
        super().build_label(self.GPIO_frame, self.choose_GPIO_txt, 0, 0, padx=2, pady=2)
        index_lst = self.vizual_exp_window_obj.available_exp_devices_dict[GPIO_str]
        print("self.vizual_exp_window_obj.available_exp_devices_dict[GPIO_str]")
        print(self.vizual_exp_window_obj.available_exp_devices_dict[GPIO_str])

        print(index_lst)
        self.GPIO_index_dict=build_listbox_index_dict(index_lst, start_val=0)

        self.GPIO_index_listbox = super().build_listbox(self.GPIO_frame, index_lst, 1, 0,
                                                       [i - 1 for i in self.selected_GPIO_devices],
                                                       self.handle_choose_GPIO_index_event, selected=False)

        GPIO_index_scrollbar = ctk.CTkScrollbar(self.GPIO_frame, orientation='vertical',
                                               command=self.AOM_index_listbox.yview)
        GPIO_index_scrollbar.grid(row=1, column=1, sticky='ns')
        GPIO_index_scrollbar['yscrollcommand'] = GPIO_index_scrollbar.set

        selected_curselection = self.GPIO_index_listbox.curselection()
        print("selected_curselection")
        print(selected_curselection)
        self.selected_GPIO_index_lst = self.get_dict_keys_by_val_lst(self.GPIO_index_dict, selected_curselection)
        print("self.selected_GPIO_index_lst")
        print( self.selected_GPIO_index_lst)
        super().change_widget_config(self.GPIO_index_listbox, "selectmode", "multiple")

    def handle_choose_GPIO_index_event(self, event):
        selected_curselection = self.GPIO_index_listbox.curselection()
        self.selected_GPIO_index_lst = self.get_dict_keys_by_val_lst(self.GPIO_index_dict,selected_curselection)

    def select_action_cmd(self):
        #TODO add here conversion from index in listbox to the channel
        if not self.selected_AOM_index_lst and not self.selected_GPIO_index_lst:
            super().show_err_msg(self.no_selected_devices_err_msg, self.no_selected_devices_err_msg)
        else:

            self.vizual_exp_window_obj.change_device_info_after_select(self.selected_AOM_index_lst, self.selected_GPIO_index_lst)
            self.window.destroy()
