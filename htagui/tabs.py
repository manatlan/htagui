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

class Tabs(Tag.div,TagStep):
    statics="""
    .tab {
        border:0px;
        cursor:pointer;
        margin:2px;
    }
    .tab.selected {
        color:blue;
        border-bottom: 1px solid blue;
    }
    """
    #-:-:-:-:-:-:-:-:-:-:-:-:-:-:-:-:-:-:-:-:-:-:-:-:-:-:-:-:-:-:-:-:-:-:-:
    class Show(Tag.div):
        def init(self,main,selected=0):
            for idx,i in enumerate(main._tabs):
                name = hasattr(i,"name") and i.name or "?(name)?"
                self+=Tag.button(name, _onclick = main.stepevent(select=idx), _class="tab selected" if idx==selected else "tab")
            if main._tabs: self+=main._tabs[selected]
    #-:-:-:-:-:-:-:-:-:-:-:-:-:-:-:-:-:-:-:-:-:-:-:-:-:-:-:-:-:-:-:-:-:-:-:

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
            self( Tabs.Show, self._selected )
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
