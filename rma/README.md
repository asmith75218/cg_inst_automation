# CGSN Automated RMA Document Creator

Simple script to auto-create RMA (3305-00900) shipping documents.

## Requirements

* Python 3.X
* [Instrument Refurbishment Status][refurb-sheet] Google spreadsheet
* Microsoft Word

## Usage

Make sure the following files are located together in the same directory:

* 3305-00900-00000.docx document template
* refurb_data.txt 
* rma.py
* vendors.csv

Complete the first six columns (**RMA #, Items with Serial #, Vendor, Recovered Platform,
Return Record Doc, Departure Date**) in the _Instrument Refurbishment Status_ spreadsheet.
Copy and paste the values from these columns into the file `refurb_data.txt`, replacing
any existing contents. Edit the file to remove line breaks, if any, so that each line in
the spreadsheet takes up exactly one line in the text file.

Edit line 8 of the file `rma.py` to include your name.

Open a command terminal window and `cd` into the script directory. Enter
`python rma.py` into the command line to start the script.

Alternatively, depending on your python installation, you may be able to double-click
the file `rma.py` to start the program.

RMA shipping documents will be created according to the values from the spreadsheet in the
same directory as the script.

Open the documents in Microsoft Word and edit as necessary to include shipping photos,
part numbers, detailed reason for return, etc.

[refurb-sheet]:https://docs.google.com/spreadsheets/d/1vPVL_oJb2FWypvnnMCBrtdQaXW3ax9st2FtRzVnMq8M/edit?usp=sharing