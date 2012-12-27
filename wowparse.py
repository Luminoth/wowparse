#! /usr/bin/env python

import logging
import optparse
import sys
import wx

from wowparse.Event import Event
from wowparse.gui.MainWindow import MainWindow

VERSION = "0.1"
logger = None

def parse_arguments(argv):
    parser = optparse.OptionParser(version="%prog " + VERSION, description="WoW Combat Log Parser",
        usage="Usage: wowparse.py [options]")
    (options, args) = parser.parse_args(argv[1:])

def initialize_logger():
    global logger

    try:
        logger = logging.getLogger("wowparse")
        handler = logging.StreamHandler()
        handler.setFormatter(logging.Formatter("%(asctime)s %(module)s:%(lineno)d %(levelname)s %(message)s"))
        logger.addHandler(handler)
        logger.setLevel(logging.DEBUG)
    except IOError, e:
        print >> sys.stderr, "Could not initialize logger: %s" % e[1]
        sys.exit(1)

def main(argv=None):
    global logger

    if not argv:
        argv = sys.argv
    parse_arguments(argv)

    initialize_logger()
    logger.info("WoW Combat Log Parser version %s starting..." % VERSION)

    logger.info("Building event tables...")
    Event.build_event_tables()

    app = wx.App(False)
    window = MainWindow()
    window.Show(True)
    app.MainLoop()

    return 0

if __name__ == "__main__":
    sys.exit(main())
