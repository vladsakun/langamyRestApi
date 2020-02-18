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

    var termElements = document.getElementsByClassName("term");

    for (var i = 0; i < termElements.length; i++) {

        Quiz.answers[termElements[i].textContent] = "empty";

    }

    $(".answer").on("click", function () {
        $(this).parent().find('.answer').removeClass('active');
        $(this).addClass('active');

        var key = $(this).parent().parent().attr('data-id');

        var term = $(this).parent().parent().find('.term').text();

        Quiz.answers[term] = $(this).text();

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
                var mark = res.data.mark;
                var questionDiv = $('#quiz-questions--div');
                var questionDivHeight = questionDiv.height();
                questionDiv.height(questionDivHeight);
                $("#question-info--div").fadeOut("slow", function () {
                    questionDiv.html('<div id="result--div">' + mark +
                        '/' + Quiz.amount + ' </div>');

                });
            });
    })

});