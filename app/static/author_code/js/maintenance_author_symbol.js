function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

function csrfSafeMethod(method) {
    // these HTTP methods do not require CSRF protection
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}

$('form.maintenance-form').on('submit', function(e) {
    // デフォルトのPOST動作をストップ
    e.preventDefault();
    // jquery-loading-overlay の実行
    var target = $(this)
    target.LoadingOverlay("show", {
        text: "Merging..."
    });
    // ajax
    var id = $(this).find('input:radio:checked').val()
    var csrf_token = getCookie('csrftoken');
    console.log(recalculation_url)
    $.ajax({
        'url': recalculation_url,
        'type': 'POST',
        'data': {
            'id': id,
        },
        'dataType': 'json',
        beforeSend: function (xhr, settings) {
            if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
                xhr.setRequestHeader("X-CSRFToken", csrf_token);
            }
        },
    }).done(function (response) {
        var task_id = response.task_id;
        console.log(task_url + task_id)
        var interval = setInterval(function(){
            fetch(task_url + task_id).then(response => {
                return response.json();
            }).then(response => {
                console.log(response.state)
                if (response.state == 'SUCCESS') {
                    target.LoadingOverlay("hide");
                    target.remove();
                    console.log('ajax complete')
                    clearInterval(interval)
                } else if (response.state == 'FAILURE') {
                    target.LoadingOverlay("hide");
                    console.log('ajax failed')
                    clearInterval(interval)
                }
            });
        }, 1000);
    });
});