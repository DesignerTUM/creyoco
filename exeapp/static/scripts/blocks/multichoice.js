var multichoice = {
    init: function () {
        "use strict";
        $(document).ready(function () {
            $(".check_multichoice").off("click").on("click", function (e) {
                var $this = $(this);
                var result_el = $(this).parent().find(".mc-result");
                if (!multichoice.checkCorectness($this)) {
                    result_el.removeClass("mc-right")
                        .addClass("mc-wrong")
                        .text("Incorrect answer!");
                    return false;
                } else {
                    result_el.removeClass("mc-wrong")
                        .addClass("mc-right")
                        .text("Correct!");
                }
            });
            $(".show_answers_multiplechoice").off("click").on("click", function (e) {
                multichoice.show_answers($(this));
            })
            $(".reset_multichoice").off('click').on('click', function(e) {
                multichoice.reset($(this));
            })
        });
    },
    show_answers: function ($this) {
        this.reset($this);
        var options = $this.parent().find("input[type='radio'], input[type='checkbox']");
        $this.parent().find(".mc-feedback").remove();
        $.each(options, function (n, el) {
            $(el).parent()
                .removeClass("wrong_answer")
                .removeClass("right_answer");
            if ($(el).attr("data-right") === "true") {
                $(el).parent().addClass('right_answer');
                if (!($(el).prop("checked"))) {
                    multichoice.show_feedback($(el));
                }
            } else {
                if ($(el).prop("checked")) {
                    multichoice.show_feedback($(el));
                    $(el).parent().addClass('wrong_answer');
                }
            }
        });
    },
    checkCorectness: function ($this) {
        var options = $this.parent().find("input[type='radio'], input[type='checkbox']");
        var correct = true;
        $this.parent().find(".mc-feedback").remove();
        $.each(options, function (n, el) {
            if ($(el).attr("data-right") === "true") {
                if (!($(el).prop("checked"))) {
                    correct = false;

                }
            } else {
                if ($(el).prop("checked")) {
                    correct = false;
                    multichoice.show_feedback($(el));
                }
            }
        });
        return correct;
    },
    show_feedback: function ($el) {
        $("<p />")
            .html($el.attr("data-feedback"))
            .addClass("mc-feedback")
            .appendTo($el.parent());
    },
    reset: function($this) {
        $this.parent().find('.right_answer').removeClass('right_answer');
        $this.parent().find('.wrong_answer').removeClass('wrong_answer');
        $this.parent().find('.mc-feedback').remove();
        $this.parent().find('.mc-result')
            .removeClass('right')
            .removeClass('wrong')
            .html('');

    }
};

if (typeof(requirejs) !== "undefined") {
    define("multichoice", ['jquery'], function ($) {
        return multichoice;
    })
} else {
    multichoice.init();
}
