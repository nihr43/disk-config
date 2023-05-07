import json
import subprocess

def get_disks():
    process = subprocess.run("/usr/bin/lsblk --json -o NAME".split(),
                             capture_output=True, text=True)

    disks = []

    # dict blockdevices contains key blockdevices
    blockdevices = json.loads(process.stdout)
    for d in blockdevices['blockdevices']:
        # im not interested in nvme devices for now
        if d['name'].startswith('sd'):
            print('found {}'.format(d['name']))
            disks.append(d['name'])

    return disks


def disable_cache(disk):
    '''
    disables write cache using hdparm
    '''
    subprocess.check_output("/usr/sbin/hdparm -W 0 /dev/{}".format(disk).split())

if __name__ == '__main__':
    for d in get_disks():
        disable_cache(d)
