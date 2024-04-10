# -*- coding: utf-8 -*-
# #############################################################################
# Copyright (C) 2024 manatlan manatlan[at]gmail(dot)com
#
# MIT licence
#
# https://github.com/manatlan/htag
# #############################################################################

from htag import Tag

SPLITJS="//cdn.jsdelivr.net/npm/split.js@1.6.5/dist/split.min.js"

class HSplit(Tag.div):
    statics = [
        Tag.script(_src=SPLITJS),
        Tag.style("""
.split {
    display: flex;
    flex-direction: row;
}

.gutter {
    background-color: #eee;
    background-repeat: no-repeat;
    background-position: 50%;
}

.gutter.gutter-horizontal {
    background-image: url('data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAUAAAAeCAYAAADkftS9AAAAIklEQVQoU2M4c+bMfxAGAgYYmwGrIIiDjrELjpo5aiZeMwF+yNnOs5KSvgAAAABJRU5ErkJggg==');
    cursor: col-resize;
}        
        """),
    ]
    def init(self,*objs,sizes=None,minSize=None,**a):
        self["class"].add("split")
        self<=objs
        opts={}
        if sizes: opts["sizes"]=sizes
        if minSize: opts["minSize"]=minSize
        self.js = f"""window.Split( self.children , {opts} ) """

        
# class VSplit(Tag.div):
#     statics = [
#         Tag.script(_src="//cdn.jsdelivr.net/npm/split.js@1.6.5/dist/split.min.js"),
#         Tag.style("""
# .split {
#     display: flex;
#     flex-direction: column;
# }

# .gutter {
#     background-color: #eee;
#     background-repeat: no-repeat;
#     background-position: 50%;
# }

# .gutter.gutter-horizontal {
#     background-image: url('data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAUAAAAeCAYAAADkftS9AAAAIklEQVQoU2M4c+bMfxAGAgYYmwGrIIiDjrELjpo5aiZeMwF+yNnOs5KSvgAAAABJRU5ErkJggg==');
#     cursor: col-resize;
# }        
#         """),
#     ]
#     def init(self,*objs,sizes=None,minSize=None,**a):
#         self["class"]="split"
#         self<=objs
#         opts={}
#         if sizes: opts["sizes"]=sizes
#         if minSize: opts["minSize"]=minSize
#         self.js = f"""window.Split( self.children , {opts} ) """

        
