exports = {
    init: function () {
        $(document).ready(function () {
            $(".check_multichoice").off("click").on("click", function (e) {
                var checked = $(this).parent().find("input:checked");
                var wrong = false;
                var result_el = $(this).parent().find(".result");
                $.each(checked, function (n, el) {
                    if ($(el).attr("data-right") != "True") {
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
