import pyvisa
import numpy as np

from numpy import ndarray
from typing import Tuple, Union


class FPC:
    """Class for communication with Rohde & Schwarz FPC spectrum analyzers.

    Args:
        address: Visa resource name.

    Attributes:
        comm: Communication resource that performs read and write operations  
            on the physical device. 
    """
    comm = None

    def __init__(self, address: str = r'TCPIP0::172.16.10.10::inst0::INSTR'):
        rm = pyvisa.ResourceManager()
        self.comm = rm.open_resource(address)

    def get_trace(self, n: int = 1) -> Tuple[ndarray, ndarray, dict]:
        """Reads a current trace from the instrument. Does not initiate or 
        stop data acquisition.

        Args:
            n: Trace number.

        Returns:
            A tuple (x, y, mdt), where x and y are numeric vectors and mdt is
            a metadata dictionary.
        """

        mdt = dict()
        mdt['name_x'] = 'Frequency'
        mdt['unit_x'] = 'Hz'
        mdt['name_y'] = '$S_V$'
        mdt['unit_y'] = ''  # It will be determined later.

        # Configures the device for binary data transfer and queries y data.
        req = 'FORMat REAL,32;:TRACe:DATA? TRACE%i' % n
        y = self.comm.query_binary_values(req, datatype='f',
                                          container=np.ndarray)

        # Queries the start frequency, the stop frequency
        # and the unit of the y data.
        resp = self.comm.query(':FREQuency:STARt?;:FREQuency:STOP?;'
                               ':UNIT:POWer?;:BWIDth:RESolution?')

        f1, f2, unit, rbw = resp.split(sep=';')

        # Calculates the frequency axis.
        x = np.linspace(float(f1), float(f2), len(y))

        if unit.lower() == 'dbm':
            # Normally, spectra returned by the device are in dBm, while
            # it is more convenient to process them on a linear scale.

            # Converts the data to V^2/Hz, assuming 50 Ohm input impedance.
            y = 50*0.001*(10**(y/10))/float(rbw)
            mdt['unit_y'] = 'V$^2$/Hz'
        else:
            # Leaves the data as it is.
            mdt['unit_y'] = unit

        return (x, y, mdt)

    def get_idn(self):
        """Reads the identifying string from the device."""
        str = self.comm.query('*IDN?')
        return str.strip()

    # Setter and getter methods for the instrument parameters

    def set_start_freq(self, x: Union[float, str]) -> None:
        """Sets start frequency (Hz)."""
        self.comm.write('FREQuency:STARt %s' % str(x))

    def get_start_freq(self) -> float:
        """Reads start frequency (Hz)."""
        x = self.comm.query('FREQuency:STARt?')

        # Converts the result to the expected type,
        # if fails, returns the raw string.
        try:
            x = float(x)
        except ValueError:
            x = x.strip()

        return x

    def set_stop_freq(self, x: Union[float, str]) -> None:
        """Sets stop frequency (Hz)."""
        self.comm.write('FREQuency:STOP %s' % str(x))

    def get_stop_freq(self) -> float:
        """Reads stop frequency (Hz)."""
        x = self.comm.query('FREQuency:STOP?')

        # Converts the result to the expected type,
        # if fails, returns the raw string.
        try:
            x = float(x)
        except ValueError:
            x = x.strip()

        return x

    def set_cent_freq(self, x: Union[float, str]) -> None:
        """Sets center frequency (Hz)."""
        self.comm.write('FREQuency:CENTer %s' % str(x))

    def get_cent_freq(self) -> float:
        """Reads center frequency (Hz)."""
        x = self.comm.query('FREQuency:CENTer?')

        # Converts the result to the expected type,
        # if fails, returns the raw string.
        try:
            x = float(x)
        except ValueError:
            x = x.strip()

        return x

    def set_span(self, x: Union[float, str]) -> None:
        """Sets span (Hz)."""
        self.comm.write('FREQuency:SPAN %s' % str(x))

    def get_span(self) -> float:
        """Reads span (Hz)."""
        x = self.comm.query('FREQuency:SPAN?')

        # Converts the result to the expected type,
        # if fails, returns the raw string.
        try:
            x = float(x)
        except ValueError:
            x = x.strip()

        return x

    def set_rbw(self, x: Union[float, str]) -> None:
        """Sets resolution bandwidth (Hz)."""
        self.comm.write('BWIDth:RESolution %s' % str(x))

    def get_rbw(self) -> float:
        """Reads resolution bandwidth (Hz)."""
        x = self.comm.query('BWIDth:RESolution?')

        # Converts the result to the expected type,
        # if fails, returns the raw string.
        try:
            x = float(x)
        except ValueError:
            x = x.strip()

        return x

    def set_vbw(self, x: Union[float, str]) -> None:
        """Sets video bandwidth (Hz)."""
        self.comm.write('BANDwidth:VIDeo %s' % str(x))

    def get_vbw(self) -> float:
        """Reads video bandwidth (Hz)."""
        x = self.comm.query('BANDwidth:VIDeo?')

        # Converts the result to the expected type,
        # if fails, returns the raw string.
        try:
            x = float(x)
        except ValueError:
            x = x.strip()

        return x
