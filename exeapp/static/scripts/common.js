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


// Strings to be translated
SELECT_AN_IMAGE = "Select an image";
IMAGE_FILES = "Image Files (.jpg, .jpeg, .png, .gif)";
JPEG_FILES = "JPEG Files (.jpg, .jpeg)";
SELECT_A_FILE = "Select a file";
FLASH_MOVIE = "Flash Movie (.flv)";
FLASH_OBJECT = "Flash Object (.swf)";
SELECT_AN_MP3_FILE = "Select an mp3 file";
SELECT_AN_TEX_FILE = "Select an TeX file";
TEX_FILE = "TeX File"
MP3_AUDIO = "MP3 Audio (.mp3)";
PDF = "PDF Files (.pdf)";
SELECT_A_PDF = "Select a pdf file";
SHOCKWAVE_FILES = "Shockwave Director Files (.dcr)"
QUICKTIME_FILES = "Quicktime Files (.mov, .qt, .mpg, .mp3, .mp4, .mpeg)"
WINDOWSMEDIA_FILES = "Windows Media Player Files (.avi, .wmv, .wm, .asf, .asx, .wmx, .wvx)"
REALMEDIA_AUDIO = "RealMedia Audio Files (.rm, .ra, .ram, .mp3)"
SELECT_KPSE = "Select kpsewhich"


SELECT_A_PACKAGE = "Select a package";
YOUR_SCORE_IS = "Your score is ";

define(['jquery', 'jquery-form', 'jquery-pjax', 'jquery-jsonrpc', 'jquery-cookie'], function ($) {


    var exports = {
        initialize_authoring: function () {

            //$(".action_button").bind("click", handle_action_button)
            $(".idevice_form").ajaxForm({success: function (responseText, statusText, xhr, $form) {
                var idevice_id = $form.attr("idevice_id");
                exports.scroll_to_element($form);
                $form.find("textarea").each(function () {
                    tinyMCE.execCommand("mceRemoveControl", true, $(this).attr("id"));
                });
                if (responseText) {
                    exports.get_media("authoring/?idevice_id=" + idevice_id + "&media=true");
                    $form.html(responseText);
                } else {
                    exports.reload_authoring();
                }
            },
                beforeSerialize: function () {
                    tinyMCE.triggerSave(true, true);
                }
            });
        },

        init: function () {

            jQuery(document).ready(function () {
                $(document).on("pjax:success", function (event, data) {
                    // while (tinyMCE.activeEditor && tinyMCE.activeEditor != "undefined"){
                    // tinyMCE.activeEditor.remove();
                    // }
                    exports.initialize_authoring();
                });
                $(document).on("pjax:popstate", function (event) {
                    var current_url = event.state.url;
                    var current_node_id = current_url.match(/.*\/(\d+)\//)[1]
                    get_outline_pane().jstree("select_node", "#node" + current_node_id, true);
                });
                $.jsonRPC.setup({
                    endPoint: '/exeapp/json/',
                    namespace: 'package'
                });
                exports.initialize_authoring();
                node_id = $("#node_id").text();
            })
        },

        scroll_to_element: function (element) {
            var middle_row = $("#middle-row");
            var middle_row_pos = middle_row.offset().top;
            console.log(middle_row_pos);
            var offset = element.offset().top - middle_row_pos;
            console.log(offset);

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
            node = exports.get_current_node();
            return node.attr('id').match(/node(\d+)/)[1]
        },

        reload_authoring: function () {
            url = "/exeapp/package/" + exports.get_package_id() + "/" + exports.get_current_node_id() + "/";
            $("#authoring").load(url, function () {
                exports.initialize_authoring();
                exports.get_media("authoring/?partial=true&media=true");

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
            // dynamically load scripts for idevices
            exports.get_media("authoring/?idevice_id=" + idevice_id + "&media=true");
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

        // contentForm to the server
        submitLink: function (action, idevice_id, changed, arguments) {
            $.jsonRPC.request("idevice_action", {
                params: [
                    exports.get_package_id(),
                    idevice_id,
                    action,
                    arguments],
                success: reload_authoring
            });

        },
        update_preview: function () {
            var url = window.location.protocol + '//' + location.host + location.pathname;
            $('#previewIFrame').find('iframe').attr('src', url + "preview/");
        }
    };
    return exports;
});
