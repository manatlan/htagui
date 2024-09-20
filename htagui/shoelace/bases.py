# -*- coding: utf-8 -*-
# #############################################################################
# Copyright (C) 2024 manatlan manatlan[at]gmail(dot)com
#
# MIT licence
#
# https://github.com/manatlan/htag
# #############################################################################

from htag import Tag,expose
from ..form import Form
from ..common import ensuredict,ListOrDict,autoclosemenu

STATICS = [
        Tag.link(_rel="stylesheet",_href="https://cdn.jsdelivr.net/npm/@shoelace-style/shoelace@2.16.0/cdn/themes/dark.css" ),
        Tag.link(_rel="stylesheet",_href="https://cdn.jsdelivr.net/npm/@shoelace-style/shoelace@2.16.0/cdn/themes/light.css" ),
        Tag.script(_type="module",_src="https://cdn.jsdelivr.net/npm/@shoelace-style/shoelace@2.16.0/cdn/shoelace-autoloader.js"),
        Tag.style("""
:not(:defined) {
  visibility: hidden;
}

.sl-toast-stack {
  display: flex;
  flex-direction: column-reverse;
  top: auto;
  bottom: 0;
  right: 0;
}

* {
    font-family: sans-serif;
}
"""),
]


class Input(Tag.input):
    statics= STATICS
    def init(self,*a,**k):
        type=self.attrs.get("type") or "text"
        if type in ["text","search","password"]:
            self.tag = "sl-input"
            self["type"]=type
        elif type=="checkbox":
            self.tag = "sl-switch"
            # self.tag = "sl-checkbox"
        elif type=="radio":
            self.tag = "sl-radio"
        elif type=="range":
            self.tag = "sl-range"

class Textarea(Tag.sl_textarea):
    statics=STATICS
    def init(self,txt:str,**a):
        self["value"]=txt

class Button(Tag.sl_button):
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


class Menu(Tag.sl_menu):
    statics= STATICS
    def __init__(self,entries:dict,**a):
        self._entries=entries
        Tag.__init__(self,**a)

        for idx,(k,v) in enumerate(entries.items()):
            self+=Tag.sl_menu_item(k,_value=idx)

        self.js="""
        self.addEventListener('sl-select', (e)=> {
            self._select(e.detail.item.value);
        });"""
        
    @expose
    def _select(self,idx):
        autoclosemenu( self.parent )
        return list(self._entries.values())[int(idx)]()



class Spinner(Tag.sl_spinner):
    statics=STATICS
    def init(self,**a):
        self["style"]="font-size: 32px; --track-width: 8px;"


class Select(Tag.sl_select):
    statics=STATICS
    def init(self,options:ListOrDict, **a):
        options = ensuredict(options)
        self["class"].add("select")
        for k,v in options.items():
            self <= Tag.sl_option(v,_value=k,_selected=(str(self.attrs["value"])==str(k)))

class Radios(Tag.sl_radio_group):
    statics=STATICS
    def init(self,options:ListOrDict, **a):
        options = ensuredict(options)
        for k,v in options.items():
            self <= Tag.sl_radio(v,_value=k)


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

class ModalAlert(Tag.sl_dialog):
    def init(self,metatag,obj,closable=True,wsize:float=None):
        if wsize is not None:
            pwidth=f"{int(wsize*100)}%"        
        else:
            pwidth=None

        self.metatag=metatag
        # self["open"]=True
        self["no-header"]=True
        if pwidth:
            self["style"] = f"--width: {pwidth};"
        self.js = "window.customElements.whenDefined('sl-dialog').then( function() { document.getElementById('%s').show() });" % id(self)
        self.js += """
        self.addEventListener('sl-after-hide', ()=> {
            %s;
        });""" % metatag.bind.step()
        if closable:
            bc=Tag.button("X",_onclick = self.close,_style="float:right;border-radius:50%;border:0px;cursor:pointer;background:Canvas")
            self <= [bc,obj]
        else:
            self <= obj
            self.js += "self.addEventListener( 'sl-request-close', function(ev) { ev.preventDefault() });"

    def close(self,ev=None):
        self.call( "try{self.hide()}catch(e){}")    # the self.hide crash in some cases ?!?


class ModalBlock(ModalAlert):
    def __init__(self,metatag,obj):
        ModalAlert.__init__(self,metatag,obj,closable=False)

class ModalConfirm(ModalAlert):
    def __init__(self,metatag,obj,cb):
        def call(ev):
            self.close()
            return cb(ev.target.val)
        box=[ 
            Tag.div(obj),
            Button("Yes",val=True,_onclick=call),
            Button("No",val=False,_onclick=call),
        ]
        ModalAlert.__init__(self,metatag,box)

class ModalPrompt(ModalAlert):
    def __init__(self,metatag, value,title,cb):
        def call(dico):
            self.close()
            return cb(dico["promptvalue"])
        with Form(onsubmit=call) as f:
            f+=Tag.div( title )
            f+=Tag.div( Input(_value=value,_name="promptvalue", _autofocus=True), _style="padding:4px 0" )
            # f+=Tag.div( Input(_value=value,_name="promptvalue",js="self.focus();self.select()", _autofocus=True) )
            f+=Button("Ok" ,_type="submit")
            f+=Button("Cancel",_type="button",_onclick=self.close)
        ModalAlert.__init__(self,metatag,f)


class Drawer(Tag.sl_drawer):
    def init(self,metatag,obj,mode:str):
        self["no-header"]=True
        if mode=="left":        self["placement"]="start"
        elif mode=="right":     self["placement"]="end"
        elif mode=="bottom":    self["placement"] = "bottom"
        elif mode=="top":       self["placement"] = "top"
        
        self <= obj
        self.js = "window.customElements.whenDefined('sl-drawer').then( function() { document.getElementById('%s').show() })" % id(self)



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
class Toast(Tag.sl_alert):
    def init(self,main_non_used,obj,timeout=1000):
        self["duration"]=timeout
        self <= obj
        self.js = "window.customElements.whenDefined('sl-alert').then( function() { document.getElementById('%s').toast() })" % id(self)
######################################################################################

class Tabs(Tag.sl_tab_group): #TODO: replace by https://shoelace.style/components/tab-group
    def init(self,metatag,selected=0):
        for idx,i in enumerate(metatag._tabs):
            name = hasattr(i,"name") and i.name or "?(name)?"
            self+=Tag.sl_tab(name, _slot="nav", _onclick = metatag.stepevent(select=idx), _active=(idx==selected))
        if metatag._tabs: self+=metatag._tabs[selected]
