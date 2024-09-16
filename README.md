# htagUI

This is a (basic) UI toolkit for [htag](https://github.com/manatlan/htag) apps. Contrario to [htbulma](https://github.com/manatlan/htbulma), this one is a minimal toolkit, providing only useful and solid widgets, and will be maintained (you can use it ;-)).

<img src="https://manatlan.github.io/htag/htag.png" width="100" height="100">

[![Test](https://github.com/manatlan/htagui/actions/workflows/on_commit_do_all_unittests.yml/badge.svg)](https://github.com/manatlan/htagui/actions/workflows/on_commit_do_all_unittests.yml)

<a href="https://pypi.org/project/htagui/">
    <img src="https://badge.fury.io/py/htagui.svg?x" alt="Package version">
</a>

**roadmap**

 - provide a darker theme css
 - test test & test, to be rock solid
 - be available in htag4brython too, with the same apis.
 - perhaps provide version using "shoelace web components", or "simple bulma styles" (like htbulma) ... but the basics version (current one) will always be available, with its minimal footprint (js/css dependancies in mind)


**INSTALL**
```bash
python3 -m pip install -U htagui
```
**note**: it will install htag and htagui, and provide the `ui` in the htag namespace (`htag.ui`)

A hello world could be :

```python
from htag import Tag, Runner, ui

class MyApp(ui.App):
    def init(self):
        self <= ui.Button("test", _onclick=lambda ev: self.ui.alert( "hello world" ) )

if __name__ == "__main__":
    Runner(MyApp).run()
```



It provides some (ready-to-use) Htag Objects, and some utilities methods.


## Object App

This is a surcharge of Tag.body( ... ) which auto provide an `ui` property on the instance, to interact with `Dialog` features

In place of:
```python
class MyApp(Tag.body):
    def init(self):
        self.ui = ui.Dialog(self)   # <- it will do that, automatically
        self <= ui.Button("test", _onclick=lambda ev: self.ui.alert( "hello" ) )
```

you can do :
```python
class MyApp(ui.App):
    def init(self):
        self <= ui.Button("test", _onclick=lambda ev: self.ui.alert( "hello" ) )
```

## Object Button

A simple surcharge of Tag.button(...), to define a css class 

```python
import htagui as ui
self <= ui.Button("my button",_class="myclass", _onclick = myevent )
```

## Object Input

A simple surcharge of Tag.input(...), to define a css class 


```python
import htagui as ui
self <= ui.Input(_value="my value", _name="myfield", _class="myclass", _required=True )
```

Availables managed `type`s (setted with `_type`) params:
 * `text` : the default one (if omitted): an input text
 * `checkbox` : a checkbox
 * `radio` : a radio button (non sense : use ui.Radios or uiIRadios !)
 * `range` : a slider/range

For `text`: a special field "_label" will set the html "placeholder" attribut.

## Object Textarea

A simple surcharge of Tag.textarea(...), to define a css class 


```python
import htagui as ui
self <= ui.Textarea("my value", _name="myfield", _class="myclass", _required=True )
```

A special field "_label" will set the html "placeholder" attribut.

## Object Spinner

A spinner object.

```python
import htagui as ui
self <= ui.Spinner()
```

## Objets "I-fields"

Theses are interactive/reactive fields, which are automatically synced between client and server side, thru a 'value' property

- IText .. an input of type text
- ITextarea ... a textarea 
- IBool ...  an input of type checkbox
- IRange ...  an input of type range
- ISelect ... a multichoice select/option
- IRadios ... a multichoice radio buttons

## Object Select

An htag class to help to create "select/option" html tags, using a dict of {value:title, ...}.

```python
import htagui as ui
self <= ui.Select( dict(a="A",b="B"), _value="a", _name="myfield" )
```

## Object Radios

An htag class to help to create "radio button choices" html tags, using a dict of {value:title, ...}.

```python
import htagui as ui
self <= ui.Radios( dict(a="A",b="B"), _value="a", _name="myfield" )
```

## Object Menu

An htag class to help to create a (first-level) menu and menu items, using a dict of {title:callback,...}

```python
import htagui as ui
ux = ui.Dialog(self)
entries={
    "menu1": lambda: ux.notify("menu1"),
    "menu2": lambda: ux.notify("menu2"),
    "menu3": lambda: ux.notify("menu3"),
}  
self <= ui.Menu( entries )
```


## Object Form

A simple surcharge of Tag.form(...) where you can define a callback to call a method wich will receive a python "dict" of all named inputs defined in the form.

```python
import htagui as ui
ux = ui.Dialog( self )
form = ui.Form( onsubmit=lambda dico: ux.notify(str(dico)) )
form <= ui.Input(_name="mystring",_placeholder="input something")
form <= ui.Button("ok")
self <= form
```

## Object FileUpload

A simple surcharge of Tag.input( _type='file'...) which call a method to upload the selected file.

```python
import htagui as ui

def uploaded(name:str, content:bytes):
    print(name,content)

self <= ui.FileUpload( uploaded , _multiple=True)
```

## Object Tabs

An htag class to easily create tabs structure. And provides somes attributs/methods to interact with it.

```python
import htagui as ui
tab1 = Tag.div("content1",name="tab1") # tab object needs a `name` property !
tab2 = Tag.div("content2",name="tab2")
t = ui.Tabs( tab1, tab2 )
self += t
```

### method t.add_tab( obj )

A method to add dynamically a tab instance, which is automatically selected.
(note that the tab object needs a `name` property !)

### property t.selected

Dynamic property to retrieve or select the current selected tab.

### event "onchange"

Event which is called when selected index changes.

## Object Dialog

Expose "Dialog boxes" with methods on the instance.
Note that, there can be only one dialog at a time (except toast notification)

```python
import htagui as ui
dialog = ui.Dialog( self )
```

### method dialog.alert(obj, size:float=None)

(like js window.alert(...)) Display a modal dialog box containing the object 'obj' (obj must be str'able)

size is a float to force the percent of width on the dialog box. If None, it will use the default from the ui used.

### method dialog.confirm(obj, cbresponse=lambda bool)

(like js window.confirm(...)) Display a modal dialog box containing the object 'obj' (obj must be str'able), and let the user click on Yes|No buttons, which will call the cbresponse callback with True or False ...

### method dialog.prompt(title, value=None, cbresponse=lambda val)

(like js window.prompt(...)) Display a modal dialog letting the user edit the `value` in an Input box, with a `title` (title must be str'able). When the user click the OK button the value is sent in the callback cbresponse. (clicking the cancel button does nothing, except close the dialog)



### method dialog.notify(obj, time=2000)

Display a toast message (notification), in the right-bottom ... during 2000 ms.
(currently toast messages are not stacked)

### method dialog.pop(obj, xy:tuple)

Display an object, at coords (x,y).

ex "create a popmenu", using "Menu object"
```python
import htagui as ui
dialog = ui.Dialog(self)
entries={
    "menu1": lambda: dialog.notify("menu1"),
    "menu2": lambda: dialog.notify("menu2"),
    "menu3": lambda: dialog.notify("menu3"),
}  
self <= ui.Button("pop menu", _onclick=lambda ev: dialog.pop( ui.Menu(entries) ,(ev.clientX,ev.clientY)) )
```
note: it ensures that the object is fully visible in the inner window.

### method dialog.drawer(obj, mode="left")

Display a drawer, in the left-side. mode can be left,right,top,bottom.

### method dialog.page(obj=None)

Display a full page 'obj', or remove page if obj is None. (note that ui.close() does not close the page) 

### method dialog.block(obj=None)

Display a modal dialog box containing the object 'obj'. But the dialog is not closable, so be sure to provide a way to close it.

### method dialog.close()

Close programatically, the current ui dialog.

### method dialog.clipboard_copy(txt:str)

Copy the txt in the clipboard

### method dialog.clipboard_paste( lambda content )

Call the callback with the text content from the clipboard. (user may need to authorize the interaction from the navigator)

### method dialog.download( name:str, content:bytes ):

Force the navigator to download a file named 'name', with the content bytes 'content' into the browser.

## Object HSplit & VSplit

A Tag object to use "SplitJS"

```python
import htagui as ui
split = ui.HSplit( Tag.div(1), Tag.div(2), sizes=[60,40], minSize=100, _style="border:2px solid red;height:100px" )
self <= split
```

methods:
split.setSizes( [50,50] )
split.onchange = lambda object: print( object.sizes )   # event


## Object Sortable

A component to let the user reorder items using drag'n'drop.

```python
ll=[Tag.div(f"Item {i} (drag me)",value=i) for i in range(10)]
        
def onchange(o:ui.Sortable):
    print( str([i.value for i in o.values]) )

self <= ui.Sortable(ll,onchange=onchange)
```

## Object VScroll

A component to help you to create an infinite scroller.

```python
def feed():
    yield [Tag.div(i) for i in range(20) ]

self <= Tag.div(_style="height:200px; border:1px solid red;" ) <= ui.VScroll( feed )
```

This component should be embbeded in an element which have a constraint on its height. The given callback should yield Tag(s) (or `None` to finnish the endless scroll)

## Object VScrollPager

A component (which inherit from VScroll) to present a finnished list of items in an "on-demand" way (create items on-demand), can contain a big amount of data.

```python

ll=[lambda i=i: MyObject(i) for i in range(1,200_000_000)]
self <= Tag.div(_style="height:200px; border:1px solid red;" ) <= ui.VScrollPager(ll,preload=50,moreload=10,endzone=50)

```
This component should be embbeded in an element which have a constraint on its height. `preload` is the number of items which will be created (it should overflow on height). `moreload` is the number of items which will be loaded when scrolling is in the `endzone` pixels at the end.

Note that the list is a list of lambda (`List[Callable[[], Tag]]`) to create the rendering on-demand.


## Object Swipper

**IMPORTANT** : not included in default (`ui.ALL`). If you want to use it, you must include it, or `imports=ui.FULL` (because +170ko). TODO: need to find a clever soluce ;-)

A component to use a Swiper (https://swiperjs.com/).

```python

ll=[lambda i=i: MyObject(i) for i in range(1,200_000)]  # slide created on demand
# or ll=[MyObject(i) for i in range(1,20)]              # concrete slides
self <= ui.Swiper(ll, default=0)

```


## Object View

A view component which handle the browser navigation mechanism (go back)

**IMPORTANT**:

 - this component is here for tests only (it may disappear if real problems)
 - FOR POWER USERS : may be used as first class, and you need to understand how htag works, and how the browser history works ! (if the object is deleted -> nothing work)

TODO: make a better good example !

```python

default_view=Tag.div("Default view")

v = ui.View( default_view, _style="border:1px solid red;width:100%;height:400px" )

self <= ui.Button("p1", _onclick = lambda ev: v.go( Tag.div("p1") ))
self <= ui.Button("p2", _onclick = lambda ev: v.go( Tag.div("p2") ))
self <= v
```


## utilities methods

### hflex & vflex

Methods to create an HBox or VBox htag class (flexbox horizontal or vertical, with nowrap mode)

```python
import htagui as ui
HBox = ui.hflex(50, 50)  # create a hbox of 2 elements of 50% each
self <= HBox( Tag.div(1), Tag.div(2) )
```
