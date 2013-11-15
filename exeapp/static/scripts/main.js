require.config({
    baseUrl: '/static/scripts/',
    paths: {
        "jquery": "bower_components/jquery/jquery",
        "eventEmitter": "bower_components/eventEmitter",
        "eventie": "bower_components/eventie",
        "chosen": "thirdparty/chosen.jquery",
        "imagesloaded": "bower_components/imagesloaded/imagesloaded",
        "jquery-pjax": "bower_components/jquery-pjax/jquery.pjax",
        "jquery-cookie": "bower_components/jquery.cookie/jquery.cookie",
        "qtip2": "//cdnjs.cloudflare.com/ajax/libs/qtip2/2.1.1/jquery.qtip.min",
        "jquery-jsonrpc": "thirdparty/jquery.jsonrpc",
        "jquery-form": "bower_components/jquery-form/jquery.form",
        "jquery-modal": "bower_components/jquery-modal/jquery.modal",
        "jstree": "bower_components/jstree-dist/jquery.jstree",
        "feedback": "widgets/feedback",
        "multichoice": "blocks/multichoice"
    },

    shim: {
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
