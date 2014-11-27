# -*- coding: utf-8 -*-

import os
import sys
import daemon
import argparse
try:
    from daemon.pidlockfile import PIDLockFile
except ImportError:
    from daemon.pidfile import PIDLockFile
from main import do_dsm

DEFAULT_OUT_PATH = os.path.join(os.path.sep, 'tmp', '.dsm')


def get_pid_path(args):
    return os.path.join(args.out_dir, 'pid')


def get_log_path(args):
    return os.path.join(args.out_dir, 'log')


def get_parser():

    parser = argparse.ArgumentParser(description='Run DSM daemon')

    parser = argparse.ArgumentParser()
    parser.add_argument('-v', '--verbose', dest='verbose', action='store_true', default=False)
    parser.add_argument('-d', '--out-dir', dest='out_dir', metavar='output_directory', default=DEFAULT_OUT_PATH,
                        help='Direcotry for logs, PID file, etc.',)

    mode = parser.add_subparsers(dest="mode")

    class Args(object):
        def __init__(self, *args, **kwargs):
            self.args = args
            self.kwargs = kwargs

    # args re-used in different subparsers
    foreground = Args('-F', '--foreground', action='store_true', default=False)
    ignore_pid = Args('-i', '--ignore-stale-pid', action='store_true', default=False)
    force = Args('-f', '--force', action='store_true', default=False)

    start = mode.add_parser('start')
    start.add_argument(*foreground.args, **foreground.kwargs)
    start.add_argument(*ignore_pid.args, **ignore_pid.kwargs)
    parser.add_argument('port', metavar='port', help="Serial port device path")

    stop = mode.add_parser('stop')
    stop.add_argument(*force.args, **force.kwargs)

    restart = mode.add_parser('restart')
    restart.add_argument(*foreground.args, **foreground.kwargs)
    restart.add_argument(*ignore_pid.args, **ignore_pid.kwargs)
    restart.add_argument(*force.args, **force.kwargs)

    return parser


def start(args):
    if not os.path.exists(args.out_dir):
        os.makedirs(args.out_dir)
    if os.path.exists(get_pid_path(args)):
        if args.ignore_stale_pid:
            os.remove(get_pid_path(args))
        else:
            print >>sys.stderr, '{0}: File exists. Already running?'.format(get_pid_path(args))
            sys.exit(1)

    pid_file = PIDLockFile(get_pid_path(args))
    log_file = open(get_log_path(args), 'a')

    if not args.foreground:
        with daemon.DaemonContext(pidfile=pid_file, stdout=log_file, stderr=log_file):
            do_dsm(args.port)
    else:
        do_dsm(args.port)


def stop(args):

    SIGTERM = 15
    SIGKILL = 9
    try:
        os.kill(int(open(get_pid_path(args), 'r').read()), SIGTERM)
    except IOError:
        pass
    except Exception:
        if args.force:
            os.kill(int(open(get_pid_path(args), 'r').read()), SIGKILL)


def run():

    args = get_parser().parse_args()

    if args.mode == 'start':
        start(args)
    elif args.mode == 'stop':
        stop(args)
    elif args.mode == 'restart':
        stop(args)
        start(args)
    else:
        raise ValueError('Unknown subcommand "{0}"'.format(args.mode))
