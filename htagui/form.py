# -*- coding: utf-8 -*-
# #############################################################################
# Copyright (C) 2024 manatlan manatlan[at]gmail(dot)com
#
# MIT licence
#
# https://github.com/manatlan/htag
# #############################################################################

from htag import Tag,expose

class Form(Tag.form):
    def init(self,onsubmit=lambda dico:dico,**a):
        # rewrite the form.submit() (bicoz this method doesn't call the onsubmit ;-( )
        self.js = """self.submit=function() {self._submit(Object.fromEntries(new FormData( self )))}"""

        self["onsubmit"]="event.preventDefault();this.submit()"
        self.onsubmit = onsubmit

    @expose
    async def _submit(self,data:dict):
        return self.onsubmit(data)
