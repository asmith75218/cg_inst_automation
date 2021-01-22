# from common import common
# from common.{subclass}_common import {subclass}_instrument
# from instrumentbase import Instrument
# from . import {proc1}, {proc2}...
# 
# class _Template({subclass}_instrument):
# 	# class variables common to all {instrument}
# 	proctypes = ['{proc1}', '{proc2}'...]
#
#
#
# To add a new instrument package, duplicate the _inst_pkg_template directory and rename
# it to the name of the instrument (no spaces). The name you give the directory is
# the name that will appear in the program's interactive menus.
# 
# The __init__.py file must be present in the new instrument's directory.
# 
# Edit _inst_template.py (this file) for the new instrument:
#     - uncomment the first import statement to enable use of common instrument
#     automation code.
#     - if the new instrument will belong to an instrument subclass, uncomment and edit
#     the second import statement, replacing {subclass} with the actual subclass name
#     - OR if the new instrument will not belong to any instrument subclass, uncomment
#     the third import statement, assigning it to the Instrument super class
#     - uncomment and edit the fourth import statement to import procedure code (you will
#     need to create {proc1}.py, etc. for each one you import)
#     - edit the class definition for the new instrument. Replace _Template with the name
#     for the new instrument Class (capitalize the first letter). Replace
#     {subclass}_instrument with the name of the desired parent subclass, OR Instrument if
#     it will have no parent subclass.
#     - In the list proctypes, rename {proc1}, etc. with the names of procedures that will
#     appear in the instrument's interactive menu. These must match the import statement
#     above. Create files {proc1}.py, etc. with your code to define these procedures.
# 
# Package is ready for use.