from common import common
from common.seabird_common import Seabird_instrument
from . import qct

class Ctdbp(Seabird_instrument):
    # class variables common to all CTDBP
    proctypes = ['qct', 'deploy']
    name = "CTDBP"
    baudrate = 9600
    class_id = "1336-00001"
    sbe_prefix = "16"
    
    # instrument command to display cal coefs...
    cc = "dcal"

    # index of various elements in reply to 'ds' command...
    fw_idx = 4
    sn_idx = 7
    vbatt_idx = 14
    dt_idx = [8,12]
    
    # commands to put into baseline "reference" configuration...
    ref_configs =   [
                    'OUTPUTEXECUTEDTAG=N',
                    'ECHO=Y',
                    'OUTPUTSAL=N',
                    'OUTPUTSV=N',
                    'OUTPUTUCSD=N',
                    'NCYCLES=4',
                    'PUMPMODE=1',
                    'OUTPUTFORMAT=3',
                    'TXREALTIME=Y'
                    ]

    # deployment configurations (assuming the above reference configuration)...
    dep_configs =    {
                    'CP-NSIF':  [
                                'SAMPLEINTERVAL=10'
                                ],
                    'CP-MFN':   [
                                'SAMPLEINTERVAL=900'
                                ]
                    }
   
    def __init__(self):
        # instance variables...
        self.timeout = 3
                
        # Initialize shared superclass attributes...
        super().__init__()
    
    # these first definitions are for launching available procedures and should
    # match the above proctypes
#     def configure(self):
#         self.imm_configure("instruments/ctdbpp/ctdbp-p_configuration.txt")

    def qct(self):
        qct.init_qct(self)
        
    def deploy(self):
        self.sbe_deploy()

    # --------------------------

