function checkStatusInterval(ele, interval=3000, maxCount=3) {
    var count = 0;
    var intervalId = null;
    var descriptionEle = $(ele).find('#id-status-description')
    const {checkUrl, checkKey, checkValue} = ele.dataset;
    
    function _checkstatus() {
        if (count > maxCount) {
            clearInterval(intervalId);
            if (descriptionEle) {
                descriptionEle.text(
                    $(ele).data('maxTryMsg')
                );
            }
            return ;
        }

        $.ajax({
            url: checkUrl,
            method: 'GET',
        }).done(function(json) {
            if (json[checkKey] == checkValue) document.location.reload();
            if (descriptionEle) descriptionEle.text(json[checkKey]);
            count++;
            console.log('status check success')
        }).fail(function(xhr, status, errorThrown) {
            console.log('status check fail');
        });
    }
    intervalId = setInterval(_checkstatus, interval);
}


$(document).ready(function() {
    var target = $('#id-status-refresh[data-check-url][data-check-key][data-check-value]');

    if (target.length == 1) checkStatusInterval(target[0]);
})