'''
This is a script for adb
'''
import subprocess
import time
import re
import inspect
import ctypes
from threading import Thread

import argparse
parser = argparse.ArgumentParser(description='This is a script for adb.')
parser.add_argument('-p', '--package', type=str, help='Package you need to debug.')
parser.add_argument('-i', '--interactive', action='store_true', help='Interactive mode.')

'''
    Constants
'''
# TODO Can get from env
ADB_PATH = 'adb'

RESULT_EXIT = -1
RESULT_SUCCESS = 0
RESULT_FAIL = 1

CMD_EXIT = 'exit()'
CMD_LOGCAT = 'logcat'
CMD_PACKAGE_LOGCAT = 'package logcat'
CMD_SHELL = 'shell'
CMD_GET_PID = 'getpid'

MSG_ENTER_TO_QUIT = 'Enter to quit:'
MSG_QUIT_CMD = 'CMD - {} - finished.'
MSG_EMPTY = ' ' * 128
MSG_WAITING_FOR_PACKAGE = 'Waiting for pacakge {}{}'

RE_PS_FORMAT = '(\S+)\s+(\S+)\s+(\S+)\s+(\S+)\s+(\S+)\s+(\S+)\s+(\S+)\s+(\S+)\s+(\S+)'
'''
    Common Functions
'''
def _errorLog(err):
    print('Error:', err)

def _verboseLog(err):
    print('Verbose:', err)

def _cmd(cmd, block=False):
    # print(cmd)
    p = subprocess.Popen(cmd, stderr=subprocess.PIPE, stdout=subprocess.PIPE, shell=True)
    if block:
        result = p.communicate()[0].decode('utf-8').strip()
        return result
    return p

'''
    Class
'''
class InteractiveSystem:
    def __init__(self, package) -> None:
        self.package = package
        self._running = False
        self._adbTool = AdbTool()

    # Start to get cmd for debug
    def start(self):
        self._running = True
        while self._running:
            # Get input from user
            try:
                cmd = input('$ ')
                rst = self._parseCmd(cmd)

                # Exit interactive system if call exit()
                if RESULT_EXIT == rst:
                    self._running = False
            except EOFError:
                pass
            
    # Parse cmd
    def _parseCmd(self, cmd: str):
        if CMD_EXIT == cmd:
            return RESULT_EXIT
        if cmd.startswith(CMD_LOGCAT):
            self._adbTool.logcat(cmd.split(' ')[1:]) 
        elif cmd.startswith(CMD_PACKAGE_LOGCAT):
            self._adbTool.logcat(cmd.split(' ')[2:], self.package) 
        elif cmd.startswith(CMD_GET_PID):
            self._adbTool.getPackagePid(self.package) 
        else:
            self._adbTool.default(*cmd.split(' '))
        return 0

# Adb commands
class AdbTool:
    def __init__(self) -> None:
        self.rePs = re.compile(RE_PS_FORMAT)
        self.status = {}
        self.printThread = 0

    # Get pid by package name
    def getPackagePid(self, package):
        cmd = [ADB_PATH, CMD_SHELL, f'ps -A | grep {package}']
        result = _cmd(cmd, block=True)
        rst = self.rePs.match(result)
        if rst:
            return int(rst.group(2))
        return 0
    
    # Make sure only the current thread can print
    def _print(self, printId, *args, **kwargs):
        if self.printThread == printId:
            print(*args, **kwargs)
    
    def _logcatThread(self, status, cmd, package, preFunc=None):
        pid = 0
        # Start check package thread to listen pid change
        if package:
            pStatus = self.checkPackageStatus(package)
            index = 0
            while status[0] and pStatus[2] is not True:
                time.sleep(1)
                index = (index + 1) % 3
                print(MSG_WAITING_FOR_PACKAGE.format(package, '.' * (index + 1)) + ' ' * (2 - index), end='\r')
            pid = pStatus[0]

        def startPrintThread(pid):
            process = _cmd(cmd + [f'--pid={pid}'])
            thread = Thread(target=self._logcatPrintThread, args=[process, self.printThread, preFunc])
            thread.setDaemon(True)
            thread.start()
            return process
        
        needToRestart = True
        process = None
        while status[0]:
            if needToRestart:
                if process: 
                    process.kill()
                self.printThread += 1 
                process = startPrintThread(pid)
                needToRestart = False
            if pid != pStatus[0]:
                if pStatus[0] != 0:
                    pid = pStatus[0]
                    needToRestart = True
        self.printThread += 1 
        if process: 
            process.kill()
        pStatus[1] = False

    def _logcatPrintThread(self, process, printId, preFunc=None):
            while process.poll() is None:
                content = process.stdout.readline().decode('utf-8').strip()
                if preFunc:
                    content = preFunc(content)
                self._print(printId, content)
                self._print(printId, MSG_ENTER_TO_QUIT, end='\r')
            

    # Start a thread to listen the package status
    # status: [pid, running, packageIsRunning]
    def checkPackageStatus(self, package):
        # [pid, running, packageIsRunning]
        status = [0, True, None]
        def checkStatus(status):
            while status[1]:
                status[0] = self.getPackagePid(package)
                status[2] = True if status[0] > 0 else False
                time.sleep(0.1)
            
        thread = Thread(target=checkStatus, args=[status])
        thread.start()
        self.status[package] = status
        return status

    def logcat(self, args, package=None):
        status = [True,]
        cmd = [ADB_PATH, CMD_LOGCAT]
        cmd.extend(args)
        thread = Thread(target=self._logcatThread, args=[status, cmd, package])
        thread.setDaemon(True)
        thread.start()
        input()
        status[0] = False
        while thread.is_alive():
            time.sleep(0.1) 
        print(MSG_QUIT_CMD.format(CMD_LOGCAT))
            
    def default(self, *args):
        cmd = [ADB_PATH]
        cmd.extend(args)
        result = _cmd(cmd, block=True)
        print(result)

'''
    Main Functions
'''
def _interactive(package):
    _verboseLog('Coming into the interactive mode for debug')
    interactiveSystem = InteractiveSystem(package)
    interactiveSystem.start()

def main(args):
    if args.interactive:
        assert args.package, 'Interactive mode need package to debug.'
        _interactive(args.package)

if __name__ == '__main__':
    args = parser.parse_args()
    main(args)
