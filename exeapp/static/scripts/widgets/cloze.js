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
            $(elem).prepend(div);
            $(".drag_n_drop_answer").draggable({
                revert: true,
                cursor: 'move',
            });
        }

        function resetGap($gap) {
            $gap
                .find('div.drag_n_drop_answer')
                .appendTo($gap.parents('.cloze').find('.drag_n_drop_container'));
            $gap.text('');
        }

        $(document).ready(function () {
            $(".cloze").each(function(){
                var answers = $(this).find(".cloze_answer");
                var drag_n_drop = $(this).nextAll(".drag_n_drop");
                if (answers.length > 0) {
                    if (drag_n_drop.val() == "True") {
                        show_suggestion(this, answers);
                        $(".cloze_gap").prop("contenteditable", false);
                        $(".cloze_gap").each(function() {
                            var $this = $(this);
                            if ($this.parent().prop('tagName') === 'TD'
                                && $this.parent().text() === $this.text()) {
                                // the same text means parent has a single element
                                $this.parent().addClass('cloze_single_cell');
                            }
                        })
                    }
                }
            });

            $(".cloze_gap").droppable({
                accept: ".drag_n_drop_answer",
                hoverClass: "ui-state-hover",
                tolerance: "pointer",
                drop: function( event, ui ) {
                    {
                        var $this = $(this);
                        var answer = $this.find('div.drag_n_drop_answer')[0];
                        resetGap($this);

                        $(ui.draggable)
                            .hide()
                            .css({ top: 0, left: 0 })
                            .appendTo($this)
                            .fadeIn(200);
                    }
                }
            })
                .click(function() {
                    resetGap($(this));
                });
            $(".cloze_submit").off("click").on("click", submit_cloze);
            var that = this;
            $(".cloze_restart").off("click").on("click", function (e) {
                e.preventDefault();
                $(this).parent().hide();
                $(this).parents(".iDevice")
                    .find(".cloze_gap").each(function () {
                        var $this = $(this);
                        resetGap($this);
                        $this.removeClass('cloze_right').removeClass('cloze_wrong');
                    });
            });
            $(".cloze_show_answers").off("click").on("click", function (e) {
                $(this).parents(".iDevice").find(".cloze_gap").each(function () {
                    var $this = $(this);
                    resetGap($this);
                    $this.text(get_right_answer($this));
                    $this.removeClass("cloze_wrong").addClass("cloze_right");
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
