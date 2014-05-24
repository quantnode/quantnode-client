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



COMMAND_REMOTE_INVOCATION = 'start_invocation_handler'

COMMAND_METHODS = {
    COMMAND_REMOTE_INVOCATION: start_invocation_handler,
}

