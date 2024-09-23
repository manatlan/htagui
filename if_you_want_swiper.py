from htag import Tag,expose,Runner
from htagui import shoelace as ui

DOC = """Versions 0.6.1 to 0.6.4 provided an object ui.Swiper(). But it was a bad idea ;-)
So it was removed for versions > 0.6.4, because it's easy (using shoelace) to provide
this kind of component... Here is an example, which provide exactly the same features.
"""

class SLSwiper(Tag.sl_carousel): 
    def init(self,ll:list,default=0,**a):
        isAllRealTags = all([isinstance(i,Tag) for i in ll])
        self["mouse-dragging"]=True
        self["--slide-gap"]="30px"
        self["pagination"]=True
        self["navigation"]=True

        if isAllRealTags:
            for i in ll:
                self <= Tag.sl_carousel_item() <= i
            self.js=""
        else:
            for idx,i in enumerate(ll):
                self <= Tag.sl_carousel_item( ui.Spinner(), create=i)
            self._activate(default)
            self.js = """self.addEventListener('sl-slide-change', function (e) {self._activate( e.detail.index ) });"""

        self.js+="""
        if(self.goToSlide)
            self.goToSlide(%s);
        else
            window.customElements.whenDefined('sl-carousel').then( function() {
                self.goToSlide(%s);
            });
        """ % (default,default)
    
    @expose
    def _activate(self,idx):
        if self.childs[idx].create:
            self.childs[idx].clear( self.childs[idx].create() ) 
            self.childs[idx].create=None



class App(Tag.div):
    def init(self):

        class Item(Tag.img):
            def init(self,i):
                self["src"]=f"https://loremflickr.com/400/400/colors?random={i}"

        self<= Tag.h3("""A swipper (using shoelace)""")
        self<= Tag.p(DOC)

        self<= Tag.b("A static use:")
        self<= SLSwiper([Item(i) for i in range(50)],_style="height:300px")
        
        self<= Tag.b("A dynamic use (tags created on-demand):")
        self<= SLSwiper([lambda i=i: Item(i) for i in range(50)],_style="height:300px")


if __name__ == "__main__":
    Runner(App).run()