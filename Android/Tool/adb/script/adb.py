'''
This is a script for adb
'''
import subprocess
import time
import re
import sys
from pathlib import Path
from threading import Thread

import argparse
parser = argparse.ArgumentParser(description='This is a script for adb.')
parser.add_argument('-p', '--package', type=str, help='Package you need to debug.')
parser.add_argument('-i', '--interactive', action='store_true', help='Interactive mode.')
parser.add_argument('-s', '--stack', action='append', help='so libraries.')
# parser.add_argument('getpid', nargs='*', help='Interactive mode.')
# parser.add_argument('package', nargs='*', help='Use package.')

'''
    Constants
'''
# TODO Can get from env
# ADB_PATH = ['adb', '-s', '127.0.0.1:1111']
ADB_PATH = ['adb']

RESULT_EXIT = -1
RESULT_SUCCESS = 0
RESULT_FAIL = 1

CMD_EXIT = 'exit()'
CMD_LOGCAT = 'logcat'
CMD_PACKAGE = 'package'
CMD_SHELL = 'shell'
CMD_STACK = 'stack'
CMD_GET_PID = 'getpid'

MSG_ENTER_TO_QUIT = 'Enter to quit:'
MSG_QUIT_CMD = 'CMD - {} - finished.'
MSG_EMPTY = ' ' * 128
MSG_WAITING_FOR_PACKAGE = 'Waiting for pacakge {}{}'

RE_PS_FORMAT = '(\S+)\s+(\S+)\s+(\S+)\s+(\S+)\s+(\S+)\s+(\S+)\s+(\S+)\s+(\S+)\s+(\S+)'
RE_STACK_FORMAT = '(\S+)\s+(\S+)\s+(\S+)\s+(\S+)\s+(\S+)\s+xunwind_tag:\s+(\S+)\s+(\S+)\s+(\S+)\s+(\S+).*'
'''
    Common Functions
'''
def _errorLog(err):
    print('Error:', err)

def _verboseLog(err):
    print('Verbose:', err)

def _cmd(cmd, block=False):
    p = subprocess.Popen(cmd, stderr=subprocess.PIPE, stdout=subprocess.PIPE)
    if block:
        try:
            result = p.stdout.read().decode('utf-8').strip()
            # result = p.communicate()[0].decode('utf-8').strip()
        except:
            pass
        return result
    return p

'''
    Class
'''
class InteractiveSystem:
    def __init__(self, args) -> None:
        self.args = args
        self._running = False

    # Start to get cmd for debug
    def start(self):
        self._running = True
        while self._running:
            # Get input from user
            try:
                cmd = input('$ ')
                rst = _execCmd(cmd, self.args.package, self.args.stack)

                # Exit interactive system if call exit()
                if RESULT_EXIT == rst:
                    self._running = False
            except EOFError:
                pass


# Adb commands
class AdbTool:
    def __init__(self) -> None:
        self.rePs = re.compile(RE_PS_FORMAT)
        self.status = {}
        self.printThread = 0
        self.reStack = re.compile(RE_STACK_FORMAT)

    # Get pid by package name
    def getPackagePid(self, package):
        cmd = ADB_PATH + [CMD_SHELL, 'ps', '-A', '|', 'grep', package]
        result = _cmd(cmd, block=True)
        rst = self.rePs.match(result)
        if rst:
            try:
                return int(rst.group(2))
            except Exception as e:
                print(e.args)
        return 0

    # Make sure only the current thread can print
    def _print(self, printId, *args, **kwargs):
        if self.printThread == printId:
            print(*args, **kwargs)

    def _logcatThread(self, status, cmd, package, preFunc=None):
        pid = None
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
            tCmd = cmd[:]
            if pid:
                tCmd += [f'--pid={pid}']
            process = _cmd(tCmd)
            thread = Thread(target=self._logcatPrintThread, args=[process, self.printThread, preFunc])
            thread.daemon = True
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
            if package and pid != pStatus[0]:
                if pStatus[0] != 0:
                    pid = pStatus[0]
                    needToRestart = True
        self.printThread += 1
        if process:
            process.kill()
        if package:
            pStatus[1] = False

    def _logcatPrintThread(self, process, printId, preFunc=None):
            while process.poll() is None:
                try:
                    content = process.stdout.readline().decode('utf-8').strip()
                except:
                    pass
                if preFunc:
                    content = preFunc(content)
                self._print(printId, content)
                # self._print(printId, MSG_ENTER_TO_QUIT, end='\r')


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

    def logcat(self, args, package=None, stack=None):
        status = [True,]
        cmd = ADB_PATH + [CMD_LOGCAT]
        cmd.extend(args)

        def stackFunc(content):
            libMap = {}
            for lib in stack:
                libPath = Path(lib)
                if libPath.exists():
                    libMap[libPath.name] = libPath
            rst = self.reStack.match(content)
            func = ''
            if rst:
                addr = rst.group(8)
                lib = rst.group(9).split('/')[-1]
                libPath = libMap.get(lib)
                if libPath:
                    func = _cmd('addr2line -f -e ' + str(libPath) + ' ' + addr, block=True)
                    return content.replace(rst.group(9), lib) + ' ' + func
            return content
        preFunc = None
        if stack:
            preFunc = stackFunc

        thread = Thread(target=self._logcatThread, args=[status, cmd, package, preFunc])
        thread.daemon = True
        thread.start()
        input()
        status[0] = False
        while thread.is_alive():
            time.sleep(0.1)
        print(MSG_QUIT_CMD.format(CMD_LOGCAT))

    def default(self, *args):
        cmd = ADB_PATH
        cmd.extend(args)
        result = _cmd(cmd, block=True)
        print(result)

'''
    Main Functions
'''
_adbTool = AdbTool()

# Exec cmd
def _execCmd(cmd: str, package=None, stack=None):
    if CMD_EXIT == cmd:
        return RESULT_EXIT
    if cmd.startswith(CMD_LOGCAT):
        _adbTool.logcat(cmd.split(' ')[1:])
    elif cmd.startswith(CMD_PACKAGE):
        secCmd = cmd.split(' ')[1]
        if secCmd == CMD_LOGCAT:
            _adbTool.logcat(cmd.split(' ')[2:], package)
        elif secCmd == CMD_STACK:
            _adbTool.logcat(cmd.split(' ')[2:], package, stack)
    elif cmd.startswith(CMD_GET_PID):
        print(_adbTool.getPackagePid(package))
    else:
        _adbTool.default(*cmd.split(' '))
    return 0

def _interactive(args):
    _verboseLog('Coming into the interactive mode for debug')
    interactiveSystem = InteractiveSystem(args)
    interactiveSystem.start()

def main(args):
    if args.interactive:
        _interactive(args)
    else:
        # TODO make all cmd the same
        cmd = sys.argv[1:]
        indexP = cmd.index('-p')
        cmd.pop(indexP)
        cmd.pop(indexP)
        _execCmd(' '.join(cmd), args.package, args.stack)

if __name__ == '__main__':
    args = parser.parse_args()
    main(args)
