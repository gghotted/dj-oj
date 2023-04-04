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


function alertMssage(message, alert_cls = 'alert-success', time=3000) {
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


function setupLikeBtn() {
    var target = $('.dj-like-btn');
    const disableTime = 500;

    function render(ele) {
        // ele 데이터를 가지고 랜더링
        const liked = $(ele).is('[liked]');
        const count = $(ele).attr('value');

        $(ele).text('좋아요 ' + count);
        if (liked) {
            $(ele).attr('class', 'btn btn-sm btn-primary');
        }
        else {
            $(ele).attr('class', 'btn btn-sm btn-outline-primary');
        }
    }

    function toggle(ele) {
        const liked = $(ele).is('[liked]');
        const curr_val = Number($(ele).attr('value'));

        if (liked) { // cancle
            $(ele).removeAttr('liked');
            $(ele).attr('value', curr_val - 1);
        }
        else {
            $(ele).attr('liked', 'true');
            $(ele).attr('value', curr_val + 1);
        }
    }

    function update(ele) {
        const liked = $(ele).is('[liked]');
        var url = '';
        if (liked) url = $(ele).data('unlikeUrl');
        else       url = $(ele).data('likeUrl');

        $.ajax({
            url: url,
            method: 'post',
            dataType: 'json',
        }).done(function (json) {
            toggle(ele);
            render(ele);
            console.log(json.message);
        }).fail(function (xhr, status, errorThrown) {
            alertMssage('정상적으로 처리되지 않았습니다', 'alert-danger');
        });
    }

    target.each((i, ele) => {render(ele)});
    target.click(function() {
        $(this).attr('disabled', true);
        update(this)
        setTimeout(()=>{$(this).attr('disabled', false)}, disableTime);
    })
}

function setupAPIBtn () {
    $('[role=requestAPI][data-url][data-method]').click(function ({ target }) {
        $(target).attr('disabled', true);

        const { url, method, confirmMessage, redirectUrl } = target.dataset

        if (confirmMessage && !confirm(confirmMessage)) return ;

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
            if (redirectUrl) document.location.href = redirectUrl;
            else if (json.redirect_url) document.location.href = json.redirect_url;
            else {
                setTimeout(function() {
                    $(target).attr('disabled', false);
                }, 3000);
                alertMssage(json.message || '정상적으로 처리되었습니다');
                console.log(json);
            }
        }).fail(function (xhr, status, errorThrown) {
            alertMssage('정상적으로 처리되지 않았습니다', 'alert-danger');
        });
    })
}

$(document).ready(function() {
    setupAPIBtn();
    setupLikeBtn();
})