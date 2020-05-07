let FontStyle = Quill.import('attributors/style/font');
FontStyle.whitelist = null;
Quill.register(FontStyle, true);

let SizeStyle = Quill.import('attributors/style/size');
SizeStyle.whitelist = null;
Quill.register(SizeStyle, true);

let quill = new Quill('#editor', {
    modules: {
        syntax: true,
        toolbar: false,
    },
    theme: 'snow'
});
let editor = quill.container.firstChild;
let searcher = new Searcher(quill);

quill.is_content_loading = false;

quill.on('selection-change', function(){
    pyOnFormatChanged(quill.getFormat());
});

quill.on('text-change', function(_,__,source){
    if(source === 'api' || quill.is_content_loading) {
        return;
    }
    pyOnContentChanged(editor.innerHTML);
});

quill.loadContent = function(value) {
    quill.is_content_loading = true;
    quill.setContents([]);
    editor.innerHTML = value;
    setTimeout(function () {
        quill.is_content_loading = false;
    },0);
};

quill.findAll = function(keyword) {
    searcher.findAll(keyword);
};