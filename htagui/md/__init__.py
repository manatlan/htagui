# -*- coding: utf-8 -*-
# #############################################################################
# Copyright (C) 2024 manatlan manatlan[at]gmail(dot)com
#
# MIT licence
#
# https://github.com/manatlan/htag
# #############################################################################

import __main__
__main__.htaguimodule = "htagui.md.bases"

"""
MD miss a lot of native widgets ;-(
and pop menu in a dialog box appears behind ;-( (not a zindex troubble, but a big problem))
so MD is not first class as others ;-(
"""

########################################################################################
from .bases import Button,Input,Textarea,Menu,Spinner,Select,Radios
########################################################################################
from ..all import *

ALL.extend( [Button,Input,Textarea,Select,Radios,Menu,Spinner] )
__all__=[i.__name__ for i in ALL] + ["hflex","vflex", "ALL"]
