
import pytest
import htagui as ui
from htag import Tag

def test_hflex_vflex():
    HBox= ui.hflex(50,50)
    assert issubclass(HBox,Tag)

    VBox= ui.vflex(50,50)
    assert issubclass(VBox,Tag)


def test_ui_App():
    x=ui.App()
    assert isinstance( x.ui, ui.Dialog )
    x.ui.alert("yolo")
    assert ">yolo<" in str(x)           # there is a message box in x
    assert "try{interact" in str(x)     # there are js-interaction  in x (to close the box)


if __name__=="__main__":
    test_hflex_vflex()
    test_ui_App()