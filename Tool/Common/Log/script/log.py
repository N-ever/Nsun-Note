from pathlib import Path

import argparse
import re

GLOB_LOG_PATH = '*.log'
RE_LOG_PATH = 'log\D*(\d*)\.log'

parser = argparse.ArgumentParser(description='This is a script for adb.')
parser.add_argument('-i', '--input', type=str, help='The log dir.')
parser.add_argument('-o', '--output', type=str, default='all.log', help='The output log.')

def getLogPaths(inputPath: Path):
    reLog = re.compile(RE_LOG_PATH)
    logPaths = []
    for log in inputPath.glob(GLOB_LOG_PATH):
        rst = reLog.match(str(log.name))
        if rst:
            num = rst.group(1)
            if num == '':
                num = 0
            else:
                num = int(num)
            logPaths.append((num, log))
    logPaths.sort(key=lambda a: a[0], reverse=True)
    return logPaths

def joinLogs(logPaths, output):
    with open(str(output), 'w+') as outLog:
        for _, log in logPaths:
            with open(str(log), 'r+') as f:
                outLog.write(f'-------------------------------- {log.name} --------------------------------\n')
                outLog.write(f.read())


def main(args):
    inputPath = Path(args.input)
    outputPath = inputPath.joinpath(args.output)
    assert inputPath.exists(), "Can not find input dir."
    logPaths = getLogPaths(inputPath)
    joinLogs(logPaths, outputPath)


if __name__ == '__main__':
    args = parser.parse_args()
    main(args)
