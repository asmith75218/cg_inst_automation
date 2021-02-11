## Installation using Anaconda and Git

Using *Anaconda Prompt* (Windows) or *Terminal* (Mac)...
    > git clone https://github.com/asmith-whoi/cg_inst_automation.git

A new folder will be created with the required files and folder structure.

    > cd cg_inst_automation

Set up the software environment...

    > conda env create -f instruments.yml

Activate the new environment...

    > conda activate instruments

If you encounter any problems during the installation or setup, try updating conda.

## Usage

Calling the program from the command line is the best way to run the program. If using
Anaconda, be sure the **instruments** environment is configured and activated.

    (instruments) cg_inst_automation> python main.py





## Adding Instruments

A new instrument may be added to the program as either a python package or a module. A
package is best for supporting many varied actions and procedures, but is more complex
to create. A module may be easier if very little code will be required.

Templates for both are located in the **cg_inst_automation/instruments** folder.





###The module template

Duplicate **_inst_mod_template.py** and rename it to {instrument}.py with the name of the
instrument, e.g. `dosta.py` for a DOSTA instrument. Use all lower case letters, with no
spaces. The name you give the file will be used to automatically generate the program's
interactive menus.

####Common code

To access the program's common code, uncomment the `common` and `instrumentbase` import
statements...

    from common import common
    from instrumentbase import Instrument

If you will be assigning your instrument to one of the program's existing
instrument subclasses, uncomment the subclass import statement and replace `{subclass}`
with the name of the desired subclass...

    from common.{subclass}_common import {subclass}_instrument

Define a new class for the new instrument. Uncomment the following lines, and replace
`_Template` with the name of the instrument, *exactly as you named the file* with the
first letter capitalized, e.g. `class Dosta({subclass}_instrument)` for a DOSTA
instrument. Replace `{subclass}` exactly as in the above import statement...

```python
class _Template({subclass}_instrument):
    # class variables common to all {instrument}
    proctypes = ['{proc1}', '{proc2}'...]
```

Edit the `proctypes` list in the above block to include all the procedures for the new
instrument that will appear in the program's interactive menus. Replace `{proc1}`, etc.
with the names of these procedures.

Add your code to define these procedures as methods of the new class.


###The package template

Duplicate the **_inst_pkg_template** directory and rename it to `{instrument}` with the
name of the instrument, e.g. `dosta` for a DOSTA instrument. Use all lower case letters,
with no spaces. The name you give the directory will be used to automatically generate the
program's interactive menus.

####The __init__.py file

The `__init__.py` file must be present in the new instrument's directory. Edit this file,
replacing `{instrument}` with the name of the instrument, as above. Replace
`{Instrument}`, capitalizing the first letter.

####The _inst_template.py file

To access the program's common code, uncomment the `common` and `instrumentbase` import
statements...

    from common import common
    from instrumentbase import Instrument

If you will be assigning your instrument to one of the program's existing
instrument subclasses, uncomment the subclass import statement and replace `{subclass}`
with the name of the desired subclass...

    from common.{subclass}_common import {subclass}_instrument

Define a new class for the new instrument. Uncomment the following lines, and replace
`_Template` with the name of the instrument, *exactly as you named the file* with the
first letter capitalized, e.g. `class Dosta({subclass}_instrument)` for a DOSTA
instrument. Replace `{subclass}` exactly as in the above import statement...

```python
class _Template({subclass}_instrument):
    # class variables common to all {instrument}
    proctypes = ['{proc1}', '{proc2}'...]
```

Edit the `proctypes` list in the above block to include all the procedures for the new
instrument that will appear in the program's interactive menus. Replace `{proc1}`, etc.
with the names of these procedures.

Add your code to define these procedures as methods of the new class.

You may create separate modules to contain your code for each procedure. To do this, name
the modules exactly as you named the corresponding procedure in the `proctypes` list.
Uncomment and edit the last import statement at the top of the template file to import the
modules when the package is loaded.

You may add as many modules to the package as you wish. They do not need to be added to
the `proctypes` list unless you wish for them to appear in the program's interactive
menus.