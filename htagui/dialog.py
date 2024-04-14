# -*- coding: utf-8 -*-
# #############################################################################
# Copyright (C) 2024 manatlan manatlan[at]gmail(dot)com
#
# MIT licence
#
# https://github.com/manatlan/htag
# #############################################################################
from htag import Tag,expose
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

class Dialog(Tag.div,TagStep):
    imports=[cui.Voile,cui.Button,cui.Input]

    def init(self,parent):
        self["info"]="UI.current object"
        self._toasts = Tag.div(_info="UI.toasts objects")
        self._previous=None
        parent += self  # auto add
        parent += self._toasts  # add a personnal place for toasts
        TagStep.init(self)

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
        self.step( box = obj, size=50 - size*50 )
        
    def confirm(self,obj,cbresponse=lambda bool:bool):
        self.step( confirm = obj, cb=cbresponse )
        
    def prompt(self,value:str,title,cbresponse=lambda val:val):
        self.step( prompt = value, title=title, cb=cbresponse )

    def notify(self,obj,time=2000):
        self.step( toast = obj, time=time )

    def pop(self, obj, xy:tuple):
        self.step( pop = obj, xy=xy )

    def drawer(self, obj, mode="left", size:float=0.5):
        assert mode in ["left","right","bottom","top"]
        self.step( drawer = obj, mode=mode, size=100 - 100*size )

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

        if "alert" in params:
            set( cui.Modal, params["alert"] )
        elif "box" in params:
            size=params["size"]
            set( cui.Modal, params["box"],(f"{size}%",f"{size}%",f"{size}%",f"{size}%") )
        elif "block" in params:
            set( cui.Modal, params["block"],("50%","50%","50%","50%"),closable=False )
        elif "confirm" in params:
            set( cui.ModalConfirm, params["confirm"], params["cb"] )
        elif "prompt" in params:
            set( cui.ModalPrompt, params["prompt"],params["title"], params["cb"] )
        elif "pop" in params:
            set( cui.Pop, params["pop"],params["xy"] )
        elif "drawer" in params:
            size=params["size"]
            if params["mode"]=="left":
                self( cui.Drawer, params["drawer"], ("0px",f"{size}%","0px","0px"),radius=0 )
            elif params["mode"]=="right":
                self( cui.Drawer, params["drawer"], ("0px","0px","0px",f"{size}%"),radius=0 )
            elif params["mode"]=="bottom":
                self( cui.Drawer, params["drawer"], (f"{size}%","0px","0px","0px"),radius=0 )
            elif params["mode"]=="top":
                self( cui.Drawer, params["drawer"], ("0px","0px",f"{size}%","0px"),radius=0 )
        elif "toast" in params:
            self._toasts.clear( cui.Toast( self, params["toast"], params["time"] ))
        else:
            set( cui.Empty )


    
