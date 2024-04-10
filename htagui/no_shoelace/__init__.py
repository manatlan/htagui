#!/usr/bin/python3 -u
# -*- coding: utf-8 -*-
from htag import Tag,expose

SHOELACE = [
        Tag.link(_rel="stylesheet",_href="https://cdn.jsdelivr.net/npm/@shoelace-style/shoelace@2.14.0/cdn/themes/dark.css" ),
        Tag.link(_rel="stylesheet",_href="https://cdn.jsdelivr.net/npm/@shoelace-style/shoelace@2.14.0/cdn/themes/light.css" ),
        Tag.script(_type="module",_src="https://cdn.jsdelivr.net/npm/@shoelace-style/shoelace@2.14.0/cdn/shoelace-autoloader.js"),
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

"""),
]

class Input(Tag.sl_input):
    statics= SHOELACE
class Button(Tag.sl_button):
    statics= SHOELACE
    def init(self,title,**a):
        self <= title

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


class Menu(Tag.sl_menu):
    statics= SHOELACE
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
        list(self._entries.values())[int(idx)]()



class Spinner(Tag.sl_spinner):
    statics=SHOELACE
    def init(self):
        self["style"]="font-size: 32px; --track-width: 8px;"


