$.ajaxSetup({
    beforeSend: function (xhr, settings) {
        function getCookie(name) {
            var cookieValue = null;
            if (document.cookie && document.cookie != '') {
                var cookies = document.cookie.split(';');
                for (var i = 0; i < cookies.length; i++) {
                    var cookie = jQuery.trim(cookies[i]);
                    // Does this cookie string begin with the name we want?
                    if (cookie.substring(0, name.length + 1) == (name + '=')) {
                        cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                        break;
                    }
                }
            }
            return cookieValue;
        }
        if (!(/^http:.*/.test(settings.url) || /^https:.*/.test(settings.url))) {
            // Only send the token to relative URLs i.e. locally.
            xhr.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));
        }
    }
});


function alertMssage(message, alert_cls = 'alert-success', time = 5000) {
    var ele = $('#id-message-alert');

    var alertEle = $(
        `<div class="text-center alert alert-dismissible show mb-0 ${alert_cls}">` +
        `<strong>${message}</strong>` +
        '<button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>' +
        '</div>'
    )
    alertEle.appendTo(ele);
    setTimeout(function () {
        alertEle.remove();
    }, time);
}


$(document).ready(function () {
    $('[role=requestAPI][data-url][data-method]').click(function ({ target }) {
        $(target).attr('disabled', true);

        const { url, method } = target.dataset
        var data = {};
        
        if (target.dataset.getData) {
            var getData = eval(target.dataset.getData);
            data = getData(target);
        }
        data = JSON.stringify(data)

        $.ajax({
            url: url,
            method: method,
            data: data,
            dataType: 'json',
            contentType: 'application/json',
        }).done(function (json) {
            if (json.redirect_url) document.location.href = json.redirect_url;
            else {
                setTimeout(function() {
                    $(target).attr('disabled', false);
                }, 2000);
                alertMssage(json.message || '정상적으로 처리되었습니다');
                console.log(json);
            }
        }).fail(function (xhr, status, errorThrown) {
            alertMssage('정상적으로 처리되지 않았습니다', 'alert-danger');
        });
    })
});