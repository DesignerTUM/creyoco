exports = {
    init: function () {
        $(document).ready(function () {
            $(".cloze_submit").off("click").on("click", submit_cloze);
            $(".cloze_restart").off("click").on("click", function (e) {
                $(this).parent().hide();
                $(this).parent().parent()
                    .find(".cloze_gap").each(function () {
                        $(this).val("");
                        $(this).css("backgroundColor", "white");
                    });
                e.preventDefault();
            });
            $(".cloze_show_answers").off("click").on("click", function (e) {
                $(this).parent().parent().find(".cloze_gap").each(function () {
                    $(this).val(get_right_answer($(this)));
                    $(this).css("backgroundColor", "green");
                });
                e.preventDefault();
            });
        });

        function submit_cloze(e) {
            var gap_count = 0;
            var right_answer_count = 0;
            $(this).parent().find(".cloze_gap").each(function () {
                gap_count++;
                var gap_id = /gap_(.*)$/.exec($(this).attr("id"))[1];
                var right_answer = get_right_answer($(this));
                if ($(this).val() == right_answer) {
                    $(this).css("backgroundColor", "green");
                    right_answer_count++;
                }
                else {
                    $(this).css("backgroundColor", "red");
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
            return $gap.parent().parent().find("#answer_" + gap_id).val();
        }
    }
}

if (typeof(requirejs) !== "undefined") {
    define("cloze", ['jquery'], function ($) {
        return exports;
    })
} else {
    exports.init();
}
