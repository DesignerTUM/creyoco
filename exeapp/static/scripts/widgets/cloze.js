var cloze = {
    init: function () {
        "use strict";
        function submit_cloze(e) {
            var gap_count = 0;
            var right_answer_count = 0;
            $(this).parents(".iDevice").find(".cloze_gap").each(function () {
                gap_count++;
                var right_answer = get_right_answer($(this));
                $(this).removeClass("cloze_right cloze_wrong");
                if ($(this).text().toUpperCase() == right_answer.toUpperCase()) {
                    $(this).addClass("cloze_right");
                    right_answer_count++;
                }
                else {
                    $(this).addClass("cloze_wrong");
                }
            });
            var result_string = "Your score is " + right_answer_count + "/" + gap_count + ".";
            $(this).next().find(".cloze_result_text").text(result_string);
            $(this).next(".cloze_result").show();
            e.preventDefault();
            return false;
        }

        function get_right_answer($gap) {
            var gap_id = /gap_(.*)$/.exec($gap.attr("id"))[1];
            return $gap.parents(".iDevice").find("#answer_" + gap_id).val();
        }

        function shuffle(array) {
            var currentIndex = array.length, temporaryValue, randomIndex;

            // While there remain elements to shuffle...
            while (0 !== currentIndex) {

                // Pick a remaining element...
                randomIndex = Math.floor(Math.random() * currentIndex);
                currentIndex -= 1;

                // And swap it with the current element.
                temporaryValue = array[currentIndex];
                array[currentIndex] = array[randomIndex];
                array[randomIndex] = temporaryValue;
            }

            return array;
        }

        function show_suggestion(elem, answers) {
            if($(elem).hasClass("checked") == false) {
                shuffle(answers);
                var div = document.createElement("div");
                $(div).addClass("drag_n_drop_container");
                div.innerHTML += "<p>Drag and drop suggestions:</p>";
                for (var i = 0; i < answers.length; i++) {
                    var ansDiv = document.createElement("div");
                    $(ansDiv).addClass("drag_n_drop_answer");
                    ansDiv.innerHTML += answers[i].value;
                    div.appendChild(ansDiv);
                }
                $(elem).find(".cloze_submit").before(div);
                $(elem).addClass("checked");
                $(".drag_n_drop_answer").draggable({ revert: true });
            }
        }

        $(document).ready(function () {
            $(".cloze").each(function(){
                var answers = $(this).find(".cloze_answer");
                var drag_n_drop = $(this).nextAll(".drag_n_drop");
                if (answers.length > 0) {
                    if (drag_n_drop.val() == "True") {
                        show_suggestion(this, answers);
                        $(".cloze_gap").prop("contenteditable", false);
                    }
                }
            });

            $(".cloze_gap").droppable({
                accept: ".drag_n_drop_answer",
                hoverClass: "ui-state-hover",
                drop: function( event, ui ) {
                    {
                        $(ui.draggable).hide();
                        $(this).text(ui.draggable.text());
                    }
                }
            })
                .click(function() {
                    var answer = $(this).text();
                    if (answer) {
                      var draggable = $("div.drag_n_drop_answer:contains("+answer+")");
                      $(this).text("");
                      draggable.show();
                    }
                });
            $(".cloze_submit").off("click").on("click", submit_cloze);
            var that = this;
            $(".cloze_restart").off("click").on("click", function (e) {
                $(this).parent().hide();
                $(this).parents(".iDevice")
                    .find(".cloze_gap").each(function () {
                        $(this).text("");
                        $(this).removeClass("cloze_right cloze_wrong");
                    });
                e.preventDefault();
                var drag_n_drop = $(".drag_n_drop_answer");
                if (drag_n_drop.length !== 0) {
                    $("#wrapper").removeClass("checked");
                    $("div.drag_n_drop_answer").show();
                }
            });
            $(".cloze_show_answers").off("click").on("click", function (e) {
                $(this).parents(".iDevice").find(".cloze_gap").each(function () {
                    $(this).text(get_right_answer($(this)));
                    $(this).removeClass("cloze_wrong").addClass("cloze_right");
                });
                e.preventDefault();
            });

        });
    }
}

if (typeof(requirejs) !== "undefined") {
    define("cloze", ['jquery', 'jquery-ui'], function ($) {
        return cloze;
    })
} else {
    cloze.init();
}
