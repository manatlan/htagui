# -*- coding: utf-8 -*-
# #############################################################################
# Copyright (C) 2024 manatlan manatlan[at]gmail(dot)com
#
# MIT licence
#
# https://github.com/manatlan/htag
# #############################################################################
import os,sys,re


class StepRules: # DEPRECATED
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


class TagStep: # THE FUTUR
    """ 
        Inherit Special features to create an htag class which will act
        as a "state machine" (ability to render different form, and
        evolve its state with step() interactions)
    """
    def init(self):
        """ default constructor """
        self._current=None
        self.step()  # start
    
    def render(self):
        """ render current component in a dynamic way 
            (render is a specific method of htag.Tag, to be dynamic)
        """
        self.clear()
        self <= self._current

    def __call__(self, klass,*a,**k ):
        """ set the current class abstraction """
        self._current = klass(self,*a,**k)
    
    def stepevent(self,**params):
        """ return a caller object (for js interaction with self.step) """
        return self.bind( self.step, **params)

    def step(self,**params):
        """ TO OVERRIDE (should contain the rules/bpm)"""
        pass

class Selector(Tag.div,TagStep):
    " an example of use ^^ "
    #-:-:-:-:-:-:-:-:-:-:-:-:-:-:-:-:-:-:-:-:-:-:-:-:-:-:-:-:-:-:-:-:
    class Choose(Tag.div):
        def init(self,main):
            " all the ui logic goes here "
            for i in main.all:
                self <= Tag.button(i, _onclick = main.stepevent(select=i),_style="background:white;cursor:pointer;border:1px dotted #CCC")
    class Current(Tag.div):
        def init(self,main,val):
            " all the ui logic goes here "
            self <= Tag.button( val , _onclick = main.stepevent(select="?"))
    #-:-:-:-:-:-:-:-:-:-:-:-:-:-:-:-:-:-:-:-:-:-:-:-:-:-:-:-:-:-:-:-:

    def init(self,selected,all):
        " ex of surcharge on the default constructor "
        self.selected=selected
        self.all=all
        TagStep.init(self)

    def step(self,**params):
        " all the functionnal logic goes here "
        select=params.get("select")
        if select is None:
            self( Selector.Current, self.selected )
        elif select == "?":    
            self( Selector.Choose )
        else:
            self.selected=select
            self( Selector.Current, self.selected )


if __name__=="__main__":
    from htag import Tag

    class Empty(Tag.div,TagStep):
        #-:-:-:-:-:-:-:-:-:-:-:-:-:-:-:-:-:-:-:-:-:-:-:-:-:-:-:-:-:-:-:-:-:-:-:
        class Empty(Tag.div):
            def init(self,main):
                self <= "empty content"
        #-:-:-:-:-:-:-:-:-:-:-:-:-:-:-:-:-:-:-:-:-:-:-:-:-:-:-:-:-:-:-:-:-:-:-:

        def step(self,**params):
            self(Empty.Empty)
