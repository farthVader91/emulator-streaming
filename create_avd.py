#!/usr/bin/env python
import os
from subprocess import check_call

def _create_avd(name):
    check_call([
        'android', 'create', 'avd', '-t', 'android-24',
        '-b', 'google_apis/x86', '-d', 'he-custom-480',
        '-s', '480x800', '-c', '512M', '-n', name, '-f'
    ])


def get_avd_path(name):
    AVD_ROOT = os.path.expanduser('~/.android/avd/')
    return os.path.join(AVD_ROOT, name+'.avd')

def modify_avd_config(name):
    config_p = os.path.join(get_avd_path(name), 'config.ini')
    with open(config_p, 'a') as target:
        target.write('disk.dataPartition.size=768M\n')
        target.write('vm.heapSize=64\n')
        target.write('hw.ramSize=1024\n')
        target.write('hw.gpu.enabled=yes\n')

def create_avd(name):
    _create_avd(name)
    modify_avd_config(name)
    return True

def main():
    name = 'my-avd'
    create_avd(name)

if __name__ == '__main__':
    main()
