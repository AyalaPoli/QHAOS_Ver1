from dataclasses import dataclass
from main.GUI.Function_Setting import *

@dataclass
class Queue_Item():
    name: str
    args: dict=None

    #for start exp name
    def get_exp_state(self):
        if self.name == start_exp_name or self.name == stop_exp_name:
            return self.args[experiment_state_field_name]

    def get_dir_path(self):
        if self.name==start_exp_name:
            return self.args[dir_path_field_name]

    def get_iter_num(self):
        if self.name==start_exp_name:
            return self.args[iterations_num_field_name]

    def get_cycle_time(self):
        if self.name==start_exp_name:
            return self.args[cycle_time_field_name]
