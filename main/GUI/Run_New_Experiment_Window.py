import tkinter as tk
from main.GUI.Upload_New_Experiment_Window import *
from main.GUI.GUI_params import *
from main.GUI.Base_Window import Base_Window
from main.GUI.Function_Setting import start_exp_name
from main.GUI.Queue_Item import *
from main.GUI.Function_Setting import *

class Run_New_Experiment(Base_Window):

    #buttons_font_size=10
    sticky="nsew"

    curr_title = 'Run New Experiment'
    window_width = 600
    window_height = 600
    new_experiment_window_msg = "This window controls the experiment run"

    other_run_exp_title="Another experiment is running"
    other_run_exp_msg="Another experiment is already running\n{}"

    upload_dir_button_txt = "Upload Experiment Directory"
    default_seq_button_txt = "Start Default Sequence"
    start_again_button_txt = "Restart Last Sequence Again"
    #visualize_file_button_txt = "File Visualization"

    start_experiment_txt = "Start Experiment"
    stop_experiment_txt = "Stop Experiment"

    output_dir=add_to_path(config_dir,"temp_output.txt")

    #info_label_txt_format = "Uploaded Experiment Directory: \n{}\nExperiment iteration number:{}"
    #info_wraplength=200
    #device_configuration_experiment_txt = "Device Configuration"

    no_dir_uploaded_txt="There is no uploaded directory. Press \"Upload\" to select your experiment directory."
    dir_upload_txt= "The following experiment directory was uploaded: \n{}. \n\nPress \"Start Experiment\" to run the experiment.\n\n"

    err_last_dir_format_title="Error in last sequence format"
    err_last_dir_format_msg="Error in last sequence format: \n[}"

    exp_start_txt="The following experiment directory is running: \n{}. \nPress \"Stop Experiment\" to permanently stop the execution.\n"
    exp_stop_txt="The experiment directory was stopped.\nThe experiment output found here:\n{}.\n\nPress " \
                 "\"Upload\" to select the next experiment directory.\n".format(output_dir)

    no_prev_exp_title="An experiment has not been uploaded"
    no_prev_exp_msg="An experiment has not been uploaded yet"

    restart_exp_title="Restart a sequence"
    restart_exp_msg="Restart the last sequence: {}\nIteration: {}\nCycle_time: {}." \
                    "\n\nNote: restart includes the changes have beening made to the directory"

    run_iter_txt="Current experiment iteration: {} mod {} billion"



    rows_weights_dict={0:1, 1:20, 2:5}
    columns_weights_dict={0:1}

    def __init__(self, app):
        self.app=app
        super().__init__(app.window)

        new_experiment_label=super().build_label(self.window, self.new_experiment_window_msg, 0, 0, sticky="W")
        #super().change_widget_config(new_experiment_label, "bg", "white")
        new_experiment_label.grid(columnspan=3)

        self.upload_dir_frame()
        #self.build_visualization_file_frame()
        self.build_experiment_buttons_frame()

        self.hidden_flag=False

    def upload_dir_frame(self):

        self.upload_dir_frame=super().build_frame(self.window, 1, 0)
        super().change_widget_config(self.upload_dir_frame, "borderwidth", 1)
        self.initial_window_params_by_running_exp()
        exp_status_txt=self.uploaded_experiment_msg if self.app.experiment else self.no_dir_uploaded_txt
        self.experiment_status=super().build_label(self.upload_dir_frame, exp_status_txt, 0, 0, sticky="W")
        if self.app.experiment:
            self.build_running_iteration_label()

        super().change_widget_config(self.experiment_status, 'font', self.buttons_font)
        super().change_widget_config(self.experiment_status, 'anchor', "w")
        self.experiment_status.grid(columnspan=1)

        self.create_upload_new_dir_button()
        super().change_widget_config(self.upload_new_dir_button, 'font', self.buttons_font)
        self.create_start_default_dir_button()
        self.create_start_again_button()


    def initial_window_params_by_running_exp(self):
        if self.app.experiment:
            self.dir_path = self.app.experiment.input_dir_path
            self.iteration_num = self.app.experiment.iteration_num
            self.cycle_time = self.app.experiment.cycle_time
            self.set_exp_msg_info_str(self.dir_path,  self.iteration_num, self.cycle_time, uploaded=False)

    def create_upload_new_dir_button(self):
        self.upload_new_dir_button=super().build_button(self.upload_dir_frame, self.upload_dir_button_txt,
                                                        self.open_upload_experiment_file_window, 2, 0)
        #if self.app.experiment:
        #    super().change_widget_state(self.upload_new_dir_button, activate=False)

    def create_start_default_dir_button(self):
        self.start_default_dir_button=super().build_button(self.upload_dir_frame, self.default_seq_button_txt,
                                                        self.start_default_seq_cmd, 3, 0)

        #if self.app.experiment:
        #    super().change_widget_state(self.start_default_dir_button, activate=False)

    def create_start_again_button(self):
        self.start_again_button=super().build_button(self.upload_dir_frame, self.start_again_button_txt,
                                                        self.start_again_seq_cmd, 4, 0)


    def open_upload_experiment_file_window(self):
        Upload_New_Experiment(self)

    def start_default_seq_cmd(self):
        self.app.client.start_default_experiment_command()

    def start_again_seq_cmd(self):
        if not self.app.client.last_dir_path:
            super().show_info_msg(self.no_prev_exp_title, self.no_prev_exp_msg)
        else:

            valid_def, valid_msg = self.app.client.get_validation_of_file(restart_flag=True)
            if valid_def:
                #self.show_info_msg(self.restart_exp_title, self.restart_exp_msg.format(self.app.client.last_dir_path,
                #                                                                       self.app.client.last_iteration_num,
                #                                                                       self.app.client.last_cycle_time))
                start_exp_args = {experiment_state_field_name: start_exp_dec_op_code,
                                  dir_path_field_name: self.app.client.last_dir_path,
                                  iterations_num_field_name: self.app.client.last_iteration_num,
                                  cycle_time_field_name: self.app.client.last_cycle_time}
                current_queue_command = Queue_Item(start_exp_name, start_exp_args)
                self.app.insert_to_queue(current_queue_command)
                #print("after insert to queue")
                #print("current queue {}".format(current_queue_command))

            else:
                self.app.show_err_msg(self.err_last_dir_format_title,
                                      self.err_last_dir_format_msg.format(valid_msg))


    def visualize_file_command(self):
        print("visualize_file_command")

    def build_experiment_buttons_frame(self):
        experiment_buttons_frame=super().build_frame(self.window, 2, 0)
        #super().change_widget_config(experiment_buttons_frame, "bg", "white")

        self.start_experiment_button=super().build_button(experiment_buttons_frame, self.start_experiment_txt,
                                                          self.start_experiment_command, 0, 0, pady=5, sticky="nsew")
        self.stop_experiment_button=super().build_button(experiment_buttons_frame, self.stop_experiment_txt,
                                                          self.stop_experiment_button_command,
                                                         0, 1, pady=5, sticky="nsew")
        super().change_widget_config(self.start_experiment_button, 'font',  self.buttons_font)
        super().change_widget_config(self.stop_experiment_button, 'font',  self.buttons_font)

        super().change_widget_state(self.start_experiment_button, activate=False)

        if not self.app.experiment:
            super().change_widget_state(self.stop_experiment_button, activate=False)

        #super().change_widget_config(self.stop_experiment_button, "state", tk.DISABLED)
        #uploaded_experiment_label=super().build_label(self.window, self.new_experiment_window_msg, 0, 0, sticky="nsew")


    def set_exp_msg_info_str(self, dir_path, iter_num, cycle_time, uploaded=True):
        prefix=self.dir_upload_txt if uploaded else self.exp_start_txt
        self.uploaded_experiment_msg= prefix.format(dir_path)
        self.uploaded_experiment_msg += self.get_dir_devices_and_channels_str()
        iter_str = get_val_by_dict(str_value_iterations_dict, iter_num)
        self.uploaded_experiment_msg += "\nIterations  :{}\n".format(iter_str)
        self.uploaded_experiment_msg += "\nTotal time of each Iteration: {}\n".format(cycle_time)

    def change_experiment_info_details_after_upload(self, dir_path, iteration_num, cycle_time):
        self.dir_path=dir_path
        self.iteration_num=iteration_num
        self.cycle_time=cycle_time

        self.upload_new_dir_button.destroy()
        self.start_default_dir_button.destroy()
        self.start_again_button.destroy()
        super().change_widget_state(self.start_experiment_button)
        self.set_exp_msg_info_str(dir_path, iteration_num, cycle_time)
        self.experiment_status.configure(text=self.uploaded_experiment_msg)



    def change_widgets_after_start_exp(self):
        self.initial_window_params_by_running_exp()
        self.experiment_status.configure(text=self.set_exp_msg_info_str(self.app.experiment.input_dir_path,
                                                                        self.app.experiment.iteration_num,
                                                                        self.app.experiment.cycle_time, uploaded=False))
        self.switch_experiment_buttons_state(is_start=True)

        self.build_running_iteration_label()

    def build_running_iteration_label(self):
        self.running_iteration_label=super().build_label(self.upload_dir_frame,
                                                         self.run_iter_txt.format(self.app.experiment.iter_count, self.app.experiment.rem),
                                                         1, 0, sticky="W")

    def update_running_iteration_num_label(self, new_iter_num, rem):
        print(self.running_iteration_label)
        self.running_iteration_label.configure(text=self.run_iter_txt.format(new_iter_num, rem))

    def change_experiment_info_details_after_stop(self):
        self.experiment_status.configure(text=self.exp_stop_txt)

    def change_widgets_after_stop_exp(self):
        self.change_experiment_info_details_after_stop()
        self.create_upload_new_dir_button()
        self.create_start_default_dir_button()
        self.create_start_again_button()
        super().change_widget_state(self.start_experiment_button, activate=False)
        super().change_widget_state(self.stop_experiment_button, activate=False)


    def get_dir_devices_and_channels_str(self):
        dev_channel_dict = {dev: [] for dev in device_choices}

        for input_file in os.listdir(self.dir_path):
            device, channel = get_device_channel_tupple(input_file)
            dev_channel_dict[device].append(channel)

        return "\n".join(["{}: {}".format(dev, ", ".join(chan_lst)) for dev, chan_lst in dev_channel_dict.items()])

    def switch_experiment_buttons_state(self, is_start=True):
        (button_to_disable, button_to_normal)=(self.start_experiment_button, self.stop_experiment_button) if is_start \
            else (self.stop_experiment_button, self.start_experiment_button)

        #super().change_widget_config(button_to_disable, "state", tk.DISABLED)
        super().change_widget_state(button_to_disable, activate=False)

        #super().change_widget_config(button_to_normal, "state", tk.NORMAL)
        super().change_widget_state(button_to_normal)

    def start_experiment_command(self):
        if self.app.experiment:
            self.app.show_info_msg(self.other_run_exp_title, self.other_run_exp_msg.format(self.app.experiment.input_dir_path))
        else:
            start_exp_args={experiment_state_field_name : start_exp_dec_op_code, dir_path_field_name: self.dir_path,
                                                                iterations_num_field_name:self.iteration_num, cycle_time_field_name:self.cycle_time}
            current_queue_command = Queue_Item(start_exp_name, start_exp_args)
            self.app.insert_to_queue(current_queue_command)

    def stop_experiment_button_command(self):
        self.app.client.stop_exp_func()



    # def close_window(self):
    #     print("****in close window")
    #     self.window.withdraw()
    #     self.hidden_flag=True

    # def build_visualization_file_frame(self):
    #     self.visualize_center_frame=super().build_frame(self.window, 1, 1)
    #     super().change_widget_config(self.visualize_center_frame, "bg", 'cornsilk')
    #     super().change_widget_config(self.visualize_center_frame, "borderwidth", 1)
    #     visulaize_file_button=super().build_button(self.visualize_center_frame, visualize_file_button_txt,
    #                                                self.visualize_file_command, 0, 0)
    #     super().change_widget_config(visulaize_file_button, "font", self.buttons_font)
    #     super().change_widget_config(visulaize_file_button, "state", tk.DISABLED)