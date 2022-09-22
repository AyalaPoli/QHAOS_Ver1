from main.GUI.GUI_params import *

def get_screen_dimension(root):
    return root.winfo_screenwidth(), root.winfo_screenheight()

def get_center_point(screen_width, window_width, screen_height, window_height):
    center_x = int(screen_width / 2 - window_width / 2)
    center_y = int(screen_height / 2 - window_height / 2)
    return center_x, center_y

def define_window_position(window, window_width, window_height):
    #based on https://www.pythontutorial.net/tkinter/tkinter-window/

    screen_width, screen_height=get_screen_dimension(window)
    center_x, center_y=get_center_point(screen_width, window_width, screen_height, window_height)
    window.geometry(f'{window_width}x{window_height}+{center_x}+{center_y}')



