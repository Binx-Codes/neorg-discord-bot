#! /usr/bin/env python3
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# File Name: __main__.py

from neorg import neorg
from neorg.log import get_logger, setup_sentry
from neorg.neorg import Neorg, StartupError, constants

if constants.USE_SENTRY:
    setup_sentry()

try:
    neorg.instance = Neorg.create()
    neorg.instance.load_cogs()
    neorg.instance.run(constants.TOKEN)

except StartupError as e:
    message = "Unknown Startup Error Occurred."
    # better error message
    if e.args:
        message = e.args[0]
    log = get_logger("bot")
    log.fatal("", exc_info=e.exception)
    log.fatal(message)

    exit(69)
