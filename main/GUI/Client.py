import os
import re
import threading
import socket
import time
import traceback
import datetime

from main.Configuration_files.session_configuration import *
from main.GUI.Function_Setting import *
from main.Session.Command_Packet import *
from main.GUI.Queue_Item import *
from main.GUI.Upload_New_Experiment_Window import Upload_New_Experiment

from time import (
    process_time,
    perf_counter,
    sleep,
)

import errno

class Client():
    connect_flag = False
    socket_timeout=2
    wait_for_control_sec=3

    con_success_title = "Connected To Control"
    con_success_format = "Connected successfully to the control: \n\n" \
                         "Connection Time: {}\nHost: {}\nPort: {} \nUsername: {}\n"
    func_err_title = "Control Respond Error"
    func_err_txt_format = "Control doesn't respond to function {}:\n\n"

    received_messages = ""
    sent_messages = ""

    con_error_title = "Error connection to control"
    con_error_msg = "Error connecting to control:\n\n{}"

    received_error_title = "Error receiving from control"
    received_error_msg = "Error receiving from control:\n\n{}"

    send_error_title = "Error sending to control"
    send_error_msg = "Error sending to control:\n\n{}"
    stop_send_err_msg="\n\nThe experiment stopped"

    handle_con_error_title = "Error handling the commands queue or the tcp connection"
    handle_con_error_msg = "Error handling the commands queue or the tcp connection: \n\n{}"
    restart_connection_err_mgs="\n\nDo you want to restart the connection to the control?"

    start_default_exp_title = "Starting default sequence"
    start_default_exp_msg = "Do you want to run the default sequence?\n\n{}".format(default_dir_path)

    stop_unexist_exp_err_title ="Stop error no experiment running"
    stop_unexist_exp_err_msg = "Stop experiment error: no experiment is currently running"

    illegal_queue_cmd_title="Invalid command name"
    illegal_queue_cmd_msg="Command name: {} is invalid queue command"

    recv_error_title="Error in receiving from control"
    recv_error_msg="Error in receiving from control: \n\n{}"
    terminate_exp_msg="\n\nExperiment terminated"
    ack_err_msg= "Start packet has not received from control"

    err_default_dir_format_title="Error in default sequence format"
    err_default_dir_format_msg="Error in default sequence format: \n[}"

    start_exp_name="START EXPERIMENT"
    stop_exp_name="STOP EXPERIMENT"
    set_GPIO_name="SET_GPIO"
    set_AOM_name="SET_AOM"

    control_ack_header=b'\xaa'
    control_start_ack=b'\x00\x00\x00\x00'
    control_stop_ack=b'\x00\x00\x00\x01'
    control_stop_ack_for_initial=b'\x00\x00\x00\xff'

    stop_for_initial_flag=True

    get_from_queue_time=0.01
    lock = threading.Lock()

    start_time = time.time_ns()
    times_measure_output_file=add_to_path(config_dir, "Time_measurement_256_packets_in_nano.txt")
    f_times = open(times_measure_output_file, "w")
    f_times.write("start")

    last_dir_path=None
    last_iteration_num=None
    last_cycle_time=None

    def __init__(self, app):
        self.app = app
        self.initial_client_configures()
        self.functions_settings_dict = create_functions_settings_names_dict(functions_settings_lst)

    def initial_client_configures(self):
        self.address_family = address_family
        self.socket_type = socket_type
        self.format = format
        self.server_host = server_host
        self.port = port
        self.BUFFERSIZE = BUFFERSIZE
        self.server_messages = server_messages
        self.username = username
        self.password = password

    def connect_client(self):
        try:
            address = (self.server_host, self.port)
            self.client_socket = socket.socket(self.address_family, self.socket_type)
            self.client_socket.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)

            self.client_socket.connect(address)
            self.client_socket.settimeout(self.socket_timeout)

            self.con_time=self.get_current_time_str()

            con_suc_msg=self.con_success_format.format(self.con_time, self.server_host, self.port, self.username)
            self.app.show_info_msg(self.con_success_title, con_suc_msg)
            self.app.connected_success_func()


            self.tcp_thread = threading.Thread(target=self.handle_tcp_thread_func, daemon=True)
            self.tcp_thread.start()
            self.app.insert_stop_experiment_command_to_queue()#check with Meni the implementation
            self.start_default_experiment_command()


        except Exception as err:
            self.app.connection_failed_func(self.con_error_title, self.con_error_msg.format(err))

            print(traceback.format_exc())
            #self.client_socket.close()

    def start_default_experiment_command(self):
        if self.app.get_ok_cancel_by_msg(self.start_default_exp_title, self.start_default_exp_msg):
            print("start_default_experiment_command")
            valid_def, valid_msg=self.get_validation_of_file(default_flag=True)
            if valid_def:
                start_exp_args={experiment_state_field_name : start_exp_dec_op_code,
                                dir_path_field_name: default_dir_path,
                                iterations_num_field_name:str_value_iterations_dict[infinite_iteration_txt],
                                cycle_time_field_name: default_cycle_time}

                current_queue_command = Queue_Item(start_exp_name, start_exp_args)
                self.app.insert_to_queue(current_queue_command)
                print("after insert to queue")
                print("current queue {}".format(current_queue_command))

            else:
                self.app.show_err_msg(self.err_default_dir_format_title, self.err_default_dir_format_msg.format(valid_msg))
                self.app.stop_experiment()

            # else:
            #     trace=valid_msg[:100]+"..." if len(valid_msg)>100 else valid_msg
            #     self.app.show_err_msg(self.err_default_dir_format_title, self.err_default_dir_format_msg.format(trace))

    def get_validation_of_file(self, default_flag=False, restart_flag=False, external_path=None):
        validate_window_hided = Upload_New_Experiment(self.app, default_flag=default_flag, restart_flag=restart_flag, external_uploaded_path=external_path)
        valid_msg = validate_window_hided.get_validatation_message_of_dir_format()
        print("valid msg")
        print(valid_msg)
        valid_def = True if valid_msg == validate_window_hided.valid_message_str else False
        validate_window_hided.create_experiment_df()
        validate_window_hided.window.destroy()
        valid_def = True if valid_msg == validate_window_hided.valid_message_str else False
        return valid_def, valid_msg

    def handle_tcp_thread_func(self):
        while True:
            while self.app.send_queue.empty():
                time.sleep(self.get_from_queue_time)

            self.execute_command_from_queue()

    def execute_command_from_queue(self):
        print("in execute_command_from_queue")
        try:
            if not self.app.send_queue.empty():
                print("in not empty")
                curr_queue_item = self.app.send_queue.get_nowait()
                curr_cmd_name = curr_queue_item.name
                match curr_cmd_name:

                    case self.stop_exp_name:
                        self.stop_exp_func()

                    case self.set_GPIO_name:
                        self.set_GPIO_func_from_queue(curr_queue_item)

                    case self.set_AOM_name:
                        self.set_AOM_func_from_queue(curr_queue_item)

                    case self.start_exp_name:
                        self.start_exp_func(curr_queue_item)

                    case other:
                        self.app.show_err_msg(self.illegal_queue_cmd_title, self.illegal_queue_cmd_title.format(other))

        except Exception as e:
            print(traceback.format_exc())
            restart_flag = self.app.get_ok_cancel_by_msg(self.handle_con_error_title,
                                                                self.handle_con_error_msg.format(e) + self.restart_connection_err_mgs)
            if restart_flag:
                self.app.restart_app()


    def start_exp_func(self, curr_queue_item):
        print("in start exp func")
        if not self.app.experiment:
            self.app.initial_experiment(curr_queue_item.get_dir_path(), curr_queue_item.get_iter_num(),
                                        curr_queue_item.get_cycle_time())
            experiment_state = curr_queue_item.get_exp_state()
            params_lst = [experiment_state]
            self.send_to_control(set_exp_state_dec_op_code, "B", params_lst)
            self.start_exp_func(curr_queue_item)

        else:
            try:
                print("in try to recevice packet")
                #recv_packet=self.get_received_packet_from_control("B")
                #if recv_packet.is_start_experiment_packet(): for packet implementation
                start_exp_flag=self.is_got_ack_from_control([self.control_start_ack])
                print("start_exp_flag {}".format(start_exp_flag))
                if start_exp_flag:
                    self.app.start_experiment()
                    self.app.experiment.start_experiment_runner()
                else:
                    print("printing error msg and stop function")
                    print(self.recv_error_msg.format(self.ack_err_msg))
                    self.app.show_err_msg(self.recv_error_title, self.recv_error_msg.format(self.ack_err_msg))
                    self.app.stop_experiment()

            except Exception as e:
                self.app.show_err_msg(self.recv_error_title, self.recv_error_msg.format(e))
                print(traceback.format_exc())
                self.app.stop_experiment()



    def stop_exp_func(self):
        try:
            if self.stop_for_initial_flag: #if it is the stop sent for initial the system state
                self.is_stop_ack_sent_and_received(initial_flag=self.stop_for_initial_flag)
                self.stop_for_initial_flag=False
            else:
                if not self.app.experiment:
                    self.app.show_err_msg(self.stop_unexist_exp_err_title, self.stop_unexist_exp_err_msg)
                else:
                    self.app.experiment.stop_exp_flag = True
                    self.app.experiment.return_to_initial_state() #return to the state in time 0
                    print("self.app.experiment.got_stop_exp_flag= {}".format(self.app.experiment.stop_exp_flag))
                    self.app.experiment.stop_exp_flag=self.is_stop_ack_sent_and_received()
                    print("in else: {} ".format(self.app.experiment.stop_exp_flag))
                print("before self.app.stop_experiment()")
                self.app.stop_experiment()

        except Exception as e:
            self.app.show_err_msg(self.recv_error_title, self.recv_error_msg.format(str(e)+self.terminate_exp_msg))
            print(traceback.format_exc())
            self.app.stop_experiment()

    def is_stop_ack_sent_and_received(self, initial_flag=False):
        self.send_to_control(set_exp_state_dec_op_code, "B", [1])
        #req_stop_ack=self.control_stop_ack_for_initial if initial_flag else self.control_stop_ack
        req_stop_ack_lst=[self.control_stop_ack_for_initial, self.control_stop_ack]
        received_stop_flag = self.is_got_ack_from_control(req_stop_ack_lst)
        print("received_stop_flag {}".format(received_stop_flag))
        if not received_stop_flag:
            self.app.show_err_msg(self.recv_error_title, self.recv_error_msg.format(self.ack_err_msg))
        return received_stop_flag



    def send_to_control(self, op_code, params_format, params_lst):
        with self.lock:
            try:
                # print("in send to control")
                if self.app.sent_packets_index == 256:
                    self.app.sent_packets_index = 0

                    print(self.app.sent_packet_total_time)
                    self.f_times.write(str(self.app.sent_packet_total_time) + "\n")

                    self.app.sent_packet_total_time = 0

                packet = Sent_Packet(op_code, params_format, tuple(params_lst), self.app.sent_packets_index)
                start_time = time.perf_counter_ns()
                size_sent=self.client_socket.send(packet.packed_data)  # send return the number of data sent. Can be asserted by calcsize
                stop_time = time.perf_counter_ns()
                # self.sent_messages += "{} sent packet: {}\n".format(self.get_current_time_str(), packet)
                self.app.sent_packets_index += 1
                self.app.sent_packet_total_time += (stop_time - start_time)


            except Exception as e:
                print(traceback.format_exc())
                self.app.show_err_msg(self.send_error_title, self.send_error_msg.format(e) + self.stop_send_err_msg)
                self.stop_exp_func()


    def is_got_ack_from_control(self, req_msg_lst):
        start_time = time.time()
        current_time = time.time()
        while current_time - start_time < self.wait_for_control_sec:
            msg = self.get_received_msg_from_control()
            print("mgs in while")
            print(msg)
            print(req_msg_lst)
            if any(req_msg in msg for req_msg in req_msg_lst):
                print("in if self.control_ack in msg")
                return True
            current_time = time.time()
        return False

    def set_GPIO_func_from_queue(self, curr_queue_item):
        print("set GPIO from queue")
        channel_index = curr_queue_item.args[channel_index_field_name]
        channel_value = curr_queue_item.args[set_function_param_str]
        params_lst=[channel_index, channel_value]
        self.send_to_control(set_GPIO_imm_op_code, set_GPIO_format, params_lst)

    def set_AOM_func_from_queue(self, curr_queue_item):
        print("in set aom from queue")
        channel_index = curr_queue_item.args[channel_index_field_name]
        params_to_configure = curr_queue_item.args[params_config_field_name]
        first_param = curr_queue_item.args[first_param_field_name]

        params_lst=[channel_index, params_to_configure, first_param]
        if params_to_configure==two_params_to_config:
            params_lst.append(curr_queue_item.args[second_param_field_name])
            format=set_aom_format_two_params
        else:
            format = set_aom_format
        self.send_to_control(set_AOM_imm_op_code, format, params_lst)
        print("send_to_control(set_AOM_imm_op_code, format, params_lst)")

    def get_received_msg_from_control(self):
        recv_msg = self.client_socket.recv(self.BUFFERSIZE)
        print("recv_msg")
        print(recv_msg)
        return recv_msg


    def get_received_packet_from_control(self, params_format):
        recv_msg = self.client_socket.recv(self.BUFFERSIZE)
        print("recv_msg")
        print(recv_msg)
        return Received_Packet(recv_msg, params_format)

    def get_functions_setting_obj(self, function_str):
        return self.functions_settings_dict[function_str]

    def get_current_time_str(self):
        return time.ctime(time.time())

    def close_client(self):
        self.client_socket.close()
        self.set_control_flag_on = False

