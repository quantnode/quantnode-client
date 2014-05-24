#!/usr/bin/env python

"""
Quantnode command script
"""

if __name__ == '__main__':
    import argparse
    import os
    from quantnode import commands

    parser = argparse.ArgumentParser()
    parser.add_argument(
        "command",
        help="The command to execute",
        choices = commands.COMMAND_METHODS.keys(),
        type = str
    )

    parser.add_argument(
        '-p', '--path',
        help = "Project path. Only required for remote invocations",
        default = os.getcwd()
    )

    parser.add_argument(
        '-d', '--data',
        help = "Remote invocation data. Only required for remote invocations"
    )

    args = parser.parse_args()
    settingspath = os.path.join(os.getcwd(), 'settings.py')
    commands.load_settings(settingspath)


    cmd = commands.COMMAND_METHODS.get(args.command)
    if cmd:
        cmd(args)
    else:
        raise Exception('Unknown command: %s' % args.command)

