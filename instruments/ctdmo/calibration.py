from common import common
import xml.etree.ElementTree as ET
from datetime import datetime as dt
import csv

def init_calibration(instrument):
    while True:
        header = ''.join(("\n", "-" * 21, " CALIBRATION MENU ", "-" * 21))
        proclist = [{'EXPORT CAL CSV': export_cal}, {'UPDATE COEFFICIENTS': update_cal}]
        try:
            proc_id = int(common.dynamicmenu_get("Select a procedure", [[*d.keys()][0] for d in proclist], header=header))
        except TypeError:
            break
        else:
            [*proclist[proc_id].values()][0](instrument)

def export_cal(instrument):
    # Display an instruction message to the user...
    print("This procedure will connect to an instrument and generate a calibration csv")
    print("from the coefficients stored on the instrument.")
    input("Press the ENTER key when ready to begin...")

    # Open a serial (RS232) connection...
    instrument.set_timeout(2)
    instrument.init_connection()

    instrument.cal_source_file = "retreived from instrument on %s" % common.current_utc().strftime("%Y-%m-%d")
    instrument.generate_cal_csv()
    
    print("Procedure complete.")
    
    if not instrument.disconnect():
        print("Error closing serial port!")
    return True
    
def update_cal(instrument):
    # Display an instruction message to the user...
    print("Place the factory calibration file (e.g. 12345.cal) in the import folder.")
    input("Press the ENTER key when ready to begin the procedure...")

    # Specify a capture file...
    instrument.capfile = "save/update_cal.log.txt"
    
    # Open a serial (RS232) connection...
    instrument.set_timeout(2)
    instrument.init_connection()

    # Enable printing to user screen...
    print("Instrument will now print to your screen...")
    instrument.echo = True

    # Display current cal coefficients from instrument...
    instrument.imm_cmd('#%sdc' % instrument.remote_id)
    
    # Set the source file for the new coefficients...
    instrument.cal_source_file = "%s.cal" % instrument.serialnumber[3:]
    
    # Get coefficients from cal file...
    coefs = get_cal_from_file(instrument)
    coefs.pop('INSTRUMENT_TYPE')
    coefs.pop('SERIALNO')
    
    # Update the instrument...
    for coef in coefs.keys():
        instrument.imm_cmd('#%s%s=%s' % (instrument.remote_id, coef, coefs[coef]))

    # Display updated cal coefficients from instrument...
    instrument.imm_cmd('#%sdc' % instrument.remote_id)
    
    # Wrap up...
    instrument.echo = False
    
    # Prompt to generate a new cal csv...
    again = input("Would you like to create a new calibration csv? [y]/n ")
    if again.lower() != "n":
        instrument.generate_cal_csv()

    print("\nUpdate complete.\n")
    
    filedate = common.current_utc().strftime('%Y%m%d')
    instrument.rename_capfile("save/CTDMO_%s_update_coefficients_%s.txt" % (instrument.serialnumber, filedate))
    
    if not instrument.disconnect():
        print("Error closing serial port!")
    return True
    
def get_cal_from_file(instrument):
    fname = "import/%s" % instrument.cal_source_file
    coefs = {}    
    with open(fname, 'r') as infile:
        for line in infile.readlines():
            key, value = line.split('=')
            coefs[key] = value.strip()
    return coefs


def export_csv(cal_xml, instrument):
    """Parse XML instrument calibration values into a new CSV file"""
    root = ET.fromstring(cal_xml)
    
    cal_date = get_cal_date(root)
    filename = get_filename(instrument.seriesletter, instrument.serialnumber, cal_date)
    
    write_cal_file(root, instrument.serialnumber, filename, instrument.cal_source_file)
    
def get_filename(series_letter, serial_no, cal_date):
    """Construct the filename string for the CSV"""
    file_date = cal_date.strftime('%Y%m%d')
    return "CGINS-CTDMO%s-%s__%s" % (series_letter, serial_no[3:], file_date)

def get_cal_date(root):
    """Parse out cal dates for P, T and C, and return the latest one"""
    cal_dates_text = iter(root.findall('Calibration/CalDate'))
    cal_dates = [dt.strptime(d.text, '%d-%b-%y') for d in cal_dates_text]
    return max(cal_dates)

def write_cal_file(root, serial_no, filename, source_file):
    """Open a new CSV file and write cal coefficients to each line"""
    # Separate temperature, conductivity and pressure from XML...
    t, c, p = iter(root.findall('Calibration'))
    # Make a new file and write out the rows...
    with open('save/%s.csv' % filename, 'w', newline='') as cal_file:
        writer = csv.writer(cal_file)
        writer.writerow(["serial", "name","value","notes"])
        writer.writerow([serial_no, "CC_a0", t.find('A0').text,"source_file %s" % source_file])
        writer.writerow([serial_no, "CC_a1", t.find('A1').text,""])
        writer.writerow([serial_no, "CC_a2", t.find('A2').text,""])
        writer.writerow([serial_no, "CC_a3", t.find('A3').text,""])
        writer.writerow([serial_no, "CC_cpcor", c.find('PCOR').text,""])
        writer.writerow([serial_no, "CC_ctcor", c.find('TCOR').text,""])
        writer.writerow([serial_no, "CC_g", c.find('G').text,""])
        writer.writerow([serial_no, "CC_h", c.find('H').text,""])
        writer.writerow([serial_no, "CC_i", c.find('I').text,""])
        writer.writerow([serial_no, "CC_j", c.find('J').text,""])
        writer.writerow([serial_no, "CC_p_range", int(float(p.find('PRANGE').text)),""])
        writer.writerow([serial_no, "CC_pa0", p.find('PA0').text,""])
        writer.writerow([serial_no, "CC_pa1", p.find('PA1').text,""])
        writer.writerow([serial_no, "CC_pa2", p.find('PA2').text,""])
        writer.writerow([serial_no, "CC_ptca0", p.find('PTCA0').text,""])
        writer.writerow([serial_no, "CC_ptca1", p.find('PTCA1').text,""])
        writer.writerow([serial_no, "CC_ptca2", p.find('PTCA2').text,""])
        writer.writerow([serial_no, "CC_ptcb0", p.find('PTCB0').text,""])
        writer.writerow([serial_no, "CC_ptcb1", p.find('PTCB1').text,""])
        writer.writerow([serial_no, "CC_ptcb2", p.find('PTCB2').text,""])
        writer.writerow([serial_no, "CC_ptempa0", p.find('PTEMPA0').text,""])
        writer.writerow([serial_no, "CC_ptempa1", p.find('PTEMPA1').text,""])
        writer.writerow([serial_no, "CC_ptempa2", p.find('PTEMPA2').text,""])
        writer.writerow([serial_no, "CC_wbotc", c.find('WBOTC').text,""])
    return
