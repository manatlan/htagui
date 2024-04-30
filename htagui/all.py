# -*- coding: utf-8 -*-
# #############################################################################
# Copyright (C) 2024 manatlan manatlan[at]gmail(dot)com
#
# MIT licence
#
# https://github.com/manatlan/htag
# #############################################################################

from htag import Tag

# global objects
from .form import Form
from .tabs import Tabs
from .dialog import Dialog
from .splitters import HSplit, VSplit
from .ifields import IText,ITextarea,IRange,IBool,ISelect,IRadios
from .fileupload import FileUpload

class App(Tag.body):
    _ui=None
    
    @property
    def ui(self):
        if self._ui is None:
            self._ui = Dialog(self)
        return self._ui

# global methods
from .flex import hflex,vflex  # utilities (Htag contructor methods)


ALL=[App,Form,Tabs,Dialog,HSplit,VSplit,IText,ITextarea,IRange,IBool,ISelect,IRadios,FileUpload]
