#!/usr/bin/python3 -u
# -*- coding: utf-8 -*-
from htag import Tag,expose

class Form(Tag.form):
    def init(self,onsubmit=lambda dico:dico,**a):
        # rewrite the form.submit() (bicoz this method doesn't call the onsubmit ;-( )
        self.js = """self.submit=function() {self._submit(Object.fromEntries(new FormData( self )))}"""

        self["onsubmit"]="event.preventDefault();this.submit()"
        self.onsubmit = onsubmit

    @expose
    def _submit(self,data:dict):
        self.onsubmit(data)
