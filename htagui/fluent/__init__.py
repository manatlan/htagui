# -*- coding: utf-8 -*-
# #############################################################################
# Copyright (C) 2024 manatlan manatlan[at]gmail(dot)com
#
# MIT licence
#
# https://github.com/manatlan/htag
# #############################################################################

import __main__
__main__.htaguimodule = "htagui.fluent.bases"

"""TODO: ui.Tabs is KO ! fix !"""

########################################################################################
from .bases import Button,Input,Textarea,Menu,Spinner,Select,Radios
########################################################################################
from ..all import *

ALL.extend( [Button,Input,Textarea,Select,Radios,Menu,Spinner] )
__all__=[i.__name__ for i in ALL] + ["hflex","vflex", "ALL"]
