from . import common
from datetime import datetime as dt

def init_deploy(instrument):
    header = ''.join(("\n", "-" * 24, " DEPLOY MENU ", "-" * 24))
    platforms = [platform for platform in instrument.dep_configs.keys()]

    # Present platform selection menu to user...
    userselection = common.dynamicmenu_get("Select a platform", platforms, lastitem=('C', 'Cancel'), header=header)
    if not userselection:
        # Cancelled by user...
        return False

    sbe_deploy(instrument, platforms[int(userselection)])
    return True

def sbe_deploy(instrument, platform):
    # Connect to the instrument and begin logging...
    instrument.sbe_connect()
    
    # Enable printing to user screen...
    print("Instrument will now print to your screen...")
    instrument.echo = True

    # Capture hardware and calibration information...
    instrument.sbe_cmd('gethd')
    instrument.sbe_cmd('getcc')
    
    # Put instrument into reference configuration...
    instrument.sbe_set_ref_configs()
    
    # Make platform-specific configurations...
    for config in instrument.dep_configs[platform]:
        instrument.sbe_cmd('%s\n' % config)
    
    # Set UTC time...
    instrument.sbe_set_datetime(common.formatdate(common.current_utc(), 'sbe'))

    # Capture updated instrument configuration...
    instrument.sbe_cmd('ds')

    # Set deploy date/time...
    if not 'NSIF' in platform:      # Assumes an NSIF instrument is not deployed by user
        msg = "Setting the date and time to start logging..."
        t_start = common.userdatetime(msg)
        instrument.sbe_set_startdatetime(common.formatdate(t_start, 'sbe'))
        instrument.sbe_cmd("startlater")
        print("Instrument deployed!")
    else:
        print("Instrument is not deployed! Waiting for command to begin logging.")
        
    # Wrap up...
    instrument.echo = False

    # Rename and save log file...
    filedate = common.current_utc().strftime('%Y%m%d')
    instrument.rename_capfile("save/%s_%s_config_%s.txt" % (instrument.name, instrument.serialnumber, filedate))

    # Disconnect and end procedure...
    print("Configuration complete.")
    
    if not instrument.disconnect():
        print("Error closing serial port!")
    return True

def imm_configure(instrument, cmdfile):
    # Specify a capture file...
    instrument.capfile = "save/%s_TMP_config.txt" % instrument.name

    # Open a serial (RS232) connection...
    instrument.imm_init_connection()

    # Prompt to set inductive ID...
    print("Remote id: %s" % instrument.remote_id)       
    if input("Would you like to set the inductive ID? y/[n] ").lower() == "y":
        instrument.imm_set_remote_id(str(common.userrange("Enter the desired ID: ", range(0, 100))))
        print("Remote id: %s" % instrument.remote_id)       

    # Enable printing to user screen...
    print("Instrument will now print to your screen...")
    instrument.echo = True

    # Load configuration commands...
    configs = common.load_command_file(cmdfile)
    
    # Send configuration commands to instrument...
    for config in configs:
        instrument.imm_cmd('#%s%s' % (instrument.remote_id, config))

    # Set the time and date...
    instrument.imm_set_datetime(common.formatdate(common.current_utc(), 'sbe'))

    # Erase the logger...
    if input("Would you like to erase all samples from the instrument? y/[n] ").lower() == "y":
        instrument.imm_initlogging()
        
    # Display and capture instrument configuration...
    print("Capturing instrument configuration. Please review for accuracy...")
    instrument.imm_cmd('#%sds' % instrument.remote_id)
    instrument.imm_cmd('#%s%s' % (instrument.remote_id, instrument.cc))

    # Set start date and time, and deploy instrument...
    if input("Would you like to deploy the instrument? [y]/n ").lower() != "n":
        msg = "Setting the date and time to start logging..."
        t_start = common.userdatetime()
        instrument.imm_set_startdatetime(common.formatdate(t_start, 'sbe'))
        instrument.imm_cmd('#%sstartlater' % instrument.remote_id)

    # Wrap up...
    instrument.echo = False

    # Rename and save log file...
    filedate = common.current_utc().strftime('%Y%m%d')
    instrument.rename_capfile("save/%s_%s_config_%s.txt" % (instrument.name, instrument.serialnumber, filedate))

    # Disconnect and end procedure...
    print("Configuration complete.")
    
    if not instrument.disconnect():
        print("Error closing serial port!")
    return True
