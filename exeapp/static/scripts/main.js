require.config({
    baseUrl: '/static/scripts/',
    paths: {
        "jquery": "bower_components/jquery/jquery",
        "modernizr": "bower_components/modernizr/modernizr",
        "eventEmitter": "bower_components/eventEmitter",
        "eventie": "bower_components/eventie",
        "chosen": "thirdparty/chosen.jquery",
        "imagesloaded": "bower_components/imagesloaded/imagesloaded",
        "jquery-pjax": "bower_components/jquery-pjax/jquery.pjax",
        "jquery-cookie": "bower_components/jquery.cookie/jquery.cookie",
        "qtip2": "bower_components/qtip2/jquery.qtip",
        "jquery-jsonrpc": "thirdparty/jquery.jsonrpc",
        "jquery-form": "bower_components/jquery-form/jquery.form",
        "jquery-modal": "bower_components/jquery-modal/jquery.modal",
        "jstree": "bower_components/jstree-dist/jquery.jstree",
        "filebrowser": "../filebrowser/js/AddFileBrowser",
        "feedback": "widgets/feedback",
        "cloze": "widgets/cloze",
        "multichoice": "blocks/multichoice",
        "autobahn": "thirdparty/autobahn.min",
        "wamp_handler": "wamp_handler",
        "jquery-ui": "thirdparty/jquery-ui.min",
        "dragula": "thirdparty/dragula/dragula"
    },

    shim: {
        "jquery-ui": {
            "deps": ['jquery'],
            "exports": ["jQuery.fn.draggable", "jQuery.fn.droppable"]
        },
        "jquery-jsonrpc": {
            "deps": ['jquery'],
            "exports": "jQuery.fn.jsonrpc"
        },
        "jquery-cookie": {
            "deps": ['jquery'],
            "exports": "jQuery.fn.cookie"
        },
        "jquery-pjax": {
            "deps": ['jquery']
        },
        "jquery-form": {
            "deps": ['jquery'],
            "exports": "jQuery.fn.form"
        },
        "jquery-modal": {
            "deps": ['jquery'],
            "exports": "jQuery.fn.modal"
        },
        "jstree": {
            "deps": ['jquery'],
            "exports": "jQuery.fn.jstree"
        },
        "chosen": {
            "deps": ['jquery'],
            "exports": "jQuery.fn.chosen"
        }
    },

    packages: [
        {
            name: 'cs',
            location: 'bower_components/require-cs',
            main: 'cs'
        },
        {
            name: "coffee-script",
            location: 'bower_components/coffee-script',
            main: 'index'
        }
    ]
});

require(["mainpage"]);
