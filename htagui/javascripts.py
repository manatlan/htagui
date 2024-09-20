# -*- coding: utf-8 -*-
# #############################################################################
# Copyright (C) 2024 manatlan manatlan[at]gmail(dot)com
#
# MIT licence
#
# https://github.com/manatlan/htag
# #############################################################################
from htag import Tag

""" will contains some htag placeholder objects, to just add some JS at import """


class JSKEYABLE(Tag):
    statics = [Tag.script("""function keyable(o) {
    o.onkeydown = function(e) {
        const ll = [...o.querySelectorAll(".keyable")];

        function calcOffset() {
            let hh={};
            for(let i of ll) {
                const h=i.getBoundingClientRect().top;
                hh[h]=(!hh[h]) ? 1 : hh[h]+1;
            }
            return Math.max( ...Object.values(hh) );
        }
        
        const current=document.activeElement;
        if(ll.indexOf(current)>=0) {
            let idx=ll.indexOf(current);
            if(e['key']=="ArrowLeft") {
                idx = (idx - 1 >= 0) ? idx-1 : 0;
                ll[idx].focus();
                e.preventDefault();
            }
            else if(e['key']=="ArrowRight") {
                idx = (idx + 1 < ll.length) ? idx+1 : ll.length-1;
                ll[idx].focus();
                e.preventDefault();
            }
            else if(e['key']=="ArrowUp") {
                const offset = calcOffset();
                idx = (idx - offset >= 0) ? idx-offset : 0;
                ll[idx].focus();
                e.preventDefault();
            }
            else if(e['key']=="ArrowDown") {
                const offset = calcOffset();
                idx = (idx + offset < ll.length) ? idx+offset : ll.length-1;
                ll[idx].focus();
                e.preventDefault();
            }
            else if(e['key']=="Enter" ) {
                ll[idx].click();
                e.preventDefault();
            }
        }
    }    
        
    const ll = [...o.querySelectorAll(".keyable")];
    if(ll) {
        for(const i of ll)
            i.setAttribute("tabindex",1)
        ll[0].focus();
    }
    else
        console.warn( "keyable(element):", "No child elements with 'keyable' class in", o )
}
""")]