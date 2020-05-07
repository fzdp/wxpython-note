const Inline = Quill.import('blots/inline');
class MarkerBlot extends Inline {}
MarkerBlot.blotName = 'Marker';
MarkerBlot.className = 'marked';
MarkerBlot.tagName = 'div';
Quill.register(MarkerBlot);

class Searcher {
    constructor(quill) {
        this.quill = quill;
    }

    findAll(keyword) {
        this.removeMark();
        let keywordLength = keyword.length;
        this.getIndexesOf(keyword).forEach(
            index => this.quill.formatText(index, keywordLength, "Marker", true)
        )
    }

    removeMark() {
        this.quill.formatText(0, this.quill.getText().length, 'Marker', false);
    }

    getIndexesOf(keyword) {
        if (keyword == null || keyword === "") {
            return [];
        }
        keyword = keyword.toLowerCase();
        let text = this.quill.getText().toLowerCase();
        let keywordLength = keyword.length;
        let startIndex = 0, curIndex, indexList = [];
        while ((curIndex = text.indexOf(keyword, startIndex)) > -1) {
            indexList.push(curIndex);
            startIndex = curIndex + keywordLength;
        }
        return indexList;
    }
}
