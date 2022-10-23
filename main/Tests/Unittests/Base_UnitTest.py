import unittest
import tkinter
import _tkinter
from main.GUI.Root_Window_with_client import *

import pyautogui as gui
import warnings
import time


class ER_App_Test_Case(unittest.TestCase):

    moving_mouse_duration=0.1
    run_exp_win_name="run_new_exp"
    device_action_win_name="device_action"
    session_win_name="session_window"
    connect_button_name="connect_button"

    x_button_path = add_to_path(widgets_photos_dir, "x_button.png")

    #async def _start_app(self):#check if seperate thread async is needed
    async def _start_app(self):#check if seperate thread async is needed
        self.app.root.mainloop()
        #self.app.root.update()
        self.pump_events()

    def setUp(self) :
        print("in setUp")
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")

            self.app=start_application()
            self._start_app()

        self.app_window=self.app.window
        self.session_window=self.app.get_window_obj(self.app.session_win_name)


    def get_x_y_widget_location(self, widget):
        return widget.winfo_rootx(), widget.winfo_rooty()

    def click_on_widget(self, widget):
        x, y=self.get_x_y_widget_location(widget)
        gui.click(x+10,y+10, duration=self.moving_mouse_duration)

    def press_key(self, key):
        gui.press(key)


    def press_enter(self):
        self.press_key('enter')

    def press_tab(self):
        self.press_key('tab')

    def click_on_main_menu_option(self, req_label, req_submenu):
        win_corner_x=self.app.window.winfo_rootx()
        win_corner_y=self.app.window.winfo_rooty()
        print("menu x {} y {}".format(win_corner_x, win_corner_y))
        experiment_y= win_corner_y -10
        main_menu_labels=[self.app.experiment_str, self.app.device_action_str, self.app.session_str, self.app.help_str]
        for submenu_label, submenu_obj in self.app.labels_menus_dict.items():
            if submenu_label==req_label:
                option=submenu_obj.index(req_submenu)
                print(option)
                print(type(option))
                index_mul_x = (main_menu_labels.index(submenu_label) + 1) * 10
                gui.click(win_corner_x + index_mul_x, experiment_y, duration=self.moving_mouse_duration)
                self.pump_events()
                submenu_index_mul_x = (submenu_obj.index(req_submenu) + 1) * 20
                gui.click(win_corner_x + submenu_index_mul_x, win_corner_y, duration=self.moving_mouse_duration)
                self.pump_events()


    def raise_above_all(self, window_obj):
        #window_obj.attributes('-topmost', 1)
        window_obj.attributes('-topmost', 0)

    def pump_events(self):
        while self.app.root.dooneevent(_tkinter.ALL_EVENTS | _tkinter.DONT_WAIT):
            pass

    def x_click(self):
        location = gui.locateOnScreen(self.x_button_path)
        gui.click(location)

    def tearDown(self):
        self.app.window.destroy()
        self.pump_events()

        #self.app.window.update()

