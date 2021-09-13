import json
import os
import pyvisa
import numpy as np

from typing import Union


class FPC:
    """Class for communication with Rohde & Schwarz FPC spectrum analyzers.

    Attributes:
        comm: Visa resource that performs read and write operations on 
            the physical device. 
    """

    def __init__(self, address: str = ''):
        """"Inits an instance of the instrument class and open communication
        using the address.

        Args:
            address: 
                A visa resource name, e.g. 'TCPIP0::172.16.10.10::inst0::INSTR'.
                If not supplied explicitly, it is loaded from the config file.
        """

        rm = pyvisa.ResourceManager()

        if not address:
            c = get_config()

            if 'address' in c:
                address = c['address']
            else:
                raise ValueError('An instrument address must be supplied '
                                 'or set in the config file using set_config.')

        self.comm = rm.open_resource(address)

    def get_trace(self, n: int = 1, mem: bool = False) -> dict:
        """Reads a current trace from the instrument. Does not initiate or 
        stop data acquisition.

        Args:
            n: 
                Trace number.
            mem: 
                Selects between reading a currently displayed trace (False) 
                and reading a reference stored in the memory (True).

        Returns:
            A dictionary with the x and y data (under the keys 'x' and 'y'), 
            and metadata.
        """

        d = {'x': None,
             'y': None,
             'xlabel': 'Frequency (Hz)',
             'ylabel': '$S_V$'}  # y unit will be determined later.

        if mem:
            kind = ':MEMory'
        else:
            kind = ''

        # Configures the device for binary data transfer and queries y data.
        req = 'FORMat REAL,32;:TRACe:DATA%s? TRACE%i' % (kind, n)
        y = self.comm.query_binary_values(req, datatype='f',
                                          container=np.ndarray)

        # Queries the start frequency, the stop frequency
        # and the unit of the y data.
        resp = self.comm.query(':FREQuency:STARt?;:FREQuency:STOP?;'
                               ':UNIT:POWer?;:BWIDth:RESolution?')

        f1, f2, unit, rbw = resp.split(sep=';')

        # Calculates the frequency axis.
        d['x'] = np.linspace(float(f1), float(f2), len(y))

        if unit.lower() == 'dbm':
            # Normally, spectra returned by the device are in dBm, while
            # it is more convenient to process them on a linear scale.

            # Converts the data to V^2/Hz, assuming 50 Ohm input impedance.
            d['y'] = 50*0.001*(10**(y/10))/float(rbw)
            d['ylabel'] = ('%s (V$^2$/Hz)' % d['ylabel'])
        else:
            # Leaves the data as it is.
            d['y'] = y

        return d

    def get_idn(self):
        """Reads the identifying string from the device."""
        str = self.comm.query('*IDN?')
        return str.strip()

    # Setter and getter methods for the instrument parameters

    def set_start_freq(self, x: Union[float, str]) -> None:
        """Sets the start frequency (Hz)."""
        self.comm.write(f'FREQuency:STARt {x}')

    def get_start_freq(self) -> float:
        """Reads the start frequency (Hz)."""
        x = self.comm.query('FREQuency:STARt?')

        # Converts the result to the expected type,
        # if fails, returns the raw string.
        try:
            x = float(x)
        except ValueError:
            x = x.strip()

        return x

    def set_stop_freq(self, x: Union[float, str]) -> None:
        """Sets the stop frequency (Hz)."""
        self.comm.write(f'FREQuency:STOP {x}')

    def get_stop_freq(self) -> float:
        """Reads the stop frequency (Hz)."""
        x = self.comm.query('FREQuency:STOP?')

        # Converts the result to the expected type,
        # if fails, returns the raw string.
        try:
            x = float(x)
        except ValueError:
            x = x.strip()

        return x

    def set_cent_freq(self, x: Union[float, str]) -> None:
        """Sets the center frequency (Hz)."""
        self.comm.write(f'FREQuency:CENTer {x}')

    def get_cent_freq(self) -> float:
        """Reads the center frequency (Hz)."""
        x = self.comm.query('FREQuency:CENTer?')

        # Converts the result to the expected type,
        # if fails, returns the raw string.
        try:
            x = float(x)
        except ValueError:
            x = x.strip()

        return x

    def set_span(self, x: Union[float, str]) -> None:
        """Sets the span (Hz)."""
        self.comm.write(f'FREQuency:SPAN {x}')

    def get_span(self) -> float:
        """Reads the span (Hz)."""
        x = self.comm.query('FREQuency:SPAN?')

        # Converts the result to the expected type,
        # if fails, returns the raw string.
        try:
            x = float(x)
        except ValueError:
            x = x.strip()

        return x

    def set_rbw(self, x: Union[float, str]) -> None:
        """Sets the resolution bandwidth (Hz)."""
        self.comm.write(f'BWIDth:RESolution {x}')

    def get_rbw(self) -> float:
        """Reads the resolution bandwidth (Hz)."""
        x = self.comm.query('BWIDth:RESolution?')

        # Converts the result to the expected type,
        # if fails, returns the raw string.
        try:
            x = float(x)
        except ValueError:
            x = x.strip()

        return x

    def set_vbw(self, x: Union[float, str]) -> None:
        """Sets the video bandwidth (Hz)."""
        self.comm.write(f'BANDwidth:VIDeo {x}')

    def get_vbw(self) -> float:
        """Reads the video bandwidth (Hz)."""
        x = self.comm.query('BANDwidth:VIDeo?')

        # Converts the result to the expected type,
        # if fails, returns the raw string.
        try:
            x = float(x)
        except ValueError:
            x = x.strip()

        return x


def set_config(newc: dict) -> None:
    """Adds the content of newc dictionary to the configuration file. """

    c = get_config()
    c.update(newc)

    # Configurations are stored in the package installation folder.
    filename = os.path.join(os.path.dirname(__file__), 'config.json')

    with open(filename, 'w') as fp:
        json.dump(c, fp, indent=1)


def get_config() -> dict:
    """Returns the content of the configuration file as a dictionary. """

    # Configurations are stored in the package installation folder.
    filename = os.path.join(os.path.dirname(__file__), 'config.json')

    try:
        with open(filename, 'r') as fp:
            c = json.load(fp)
    except FileNotFoundError:
        c = {}
    
    return c