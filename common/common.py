from . import userinput
from datetime import datetime as dt
from datetime import timedelta
import csv
import os

# Dynamic menu
#
#
def dynamicmenu(msg, menuoptions, lastitem, header):
    """
    Displays a dynamically generated menu and returns the letter or number used to
    index the menu option as a string. Called by dynamicmenu_get.
    """
    if header: print(header)
    print("%s:" % msg)
    menuid = []   # Dynamic menu...
    for i, option in enumerate(menuoptions):
        menuid.append(str(i+1))
        print("%s) %s" % (menuid[i], option))
    print("%s) %s" % (lastitem[0].upper(), lastitem[1].title()))
    selection = input("Enter your selection: ")
    
    if selection.lower() == lastitem[0].lower():
        return None
    elif selection in menuid:
        return selection
    else:
        return 999

def dynamicmenu_get(msg, menuoptions, lastitem=('B', 'Go Back'), header=None):
    """
    Executes a dynamically generated menu calling on dynamicmenu function to
    display the options and pass back a selection.
    
    Params:
    msg (string)        Required. Message or prompt to display above the menu
                        options. Suggested message might be "Select an instrument"
                        or similar. Do not include space, colon, dash, etc at
                        the end.
    menuoptions (list)  Required. List of strings to display as menu options. Do
                        not include index numbers or letters in the string, as
                        these will be generated programmatically. Strings will
                        appear in the order they occur in the list, so if this is
                        important, sort the list before passing to this function.
    lastitem (tuple)    Two-item tuple or list of strings used to generate the
                        last menu option. The first item shall be the letter or
                        number used to index the option in the menu. The second
                        item shall be the text to display. Capitalizes first
                        letters. Defaults to ('B', 'Go Back') when not provided.
    header (string)     Optional. Text header to display before msg and all menu
                        options. No formatting will be applied, so format the
                        string before passing to this function if desired.
                        
    Returns:
    (string)            As a string, the index value of the selection from
                        menuoptions list.
    (None)              If lastitem is selected.
        
    """
    while True:
        selection = dynamicmenu(msg, menuoptions, lastitem, header)
        if not selection:
            return None
        elif selection == 999:
            input("\nError! Unrecognized entry [Press ENTER to continue]...")
            continue
        else:
            print("\nYou have selected %s" % menuoptions[int(selection)-1])
            response = input("Is this correct? [y]/n ")
            if response.lower() == 'n':
                continue
            else:
                return str(int(selection) - 1)

    

# Use this function to prompt the user for a name to use on forms and documents. It
# has built-in input validation (see common/userinput.py for validation details).
#
def set_username(msg='Enter your name'):
    """
    Prompt the user for a name to use on forms and documents.
    """
    while True:
        username = userinput.Userinput(input("\n%s: " % msg))
        if username.valid_name():
            return username.user_response
        else:
            print("Unknown error! Try again.")



# Use this function to increment or set the starting form number to use on forms and
# documents. It has built-in input validation (see common/userinput.py for
# validation details).
#
def set_cgformnumber(formnumber=None):
    """Prompt the user for a form number, or increment it if it already exists."""
    while not formnumber:
        # Prompt user and test for valid input...
        formnumber = userinput.Userinput(input("\nEnter the five-digit form number (ex: 00123): "))
        if formnumber.valid_range(range(1, 100000)):
            return str(int(formnumber.user_response)).rjust(5, '0')
        else:
            formnumber = None
            input("\nError! Unrecognized entry [Press ENTER to continue]...")
    # increment the form number...
    return str(int(formnumber)+1).rjust(5, '0')

# ---------- Common prompts and messages ----------
#
#
def usercancelled():
    input("\nOperation cancelled by user. [Press ENTER to continue]...")
    return
    
# When something goes wrong, use this function for the option to try again...
def usertryagain(msg):
    response = input("\n%s Would you like to try again? [y]/n..." % msg)
    if response.lower() == 'n':
        return False
    return True

# When test conditions are not met, use this function for the options to fail the step,
# or pass the step anyway...
def userpassanyway(alert=None):
    if alert:
        print(alert)
    response = input("\nWould you like to accept the result and pass this step? y/[n]...")
    if response.lower() == 'y':
        return True
    return False


# Use this function to prompt the user to enter some text and validate it against
# validselections, which may be a string, list etc.
def usertextselection(msg, validselections):
    """
    Prompt the user to enter some text for validation. Parameters are msg: a text message
    to display to the user, and validselections: the criteria for successful validation.
    """
    while True:
        selection = userinput.Userinput(input(msg))
        if selection.valid_textselection(validselections):
            return selection.user_response
        else:
            print("Invalid entry! Try again.")

# Use this function to prompt the user to enter an integer and validate it against
# an integer range
def userrange(msg, validrange):
    """
    Prompt the user to enter some text for validation. Parameters are msg: a text message
    to display to the user, and validrange: the range for successful validation.
    """
    while True:
        selection = userinput.Userinput(input(msg))
        if selection.valid_range(validrange):
            return int(selection.user_response)
        else:
            print("Invalid entry! Try again.")

def dict_from_csv(csvfilename):
    """
    Import and convert a csv file to a python dictionary. Each line in the csv should
    be in the format "key, value".
    """
    with open(csvfilename, 'r') as csvfile:
        return dict(csv.reader(csvfile))

def cgpartno_from_series(series_letter):
    """Return the numeric zero-padded part number for a given series letter"""
    return str(ord(series_letter)-64).rjust(5, '0')

def rename_file(src, dst):
    try:
        os.replace(src, dst)
    except OSError:
        print("Error saving log file!")
        return False
    return True

def load_command_file(cmdfilename):
    """
    Load a file of commands to send to an instrument, one command per line, and return
    as a list.
    """
    commands = []
    with open(cmdfilename, 'r') as infile:
        for line in infile.readlines():
        	commands.append(line)
    return commands

# ---------- Time Functions ----------
#
#
def compare_times_ordered(t1, t2, margin):
    """Test if t2 is within margin (seconds) after t1"""
    return 0 <= (t2 - t1).seconds <= margin

def compare_times_abs(t1, t2, margin):
    """Test if t1 and t2 are within +/- margin (seconds) of each other"""
    return abs(t1 - t2).seconds <= margin
    
def compare_date_now(d, fmt):
    """Test if date d is today"""
    return formatdate(d, fmt).date() == dt.utcnow().date()
    
def noon_yesterday():
    """Return a datetime object for noon yesterday"""
    return (dt.utcnow() - timedelta(days=1)).replace(hour=12, minute=0, second=0, microsecond=0)
    
def current_utc():
    """Return a datetime object for the current time UTC"""
    return dt.utcnow()

def formatdate(t, fmt):
    """
    Returns a date formatted for use with a specific instrument, for human consumption, or
    for use by python datetime library. If 't' is a datetime obj, and a formatted date
    string is desired, use one of the 'fmt' options below. If a datetime object is desired
    and 't' is a formatted date string, 'fmt' must match the appropriate formatter to
    convert the string.
    """
    if fmt == 'sbe':
        return t.strftime('%m%d%Y%H%M%S')
    elif fmt == 'suna':
        return t.strftime('%Y/%m/%d %H:%M:%S')
    elif fmt == 'iso':
        return t.isoformat()
    elif fmt == 'us':
        return t.strftime('%m/%d/%Y %H:%M:%S')
    elif fmt == 'filename':    # for use in txt doc filenames
        return t.strftime('%Y%m%d%H%M%S')
    else:
        return dt.strptime(t, fmt)
