import time
from htag import Tag,expose

import importlib,__main__
print(f"IMPORT [{__main__.htaguimodule}]")
ui = importlib.import_module(__main__.htaguimodule)


class IField:
    """ append a field self.value which interact with 'prop' of object using 'onchange' event 
    """
    _value=None
    def __init__(self,object:Tag,prop:str,js_value_getter:bytes,caster=lambda x:x):
        self.object=object
        self.prop = prop
        self.caster = caster
        if prop:
            self._value=self.caster(self.object.attrs.get( prop ))
        else:
            self._value=self.caster(self.object.innerHTML)
        
        if self.object.tag.startswith("sl-") or self.object.tag.startswith("sl_"):
            self.js="""
            self.addEventListener('sl-change', (e)=> {
                %s
            });""" % self.bind._iset_sl( b"jevent(e)", js_value_getter.replace(b"this",b"self") )
        else:
            self.object["onchange"] = self.bind( self._iset, js_value_getter )

    def _iset(self, ev, value:str):
        """ set from clientside """
        self._value = self.caster(value)

        return self.object.onchange(ev)

    def _iset_sl(self, jsevent:dict, value:str):
        """ set from clientside (for shoelace comp)"""

        from collections import namedtuple
        typevent=namedtuple("event", ["target"] + list(jsevent.keys()))
        event = typevent( self.object, **jsevent )
                
        self._iset(event,value)
           
    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, value):
        """ set from serverside, and update UI """
        if hasattr(self,"rerender"):
            self.rerender( value )
        else:            
            self.object.attrs["nimp_nawak"] = time.time()
            self._value = self.caster(value) 
            if self.prop:
                self.object.attrs[ self.prop ] = self._value
            else:
                self.object.clear( self._value )
        

class IText(ui.Input,IField):
    def __init__(self, value:str, onchange=lambda ev: None,**k):
        self.onchange = onchange
        ui.Input.__init__(self,_value=value,_type="text",**k)
        IField.__init__(self, self, "value", b"this.value",lambda x: str(x) )

class ITextarea(ui.Textarea,IField):
    def __init__(self, value:str, onchange=lambda ev: None,**k):
        self.onchange = onchange
        ui.Textarea.__init__(self,value,**k)
        IField.__init__(self, self, None, b"this.value",lambda x: str(x) )

class IBool(ui.Input,IField):
    def __init__(self, value:bool, onchange=lambda ev: None,**k):
        self.onchange = onchange
        ui.Input.__init__(self,_checked=bool(value),_type="checkbox",**k)
        if self.tag.startswith("md-"):
            IField.__init__(self, self, "selected", b"this.selected", lambda x: bool(x) )
        else:
            IField.__init__(self, self, "checked", b"this.checked", lambda x: bool(x) )

class IRange(ui.Input,IField):
    def __init__(self, value:int, onchange=lambda ev: None,**k):
        self.onchange = onchange
        ui.Input.__init__(self,_value=value,_type="range",**k)
        IField.__init__(self, self, "value", b"this.value", lambda x: int(x) )

class ISelect(ui.Select,IField):
    def __init__(self, value, options:dict, onchange=lambda ev: None,**k):
        self.onchange = onchange
        ui.Select.__init__(self, options, _value=value,**k)
        IField.__init__(self, self, "value", b"this.value", lambda x:x )

class IRadios(ui.Radios,IField):
    def __init__(self, value, options:dict, onchange=lambda ev: None,**k):
        self.onchange = onchange
        ui.Radios.__init__(self, options, _value=value,**k)
        IField.__init__(self, self, "value", b"this.value", lambda x:x )
