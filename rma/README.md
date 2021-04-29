Automate creation of RMA (3305-00900) shipping documents.

### Usage

Complete the first six columns (**RMA #, Items with Serial #, Vendor, Recovered Platform,
Return Record Doc, Departure Date**) in the [Instrument Refurbishment Status][refurb-sheet]
spreadsheet. Copy and paste the values from these columns into the file
`rma/refurb_data.txt`, replacing any existing contents. Edit the file to remove line
breaks, if any, so that each line in the spreadsheet takes up exactly one line in the text
file.

One document will be created per each line in the file.

From the Main Menu, type `r` to select **RMA and SHIPPING**, then type `1` to begin the
automated procedure. Follow the prompts and enter your name when indicated.

New documents will be created in the `save/` directory using the values from the text file
to complete certain fields. Copy these files to your desired location, and edit them in
Microsoft Word as necessary to include shipping photos, part numbers, detailed reason for
return, etc.

[refurb-sheet]:https://docs.google.com/spreadsheets/d/1vPVL_oJb2FWypvnnMCBrtdQaXW3ax9st2FtRzVnMq8M/edit?usp=sharing