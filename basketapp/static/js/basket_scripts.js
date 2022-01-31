window.onload = function () {
    $('.card-body').on('click', 'input[type="number"]', function () {
        var t_href = event.target;
//        console.log (t_href);
        $.ajax({
            url: "/basket/edit/" + t_href.name + "/" + t_href.value + "/",

            success: function (data) {
                $('.card-body').html(data.result);
            },
        });

        event.preventDefault();
    });
}