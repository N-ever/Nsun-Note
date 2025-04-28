from argparse import ArgumentParser
import json
import os
import subprocess
import datetime

parser = ArgumentParser(description='This is a script for build.')
parser.add_argument('-r', '--remote', help='Install on remote.')
parser.add_argument('-p', '--projects', nargs="+", help='SubProject names.')
parser.add_argument('-s', '--skips', nargs="+", default="", help='Skip steps.')
parser.add_argument('-n', '--name', help='Project name.')
parser.add_argument('-o', '--out', help='Save log as file.')

ROOT_DIR = os.path.expanduser('~')
TMP_NAME = '.evern'
TMP_DIR = os.path.join(ROOT_DIR, TMP_NAME)

class Log:
    LOG_VERBOSE = 0
    LOG_DEBUG = 1
    LOG_INFO = 2
    LOG_WARN = 3
    LOG_ERROR = 4
    LOG_LEVERL = LOG_VERBOSE
    LOG_TIME = False

    def log(log_level, *msg, tag=None, color=None, time=LOG_TIME):
        if log_level >= Log.LOG_LEVERL:
            content = ' '.join(str(tmp) for tmp in msg)
            if tag:
                content = '[{}] {}'.format(tag, content)
            if time:
                content = '{} {}'.format(get_current_time(), content)
            if color:
                content = '\033[{}m{}\033[0m'.format(color, content)
            print(content)


    def e(*msg, exit=False):
        Log.log(Log.LOG_ERROR, *msg, tag='E', color=31, time=Log.LOG_TIME)
        assert not exit


    def i(*msg):
        Log.log(Log.LOG_ERROR, *msg, tag='I', color=32, time=Log.LOG_TIME)


    def w(*msg):
        Log.log(Log.LOG_WARN, *msg, tag='W', color=33, time=Log.LOG_TIME)


    def d(*msg):
        Log.log(Log.LOG_DEBUG, *msg, tag='D', time=Log.LOG_TIME)


    def v(*msg):
        Log.log(Log.LOG_VERBOSE, *msg, tag='V', time=Log.LOG_TIME)


    def set_log_level(level):
        Log.LOG_LEVERL = level

    def set_time(time):
        Log.LOG_TIME = time


def get_current_time():
    return (datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'), datetime.datetime.now().timestamp())


def cmd(cmd, cwd=None, block=True, file=None):
    Log.d('cmd: {} cwd: {}'.format(cmd, cwd))
    p = subprocess.Popen(cmd, cwd=cwd, stderr=subprocess.STDOUT, stdout=subprocess.PIPE, shell=True)
    if block:
        try:
            # 实时读取输出
            f = None
            if file:
                f = open(file, "w")
            result = []
            for line in iter(p.stdout.readline, b""):  # 使用迭代逐行读取
                line_decoded = line.decode("utf-8").strip()
                if f:
                    f.write(line_decoded + "\n")
                else:
                    print(line_decoded)  # 实时打印
                result.append(line_decoded)
            if f:
                f.close()
            p.stdout.close()  # 关闭标准输出
            p.wait()  # 等待进程结束
            if p.returncode != 0:
                print(f"Command failed with return code {p.returncode}")
                return False
            return "\n".join(result)
        except Exception as e:
            print(f"Error: {e}")
            return False
    #     try:
    #         result = p.stdout.read().decode('utf-8').strip()
    #     except:
    #         pass
    #     return result
    return True

def project_to_dict(obj):
    if isinstance(obj, JSONSerializable):
        return obj.__dict__


class JSONSerializable:
    def to_json(self):
        return json.dumps(vars(self), indent=4, ensure_ascii=False, default=project_to_dict)

class Project(JSONSerializable):
    def __init__(self, content=None) -> None:
        if content:
            self.parse(content)
        else:
            self.name = ""
            self.build = ""
            self.install = ""
            self.start = ""
            self.pre_remote = ""

    def parse(self, data):
        self.name = data.get("name")
        self.build = data.get("build")
        self.install = data.get("install")
        self.start = data.get("start")
        self.pre_remote = data.get("pre_remote")

class BuildConfig(JSONSerializable):
    def __init__(self, content=None) -> None:
        if content:
            self.parse(content)
        else:
            self.build = None
            self.dir = ""
            self.projects = [Project()]

    def parse(self, data):
        self.dir = data.get("dir")
        self.projects = [Project(p) for p in data.get("projects")]
        self.build = data.get("build")

def get_config(name):
    file_name = os.path.join(TMP_DIR, "{}.json".format(name))
    with open(file_name, "r") as f:
        return BuildConfig(json.loads(f.read()))

def main(args):
    starttime = get_current_time()
    config = get_config(args.name)
    result = True
    if "build" not in args.skips and not args.projects and config.build:
        build_all(config.dir, config.build, args.out)
        check_result(result, "Build all")
        Log.i("Build all success.")
    for p in config.projects:
        if not args.projects or p.name in args.projects:
            if "build" not in args.skips and (args.projects or not config.build):
                result = build(config.dir, p, args.out)
                check_result(result, "Build project: " + p.name)
                Log.i("Build project: " + p.name + " success.")
            if "pre_remote" not in args.skips:
                if args.remote:
                    result = pre_remote(config.dir, p, args.out)
                    check_result(result, "Pre remote project: " + p.name)
                    Log.i("Pre remote project: " + p.name + " success.")
            if "install" not in args.skips:
                result = install(config.dir, p, args.remote, args.out)
                check_result(result, "Install project: " + p.name)
                Log.i("Install project: " + p.name + " success.")
            if "start" not in args.skips:
                result = start(config.dir, p, args.remote, args.out)
                check_result(result, "Start project: " + p.name)
                Log.i("Start project: " + p.name + " success.")
    endtime = get_current_time()
    Log.i("Start time: " + starttime[0])
    Log.i("End time: " + endtime[0])
    Log.i("Total time: " + str(round(endtime[1] - starttime[1])) + "s")

def check_result(result, operation=None):
    if not result:
        Log.e("Error: ", operation, "result:", result)
        os._exit(1)

def build_all(cwd, build, out):
    Log.i("Build all: ")
    return cmd(build, cwd=cwd, file=out)

def build(cwd, project, out):
    Log.i("Build project: ", project.name)
    return cmd(project.build, cwd=cwd, file=out)

def pre_remote(cwd, project, out):
    Log.i("Pre remote project: ", project.name)
    return cmd(project.pre_remote, cwd=cwd, file=out)

def install(cwd, project, remote, out):
    Log.i("Install project: ", project.name)
    return cmd(project.install, cwd=cwd, file=out)

def start(cwd, project, remote, out):
    if not project.start or project.start == "":
        return True
    Log.i("Start project: ", project.name)
    return cmd(project.start, cwd=cwd, file=out)

if __name__ == '__main__':
    args = parser.parse_args()
    main(args)
