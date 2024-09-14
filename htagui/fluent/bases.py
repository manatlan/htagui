# -*- coding: utf-8 -*-
# #############################################################################
# Copyright (C) 2024 manatlan manatlan[at]gmail(dot)com
#
# MIT licence
#
# https://github.com/manatlan/htag
# #############################################################################
# -*- coding: utf-8 -*-

from htag import Tag,expose
from ..form import Form
from ..common import ensuredict,ListOrDict,autoclosemenu

STATICS = [
        Tag.script(_type="module",_src="https://unpkg.com/@fluentui/web-components"),
        Tag.style("""
:not(:defined) {
  visibility: hidden;
}

* {
    font-family: ubuntu;
}

                  
.tab {
    border:0px;
    cursor:pointer;
    margin:2px;
    background:Canvas;
    padding:8px;
    font-family: ubuntu;
}
.tab.selected {
    color:#0075ff;
    border-bottom: 1px solid #0075ff;
}
"""),
]

class Input(Tag.input):
    statics= STATICS
    def init(self,*a,**k):
        type=self.attrs.get("type") or "text"
        if type in ["text","search","password"]:
            self.tag = "fluent-text-field"
            self["type"]=type
        elif type=="checkbox":
            self.tag = "fluent-switch"
        elif type=="radio":
            self.tag = "fluent-radio"
        elif type=="range":
            self.tag = "fluent-slider"

        self["placeholder"] = self.attrs.get("label")

class Textarea(Tag.fluent_text_area):
    statics=STATICS
    def init(self,txt:str,**a):
        self["value"]=txt

class Button(Tag.fluent_button):
    statics= STATICS
    def init(self,title,**a):
        self <= title
        if not self.attrs.get("type"):
            self["type"]="submit"

class Voile(Tag.div):
    def init(self,**a):
        self["style"].set("position","fixed")
        self["style"].set("top","0px")
        self["style"].set("bottom","0px")
        self["style"].set("right","0px")
        self["style"].set("left","0px")
        self["style"].set("z-index","1000")
        self["style"].set("background","#CCC")
        self["style"].set("opacity","0.5")

class VoileTransparent(Tag.div):
    def init(self,**a):
        self["style"].set("position","fixed")
        self["style"].set("top","0px")
        self["style"].set("bottom","0px")
        self["style"].set("right","0px")
        self["style"].set("left","0px")
        self["style"].set("z-index","2000")


class Menu(Tag.fluent_menu):
    statics=STATICS
    def init(self,entries:dict):
        def call(ev):
            autoclosemenu( self.parent)

            return ev.target.method()

        for k,v in entries.items():
            self += Tag.fluent_menu_item(k,method=v,_onclick=call)




class Spinner(Tag.fluent_progress_ring):
    statics=STATICS
    def init(self,**a):
        pass

class Select(Tag.fluent_select):
    statics=STATICS
    def init(self,options:ListOrDict, **a):
        options = ensuredict(options)
        self["class"].add("select")
        for k,v in options.items():
            self <= Tag.fluent_option(v,_value=k,_selected=(str(self.attrs["value"])==str(k)))

class Radios(Tag.fluent_radio_group):
    statics=STATICS
    def init(self,options:ListOrDict, **a):
        options = ensuredict(options)
        for k,v in options.items():
            self <= Tag.fluent_radio(v,_value=k)


######################################################################################
## Dialog objects
######################################################################################
class Empty(Tag.div):
    def init(self,metatag):
        self.clear()

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


class ModalAlert(Tag.fluent_dialog):
    def init(self,metatag,obj,wsize:float=None):
        if wsize is not None:
            self["style"].set("--dialog-width",f"{int(wsize*100)}%")
        self["style"].set("--dialog-height","auto")
        bc = Tag.button("X",_onclick=metatag.stepevent(),_style="float:right;border-radius:50%;border:0px;cursor:pointer;background:Canvas")
        box = Tag.div( obj,_style=f"background:Canvas;overflow-y:auto;margin:10px;",_onmousedown="event.stopPropagation();")
        self <= bc+box
        
        #~ self.childs[1]["onmousedown"]=metatag.stepevent()

class ModalBlock(Tag.fluent_dialog):
    def init(self,metatag,obj):
        self["style"]="--dialog-width:auto;--dialog-height:auto"
        self <= obj

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
            setTimeout(function() {
                let bw=window.innerWidth;
                let bh=window.innerHeight;
                let w=tag.clientWidth;
                let h=tag.clientHeight;
                if(x+w > bw) x=bw-w;
                if(y+h > bh) y=bh-h;
                tag.style="position:fixed;z-index:2001;padding:2px;left:"+x+"px;top:"+y+"px";
            },0);
        })(self,%s,%s)""" % (x,y)

        self <= Tag.div( obj ,js=js)

class Toast(Tag.div):
    def init(self,main_non_used,obj,timeout=1000):
        self <= Tag.div(obj,_style="position:fixed;right:10px;bottom:10px;z-index:1001;background:Canvas;padding:10px;border:2px solid black;border-radius:10px;min-width:200px")
        self.js="setTimeout( function() {self.remove()} , %s)" % timeout

######################################################################################


# class Tabs(Tag.div):
#     def init(self,metatag,selected=0):
#         selTab=None
#         tabs=[]
#         for idx,i in enumerate(metatag._tabs):
#             name = hasattr(i,"name") and i.name or "?(name)?"
#             tab=Tag.fluent_tab(name, _onclick = metatag.stepevent(select=idx))
#             tabs.append( tab )
#             if idx==selected:
#                 selTab=tab

#         self <= Tag.fluent_tabs( tabs, _activeindicator=True, _activeid=id(selTab))
#         # self <= f"""<fluent-tab-panel id="{id(selTab)}Panel">"""
#         # self <= metatag._tabs[selected]
#         # self <= """</fluent-tab-panel>"""
#         for idx,i in enumerate(tabs):
#             self <= f"""<fluent-tab-panel id="{id(i)}Panel" hidden={selected!=idx}>"""
#             self <= metatag._tabs[idx]
#             self <= """</fluent-tab-panel>"""

class Tabs(Tag.div):
    def init(self,metatag,selected=0):
        for idx,i in enumerate(metatag._tabs):
            name = hasattr(i,"name") and i.name or "?(name)?"
            self+=Tag.button(name, _onclick = metatag.stepevent(select=idx), _class="tab selected" if idx==selected else "tab")
        if metatag._tabs: self+=metatag._tabs[selected]
