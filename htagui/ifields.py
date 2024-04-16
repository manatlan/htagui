import time
from htag import Tag

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
        
        self.object["onchange"] = self.bind( self._iset, js_value_getter )

    def _iset(self, ev, value:str):
        """ set from clientside """
        #TODO: remove
        print("=== ISET ===",self.object.__class__.__name__,self.prop,"<-",value)
        self._value = self.caster(value)

        return self.object.onchange(ev)
            
    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, value):
        """ set from serverside, and update UI """
        #TODO: clean that
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

class ITextarea(Tag.textarea,IField):
    def __init__(self, value:str, onchange=lambda ev: None,**k):
        self.onchange = onchange
        Tag.textarea.__init__(self,value,**k)
        IField.__init__(self, self, None, b"this.value",lambda x: str(x) )

class IBool(ui.Input,IField):
    def __init__(self, value:bool, onchange=lambda ev: None,**k):
        self.onchange = onchange
        ui.Input.__init__(self,_checked=bool(value),_type="checkbox",**k)
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
