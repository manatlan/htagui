__version__ = "0.0.0" # auto updated

from htag import Tag

########################################################################################
from .bases import Button,Input,Menu,Spinner,Select
########################################################################################
from ..form import Form
from ..tabs import Tabs
from ..dialog import Dialog
from ..splitters import HSplit #VSplit
from ..flex import hflex,vflex  # utilities (Htag contructor methods)

class App(Tag.body):
    _ui=None
    
    @property
    def ui(self):
        if self._ui is None:
            self._ui = Dialog(self)
        return self._ui

ALL=[App,Button,Input,Select,Menu,Spinner,Form,Tabs,Dialog,HSplit]
__all__=["App","Button","Input","Select","Menu","Spinner","Form","Tabs","Dialog","HSplit",      "hflex","vflex", "ALL"]