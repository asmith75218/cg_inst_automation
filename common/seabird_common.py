from .serial_common import Serial_instrument
from . import common, seabird_configure

## This module shall contain functions/methods etc common to one or more Seabird
## instruments. To access the serial driver, all functions etc must call the
## serial_common module, NOT THE SERIAL DRIVER DIRECTLY. In this way, changes to
## the serial driver will not require updates to this module.

class Seabird_instrument(Serial_instrument):
    def __init__(self):
        # Initialize shared Instrument superclass attributes...
        super().__init__()

    def imm_timedout(self):
        if not self.buffer_empty():
            self.cap_buf()
            if "TIMEOUT" in self.buf:
                return True
        else:
            return False
    
    def imm_poweron(self):
        self.cap_cmd('')
        if "S>" in self.buf:
            return True
        elif "IMM>" in self.buf:
            return True
        else: return False
        
    def imm_setconfigtype(self, configtype, **kwargs):
        """
        Check the configtype of the IMM and set to the desired configtype if not already
        set. The first param must be the desired configtype. This will reinitialize the
        IMM. Any additional configurations desired may be passed in as optional keyword
        value pairs.
    
        Example: instrument.imm_setconfigtype(configtype='1', setenablebinarydata='0')
        """
        # Determine the currently set configtype of the imm...
        while True:
            print("Verifying IMM configuration...")
            self.imm_cmd('getcd')
            configtypestr = "ConfigType='"
            i = self.buf.find(configtypestr)
            if i < 0:   # For whatever reason, 'getcd' did not do what we expected...
                if not common.usertryagain("Could not get IMM configtype."):
                    return False
                else:   # If this was called before powering the IMM, etc., try again...
                    continue
            current_configtype = self.buf[i + len(configtypestr)]
        
            # If different from intended configtype, change it...
            if configtype != current_configtype:
                print("Configuring IMM...")
                self.imm_init()
                self.cap_cmd('setconfigtype=%s' % configtype)
                self.cap_cmd('setconfigtype=%s' % configtype)
                self.imm_poweron()
                for name, value in kwargs.items():
                    self.imm_cmd("%s=%s" % (name, value))
                continue
            return True

    def imm_init(self):
        self.cap_cmd('*INIT')
        self.cap_cmd('*INIT')
        return self.imm_poweron()
        
    def imm_init_connection(self):      
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
        self.serialnumber = "%s-%s" % (self.sbe_prefix, ds[self.sn_idx])
        print("Serial no.: %s" % self.serialnumber)
        return True

    def imm_cmd(self, cmd):
        """
        Send a command to an IMM, checking first that the IMM has not timed out, or
        waking it if it has.
        """
        if self.imm_timedout():
            self.imm_poweron()
        return self.cap_cmd(cmd)
        
    def imm_remote_wakeup(self):
        return self.imm_cmd('pwron')
        
    def imm_get_remote_id(self):
        while True:
            self.imm_cmd('id?')
            loc = self.buf.find('id = ')
            if loc == -1:       # id not found in imm response...
                if common.usertryagain("Unable to get remote id."):
                    continue
                else:
                    return False
            self.remote_id = self.buf[loc+5:loc+7]
            return True
    
    def imm_set_remote_id(self, ID):
        i = 0
        while True:
            self.imm_get_remote_id()
            if self.remote_id == ID:
                return True
            if i:
                if not common.usertryagain("Failed to set remote id."):
                    return False                    
            self.cap_cmd('*id=%s' % ID)
            self.cap_cmd('*id=%s' % ID)
            i += 1

    def imm_remote_reply(self, cmd):
        self.imm_cmd('#%s%s' % (self.remote_id, cmd))
        return self.buf
    
    def imm_set_datetime(self, t):
        return self.imm_cmd('#%sdatetime=%s' % (self.remote_id, t))

    def imm_set_startdatetime(self, t):
        return self.imm_cmd('#%sstartdatetime=%s' % (self.remote_id, t))

    def imm_remote_cmd(self, cmd):
        pass

    def imm_initlogging(self):
        self.imm_cmd('#%sinitlogging' % self.remote_id)
        if 'confirm' in self.buf:
            self.cap_cmd('#%sinitlogging' % self.remote_id)
        return True
        
    def imm_configure(self, cmdfile):
        seabird_configure.imm_configure(self, cmdfile)