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

        console.log(definitionElements);

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
            });
    })

});