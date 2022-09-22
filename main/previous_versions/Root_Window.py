#from main.GUI.GUI_objects import *
from main.GUI.Run_New_Experiment_Window import *
from main.previous_versions.Device_Actions_Window_wo_Inhirit import *
from main.Configuration_files.AOM_configuration import *

#TODO: check why logo doesn't work


class ER_Application():

    root_title = 'Software Demo'
    root_message_str = "\nWelcome to the software demo!\nPlease select your action from the menu"
    root_width = 600
    root_height = 400
    window_height = 400
    rows_weights_dict={0:1, 1:8}
    columns_weights_dict={0:1}
    icon_file_path=icon_file


    def __init__(self, root):
        self.root=root
        self.root_configuration()


    def root_configuration(self):

        self.root.title(self.root_title)
        self.root.rowconfigure(0, weight=1)
        self.root.rowconfigure(1, weight=8)
        self.root.columnconfigure(0, weight=1)

        define_window_position(self.root, self.root_width, self.root_height)
        self.root.iconbitmap(icon_file)
        root_message_label = tk.Label(self.root, text=self.root_message_str)
        root_message_label.grid(row=0, sticky="N")

        root_qs_logo_image = ImageTk.PhotoImage(file=qs_logo_file)
        self.root_qs_logo_label = tk.Label(root, image=root_qs_logo_image)
        self.root_qs_logo_label.image=root_qs_logo_image #keep a reference
        self.root_qs_logo_label.grid(row=1)

        self.build_main_menu()

    def configure_rows_and_columns_weights(self, master):
        for row_index,row_weight in self.rows_weights_dict.items():
            master.rowconfigure(row_index, weight=row_weight)

        for column_index,column_weight in self.columns_weights_dict.items():
            master.columnconfigure(column_index, weight=column_weight)

    def build_main_menu(self):
        self.main_menu_bar = tk.Menu(self.root)
        self.root.config(menu=self.main_menu_bar)

        experiment_submenu_dict = {"Run New Experiment": self.open_run_new_experiment_window,
                                              "Get File Template": self.get_file_template}
        device_actions_submenu_dict = {AOM_str: self.open_AOM_device_action_window,
                                                  GPIO_str: self.open_GPIO_device_action_window}
        session_submenu_dict = {"Get Session Info": self.get_session_info,
                                "Login Settings": self.open_login_settings_window,
                                "Teminate session": self.terminate_session}
        help_submenu_dict = {"Open Documentation": self.open_documentation,
                             "Bug Reporting": self.report_bug}

        labels_submenus_dict={"Experiment":experiment_submenu_dict, "Device Actions": device_actions_submenu_dict,
                           "Session": session_submenu_dict, "Help":help_submenu_dict}

        for submenu_label,submenu_dict in labels_submenus_dict.items():
            added_submenu = tk.Menu(self.main_menu_bar, tearoff=0)
            self.main_menu_bar.add_cascade(label=submenu_label, menu=added_submenu)
            for option, cmd in submenu_dict.items():
                added_submenu.add_command(label=option, command=cmd)

    def open_run_new_experiment_window(self):
        Run_New_Experiment(self.root)

    def get_file_template(self):
        print("get file template")

    def open_AOM_device_action_window(self):
        print("open_AOM_device_action_window")
        Device_Actions(self.root, AOM_str)

    def open_GPIO_device_action_window(self):
        print("open_GPIO_device_action_window")
        Device_Actions(self.root, GPIO_str)

    def get_session_info(self):
        print("get_session_info")

    def open_login_settings_window(self):
        print("open_login_settings_window")

    def open_documentation(self):
        print("open_documentation")

    def report_bug(self):
        print("report_bug")

    def terminate_session(self):
        self.root.destroy()
        print("terminate_session")

#Root functions


def get_screen_dimension(root):
    return root.winfo_screenwidth(), root.winfo_screenheight()

def get_center_point(screen_width, window_width, screen_height, window_height):
    center_x = int(screen_width / 2 - window_width / 2)
    center_y = int(screen_height / 2 - window_height / 2)
    return center_x, center_y

def define_window_position(window, window_width, window_height):
    screen_width, screen_height=get_screen_dimension(window)
    center_x, center_y=get_center_point(screen_width, window_width, screen_height, window_height)
    window.geometry(f'{window_width}x{window_height}+{center_x}+{center_y}')



if __name__ == '__main__':
    root=tk.Tk()
    er_app=ER_Application(root)
    root.mainloop()
