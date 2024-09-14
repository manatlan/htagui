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

# using https://material-web.dev/

STATICS = [
        Tag.style("""html,body {width:100%;height:100%}"""),
Tag.link(_href="https://fonts.googleapis.com/css2?family=Roboto:wght@400;500;700&display=swap", _rel="stylesheet"),
Tag.script("""    {
  "imports": {
    "@material/web/": "https://esm.run/@material/web/"
  }
}
""", _type="importmap"),
Tag.script("""
import '@material/web/all.js';
import {styles as typescaleStyles} from '@material/web/typography/md-typescale-styles.js';

document.adoptedStyleSheets.push(typescaleStyles.styleSheet);""",_type="module"),
Tag.style("""
:not(:defined) {
  visibility: hidden;
}
:root {
  --md-filled-tonal-button-container-shape: 8px;
  --md-dialog-container-shape: 8px;
}
"""),
    ]



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


class Button(Tag.md_filled_tonal_button):
    statics=STATICS
    def init(self,title,**a):
        self <= Tag.md_ripple() + title
        self["style"].set("margin","1px")

class Spinner(Tag.md_circular_progress):
    statics=STATICS
    def init(self,**a):
        self["indeterminate"]=True

class Input(Tag.input):
    statics= STATICS
    def init(self,*a,**k):
        type=self.attrs.get("type") or "text"
        if type in ["text","search","password"]:
            self.tag = "md-filled-text-field"
            self["style"].set("width","calc(100% - 16px)")
            self["type"]=type
        elif type=="checkbox":
            self.tag = "md-switch"
        elif type=="radio":
            self.tag = "md-radio"
        elif type=="range":
            self.tag = "md-slider"

class Textarea(Tag.md_filled_text_field):
    statics=STATICS
    def init(self,txt:str, **a):
        self["type"]="textarea"
        self["style"].set("width","calc(100% - 16px)")
        self.rerender( txt )

    def rerender(self,value):
        """ special method (see ifields), to rerender all the widget (to avoid to deal with js)"""
        self["value"]=value
        self.clear( value )


class Select(Tag.md_filled_select):
    statics=STATICS
    def init(self,options:ListOrDict, **a):
        options=ensuredict(options)
        default = a.get("_value")
        for k,v in options.items():
            self <= Tag.md_select_option(v,_value=k,_selected=(default==k))


class Radios(Tag.span):
    statics=STATICS
    def init(self,options:ListOrDict, **a):
        self.options = ensuredict(options)
        self.rerender( self.attrs.get("value",None) )

    def rerender(self,value):
        """ special method (see ifields), to rerender all the widget (to avoid to deal with js)"""
        self.clear()
        for k,v in self.options.items():
            ipt=Tag.md_radio(
                _value=k,
                _name=self.attrs.get("name",str(id(self))),             # need a name to be valid
                _checked=(str(value)==str(k)),
                _required=bool(self.attrs.get("required",None)),
                _readonly=bool(self.attrs.get("readonly",None)),
                _onchange=f"document.getElementById('{id(self)}').value='{k}';"
            )
            self <= Tag.div([
                ipt,
                Tag.label( v , _for=str(id(ipt)))
            ],_style="padding:8px")

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
        def call(ev):
            autoclosemenu( self.parent )
            return ev.target.method()

        for k,v in entries.items():
            self <= Tag.md_menu_item( Tag.div(k,_slot="headline") ,method=v,_onclick=call)

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


class ModalBlock(Tag.div):
    def init(self,metatag,obj):
        modal=Tag.div( obj, _style="position:fixed;left:0px;right:0px;top:0px;bottom:0px;z-index:1001;    display:flex;align-items:center;justify-content:center;")
        self <= Voile() + modal


class ModalAlert(Tag.md_dialog):

    def init(self,metatag,obj,wsize:float=None):
        #*IMPORTANT* : "wsize" as no effect in md ;-(
        
        self.metatag=metatag
        self["open"]=True
        self["type"]="alert"
        # self <= Tag.div("title",_slot="headline")

        self <= Tag.div(obj,_slot="content",_method="dialog")

        self.js="""
        self.addEventListener('closed', () => {
            self.closed()
        });"""

    def close(self,ev=None):
        self.call( "try{self.close()}catch(e){}")    # the self.close crash in some cases ?!?


    @expose
    def closed(self):
        self.metatag.step()



class ModalConfirm(ModalAlert):
    def __init__(self,metatag,obj,cb):
        def call(ev):
            self.close()
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
            self.close()
            return cb( dico["promptvalue"] )
        with Form(onsubmit=call) as f:
            f+=Tag.div( title )
            f+=Tag.div( Input(_value=value,_name="promptvalue",js="self.focus();self.select()", _autofocus=True) ,_style="padding:4px 0")
            f+=Button("Ok" )
            f+=Button("Cancel",_type="button",_onclick=self.close)
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
                tag.style="position:fixed;z-index:2001;padding:2px;left:"+x+"px;top:"+y+"px;background:Canvas";
            },0);
        })(self,%s,%s)""" % (x,y)

        self <= Tag.div( obj ,js=js)
class Toast(Tag.div):
    def init(self,main_non_used,obj,timeout=1000):
        self["style"]="position:fixed;right:10px;bottom:10px;z-index:1001;border:2px solid black;background:Canvas;padding:10px";
        self <= obj
        self.js="setTimeout( function() {self.remove()} , %s)" % timeout

######################################################################################



class Tabs(Tag.div):
    statics=STATICS
    def init(self,metatag,selected=0):
        with Tag.md_tabs() as t:
            for idx,i in enumerate(metatag._tabs):
                name = hasattr(i,"name") and i.name or "?(name)?"
                t<=Tag.md_primary_tab(name, _onclick = metatag.stepevent(select=idx), _active=(idx==selected))
        self += t
        if metatag._tabs: self+=metatag._tabs[selected]

