# -*- coding: utf-8 -*-
import html,sys,os
from htag import Tag,expose,Runner


def r(o):
    x=o.__class__.__name__
    if o.attrs.get("name"):
        x+=f"[{o['name']}]"
    return x

#=================================================================================
if __name__ == "__main__":
    # import logging
    # logging.basicConfig(format='[%(levelname)-5s] %(name)s: %(message)s',level=logging.INFO)
    # logging.getLogger("htag.tag").setLevel( logging.INFO )


    base=sys.argv[1] if len(sys.argv)>1 else "basics"
    if base == "bulma":
        import htagui.bulma as ui
    elif base == "shoelace":
        import htagui.shoelace as ui      
    elif base == "md":
        import htagui.md as ui      
    else:
        import htagui.basics as ui

    class TestInputs(Tag.div):
        def init(self, root, dynamic=False):
            self.output=root.output
            self.dynamic=dynamic

            OPTS = {1:"v1",2:"v2",3:"v3"}
            if dynamic:
                self.objects=[
                    ui.IText("itext",           onchange=self.onchange_dynamic),
                    ui.ITextarea("itextarea",   onchange=self.onchange_dynamic),
                    ui.IBool(True,              onchange=self.onchange_dynamic),
                    ui.IRange(42,               onchange=self.onchange_dynamic),
                    ui.ISelect(2,OPTS,          onchange=self.onchange_dynamic),
                    ui.IRadios(3,OPTS,          onchange=self.onchange_dynamic),
                ]
            else:
                self.objects=[ # _onchange can't work sith shoelace !!!!
                    ui.Input(_value="input",                    _onchange=self.bind( self.onchange_static, b"this.value"),_name="myinput"),
                    ui.Textarea("textarea",                     _onchange=self.bind( self.onchange_static, b"this.value"),_name="mytextarea"),
                    ui.Input(_type="checkbox",_checked=True,    _onchange=self.bind( self.onchange_static, b"this.checked || this.selected"),_name="mycheckbox"),   # selected for "MD" !!!!
                    ui.Input(_type="range",_value=42,           _onchange=self.bind( self.onchange_static, b"this.value"),_name="myrange"),
                    ui.Select(OPTS,_value=2,                    _onchange=self.bind( self.onchange_static, b"this.value"),_name="myselect"),
                    ui.Radios(OPTS,_value=2,                    _onchange=self.bind( self.onchange_static, b"this.value"),_name="myradios"),
                ]

            self.omain=Tag.div()
            self <= self.omain
            self.generate()

        def generate(self):
            self.output() # clean if real
            HBox=ui.hflex("0 0 200px","*")

            if self.dynamic:
                self.omain.clear( Tag.h1( "Dynamics" ))
                self.omain <= [HBox( i.__class__.__name__,i) for i in self.objects]
                self.omain <= ui.Button("save",_onclick=lambda ev: self.dyn_save(self.objects))
                self.omain <= ui.Button("load",_onclick=lambda ev: self.dyn_load(self.objects))
            else:
                self.omain.clear( Tag.h1( "Statics" ))
                def onsubmit(d):
                    self.output(f"form/dict submitted: {d}")
                self.omain <= ui.Form( onsubmit ) <= [HBox( r(i),i) for i in self.objects] + ui.Button("submit") + ui.Button("reset",_type="reset")

        def dyn_save(self,liste):
            for i in liste:
                i.saved_value=i.value
                self.output(f"getter {r(i)} -> {i.value} ({type(i.value)})")

        def dyn_load(self,liste):
            for i in liste:
                i.value = i.saved_value
                self.output(f"setter {r(i)} <- {i.value} ({type(i.value)})")

        def onchange_static(self,v):
            self.output( f"_onchange static : {v}")

        def onchange_dynamic(self,ev):
            o = ev.target
            self.output( f"onchange dynamic on {r(o)} : {o.value} ({type(o.value)})")


    class TestTabs(Tag.div):
        def init(self,root):
            output = root.output
            #================================================
            self<=Tag.h2("Test TABS features")
            #================================================
            t1=Tag.div("hello1",name="tab1")
            t2=Tag.div("hello2",name="tab2")
            t3=Tag.div("hello3",name="tab3")
            t=ui.Tabs( t1,t2,t3,onchange = lambda x: output("tab changed"+str(x.selected)))
            self <= t

            def force_select(nb):
                t.selected=nb
            self <= ui.Button("Select 1",_onclick=lambda ev: force_select(0) )
            self <= ui.Button("Select 2",_onclick=lambda ev: force_select(1) )
            self <= ui.Button("add a tab",_onclick=lambda ev: t.add_tab(Tag.div("Fresh",name="fresh") ) )



    class TestDialogs(ui.App):
        imports=ui.ALL
        def init(self,root):
            self_ui=root.ui
            #================================================
            self<=Tag.h2("Test UI features")
            #================================================
            entries={
                "menu1": lambda: self_ui.notify("menu1"),
                "menu2": lambda: self_ui.notify("menu2"),
                "menu3": lambda: self_ui.notify("menu3"),
            }  

            self <= ui.Button("alert", _onclick=lambda ev: self_ui.alert("kkkk"))
            self <= ui.Button("confirm", _onclick=lambda ev: self_ui.confirm("kkkk", self_ui.notify), _class="blue")
            self <= ui.Button("prompt", _onclick=lambda ev: self_ui.prompt("value","text?", self_ui.notify) )

            self <= ui.Button("notify", _onclick=lambda ev: self_ui.notify("kkkk") ,_class="green")

            self <= ui.Button("box .1", _onclick=lambda ev: self_ui.box("kkkk",size=0.1) ,_class="red")
            self <= ui.Button("box .2", _onclick=lambda ev: self_ui.box("kkkk",size=0.2) ,_class="red")
            self <= ui.Button("box .5", _onclick=lambda ev: self_ui.box("kkkk",size=0.5) ,_class="red")
            self <= ui.Button("box .6", _onclick=lambda ev: self_ui.box("kkkk",size=0.6) ,_class="red")
            self <= ui.Button("box .7", _onclick=lambda ev: self_ui.box("kkkk",size=0.7) ,_class="red")
            self <= ui.Button("box .9", _onclick=lambda ev: self_ui.box("kkkk",size=0.9) ,_class="red")
            self <= ui.Button("box 1", _onclick=lambda ev: self_ui.box("kkkk",size=1) ,_class="red")

            self <= ui.Button("pop", _onclick=lambda ev: self_ui.pop("kkkk",(ev.clientX,ev.clientY)) )
            self <= ui.Button("pop menu", _onclick=lambda ev: self_ui.pop( ui.Menu(entries) ,(ev.clientX,ev.clientY)) )
            self <= ui.Button("drawer left", _onclick=lambda ev: self_ui.drawer( ui.Menu(entries),"left" ))
            self <= ui.Button("drawer right", _onclick=lambda ev: self_ui.drawer( "yo","right" ))
            self <= ui.Button("drawer top", _onclick=lambda ev: self_ui.drawer( "yo","top" ))
            self <= ui.Button("drawer bottom", _onclick=lambda ev: self_ui.drawer( "yo","bottom" ))

            self.nb=0
            def imbricated(ev):
                self.nb+=1
                o=Tag.div(f"hello {self.nb}")
                o <= ui.Button("previous alert", _onclick=lambda ev: self_ui.previous() )
                o <= ui.Button("next alert", _onclick=imbricated )
                self_ui.alert(o)
                
            self <= ui.Button("imbricated alert", _onclick=imbricated )

            def block(ev):
                self_ui.block( Tag.div(ui.Spinner()+ui.Button("unblock",_onclick=lambda ev: self_ui.close())) )
                # self_ui.block( Tag.img(_src="https://picsum.photos/501/501",_onclick=lambda ev: self_ui.close())) 
            
            self <= ui.Button("block", _onclick=block)


            self <= Tag.hr()
            async def atest_yield(v):
                self_ui.block( Tag.div(f"yield({v})"+ui.Button("unblock",_onclick=lambda ev: self_ui.close())) )
                yield
                import time;time.sleep(0.5)
                self_ui.close()

            def test_yield(v):
                self_ui.block( Tag.div(f"yield({v})"+ui.Button("unblock",_onclick=lambda ev: self_ui.close())) )
                yield
                import time;time.sleep(0.5)
                self_ui.close()

            self <= ui.Button("test cb ayield", _onclick=lambda ev: self_ui.prompt("value","?", atest_yield))
            self <= Tag.a("test cb ayield", _onclick=atest_yield)
            self <= ui.Button("test cb ayield", _onclick=lambda ev: self_ui.prompt("value","?", test_yield))
            self <= Tag.a("test cb ayield", _onclick=test_yield)

            self <= Tag.hr()

            def copy(ev):
                self_ui.clipboard_copy("hello")
                self_ui.notify("copied")
            
            self <= ui.Button("copy into clipboard", _onclick=copy)


    class TestOthers(Tag.div):
        def init(self,root):
            self <= ui.HSplit( Tag.div("A"), Tag.div("B"),_style="height:100px;border:1px solid black")
            self <= ui.HSplit( Tag.div("A"), Tag.div("B"), Tag.div("C"), sizes=[20,20,60],minSize=20,_style="height:100px;border:1px solid black")
                    

    class App(ui.App):
        imports=ui.ALL
        def init(self):
            self["class"]="content" # for bulma

            self.omain = Tag.div( )
            self.oresult = Tag.div(_style="display:flex;flex-flow:column nowrap;flex-direction: column-reverse;")

            self <= ui.Button("basics",_onclick=lambda ev: self.restart_with("basics"))
            self <= ui.Button("bulma",_onclick=lambda ev: self.restart_with("bulma"))
            self <= ui.Button("shoelace",_onclick=lambda ev: self.restart_with("shoelace"))
            self <= ui.Button("md",_onclick=lambda ev: self.restart_with("md"))
            self <= Tag.hr()
            self <= ui.Button("Dialogs",_onclick=lambda ev: self.omain.clear(TestDialogs( self )) )
            self <= ui.Button("Tabs",_onclick=lambda ev: self.omain.clear(TestTabs( self )) )
            self <= ui.Button("Inputs statics",_onclick=lambda ev: self.omain.clear(TestInputs(self)) )
            self <= ui.Button("I-fields dynamics",_onclick=lambda ev: self.omain.clear(TestInputs(self,True)) )
            self <= ui.Button("others",_onclick=lambda ev: self.omain.clear(TestOthers(self)) )

            self <= self.omain
            self <= self.oresult

            self.omain<= TestDialogs( self )

        def restart_with(self,mode):
            self.call("window.close()")
            yield
            os.execv(sys.executable, ["python3"]+[os.path.abspath(sys.argv[0]), mode])

        def output(self,x=None):
            if x:
                self.oresult <= Tag.li( html.escape(x) )
            else:
                self.oresult.clear()

    Runner(App).run()
