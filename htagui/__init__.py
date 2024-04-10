#!/usr/bin/python3 -u
# -*- coding: utf-8 -*-

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
