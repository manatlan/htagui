# -*- coding: utf-8 -*-
from htag import Tag,expose,Runner
# import htagui.basics as ui
# import htagui.bulma as ui
import htagui.shoelace as ui      


class App(ui.App):
    imports=ui.ALL
    def init(self):
        OPTS = {1:"v1",2:"v2",3:"v3"}
        dynamics=[
            ui.IText("itext",onchange=self.onchange),
            ui.ITextarea("itextarea",onchange=self.onchange),
            ui.IBool(True,onchange=self.onchange),
            ui.IRange(42,onchange=self.onchange),
            ui.ISelect(2,OPTS,onchange=self.onchange),
        ]
        statics=[
            ui.Input(_value="input",_onchange=self.onchange),
            ui.Textarea("textarea",_onchange=self.onchange),
            ui.Input(_type="checkbox",_checked=True,_onchange=self.onchange),
            ui.Input(_type="range",_value=42,_onchange=self.onchange),
            ui.Select(OPTS,_value=2,_onchange=self.onchange),
        ]

        # tab1=Tag.div( dynamics , name="Dynamics")
        # tab2=Tag.div( statics , name="Statics")
        # self <= ui.Tabs( tab1, tab2 )
        self <= dynamics
        self <= Tag.button("save",_onclick=lambda ev: self.save(dynamics))
        self <= Tag.button("load",_onclick=lambda ev: self.load(dynamics))

    def save(self,liste):
        for i in liste:
            print( i.tag,"getter", i.value, type(i.value) )
            i.saved_value=i.value

    def load(self,liste):
        for i in liste:
            print( i.tag,"setter", i.value, type(i.value) )
            i.value = i.saved_value

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
