function readyFn() {
    console.log("Hello World!")

    var delayTimer;
    var API_KEY = "AIzaSyDd_yJ-TyaWGzGNN0DyAC3rZPy9izKkjmQ";

    $('#id_search_term').keyup(function () {
        clearTimeout(delayTimer);
        $('#search_results').text("loading ...")
        delayTimer = setTimeout(function () {
            if ($("#id_search_term").val() === "") {
                $('#search_results').text("")
            }
            else {
                $('#search_results').text("")
                search_term = $("#id_search_term").val();
                var url = `https://www.googleapis.com/youtube/v3/search?part=snippet&maxResults=3&q=${search_term}&key=${API_KEY}`;
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
                                // var html = '<div class="col-sm m-1 text-center">' + embed + '</div>'
                                var html = `<div class="col"><div class="card mb-4 shadow-sm">${embed}<div class="card-body"><div class="card-text">${title}</div><button class="btn-primary">Add</button></div></div></div>`
                                $("#search_results").append(html)
                            });
                        }
                    }
                );
            }
        }, 1000);
    });
}

$(document).ready(readyFn);