from common import common
from common.qct_common import Qct


def init_qct(instrument):
#     # COMMON VARIABLES
#     USERNAME = common.set_username()        # Test conductor name (entered by user)
#     FORMNUMBER = common.set_cgformnumber()    # QCT sequential form number (or starting number)
#     DOCNUMBER = "3305-00102"                # QCT document number
    
    # Main test loop...
    while True:
        qct = Qct_ctdbp()
#         qct.init_header(FORMNUMBER, DOCNUMBER, USERNAME)
        
       # call test procedure...
        qct.proc_qct(instrument)
#         
#         # test complete, display results to screen...
#         for key in qct.results_pass:
#             b = 'Pass' if qct.results_pass[key] else 'Fail'
#             print("%s %s: %s" % (key, b, qct.results_text[key]))
#         # Generate the results document...
#         print("Generating results document...")
#         doc_ctdmo.qct_to_doc(instrument, qct)
#         print("Test complete!\r\n")
#         
#         # Prompt to test another instrument, which will increment the form number
#         # and run the loop again...
#         again = input("Would you like to test another instrument? y/[n] ")
#         if again.lower() != "y":
#             return
#         print("Connect the next instrument now.")
#         input("Type ENTER to begin the next test...")
#         FORMNUMBER = common.set_cgformnumber(FORMNUMBER)
        print("Nice to meet you, bye!\r\n")
        return

class Qct_ctdbp(Qct):
    # class variables common to all CTDBP QCT
    
    def __init__(self):
        # Initialize shared Qct superclass attributes...
        super().__init__()
        
        # Initialize or override ctdbp-specific attributes...
        
    def proc_qct(self, instrument):
#         # Specify a capture file...
#         instrument.capfile = "save/%s-A.txt" % self.header['docname']

        # Open a serial (RS232) connection...
        instrument.connect()

        while not instrument.sbe_get_prompt():
            if common.usertryagain("Failed to communicate with instrument."):
                continue
            else:
                common.usercancelled()
                return True

        instrument.sbe_parse_ds()
        print("Serial number: %s" % instrument.serialnumber)
        
        self_confirm = {
                        "Firmware version":instrument.firmware,
                        "Battery voltage":instrument.vbatt
                        }
        self.user_confirm_value_no_prompt(self_confirm)
        # ---- 8.2.2 ----
        self.results_text['8.2.2'] = "Battery voltage %s V" % instrument.vbatt
        self.results_pass['8.2.2'] = True
       
        # ---- 8.3.6 ----
        self.results_text['8.3.6'] = "Firmware v%s confirmed." % instrument.firmware
        self.results_pass['8.3.6'] = True

        # Put instrument into reference config...
        instrument.sbe_set_ref_configs()
        
        # TODO: generate cal file here!
        # ---- 8.3.5 ----

        # ---- 8.3.8 ----
        print("Testing instrument clock...")
        self.test_step('8.3.8',
                        instrument.sbe_clock_set_test(5, ['noon', 'utc']),
                        'The clock was set successfully.',
                        'The clock was not set successfully.',
                        'The instrument clock was not set to the expected time.')

#        # ---- 8.3.6 ----
#         print("Establishing communication...")
#         # Set the instrument's IMM ID...
#         self.test_step('8.3.5',
#                         instrument.imm_set_remote_id(self.ID),
#                         'Established communication with instrument.',
#                         'Failed to establish communication with instrument.')
#         print("Remote id: %s" % instrument.remote_id)       
#         
#         # ---- 8.3.7 ----
#         instrument.imm_cmd('#%soutputformat=1' % instrument.remote_id)
#         #instrument.imm_cmd('#%soutputexecutedtag=n' % instrument.remote_id)
#         ds = instrument.imm_remote_reply('ds').split()
#         #instrument.serialnumber = "37-%s" % ds[5]
#         instrument.firmware = ds[2]
#         #print("Serial number: %s" % instrument.serialnumber)
#         print("Firmware version: %s" % instrument.firmware)
# 
#         # Add step results to test results dictionaries...
#         self.results_text['8.3.7a'] = "Serial number confirmed."
#         self.results_pass['8.3.7a'] = True
#         self.results_text['8.3.7b'] = "Firmware %s confirmed." % instrument.firmware
#         self.results_pass['8.3.7b'] = True
# 
#         # Get series letter and part number...
#         #instrument.get_seriesletter()
#         print("Class/Series: CTDMO-%s" % instrument.seriesletter)
#         print("Part No.: %s" % instrument.part_no)
#         
#         # ---- 8.3.8 ----
#         # Generate the calibration CSV...
#         print("Retrieving calibration information...")
#         instrument.cal_source_file = "%s-A_SN_%s_QCT_Results_CTDMO-%s.txt" % (self.header['docname'], instrument.serialnumber, instrument.seriesletter)
#         instrument.generate_cal_csv()
#         
#         # ---- 8.3.10 ----
#         print("Testing instrument clock...")
#         self.test_step('8.3.10',
#                         instrument.clock_set_test(5, ['noon', 'utc']),
#                         'The clock was set successfully.',
#                         'The clock was not set successfully.',
#                         'The instrument clock was not set to the expected time.')
#             
#         # ---- 8.3.11 - 8.3.12 ----
#         print("Testing configuration...")
#         current_steps = ['8.3.11', '8.3.12']
#         # change sample interval first to 120, then to 10...
#         for i, interval in enumerate(['120', '10']):
#             instrument.imm_remote_reply('sampleinterval=%s' % interval)
#             ds = instrument.imm_remote_reply('ds').split()
#             self.test_step( current_steps[i],
#                             ds[29] == interval,
#                             'The sample interval was set successfully.',
#                             'The sample interval was not set successfully.',
#                             'The sample interval was not set to the expected value!')
# 
#         # ---- 8.3.13 ----
#         print("Acquiring a sample...") #TODO complete this step... make loop for try again, etc
#         sample_in_air = instrument.take_sample()
#         # Test for a valid sample date i.e. today...
#         self.test_step('8.3.13a',
#                         common.compare_date_now(', '.join([sample_in_air[k] for k in ['date','time']]), '%d %b %Y, %H:%M:%S'),
#                         'The sample contains a vaild timestamp.',
#                         'The sample does not contain a vaild timestamp.',
#                         'The sample date is not today!')
#         # Overly simple sample range test...
#         self.test_step('8.3.13b',
#                         instrument.sample_range_test(sample_in_air),
#                         'The sample data appear to be valid.',
#                         'The sample data appear invalid.')
#             
#         # ---- 8.3.15 - 8.3.16 ----
#         print("Place the instrument in a container of warm water now.")
#         input("Press ENTER to continue...")
#         print("Acquiring a sample...")
#         sample_in_bucket = instrument.take_sample()
#         self.test_step('8.3.15',
#                         instrument.sample_compare_increase(sample_in_air['p'], sample_in_bucket['p'], 'pressure'),
#                         'The pressure data appear to be valid.',
#                         'The pressure data appear invalid.')
#         self.test_step('8.3.16',
#                         instrument.sample_compare_increase(sample_in_air['t'], sample_in_bucket['t'], 'temperature'),
#                         'The temperature data appear to be valid.',
#                         'The temperature data appear invalid.')

        if not instrument.disconnect():
            print("Error closing serial port!")
        return True