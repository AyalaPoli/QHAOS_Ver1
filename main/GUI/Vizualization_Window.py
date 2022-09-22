from main.GUI.Base_Window import *
from main.GUI.Select_Device_Window import *

import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.backends.backend_tkagg import NavigationToolbar2Tk

from main.GUI.Upload_New_Experiment_Window import *
from itertools import product


class Vizualization_Window(Base_Window):
    curr_title = "Experiment Vizualization"
    window_width = 1700
    window_height = 1100
    vizualize_window_msg = "This window shows a graphical representation of the experiment directory"

    rows_weights_dict = {0: 1, 1: 1, 2: 1}
    columns_weights_dict = {0: 1}

    req_rows_file_num = 4
    max_AOM_channels_lines = 5
    max_GPIO_channels_lines = 5

    dir_to_work = add_to_path(experiments_directories, "vizualization_dir")
    upload_dir_button_txt = "Upload Experiment Directory"
    select_devices_button_txt = "Select Devices to Display"
    input_dir_path=""
    devices_label_txt=""
    devices_label_format= "AOM: {}\nGPIO: {}"
    err_uploaded_dir_title = "Invalid Uploaded Experiment Directory"
    err_uploaded_dir_msg = "Invalid uploaded experiment directory:\n{}\n\n{}"

    available_exp_devices_dict = {AOM_str: [], GPIO_str: []}
    selected_exp_devices_dict = {AOM_str: [], GPIO_str: []}

    fig_height = 3
    fig_width = 3

    max_AOM_devices = 3
    max_GPIO_devices = 3
    max_events_num = 10
    max_view_devices_dict={AOM_str:max_AOM_devices, GPIO_str:max_GPIO_channels_lines}


    def __init__(self, app):
        self.app=app
        super().__init__(app.window)

        super().build_label(self.window, self.vizualize_window_msg, 0, 0, sticky="N")

        self.build_buttons_frame()


    def build_buttons_frame(self):
        self.buttons_frame=super().build_frame(self.window, 1, 0, sticky="nsew")

        self.upload_file_button=super().build_button(self.buttons_frame, self.upload_dir_button_txt,
                                                self.upload_experiment_dir_command, 0, 0, sticky="W")
        self.filename_label=super().build_label(self.buttons_frame, self.input_dir_path, 0, 1, sticky="W")
        super().change_widget_config(self.filename_label, "font", ("Ariel", 15))
        self.select_device_button = super().build_button(self.buttons_frame, self.select_devices_button_txt,
                                                       self.select_devices_command, 1, 0, sticky="W")
        super().change_widget_state(self.select_device_button, activate=False)

        self.selected_devices_label = super().build_label(self.buttons_frame, self.devices_label_txt, 1, 1, sticky="W")
        super().change_widget_config(self.selected_devices_label, "font", ("Ariel", 15))


    def upload_experiment_dir_command(self):
        with open(last_view_path_file, 'r') as f:
            last_running_path = f.read().rstrip()
        self.input_dir_path = tk.filedialog.askdirectory(initialdir=last_running_path)
        with open(last_view_path_file, 'w') as f:
            f.write(self.input_dir_path)
        if not self.input_dir_path:
            return

        validate_window_hided = Upload_New_Experiment(self.app, restart_flag=True, external_uploaded_path=self.input_dir_path)
        valid_msg = validate_window_hided.get_validatation_message_of_dir_format()
        validate_window_hided.window.destroy()
        valid_def = True if valid_msg == validate_window_hided.valid_message_str else False

        if valid_def:
            self.filename_label.configure(text=self.input_dir_path)
            self.set_exp_devices_list()
            self.set_events_times()
            super().change_widget_state(self.select_device_button, activate=True)
        else:
            self.app.show_err_msg(self.err_uploaded_dir_title,
                                  self.err_uploaded_dir_msg.format(self.input_dir_path, valid_msg))

    def set_exp_devices_list(self):
        for filename in os.listdir(self.input_dir_path):
            if filename!=events_time_filename:
                device, index=get_device_channel_tupple(filename)
                self.available_exp_devices_dict[device].append(index)

    def set_events_times(self):
        times_file=add_to_path(self.input_dir_path, events_time_filename)
        with open(times_file, 'r') as f:
            times_lst = [int(i) for i in f.read().rstrip().split(',')]
        self.events_ranges=[(times_lst[i], times_lst[i+1]) for i in range(1, len(times_lst)-1)]
        self.events_num_to_display=min(len(self.events_ranges), self.max_events_num)

    def select_devices_command(self):
        Select_Devices_Window(self)

    def change_device_info_after_select(self, AOM_list, GPIO_list):
        print("in change")
        print(AOM_list)
        print(GPIO_list)
        self.selected_exp_devices_dict[AOM_str]=AOM_list
        self.selected_exp_devices_dict[GPIO_str]=GPIO_list
        self.devices_label_txt=self.devices_label_format.format(self.get_lst_str(AOM_list), self.get_lst_str(GPIO_list))
        self.selected_devices_label.configure(text=self.devices_label_txt)

        self.build_vizual_frame()

    def get_lst_str(self, int_lst):
        return ', '.join([str(i) for i in int_lst])

    def build_vizual_frame(self):
        self.analog_frame=super().build_frame(self.window, 2, 0, sticky="nsew")
        self.digital_frame=super().build_frame(self.window, 3, 0, sticky="nsew")

        self.build_devices_group_vizual_frame(AOM_str)
        self.build_devices_group_vizual_frame(GPIO_str)


    def build_devices_group_vizual_frame(self, device_type):

        self.req_device_index_lst=self.selected_exp_devices_dict[device_type]
        if not self.req_device_index_lst:
            return

        if device_type==AOM_str:
            curr_frame=self.analog_frame
            num_rows = min(len(self.req_device_index_lst), self.max_AOM_devices*2) #amplitude and frequency plots
        if device_type==GPIO_str:
            curr_frame=self.digital_frame
            num_rows = min(len(self.req_device_index_lst), self.max_GPIO_devices)

        curr_frame.rowconfigure(0, weight=20)
        curr_frame.rowconfigure(1, weight=1)
        curr_frame.columnconfigure(0, weight=20)
        curr_frame.columnconfigure(1, weight=1)
        #curr_frame.grid(columnspan=2)

        self.fig, self.ax = plt.subplots(num_rows, self.events_num_to_display, figsize=(self.fig_height, self.fig_height)) ## axes are in a two-dimensional array, indexed by [row, col]
        self.channel_subplots_lst=[]

        if device_type==AOM_str:
            self.build_AOM_vizual_frame(num_rows)

        elif device_type==GPIO_str:
            self.build_GPIO_vizual_frame(num_rows)

        for ax in self.fig.get_axes():
            ax.label_outer()

        #self.fig.subplots_adjust(left=None, bottom=None, right=None, top=None, wspace=None, hspace=None)

        canvas = FigureCanvasTkAgg(self.fig, master=curr_frame)
        canvas._tkcanvas.pack(fill=tk.BOTH, expand=1)
        #canvas.get_tk_widget().pack(

        #self.toolbar_frame = super().build_frame(curr_frame, 2, 0)

        plt.subplots_adjust(wspace=0.01, hspace=0.15)

        vert_scrollbar = ctk.CTkScrollbar(master=curr_frame, orientation='vertical')
        vert_scrollbar.pack(side=tk.RIGHT,fill=tk.Y)
        curr_frame['yscrollcommand']=vert_scrollbar.set

        self.toolbar = NavigationToolbar2Tk(canvas, curr_frame)
        self.toolbar.pack(side=tk.BOTTOM, fill=tk.X)

        #scrollbar x and y

    def get_current_file_by_type_channel(self, device_type, index):
        return add_to_path(self.input_dir_path, "{}_{}.csv".format(device_type, index))

    def build_AOM_vizual_frame(self, num_rows):

        for row, event_index in product(range(num_rows), range(self.events_num_to_display)):
            channel_index=self.req_device_index_lst[int(row/2)]
            curr_filename=self.get_current_file_by_type_channel(AOM_str, channel_index)
            amplitude_flag = True if row % 2 == 0 else False
            min_time, max_time = (self.events_ranges[event_index][0], self.events_ranges[event_index][1])
            df = pd.read_csv(curr_filename)
            min_y, max_y = self.get_min_max_val_from_df(df, amplitude_flag)
            subplot = Channel_Subplot(curr_filename, df, self.ax[row, event_index], min_time, max_time, amplitude_flag=amplitude_flag)
            self.channel_subplots_lst.append(subplot)
            x, y = subplot.get_x_y_params_col()
            if len(x) and len(y):
                subplot.ax.plot(x, y)
                subplot.ax.set_xlim(min_time, max_time)
                subplot.ax.set_ylim(min_y, max_y+1)
            else:
                self.plot_constant_line_AOM(subplot, min_time, max_time)
            self.set_titles_AOM(row, event_index, subplot)
            self.channel_subplots_lst.append(subplot)

    def set_titles_AOM(self, row, col, subplot):
        if col == 0:
            freq_amp_str = amplitude_str if subplot.amplitude_flag else frequency_str
            channel_label = "AOM {} {}".format(int(row / 2) + 1, freq_amp_str[:3])

            subplot.ax.set_ylabel(channel_label)
        if row == 0:
            event_title = "Event {}".format(col+1)
            subplot.ax.set_title(event_title)

    def get_min_max_val_from_df(self, df, amplitude_flag):
        req_col_name=amplitude_str if amplitude_flag else frequency_str
        req_col=df[req_col_name].tolist()
        return min(req_col), max(req_col)

    def plot_constant_line_AOM(self,subplot, min_time, max_time):
        if not self.channel_subplots_lst:
            subplot.ax.hlines.plot(y=0, color='white', xmin=min_time, xmax=max_time)
        else:
            prev_y=self.channel_subplots_lst[:-1].get_x_y_params_col[1][:-1]
            subplot.ax.hlines(y=prev_y, xmin=min_time, xmax=max_time)

    def plot_empty_by_activate_value_GPIO(self, subplot, min_time, max_time):
        if not self.channel_subplots_lst:
            subplot.ax.hlines.plot(y=0, color='white', xmin=min_time, xmax=max_time)
        else:
            prev_y = self.channel_subplots_lst[:-1].get_x_y_params_col[1][:-1]
            if prev_y:
                subplot.ax.fill_between([min_time, max_time], [prev_y, prev_y], 0)

    def build_GPIO_vizual_frame(self, num_rows):
        prev_active_range=False
        for row, event_index in product(range(num_rows), range(self.events_num_to_display)):
            channel_index=self.req_device_index_lst[row]
            curr_filename=self.get_current_file_by_type_channel(GPIO_str, channel_index)
            df = pd.read_csv(curr_filename)
            min_time, max_time = (self.events_ranges[event_index][0], self.events_ranges[event_index][1])
            print("row {}".format(row))
            print("event_index {}".format(event_index))
            subplot = Channel_Subplot(curr_filename, df, self.ax[row, event_index], min_time, max_time, in_active_range=prev_active_range)
            self.channel_subplots_lst.append(subplot)
            prev_active_range=subplot.in_active_range
            x, y = subplot.get_x_y_params_col()
            if len(x) and len(y):
                subplot.ax.plot(x, y, drawstyle='steps')
                subplot.ax.set_ylim(off_value, on_value)

            for active_range in subplot.active_time_ranges:
                subplot.ax.axvspan(active_range[0], active_range[1], alpha=0.8, color='green')

    def set_titles_GPIO(self, row, col, subplot):
        if col == 0:
            channel_label = "AOM {}".format(row+1)
            subplot.ax.set_ylabel(channel_label)
        if row == 0:
            event_title = "Event {}".format(col)
            subplot.ax.set_title(event_title)

class Channel_Subplot():

    def __init__(self, file_path, df, ax, min_time, max_time, in_active_range=False, amplitude_flag=True):
        self.file_path = file_path
        self.init_device_type_from_filename()
        self.df=df
        self.ax=ax
        self.amplitude_flag=amplitude_flag
        self.min_time=min_time
        self.max_time=max_time
        self.init_subset()
        self.set_x_y_params_col()

        if self.device_type==AOM_str:
            self.params_range_dict = AOM_function_parameters_range_dict
            self.param = amplitude_str if amplitude_flag else frequency_str

        if self.device_type==GPIO_str:
            self.params_range_dict = GPIO_function_parameters_range_dict
            self.in_active_range = in_active_range
            self.set_active_time_ranges()

    def init_device_type_from_filename(self):
        dirname, filename = os.path.split(self.file_path)
        self.device_type, self.device_index=get_device_channel_tupple(filename)

    def init_subset(self):
        self.df_subset = self.df.loc[(self.df[time_str] > self.min_time) & (self.df[time_str]< self.max_time)]
        self.df_subset = self.df_subset
        if self.df_subset.empty:
            return [], []

    def set_x_y_params_col(self):
        self.x = self.df_subset[time_str].tolist()
        if self.is_AOM_channel():
            self.y = self.df_subset[amplitude_str] if self.amplitude_flag else self.df_subset[frequency_str]
        if self.is_GPIO_channel():
            self.y = self.df_subset[activate_str]

    def get_x_y_params_col(self):
        return self.x, self.y

    def is_AOM_channel(self):
        return True if self.device_type == AOM_str else False

    def is_GPIO_channel(self):
        return True if self.device_type == GPIO_str else False

    def set_active_time_ranges(self):
        self.active_time_ranges=[]
        self.in_active_range=False
        for curr_time, activate_value in zip(self.x, self.y):
            if activate_value and not self.in_active_range:
                start_active_time=curr_time #open new active range
                in_active_range=True
            if not activate_value and self.in_active_range:
                self.active_time_ranges.append([start_active_time, curr_time]) #save active range
                in_active_range=False
