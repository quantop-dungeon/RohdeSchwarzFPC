# A python interface to Rohde Schwarz FPC spectrum analyzers
A minimalistic class for reading parameters and data from Rohde Schwarz FPC spectrum analyzers. Tested with FPC1500.

## Installation
One way of installing the package is to download the files and run
```bash
pip install c:\...\loc\RohdeSchwarzFPC
```
where `c:\...\loc` is the folder path. 

## Basic usage

```python
from rohdeschwarzfpc import FPC

sa = FPC(address='TCPIP0::172.16.10.10::inst0::INSTR')

# Reads the currently displayed data from the trace no 1
# of the device. The retuned value tr is a dictionary containing 
# the data (1D arrays tr['x'] and tr['y']) and the axes names 
# and units. Usually the returned x is in Hz and y is in V^2/Hz.
tr = sa.get_trace(n=1)

# Reads the center frequency.
f = sa.get_cent_freq()

```
 A default value for the instrument address can be saved in the configuration file, in which case there will be no need to supply the address every time an insturment object is instantiated. 

```python
from rohdeschwarzfpc import FPC, set_config, get_config

set_config({'address': 'TCPIP0::172.16.10.10::inst0::INSTR'})

# Now the address will be read from the config file if we don't supply 
# a value explicitly. 
sa = FPC()

# Reads existing configurations and returns them as a dictionary. 
d = get_config() 
```