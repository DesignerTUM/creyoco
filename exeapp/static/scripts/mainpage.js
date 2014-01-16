// ===========================================================================
// eXe
// Copyright 2004-2005, University of Auckland
// Copyright 2004-2007 eXe Project, New Zealand Tertiary Education Commission
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

// This file contains all the js related to the main xul page

// Set it to false upon deployement
DEBUG = true;

// Strings to be translated
DELETE_ = 'Delete "';
NODE_AND_ALL_ITS_CHILDREN_ARE_YOU_SURE_ = '" node and all its children. Are you sure?';
RENAME_ = 'Rename "';
ENTER_THE_NEW_NAME = "Enter the new name";
SAVE_PACKAGE_FIRST_ = "Save Package first?";
THE_CURRENT_PACKAGE_HAS_BEEN_MODIFIED_AND_NOT_YET_SAVED_ = "The current package has been modified and not yet saved. ";
WOULD_YOU_LIKE_TO_SAVE_IT_BEFORE_LOADING_THE_NEW_PACKAGE_ = "Would you like to save it before loading the new package?";
DISCARD = 'Discard';
SELECT_A_FILE = "Select a File";
EXE_PACKAGE_FILES = "eXe Package Files";
APPARENTLY_USELESS_TITLE_WHICH_IS_OVERRIDDEN = "Apparently Useless Title which is Overridden";
IDEVICE_EDITOR = "iDevice Editor";
PREFERENCES = "Preferences";
METADATA_EDITOR = "metadata editor";
ABOUT = "About";
SELECT_THE_PARENT_FOLDER_FOR_EXPORT_ = "Select the parent folder for export.";
EXPORT_TEXT_PACKAGE_AS = "Export text package as";
TEXT_FILE = "Text File";
EXPORT_COMMONCARTRIDGE_AS = "Export Common Cartridge as";
EXPORT_SCORM_PACKAGE_AS = "Export SCORM package as";
EXPORT_IMS_PACKAGE_AS = "Export IMS package as";
EXPORT_WEBSITE_PACKAGE_AS = "Export Website package as";
EXPORT_IPOD_PACKAGE_AS = "Export iPod package as";
INVALID_VALUE_PASSED_TO_EXPORTPACKAGE = "INVALID VALUE PASSED TO exportPackage";
SELECT_PACKAGE_TO_INSERT = "Select package to insert";
SAVE_EXTRACTED_PACKAGE_AS = "Save extracted package as";
OVERWRITE_DIALOG = "\nFile already exists. Would you like to overwrite?"
NODE_WAS_NOT_MOVED = "An server error occured. Node was not moved."
CANT_MOVE_NODE_FURTHER = "Can't move up any farther"
NOT_IMPLEMENTED = "This function is not implemented yet."
SAVE_DIRTY_PACKAGE = "Package has been changed. Do you want to save it, before you leave?"

require(['jquery', "common", "eyecandy", 'jquery-pjax', 'jquery-cookie', 'jquery-jsonrpc', "jstree", 'jquery-modal', 'modernizr',
    'multichoice', 'feedback', 'cloze', 'filebrowser'],
    function ($, common, eyecandy) {
        // set crfs cookie
        function csrfSafeMethod(method) {
            // these HTTP methods do not require CSRF protection
            return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
        }

        $.ajaxSetup({
            crossDomain: false, // obviates need for sameOrigin test
            beforeSend: function (xhr, settings) {
                if (!csrfSafeMethod(settings.type)) {
                    xhr.setRequestHeader("X-CSRFToken", $.cookie('csrftoken'));
                }
            }
        });

        // initialize
        jQuery(document).ready(function () {
            $.jsonRPC.setup({
                endPoint: '/exeapp/json/',
                namespace: 'package'
            });
            // Load idevice media
            common.get_media("authoring/?media=true");
            // Initialize outline tree
            common.get_outline_pane().jstree({
                "core": {    "animation": 200
                },
                "ui": {        "select_limit": 1,
                    "initially_select": ["node" + common.get_outline_pane().attr("current_node")]
                },
                "themes": {
                    "url": "/static/scripts/themes/default/style.css",
                    "dots": false,
                    "icons": false
                },
                "dnd": {
                    "drop_check": function(data) {
                        if (data.r.parent().attr("id") == "btnRemove") {
                            data.r
                                .removeClass("icon-trash")
                                .addClass("icon-about-to-remove");
                            return {
                                after: false,
                                before: false,
                                inside: true
                            }
                        }
                        return true;
                    },
                    "drop_finish": function(data) {
                        if (data.r.parent().attr("id") == "btnRemove") {
                            ask_delete_confirmation(undefined,
                                data.o.find("a").attr("nodeid"));
                            $("#btnRemove").mouseleave();
                        }
                    }
                },
                "crrm": {
                    "move": {
                        "check_move": function(data) {
                            if (data.np.attr("id")=="outline_pane") {
                                return false;
                            } else {
                                return true;
                            }
                        }
                    }
                },
                "plugins": ["themes", "json_data", "html_data", "ui", "crrm", "dnd"]})
                .on("move_node.jstree", function(event, data, a, b, c, d) {
                        var current_node_id = data.rslt.o.find("a").attr("nodeid");
                        var target_node_id = data.rslt.r.find("a").attr("nodeid");
                        $.jsonRPC.request('move_node_' + data.rslt.p, {
                            params: [get_package_id(), current_node_id, target_node_id]
                        });
                });

            // remove exclamation sign from #btnRemove after mouse leaves it
            $("#btnRemove").mouseleave(function() {
                $(this).find("i")
                    .removeClass("icon-about-to-remove")
                    .addClass("icon-trash");
            })
            common.get_outline_pane().on("loaded.jstree", function (event, data) {
                common.get_outline_pane().jstree('open_all', $('#outline_pane>ul'));
                bind_pjax();
            });
            //bind renaming event
            common.get_outline_pane().bind("rename_node.jstree", handle_renamed_current_node);
            //refresh pjax on every request
            $.pjax.defaults.maxCacheLength = 0;
            // handle theme selection
            $(".theme").click(handle_select_style);
            $("#previewIFrame iframe")[0].onload = function() {
                $('#previewIFrame').removeClass("loading");
            };

            // Initialize idevice Tree
            $("#idevice_pane").jstree({"themes": {
                "url": "/static/scripts/themes/default/style.css",
                "dots": false,
                "icons": false
            },
                "plugins": ["themes", "html_data", "ui"]
            });
            $("#idevice_pane").on("loaded.jstree", function (event, data) {
                $("#idevice_pane").jstree('open_all', $('#idevice_pane>ul'));
            });

            //bind actions to outline buttons
            $("#btnAdd").click(ask_child_node_name);
            $("#btnRemove").click(ask_delete_confirmation);
            $("#btnRename").click(rename_current_node);
            $("#btnDuplicate").click(duplicate_node);

            $("#btnPromote").click(promote_current_node);
            $("#btnDemote").click(demote_current_node);
            $("#btnUp").click(move_current_node_up);
            $("#btnDown").click(move_current_node_down);

            // init ajax forms
            $("#properties_form, #dublincore_form").ajaxForm(function (responseText, statusText, xhr, form) {
                $(".errorlist").hide();
                if (responseText != "") {
                    form.html(responseText);
                }
            });


            //$(".bigButton:not(#btnRename), .smallButton").each(function(index) {
            //    bindButtonClicked(this);
            //});
            //bind action to idevice items
            $("#idevice_pane").delegate(".ideviceItem", "click", add_idevice);
            updateTitle();

            // $("#authoringIFrame1").load(function() {
            // var node_id = $("#authoringIFrame1").contents().find("#node_id").text();
            // if (current_outline_id() != node_id){
            // common.get_outline_pane().jstree("select_node", $("#node" + node_id), true);
            // }
            // })
            set_current_style();
            common.init();
            eyecandy.init();

        });

        // Called after successful package deletion
        function callback_delete_package(id) {
            var package_li = $(".package[package_id=" + id + "]");
            package_li.remove();
        }

        //Bind pjax to a's of outline pane
        function bind_pjax() {
            var $nodes = common.get_outline_pane().find("ul > li > a");
            $nodes.off("click");
            $nodes.on("click", function (event) {
                common.get_outline_pane().jstree("select_node", "#" + $(this).attr("id"), true);
                handle_select_node(event);
                return false;
            });
        }

        // Promps a new package new and sens a "main.create_package" call via
        // rpc
        function create_package() {
            var package_title = prompt('Enter package title');
            $.jsonRPC.request('create_package', {
                params: [package_title],
                success: function (results) {
                    window.open(results.result.url, "_self");
                }
            });
        }

        function delete_package() {
            var package_id = $(this).parent().attr('package_id');
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
        }


        function ask_child_node_name() {
            var modal = $("#node_name");
            var button = modal.find("input[type=button]");
            var text = modal.find("input[type=text]");
            modal.modal();
            text.val("");
            text.focus();

            button.off("click").click(function () {
                var new_name = text.val();
                $.modal.close();
                add_child_node(new_name);
            });
            text.off("keypress").keypress(function (e) {
                var code = (e.keyCode ? e.keyCode : e.which);
                if (code === 13) {
                    button.click();
                }
            });
        }

        // Adds a new node to current one
        function add_child_node(new_name) {

            $.jsonRPC.request('add_child_node', {
                params: [get_package_id(), common.get_current_node_id(), new_name],
                success: function (results) {
                    callback_add_child_node(results.result.id, results.result.title, new_name);
                }
            })
        }

        //Duplcates current node
        function duplicate_node() {
            $.jsonRPC.request('duplicate_node', {
                params: [get_package_id(), common.get_current_node_id()],
                success: function (results) {
                    callback_duplicate_node(results.result);
                }
            });
        }

        function ask_delete_confirmation(event, nodeid) {
            if (nodeid !== undefined) {
                var node = $("#node" + nodeid);
            } else {
                var node = common.get_current_node();
            }

            common.ask_delete_confirmation("node " + node.text(), function() {
                delete_node(nodeid);
                $.modal.close();
            });
        }

        //Removes current node
        function delete_node(nodeid) {
            if (nodeid === undefined) {
                var nodeid = common.get_current_node_id();
            }
            $.jsonRPC.request('delete_node', {
                params: [get_package_id(), nodeid],
                success: function (results) {
                    var new_node_id = results.result.new_node;
                    if (new_node_id != 0) {
                        callback_delete_current_node(new_node_id, nodeid);
                    }
                }
            })
        }

        //Simply triggeds jstree's rename routine
        function rename_current_node() {
            if (common.get_current_node().attr('id') != "node" + current_outline_id()) {
                alert("Somehow you managed to call dblclik event without a single click. Please, reload page!");
                return null;
            }
            common.get_outline_pane().jstree("rename");
        }

        // Promotes current node to a sibling of it's parent.
        function promote_current_node() {
            // check if the current node is the root or a child of the root
            if (is_root(common.get_current_node()) ||
                is_root(common.get_current_node().parent().parent().parent())) {
                alert(CANT_MOVE_NODE_FURTHER);
                return -1;
            }
            $.jsonRPC.request('promote_current_node', {
                params: [get_package_id(), common.get_current_node_id()],
                success: function (results, event) {
                    if (results.result.promoted != "1") {
                        alert(NODE_WAS_NOT_MOVED);
                    } else {
                        callback_promote_current_node();
                    }
                }
            });
        }

        function demote_current_node() {
            // Check if current node if a root
            if (is_root(common.get_current_node())) {
                alert("Can't demote the root.");
            } else
            // Check if there are any nodes before current one on the same level
            if (common.get_current_node().parent().prev().length == 0) {
                alert("No previous node, can't demote.");
            } else {
                $.jsonRPC.request('demote_current_node', {
                    params: [get_package_id(), common.get_current_node_id()],
                    success: function (results) {
                        if (results.result.demoted != "1") {
                            alert(NODE_WAS_NOT_MOVED);
                        } else {
                            callback_demote_current_node();
                        }
                    }
                });
            }
        }

        // Move node up at the same level
        function move_current_node_up() {
            // Check if there are any nodes before the current one on the same level
            if (common.get_current_node().parent().prev().length == 0) {
                alert(CANT_MOVE_NODE_FURTHER);
            }
            $.jsonRPC.request('move_current_node_up', {
                params: [get_package_id(), common.get_current_node_id()],
                success: callback_move_current_node_up,
                error: function (result) {
                    alert(NODE_WAS_NOT_MOVED);
                }
            });
        }

        // Move current node down at the same level
        function move_current_node_down() {
            if (common.get_current_node().parent().next().length == 0) {
                alert(CANT_MOVE_NODE_FURTHER);
                return -1;
            }
            $.jsonRPC.request('move_current_node_down', {
                params: [get_package_id(), common.get_current_node_id()],
                success: function (results) {
                    if (results.result.moved != '1') {
                        alert(NODE_WAN_NOT_MOVED);
                    } else {
                        callback_move_current_node_down();
                    }
                }
            });
        }

        function add_idevice() {
            var ideviceid = $("#idevice_pane").jstree("get_selected").find(">a").attr('ideviceid');
            $.jsonRPC.request('add_idevice', {
                params: [get_package_id(), common.get_current_node_id(), ideviceid],
                success: function (results) {
                    common.insert_idevice(
                        results.result.idevice_id
                    );
                }
            });
            return false;
        }

        // Handles outline_pane selection event. Calls package.change_current_node
        // via rpc.
        function handle_select_node(event, data) {

            // for (key in data){alert(key);};
            if (data == undefined) {
                var node = common.get_current_node();
                set_current_node(event, node);
            }
        }

        function handle_select_style() {
            var _this = $(this);
            $.jsonRPC.request("set_package_style", {
                params: [get_package_id(), common.get_current_node_id(), $(this).attr('id')],
                success: function() {
                    $("#previewIFrame").addClass("loading");
                    common.update_preview();
                    eyecandy.show_lightbox(0,0, $("#previewIFrame"));
                    $('.theme').removeClass('selected');
                    _this.addClass('selected');
                }
            });
        }

        //handle renamed node event. Calls package.rename_node over rpc.
        function handle_renamed_current_node(e, data) {
            var new_title = data.rslt.name;
            $.jsonRPC.request('rename_current_node', {params: [get_package_id(), common.get_current_node_id(), new_title]}, {
                success: function (results) {
                    var server_title = ""
                    if ("title" in results.result) {
                        server_title = results.result.title;
                        common.reload_authoring();
                    }
                    if (new_title != server_title) {
                        alert("Server couldn't rename the node");
                        common.get_current_node().html($("<ins />").addClass('jstree-icon'));
                        common.get_current_node().append(server_title);
                    }
                }});
        }

        // Returns the _exe_nodeid attribute of the currently selected row item
        function current_outline_id(index) {
            return common.get_current_node().attr('nodeId');
        }

        var outlineButtons = new Array('btnAdd', 'btnDel', 'btnRename', 'btnPromote', 'btnDemote', 'btnUp', 'btnDown', 'btnDbl')

        function disableButtons(state) {
            if (state) {
                //$(".bigButton, .smallButton").button("disable");
                $.blockUI();
            } else {
                enableButtons();
            }
        }


        function addStyle() {
            var src = addDir();
            $.jsonRPC('importStyle', [get_package_id(), '', src]);
        }

        function enableButtons() {
            //$(".bigButton, .smallButton").button('enable');
            $.unblockUI();
        }

        function get_package_id() {
            return $("#package_id").text()
        }

        // Appends a child node with name and _exe_nodeid to the currently
        // selected node
        function callback_add_child_node(nodeid, title) {
            var current_li = common.get_current_node().parent();
            var new_node = {'data': {'title': title,
                'attr': {'id': 'node' + nodeid,
                    'nodeid': nodeid,
                    'href': "/exeapp/package/" + get_package_id() + "/" + nodeid + "/"}}}
            common.get_outline_pane().on("create_node.jstree", function (event, data) {
                var id_attr = data.rslt.obj.find("a").attr('id');
                bind_pjax();
                var node = $("#" + id_attr);
                node.click();
            });
            common.get_outline_pane().jstree("create_node", current_li, "last", new_node);
            common.get_outline_pane().jstree("open_node", current_li);
        }


        //generates node data from a result object
        function generate_node_data(result) {
            var children = [];
            for (child in result.children) {
                children.push(generate_node_data(result.children[child]));
            }
            rslt = {'data': {
                'title': result.title,
                'attr': {
                    'id': 'node' + result.id,
                    'nodeid': result.id,
                    'href': "/exeapp/package/" + get_package_id() + "/" + result.id + "/"
                }
            },
                'children': children
            };

            if (children.length != 0) {
                rslt['state'] = 'open';
            }
            return rslt;
        }

        //Duplicate current node
        function callback_duplicate_node(result, parent) {
            var new_id = result.id;
            var title = result.title;
            if (parent == undefined) {
                var parent = common.get_current_node();
            }
            var current_li = parent.parent().parent().parent();
            if (current_li[0] === common.get_outline_pane()[0]) {
                current_li = parent.parent();
            }
            var new_node = generate_node_data(result);
            var tree = common.get_outline_pane().jstree("tree-container");
            current_li.append(tree._parse_json(new_node));
            tree.clean_node(current_li);
            bind_pjax();
        }

        // Delete the currently selected node
        function callback_delete_current_node(new_node_id, removed_node_id) {
            if (removed_node_id === undefined) {
                removed_node_id = common.get_current_node_id();
            }
            common.get_outline_pane().jstree("delete_node", "#node" + removed_node_id);
            common.get_outline_pane().jstree("select_node", "#node" + new_node_id, true);
            var url = "/exeapp/package/" + get_package_id() + "/" + new_node_id + "/";
            $.pjax({url: url,
                container: "#authoring"
            });
            updateTitle();
        }

        // Move the node to the same level as it's parent and place it after.
        function callback_promote_current_node() {
            // Move through <li>, <ul> to parent's <li>
            var parent_container_node = common.get_current_node().parent().parent().parent()
            move_current_node_to_neighbour(parent_container_node, "after")
        }

        function callback_demote_current_node() {
            var previous_node = common.get_current_node().parent().prev();
            move_current_node_to_neighbour(previous_node, "last")
        }

        // Move current node before the previous
        function callback_move_current_node_up() {
            var neighbour_node = common.get_current_node().parent().prev();
            move_current_node_to_neighbour(neighbour_node, "before")
        }

        // Move current node after the next
        function callback_move_current_node_down() {
            var neighbour_node = common.get_current_node().parent().next();
            move_current_node_to_neighbour(neighbour_node, "after");
        }

        // places the current node to position relatively to neighbour
        function move_current_node_to_neighbour(neighbour_node, position) {
            var current_node = common.get_current_node();
            common.get_outline_pane().jstree("move_node", current_node, neighbour_node, position);
        }


        // Checks if node is root, saves a lot parent() in the code
        function is_root(node) {
            // Get parent li, if node is a <a>-reference
            if ($(node).is('a')) {
                node = $(node).parent();
            }
            return (node.parent().parent().attr('id') == 'outline_pane');
        }

        // called to synchronize current_node attribute of outline_pane with
        // currently selected node. Refreshes authoring
        function set_current_node(event, node) {
//            common.get_outline_pane().attr('current_node', common.get_current_node().attr('nodeid'));
            updateTitle();
            $.pjax.click(event, {container: "#authoring"});
        }

        function set_current_style() {
            $.jsonRPC.request('get_current_style', {
                params: [get_package_id()],
                success: function (results) {
                    var style_val = results.result.style;
                    $("#" + style_val).addClass("selected");
                }});
        }

        function setDocumentTitle(title) {
            document.title = title + " : " + $(".curNode").text();
        }

        //gets editors width in pixel and sets its width accordingly
        function setEditorsWidth() {
            var width = prompt("Enter editor's new width. 0 or empty to set it to 100%");
            $.jsonRPC('setEditorsWidth', [get_package_id(), '', width]);
        }

        //Set the page title
        function updateTitle() {
            ;
        }
    });
