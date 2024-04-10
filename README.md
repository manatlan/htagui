# htagUI

HtagUI ... Basic widgets for htag apps

Expose :

## Button

A simple surcharge of Tag.button(...)

## Input

A simple surcharge of Tag.input(...)

## Spinner

A spinner object.

## Select

TODO: ...

## Menu

TODO: ...

## Form

A simple surcharge of Tag.form(...) providing where you can define a callback to call a method wich will receive a python "dict" of all named inputs defined in the form.

## Tabs

TODO: ...

## UI

Expose "Dialog boxes" with methods on the ui instance.

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

## HSplit

A Tag object to use "SplitJS" (currently only in horizontal form)

## utilities

### hflex a vflex

Method to create an HBox or VBox class (flexbox)