// ===========================================================================
// eXe
// Copyright 2004-2005, University of Auckland
// Copyright 2004-2008 eXe Project, http://eXeLearning.org/
//
// This program is free software; you can redistribute it and/or modify
// it under the terms of the GNU General Public License as published by
// the Free Software Foundation; either version 2 of the License, or
// (at your option) any later version.
//
// This program is distributed in the hope that it will be useful,
// but WITHOUT ANY WARRANTY; without even the implied warranty of
// MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
// GNU General Public License for more details.
//
// You should have received a copy of the GNU General Public License
// along with this program; if not, write to the Free Software
// Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA
// ===========================================================================



define(['jquery', 'wamp_handler', 'jquery-form', 'jquery-pjax', 'jquery-jsonrpc', 'jquery-cookie'],
    function ($, wamp_handler) {
        "use strict";
        // Strings to be translated
        var SELECT_AN_IMAGE = "Select an image";
        var IMAGE_FILES = "Image Files (.jpg, .jpeg, .png, .gif)";
        var JPEG_FILES = "JPEG Files (.jpg, .jpeg)";
        var SELECT_A_FILE = "Select a file";
        var FLASH_MOVIE = "Flash Movie (.flv)";
        var FLASH_OBJECT = "Flash Object (.swf)";
        var SELECT_AN_MP3_FILE = "Select an mp3 file";
        var SELECT_AN_TEX_FILE = "Select an TeX file";
        var TEX_FILE = "TeX File"
        var MP3_AUDIO = "MP3 Audio (.mp3)";
        var PDF = "PDF Files (.pdf)";
        var SELECT_A_PDF = "Select a pdf file";
        var SHOCKWAVE_FILES = "Shockwave Director Files (.dcr)"
        var QUICKTIME_FILES = "Quicktime Files (.mov, .qt, .mpg, .mp3, .mp4, .mpeg)"
        var WINDOWSMEDIA_FILES = "Windows Media Player Files (.avi, .wmv, .wm, .asf, .asx, .wmx, .wvx)"
        var REALMEDIA_AUDIO = "RealMedia Audio Files (.rm, .ra, .ram, .mp3)"
        var SELECT_KPSE = "Select kpsewhich"
        var SELECT_A_PACKAGE = "Select a package";
        var YOUR_SCORE_IS = "Your score is ";

        var exports = {
            initialize_authoring: function () {
                // initialize uninitialized editors
                $(".idevice_form textarea").each(function () {
                    if ($(this).css("visibility") == "hidden") return;
                    CKEDITOR.replace($(this).attr("id"), {'customConfig': '/exeapp/ckeditor_config/'});
                });
                //$(".action_button").bind("click", handle_action_button)
                $(".idevice_form").ajaxForm({
                    success: function (responseText, statusText, xhr, $form) {
                        var idevice_id = $form.attr("idevice_id");
                        exports.scroll_to_element($form);
                        $form.find("textarea").each(function () {
                            var editor = CKEDITOR.instances[$(this).attr("id")];
                            if (editor) { editor.destroy(true); }
                        });
                        if (responseText) {
                            exports.get_media("authoring/?idevice_id=" + idevice_id + "&media=true");
                            $form.html(responseText);
                            $form.find("textarea").each(function () {
                                CKEDITOR.replace($(this).attr("id"), {'customConfig': '/exeapp/ckeditor_config/'});
                            });
                            MathJax.Hub.Typeset();
                        } else {
                            exports.reload_authoring();
                        }
                        exports.bind_wamp();
                    },
                    beforeSerialize: function () {
                        for (var x in CKEDITOR.instances)
                           CKEDITOR.instances[x].updateElement();
                    },
                    beforeSubmit: function (arr, $form, opts) {
                        for (var i = 0; i < arr.length; i++) {
                            var el = arr[i];
                            if (el.name == "idevice_action") {
                                if (el.value == "delete") {
                                    exports.ask_idevice_delete_confirmation($form, opts);
                                    return false;
                                } else {
                                    return true;
                                }
                            }
                        }
                        return true;
                    }
                });
                MathJax.Hub.Typeset();
                exports.get_media("authoring/?partial=true&media=true");
                exports.bind_wamp();
            },

            bind_wamp: function () {
                $("input[name='idevice_action']").off("click").on("click", function () {
                    var connection = wamp_handler.create_connection();
                    connection.onopen = function (session) {
                        var idevice_id = $(_this).parents(".idevice_form").attr("idevice_id");
                        if ($(_this).val() == "edit_mode") {
                            var status = "edited";
                        } else {
                            var status = "preview";
                        }
                        session.publish(
                            "com.dautobahn.idevice_changed",
                            [JSON.stringify({'idevice_id': idevice_id, 'status': status})]
                        )
                    }
                    connection.open();
                })
            },

            ask_idevice_delete_confirmation: function ($form, opts) {
                exports.ask_delete_confirmation("this iDevice", function () {
                    $.modal.close();
                    opts.data = {idevice_action: "delete"};
                    $form.ajaxSubmit(opts);
                });
            },

            ask_delete_confirmation: function (name, callback) {
                var modal = $("#confirm_removal");
                var yes = modal.find(".btnyes");
                var no = modal.find(".btnno");
                var nodename = modal.find("#removenode");
                nodename.text("this iDevice");
                modal.modal();
                no.focus();
                yes.off("click").on("click", function () {
                    callback();
                })
                no.off("click").click(function () {
                    $.modal.close();
                });
            },

            init: function () {

                jQuery(document).ready(function () {
                    $(document).on("pjax:success", function (event, data) {
                        exports.initialize_authoring();
                    });
                    $(document).on("pjax:popstate", function (event) {
                        var current_url = event.state.url;
                        var current_node_id = current_url.match(/.*\/(\d+)\//)[1]
                        exports.get_outline_pane().jstree("select_node", "#node" + current_node_id, true);
                    });
                    $.jsonRPC.setup({
                        endPoint: '/exeapp/json/',
                        namespace: 'package'
                    });
                    exports.initialize_authoring();
                })
            },

            scroll_to_element: function (element) {
                var middle_row = $("#middle-row");
                var middle_row_pos = middle_row.offset().top;
                var offset = element.offset().top - middle_row_pos;

                if (offset + element.innerHeight() > middle_row.height()) {
                    // Not in view so scroll to it
                    $('#middle-row').animate({scrollTop: offset}, 1000);
                } else if (offset < 0) {
                    $('#middle-row').animate({scrollTop: middle_row.scrollTop() + offset - 100}, 1000);
                }
            },

            get_outline_pane: function () {
                return $("#outline_pane");
            },

            get_current_node: function () {
                var selected = exports.get_outline_pane().jstree("get_selected").find(">a");
                return selected;
            },

            get_current_node_id: function () {
                var node = exports.get_current_node();
                return node.attr('id').match(/node(\d+)/)[1]
            },

            reload_authoring: function () {
                var url = "/exeapp/package/" + exports.get_package_id() + "/" + exports.get_current_node_id() + "/";
                $("#authoring").load(url, function () {
                    exports.initialize_authoring();
                });
            },

            get_media: function (request_url) {
                $.ajax({
                    url: request_url,
                    dataType: 'json',
                    async: false,
                    success: function (data) {
                        $.each(data['css'], function (key, val) {
                            if (!($("link[href='" + val + "']")).length > 0) {
                                $('<link rel="stylesheet" href="' + val + '">')
                                    .appendTo("head");
                            }
                        });
                        $.each(data['js_modules'], function (key, module_name) {
                            requirejs([module_name], function (module) {
                                module.init();
                            })
                        })
                    }});
            },

            insert_idevice: function (idevice_id) {
                $.ajax({
                    url: "authoring/?idevice_id=" + idevice_id,
                    dataType: 'html',
                    success: function (data) {
                        $('#authoring').append(data);
                        exports.initialize_authoring();
                        var element = $('#authoring').children().last();
                        exports.scroll_to_element(element);
                    }
                });
            },

            insert_idevice_in_position: function (idevice_id, pos) {
                $.ajax({
                    url: "authoring/?idevice_id=" + idevice_id,
                    dataType: 'html',
                    success: function (data) {
                        $('#authoring').eq(pos).before(data);
                        exports.initialize_authoring();
                        var element = $('#authoring').children().eq(pos);
                        exports.scroll_to_element(element);
                    }
                });
            },


            // Takes a jQuery object and returns the id of the idevice it
            // belongs to
            get_idevice_id: function (obj) {
                re_idevice_id = /idevice(\d*)/;
                return re_idevice_id.exec(get_idevice(obj).attr("id"))[1];
            },

            // Takes a jQuery object and returns it's idevice block
            get_idevice: function (obj) {
                return obj.closest(".block");
            },

            get_package_id: function () {
                return $("#package_id").text()
            },

            // Returns a dictionary of all elements of the idevice with non-empty
            // values.
            get_arguments: function (idevice_block) {
                var args = {};
                idevice_block.find(":input").each(function () {
                    // Don't post elements without name
                    if ($(this).attr("name") != undefined) {
                        args[$(this).attr("name")] = $(this).val();
                    }
                });
                return args;
            },

            update_preview: function () {
                var url = window.location.protocol + '//' + location.host + location.pathname;
                $('#previewIFrame').find('iframe').attr('src', url + "preview/");
            }
        };
        return exports;
    });
