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
from .form import Form
from .basics import Voile,Button,Input

class Dialog(Tag.div,TagStep):
    imports=[Voile,Button,Input]
    #-:-:-:-:-:-:-:-:-:-:-:-:-:-:-:-:-:-:-:-:-:-:-:-:-:-:-:-:-:-:-:-:-:-:-:
    class Empty(Tag.div):
        def init(self,main):
            self.clear()
            
    class Modal(Tag.div):
        def init(self,main,obj,trbl:tuple=("30%","30%","","30%"),closable=True,radius=6):
            t,r,b,l = trbl
            if closable:
                bc=Tag.button("X",_onclick=main.stepevent(),_style="float:right;border-radius:50%;border:0px;cursor:pointer;background:white")
                self <= Voile(_onmousedown=main.stepevent())
                self <= Tag.div( [bc,obj] ,_style=f"position:fixed;top:{t};bottom:{b};left:{l};right:{r};background:white;border-radius:{radius}px;box-shadow: rgba(0, 0, 0, 0.35) 0px 5px 15px;;z-index:1001;padding:10px")
            else:
                self <= Voile(_style="cursor:wait")
                self <= Tag.div( obj ,_style=f"position:fixed;top:{t};right:{r};z-index:1001;transform:translate(50%,50%);")

    class ModalConfirm(Modal):
        def __init__(self,main,obj,cb):
            def call(ev):
                cb(ev.target.val)
                main.step()
            box=[ 
                Tag.div(obj),
                Button("Yes",val=True,_onclick=call),
                Button("No",val=False,_onclick=call),
            ]
            Dialog.Modal.__init__(self,main,box)

    class ModalPrompt(Modal):
        def __init__(self,main, value,title,cb):
            def call(dico):
                cb(dico["promptvalue"])
                main.step()
            with Form(onsubmit=call) as f:
                f+=Tag.div( title )
                f+=Tag.div( Input(_value=value,_name="promptvalue",js="self.focus();self.setSelectionRange(0, self.value.length)") )
                f+=Button("Ok" )
                f+=Button("Cancel",_type="button",_onclick=main.stepevent())
            Dialog.Modal.__init__(self,main,f)

    class Pop(Tag.div):
        def init(self,main,obj,xy:tuple):
            x,y=xy
            self <= Voile(_onmousedown=main.stepevent())
            self <= Tag.div( obj ,_style=f"position:fixed;top:{y}px;left:{x}px;z-index:1001;background:white")

    class Toast(Tag.div):
        def init(self,main_non_used,obj,timeout=1000):
            self <= Tag.div(obj,_style="position:fixed;right:10px;bottom:10px;z-index:1001;background:white;padding:10px;border:2px solid black")
            self.js="setTimeout( function() {self.remove()} , %s)" % timeout
    #-:-:-:-:-:-:-:-:-:-:-:-:-:-:-:-:-:-:-:-:-:-:-:-:-:-:-:-:-:-:-:-:-:-:-:

    def init(self,parent):
        self["info"]="UI.current object"
        self._toasts = Tag.div(_info="UI.toasts objects")
        parent += self  # auto add
        parent += self._toasts  # add a personnal place for toasts
            
        TagStep.init(self)

    def alert(self,obj):
        self.step( alert = obj )
        
    def confirm(self,obj,cbresponse=lambda bool:bool):
        self.step( confirm = obj, cb=cbresponse )
        
    def prompt(self,value:str,title,cbresponse=lambda val:val):
        self.step( prompt = value, title=title, cb=cbresponse )

    def notify(self,obj,time=2000):
        self.step( toast = obj, time=time )

    def pop(self, obj, xy:tuple):
        self.step( pop = obj, xy=xy )

    def drawer(self, obj, mode="left", size:int=50):
        assert mode in ["left","right","bottom","top"]
        self.step( drawer = obj, mode=mode, size=100-size )

    def block(self,obj=None):
        self.step( block=obj )

    def close(self):
        self.step()

    def step(self,**params):
        if "alert" in params:
            self( Dialog.Modal, params["alert"] )
        elif "block" in params:
            self( Dialog.Modal, params["block"],("50%","50%","50%","50%"),closable=False )
        elif "confirm" in params:
            self( Dialog.ModalConfirm, params["confirm"], params["cb"] )
        elif "prompt" in params:
            self( Dialog.ModalPrompt, params["prompt"],params["title"], params["cb"] )
        elif "pop" in params:
            self( Dialog.Pop, params["pop"],params["xy"] )
        elif "drawer" in params:
            size=params["size"]
            if params["mode"]=="left":
                self( Dialog.Modal, params["drawer"], ("0px",f"{size}%","0px","0px"),radius=0 )
            elif params["mode"]=="right":
                self( Dialog.Modal, params["drawer"], ("0px","0px","0px",f"{size}%"),radius=0 )
            elif params["mode"]=="bottom":
                self( Dialog.Modal, params["drawer"], (f"{size}%","0px","0px","0px"),radius=0 )
            elif params["mode"]=="top":
                self( Dialog.Modal, params["drawer"], ("0px","0px",f"{size}%","0px"),radius=0 )
        elif "toast" in params:
            self._toasts.clear( Dialog.Toast( self, params["toast"], params["time"] ))
        else:
            self( Dialog.Empty )


    
