# -*- coding: utf-8 -*-
from htag import Tag,expose,Runner
import htagui.basics as ui
# import htagui.bulma as ui
# import htagui.shoelace as ui


#----------------------------------------------------
#TODO: declare in bases !
#----------------------------------------------------
class ui_Textarea(Tag.textarea):
    def init(self,content=None,**a):
        self <= content
#----------------------------------------------------

class IString(ui.Input):
    def __init__(self,value:str, onchange=lambda ev: None,**a):
        ui.Input.__init__(self,_value=value, _type="text", **a )
class IBool(ui.Input):
    def __init__(self,value:bool, onchange=lambda ev: None,**a):
        ui.Input.__init__(self,_value=bool(value), _type="checkbox", **a )
class IRange(ui.Input):
    def __init__(self,value:int, onchange=lambda ev: None,**a):
        ui.Input.__init__(self,_value=value, _type="range", **a )
class IText(ui_Textarea):
    def __init__(self,value:str, onchange=lambda ev: None, **a):
        ui_Textarea.__init__(self,value, **a)
class ISelect(ui.Select):
    def __init__(self,value, opts:dict, onchange=lambda ev: None,**a):
        ui.Select.__init__(self,opts, _value=value, **a )

class App(ui.App):
    imports=ui.ALL
    def init(self):
        OPTS = {1:"v1",2:"v2",3:"v3"}
        dynamics=[
            IString("val",onchange=self.onchange),
            IText("val",onchange=self.onchange),
            IBool(True,onchange=self.onchange),
            IRange(42,onchange=self.onchange),
            ISelect(42,OPTS,onchange=self.onchange),
        ]
        statics=[
            ui.Input(_value="val",_onchange=self.onchange),
            ui_Textarea("val",_onchange=self.onchange),
            ui.Input(_type="checkbox",_checked=True,_onchange=self.onchange),
            ui.Input(_type="range",_value=42,_onchange=self.onchange),
            ui.Select(OPTS,_value=42,_onchange=self.onchange),
        ]

        tab1=Tag.div( dynamics , name="Dynamics")
        tab2=Tag.div( statics , name="Statics")
        self <= ui.Tabs( tab1, tab2 )
            
    def onchange(self,ev):
        o = ev.target
        if hasattr(o,"value"): # <- TODO: can do better here
            dynamicvalue = o.value
        else:
            dynamicvalue = "NOT DYNAMIC FIELD"
        print( repr(o), dynamicvalue )
#=================================================================================
if __name__ == "__main__":
    Runner(App).run()
