from . import common
from datetime import datetime as dt

class Qct:
    def __init__(self):
        self.header = {}
        self.results_text = {}
        self.results_pass = {}
    
    def init_header(self, formnumber, docnumber, username):
        self.header['username'] = username
        self.header['formnumber'] = formnumber
        self.header['docname'] = "%s-%s" % (docnumber, formnumber)
        self.header['testdate'] = dt.today().strftime("%Y-%m-%d")

    def test_step(self, step_no, result, passmsg, failmsg, alert=None):
        """
        Updates the qct results dictionaries according to the results of the test step that
        is performed.
    
        step_no: string, unique step identifier from results form template
        result: boolean, results of the test step action - True = pass, False = fail
        passmsg: string, text to appear on results form if step is passed
        failmsg: string, text to appear on results form if step is failed
        alert: string, default None, optional message to user if step test fails
        """
        while True:
            if result:
                self.results_text[step_no] = passmsg
                self.results_pass[step_no] = True
                return True
            elif common.userpassanyway(alert):
                result = True
            else:
                self.results_text[step_no] = failmsg
                self.results_pass[step_no] = False
                common.usercancelled()
                return True

    def user_confirm_value_no_prompt(self, value_dict):
        """
        Display one or more values along with an alert message prompting user to self-
        verify. Does not wait for user action.
        
        value_dict: dictionary, string label:string value
        """
        for d in value_dict:
            print("%s: %s  ---> Be sure to verify this value is what you expect!" % (d, value_dict[d]))
        return True