# -*- coding: utf-8 -*-
# #############################################################################
# Copyright (C) 2024 manatlan manatlan[at]gmail(dot)com
#
# MIT licence
#
# https://github.com/manatlan/htag
# #############################################################################
from htag import Tag,expose
from .common import MetaTag

import importlib,__main__
print(f"IMPORT [{__main__.htaguimodule}]")
cui = importlib.import_module(__main__.htaguimodule)

class Dialog(Tag.div,MetaTag):
    imports=[cui.Voile,cui.Button,cui.Input]

    def init(self,parent):
        self["info"]="UI.current object"
        self._toasts = Tag.div(_info="UI.toasts objects")
        self._previous=None
        parent += self  # auto add
        parent += self._toasts  # add a personnal place for toasts
        MetaTag.init(self)

    def clipboard_copy(self,txt:str):
        self.call(f"""
let ta = document.createElement('textarea');
ta.value = `{txt}`;
self.appendChild(ta);
ta.select();
document.execCommand('copy');
self.removeChild(ta);
""")

    def alert(self,obj):
        self.step( alert = obj )

    def box(self,obj,size:float=0.5):
        self.step( box = obj, size=size )
        
    def confirm(self,obj,cbresponse=lambda bool:bool):
        self.step( confirm = obj, cb=cbresponse )
        
    def prompt(self,value:str,title,cbresponse=lambda val:val):
        self.step( prompt = value, title=title, cb=cbresponse )

    def notify(self,obj,time=2000):
        self.step( toast = obj, time=time )

    def pop(self, obj, xy:tuple):
        self.step( pop = obj, xy=xy )

    def drawer(self, obj, mode="left"):
        assert mode in ["left","right","bottom","top"]
        self.step( drawer = obj, mode=mode )

    def block(self,obj=None):
        self.step( block=obj )

    def close(self):
        self.step()

    def previous(self): # just the previous one (no history yet)
        if self._previous is None:
            self.close()
        else:
            self._current = self._previous
            self._previous = None

    def step(self,**params):

        def set(*a,**k):
            self._previous = self._current
            self(*a,**k)

        if "block" in params:
            set( cui.ModalBlock, params["block"] )
        elif "alert" in params:
            set( cui.ModalAlert, params["alert"] )
        elif "confirm" in params:
            set( cui.ModalConfirm, params["confirm"], params["cb"] )
        elif "prompt" in params:
            set( cui.ModalPrompt, params["prompt"],params["title"], params["cb"] )
        elif "box" in params: # NEW
            size=params["size"]
            set( cui.ModalBox, params["box"], size )
        elif "pop" in params:
            set( cui.Pop, params["pop"],params["xy"] )
        elif "drawer" in params:
            self( cui.Drawer, params["drawer"], params["mode"] )
        elif "toast" in params:
            self._toasts.clear( cui.Toast( self, params["toast"], params["time"] ))
        else:
            set( cui.Empty )


    
