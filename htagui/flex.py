# -*- coding: utf-8 -*-
# #############################################################################
# Copyright (C) 2024 manatlan manatlan[at]gmail(dot)com
#
# MIT licence
#
# https://github.com/manatlan/htag
# #############################################################################
from htag import Tag

def istyle(item) -> dict:
    """
    examples:
        istyle(None)      -> {}
        istyle(10)        -> {'flex': '1 1 10%'}
        istyle("*")       -> {'flex': '1 1 auto'}
        istyle("auto")    -> {'flex': '1 1 auto'}
        istyle("50%")     -> {'flex': '1 1 50%'}
        istyle("1 0 50%") -> {'flex': '1 0 50%'}
        istyle(dict(background="red")) -> {'background': 'red'}
    """
    if isinstance(item,str) or isinstance(item,int):
        # flex style        
        item=str(item).strip()
        if " " in item:
            # in the form "1 1 auto" ...
            return dict(flex=item)
        else:
            # in the form "50%", "*" , "50" ...
            if item in ["*","auto"]:
                item="auto"
            elif item.isnumeric():
                item=f"{item}%"
            return dict(flex=f"1 1 {item}")
    elif isinstance(item,dict):
        return item
    else:
        return {}

def flex_creator(defaults:list,mode="row"):
    """ Class creator (for hbox,vbox ...)"""
    assert mode in ["row","column"]
    class Class(Tag.div):
        def init(self,*objs,**a):
            self["style"]=f"display:flex;flex-flow:{mode} nowrap;align-items:baseline"
            for idx,obj in enumerate(objs):
                styles="".join([f"{k}:{v};" for k,v in istyle(defaults[idx]).items()])
                self <= Tag.div(obj,_style=styles)
    return Class

def hflex(*defaults):
    return flex_creator(defaults,mode="row")

def vflex(*defaults):
    return flex_creator(defaults,mode="column")
