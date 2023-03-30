var editors = {};

document.addEventListener("DOMContentLoaded", function () {
    function initEditor(ele) {
        var tabEle = ele;
        if (!(tabEle.id in editors)) {
            var contentId = tabEle.dataset['bsTarget'];
            var editorEle = $(contentId + '>textarea')[0];
            editors[tabEle.id] = CodeMirror.fromTextArea(editorEle, {
                theme: "base16-dark",
                mode: "python",
                lineNumbers: true,
                indentUnit: 4,
                indentWithTabs: true,
                readOnly: editorEle.hasAttribute('readonly'),
            });
        }
    }

    $('.nav-pills .nav-link').click(function(event) {
        initEditor(event.target);
    });

    $(document).ready(function() {
        $($('.nav-pills .nav-link').get().reverse()).each(function (index, item) {
            item.click();
        })
    })
});


function getEditorData() {
    var data = {};
    for (const [key, editor] of Object.entries(editors)) {
        const fileName = editor.getTextArea().dataset['fileName']
        const contents = editor.getValue();
        data[fileName] = contents;
    }
    return data;
}