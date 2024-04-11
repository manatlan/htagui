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

class App(Tag.body):
    _ui=None
    
    @property
    def ui(self):
        if self._ui is None:
            self._ui = UI(self)
        return self._ui

ALL=[App,Button,Input,Select,Menu,Spinner,Form,Tabs,UI,HSplit]
__all__=["App","Button","Input","Select","Menu","Spinner","Form","Tabs","UI","HSplit",      "hflex","vflex"]
