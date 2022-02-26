#   -*- coding: utf-8 -*-
from pybuilder.core import init, use_plugin

use_plugin("python.core")
use_plugin("python.unittest")
use_plugin("python.flake8")
use_plugin("python.coverage")
use_plugin("python.distutils")

name = "neorg-discord-bot"
default_task = "publish"


@init
def set_properties(project):
    pass
