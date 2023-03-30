function _renderStatus(status) {
    $('#id-status-description').text(status);
}

function _renderResult(json) {
    
}


function _renderServerBusy() {
    $('#id-status-spinner').addClass('d-none');
    $('#id-status-description').text(
        '요청이 많아 처리가 느립니다'
    );
}


function _updateResult(json) {
    if (json.test_status == 'completed') {
        clearInterval(updateResultInterval);
        _renderResult(json);
    }
    else {
        _renderStatus(json.test_status_display);
    }
}


function updateResult() {
    if (intervalCount > maxIntervalCount) {
        clearInterval(updateResultInterval);
        _renderServerBusy();
        return
    }

    const url = $('#id-result').data('apiUrl');
    $.ajax({
        url: url,
        method: 'GET',
    }).done(function(json) {
        _updateResult(json);
        console.log('result updated');
    }).fail(function(xhr, status, errorThrown) {
        console.log('result update fail');
    });

    intervalCount++;
}


var updateResultInterval = null;
var intervalCount = 0
var maxIntervalCount = 5;


$(document).ready(function() {
    updateResultInterval = setInterval(updateResult, 3000);
})