from __future__ import print_function

import os
import sys
import Pyro4

settings = None

def load_settings(settingspath):
    dirpath = os.path.dirname(settingspath)
    if dirpath not in sys.path:
        sys.path.insert(0, dirpath)

    fname = os.path.basename(settingspath)
    modname = fname.replace('.py', '')

    global settings
    settings = __import__(modname)


def get_setting(name):
    global settings
    if hasattr(settings, name):
        return getattr(settings, name)
    return None



def start_invocation_handler(args):
    import invoke
    handler = invoke.RemoteInvocationHandler()
    config = {
        handler: 'quantnode.remote_invocation_handler'
    }

    Pyro4.Daemon.serveSimple(config, ns = True)


def handle_run_command(args):
    from .actors import run

    testserver_host = args.testserver
    if args.testserver:
        run(testserver_host, calculations=True, backtest=True)

    if hasattr(settings, 'TEST_SERVER_ADDRESS'):
        testserver_host = getattr(settings, 'TEST_SERVER_ADDRESS', '')
        if testserver_host:
            run(testserver_host, calculations=True, backtest=True)

    sys.stderr.write('no testserver hostname found\n')
    print('No testserver hostname found. Use: ./quantnode-run.py run -t hostname or set TEST_SERVER_ADDRESS in settings.py')



COMMAND_REMOTE_INVOCATION = 'start_invocation_handler'
COMMAND_RUN = 'run'

COMMAND_METHODS = {
    COMMAND_REMOTE_INVOCATION: start_invocation_handler,
    COMMAND_RUN: handle_run_command
}

