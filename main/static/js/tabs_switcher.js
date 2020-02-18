/**** JQuery *******/
jQuery('body').on('click', '.next-tab', function () {
    var next = jQuery('.nav-tabs > .active').next('li');
    if (next.length) {
        next.find('a').trigger('click');
    } else {
        jQuery('#question-tabs--ul a:first').tab('show');
    }
});

jQuery('body').on('click', '.previous-tab', function () {
    var prev = jQuery('.nav-tabs > .active').prev('li')
    if (prev.length) {
        prev.find('a').trigger('click');
    } else {
        jQuery('#question-tabs--ul a:last').tab('show');
    }
});

var Quiz = {
    answers: {},
    amount: 0
};

$(window).ready(function () {

    $.ajaxSetup({
        beforeSend: function (xhr) {
            xhr.setRequestHeader("X-CSRFToken", app.csrf_token);
        }
    });

    Quiz.amount = $('.d-word').length;

    $(".answer").on("click", function () {
        $(this).parent().find('.answer').removeClass('active');
        $(this).addClass('active');

        var key = $(this).parent().parent().attr('data-id');

        var term = $(this).parent().find('.term').text();

        Quiz.answers[term] = $(this).text();

        console.log($(this).text());
    });
    $(".finish").on("click", function () {
        $.ajax("/check/answers/", {
            method: 'POST',
            data: {
                answers: JSON.stringify(Quiz.answers),
                dictation_id: dictation.id
            }
        })
            .done((res) => {
                console.log(res);
            });
    })
});