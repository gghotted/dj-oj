var editors = {};

document.addEventListener("DOMContentLoaded", function () {
    function initEditor(ele) {
        var tabEle = ele;
        if (!(tabEle.id in editors)) {
            var contentId = tabEle.dataset['bsTarget'];
            var editorEle = $(contentId + '>textarea')[0];
            var readOnly = editorEle.hasAttribute('readonly')
            if (readOnly) readOnly = 'nocursor';
            editors[tabEle.id] = CodeMirror.fromTextArea(editorEle, {
                theme: "base16-dark",
                mode: "python",
                lineNumbers: true,
                indentUnit: 4,
                // indentWithTabs: true,
                readOnly: readOnly,
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

    if ($('#id-stderr').length == 1) {
        editors['id-stderr'] = CodeMirror.fromTextArea($('#id-stderr')[0], {
            theme: "base16-dark",
            mode: null,
            lineNumbers: true,
            indentUnit: 4,
            readOnly: true,
        });
    }
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


function setEditorValue(fromId, toId, mode='sql', readonly='nocursor') {
    var editor = null;

    if (toId in editors) editor = editors[toId]
    else {
        editor = CodeMirror.fromTextArea($('#' + toId)[0], {
            theme: "base16-dark",
            mode: mode,
            lineNumbers: true,
            indentUnit: 4,
            readOnly: readonly,
        });
        editors[toId] = editor
    }
    editor.setValue($('#' + fromId).val());
}