document.addEventListener("DOMContentLoaded", function () {
    tinymce.init({
        selector: '#description',
        menubar: "false",
        plugins: "codesample",
        skin: "oxide-dark",
        content_css: [
            "dark",
            "/static/core/dark_scrollbar.css"
        ],
        toolbar: false,
        readonly: 1,
        statusbar: false,
        height: '100%',
    });
});