#!/usr/bin/env python

"""
Usage:
    zm_state.py --list [options]
    zm_state.py --get [options]
    zm_state.py --set STATE [options]

Options:
    -h, --help                  Show this help message and exit.
    -c CONFIG, --config CONFIG  Configuration file. Defaults to secrets.yaml. [default: /home/homeassistant/.homeassistant/secrets.yaml]
    -g, --get                   Get the current state.
    -l, --list                  List all states.
    -d LEVEL, --debug LEVEL     Debugging level during execution. Available options: DEBUG, INFO, WARNING, ERROR (default), CRITICAL. [default: ERROR]
    -s STATE, --set STATE       Change the current state.
"""

import json, logging, os, yaml
from docopt import docopt
from zoneminder import ZoneMinder

def main():
    zm = ZoneMinder(cfg['zm_host'], cfg['zm_user'], cfg['zm_pass'])
    if arguments['--list']:
        print(json.dumps(zm.getAllStates(), indent=2, sort_keys=True))
    elif arguments['--get']:
        print(zm.getCurrentState())
    elif arguments['--set'] != None:
        if zm.getCurrentState() != arguments['--set']:
            zm.setState(arguments['--set'])
            new_state = zm.getCurrentState()
            if new_state == arguments['--set']:
                print("SUCCESS")
            else:
                print("FAIL")
        else:
            print("State is already {}".format(arguments['--set']))
    else:
        print("Invalid option or usage.")

if __name__ == "__main__":
    arguments = docopt(__doc__)

    # configure logger
    logging.basicConfig(level="WARNING", format='%(asctime)s %(filename)s:%(funcName)s - [%(levelname)s] %(message)s', datefmt='%Y/%m/%d %H:%M:%S')
    logger = logging.getLogger()
    logger.setLevel(arguments['--debug'])
    logger.debug(arguments)

    # read in YAML configuration file
    if "~" in arguments['--config']:
        pattern = re.compile('~')
        arguments['--config'] = pattern.sub(os.path.expanduser("~"), arguments['--config'])
    if not os.path.exists(arguments['--config']):
        logger.error("Specified configuration file does not exist!")
        exit(1)
    with open(arguments['--config'], 'r') as ymlfile:
        cfg = yaml.load(ymlfile)

    main()

    exit(0)
