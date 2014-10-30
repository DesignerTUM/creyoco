var protectedfreetext = {
    init: function () {
        "use strict";
        $(document).ready(function () {
            var input = $("#pwd_for_protected_freetext").val();
            var pwd_from_db = "{{self.idevice.password}}";
            console.log(input);
            console.log(pwd_from_db);

        });
    }
};

if (typeof(requirejs) !== "undefined") {
    define("protectedfreetext", ['jquery'], function ($) {
        return protectedfreetext;
    })
} else {
    protectedfreetext.init();
}
