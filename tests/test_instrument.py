import unittest
import matplotlib.pyplot as plt

from rohdeschwarzfpc import FPC


class InstrumentTest(unittest.TestCase):
    instrument_address = 'TCPIP0::172.16.10.10::inst0::INSTR'

    def test_init(self):
        s = FPC(self.instrument_address)
        id = s.comm.query('*IDN?')
        print(f'Instrument IDN string: {id}')

    def test_get_trace(self):
        s = FPC(self.instrument_address)

        n = 1  # Trace number
        tr = s.get_trace(n)
        self.assertEqual(tr['x'].shape, tr['y'].shape)

        # plt.semilogy(tr['x'], tr['y'])
        # plt.xlabel('%s (%s)' % (tr['name_x'], tr['unit_x']))
        # plt.ylabel('%s (%s)' % (tr['name_y'], tr['unit_y']))

    def test_prop_setget(self):
        set_vals = {'cent_freq': 1e8, 'span': 1e5,
                    'start_freq': 1.5e8, 'stop_freq': 1.7e8,
                    'rbw': 1e3, 'vbw': 1e3}

        s = FPC(self.instrument_address)

        for p in set_vals:
            get_func = getattr(s, f'get_{p}')
            set_func = getattr(s, f'set_{p}')

            # Reads the current value.
            old_val = get_func()

            # Sets a new value and reads it out.
            set_func(set_vals[p])
            new_val = get_func()

            # Restores the initial value.
            set_func(old_val)

            self.assertEqual(new_val, set_vals[p])


if __name__ == "__main__":
    unittest.main()
