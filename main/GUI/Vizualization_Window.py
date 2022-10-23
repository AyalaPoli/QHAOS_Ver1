import tkinter

from main.GUI.Base_Window import *
from main.GUI.Select_Device_Window import *

import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.backends.backend_tkagg import NavigationToolbar2Tk
from matplotlib.ticker import ScalarFormatter

import matplotlib
from main.GUI.Upload_New_Experiment_Window import *
from itertools import product
from collections import OrderedDict

import math

class Vizualization_Window(Base_Window):
    curr_title = "Experiment Vizualization"
    window_width = 700
    window_height = 500
    vizualize_window_msg = "This window displays a graphical representation of an experiment scheduled operations"

    #rows_weights_dict = {0: 1, 1: 5, 2: 15, 3: 5}
    rows_weights_dict = {0: 1, 1: 1, 2: 10, 3: 10}
    columns_weights_dict = {0: 1}



    dir_to_work = add_to_path(experiments_directories, "vizualization_dir")
    upload_dir_button_txt = "Upload Experiment Directory"
    select_devices_button_txt = "  Select Devices to Display    "
    input_dir_path=""
    devices_label_txt=""
    devices_label_format= "AOM: {}\nGPIO: {}"
    err_uploaded_dir_title = "Invalid Uploaded Experiment Directory"
    err_uploaded_dir_msg = "Invalid uploaded experiment directory:\n{}\n\n{}"
    browser_txt="Browse events and channels"
    events_file_error_title="Error In Events File"
    no_events_file_msg="No events times file were found. \n\nPlease add the file to the following path: \n{}"

    available_exp_devices_dict = {AOM_str: [], GPIO_str: []}
    selected_exp_devices_dict = {AOM_str: [], GPIO_str: []}

    fig_height = 3
    fig_width = 3

    req_rows_file_num = 4
    max_AOM_channels_lines = 4
    max_GPIO_channels_lines = 5

    max_AOM_devices = 6
    max_GPIO_devices = 10
    max_events_num = 10
    max_view_devices_dict={AOM_str:max_AOM_devices, GPIO_str:max_GPIO_channels_lines}

    req_frames_lst=[]
    decimal_annot_num=3
    annot = None
    curr_ax=None

    def __init__(self, app):
        self.app=app
        self.prev_view_selections=self.app.get_prev_user_selections_dict()

        super().__init__(app.window)
        #screen_width=self.window.winfo_screenwidth()
        #screen_height=self.window.winfo_screenheight()
        #delta=0
        #self.window.geometry(f'{screen_width}x{screen_height}+{delta}+{delta}')
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
        last_view_path_file=self.prev_view_selections[exp_viewer_key][exp_view_last_path]
        self.input_dir_path = tk.filedialog.askdirectory(initialdir=last_view_path_file)
        self.is_prev_selected_path=True if self.input_dir_path == last_view_path_file else False
        if not self.is_prev_selected_path:
            self.prev_view_selections[exp_viewer_key][exp_view_last_path] = self.input_dir_path
            self.app.update_user_selections_dict(self.prev_view_selections)
        if not self.input_dir_path:
            return

        validate_window_hided = Upload_New_Experiment(self.app, restart_flag=True, external_uploaded_path=self.input_dir_path)
        valid_msg = validate_window_hided.get_validatation_message_of_dir_format()
        validate_window_hided.window.destroy()
        valid_def = True if valid_msg == validate_window_hided.valid_message_str else False

        if valid_def:
            self.filename_label.configure(text=self.input_dir_path)
            self.set_exp_devices_list()
            self.set_events_times_dict()

            super().change_widget_state(self.select_device_button, activate=True)
            if self.is_prev_selected_path:
                AOM_channels = self.prev_view_selections[exp_viewer_key][exp_view_last_AOMs]
                GPIO_channels = self.prev_view_selections[exp_viewer_key][exp_view_last_GPIOs]
            else:
                AOM_channels = []
                GPIO_channels = []
            self.change_device_info_after_select(AOM_channels, GPIO_channels)

        else:
            self.app.show_err_msg(self.err_uploaded_dir_title,
                                  self.err_uploaded_dir_msg.format(self.input_dir_path, valid_msg))

    def set_exp_devices_list(self):
        self.available_exp_devices_dict = {AOM_str: [], GPIO_str: []}
        for filename in os.listdir(self.input_dir_path):
            if filename!=events_time_filename:
                device, index=get_device_channel_tupple(filename)
                self.available_exp_devices_dict[device].append(index)
                #new_index=list(sorted([i for i in index if i not in self.available_exp_devices_dict[device]]))
                #self.available_exp_devices_dict[device].extend(new_index)

    def set_events_times_dict(self):
        times_file=add_to_path(self.input_dir_path, events_time_filename)
        validation_msg = self.get_times_validation(times_file)
        if validation_msg:
            self.show_err_msg(self.events_file_error_title, validation_msg)
        with open(times_file, 'r') as f:
            #times_lst= = [int(i) for i in f.read().rstrip().split(',')]
            self.times_dict = OrderedDict(x.rstrip().split(None, 1) for x in f)
        #self.events_ranges=[(times_lst[i], times_lst[i+1]) for i in range(len(times_lst)-1)]
        self.req_events_len=min(len(self.times_dict.keys()), self.max_events_num)
        self.req_events_dict=OrderedDict()
        index_keys=range(self.req_events_len)
        dict_vals= list(self.times_dict.keys())[:self.req_events_len]
        for i, val in zip(index_keys, dict_vals):
            self.req_events_dict[i]=val
        self.req_events_keys=self.req_events_dict.keys()

        #self.events_num_to_display=min(len(self.events_ranges), self.max_events_num)

    def get_last_time_from_device_files(self, device_type):
        last_exp_time=0
        for channel_index in self.selected_exp_devices_dict[device_type]:
            input_file="{}_{}.csv".format(device_type, channel_index)
            df = pd.read_csv(add_to_path(self.input_dir_path, input_file), keep_default_na=False)
            curr_last_time= df[time_str].iat[-1]
            if curr_last_time>last_exp_time:
                last_exp_time=curr_last_time
        return last_exp_time

    def set_last_experiment_time(self):
        self.last_exp_time=max(self.get_last_time_from_device_files(AOM_str), self.get_last_time_from_device_files(GPIO_str))

    def get_times_validation(self, times_file):
        msg=""
        if not os.path.isfile(times_file):
            return self.no_events_file_msg.format(times_file)


    def select_devices_command(self):
        Select_Devices_Window(self)

    def change_device_info_after_select(self, AOM_list, GPIO_list):
        #screen_width=self.window.winfo_screenwidth()
        #screen_height=self.window.winfo_screenheight()
        #delta=0
        #self.window.geometry(f'{screen_width}x{screen_height}+{delta}+{delta}')
        self.selected_exp_devices_dict[AOM_str]=AOM_list
        self.selected_exp_devices_dict[GPIO_str]=GPIO_list
        self.devices_label_txt=self.devices_label_format.format(self.get_lst_str(AOM_list), self.get_lst_str(GPIO_list))
        self.selected_devices_label.configure(text=self.devices_label_txt)

        self.prev_view_selections[exp_viewer_key][exp_view_last_AOMs]=AOM_list
        self.prev_view_selections[exp_viewer_key][exp_view_last_GPIOs]=GPIO_list
        self.app.update_user_selections_dict(self.prev_view_selections)
        self.set_last_experiment_time()

        for frame in self.req_frames_lst:
            frame.destroy()
        self.req_frames_lst=[]
        self.build_vizual_frame()

    def get_lst_str(self, int_lst):
        return ', '.join([str(i) for i in int_lst])

    def build_vizual_frame(self):
        frame_row_index=2

        if len(self.selected_exp_devices_dict[AOM_str]):
            self.analog_frame=super().build_frame(self.window, frame_row_index, 0, sticky="nsew")
            self.req_frames_lst.append(self.analog_frame)
            #self.analog_frame.configure(width=self.fig_width, height=self.fig_height)

            self.req_device_index_lst = self.selected_exp_devices_dict[AOM_str]
            self.req_devices=self.req_device_index_lst[:min(len(self.req_device_index_lst), self.max_AOM_devices)]

            self.build_devices_group_vizual_frame(AOM_str, self.req_devices)

        if len(self.selected_exp_devices_dict[GPIO_str]):
            self.digital_frame=super().build_frame(self.window, len(self.req_frames_lst)+frame_row_index, 0, sticky="nsew")
            self.req_frames_lst.append(self.digital_frame)

            self.req_device_index_lst = self.selected_exp_devices_dict[GPIO_str]
            self.req_devices = self.req_device_index_lst[:min(len(self.req_device_index_lst), self.max_GPIO_devices)]

            #self.digital_frame.configure(width=self.fig_width, height=self.fig_height)
            self.build_devices_group_vizual_frame(GPIO_str, self.req_devices)

    def build_devices_group_vizual_frame(self, device_type, req_devices):
        self.curr_device_type=device_type

        if not req_devices:
            return

        curr_frame=self.analog_frame if device_type==AOM_str else self.digital_frame
        #curr_frame.rowconfigure(0, weight=10)
        #curr_frame.rowconfigure(1, weight=1)
        #curr_frame.rowconfigure(2, weight=1)
        if device_type==AOM_str:
            #req_devices=self.req_device_index_lst[:min(len(self.req_device_index_lst), self.max_AOM_devices)]
            num_rows=len(req_devices)*2
        if device_type==GPIO_str:
            curr_frame=self.digital_frame
            num_rows=len(req_devices)

        plt.style.use("seaborn-notebook")
        for param in ['figure.facecolor', 'axes.facecolor', 'savefig.facecolor']:
            plt.rcParams[param] = '#212946'  # bluish dark grey
        for param in ['text.color', 'axes.labelcolor', 'axes.edgecolor', 'xtick.color', 'ytick.color']:
            plt.rcParams[param] = '0.9'  # very light grey

        #plt.rcParams["figure.figsize"] = [8, 4]
        #plt.rcParams["figure.autolayout"] = True
        #fig_size=(5*num_rows, 5) if device_type==AOM_str else (5*num_rows,5)
        self.fig, self.ax = plt.subplots(num_rows, self.req_events_len)  ## axes are in a two-dimensional array, indexed by [row, col]

        # vert_scrollbar = ctk.CTkScrollbar(master=curr_frame, orientation='vertical')
        # vert_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        # curr_frame['yscrollcommand'] = vert_scrollbar.set
        # # #
        # horizontal_scrollbar = ctk.CTkScrollbar(master=curr_frame, orientation='horizontal')
        # horizontal_scrollbar.pack(side=tk.BOTTOM, fill=tk.X)
        # curr_frame['xscrollcommand'] = horizontal_scrollbar.set

        #plt.axes.linewidth=0.8
        #self.fig, self.ax = plt.subplots(num_rows, self.events_num_to_display, figsize=(self.fig_height, self.fig_height), sharex=True) ## axes are in a two-dimensional array, indexed by [row, col]

        self.fig.suptitle("{} Channels".format(device_type))
        plt.subplots_adjust(wspace=0.012, hspace=0.15)

        self.channel_subplots_lst=[]
        self.canvas = FigureCanvasTkAgg(self.fig, master=curr_frame)

        self.canvas._tkcanvas.pack(fill=tk.BOTH, expand=1)
        self.canvas.draw()

        for curr_ax in self.fig.get_axes():
            curr_ax.label_outer()

        self.fig.canvas.mpl_connect("motion_notify_event", self.show_annotation_by_hover)
        self.fig.canvas.mpl_connect("scroll_event", self.scroll_by_mouse_wheel)
        self.fig.canvas.mpl_connect("button_press_event", lambda event: self.open_plot_by_click(event, device_type))

        curr_frame.pack_propagate(False) #The widgets children do not control the frame size
        #self.fig.canvas.draw_idle()
        #VerticalNavigationToolbar2Tk

        toolbar_frame=super().build_frame(curr_frame, 0, 0)
        curr_toolbar = NavigationToolbar2Tk(self.canvas, toolbar_frame, pack_toolbar=False)
        curr_toolbar.pack(side=tk.BOTTOM, fill=tk.X)
        #curr_toolbar.pack(side=tk.LEFT, fill=tk.Y)

        #browser_frame=super(buid_frame())
        #self.build_browser_frame(curr_frame, device_type)
        self.build_device_subplots(device_type, req_devices)

    def build_browser_frame(self, curr_frame, device_type):
        browser_frame=super().build_frame(curr_frame, 1, 0, pady=10)
        browser_frame.configure(bg="#212946")

        self.up_button=super().build_button(browser_frame, "\u25B2", self.up_button_cmd, 0, 1, padx=0, pady=2, sticky="n")
        self.left_button=super().build_button(browser_frame, "\u25C0", self.left_button_cmd, 1, 0, padx=1, pady=2, sticky="n")
        self.right_button=super().build_button(browser_frame, "\u25B6", self.right_button_cmd, 1, 2,padx=1, pady=2, sticky="n")
        self.down_button=super().build_button(browser_frame, "\u25BC", self.down_button_cmd, 2, 1, padx=0, pady=2, sticky="n")
        browser_buttons_lst=[self.up_button, self.left_button,self.right_button, self.down_button]

        if self.req_events_len<self.max_events_num:
            super().change_widget_state(self.up_button, activate=False)
            super().change_widget_state(self.down_button, activate=False)

        max_devices=self.max_AOM_channels_lines if device_type==AOM_str else self.max_GPIO_devices
        if len(self.req_devices)<max_devices:
            super().change_widget_state(self.left_button, activate=False)
            super().change_widget_state(self.right_button, activate=False)

        for button in browser_buttons_lst:
            super().set_button_size(button, 5, 5)

        curr_label=ctk.CTkLabel(browser_frame, text= self.browser_txt)
        curr_label.grid(row=3, columnspan=3)

    def up_button_cmd(self):

        first_req_device_index= self.selected_exp_devices_dict[self.curr_device_type].index(self.req_devices[0])
        self.req_devices=self.selected_exp_devices_dict[self.curr_device_type][first_req_device_index-1: first_req_device_index-1+len(self.req_devices)]

        self.selected_exp_devices_dict[self.curr_device_type][0]

        if self.req_devices[0] == self.selected_exp_devices_dict[self.curr_device_type][0]:
            super().change_widget_state(self.up_button, activate=False)

        if self.req_devices[-1] != self.selected_exp_devices_dict[self.curr_device_type][-1]:
            super().change_widget_state(self.down_button, activate=True)

        for frame in self.req_frames_lst:
            frame.destroy()

        self.req_frames_lst = []
        self.build_vizual_frame()

    def down_button_cmd(self):
        first_req_device_index = self.selected_exp_devices_dict[self.curr_device_type].index(self.req_devices[0])
        self.req_devices = self.selected_exp_devices_dict[self.curr_device_type][
                           first_req_device_index + 1: first_req_device_index + 1 + len(self.req_devices)]

        if self.req_devices[-1] == self.selected_exp_devices_dict[self.curr_device_type][-1]:
            super().change_widget_state(self.down_button, activate=False)

        if self.req_devices[0] != self.selected_exp_devices_dict[self.curr_device_type][0]:
            super().change_widget_state(self.up_button, activate=True)

        for frame in self.req_frames_lst:
            frame.destroy()

        self.req_frames_lst = []
        self.build_vizual_frame()


    def left_button_cmd(self):

        first_req_event_index = self.selected_exp_devices_dict[self.curr_device_type].index(self.req_events_keys[0])
        self.req_events_dict=OrderedDict(zip(range(first_req_event_index+self.req_events_len), self.times_dict.keys()[first_req_event_index :first_req_event_index+self.req_events_len]))
        self.req_events_keys=self.req_events_dict.keys()

        self.req_events_keys = self.move_list_left(self.req_events_keys.copy())

        if self.req_events_keys[-1] == self.times_dict.keys()[-1]:
            super().change_widget_state(self.left_button, activate=False)

        if self.req_events_keys[0] != self.times_dict.keys()[0]:
            super().change_widget_state(self.right_button, activate=True)

        for frame in self.req_frames_lst:
            frame.destroy()

        self.req_frames_lst = []
        self.build_vizual_frame()


    def right_button_cmd(self):
        self.req_events_keys = self.move_list_right(self.req_events_keys.copy())

        if self.req_events_keys[-1]==self.times_dict.keys()[-1]:
            super().change_widget_state(self.right_button, activate=False)

        if self.req_events_keys[0]!=self.times_dict.keys()[0]:
            super().change_widget_state(self.left_button, activate=True)

        for frame in self.req_frames_lst:
            frame.destroy()

        self.req_frames_lst=[]
        self.build_vizual_frame()

    def move_list_left(self, list_to_move_left):
        return [list_to_move_left[i-1] for i in range(len(list_to_move_left)+1)]

    def move_list_right(self, list_to_move_right):
        return [list_to_move_right[i+1] for i in range(len(list_to_move_right)-1)]


    def build_device_subplots(self, device_type, req_devices):
        start_value=0
        num_rows=len(req_devices)
        if device_type==AOM_str:
            num_rows*=2
        curr_events_indexes= list(self.req_events_keys)[:min(self.req_events_len, self.max_events_num)]

        for row, event_index in product(range(num_rows), range(len(curr_events_indexes))):
            dev_index=row
            if device_type==AOM_str:
                dev_index=int(row/2)
                amplitude_flag = True if row % 2 == 0 else False

            channel_index=req_devices[dev_index]
            curr_filename=self.get_current_file_by_type_channel(device_type, channel_index)
            min_time, max_time = self.get_times_by_event_index(event_index)
            df = pd.read_csv(curr_filename)
            if num_rows==1:
                curr_ax=self.ax[event_index]
                if self.req_events_len==1:
                    curr_ax=self.ax[0]
            else:
                curr_ax=self.ax[0][row] if self.req_events_len == 1 else self.ax[row, event_index]
            event_name= self.get_event_key_by_index(event_index)
            if device_type==AOM_str:
                subplot = AOM_Channel_Subplot(curr_filename, df, curr_ax, min_time, max_time, channel_index, event_index, event_name, start_value, amplitude_flag=amplitude_flag)
            elif device_type==GPIO_str:
                subplot = GPIO_Channel_Subplot(curr_filename, df, curr_ax, min_time, max_time, channel_index, event_index,
                                          event_name, start_value)
            start_value=subplot.end_value
            self.channel_subplots_lst.append(subplot)

            subplot.draw_plot(row)
            if row!=num_rows-1:
                subplot.ax.set_xticks([])


    def get_annotation_of_axis(self, ax):
        for child in ax.get_children():
            if isinstance(child, matplotlib.text.Annotation):
                return child

    def is_coordinates_on_ax_line(self, x, y, ax):
        line = ax.lines[0]
        return True if x in line.get_xdata() and y in line.get_ydata() else False

    def show_annotation_by_hover(self, event):
        curr_hovered_ax=event.inaxes
        if curr_hovered_ax:
            if curr_hovered_ax!=self.curr_ax and self.annot:
                self.annot.set_visible(False)
            self.curr_ax=curr_hovered_ax
            self.annot = self.get_annotation_of_axis(event.inaxes)
            self.ax=event.inaxes
            x, y = event.xdata, event.ydata
            self.annot.xy = np.round(np.array((x, y))).astype(int)
            txt="{:,}ns, {}".format(int(x), round(y, self.decimal_annot_num))
            self.annot.set_text(txt)
            self.annot.set_visible(True)
            #event.inaxes.annotate(txt, xy=(0, 0), textcoords="offset points", arrowprops=dict(arrowstyle="->"), visible=True, bbox=dict(boxstyle="round", fc="w"))
            #event.inaxes.plot(x,y,'ro')
#            event.canvas.draw()
        else:
            if self.annot:
                self.annot.set_visible(False)
        event.canvas.draw()


    def get_subplot_by_x_y(self, x, y):
        event_index=self.get_event_index_by_timepoint(x)
        channel_index=self.get_channel_index_by_y(y)

    def open_plot_by_click(self, event, device_type):
        curr_clicked_ax=event.inaxes
        if curr_clicked_ax:
            event.canvas.draw()
            #x, y = event.xdata, event.ydata

        print("**in open_plot_by_click**")
            #curr_hovered_ax.plot()
        #    curr_hovered_ax.show()


    def get_event_value_by_index(self, event_index):
        return int(list(self.times_dict.values())[event_index])

    def get_event_key_by_index(self, event_index):
        return list(self.times_dict.keys())[event_index]


    def get_current_file_by_type_channel(self, device_type, index):
        return add_to_path(self.input_dir_path, "{}_{}.csv".format(device_type, index))


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

    def get_times_by_event_index(self, event_index):
        min_time=self.get_event_value_by_index(event_index)
        max_time = self.get_event_value_by_index(event_index+1) if event_index != self.req_events_len- 1 else self.last_exp_time
        return min_time, max_time

    def build_GPIO_vizual_frame_OLD(self, req_devices):
        start_value=0
        curr_event_index=min(self.req_events_len, self.max_events_num)
        num_rows=len(req_devices)

        for row, event_index in product(range(num_rows), range(curr_event_index)):
            channel_index=self.req_device_index_lst[row]
            curr_filename=self.get_current_file_by_type_channel(GPIO_str, channel_index)
            df = pd.read_csv(curr_filename)
            min_time, max_time = self.get_times_by_event_index(event_index)
            #min_time, max_time = (self.get_event_value_by_index(event_index), self.get_event_value_by_index(event_index+1))
            if num_rows == 1:
                curr_ax = self.ax[event_index]
                if self.req_events_len == 1:
                    curr_ax = self.ax[0]
            else:
                if self.req_events_len == 1:
                    curr_ax = self.ax[0][row]
                else:
                    curr_ax = self.ax[row, event_index]
            event_name = self.get_event_key_by_index(event_index)

            subplot = Channel_Subplot(curr_filename, df, curr_ax, min_time, max_time, channel_index, event_index, event_name, start_value)
            self.channel_subplots_lst.append(subplot)
            #curr_annot = self.create_annotation(curr_ax)
            self.fig.canvas.mpl_connect("motion_notify_event", self.show_annotation_by_hover)
            self.fig.canvas.mpl_connect("button_press_event", lambda event: self.open_plot_by_click)
            self.fig.canvas.mpl_connect("scroll_event", self.scroll_by_mouse_wheel)
            subplot.draw_plot(row)
            start_value=subplot.end_value
            if row!=num_rows-1:
                subplot.ax.set_xticks([])

    def scroll_by_mouse_wheel(self, event):
        if event.button=="up":
            print("index plus 1")
        if event.button=="down":
            print("index minus 1")

class Base_Channel_Subplot(object):
    channel_str="Channel"
    event_str="Event"
    added_y_perc=0.05
    height=2
    weight=5

    def __init__(self, file_path, df, ax, min_time, max_time, channel_index, event_index, event_name, start_value, amplitude_flag=True):
        self.file_path = file_path
        self.channel_index=channel_index
        self.init_device_type_from_filename()
        self.df=df
        self.ax=ax
        self.amplitude_flag=amplitude_flag
        self.min_time=min_time
        self.max_time=max_time
        self.event_index=event_index
        self.event_name=event_name
        self.start_value = start_value

        self.init_subset()
        self.create_annotation()
        self.ax.figure.set_size_inches(self.weight, self.height)

    def set_x_y_params_by_col(self, col_name):
        self.is_empty_event=True
        self.x = self.df_subset[time_str].tolist()
        self.y = self.df_subset[col_name].tolist()

        if len(self.x) and len(self.y):
            self.is_empty_event=False

        self.x.insert(0, self.min_time)
        self.y.insert(0, self.start_value)

        for i in range(len(self.y)): #fill empty values
            if math.isnan(self.y[i]):
                self.y[i]=self.y[i-1]

        self.end_value=self.y[-1]
        self.x.append(self.max_time)
        self.y.append(self.end_value)

    def init_device_type_from_filename(self):
        dirname, filename = os.path.split(self.file_path)
        self.device_type, self.device_index=get_device_channel_tupple(filename)
        if self.device_index!=self.channel_index:
            print("*********Error: self.device_index!=self.channel_index ")

    def init_subset(self):
        self.df_subset = self.df.loc[(self.df[time_str] >= self.min_time) & (self.df[time_str]< self.max_time)]
        self.df_subset = self.df_subset
        if self.df_subset.empty:
            return [], []

    def event_is_empty(self):
        return True if len(self.x) and len(self.y) else False



    def create_annotation(self):
        self.ax.annotate("annot", xy=(0, 0), xytext=(20, 20), textcoords="offset points", color="darkblue",
                            arrowprops=dict(arrowstyle="->"), visible=False,
                            bbox=dict(boxstyle="round", fc="w"), zorder=0)

    def set_ylabel(self):
        pass

    def set_properties(self):
        pass

    def draw_plot(self, row):
        if self.event_index == 0:
            self.set_ylabel()
        if row == 0:
            self.ax.set_title(self.event_name,  fontsize=10)

        self.set_properties()

        self.ax.set_xlim(self.min_time, self.max_time)
        self.ax.tick_params(axis='both', which='major', labelsize=8)

        self.ax.ticklabel_format(style='scientific')
        if self.event_index!=0:
            self.ax.set_yticks([])

        self.ax.plot(self.x, self.y, drawstyle='steps', color=self.curr_color)

class AOM_Channel_Subplot(Base_Channel_Subplot):
    amplitude_color="#08F7FE"
    frequency_color="#F5D300"

    def __init__(self, file_path, df, ax, min_time, max_time, channel_index, event_index, event_name, start_value, amplitude_flag=True):
        super().__init__(file_path, df, ax, min_time, max_time, channel_index, event_index, event_name, start_value)

        self.amplitude_flag=amplitude_flag
        self.params_range_dict = AOM_function_parameters_range_dict
        self.param = amplitude_str if amplitude_flag else frequency_str
        super().set_x_y_params_by_col( self.param)

        self.curr_color=self.amplitude_color if self.amplitude_flag else self.frequency_color

    def set_ylabel(self):
        suffix_len = 3 if self.param == amplitude_str else 4
        self.ax.set_ylabel( "Ch{} {}".format(self.channel_index, self.param[:suffix_len].lower()), size=8, rotation=0, loc="top")
        self.ax.yaxis.set_label_coords(-0.1, 0)

    def set_properties(self):
        min_y, max_y=self.get_min_max_y_values_from_df()
        self.ax.set_ylim(min_y-min_y*self.added_y_perc, max_y+max_y*self.added_y_perc)

    def get_min_max_y_values_from_df(self):
        absolute_y=self.df[amplitude_str].tolist() if self.amplitude_flag else self.df[frequency_str].tolist()
        return min(absolute_y), max(absolute_y)


class GPIO_Channel_Subplot(Base_Channel_Subplot):
    activate_color="#43fa74"

    def __init__(self, file_path, df, ax, min_time, max_time, channel_index, event_index, event_name, start_value):
        super().__init__(file_path, df, ax, min_time, max_time, channel_index, event_index, event_name, start_value)
        self.set_x_y_params_by_col(activate_str)

        self.curr_color=self.activate_color
        self.params_range_dict = GPIO_function_parameters_range_dict

    def set_ylabel(self):
        self.ax.set_ylabel("Ch {}".format(self.channel_index), size=8)

    def set_properties(self):
        self.ax.set_ylim(off_value, on_value)
        self.ax.fill_between(self.x, self.y, color=self.activate_color, step="post")
        if self.event_index==0:
            self.ax.set_yticks([off_value, on_value], size=8)


"""OLD"""
class Channel_Subplot():
    grid_color="#2A3459"


    def __init__(self, file_path, df, ax, min_time, max_time, channel_index, event_index, event_name, start_value, amplitude_flag=True):
        self.file_path = file_path
        self.channel_index=channel_index
        self.init_device_type_from_filename()
        self.df=df
        self.ax=ax
        self.amplitude_flag=amplitude_flag
        self.min_time=min_time
        self.max_time=max_time
        self.event_index=event_index
        self.event_name=event_name
        self.start_value = start_value

        self.init_subset()
        self.set_x_y_params_col()
        self.create_annotation()
        if self.device_type==AOM_str:
            self.params_range_dict = AOM_function_parameters_range_dict
            self.param = amplitude_str if amplitude_flag else frequency_str

        if self.device_type==GPIO_str:
            self.params_range_dict = GPIO_function_parameters_range_dict


    # def on_add(self, selected):
    #     i, j = selected.target.index
    #     selected.annotation.set_text(mapArr[i, j])

    def init_device_type_from_filename(self):
        dirname, filename = os.path.split(self.file_path)
        self.device_type, self.device_index=get_device_channel_tupple(filename)
        if self.device_index!=self.channel_index:
            print("*********Error: self.device_index!=self.channel_index ")


    def init_subset(self):

        self.df_subset = self.df.loc[(self.df[time_str] >= self.min_time) & (self.df[time_str]< self.max_time)]
        self.df_subset = self.df_subset
        if self.df_subset.empty:
            return [], []

    def set_x_y_params_col(self):
        self.is_empty_event=True
        self.x = self.df_subset[time_str].tolist()
        if self.is_AOM_channel():
            self.y = self.df_subset[amplitude_str].tolist() if self.amplitude_flag else self.df_subset[frequency_str].tolist()

        if self.is_GPIO_channel():
            self.y = self.df_subset[activate_str].tolist()
        if len(self.x) and len(self.y):
            self.is_empty_event=False

        self.x.insert(0, self.min_time)
        self.y.insert(0, self.start_value)

        self.end_value=self.y[-1]
        self.x.append(self.max_time)
        self.y.append(self.end_value)

    def get_x_y_params_col(self):
        return self.x, self.y

    def is_AOM_channel(self):
        return True if self.device_type == AOM_str else False

    def is_GPIO_channel(self):
        return True if self.device_type == GPIO_str else False

    def set_ylabel(self):

        if self.is_AOM_channel():
            suffix_len = 3 if self.param == amplitude_str else 4

            self.ax.set_ylabel( "Ch{}\n{}".format(self.channel_index, self.param[:suffix_len].lower()), size=8, rotation=0)
            self.ax.yaxis.set_label_coords(-0.1, 0)
            #self.ax.yaxis.label.set_size(5)
        if self.is_GPIO_channel():
            self.ax.set_ylabel("{} {}".format(self.channel_str, self.channel_index), size=8)

    def event_is_empty(self):
        return True if len(self.x) and len(self.y) else False

    def set_AOM_properties(self):
        min_y, max_y=self.get_min_max_y_values_from_df()

        self.ax.set_ylim(min_y-min_y*self.added_y_perc, max_y+max_y*self.added_y_perc)
        # if self.event_index==0:
        #     self.ax.tick_params(axis='both', which='major', labelsize=8)

    def get_min_max_y_values_from_df(self):
        absolute_y=self.df[amplitude_str].tolist() if self.amplitude_flag else self.df[frequency_str].tolist()
        return min(absolute_y), max(absolute_y)

    def set_gpio_properties(self):
        self.ax.set_ylim(off_value, on_value)
        self.ax.fill_between(self.x, self.y, color=self.activate_color, step="pre")
        if self.event_index==0:
            self.ax.set_yticks([off_value, on_value], size=8)

    def create_annotation(self):
        self.ax.annotate("annot", xy=(0, 0), xytext=(20, 20), textcoords="offset points", color="darkblue",
                            arrowprops=dict(arrowstyle="->"), visible=False,
                            bbox=dict(boxstyle="round", fc="w"), zorder=0)


    def draw_plot(self, row):
        if self.event_index == 0:
            self.set_ylabel()
        if row == 0:
            self.ax.set_title(self.event_name,  fontsize=10)
        #self.ax.grid(color=self.grid_color)

        if self.is_GPIO_channel():
            self.set_gpio_properties()
            curr_color=self.activate_color
        if self.is_AOM_channel():
            curr_color=self.amplitude_color if self.amplitude_flag else self.frequency_color
            self.set_AOM_properties()
        self.ax.set_xlim(self.min_time, self.max_time)
        self.ax.tick_params(axis='both', which='major', labelsize=8)

        self.ax.ticklabel_format(style='scientific')
        if self.event_index!=0:
            self.ax.set_yticks([])


        self.ax.plot(self.x, self.y, drawstyle='steps', color=curr_color)

        # self.ax.spines['top'].set_color('0.9')
        # self.ax.spines['right'].set_color('0.9')


    # def set_active_time_ranges(self):
    #     self.active_time_ranges=[]
    #     self.in_active_range=False
    #     for curr_time, activate_value in zip(self.x, self.y):
    #         if activate_value and not self.in_active_range:
    #             start_active_time=curr_time #open new active range
    #             in_active_range=True
    #         if not activate_value and self.in_active_range:
    #             self.active_time_ranges.append([start_active_time, curr_time]) #save active range
    #             in_active_range=False
