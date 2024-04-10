# -*- coding: utf-8 -*-
# #############################################################################
# Copyright (C) 2024 manatlan manatlan[at]gmail(dot)com
#
# MIT licence
#
# https://github.com/manatlan/htag
# #############################################################################
import os,sys,re


class StepRules:
    def init(self):
        self._current=None
        self.rules()  # start
    
    def render(self):
        self.clear()
        self <= self._current

    def go(self, klass,*a,**k ):
        self._current = klass(self,*a,**k)
    
    def stepevent(self,**data):
        return self.bind( self.step, **data)

    def step(self,**k):
        self.rules(**k)

if __name__=="__main__":
    from htag import Tag

    class Empty(Tag.div,StepRules):
        #-:-:-:-:-:-:-:-:-:-:-:-:-:-:-:-:-:-:-:-:-:-:-:-:-:-:-:-:-:-:-:-:-:-:-:
        class Empty(Tag.div):
            def init(self,main):
                self <= "ui"
        #-:-:-:-:-:-:-:-:-:-:-:-:-:-:-:-:-:-:-:-:-:-:-:-:-:-:-:-:-:-:-:-:-:-:-:

        def rules(self,**params):
            self.go(Empty.Empty)
