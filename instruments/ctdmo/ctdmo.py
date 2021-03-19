from common import common
from common.seabird_common import Seabird_instrument
from . import retire, qct, calibration

class Ctdmo(Seabird_instrument):
    # class variables common to all CTDMO
    proctypes = ['qct', 'calibration', 'retire']
    name = "CTDMO"
    baudrate = 9600
    class_id = "1336-00001"
    INVENTORYCSV = "instruments/ctdmo/ctdmo_inv.csv"
    
    def __init__(self):
        # instance variables...
        self.timeout = 5
        self.imm_configtype = '1'
        
        # default validation min/max values for a sample, in air, at normal indoor conditions
        self.sample_minmax = {
            'c_min':'-0.01',
            'c_max':'0.01',
            't_min':'17',
            't_max':'23',
            'p_min':'-0.5',
            'p_max':'0.5'
        }

        # Initialize shared superclass attributes...
        super().__init__()
    
    # these first definitions are for launching available procedures and should
    # match the above proctypes
    def retire(self):
        retire.proc_retire(self)
        
    def qct(self):
        qct.init_qct(self)
        
    def calibration(self):
        calibration.init_calibration(self)
    # --------------------------

    def init_connection(self):      
        self.connect()

        # Establish communication with the IMM...
        self.imm_poweron()
        self.imm_cmd("gethd")
        self.imm_setconfigtype(configtype='1', setenablebinarydata='0')
    
        # Establish communication with the instrument...
        print("Waking the instrument...")
        self.imm_remote_wakeup()
 
        self.imm_get_remote_id()

        self.imm_cmd('#%soutputexecutedtag=n' % self.remote_id)
        ds = self.imm_remote_reply('ds').split()
        self.serialnumber = "37-%s" % ds[5]
        print("Serial no.: %s" % self.serialnumber)

        self.get_seriesletter()
        return True


    def get_seriesletter(self):
        # Use serial number to look up series letter from a csv inventory file, then set
        # part number accordingly...
        inventory_dict = common.dict_from_csv(self.INVENTORYCSV)
        try:
            self.seriesletter = inventory_dict[self.serialnumber]
        except KeyError:
            self.seriesletter = common.usertextselection("Enter the instrument Series (G, H, Q or R): ", "GgHhQqRr").upper()
        self.part_no = "%s-%s" % (self.class_id, common.cgpartno_from_series(self.seriesletter))
        return True

    def get_time(self):
        ds = self.imm_remote_reply('ds')
        ds_date = ' '.join(ds.split()[6:10])
        return common.formatdate(ds_date, '%d %b %Y %H:%M:%S')
        
    def clock_set_test(self, margin, conditions=['utc']):
        for condition in conditions:
            while True:
                if condition == 'noon':
                    print("Setting clock to noon yesterday...")
                    t1 = common.noon_yesterday()
                elif condition == 'utc':
                    print("Setting clock to current time UTC...")
                    t1 = common.current_utc()
                self.imm_set_datetime(common.formatdate(t1, 'sbe')) 
                t2 = self.get_time()
                if common.compare_times_ordered(t1, t2, margin):
                    break
                else:
                    if common.usertryagain("There was a problem setting the clock. The reported time is %s. The expected time is %s" % (common.formatdate(t2, 'us'), common.formatdate(t1, 'us'))):
                        continue
                    else:
                        return False
        return True

    def take_sample(self):
        # Instruct a CTDMO to take a sample, parse the reply and return it as a dictionary
        sample = self.imm_remote_reply('ts').splitlines()[1]
        print(sample)
        sample = [s.strip() for s in sample.split(',')]
        return {'date':sample[4], 'time':sample[5], 'sn':sample[0], 't':sample[1], 'c':sample[2], 'p':sample[3]}
    
    def sample_range_test(self, sample):
        # Test sample values are within predefined min/max range...
        result = True
        params = {'t':'temperature', 'c':'conductivity', 'p':'pressure'}
        sample = {key:value for key, value in sample.items() if key in params.keys()}
        for item in sample.items():
            min, max = [self.sample_minmax[key] for key in ['%s_min' % item[0], '%s_max' % item[0]]]
            if not float(min) < float(item[1]) < float(max):
                print("The %s value '%s' appears to be out of range!" % (params[item[0]], item[1]))
                result = False
        return result   

    def sample_compare_increase(self, sample1, sample2, label):
        # Test if sample increased...
        result = True
        print('Testing %s <= %s...' % (sample1, sample2))
        if not float(sample2) >= float(sample1):
            print("The %s value did not increase as expected!" % label)
            result = False
        return result
        
    def generate_cal_csv(instrument):
        # Fetch calibration coefficients from instrument (XML format) and pass them on to
        # the calibration module to export a calibration csv...
        cc = instrument.imm_remote_reply('getcc')
        cal_xml = cc[8:-2]
        print("Exporting calibration to CSV...")
        calibration.export_csv(cal_xml, instrument)
    
