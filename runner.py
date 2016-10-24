#!/usr/bin/env python
import create_avd
import start_emulator

def main():
    """
    for i in range(5):
        avd_n = 'my-avd-%d' % (i,)
        create_avd.create_avd(avd_n)
    """
    for i in range(5):
        avd_n = 'my-avd-%d' % (i,)
        em_port = 5554 + (i*2)
        start_emulator.start_emulator(avd_n, em_port, 100)

if __name__ == '__main__':
    main()
