import tkinter as tk
import customtkinter as ctk
from tkinter import messagebox
from main.GUI.GUI_params import *
import pyautogui as gui

class Base_Window(object):


    curr_title = "Quantum Source Software"
    device_actions_window_msg = "Base Window Message"
    window_width = 600
    window_height = 400
    rows_weights_dict={0:1}
    columns_weights_dict={0:1}

    frames_padx = 10
    frames_pady = 10

    label_padx =5
    label_pady =5

    buttons_padx = 10
    buttons_pady = 10

    buttons_font_size=10
    button_txt="Base Button Text"
    sticky="nw"

    label_txt="Base Window Label"
    root_color=['#EBEBEC', '#212325']
    #root_color="white"

    is_window_open=True

    def __init__(self, parent):
        self.parent=parent
        self.window=ctk.CTkToplevel(parent)
        self.window.winfo_toplevel().title(self.curr_title)
        self.buttons_font = tk.font.Font(size=self.buttons_font_size)
        self.window.iconbitmap(icon_file)
        self.define_window_position()
        self.configure_grid_weights()
        self.window.protocol("WM_DELETE_WINDOW", self.close_window)


    def define_window_position(self):
        screen_width=self.window.winfo_screenwidth()
        screen_height=self.window.winfo_screenheight()
        center_x = int(screen_width / 2 - self.window_width / 2)
        center_y = int(screen_height / 2 - self.window_height / 2)
        self.window.geometry(f'{self.window_width}x{self.window_height}+{center_x}+{center_y}')

    def configure_grid_weights(self):
        for curr_index, curr_weight in self.rows_weights_dict.items():
            self.window.rowconfigure(curr_index, weight=curr_weight)
        for curr_index, curr_weight in self.columns_weights_dict.items():
            self.window.columnconfigure(curr_index, weight=curr_weight)

    def build_button(self, frame, txt, func, row, column, padx=None, pady=None, sticky=None):
        curr_button=ctk.CTkButton(frame, text=txt, command=func, border_width=1, border_color='black')
        curr_button['font'] = self.buttons_font
        padx, pady, sticky=self.get_config_widget_params(padx, pady, sticky)
        curr_button.grid(row=row, column=column, sticky=sticky, padx=padx, pady=pady)
        return curr_button

    def build_frame(self, parent, row, column, padx=frames_padx, pady=frames_pady, sticky=None):
        curr_frame = ctk.CTkFrame(parent)
        padx, pady,sticky=self.get_config_widget_params(padx, pady, sticky)
        curr_frame.grid(row=row, column=column, sticky=sticky, padx=padx, pady=pady)
        return curr_frame

    def build_label(self, frame, txt, row, column, padx=label_padx, pady=label_pady, sticky=None):
        # fg_color="whitesmoke",  bg="gainsboro"
        curr_label=ctk.CTkLabel(frame, text=txt)
        padx, pady, sticky=self.get_config_widget_params(padx, pady, sticky)
        curr_label.grid(row=row, column=column, sticky=sticky, padx=padx, pady=pady)
        curr_label.configure(background="gainsboro")

        return curr_label

    def build_listbox(self, frame, lst, row, column, select_set_val, func, padx=None, pady=None, sticky=None, selected=True):
        #devices_types_listbox_index_dict = self.build_listbox_index_dict(device_types_lst)
        stringvar = tk.StringVar(value=lst)
        curr_listbox=tk.Listbox(master=frame, listvariable=stringvar, exportselection=False)
        padx, pady, sticky=self.get_config_widget_params(padx, pady, sticky)

        curr_listbox.grid(row=row, column=column, sticky=sticky, padx=padx, pady=pady)
        print("select set val")
        print(select_set_val)
        if selected:
            print("in if select set")
            curr_listbox.select_set(select_set_val)
        #self.devices_listbox.activate(self.devices_types_listbox_index_dict[self.device_obj.device_type])
        #self.devices_listbox.select_set(self.devices_types_listbox_index_dict[self.device_obj.device_type])

        curr_listbox.bind('<<ListboxSelect>>', func)
        return curr_listbox

    def build_radiobutton(self, frame, txt, row, column, stringVar, val, func, padx=None, pady=None, sticky=None):
        curr_radiobutton=ctk.CTkRadioButton(frame, text=txt, variable=stringVar, value=val, command=func)
        padx, pady, sticky=self.get_config_widget_params(padx, pady, sticky)
        curr_radiobutton.grid(row=row, column=column, sticky=sticky, padx=padx, pady=pady)
        curr_radiobutton.deselect()
        return curr_radiobutton

    def build_entry(self, frame, textvar, func, row, column, padx=None, pady=None, sticky=None):
        curr_entry=ctk.CTkEntry(frame, textvariable = textvar)
        padx, pady, sticky=self.get_config_widget_params(padx, pady, sticky)
        curr_entry.grid(row=row, column=column, sticky=sticky, padx=padx, pady=pady)
        curr_entry.bind("<Return>", func)
        curr_entry.configure(background="gainsboro")
        return curr_entry

    def change_widget_config(self, widget, param, val):
        widget[param]=val

    def change_widget_state(self, widget, activate=True):
        if activate:
            widget.configure(state=tk.NORMAL)
        else:
            widget.configure(state=tk.DISABLED)

    def click_on_button(self, widget):
        gui.moveTo(widget.winfo_rootx(), widget.winfo_rooty(), duration=1)
        gui.click()

    def get_config_widget_params(self, padx, pady, sticky):
        padx=self.check_default_val(padx, self.buttons_padx)
        pady=self.check_default_val(pady, self.buttons_pady)
        sticky=self.check_default_val(sticky, self.sticky)
        return padx, pady, sticky

    def check_default_val(self, val, default):
        return val if val else default

    def show_err_msg(self, title, msg):
        tk.messagebox.showerror(title, msg)

    def show_info_msg(self, title, msg):
        tk.messagebox.showinfo(title, msg)

    def get_ok_cancel_by_msg(self, title, msg):
        return tk.messagebox.askokcancel(title, msg)

    def set_button_size(self, button_obj, height, width):
        button_obj.configure(height = height, width = width)

    def close_window(self):
        if hasattr(self, "app"):
            self.app.remove_window_obj(self.curr_title)
        self.window.destroy()