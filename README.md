# Rohde Schwarz FPC python interface
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

sa = FPC(address=r'TCPIP0::172.16.10.10::inst0::INSTR')

# Reads the currently displayed data of the trace 
# no 1 from the device. x and y are 1D arrays, and 
# mdt is a dictionary containing the axes names and units.
# Usually the returned x is in Hz and y is in V^2/Hz.
x, y, mdt = sa.get_trace(n=1)

# Reads the center frequency.
f = sa.get_cent_freq()
```
 
