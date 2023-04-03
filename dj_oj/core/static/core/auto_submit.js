
$(document).ready(function() {
    var target = $('form[data-form-type="autoSubmit"]');

    target.find('input[type=radio], select').change(function() {
        $(target).submit();
    })
});