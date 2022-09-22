from main.previous_versions.GUI_general_functions import *
from main.previous_versions.run_new_experiment import open_run_new_experiment_window

def add_submenu(main_menu, label_name, build_sub_menu_func):
    added_submenu=tk.Menu(main_menu, tearoff=0)
    main_menu.add_cascade(label=label_name, menu=added_submenu)
    build_sub_menu_func(added_submenu)
    return added_submenu

def get_file_template_command():
    print("get_file_template_command to implement")

def build_experiment_menu(experiment_menu):
    experiment_menu.add_command(label="Run New Experiment", command=lambda: open_run_new_experiment_window(root))
    experiment_menu.add_command(label="Get File Template", command=get_file_template_command)

def open_AOM_window():
    print("AOM command to implement")

def open_GPIO_window():
    print("GPIO_command to implement")

def build_device_actions_menu(device_actions_menu):
    device_actions_menu.add_command(label="AOM", command=open_AOM_window)
    device_actions_menu.add_command(label="GPIO", command=open_GPIO_window)

def open_session_info_window():
    print("get_session_info_command to implement")

def open_change_login_setting_window():
    print("change_login_parameters_command to implement")

def open_termination_window():
    print("terminate_command to implement")

def build_session_menu(session_menu):
    session_menu.add_command(label="Get Session Info", command=open_session_info_window)
    session_menu.add_command(label="Change Login Settings", command=open_change_login_setting_window)
    session_menu.add_command(label="Terminate", command=open_termination_window)

def open_documentation_command():
    print("open_documentation_command to implement")

def build_help_menu(help_menu):
    help_menu.add_command(label="Open Documentation", command=open_documentation_command)
    help_menu.add_command(label="Bugs reporting", command=open_documentation_command)

def build_main_menu_window(main_menu_bar):
    experiment_menu=add_submenu(main_menu_bar, 'Experiment', build_experiment_menu)
    device_actions_menu=add_submenu(main_menu_bar, 'Device Actions', build_device_actions_menu)
    session_menu=add_submenu(main_menu_bar, 'Session', build_session_menu)
    help_menu=add_submenu(main_menu_bar, 'Help', build_help_menu)


def build_root_window():
    global root_qs_logo_image
    root.title(root_title)
    root.rowconfigure(0, weight=1)
    root.rowconfigure(1, weight=8)
    root.columnconfigure(0, weight=1)

    define_window_position(root, root_width, root_height)
    root.iconbitmap(icon_file)
    main_menu_bar=tk.Menu(root)
    build_main_menu_window(main_menu_bar)
    root.config(menu=main_menu_bar)
    root_message_label=tk.Label(root, text=root_message_str)
    root_message_label.grid(row=0, sticky="N")

    root_qs_logo_image=ImageTk.PhotoImage(file=qs_logo_file)
    root_qs_logo_label=tk.Label(root, image=root_qs_logo_image)
    root_qs_logo_label.grid(row=1)

if __name__ == '__main__':
    root=tk.Tk()
    build_root_window()
    root.mainloop()
