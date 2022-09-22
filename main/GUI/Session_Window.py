import tkinter as tk
from main.GUI.GUI_params import *
from main.GUI.Base_Window import *
from main.GUI.Function_Setting import Parameter_Entry

class Session_Window(Base_Window):

    curr_title="Session"
    session_window_msg = "This window shows the client-control session info"

    window_width = 400
    window_height = 250

    #icon_file_path=icon_file
    sticky="w"

    connect_button_txt="Connect To Control"
    rows_weights_dict={0:1, 1:1}
    columns_weights_dict={0:1}

    host_str="Host:"
    port_str="Port:"
    username_str= "Username:"
    password_str="Password:"

    padx=5
    pady=5

    def __init__(self, app, connect=False):
        print("in session")
        self.app=app
        #self.root=app.window
        super().__init__(app.root)
        self.window.title=self.curr_title
        self.app=app
        self.params_dict={self.host_str: app.client.server_host, self.port_str : app.client.port,
                          self.username_str : app.client.username, self.password_str : app.client.password}
        self.window.title = self.curr_title

        session_label=super().build_label(self.window, self.session_window_msg, 0, 0, sticky="N")

        self.session_frame=super().build_frame(self.window, 1, 0, padx=1, pady=2, sticky="N")
        self.build_parameters_entries()
        if connect:
            self.add_connect_button()

    def build_parameters_entries(self):
        self.params_entries_dict={}
        index=1
        for param, value in self.params_dict.items():
            curr_param_entry_obj = Parameter_Entry(self.session_frame, param, index, self.sticky, self.padx,
                                                   self.pady,"", str("val"), value)
            curr_param_entry_obj.entry.bind("<Return>", self.get_parameter_value)
            curr_param_entry_obj.entry.configure(state="disabled")
            self.params_entries_dict[param]=curr_param_entry_obj
            index+=1
        self.params_entries_dict["Password:"].entry.configure(show="*")


    def get_parameter_value(self):
        input_param_val=self.curr_param_entry_obj.param_intval.get()

    def add_connect_button(self):
        self.connect_button=super().build_button(self.session_frame, self.connect_button_txt,
                             self.app.client.connect_client,
                             len(self.params_entries_dict)+1, 1, sticky="N")
