#!/usr/bin/python3 -u
# -*- coding: utf-8 -*-
from htag import Tag

BULMA = [Tag.link( _href="https://cdn.jsdelivr.net/npm/bulma@0.8.2/css/bulma.min.css",_rel="stylesheet")]

class Input(Tag.input):
    statics= BULMA
    def init(self,**a):
        self["class"].add("input")


class Button(Tag.button):
    statics= BULMA
    def init(self,title,**a):
        self <= title
        self["class"].add("button")

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

class Menu(Tag.div):
    def init(self,entries:dict):
        def call(ev):
            ev.target.method()
        for k,v in entries.items():
            self += Tag.div(k,method=v,_onclick=call,_style="padding:4px;cursor:pointer;border:1px dotted #CCC")

class Spinner(Tag.span):
    statics="""
.spinner {
    width: 32px;
    height: 32px;
    border: 8px solid #33F;
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
    def init(self):
        self["class"]="spinner"


