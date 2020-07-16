import xml.etree.ElementTree as ET
from datetime import datetime as dt
import csv

def export_csv(cal_xml, series_letter, formnumber):
    """Parse XML instrument calibration values into a new CSV file"""
    root = ET.fromstring(cal_xml)
    
    serial_no = '37-%s' % root.items()[1][1][3:]
    source_file = "source_file 3305-00101-%s-A_SN_%s_QCT_Results_CTDMO-%s.txt" % (formnumber, serial_no, series_letter)
    cal_date = get_cal_date(root)
    filename = get_filename(series_letter, serial_no, cal_date)
    
    write_cal_file(root, serial_no, filename, source_file)
    
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
    with open('%s.csv' % filename, 'w', newline='') as cal_file:
        writer = csv.writer(cal_file)
        writer.writerow(["serial", "name","value","notes"])
        writer.writerow([serial_no, "CC_a0", t.find('A0').text,source_file])
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
