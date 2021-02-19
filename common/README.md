##Common code modules

### `common` – high-level and interface functions


#### User Interface functions

`common.**dynamicmenu_get**(msg, menuoptions[, lastitem, header])`

`common.**usercancelled**()`

`common.**usertryagain**(msg)`

`common.**userpassanyway**(alert=None)`

`common.**usertextselection**(msg, validselections)`

`common.**set_username**(msg='Enter your name')`

`common.**usertextselection**(msg, validselections)`

`common.**dict_from_csv**(csvfilename)`

#### Time and Date functions

<pre>common.<b>compare_times_ordered</b>(t1, t2, margin)</pre>

<pre>common.<b>compare_times_abs</b>(t1, t2, margin)</pre>

<pre>common.<b>compare_date_now</b>(d, fmt)</pre>

<pre>common.<b>noon_yesterday</b>()</pre>

<pre>common.<b>current_utc</b>()</pre>

<pre>common.<b>formatdate</b>(t, fmt)</pre>

#### OOI and CGSN Special features

<span style="color:blue;font-family: monospace, monospace">common.<b>set_cgformnumber</b>(formnumber=None)</span>

<span style='font-family: courier'>common.<b>cgpartno_from_series</b>(series_letter)</span>
