exports = {
    init: function () {
        $(document).ready(function () {
            $(".check_multichoice").off("click").on("click", function (e) {
                var options = $(this).parent().find("input[type='radio'], input[type='checkbox']");
                var wrong = false;
                var result_el = $(this).parent().find(".result");
                $.each(options, function (n, el) {
                    if (($(el).attr("data-right") == "true") != $(el).prop("checked")) {
                        result_el.removeClass("right")
                            .addClass("wrong")
                            .text("Wrong!");
                        wrong = true;
                    }
                });
                if (!wrong) {
                    result_el.removeClass("wrong")
                        .addClass("right")
                        .text("Right!");
                }
                return false;
            });
        });
    }
};

if (typeof(requirejs) !== "undefined") {
    define("multichoice", ['jquery'], function ($) {
        return exports;
    })
} else {
    exports.init();
}
