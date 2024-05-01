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
    elif base == "fluent":
        import htagui.fluent as ui      
    else:
        import htagui.basics as ui

    class TestInputs(Tag.div):
        def init(self, root, dynamic=False):
            self.output=root.output
            self.dynamic=dynamic

            OPTS = {1:"v1",2:"v2",3:"v3"}
            if dynamic:
                self.objects=[
                    ui.IText("itext",           onchange=self.onchange_dynamic,_label="itext"),
                    ui.ITextarea("itextarea",   onchange=self.onchange_dynamic,_label="itextarea"),
                    ui.IBool(True,              onchange=self.onchange_dynamic),
                    ui.IRange(42,               onchange=self.onchange_dynamic),
                    ui.ISelect(2,OPTS,          onchange=self.onchange_dynamic),
                    ui.IRadios(3,OPTS,          onchange=self.onchange_dynamic),
                ]
            else:
                self.objects=[ # _onchange can't work sith shoelace !!!!
                    ui.Input(_value="input",                    _onchange=self.bind( self.onchange_static, b"this.value"),_name="myinput",_label="myinput"),
                    ui.Textarea("textarea",                     _onchange=self.bind( self.onchange_static, b"this.value"),_name="mytextarea" ,_label="mytextarea"),
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



    class TestDialogs(Tag.div):
        imports=ui.ALL
        def init(self,root):
            self.ui=root.ui
            #================================================
            self<=Tag.h2("Test UI features")
            #================================================
            entries={
                "menu1": lambda: self.ui.notify("menu1"),
                "menu2": lambda: self.ui.notify("menu2"),
                "menu3": lambda: self.ui.notify("menu3"),
            }  

            content="fdsfd sgfdg g gfds ggfds g"*1000

            self <= ui.Button("notify", _onclick=lambda ev: self.ui.notify("kkkk"))

            self<= Tag.hr()+"dialog alert & cousins"
            self <= ui.Button("alert", _onclick=lambda ev: self.ui.alert(content))
            self <= ui.Button("alert size=.1", _onclick=lambda ev: self.ui.alert("kkkk",size=0.1))
            self <= ui.Button("alert size=.5", _onclick=lambda ev: self.ui.alert("kkkk",size=0.5))
            self <= ui.Button("alert size=.9", _onclick=lambda ev: self.ui.alert("kkkk",size=0.9))
            self <= ui.Button("alert size=1", _onclick=lambda ev: self.ui.alert("kkkk",size=1))

            self <= ui.Button("confirm", _onclick=lambda ev: self.ui.confirm("kkkk", self.ui.notify))
            self <= ui.Button("prompt", _onclick=lambda ev: self.ui.prompt("What's your name?","value", self.ui.notify) )

            self<= Tag.hr()+"dialog poppers"
            self <= ui.Button("drawer left", _onclick=lambda ev: self.ui.drawer( ui.Menu(entries),"left" ))
            self <= ui.Button("drawer right", _onclick=lambda ev: self.ui.drawer( "yo","right" ))
            self <= ui.Button("drawer top", _onclick=lambda ev: self.ui.drawer( "yo","top" ))
            self <= ui.Button("drawer bottom", _onclick=lambda ev: self.ui.drawer( "yo","bottom" ))

            self<= Tag.hr()+"dialog blockers"

            def block(ev):
                self.ui.block( Tag.div(ui.Spinner()+ui.Button("unblock",_onclick=lambda ev: self.ui.close() ) + ui.Menu(entries)) )

            def page(ev):
                self.ui.page( ui.Menu(entries) + Tag.h3("Click the image to quit")+Tag.img(_src="https://picsum.photos/501/501",_onclick=lambda ev: self.ui.page()) ) 

            self <= ui.Button("block", _onclick=block)
            self <= ui.Button("page", _onclick=page)


            self <= Tag.hr()
            async def atest_yield(v):
                self.ui.block( Tag.div(f"yield({v})"+ui.Button("unblock",_onclick=lambda ev: self.ui.close())) )
                yield
                import time;time.sleep(0.5)
                self.ui.close()

            def test_yield(v):
                self.ui.block( Tag.div(f"yield({v})"+ui.Button("unblock",_onclick=lambda ev: self.ui.close())) )
                yield
                import time;time.sleep(0.5)
                self.ui.close()

            self <= ui.Button("test cb (async) yield", _onclick=lambda ev: self.ui.prompt("value","?", atest_yield))
            self <= ui.Button("test cb yield", _onclick=lambda ev: self.ui.prompt("value","?", test_yield))

            self <= Tag.hr()

            def copy(ev):
                self.ui.clipboard_copy("hello")
                self.ui.notify("copied")
            
            self <= ui.Button("copy into clipboard", _onclick=copy)

            self <= Tag.hr()

            def pop_in_dialog(ev):
                o=Tag.div("hello")
                o<=ui.Button("pop",_onclick = lambda ev: self.ui.pop( ui.Menu(entries) ,(ev.clientX,ev.clientY)) )
                self.ui.alert(o)

            self <= ui.Button("pop in dialog", _onclick=pop_in_dialog)

            self <= ui.Button("pop", _onclick=lambda ev: self.ui.pop("kkkk",(ev.clientX,ev.clientY)) )
            self <= ui.Button("pop menu", _onclick=lambda ev: self.ui.pop( ui.Menu(entries) ,(ev.clientX,ev.clientY)) )


    class TestOthers(Tag.div):
        def init(self,root):
            self.output=root.output

            h=ui.HSplit( Tag.div("A"), Tag.div("B"),_style="height:100px;border:1px solid black", onchange = lambda o: self.output( f"h sizes: {o.sizes}" ))
            v=ui.VSplit( Tag.div("A"), Tag.div("B"),minSize=10)
            self <= h
            self<= ui.Button("50,50",_onclick=lambda ev: h.setSizes([50,50]))
            self<= ui.Button("70,30",_onclick=lambda ev: h.setSizes([70,30]))


            self <= ui.HSplit( Tag.div("A"), Tag.div("B"), v, sizes=[20,20,60],minSize=20,_style="height:100px;border:1px solid black")
                    
            def doit(name:str,content:bytes):
                self.output( f'uploaded {name} ({len(content)} bytes)')

            self <= Tag.div("Simple:") <= ui.FileUpload( doit ) )
            self <= Tag.div("Multiple:") <= ui.FileUpload( doit, _multiple=True ) )

    class App(ui.App):
        statics="""
        my {cursor:pointer;padding:4px;margin:4px;display:inline-block;text-decoration:underline}
        my.selected {color:red;}
        hr {padding:0px !important;margin:4px !important;}
        """
        
        imports=ui.ALL
        def init(self):
            self["class"]="content" # for bulma

            self.omain = Tag.div( )
            self.oresult = Tag.div(_style="display:flex;flex-flow:column nowrap;flex-direction: column-reverse;")

            f = lambda x: "selected" if base==x else ''
            self <= Tag.my("basics",_onclick=lambda ev: self.restart_with("basics"),_class=f("basics"))
            self <= Tag.my("bulma",_onclick=lambda ev: self.restart_with("bulma"),_class=f("bulma"))
            self <= Tag.my("shoelace",_onclick=lambda ev: self.restart_with("shoelace"),_class=f("shoelace"))
            self <= Tag.my("md",_onclick=lambda ev: self.restart_with("md"),_class=f("md"))
            self <= Tag.my("fluent",_onclick=lambda ev: self.restart_with("fluent"),_class=f("fluent"))

            def setter(o,testobject):
                for i in o.parent.childs:
                    i["class"].remove("selected")    
                o["class"].add("selected")
                self.omain.clear(testobject)

            with Tag.div() as menu:
                menu <= Tag.my("Dialogs",_onclick=lambda ev: setter(ev.target,TestDialogs( self )),_class="selected" )
                menu <= Tag.my("Tabs",_onclick=lambda ev: setter(ev.target,TestTabs( self )) )
                menu <= Tag.my("Inputs statics",_onclick=lambda ev: setter(ev.target,TestInputs(self)) )
                menu <= Tag.my("I-fields dynamics",_onclick=lambda ev: setter(ev.target,TestInputs(self,True)) )
                menu <= Tag.my("others",_onclick=lambda ev: setter(ev.target,TestOthers(self)) )
            self <= menu
            self <= Tag.hr()
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
