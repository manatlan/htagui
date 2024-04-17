# -*- coding: utf-8 -*-
# #############################################################################
# Copyright (C) 2024 manatlan manatlan[at]gmail(dot)com
#
# MIT licence
#
# https://github.com/manatlan/htag
# #############################################################################

from htag import Tag
from ..form import Form

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


.textarea {
    padding:4px;
    border-radius: 4px;
    border: 2px solid #EEE;
}
.textarea:focus {
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


class Textarea(Tag.textarea):
    statics=CSS
    def init(self,txt:str, **a):
        self["class"].add("textarea")
        self <= txt

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

            return ev.target.method()

        for k,v in entries.items():
            self += Tag.div(k,method=v,_onclick=call)

######################################################################################
## Dialog objects
######################################################################################
class Empty(Tag.div):
    def init(self,metatag):
        self.clear()


class ModalBlock(Tag.div):
    def init(self,metatag,obj):
        modal=Tag.div( obj, _style="position:fixed;left:0px;right:0px;top:0px;bottom:0px;z-index:1001;    display:flex;align-items:center;justify-content:center;")
        self <= Voile() + modal

class ModalAlert(ModalBlock):
    def __init__(self,metatag,obj,pwidth="60%",pheight=None):
        bc = Tag.button("X",_onclick=metatag.stepevent(),_style="float:right;border-radius:50%;border:0px;cursor:pointer;background:white")
        box = Tag.div( [bc,obj],_style=f"width:{pwidth};background:white;overflow-y: auto;background:white;border-radius:6px;box-shadow: rgba(0, 0, 0, 0.35) 0px 5px 15px;padding:10px",_onmousedown="event.stopPropagation();")
        if pheight:
            box["style"].set("height",pheight)
        else:
            box["style"].set("max-height","80%")
                
        ModalBlock.__init__(self,metatag,box)
        self.childs[1]["onmousedown"]=metatag.stepevent()

class ModalBox(ModalAlert):
    def __init__(self,metatag,obj,size:float=.6):
        ModalAlert.__init__(self,metatag,obj,pwidth=f"{size*100}%",pheight=f"{size*100}%")

class ModalConfirm(ModalAlert):
    def __init__(self,metatag,obj,cb):
        def call(ev):
            metatag.step()
            return cb( ev.target.val )
         
        box=[ 
            Tag.div(obj),
            Button("Yes",val=True,_onclick=call),
            Button("No",val=False,_onclick=call),
        ]
        ModalAlert.__init__(self,metatag,box)

class ModalPrompt(ModalAlert):
    def __init__(self,metatag, value,title,cb):
        def call(dico):
            metatag.step()
            return cb( dico["promptvalue"] )
        with Form(onsubmit=call) as f:
            f+=Tag.div( title )
            f+=Tag.div( Input(_value=value,_name="promptvalue",js="self.focus();self.select()", _autofocus=True) ,_style="padding:4px 0")
            f+=Button("Ok" )
            f+=Button("Cancel",_type="button",_onclick=metatag.stepevent())
        ModalAlert.__init__(self,metatag,f)

class Drawer(Tag.div):
    def init(self,metatag,obj,mode:str):
        size=50
        if mode=="left":
            t,r,b,l= ("0px",f"{size}%","0px","0px")
        elif mode=="right":
            t,r,b,l= ("0px","0px","0px",f"{size}%")
        elif mode=="bottom":
            t,r,b,l=(f"{size}%","0px","0px","0px")
        elif mode=="top":
            t,r,b,l= ("0px","0px",f"{size}%","0px")

        self <= Voile(_onmousedown=metatag.stepevent())
        self <= Tag.div( obj ,_style=f"position:fixed;top:{t};bottom:{b};left:{l};right:{r};background:white;border-radius:0px;box-shadow: rgba(0, 0, 0, 0.35) 0px 5px 15px;;z-index:1001;padding:10px")

class Pop(Tag.div):
    def init(self,metatag,obj,xy:tuple):
        x,y=xy
        self <= Voile(_onmousedown=metatag.stepevent())
        self <= Tag.div( obj ,_style=f"position:fixed;top:{y}px;left:{x}px;z-index:1001;background:white")

class Toast(Tag.div):
    def init(self,main_non_used,obj,timeout=1000):
        self <= Tag.div(obj,_style="position:fixed;right:10px;bottom:10px;z-index:1001;background:white;padding:10px;border:2px solid black")
        self.js="setTimeout( function() {self.remove()} , %s)" % timeout

######################################################################################



class Tabs(Tag.div):
    def init(self,metatag,selected=0):
        for idx,i in enumerate(metatag._tabs):
            name = hasattr(i,"name") and i.name or "?(name)?"
            self+=Tag.button(name, _onclick = metatag.stepevent(select=idx), _class="tab selected" if idx==selected else "tab")
        if metatag._tabs: self+=metatag._tabs[selected]

