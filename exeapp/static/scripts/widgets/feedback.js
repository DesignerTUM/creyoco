feedback = {
    init: function() {
        $(document).ready(function() {
            $(".toggle_feedback").off("click").on("click", function(e){
                $(this).next(".feedback").toggle();
                return false;
            });
        });
    }
}
if (typeof(requirejs) !== "undefined") {
    define("feedback", ['jquery'], function($) {
        return feedback;
    })} else {
    feedback.init();
}
