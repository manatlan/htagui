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
from ..common import ensuredict,ListOrDict,autoclosemenu

STATICS="""

html,body {
    width:100%;
    font-family: ubuntu, 'Helvetica';
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
    font-family: ubuntu, 'Helvetica';
}

.button:hover {
    filter: brightness(0.95);
}

.input[type="text"],.input[type="search"],.input[type="password"] {
    font-family: ubuntu,'Helvetica';
    font-size: 1em;
    padding:6px;
    border-radius: 4px;
    border: 2px solid #EEE;
    width: calc(100% - 16px);
}
.input:focus {
    outline: none;
    border: 2px solid #0075ff !important;
}


.textarea {
    font-family: ubuntu,'Helvetica';
    font-size: 1em;
    padding:6px;
    border-radius: 4px;
    border: 2px solid #EEE;
    width: calc(100% - 16px);
}
.textarea:focus {
    outline: none;
    border: 2px solid #0075ff !important;
}

.select {
    padding:4px;
    border-radius: 4px;
    border: 2px solid #EEE;
    font-family: ubuntu,'Helvetica';
}

.select:focus {
    border: 2px solid #0075ff !important;
}

.menu {}
.menu > div {
    padding:8px;
    cursor:pointer;
    background:Canvas;
}
.menu > div:hover {
    filter: brightness(0.95);
}


.tab {
    border:0px;
    cursor:pointer;
    margin:2px;
    background:Canvas;
    padding:8px;
    font-family: ubuntu,'Helvetica';
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

class VoileTransparent(Tag.div):
    def init(self,**a):
        self["style"].set("position","fixed")
        self["style"].set("top","0px")
        self["style"].set("bottom","0px")
        self["style"].set("right","0px")
        self["style"].set("left","0px")
        self["style"].set("z-index","2000")


class Button(Tag.button):
    statics=STATICS
    def init(self,title,**a):
        self <= title
        self["class"].add("button")

class Spinner(Tag.span):
    statics=STATICS
    def init(self,**a):
        self["class"].add("spinner")

class Input(Tag.input):
    statics=STATICS
    def init(self,**a):
        self["class"].add("input")
        if not self.attrs.get("type"):
            self["type"]="text"
        self["placeholder"] = self.attrs.get("label")

class Textarea(Tag.textarea):
    statics=STATICS
    def init(self,txt:str, **a):
        self["class"].add("textarea")
        self <= txt

        self["placeholder"] = self.attrs.get("label")

class Select(Tag.select):
    statics=STATICS
    def init(self,options:ListOrDict, **a):
        self.options=ensuredict(options)
        self.rerender( self.attrs.get("value") )
        self["class"].add("select")

    def rerender(self,value):
        """ special method (see ifields), to rerender all the widget (to avoid to deal with js)"""
        self.clear()
        for k,v in self.options.items():
            self <= Tag.option(v,_value=k,_selected=(str(value)==str(k)))


class Radios(Tag.span):
    def init(self,options:ListOrDict, **a):
        self.options = ensuredict(options)
        self.rerender( self.attrs.get("value",None) )

    def rerender(self,value):
        """ special method (see ifields), to rerender all the widget (to avoid to deal with js)"""
        self.clear()
        for k,v in self.options.items():
            ipt=Tag.input(
                _type="radio",
                _value=k,
                _name=self.attrs.get("name",str(id(self))),             # need a name to be valid
                _checked=(str(value)==str(k)),
                _required=bool(self.attrs.get("required",None)),
                _readonly=bool(self.attrs.get("readonly",None)),
                _onchange=f"document.getElementById('{id(self)}').value='{k}';"
            )
            self <= Tag.div(Tag.label( ipt +" "+ v ))

# class SelectButtons(Tag.span):
#     statics="""
#     .selectbuttons button {
#         border:1px solid #CCC;
#         padding:10px;
#         background:white;
#         cursor:pointer;
#     }
#     .selectbuttons button:first-child {
#         border-radius: 8px 0 0 8px;
#     }
#     .selectbuttons button:nth-last-child(2) {
#         border-radius: 0 8px 8px 0;
#     }
#     .selectbuttons button.selected {
#         background:green;
#         color:white;
#     }
#     .selectbuttons .hidden {
#         opacity: 0;
#         height: 1px;
#         width: 1px;
#    }    
    
#     """,b"""
    
#     function select(obj,value) {
#         let o=obj.parentNode.querySelector("button.selected");
#         if(o) o.classList.remove("selected");

#         obj.parentNode.childNodes[obj.parentNode.childNodes.length-1].value=value;
#         obj.classList.add("selected");
#     }
#     """
#     def init(self,options:ListOrDict, **a):
#         options = ensuredict(options)
#         self["class"].add("selectbuttons")
        
#         for k,v in options.items():
#             ipt=Tag.button(
#                 v,
#                 _type="button",
#                 value=k,
#                 _class="selected" if str(self.attrs.get("value",None))==str(k) else "",
#             )
#             ipt["onclick"] = f"select( document.getElementById('{id(ipt)}'), '{k}')"
#             self <= ipt

#         self<=Tag.input(
#             _type="text",
#             _value=self.attrs.get("value"),
#             _name=self.attrs.get("name"),
#             _required=self.attrs.get("required"),
#             #~ _readonly=self.attrs.get("readonly"),
#             _class="hidden",
#         )




class Menu(Tag.div):
    statics=STATICS
    def init(self,entries:dict):
        self["class"].add("menu")
        def call(ev):
            autoclosemenu( self.parent)

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

class PopPage(Tag.div):
    def init(self,metatag,obj):
        self["style"].set("position","fixed")
        self["style"].set("top","0px")
        self["style"].set("bottom","0px")
        self["style"].set("right","0px")
        self["style"].set("left","0px")
        self["style"].set("z-index","500")
        self["style"].set("background","Canvas")
        self <= obj


class ModalAlert(ModalBlock):
    def __init__(self,metatag,obj,wsize:float=None):
        if wsize is None: wsize=0.6
        pwidth=f"{int(wsize*100)}%"
        bc = Tag.button("X",_onclick=metatag.stepevent(),_style="float:right;border-radius:50%;border:0px;cursor:pointer;background:Canvas")
        box = Tag.div( [bc,obj],_style=f"width:{pwidth};max-height:80%;background:Canvas;overflow-y: auto;border-radius:6px;box-shadow: rgba(0, 0, 0, 0.35) 0px 5px 15px;padding:10px",_onmousedown="event.stopPropagation();")
        ModalBlock.__init__(self,metatag,box)
        self.childs[1]["onmousedown"]=metatag.stepevent()


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
        self <= Tag.div( obj ,_style=f"position:fixed;top:{t};bottom:{b};left:{l};right:{r};background:Canvas;border-radius:0px;box-shadow: rgba(0, 0, 0, 0.35) 0px 5px 15px;;z-index:1001;padding:10px")

class Pop(Tag.div):
    def init(self,metatag,obj,xy:tuple):
        x,y=xy
        self <= VoileTransparent(_onmousedown=metatag.bind.popclose(),_oncontextmenu="event.stopPropagation();return false")

        js="""(function(tag,x,y) {
            tag.style="position:fixed;z-index:2001;padding:2px;left:"+x+"px;top:"+y+"px";
            let bw=window.innerWidth;
            let bh=window.innerHeight;
            let w=tag.clientWidth;
            let h=tag.clientHeight;
            if(x+w > bw) x=bw-w;
            if(y+h > bh) y=bh-h;
            tag.style="position:fixed;z-index:2001;padding:2px;left:"+x+"px;top:"+y+"px";
        })(self,%s,%s)""" % (x,y)

        self <= Tag.div( obj ,js=js)


class Toast(Tag.div):
    def init(self,main_non_used,obj,timeout=1000):
        self <= Tag.div(obj,_style="position:fixed;right:10px;bottom:10px;z-index:1001;background:Canvas;padding:10px;border:2px solid black;border-radius:10px;min-width:200px")
        self.js="setTimeout( function() {self.remove()} , %s)" % timeout

######################################################################################



class Tabs(Tag.div):
    def init(self,metatag,selected=0):
        for idx,i in enumerate(metatag._tabs):
            name = hasattr(i,"name") and i.name or "?(name)?"
            self+=Tag.button(name, _onclick = metatag.stepevent(select=idx), _class="tab selected" if idx==selected else "tab")
        if metatag._tabs: self+=metatag._tabs[selected]

