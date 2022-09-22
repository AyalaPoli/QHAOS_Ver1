from main.GUI.Base_Window import *
import webbrowser

class Help_Window(Base_Window):
    curr_title = 'Help'
    window_width = 500
    window_height = 150
    rows_weights_dict = {0: 1, 1: 1, 2:1}
    columns_weights_dict = {0: 1, 1: 1}

    sticky = "nw"
    padx = 5
    pady = 5
    document_label_txt= "Software documentation and user manual:"
    document_link_txt ="QHAOS wiki"
    document_link_address="https://teams.microsoft.com/l/channel/19%3Ad4q3N4IHz3-BtEn51wlFmG9xGUsAYZxHl2gBrLre7iY1%40thread.tacv2/tab%3A%3A329c6cb2-7229-4ded-8e7c-3bdb3140eb83?groupId=66d72667-9e46-46f1-90e4-760f5c5bae3e&tenantId=0fdcbfa7-0ddd-45bf-9396-fa51b2356d28&allowXTenantAccess=false"

    issues_label_txt= "Report bugs and track issues:"
    issues_link_txt="QHAOS - Bugs and Requests"
    issues_link_address="https://teams.microsoft.com/l/channel/19%3add4b5b3ecece4afc953fc3aa946a8637%40thread.tacv2/Qhaos%2520-%2520Bugs%2520and%2520requests?groupId=439ae883-c0f5-4c25-83ee-979df035d1c6&tenantId=0fdcbfa7-0ddd-45bf-9396-fa51b2356d28"

    contact_label_txt= "Please contact Ayala for any queries"

    got_it_button="Got it"

    def __init__(self, app):
        self.app = app
        super().__init__(app.root)

        self.create_link_section(self.document_label_txt, self.document_link_txt, self.document_link_address, 0)
        self.create_link_section(self.issues_label_txt, self.issues_link_txt, self.issues_link_address, 1)
        ok_button=super().build_button(self.window, self.got_it_button, self.button_cmd, 2,0, sticky="N")
        ok_button.grid(columnspan=2)

    def create_link_section(self, label_txt, link_txt, address, row):
        super().build_label(self.window, label_txt, row, 0, sticky=self.sticky)
        curr_label=tk.Label(self.window, text=link_txt)
        curr_label.configure(fg="blue", cursor="hand2")
        curr_label.grid(row=row, column=1, sticky=self.sticky, padx=5, pady=5)
        curr_label.bind("<Button-1>", lambda e: self.callback(address))

    def callback(self, address):
        print("in callback")
        webbrowser.open_new(address)

    def button_cmd(self):
        self.window.destroy()