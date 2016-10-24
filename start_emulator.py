#!/usr/bin/env python
import os
import sys
import signal
import time
if os.name == 'posix' and sys.version_info[0] < 3:
    import subprocess32 as subprocess
else:
    import subprocess


def _start_emulator(avd_n, port):
    proc = subprocess.Popen([
        'emulator', '-avd', avd_n, '-port', str(port), '-no-boot-anim',
        '-gpu', 'swiftshader', '-accel', 'on', '-netfast', '-nojni',
        '-qemu', '-enable-kvm'
    ])
    return proc


def kill_child(pid):
    os.kill(pid, signal.SIGTERM)


def wait_for_device(emulator_port, timeout, attempt=0):
    if attempt > 10:
        raise Exception('Waited too long...')
    device = 'emulator-{}'.format(emulator_port)
    try:
        result = subprocess.check_output([
            'adb', '-s', device, 'wait-for-device', 'shell', 'getprop',
            'sys.boot_completed'
        ], timeout=timeout)
        if result.strip() == '1':
            return True
        else:
            print 'device is up, but not completely booted. trying again...'
            time.sleep(2)
            wait_for_device(emulator_port, timeout, attempt+1)
    except subprocess.TimeoutExpired:
        print 'Emulator took too long to start...'
        raise
    return True


def start_emulator(avd_n, port, timeout):
    start_time = time.time()
    proc = _start_emulator(avd_n, port)
    try:
        wait_for_device(port, timeout)
        print 'emulator is ready...'
        print 'emulator took {:.2f} seconds to start'.format(
            time.time() - start_time)
        return proc
    except:
        print 'Killing Emulator...'
        kill_child(proc.pid)


def main():
    avd_n = 'my-avd'
    em_port = 5554
    timeout = 6 #seconds
    start_emulator(avd_n, em_port, timeout)

if __name__ == '__main__':
    main()
