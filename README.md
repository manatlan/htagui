# htagUI

This is a (basic) UI toolkit for [htag](https://github.com/manatlan/htag) apps. Contrario to [htbulma](https://github.com/manatlan/htbulma), this one is a minimal toolkit, providing only useful and solid widgets, and will be maintained (you can use it ;-)).

<img src="https://manatlan.github.io/htag/htag.png" width="100" height="100">

[![Test](https://github.com/manatlan/htagui/actions/workflows/on_commit_do_all_unittests.yml/badge.svg)](https://github.com/manatlan/htagui/actions/workflows/on_commit_do_all_unittests.yml)

<a href="https://pypi.org/project/htagui/">
    <img src="https://badge.fury.io/py/htagui.svg?x" alt="Package version">
</a>

**roadmap**

 - test test & test, to be rock solid
 - be available in htag4brython too, with the same apis.
 - perhaps provide version using shoelace web component, or simple bulma styles ... but the basics version (current one) will always be available, with its minimal footprint (js/css dependancies in mind)

A hello world could be (currently):

```python
from htag import Tag
import htagui as u

class MyApp(Tag.body):
    def init(self):
        self.ui = u.Dialog(self)
        self <= u.Button("test", _onclick=lambda ev: self.ui.alert( "hello" ) )

if __name__ == "__main__":
    from htag.runners import Runner
    Runner(MyApp).run()
```

but ideally (IN THE FUTURE), I'd like to come with that:

```python
from htag import Tag,Runner,ui # ui & Runner available in the htag namespace

class MyApp(ui.App):    # will autoset self.ui as Dialog (old UI) instancce
    def init(self):
        self <= ui.Button("test", _onclick=lambda ev: self.ui.alert( "hello" ) )

if __name__ == "__main__":
    Runner(MyApp).run()
```



It provides some (ready-to-use) Htag Objects, and some utilities methods.


## Object Button

A simple surcharge of Tag.button(...), to define a css class 

```python
import htagui as u
self <= u.Button("my button",_class="myclass", _onclick = myevent )
```

## Object Input

A simple surcharge of Tag.input(...), to define a css class 


```python
import htagui as u
self <= u.Input(_value="my value"_, _name="myfield", _class="myclass", _required=True )
```

## Object Spinner

A spinner object.

```python
import htagui as u
self <= u.Spinner()
```

## Object Select

An htag class to help to create `select/option` html tags, using a dict of {value:title, ...}.

```python
import htagui as u
self <= u.Select( dict(a="A",b="B"), _value="a", _name="myfield" )
```

## Object Menu

An htag class to help to create a (first-level) menu and menu items, using a dict of {title:callback,...}

```python
import htagui as u
ui = u.Dialog(self)
entries={
    "menu1": lambda: ui.notify("menu1"),
    "menu2": lambda: ui.notify("menu2"),
    "menu3": lambda: ui.notify("menu3"),
}  
self <= u.Menu( entries )
```


## Object Form

A simple surcharge of Tag.form(...) where you can define a callback to call a method wich will receive a python "dict" of all named inputs defined in the form.

```python
import htagui as u
ui = u.Dialog( self )
form = u.Form( onsubmit=lambda dico: ui.notify(str(dico)) )
form <= u.Input(_name="mystring",_placeholder="input something")
form <= u.Button("ok")
self <= form
```

## Object Tabs

An htag class to easily create tabs structure. And provides somes attributs/methods to interact with it.

```python
import htagui as u
tab1 = Tag.div("content1",name="tab1") # tab object needs a `name` property !
tab2 = Tag.div("content2",name="tab2")
t = u.Tabs( tab1, tab2 )
self += t
```

### method t.add_tab( obj )

A method to add dynamically a tab instance, which is automatically selected.
(note that the tab object needs a `name` property !)

### property t.selected

Dynamic property to retrieve or select the current selected tab.

### event "onchange"

Event which is called when selected index changes.

## Object UI (Dialog)

Expose "Dialog boxes" with methods on the ui instance.
Note that, there can be only one dialog at a time (except toast notification)

```python
import htagui as u
ui = u.Dialog( self )
```

### method ui.alert(obj)

(like js window.alert(...)) Display a modal dialog box containing the object 'obj' (obj must be str'able)

### method ui.confirm(obj, cbresponse=lambda bool:bool)

(like js window.confirm(...)) Display a modal dialog box containing the object 'obj' (obj must be str'able), and let the user click on Yes|No buttons, which will call the cbresponse callback with True or False ...

### method ui.prompt(value:str, title, cbresponse=lambda val:val)

(like js window.prompt(...)) Display a modal dialog letting the user edit the `value` in an Input box, with a `title` (title must be str'able). When the user click the OK button the value is sent in the callback cbresponse. (clicking the cancel button does nothing, except close the dialog)

### method ui.notify(obj, time=2000)

Display a toast message (notification), in the right-bottom ... during 2000 ms.
(currently toast messages are not stacked)

### method ui.pop(obj, xy:tuple)

Display an object, at coords (x,y).

ex "create a popmenu", using "Menu object"
```python
import htagui as u
ui = u.Dialog(self)
entries={
    "menu1": lambda: ui.notify("menu1"),
    "menu2": lambda: ui.notify("menu2"),
    "menu3": lambda: ui.notify("menu3"),
}  
self <= u.Button("pop menu", _onclick=lambda ev: ui.pop( u.Menu(entries) ,(ev.clientX,ev.clientY)) )
```

### method ui.drawer(obj, mode="left", size:int=50)

Display a drawer, in the left-side, which takes 50% of the page.

### method ui.block(obj=None)

Display a modal dialog box containing the object 'obj'. But the dialog is not closable, so be sure to provide a way to close it.

### method ui.close()

Close programatically, the current ui dialog.

## Object HSplit (& VSplit)

A Tag object to use "SplitJS" (currently only in horizontal form)

```python
import htagui as u
self <= u.HSplit( Tag.div(1), Tag.div(2), sizes=[60,40], minSize=100, _style="border:2px solid red;height:100px" )
```

## utilities methods

### hflex & vflex

Methods to create an HBox or VBox htag class (flexbox horizontal or vertical, with nowrap mode)

```python
import htagui as u
HBox = u.hflex(50, 50)  # create a hbox of 2 elements of 50% each
self <= HBox( Tag.div(1), Tag.div(2) )
```
