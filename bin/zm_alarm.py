#!/usr/bin/env python

"""
Usage:
    zm_alarm.py --trigger MONITOR [options]
    zm_alarm.py --clear MONITOR [options]

Options:
    -h, --help                      Show this help message and exit.
    --config CONFIG                 Configuration file. Defaults to secrets.yaml. [default: /home/homeassistant/.homeassistant/secrets.yaml]
    -c MONITOR, --clear MONITOR     Clear an alarm on the monitor.
    -t MONITOR, --trigger MONITOR   Trigger an alarm on the monitor.
    -d LEVEL, --debug LEVEL         Debugging level during execution. Available options: DEBUG, INFO, WARNING, ERROR (default), CRITICAL. [default: ERROR]
"""

import json, logging, os, yaml
from docopt import docopt
from zoneminder import ZoneMinder

def main():
    zm = ZoneMinder(cfg['zm_host'], cfg['zm_user'], cfg['zm_pass'])
    if arguments['--trigger'] != None:
        zm.triggerAlarm(arguments['--trigger'])
    elif arguments['--clear'] != None:
        zm.clearAlarm(arguments['--clear'])
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
