
import pytest
from htag import Tag

def test_hflex_vflex():
    import htagui as ui
    HBox= ui.hflex(50,50)
    assert issubclass(HBox,Tag)

    VBox= ui.vflex(50,50)
    assert issubclass(VBox,Tag)


def test_ui_App(ui=None):
    if not ui:
        import htagui as ui
    x=ui.App()
    assert isinstance( x.ui, ui.Dialog )
    x.ui.alert("yolo")
    assert ">yolo<" in str(x)           # there is a message box in x
    assert "try{interact" in str(x)     # there are js-interaction  in x (to close the box)

    x.ui.close()
    assert ">yolo<" not in str(x)           # there is NO MORE a message box in x
    assert "try{interact" not in str(x)     # there are NO MORE js-interaction  in x (to close the box)

def test_ui_App_bulma():
    import htagui.bulma as ui
    test_ui_App(ui)
    
def test_ui_App_shoelace():
    import htagui.shoelace as ui
    test_ui_App(ui)


if __name__=="__main__":
    test_hflex_vflex()
    test_ui_App()