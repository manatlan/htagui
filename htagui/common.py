# -*- coding: utf-8 -*-
# #############################################################################
# Copyright (C) 2024 manatlan manatlan[at]gmail(dot)com
#
# MIT licence
#
# https://github.com/manatlan/htag
# #############################################################################
import os,sys,re

class TagStep: # (could be in htag soon)
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
        self.clear( self._current )

    def __call__(self, klass,*a,**k ):
        """ set the current class abstraction """
        self._current = klass(self,*a,**k)
    
    def stepevent(self,**params):
        """ return a caller object (for js interaction with self.step) """
        return self.bind( self.step, **params)

    def step(self,**params):
        """ TO OVERRIDE (should contain the rules/bpm)"""
        pass


# import types,asyncio

# async def caller( cb, *a, **k):
#     if asyncio.iscoroutinefunction(cb):
#         r=await cb(*a,**k)
#     else:                
#         r=cb(*a,**k)
#     if isinstance(r, types.GeneratorType):
#         for i in r:
#             yield i
#         # yield from r
#     elif isinstance(r, types.AsyncGeneratorType):
#         async for i in r:
#             yield i
#     else:
#         assert r is None

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

    

    class App(Tag.div):
        def init(self):
            self <= Selector("A",list("ABCDEF"))
            self <= Selector("1",list("123"))
            self <= Empty()
    
    from htag.runners import Runner
    Runner(App).run()