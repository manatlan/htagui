# -*- coding: utf-8 -*-
from htag import Tag,expose,Runner
import htagui.basics as ui
# import htagui.bulma as ui
# import htagui.shoelace as ui

class App(ui.App):
    imports=ui.ALL
    def init(self):
        self <= IString("val",onchange=self.onchange)
        self <= IText("val",onchange=self.onchange)
        self <= IBool(True,onchange=self.onchange)
        self <= IRange(42,onchange=self.onchange)
    def onchange(self,ev):
        pass
#=================================================================================
if __name__ == "__main__":
    Runner(App).run()
