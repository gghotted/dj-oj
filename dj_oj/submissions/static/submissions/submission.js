function submission(formId, data) {
    var form = $('#' + formId);
    var contents = form.find('input[name="contents"]');
    contents.val(JSON.stringify(data));
    form.submit();
}