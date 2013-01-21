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

// This file contains all the js related to the<a href="OWA"></a> main xul page

// Set it to false upon deployement
DEBUG = true;

// Strings to be translated
DELETE_  = 'Delete "';
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


// set crfs cookie
$('html').ajaxSend(function(event, xhr, settings) {
    function getCookie(name) {
        var cookieValue = null;
        if (document.cookie && document.cookie != '') {
            var cookies = document.cookie.split(';');
            for (var i = 0; i < cookies.length; i++) {
                var cookie = jQuery.trim(cookies[i]);
                // Does this cookie string begin with the name we want?
                if (cookie.substring(0, name.length + 1) == (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }
    if (!(/^http:.*/.test(settings.url) || /^https:.*/.test(settings.url))) {
        // Only send the token to relative URLs i.e. locally.
        xhr.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));
    }
});

// initialize
jQuery(document).ready(function() {
                $.jsonRPC.setup({
                   endPoint: '/exeapp/json/',
                   namespace: 'package',
                });
                $("a.bigButton, a.smallButton").button();
                // Initialize outline tree
                $.jstree._themes = "/static/css/themes/"
                get_outline_pane().jstree({
                  "core" : {	"animation" : 200
                  },
                  "ui" : {		"select_limit" : 1, 
                      			"initially_select" : ["node" + get_outline_pane().attr("current_node")]
                  },
                  "themes" : {	"dots" : false,
                  				"icons" : false, 
                  },
                  "plugins" : ["themes", "html_data", "ui", "crrm"]});
                get_outline_pane().jstree('open_all', $('#outline_pane>ul'));
                //bind actions to outline nodes
                get_outline_pane().bind("select_node.jstree", 
                      handle_select_node);
                get_outline_pane().delegate("a", "dblclick", rename_current_node);
                //bind renaming event
                get_outline_pane().bind("rename_node.jstree", handle_renamed_current_node);
                // handle theme selection
                $("#style_selector").change(handle_select_style);
                
                // Initialize idevice Tree
                $("#idevice_pane").jstree({"themes" : {	"dots" : false,
                  										"icons" : false, 
                  							},
                  							"plugins" : ["themes", "html_data", "ui"]
                  						});
                $("#idevice_pane").jstree('open_all', $('#idevice_pane>ul'));
                                   
                
                //bind actions to outline buttons
                $("#btnAdd").click(add_child_node)
                $("#btnRemove").click(delete_current_node)
                $("#btnRename").click(rename_current_node);
                $("#btnDuplicate").click(function() {alert(NOT_IMPLEMENTED);});
                
                $("#btnPromote").click(promote_current_node);
                $("#btnDemote").click(demote_current_node);
                $("#btnUp").click(move_current_node_up);
                $("#btnDown").click(move_current_node_down);
                
                // init ajax forms
                $(".property_form").ajaxForm(function (responseText, statusText, xhr, form){
                 	$(".errorlist").hide();
                 	if (responseText != ""){
                 		form.find("table").html(responseText);
                 	}
                 });

                
                //$(".bigButton:not(#btnRename), .smallButton").each(function(index) {
                //    bindButtonClicked(this);
                //});
                //bind action to idevice items
                $("#idevice_pane").delegate(".ideviceItem", "click", add_idevice);
                $("#middle").tabs();
                updateTitle();
                
                // $("#authoringIFrame1").load(function() {
                	// var node_id = $("#authoringIFrame1").contents().find("#node_id").text();
                	// if (current_outline_id() != node_id){
                		// get_outline_pane().jstree("select_node", $("#node" + node_id), true);
                	// }
                // })
                set_current_style()
            });

// Adds a new node to current one
function add_child_node() {
  
  $.jsonRPC.request('add_child_node', [get_package_id()], {
    success: function(results) {
      callback_add_child_node(results.result.id, results.result.title);
    }
  })
}



//Removes current node
function delete_current_node() {
  $.jsonRPC.request('delete_current_node', [get_package_id()], {
    success: function(results) {
      if (results.result.deleted == 1) {
        callback_delete_current_node();
      }
    }
  })
}

//Simply triggeds jstree's rename routine
function rename_current_node(){
  if (get_current_node().attr('id') != "node" + current_outline_id()) {
      alert("Somehow you managed to call dblclik event without a single click. Please, reload page!");
      return null;
  }
  get_outline_pane().jstree("rename");
}

// Promotes current node to a sibling of it's parent.
function promote_current_node(){
  // check if the current node is the root or a child of the root
  if (is_root(get_current_node()) || 
  is_root(get_current_node().parent().parent().parent())) {
              alert(CANT_MOVE_NODE_FURTHER);
              return -1;
            }
  $.jsonRPC.request('promote_current_node', [get_package_id()], {
    success: function(results){
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
  if (is_root(get_current_node())) {
    alert("Can't demote the root.");
  } else 
    // Check if there are any nodes before current one on the same level
    if (get_current_node().parent().prev().length == 0) {
      alert ("No previous node, can't demote.");
    } else {
      $.jsonRPC.request('demote_current_node', [get_package_id()], {
        success: function(results) {
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
function move_current_node_up(){
  // Check if there are any nodes before the current one on the same level
  if (get_current_node().parent().prev().length == 0) {
    alert(CANT_MOVE_NODE_FURTHER);
  }
  $.jsonRPC.request('move_current_node_up', [get_package_id()], {
      success: callback_move_current_node_up,
      error: function(result) { alert (NODE_WAS_NOT_MOVED); }
    });
}

// Move current node down at the same level
function move_current_node_down() {
  if (get_current_node().parent().next().length == 0) {
    alert(CANT_MOVE_NODE_FURTHER);
    return -1;
  }
  $.jsonRPC.request('move_current_node_down', [get_package_id()], {
    success: function(results) {
      if (results.result.moved != '1'){
        alert(NODE_WAN_NOT_MOVED);
      } else {
        callback_move_current_node_down();
      }
    }
  });
}

function add_idevice() {
  var ideviceid = $("#idevice_pane").jstree("get_selected").find(">a").attr('ideviceid');
  $.jsonRPC.request('add_idevice', [get_package_id(), ideviceid],{
    success: function(results) {
    	insert_idevice(
    		results.result.idevice_id
    	);
    }
  });
  return false;
} 

// Handles outline_pane selection event. Calls package.change_current_node
// via rpc. 
function handle_select_node(event, data) {

    var node = get_current_node();
    $.jsonRPC.request('change_current_node',
    [get_package_id(), $(node).attr("nodeId")], {
        success: function(results) {
              set_current_node(node);
        }
    });
    return false;
}

function handle_select_style() {
	
	$.jsonRPC.request("set_package_style", [get_package_id(), $("#style_selector").val()]);
}

//handle renamed node event. Calls package.rename_node over rpc.
function handle_renamed_current_node(e, data){
  var new_title = data.rslt.name;
  $.jsonRPC.request('rename_current_node', [get_package_id(), new_title], {
    success: function(results){
      var server_title = ""
      if ("title" in results.result){
        server_title = results.result.title;
        reload_authoring();
      }
      if (new_title != server_title){
        alert("Server couldn't rename the node");
        get_current_node().html($("<ins />").addClass('jstree-icon'));
        get_current_node().append(server_title);
      }
    }});
}

// Returns the _exe_nodeid attribute of the currently selected row item
function current_outline_id(index)
{
    return get_current_node().attr('nodeId');
}

var outlineButtons = new Array('btnAdd', 'btnDel', 'btnRename', 'btnPromote', 'btnDemote', 'btnUp', 'btnDown', 'btnDbl')

function disableButtons(state) {
    if (state){
        //$(".bigButton, .smallButton").button("disable");
        $.blockUI();
    } else {
        enableButtons();
    }
}


function addStyle() {
    var src = addDir();
    $.jsonRPC('importStyle', [get_package_id(),'',src]);
}

function enableButtons() {
    //$(".bigButton, .smallButton").button('enable');
    $.unblockUI();
}

function get_package_id(){
  return $("#package_id").text()
}

// Appends a child node with name and _exe_nodeid to the currently
// selected node
function callback_add_child_node(nodeid, title) {
    var current_li = get_current_node().parent();
    var new_node = {'data' : {'title' : title, 
        'attr': {'id' : 'node' + nodeid, 'nodeid' : nodeid}}}
    get_outline_pane().jstree("create_node",current_li, "last", new_node);
    get_outline_pane().jstree("open_node", current_li);
    get_outline_pane().jstree("select_node", $("#node" + nodeid), true);
}

// Delete the currently selected node
function callback_delete_current_node() {
    var currentNode = get_current_node();
    // parent ul
    get_outline_pane().jstree("delete_node", currentNode);
    updateTitle();
}

// Move the node to the same level as it's parent and place it after.
function callback_promote_current_node() {
  // Move through <li>, <ul> to parent's <li>
  var parent_container_node = get_current_node().parent().parent().parent()
  move_current_node_to_neighbour(parent_container_node, "after")
}

function callback_demote_current_node() {
  var previous_node = get_current_node().parent().prev();
  move_current_node_to_neighbour(previous_node, "last")
}

// Move current node before the previous
function callback_move_current_node_up() {
  var neighbour_node = get_current_node().parent().prev();
  move_current_node_to_neighbour(neighbour_node, "before")
}

// Move current node after the next
function callback_move_current_node_down() {
  var neighbour_node = get_current_node().parent().next();
  move_current_node_to_neighbour(neighbour_node, "after");
}

// places the current node to position relatively to neighbour
function move_current_node_to_neighbour(neighbour_node, position) {
	var current_node = get_current_node();
	get_outline_pane().jstree("move_node", current_node, neighbour_node, position);
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
function set_current_node(node) {
  get_outline_pane().attr('current_node', get_current_node().attr('nodeid'));
  updateTitle();
  reload_authoring();
  update_preview();
}

function update_preview() {
  var url = window.location.protocol + '//' + location.host + location.pathname;
  $('#preview > iframe').attr('src', url + "preview/" + get_outline_pane().attr("current_node") + '/');
}

function set_current_style() {
	$.jsonRPC.request('get_current_style', [get_package_id()],
		{success: function(results){
			var style_val = results.result.style;
			$("#style_selector").val(style_val);
			update_preview();
		}});
}

function get_current_node() {
    var selected = get_outline_pane().jstree("get_selected").find(">a");
    return selected;
}

function get_outline_pane() {
  return $("#outline_pane");
}

function setDocumentTitle(title) {
    document.title = title + " : " + $(".curNode").text();
}

//gets editors width in pixel and sets its width accordingly
function setEditorsWidth() {
	var width = prompt("Enter editor's new width. 0 or empty to set it to 100%");
	$.jsonRPC('setEditorsWidth', [get_package_id(),'',width]);
}

//Set the page title
function updateTitle() {
	;
}
