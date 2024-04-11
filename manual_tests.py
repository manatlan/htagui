# -*- coding: utf-8 -*-
from htag import Tag,expose,runners
import htag.ui as u

class App(u.App):
    imports=u.ALL
    def init(self):
        #================================================
        self<=Tag.h2("Test UI features")
        #================================================
        entries={
            "menu1": lambda: self.ui.notify("menu1"),
            "menu2": lambda: self.ui.notify("menu2"),
            "menu3": lambda: self.ui.notify("menu3"),
        }  

        self <= u.Button("alert", _onclick=lambda ev: self.ui.alert("kkkk") ,_class="red")
        self <= u.Button("notify", _onclick=lambda ev: self.ui.notify("kkkk") ,_class="green")
        self <= u.Button("confirm", _onclick=lambda ev: self.ui.confirm("kkkk", self.ui.notify), _class="blue")
        self <= u.Button("prompt", _onclick=lambda ev: self.ui.prompt("value","text?", self.ui.notify) )
        self <= u.Button("pop", _onclick=lambda ev: self.ui.pop("kkkk",(ev.clientX,ev.clientY)) )
        self <= u.Button("pop menu", _onclick=lambda ev: self.ui.pop( u.Menu(entries) ,(ev.clientX,ev.clientY)) )
        self <= u.Button("drawer left", _onclick=lambda ev: self.ui.drawer( u.Menu(entries),"left",80 ))
        self <= u.Button("drawer right", _onclick=lambda ev: self.ui.drawer( "yo","right" ))
        self <= u.Button("drawer top", _onclick=lambda ev: self.ui.drawer( "yo","top" ))
        self <= u.Button("drawer bottom", _onclick=lambda ev: self.ui.drawer( "yo","bottom" ))
        
        def test(ev):
            self.ui.block( Tag.div(u.Spinner()+u.Button("unblock",_onclick=lambda ev: self.ui.close())) )
        
        self <= u.Button("block", _onclick=test)




        #================================================
        self<=Tag.h2("Test FORM feature")
        #================================================
        with u.Form( onsubmit=lambda d: self.ui.notify(str(d)) ) as f:
            HBox = u.hflex("0 0 70px","*") #<- create an htag class for 2 elements
            f<=HBox("label",u.Input(_name="lbl",_required=True))
            f<=HBox("chk",Tag.label( u.Input(_name="check",_type="checkbox") + "yoyo" ))
            f<=HBox("radio", [
                Tag.label( u.Input(_name="rb",_type="radio",_value=1) + "1"),
                Tag.label( u.Input(_name="rb",_type="radio",_value=2) + "2")
            ])
            f<=HBox("range",u.Input(_name="val",_type="range"))
            f<=HBox("Select",u.Select( {1:"v1",2:"v2",3:"v3"},_value=2, _name="myselect"))
            f<=u.Button("submit")
            f<=u.Button("no_submit",_type="button")
            f<=u.Button("reset",_type="reset")
        self <= f



        #================================================
        self<=Tag.h2("Test TABS features")
        #================================================
        t1=Tag.div("hello1",name="tab1")
        t2=Tag.div("hello2",name="tab2")
        t3=Tag.div("hello3",name="tab3")
        t=u.Tabs( t1,t2,t3 ,onchange = lambda x: self.ui.notify("tab changed"+str(x.selected)))
        self <= t

        def force_select(nb):
            t.selected=nb
        self <= u.Button("Select 1",_onclick=lambda ev: force_select(0) )
        self <= u.Button("Select 2",_onclick=lambda ev: force_select(1) )
        self <= u.Button("add a tab",_onclick=lambda ev: t.add_tab(Tag.div("Fresh",name="fresh") ) )

        #================================================
        self<=Tag.h2("Test HSPLIT features")
        #================================================
        self <= u.HSplit( Tag.div("A"), Tag.div("B"), Tag.div("C"), sizes=[20,20,60],minSize=20,_style="height:100px;border:1px solid black")
        
#=================================================================================
if __name__ == "__main__":
    Runner(App).run()
