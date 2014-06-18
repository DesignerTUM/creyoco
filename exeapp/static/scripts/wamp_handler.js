define(["autobahn"], function(autobahn) {
    "use strict";
    var exports = {
        create_connection: function() {
            return new autobahn.Connection({
                            url: "ws://localhost:8080/ws",
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
        }
    }
    return exports;
})
