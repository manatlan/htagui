# -*- coding: utf-8 -*-
# #############################################################################
# Copyright (C) 2024 manatlan manatlan[at]gmail(dot)com
#
# MIT licence
#
# https://github.com/manatlan/htag
# #############################################################################

from htag import Tag

from .form import Form
from .tabs import Tabs
from .dialog import Dialog
from .splitters import HSplit #VSplit
from .flex import hflex,vflex  # utilities (Htag contructor methods)
from .ifields import IText,ITextarea,IRange,IBool,ISelect,IRadios

class App(Tag.body):
    _ui=None
    
    @property
    def ui(self):
        if self._ui is None:
            self._ui = Dialog(self)
        return self._ui

ALL=[App,Form,Tabs,Dialog,HSplit,IText,ITextarea,IRange,IBool,ISelect,IRadios]
