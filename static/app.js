$(function () {
    $("#get-outfit").on("click", function () {
        var activity = $("#activity").val();
        var weather = $("#weather").val();

        if (!activity || !weather) {
            $("#results").html("<p class='error'>Please select both an activity and weather.</p>");
            return;
        }

        $("#results").html("<p>Loading...</p>");

        $.getJSON("/api/recommend", { activity: activity, weather: weather })
            .done(function (data) {
                if (!data.items || data.items.length === 0) {
                    $("#results").html("<p>No outfit suggestions found.</p>");
                    return;
                }
                var html = "<h2>Your Outfit</h2><ul>";
                data.items.forEach(function (item) {
                    html += "<li>";
                    if (item.image) {
                        html += "<img src=\"" + item.image + "\" alt=\"" + item.name + "\">";
                    }
                    html += "<div class=\"item-info\"><strong>" + item.name + "</strong></div>";
                    html += "</li>";
                });
                html += "</ul>";
                $("#results").html(html);
            })
            .fail(function (jqXHR) {
                var msg = "Something went wrong.";
                if (jqXHR.responseJSON && jqXHR.responseJSON.error) {
                    msg = jqXHR.responseJSON.error;
                }
                $("#results").html("<p class='error'>" + msg + "</p>");
            });
    });
});
