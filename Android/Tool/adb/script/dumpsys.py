from util import Log, cmd
from dumpsys_surfaceflinger import dump_surfaceflinger

import argparse
parser = argparse.ArgumentParser(description='This is a script for dumpsys.')
parser.add_argument('--surfaceflinger', action="store_true", help='Dump SurfaceFlinger Info.')


############### Main ###############
def main(args):
    Log.set_log_level(Log.LOG_DEBUG)
    if not args.surfaceflinger:
        dump_surfaceflinger()


if __name__ == '__main__':
    args = parser.parse_args()
    main(args)