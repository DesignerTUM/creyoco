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
SELECT_AN_IMAGE    = "Select an image";
IMAGE_FILES        = "Image Files (.jpg, .jpeg, .png, .gif)";
JPEG_FILES         = "JPEG Files (.jpg, .jpeg)";
SELECT_A_FILE      = "Select a file";
FLASH_MOVIE        = "Flash Movie (.flv)";
FLASH_OBJECT       = "Flash Object (.swf)";
SELECT_AN_MP3_FILE = "Select an mp3 file";
SELECT_AN_TEX_FILE = "Select an TeX file";
TEX_FILE           = "TeX File"
MP3_AUDIO          = "MP3 Audio (.mp3)";
PDF                = "PDF Files (.pdf)";
SELECT_A_PDF       = "Select a pdf file";
SHOCKWAVE_FILES    = "Shockwave Director Files (.dcr)"
QUICKTIME_FILES    = "Quicktime Files (.mov, .qt, .mpg, .mp3, .mp4, .mpeg)"
WINDOWSMEDIA_FILES = "Windows Media Player Files (.avi, .wmv, .wm, .asf, .asx, .wmx, .wvx)"
REALMEDIA_AUDIO    = "RealMedia Audio Files (.rm, .ra, .ram, .mp3)"
SELECT_KPSE        = "Select kpsewhich"



SELECT_A_PACKAGE   = "Select a package";
YOUR_SCORE_IS      = "Your score is ";

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

jQuery(document).ready(function() {
	$.jsonRPC.setup({
           endPoint: '/exeapp/json/',
           namespace: 'package',
        });
    initialize_authoring();
    node_id = $("#node_id").text();
    //window.parent.get_outline_pane().jstree("select_node", $("#node" + nodeid), true);
})

function initialize_authoring() {

 //$(".action_button").bind("click", handle_action_button)
 $(".idevice_form").ajaxForm({success: function(responseText, statusText, xhr, $form){
	 	var idevice_id = $form.attr("idevice_id");
	 	scroll_to_element($form);
	 		$form.find("textarea").each(function() {
	 			tinyMCE.execCommand("mceRemoveControl", true, $(this).attr("id"));
	 		});
		if (responseText){
			get_media(".authoring/?idevice_id=" + idevice_id + "&media=true");
	 		$form.html(responseText);
		} else {
			reload_authoring();
		}
		initialize_authoring();
 	},
 	beforeSerialize: function() {
 		 tinyMCE.triggerSave(true, true);},
 	});
}

function scroll_to_element(element){
	var offset = element.offset().top - $(window).scrollTop();

	if(offset > window.innerHeight){
    	// Not in view so scroll to it
    	$('html,body').animate({scrollTop: offset}, 1000);
	} else if (offset < 0) {
		$('html,body').animate({scrollTop: element.offset().top - 100}, 1000);
	} 
}

function reload_authoring() {
	// dynamically load scripts for idevices
	get_media("authoring/?partial=true&media=true");
			
	$("#authoring").load('authoring/?partial=true', function() {
		initialize_authoring();
		});
}

function get_media(request_url) {
	$.ajax({
		url: request_url,
		dataType: 'json',
		async: false,
		success: function(data){
			$.each(data, function(key, val) {
				if (/\.css$/.test(val)){
					if (!($("link[href='" + val + "']")).length > 0) {
						$('<link rel="stylesheet" href="' + val + '">')
								.appendTo("head");
					}
				} else {
					$.getScript(val);
				}
			});
		}});
}	

function insert_idevice(idevice_id) {
	// dynamically load scripts for idevices
	get_media(".authoring/?idevice_id=" + idevice_id + "&media=true");
	    $.ajax({
	    url: ".authoring/?idevice_id=" + idevice_id,
	    dataType: 'html',
	    success: function (data) {
	    	 $('#authoring').append(data);
	    	 initialize_authoring();
	    	 var element = $('#authoring').children().last();
	    	 scroll_to_element(element);
	    	 }
		});
}


// Takes a jQuery object and returns the id of the idevice it
// belongs to
function get_idevice_id(obj){
  re_idevice_id = /idevice(\d*)/;
  return re_idevice_id.exec(get_idevice(obj).attr("id"))[1];
}

// Takes a jQuery object and returns it's idevice block
function get_idevice(obj) {
  return obj.closest(".block");
}

function get_package_id(){
  return $("#package_id").text()
}

// Returns a dictionary of all elements of the idevice with non-empty
// values. 
function get_arguments(idevice_block) {
  var args = {};
  idevice_block.find(":input").each(function() {
    // Don't post elements without name
    if ($(this).attr("name") != undefined) {
      args[$(this).attr("name")] = $(this).val();
    }
  });
  return args;
}

// contentForm to the server
function submitLink(action, idevice_id, changed, arguments) 
{
    $.jsonRPC.request("idevice_action",
      [get_package_id(), idevice_id, action, arguments],
      {success: reload_authoring });

}
