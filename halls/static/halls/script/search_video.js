function searchVideo() {
    var delayTimer;
    var SEARCH_API_KEY = "AIzaSyDd_yJ-TyaWGzGNN0DyAC3rZPy9izKkjmQ";

    $('#id_search_term').keyup(function () {
        clearTimeout(delayTimer);
        // $('#search_results').text("loading ...")
        $("#loader").toggleClass("loading", true)
        delayTimer = setTimeout(function () {
            $("#loader").toggleClass("loading", true)
            if ($("#id_search_term").val() === "") {
                $('#search_results').text("")
                $("#loader").toggleClass("loading", false)
            }
            else {
                $('#search_results').text("")
                search_term = $("#id_search_term").val();
                var url = `https://www.googleapis.com/youtube/v3/search?part=snippet&maxResults=6&q=${search_term}&key=${SEARCH_API_KEY}`;
                $.ajax(
                    {
                        url: url,
                        dataType: 'json',
                        success: function (data) {
                            // $('#search_results').text(data['items']);
                            result = data['items']
                            result.forEach(video => {
                                var title = video['snippet']['title']
                                var thumbnail = video['snippet']['thumbnails']['default']['url']
                                var id = video['id']['videoId']
                                var embed = `<iframe height="200" src="https://www.youtube.com/embed/${id}" frameborder="0" allow="accelerometer; autoplay; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>`
                                var html = `<div class="col" id="col_${id}"><div class="card mb-4 shadow-sm" id="${id}">${embed}<div class="card-body"><div class="card-text">${title.slice(0, 30)}</div><button type="button" class="btn btn-primary" id="addBtn_${id}">Add</button></div></div></div>`
                                $("#search_results").append(html)

                                $("#addBtn_" + id).click(function () {
                                    $("#urlErrorAlert").text("")
                                    var url = "https://www.youtube.com/watch?v=" + id;
                                    $("#id_url").val(url)
                                    $("#addButton").click()
                                    $("#col_" + id).remove()
                                });
                            });
                        }
                    }
                ).done(function () {
                    $("#loader").toggleClass("loading", false)
                });
            }
        }, 1000);
    });
}


function addVideo() {
    $("#urlErrorAlert").text("")
    var $addVideoForm = $("#addVideo")
    $addVideoForm.submit(function (event) {
        event.preventDefault();
        var formData = $(this).serialize()
        var url = window.location.pathname
        $.ajax(
            {
                url: url,
                method: "POST",
                dataType: "json",
                data: formData,
                success: handleAddVideoSuccess,
                fail: handleAddVideoError,
                statusCode: {
                    422: function (data) {
                        var error = data.responseJSON.error
                        var $urlErrorAlert = $("#urlErrorAlert")
                        $urlErrorAlert.text("")
                        $urlErrorAlert.append(`<div class="alert alert-danger mb-2" role="alert">${error}</div>`)
                    }
                }
            }
        )
    })
}

function handleAddVideoSuccess(data, textStatus, jqXHR) {
    $("#id_url").val("");
    var videoTitle = data.video_title
    var redirectURL = data.redirect_url
    var hallTitle = data.hall_title

    console.log(videoTitle);
    console.log(redirectURL);

    $(".modal-body").text(`Successfully added ${videoTitle} to ${hallTitle}`)
    $("#nextModal").modal("show")

    // document.location.replace(redirectURL)

}

function handleAddVideoError(jqXHR, textStatus, errorThrown) {
    console.log(jqXHR);
    console.log(textStatus);
    console.log(errorThrown);
}

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
};

function csrfSafeMethod(method) {
    // these HTTP methods do not require CSRF protection
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
};

function onReady() {
    var csrftoken = getCookie('csrftoken')
    $.ajaxSetup({
        beforeSend: function(xhr, settings) {
            if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
                xhr.setRequestHeader("X-CSRFToken", csrftoken);
            }
        }
    });
    addVideo();
    searchVideo();
}

$(document).ready(onReady);