from htag import Tag,expose
import base64

class FileUpload(Tag.input):
    def init(self,onchange=lambda x:x,**a):
        self["type"]="file"
        self["onchange"]="this.fileupload()" # not self here!
        self.onchange=onchange
        self.js=r"""
self.fileupload = function( ) {
    for( let file of this.files ) {
        let reader = new FileReader();
        reader.onload =  e => { this._onchange(file.name, btoa(e.target.result)) };
        reader.readAsBinaryString(file); //reader.readAsText(file);
    }
}"""

    @expose
    def _onchange(self,name:str,content:str):
        return self.onchange(name,base64.b64decode(content))
