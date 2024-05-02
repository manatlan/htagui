# -*- coding: utf-8 -*-
# #############################################################################
# Copyright (C) 2024 manatlan manatlan[at]gmail(dot)com
#
# MIT licence
#
# https://github.com/manatlan/htag
# #############################################################################
from htag import Tag,expose
from .common import MetaTag

import importlib,__main__
print(f"IMPORT [{__main__.htaguimodule}]")
cui = importlib.import_module(__main__.htaguimodule)

import base64
def toDataurl(content:bytes):
    return u'data:;base64,'+base64.b64encode(content).decode()

class Dialog(Tag.htaguidialog,MetaTag):
    imports=[cui.Voile,cui.Button,cui.Input]

    def init(self,parent):
        self["info"]="UI.current object"
        self._toasts = Tag.div(_info="UI.toasts objects")
        self._page = Tag.div(_info="UI.page object")
        self._pop = Tag.htaguipop(_info="UI.pop object")
        parent += self  # auto add
        parent += self._toasts  # add a personnal place for toasts
        parent += self._page  # add a personnal place for page
        parent += self._pop  
        MetaTag.init(self)

    def clipboard_copy(self,txt:str):
        self.call(f"""navigator.clipboard.writeText(`{txt}`);""")

    def clipboard_paste(self,callback=lambda x:x):
        self.callback_clipboard_paste = callback
        self.call("""navigator.clipboard.readText().then( self._clipboard_paste )""")

    @expose
    def _clipboard_paste(self,content:str):
        return self.callback_clipboard_paste(content)

    def download(self,name:str,content:bytes):
        self.call( f"""
            let anchor = document.createElement('a');
            anchor.href = `{toDataurl(content)}`;
            anchor.target = '_blank';
            anchor.download = `{name}`;
            anchor.click();
        """)

    def alert(self,obj,size:float=None):
        """if no size is provided : use the default width size of the dialog (depending of ui used)"""
        self.step( alert = obj, size=size )

    def confirm(self,obj,cbresponse=lambda bool:bool):
        self.step( confirm = obj, cb=cbresponse )
        
    def prompt(self,title, value=None,cbresponse=lambda val:val):
        self.step( prompt = value or "", title=title, cb=cbresponse )


    def notify(self,obj,time=2000):
        self.step( toast = obj, time=time )

    def pop(self, obj, xy:tuple):
        self.step( pop = obj, xy=xy )
    def popclose(self):
        self.step( pop = None )

    def drawer(self, obj, mode="left"):
        assert mode in ["left","right","bottom","top"]
        self.step( drawer = obj, mode=mode )

    def block(self,obj=None):
        self.step( block=obj )

    def page(self,obj=None):
        self.step( page = obj)

    def close(self):
        self.step()

    def step(self,**params):

        def set(*a,**k):
            self(*a,**k)

        if "block" in params:
            set( cui.ModalBlock, params["block"] )
        elif "page" in params:
            # set( cui.PopPage, params["page"] )
            if params["page"] is None:
                self._page.clear()
            else:
                self._page.clear( cui.PopPage( self,  params["page"] ))
        elif "alert" in params:
            set( cui.ModalAlert, params["alert"], wsize=params.get("size") )
        elif "confirm" in params:
            set( cui.ModalConfirm, params["confirm"], params["cb"] )
        elif "prompt" in params:
            set( cui.ModalPrompt, params["prompt"],params["title"], params["cb"] )
        elif "pop" in params:
            if params["pop"] is None:
                self._pop.clear()
            else:            
                self._pop.clear( cui.Pop(self, params["pop"],params["xy"]) )
        elif "drawer" in params:
            self( cui.Drawer, params["drawer"], params["mode"] )
        elif "toast" in params:
            self._toasts.clear( cui.Toast( self, params["toast"], params["time"] ))
        else:
            set( cui.Empty )


    
