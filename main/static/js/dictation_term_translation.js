var Dictation = {
    answers: {},
    amount: 0
};

$(window).ready(function () {

    Dictation.amount = $('.d-word').length;

    var termElements = document.getElementsByClassName("term");

    for (var i = 0; i < termElements.length; i++) {

        Dictation.answers[termElements[i].textContent] = "empty";

    }

    $(".finish").on("click", function () {

        var definitionElements = document.getElementsByClassName("definition");

        for (var i = 0; i < definitionElements.length; i++) {

            var element = definitionElements[i];

            Dictation.answers[termElements[i].textContent] = element.value;

        }

        $.ajax("/check/answers/", {
            method: 'POST',
            data: {
                answers: JSON.stringify(Dictation.answers),
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
                        '/' + Dictation.amount + ' </div>');

                });
                var userAnswers = res.data.user_answers;

                var userAnswersTabs = "";
                var userAnswersTabsContent = "";
                var active;
                var status;

                for (var i = 0; i < userAnswers.length; i++) {

                    status = null;

                    if (i === 0) {
                        active = "active";
                    } else {
                        active = "";
                    }

                    status = userAnswers[i]['status'];

                    var userAnswerDiv = "<div class='user-answer-container--div'>" +

                        "<div class='term--div " + status + "'>" + userAnswers[i]['term'] + "</div>" +
                        "<div class='row'>" +

                            "<div class='col-lg-6 col-md-6 col-6 col-sm-6 correct-answer--div'>" +
                                "<div class='answer-bottom--div'>" +

                                    "<p>Correct: </p>" +
                                    "<p>"+ userAnswers[i]['translation'] +"</p>" +

                                "</div>" +

                            "</div>" +

                            "<div class='col-lg-6 col-md-6 col-6 col-sm-6 user-answer--div'>" +
                                "<div class='answer-bottom--div'>" +

                                    "<p>Your answer: </p>" +
                                    "<p>" + userAnswers[i]['user_answer'] + "</p>" +

                                "</div>" +

                            "</div>" +

                        "</div>" +

                        "</div>";


                    numOfAnswer = i;

                    userAnswersTabs += "" +
                        "<li role=\"presentation\" class='" + active + "'>" +

                        "<a class=\"btn btn-sm\" href=\"#answer" + i + "\"" +
                        "   aria-controls=\"answer" + i + "\"" +
                        "   role=\"tab\"" +
                        "   data-toggle=\"tab\">" + ++numOfAnswer + "" +
                        "</a>" +

                        "</li>"

                    userAnswersTabsContent += '' +
                        '<div role="tabpanel" class="d-word tab-pane ' + active + '"' +
                        '                    id="answer' + i + '">' +
                        '                    <div>' + userAnswerDiv +
                        '                    </div>' +
                        '                    <div style="min-height: 4em">' +
                        '                        <button class="btn btn-info previous-tab">previous</button>' +
                        '                        <button class="btn btn-info next-tab">next</button>' +
                        '                    </div>' +
                        '                </div>'

                }

                var userAnswersDiv = "" +
                    "<div id=\"answers--div\" class='row m-1'>\n" +
                    "            <div id=\"answers-nums--div\" class=\"col-lg-12 col-12 col-md-12 col-sm-12\">" +
                    "                <ul class=\"nav nav-tabs\" id=\"answers-tabs--ul\" role=\"tablist\">" +
                    "" + userAnswersTabs +
                    "                </ul>\n" +
                    "            </div>\n" +
                    "            <div class=\"tab-content\" id=\"answers-tabs--div\">" + userAnswersTabsContent +

                    "            </div>" +
                    "        </div>";

                $('#answers-backgroud---div').html(userAnswersDiv);
            });
    })

});