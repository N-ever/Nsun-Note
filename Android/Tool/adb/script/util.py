import datetime
import subprocess

ADB_PATH = ['adb']

class Log:
    LOG_VERBOSE = 0
    LOG_DEBUG = 1
    LOG_INFO = 2
    LOG_WARN = 3
    LOG_ERROR = 4
    LOG_LEVERL = LOG_VERBOSE
    LOG_TIME = False

    def log(log_level, msg, tag=None, color=None, time=LOG_TIME):
        if log_level >= Log.LOG_LEVERL:
            content = msg
            if tag:
                content = '[{}] {}'.format(tag, content)
            if time:
                content = '{} {}'.format(get_current_time(), content)
            if color:
                content = '\033[{}m{}\033[0m'.format(color, content)
            print(content)


    def e(msg, exit=False):
        Log.log(Log.LOG_ERROR, msg, 'E', 31, Log.LOG_TIME)
        assert not exit


    def i(msg):
        Log.log(Log.LOG_ERROR, msg, 'I', 32, Log.LOG_TIME)


    def w(msg):
        Log.log(Log.LOG_WARN, msg, 'W', 33, Log.LOG_TIME)


    def d(msg):
        Log.log(Log.LOG_DEBUG, msg, 'D', time=Log.LOG_TIME)


    def v(msg):
        Log.log(Log.LOG_VERBOSE, msg, 'V', time=Log.LOG_TIME)


    def set_log_level(level):
        Log.LOG_LEVERL = level

    def set_time(time):
        Log.LOG_TIME = time


def cmd(cmd, block=False):
    Log.d('cmd: {}'.format(cmd))
    p = subprocess.Popen(cmd, stderr=subprocess.STDOUT, stdout=subprocess.PIPE)
    if block:
        try:
            result = p.stdout.read().decode('utf-8').strip()
        except:
            pass
        return result
    return p

def get_current_time():
    return datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S:%f')[:-3]