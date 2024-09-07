# -*- coding: utf-8 -*-
# #############################################################################
# Copyright (C) 2024 manatlan manatlan[at]gmail(dot)com
#
# MIT licence
#
# https://github.com/manatlan/htag
# #############################################################################

from htag import Tag,expose

from typing import Callable, List

creators= List[Callable[[], Tag]]


class VScroll(Tag.div):
    def init(self,cbloader:Callable[[], Tag],endzone:int=50,**a):
        """
        the CONTAINER/PARENT should have a "height" !
        
        cbloader:   generator
        endzone:    nb of pixels before the end to do the more load
        """
        self.cbloader=cbloader
        self.js = """
        self.style.height="100%%";      // !important
        self.style.overflowY="auto";    // !important
        self.scroller = function(e) {
            if (self.scrollHeight - self.offsetHeight - %s <= self.scrollTop)
                self._loadmore();
        }
        self.addEventListener( 'scroll', self.scroller, false)
        
        """ % (endzone)

        for i in self.cbloader():
            self <= i

    
    @expose
    def _loadmore(self):
        for i in self.cbloader():
            if i:
                yield i
            else:
                self.call('self.removeEventListener( "scroll", self.scroller )')
                break


class VScrollPager(VScroll):
    def __init__(self,all:creators,preload:int=50,moreload:int=10,endzone:int=50,**a):
        """
        the CONTAINER/PARENT should have a "height" !
        
        all:        list of constructor()
        preload:    nb of items to preload at start (should overflow the height!)
        moreload:   nb of items to load more when scroll is a the end
        endzone:    nb of pixels before the end to do the more load
        """
        
        self.first=True
        self.all=all
        self.preload=preload
        self.moreload=moreload
        VScroll.__init__(self,self._more)
        
    
    def _more(self):
        if self.all:
            for i in range(0,self.preload if self.first else self.moreload):
                if len(self.all)>0:
                    yield self.all.pop(0)()
        else:
            yield None # force removing event onscroll !
        self.first=False


class O(Tag.div):
    def init(self,x):
        self <= x
        self["style"]="display:inline-block;width:100px;height:100px;border:1px solid black"
    
    
class App(Tag.div):
    imports=[]
    statics=""" html,body {height:100%;overflow:hidden} """ # NEEDED !
    
    def init(self):
        with Tag.div(_style="display:flex;flow-flow: row nowrap;height:100%") as d:
            def feed():
                yield [O(i) for i in range(50) ]
            
            # unlimited scrolling
            d <= VScroll( feed,_style="flex: 0 0 50%" )
            
            # scrolling on demand in a defined list (of lambda())
            d <= Tag.div( Tag.button("hello") + VScrollPager([lambda i=i: O(i) for i in range(1000,1200)]) ,_style="height:100%")
        self += d

if __name__=="__main__":
    from htag import Runner
    Runner(App,interface=(800,600)).run()
