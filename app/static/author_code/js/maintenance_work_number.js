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

$('button#action').on('click', function(e) {
    // デフォルトのPOST動作をストップ
    e.preventDefault();
    // jquery-loading-overlay の実行
    var target = $('div#result')
    // ajax
    var csrf_token = getCookie('csrftoken');
    $.ajax({
        'url': recalculation_url,
        'type': 'POST',
        'dataType': 'json',
        beforeSend: function (xhr, settings) {
            if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
                xhr.setRequestHeader("X-CSRFToken", csrf_token);
            }
        },
    }).done(function (response) {
        var task_id = response.task_id;
        var max_count = response.max_count;
        target.LoadingOverlay("show", {
            image: "",
            progress: true,
            text: "calculating...",
            progressMax: max_count,
        });
        var interval = setInterval(function(){
            fetch(task_url + task_id).then(response => {
                return response.json();
            }).then(response => {
                console.log(response.state)
                if (response.state == 'SUCCESS') {
                    target.LoadingOverlay("hide");
                    clearInterval(interval)
                } else if (response.state == 'FAILURE') {
                    target.LoadingOverlay("hide");
                    clearInterval(interval)
                } else {
                    let count = response.counter;
                    console.log(count)
                    console.log(count / max_count)
                    target.LoadingOverlay("text", String(Math.round((count / max_count) * 100)) + '%');
                    target.LoadingOverlay("progress", count);
                }
            });
        }, 1000);
    });
});