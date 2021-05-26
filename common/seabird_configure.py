from . import common
from datetime import datetime as dt

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
        print("Setting the date and time to start logging...")
        yr = common.userrange("Enter the start year: ", range(2000, 2100))
        mo = common.userrange("Enter the start month: ", range(1, 13))
        dy = common.userrange("Enter the start day: ", range(1, 32))
        hr = common.userrange("Enter the start hour (0-23): ", range(0, 24))
        min = common.userrange("Enter the start minute (0-59): ", range(0, 60))
        sec = common.userrange("Enter the start second (0-59): ", range(0, 60))
        t_start = dt(yr, mo, dy, hr, min, sec)
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
