from common import common
from common.seabird_common import Seabird_instrument
# from . import configure

class Ctdbpp(Seabird_instrument):
    # class variables common to all CTDMO
    proctypes = ['configure']
    name = "CTDBP-P"
    baudrate = 9600
    class_id = "1336-00001"
    sbe_prefix = "16"
    
    # instrument command to display cal coefs...
    cc = "dcal"

    # index of instrument serial number in reply to 'ds' command...
    sn_idx = 7
    
    def __init__(self):
        # instance variables...
        self.timeout = 6
        self.imm_configtype = '1'
                
        # Initialize shared superclass attributes...
        super().__init__()
    
    # these first definitions are for launching available procedures and should
    # match the above proctypes
    def configure(self):
        self.imm_configure("instruments/ctdbpp/ctdbp-p_configuration.txt")
    # --------------------------
        