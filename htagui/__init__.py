# -*- coding: utf-8 -*-
# #############################################################################
# Copyright (C) 2024 manatlan manatlan[at]gmail(dot)com
#
# MIT licence
#
# https://github.com/manatlan/htag
# #############################################################################

__version__ = "0.0.0" # auto updated

########################################################################################
from .basics import Button,Input,Menu,Spinner,Select
########################################################################################
from .form import Form
from .tabs import Tabs
from .uiservice import UI
from .splitters import HSplit #VSplit
from .flex import hflex,vflex  # utilities (Htag contructor methods)

ALL=[Button,Input,Select,Menu,Spinner,Form,Tabs,UI,HSplit]
