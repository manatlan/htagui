# -*- coding: utf-8 -*-
# #############################################################################
# Copyright (C) 2024 manatlan manatlan[at]gmail(dot)com
#
# MIT licence
#
# https://github.com/manatlan/htag
# #############################################################################

from htag import Tag
from .common import TagStep

#-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
# dont know how it can work ... but it does the job
#-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
try:
    from .basics import bases as cui
    print("IMPORT [BASICS]")
except ImportError:
    try:
        from .bulma import bases as cui
        print("IMPORT [BULMA]")
    except ImportError:
        from .shoelace import bases as cui
        print("IMPORT [SHOELACE]")
#-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=

class Tabs(Tag.div,TagStep):

    def init(self,*objs,onchange=lambda x:x,**a):
        self._previous_selected=None
        self._selected=0
        self.onchange=onchange
        self._tabs=list(objs)
        TagStep.init(self)

    def step(self,**params):
        if "select" in params:
            self._selected=int(params["select"])

        if self._selected != self._previous_selected:
            self( cui.Tabs, self._selected )
            self._previous_selected=self._selected
            self.onchange(self)

    @property
    def selected(self):
         return self._selected

    @property
    def size(self):
         return len(self._tabs)
         
    @selected.setter
    def selected(self,v):
        self.step(select=v)
    
    def cls(self):
        self._tabs.clear()
        self._selected=None
        self.step()        
    
    def add_tab(self,o):
        self._tabs.append(o)
        self._selected=self._tabs.index(o)
        self.step()
