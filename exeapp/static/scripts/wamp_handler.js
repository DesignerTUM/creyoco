define(["autobahn"], function(autobahn) {
    "use strict";
    var exports = {
        create_connection: function() {
            return new autobahn.Connection({
                            url: "ws://" + window.location.hostname + ":8080/ws",
                            realm: "creyoco"
                        });

        },
        show_messages: function() {
            var connection = exports.create_connection();
            connection.onopen = function (session) {
                session.subscribe('com.dautobahn.message',
                    function(args, kwargs, details) {
                        var message = args[0];
                        console.log("Message: " + message);
                    })
            }
            connection.open();
        },
        send_message: function(message) {
            var connection = exports.create_connection();
            connection.onopen = function(session) {
                session.publish('com.dautobahn.message', [message]);
                connection.close();
            }
            connection.open()
        },
        listen_to_idevice_changes: function() {
            var connection = exports.create_connection();
            connection.onopen = function(session) {
                session.subscribe('com.dautobahn.idevice_changed',
                    function(args, kwargs, details) {
                        var data = JSON.parse(args[0]);
                        var idevice = $('form[idevice_id='+data.idevice_id+']');
                        if (idevice.length > 0) {
                            if (data.status == "edited") {
                            $("<div />")
                                .addClass("disabled-overlay")
                                .height(idevice.outerHeight())
                                .width(idevice.outerWidth())
                                .css(
                                {
                                    position: "absolute",
                                    top: 0,
                                    left: 0,
                                    'z-index': 100,
                                    background: 'rgba(246, 246, 246, .5)'
                                })
                                .appendTo(idevice);
                            } else if (data.status == "preview") {
                                idevice.find(".disabled-overlay").remove();
                            }
                        }
                    });
            }
            connection.open();
        }
    }
    return exports;
})
