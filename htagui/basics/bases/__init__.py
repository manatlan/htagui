# -*- coding: utf-8 -*-
# #############################################################################
# Copyright (C) 2024 manatlan manatlan[at]gmail(dot)com
#
# MIT licence
#
# https://github.com/manatlan/htag
# #############################################################################

from htag import Tag
from ...form import Form
from ...common import caller

CSS="""
html,body {
    width:100%;
    font-family: ubuntu;
    padding:0px;
    margin:0px;
}

a {color: #0075ff;text-decoration:none}

.button {
    border:1px solid #DDD;
    border-radius:6px;
    padding:10px;
    margin:1px;
    cursor:pointer;
    font-family: ubuntu;
}

.button.red {
    background: #F77;
    color:white;
}

.button.green {
    background: #7C7;
    color:white;
}

.button.blue {
    background: #77F;
    color:white;
}

.button:hover {
    filter: brightness(0.95);
}

.input {
    padding:4px;
    border-radius: 4px;
    border: 2px solid #EEE;
}
.input:focus {
    outline: none;
    border: 2px solid #0075ff !important;
}

.select {
    font-family: ubuntu;
}

.menu {}
.menu > div {
    padding:8px;
    cursor:pointer;
    background:white;
}
.menu > div:hover {
    filter: brightness(0.95);
}


.tab {
    border:0px;
    cursor:pointer;
    margin:2px;
    background:white;
    padding:8px;
    font-family: ubuntu;
}
.tab.selected {
    color:#0075ff;
    border-bottom: 1px solid #0075ff;
}


.spinner {
    width: 32px;
    height: 32px;
    border: 8px solid #0075ff;
    border-bottom-color: transparent;
    border-radius: 50%;
    display: inline-block;
    box-sizing: border-box;
    animation: rotation 1s linear infinite;
    }

    @keyframes rotation {
    0% {
        transform: rotate(0deg);
    }
    100% {
        transform: rotate(360deg);
    }
}        
"""

class Voile(Tag.div):
    def init(self,**a):
        self["style"].set("position","fixed")
        self["style"].set("top","0px")
        self["style"].set("bottom","0px")
        self["style"].set("right","0px")
        self["style"].set("left","0px")
        self["style"].set("z-index","1000")
        self["style"].set("background","rgb(200,200,200,0.5)")
        self["style"].set("backdrop-filter","blur(3px)")

class Button(Tag.button):
    statics=CSS
    def init(self,title,**a):
        self <= title
        self["class"].add("button")

class Spinner(Tag.span):
    statics=CSS
    def init(self):
        self["class"].add("spinner")

class Input(Tag.input):
    statics=CSS
    def init(self,**a):
        self["class"].add("input")

class Select(Tag.select):
    statics=CSS
    def init(self,options:dict, **a):
        assert isinstance(options,dict)
        self["class"].add("select")
        default = a.get("_value")
        for k,v in options.items():
            self <= Tag.option(v,_value=k,_selected=(default==k))

class Menu(Tag.div):
    statics=CSS
    def init(self,entries:dict):
        self["class"].add("menu")
        def call(ev):
            #auto close the ui.Dialog, if this "Menu" is in a Dialog interaction
            #------------------------------------------------------------------------
            current = self.parent
            while current is not None:
                if repr(current).startswith("<Dialog'div"): #TODO: not top (can do better)
                    current.close()
                    break
                current = current.parent
            #------------------------------------------------------------------------

            return caller( ev.target.method )

        for k,v in entries.items():
            self += Tag.div(k,method=v,_onclick=call)

######################################################################################
## Dialog objects
######################################################################################
class Empty(Tag.div):
    def init(self,main):
        self.clear()
        
class Modal(Tag.div):
    def init(self,main,obj,trbl:tuple=("30%","30%","","30%"),closable=True,radius=6):
        t,r,b,l = trbl
        if closable:
            bc=Tag.button("X",_onclick=main.stepevent(),_style="position:absolute;top:2px;right:2px;z-index:1002;border-radius:50%;border:0px;cursor:pointer;background:white")
            self <= Voile(_onmousedown=main.stepevent())
            self <= Tag.div( [bc,obj] ,_style=f"position:fixed;top:{t};bottom:{b};left:{l};right:{r};background:white;border-radius:{radius}px;box-shadow: rgba(0, 0, 0, 0.35) 0px 5px 15px;;z-index:1001;padding:10px")
        else:
            self <= Voile(_style="cursor:not-allowed;")
            self <= Tag.div( obj ,_style=f"position:fixed;top:{t};right:{r};z-index:1001;transform:translate(50%,-50%);")

Drawer = Modal

class ModalConfirm(Modal):
    def __init__(self,main,obj,cb):
        def call(ev):
            main.step()
            return caller( cb, ev.target.val)
         
        box=[ 
            Tag.div(obj),
            Button("Yes",val=True,_onclick=call),
            Button("No",val=False,_onclick=call),
        ]
        Modal.__init__(self,main,box)

class ModalPrompt(Modal):
    def __init__(self,main, value,title,cb):
        def call(dico):
            main.step()
            return caller( cb, dico["promptvalue"])
        with Form(onsubmit=call) as f:
            f+=Tag.div( title )
            f+=Tag.div( Input(_value=value,_name="promptvalue",js="self.focus();self.select()", _autofocus=True) ,_style="padding:4px 0")
            f+=Button("Ok" )
            f+=Button("Cancel",_type="button",_onclick=main.stepevent())
        Modal.__init__(self,main,f)

class Pop(Tag.div):
    def init(self,main,obj,xy:tuple):
        x,y=xy
        self <= Voile(_onmousedown=main.stepevent())
        self <= Tag.div( obj ,_style=f"position:fixed;top:{y}px;left:{x}px;z-index:1001;background:white")

class Toast(Tag.div):
    def init(self,main_non_used,obj,timeout=1000):
        self <= Tag.div(obj,_style="position:fixed;right:10px;bottom:10px;z-index:1001;background:white;padding:10px;border:2px solid black")
        self.js="setTimeout( function() {self.remove()} , %s)" % timeout

######################################################################################



class Tabs(Tag.div):
    def init(self,main,selected=0):
        for idx,i in enumerate(main._tabs):
            name = hasattr(i,"name") and i.name or "?(name)?"
            self+=Tag.button(name, _onclick = main.stepevent(select=idx), _class="tab selected" if idx==selected else "tab")
        if main._tabs: self+=main._tabs[selected]

