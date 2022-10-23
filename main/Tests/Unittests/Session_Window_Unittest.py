from main.Tests.Unittests.Base_UnitTest import *

class Session_Window_TestCase(ER_App_Test_Case):

    def click_connect(self):
        super().click_on_widget(self.session_window.connect_button)

    def     \
            test_check_connection_credentials(self):
        # self.app.root.update()
        # self.app.root.update_idletasks()
        self.pump_events()

        #super().raise_above_all(self.session_window.window)
        #self.session_window.window.focus_set()
        self.click_connect()
        #.pump_events()
        #self.x_click()

        #self.pump_events()
        #super().press_enter()
        self.pump_events()


        #super().press_tab()
        #self.pump_events()

        #super().press_enter()
        #self.pump_events()

        super().click_on_main_menu_option(self.app.experiment_str, self.app.run_new_exp_txt)
        self.pump_events()

        #super().press_enter()
        #self.curr_window=self.app
        #assertNotIn(a, b)
        #super().click_on_widget(getattr(self.app, self.app.run_new_exp_txt))
        #but=super().get_button_from_main_menu("main_menu_bar").

if __name__ == '__main__':
    unittest.main()







