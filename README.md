# htagUI

HtagUI ... Basic widgets for htag apps

Expose :

## Object Button

A simple surcharge of Tag.button(...)

```python
import htagui as u

self <= u.Button("my button",_class="myclass", _onclick = myevent )
```

## Object Input

A simple surcharge of Tag.input(...)

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

TODO: complete

```python
import htagui as u

self <= u.Select( dict(a="A",b="B"), _value="a", _name="myfield" )
```

## Object Menu

TODO: complete

```python
import htagui as u

ui = u.UI(self)

entries={
    "menu1": lambda: ui.notify("menu1"),
    "menu2": lambda: ui.notify("menu2"),
    "menu3": lambda: ui.notify("menu3"),
}  
self <= u.Menu( entries )
```


## Object Form

A simple surcharge of Tag.form(...) providing where you can define a callback to call a method wich will receive a python "dict" of all named inputs defined in the form.

## Object Tabs

TODO: complete

## Object UI

Expose "Dialog boxes" with methods on the ui instance.

```python
import htagui as u

ui = u.UI( self )
```

### ui.alert(obj)

(like js window.alert(...)) Display a modal dialog box containing the object 'obj' 

### ui.confirm(obj, cbresponse=lambda bool:bool)

(like js window.confirm(...)) Display a modal dialog box containing the object 'obj', and user should ...

### ui.prompt(value:str, title, cbresponse=lambda val:val)

(like js window.prompt(...))

### ui.notify(obj, time=2000)

Display a toast message (notification), in the right-bottom ... during 2000 ms.

### ui.pop(obj, xy:tuple)

Display an object, at coords (x,y).

### ui.drawer(obj, mode="left", size:int=50)

Display a drawer, in the left-side, which takes 50% of the page.

### ui.block(obj=None)

Display a modal dialog box containing the object 'obj'. But the dialog is not closable, so be sure to provide a way to close it.

### ui.close()

Close programatically, the current ui dialog.

## Object HSplit (& VSplit)

A Tag object to use "SplitJS" (currently only in horizontal form)

```python
import htagui as u

self <= u.HSplit( Tag.div(1), Tag.div(2) )
```

## utilities methods

### hflex & vflex

Methods to create an HBox or VBox class (flexbox)

```python
import htagui as u

HBox = u.hflex(50, 50)  # create a hbox of 2 elements of 50%
self <= HBox( Tag.div(1), Tag.div(2) )
```