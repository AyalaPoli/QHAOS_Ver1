from main.previous_versions.GUI_general_functions import *


def configure_grid_new_experiment_window():
    new_experiment_window.columnconfigure(0, weight=2)
    new_experiment_window.columnconfigure(1, weight=2)
    new_experiment_window.columnconfigure(2, weight=1)
    new_experiment_window.rowconfigure(0, weight=1)
    new_experiment_window.rowconfigure(1, weight=20)

def upload_experiment_file_command(filename_label, file_validation_label):
    input_file_path=tk.filedialog.askopenfilename(initialdir=experiments_files_dir,
                                                  title=askfilenametitle,filetype=[("CSV file",".csv")])

    validation_message=get_validatation_message_experiment_file_format(input_file_path)

    validation_label_bg='lightgreen' if validation_message==valid_message_str else 'coral'

    filename_label.configure(text=input_file_path)
    file_validation_label.configure(bg=validation_label_bg)
    file_validation_label.insert(tk.INSERT, validation_message)
    file_validation_label.configure(state='disabled')

def configure_grid_upload_experiment_window():
    new_experiment_window.columnconfigure(0, weight=1)
    new_experiment_window.columnconfigure(1, weight=2)
    new_experiment_window.rowconfigure(0, weight=1)
    new_experiment_window.rowconfigure(1, weight=2)
    new_experiment_window.rowconfigure(2, weight=1)
    new_experiment_window.rowconfigure(3, weight=1)

def get_validatation_message_experiment_file_format(file_path):
    #validation_message=invalid_message_str
    validation_message=valid_message_str


    return validation_message

def build_upload_file_labels(upload_experiment_file_window, file_validation_label):
    filename_label=tk.Label(upload_experiment_file_window, text=input_file_path)
    filename_label.grid(row=0, column=1, sticky="W", padx=buttons_experiment_padx, pady=buttons_experiment_pady)

    upload_file_label=tk.Label(upload_experiment_file_window, text=upload_file_label_txt)
    upload_file_label.grid(row=0, column=0, sticky="W", padx=buttons_experiment_padx, pady=buttons_experiment_pady)

    upload_file_button=tk.Button(upload_experiment_file_window, text=upload_file_button_txt, command=lambda: upload_experiment_file_command(filename_label, file_validation_label))
    upload_file_button.grid(row=0, column=0, sticky="W", padx=buttons_experiment_padx, pady=buttons_experiment_pady)


def build_validation_file_label(upload_experiment_file_window):
    #validation_message=get_validatation_message_experiment_file_format(input_file_path)

    #validation_frame=tk.Frame(upload_experiment_file_window)
    #validation_frame.grid(row=1, column=0, sticky="nsew", padx=buttons_experiment_padx, pady=buttons_experiment_pady, columnspan=2)

    #validation_button=tk.Button(validation_frame, text=validate_experiment_button_str,
#                                command=lambda x:get_validatation_message_experiment_file_format(input_file_path, file_validation_label))
    #validation_button.grid(row=0, column=0, sticky="nsew", padx=buttons_experiment_padx, pady=buttons_experiment_pady)
    #yscrollbar = tk.Scrollbar(validation_frame)
    #yscrollbar.grid(row=1, column=1, sticky="nsew")
    #file_validation_label=tk.Text(validation_frame, bg='white', cursor='circle',
                                  #wrap=tk.WORD, yscrollcommand=yscrollbar.set)
    #file_validation_label.grid(row=1, column=0, sticky="nsew")
    print("4")

def apply_experiment_file_command():
    print("apply_experiment_file_command")

def build_upload_experiment_file_window():
    upload_experiment_file_window=tk.Toplevel(new_experiment_window)
    upload_experiment_file_window.title(upload_experiment_file_window_title)
    define_window_position(new_experiment_window, upload_exp_file_window_width, upload_exp_file_window_height)
    configure_grid_upload_experiment_window()

    #build_validation_file_label(upload_experiment_file_window)

    validation_frame=tk.Frame(upload_experiment_file_window)
    validation_frame.grid(row=1, column=0, sticky="nsew", padx=buttons_experiment_padx, pady=buttons_experiment_pady, columnspan=2)

    #validation_button=tk.Button(validation_frame, text=validate_experiment_button_str,
    #                            command=lambda x:get_validatation_message_experiment_file_format(input_file_path, file_validation_label))
    #validation_button.grid(row=0, column=0, sticky="nsew", padx=buttons_experiment_padx, pady=buttons_experiment_pady)
    yscrollbar = tk.Scrollbar(validation_frame)
    yscrollbar.grid(row=0, column=1, sticky="nsew")
    file_validation_label=tk.Text(validation_frame, bg='white', cursor='circle',
                                  wrap=tk.WORD, yscrollcommand=yscrollbar.set)
    file_validation_label.grid(row=0, column=0, sticky="nsew")


    build_upload_file_labels(upload_experiment_file_window, file_validation_label)

    iteration_frame=tk.Frame(upload_experiment_file_window)
    iteration_frame.grid(row=2, column=0, sticky="nsew", padx=buttons_experiment_padx, pady=buttons_experiment_pady, columnspan=2)

    experiment_iteration_label=tk.Label(iteration_frame, text="Please choose experiment iteration:")
    experiment_iteration_label.grid(row=0,column=0, sticky="nsew", columnspan=2)
    experiment_iteration=tk.IntVar()
    single_run=tk.Radiobutton(iteration_frame, text="Single Run", variable=experiment_iteration, value=1)
    single_run.grid(row=1, column=1, sticky="nsew")
    infinite_run=tk.Radiobutton(iteration_frame, text="Infinite Run", variable=experiment_iteration, value=2)
    infinite_run.grid(row=2, column=1, sticky="nsew")
    #print(experiment_iteration)
    print("upload experiment file command")

    apply_experiment_button=tk.Button(upload_experiment_file_window, text="Apply Experiment File", command=apply_experiment_file_command)
    apply_experiment_button.grid(row=3, column=0, sticky="nsew", padx=frames_experiment_padx, pady=frames_experiment_pady)

def build_upload_experiment_file_frame():
    file_left_frame=tk.Frame(new_experiment_window, bg='moccasin', borderwidth = 1)
    file_left_frame.grid(row=1, column=0, sticky="nsew", padx=frames_experiment_padx, pady=frames_experiment_pady)
    upload_new_file_button=tk.Button(file_left_frame, text=upload_file_button_txt)
    upload_new_file_button.bind("<Button>", build_upload_experiment_file_window())
    upload_new_file_button['font']=big_font
    upload_new_file_button.grid(row=0, column=0, padx=buttons_experiment_padx, pady=buttons_experiment_pady)

def visualize_file_command():
    print("visualize_file_command")

def build_visualization_file_frame():
    visualize_center_frame=tk.Frame(new_experiment_window, bg='cornsilk', borderwidth = 1)
    visualize_center_frame.grid(row=1, column=1, sticky="nsew", padx=frames_experiment_padx, pady=frames_experiment_pady)
    vizulaize_file_button=tk.Button(visualize_center_frame, text=visualize_file_button_txt, command=visualize_file_command, state=tk.DISABLED)
    vizulaize_file_button['font']=big_font
    vizulaize_file_button.grid(row=0, column=0, padx=buttons_experiment_padx, pady=buttons_experiment_pady)


def start_experiment_command():
    print("start_experiment_command")

def build_experiment_buttons_frame():
    experiment_buttons_frame=tk.Frame(new_experiment_window, bg='white')
    experiment_buttons_frame.grid(row=1, column=2, sticky="nsew", padx=frames_experiment_padx, pady=frames_experiment_pady)

    #start_experiment_button=tk.Button(experiment_buttons_frame, text=start_experiment_txt, command=start_experiment_command, state=tk.DISABLED)
    start_experiment_button=tk.Button(experiment_buttons_frame, text=start_experiment_txt, command=start_experiment_command)
    start_experiment_button['font']=big_font
    start_experiment_button.grid(row=0, column=0, sticky="nsew", padx=buttons_experiment_padx, pady=buttons_experiment_pady)

    device_experiment=tk.Button(experiment_buttons_frame, text=device_configuration_experiment_txt)
    device_experiment['font']=big_font
    device_experiment.grid(row=1, column=0, sticky="nsew", padx=buttons_experiment_padx, pady=buttons_experiment_pady/2)


def built_run_new_experiment_window():
    new_experiment_window.title(run_new_experiment_title)
    define_window_position(new_experiment_window, run_experiment_window_width, run_experiment_window_height)
    new_experiment_window.title(run_new_experiment_title)
    define_window_position(new_experiment_window, run_experiment_window_width, run_experiment_window_height)

    new_experiment_window.iconbitmap(icon_file)

    # configure the grid of new experiment window
    configure_grid_new_experiment_window()

    # Top frame of information message
    root_label=tk.Label(new_experiment_window, text=new_experiment_window_txt)
    root_label.grid(row=0, column=0, sticky="N", columnspan=3)

    # Left frame of upload file
    build_upload_experiment_file_frame()

    # Central frame of visualization message
    build_visualization_file_frame()

    # Right frame of experiment buttons
    build_experiment_buttons_frame()


def open_run_new_experiment_window(root):
    global new_experiment_window
    global big_font
    global input_file_path
    input_file_path=""
    new_experiment_window=tk.Toplevel(root)
    big_font = tk.font.Font(size=big_font_size)

    built_run_new_experiment_window()



