$(document).ready(function() {
	$('ul#package_list li span .check').click( function() {
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
	    }
	    else {
		    $("#delete_selected_packages").hide();
	    }
	});

	
	$.jsonRPC.setup({
    endPoint: '/exeapp/json/',
    namespace: 'main',
  });
  $("#create_package").click(create_package);
  $("#delete_selected_packages").click(delete_selected_packages);
  
	$('.icon-download').click( function() {
		var bla = $(this).parent().parent().attr('packageid');
		$('#download_box a').each(function() {
			if($(this).attr('dl_type') == 'website') {
				$(this).attr('href', '/exeapp/package/' + bla + '/download/website/');
			}
			if($(this).attr('dl_type') == 'cc') {
				$(this).attr('href', '/exeapp/package/' + bla + '/download/commoncartridge/');
			}
			if($(this).attr('dl_type') == 'ims') {
				$(this).attr('href', '/exeapp/package/' + bla + '/download/ims/');
			}
			if($(this).attr('dl_type') == 'scorm12') {
				$(this).attr('href', '/exeapp/package/' + bla + '/download/scorm12/');
			}
			if($(this).attr('dl_type') == 'scorm2004') {
				$(this).attr('href', '/exeapp/package/' + bla + '/download/scorm2004/');
			}
		});
		
		$('#download_box').show();
		$('.modal-dialog iframe').hide();
		lightbox(365, 200);
	});
})

// Promps a new package new and sens a "main.create_package" call via 
// rpc
function create_package(){
  var package_title = prompt('Enter package title');
    $.jsonRPC.request('create_package', [package_title], {
      success: function(results){
        callback_create_package(results.result.id, results.result.title)
      }
    });
}

// Deletes packages which idicated by selected checkboxes
function delete_selected_packages(){
  $(".active").
  each(function (i){
    var package_id = $(this).attr("packageid");
    $.jsonRPC.request('delete_package', [package_id], {
      success: function(results) {
        var deleted_package_id = results.result.package_id;
          if (deleted_package_id > 0) {
            // Just a pre-caution that we remove the same package as the
            // server
          callback_delete_package(deleted_package_id);
        }
      }
    })
  })
}

// Called after successful package creation
function callback_create_package(id, title){
  $("<li />").addClass('package').attr("id", "package" + id).attr('packageid', id).append($('<a />').attr('href', 'exeapp/package/' + id + '/').text(title)).appendTo('#package_list');
}

// Called after successful package deletion
function callback_delete_package(id) {
  var package_li = $("#package" + id);
  package_li.remove();
}
	function lightbox(width, height) {
		$(".modal-dialog")
		//.height(400)
		//.width(400)
		.css({
			'width' : width+'px',
			'height' : height+'px',
			'margin-left' : -width/2+'px',
			'margin-top' : -height/2+'px'
			
			
		});
		$('#lightbox').show();
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