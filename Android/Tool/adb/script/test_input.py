import re
import time
import random

from util import Log, cmd, ADB_PATH

def input_pos(displayId, x, y):
    inputCmd = ADB_PATH + ['shell', 'input', '-d', str(displayId), 'tap', str(x), str(y)]
    content = cmd(inputCmd, block=True)
    return content

def start_activity(displayId, userId, packageName, className):
    inputCmd = ADB_PATH + ['shell', 'am', 'start', '--display', str(displayId), '--user', str(userId), '{}/{}'.format(packageName, className)]
    content = cmd(inputCmd, block=True)
    return content

if __name__ == '__main__':
    while True:
        # print(input_pos(2, 80, 180))
        print(input_pos(2, 1438, 1580))

        # start_activity(2, 11, 'com.nio.timer', '.MainActivity')
        # time.sleep((random.randint(1, 10) / 10))
        time.sleep(0.1)
