require.config({
    baseUrl: '/static/scripts/',
    paths: {
        "jquery": "bower_components/jquery/jquery",
        "jquery-jsonrpc": "thirdparty/jquery.jsonrpc",
        "chosen": "thirdparty/chosen.jquery",
        "qtip2": "bower_components/qtip2/jquery.qtip",
        "jquery-modal": "bower_components/jquery-modal/jquery.modal",
        "jquery-form": "bower_components/jquery-form/jquery.form",
        "jquery-pjax": "bower_components/jquery-pjax/jquery.pjax",
        "jquery-cookie": "bower_components/jquery.cookie/jquery.cookie",
        "autobahn": "thirdparty/autobahn.min"
    },
    shim: {
        "jquery-jsonrpc": {
            "deps": ['jquery'],
            "exports": "jQuery.fn.jsonrpc"
        },
        "jquery-modal": {
            "deps": ['jquery'],
            "exports": "jQuery.fn.modal"
        },
        "chosen": {
            "deps": ['jquery'],
            "exports": "jQuery.fn.chosen"
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
        }
    }
});

require(['jquery', 'jquery-jsonrpc', 'eyecandy'], function($, _, eyecandy) {

    $(document).ready(function() {
        // fade out the error message
        $('#error_messages').delay(5000).fadeOut();

        $('#middle-row').on("click", ".check", function() {
            if($(this).parent().parent().hasClass('active')) {
                $(this).removeClass('icon-check');
                $(this).addClass('icon-check-empty');
                $(this).parent().parent().removeClass('active');
            }
            else {
                $(this).removeClass('icon-check-empty');
                $(this).addClass('icon-check');
                $(this).parent().parent().addClass('active');
            }

            if($('li').hasClass('active')) {
                $("#delete_selected_packages").show();
                $("#duplicate_selected_packages").show();
            }
            else {
                $("#delete_selected_packages").hide();
                $("#duplicate_selected_packages").hide();
            }
        });


        $.jsonRPC.setup({
        endPoint: '/exeapp/json/',
        namespace: 'main'
      });
      $("#create_package").click(create_package);
      $("#delete_selected_packages").click(delete_selected_packages);
      $("#duplicate_selected_packages").click(duplicate_selected_packages);
      $("#import_package").click(import_package);

        $('#middle-row').on("click", ".icon-download", function() {
            var packageid = $(this).parent().parent().attr('packageid');
            $('#download_box a').each(function() {
                $(this).attr('href', '/exeapp/package/' + packageid + '/download/' + $(this).attr("data-exporttype") + '/');
            });

            eyecandy.show_lightbox(365, 200, $('#download_box'));
        });

        $('#middle-row').on("click", ".icon-eye-open", function() {
            var packageid = $(this).parent().parent().attr('packageid');
            $('#previewIFrame >iframe').attr('src', '/exeapp/package/' + packageid + '/preview');
            eyecandy.show_lightbox( $( window ).width()-100, $( window ).height()-100, $('#previewIFrame'));  

            //console.log(w + ',' + h);
        });
    })

    // Promps a new package new and sens a "main.create_package" call via
    // rpc
    function create_package(){
      var package_title = prompt('Enter package title');
        $.jsonRPC.request('create_package', {
            params: [package_title],
            success: function(results){
            callback_create_package(results.result.id, results.result.title)
          }
        });
    }
    function import_package(){
        eyecandy.show_lightbox(365, 200, $('#importZip'));
    }

    // Deletes packages which idicated by selected checkboxes
    function delete_selected_packages(){
      $(".active").
      each(function (i){
        var package_id = $(this).attr("packageid");
              $.jsonRPC.request('delete_package', {
                  params: [package_id],
                  success: function (results) {
                      var deleted_package_id = results.result.package_id;
              if (deleted_package_id > 0) {
                // Just a pre-caution that we remove the same package as the
                // server
              callback_delete_package(deleted_package_id);
            }
          }
        })
      })
       $("#delete_selected_packages").hide();
        $("#duplicate_selected_packages").hide();
    }

    // Duplicates packages indicated by selected checkboxes
    function duplicate_selected_packages(){
      $(".active").
      each(function (i){
        var package_id = $(this).attr("packageid");
        $.jsonRPC.request('duplicate_package', {
            params: [package_id],
            success: function(results){
                callback_create_package(results.result.id, results.result.title)
          }
        })
      })

        $('#middle-row #package_list li.active').removeClass('active');
        if($('#middle-row #package_list li span .check').hasClass('icon-check'))
        {
            $('#middle-row #package_list li span .check').removeClass('icon-check');
            $('#middle-row #package_list li span .check').addClass('icon-check-empty');
        }



       $("#delete_selected_packages").hide();
       $("#duplicate_selected_packages").hide();
    }

    // Called after successful package creation

    function callback_create_package(id, title){
        $("<li />").addClass('package').attr("id", "package" + id).attr('packageid', id).append(
            '<span id="" style="display:block;float:left">\
                <i class="check icon-check-empty"></i>\
                <a href="exeapp/package/'+ id + '">' + title + '</a>\
            </span>\
            <span class="qs">\
                <i class="icon-eye-open" ></i>\
                <i class="icon-pencil"></i>\
                <i class="icon-download"></i>\
                <i class="icon-cog"></i>\
            </span>'
        ).appendTo('#package_list');

    }
    // Called after successful package deletion
    function callback_delete_package(id) {
      var package_li = $("#package" + id);
      package_li.remove();
    }

        function download_box() {
            /*var bla = $(this).parent().parent().attr('packageid');
            $('#download_box a').each(function() {
                $(this).attr('href', '/exeapp/package/' + bla + $(this).attr('href'));
            });

            $('#download_box').show();
            $('.modal-dialog iframe').hide();
            lightbox(365, 200);*/
        }
});
