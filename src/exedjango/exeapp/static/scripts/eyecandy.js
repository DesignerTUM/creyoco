function show_lightbox(width, height) {
    $(".modal-dialog")
    //.height(400)
    //.width(400)
    .css({
        'width' : width+'px',
        'height' : height+'px',
        'margin-left' : -width/2+'px',
        'margin-top' : -height/2+'px'


    });
    $(".modal-dialog").children().each(function() {
        $(this).hide();
    });
    $('#lightbox').show();
}

$(document).ready(function() {
	$(document).on('click', '#navi li a', function(e){
        e.preventDefault();
        history.pushState({page: this.href}, '', this.href);
      //  loadPage('body', this.href);
    });
    $(window).on('popstate', function(e){
      //  loadPage('#frontPage', location.pathname);
        console.log(e.originalEvent.state);
    });
	var url = document.URL;
	if (url.search("export") > 0) {
		$('#middle-row').children().hide();
		$('#properties').show();
		$('#navi li').removeClass('active');
		$('#export').addClass('active');
	}
	if (url.search("edit") > 0) {
		$('#middle-row').children().hide();
		$('#authoring').show();
		$('#navi li').removeClass('active');
		$('#edit').addClass('active');
	}

	if (url.search("layout") > 0) {
		$('#middle-row').children().hide();
		$('#selectStyle').show();
		$('#navi li').removeClass('active');
		$('#layout').addClass('active');
	}

	$('.chzn-select').chosen();
	$('#select_course').change( function() {
		location.href = $(this).val();
	});

	$('#settings_button').qtip ({
		content: 'Hinzufuegen, loeschen oder verschieben der Themen', // Noti ce that content.text is long-hand for simply declaring content as a string

		style: {
			tip: true,
			classes: 'tip'
		},

		show: {
			delay: 500,
			effect: function(offset) {
				$(this).slideDown(200); // "this" refers to the tooltip
			}
		},
		position: {
		adjust: {
			x: -20
		}
	}
	});

	$('#download_button').qtip ({
		content: 'Formatauswahl und herunterladen des Paketes', // Noti ce that content.text is long-hand for simply declaring content as a string

		style: {
			tip: true,
			classes: 'tip'
		},

		show: {
			delay: 500,
			effect: function(offset) {
				$(this).slideDown(200); // "this" refers to the tooltip
			}
		},
		position: {
			adjust: {
				x: -20
			}
		}
	});

	$('#outline img').click( function() {
		if($(this).attr('id') == 'settings_button') {
			$(this).removeClass('transparent');
			$('#download').hide();
			$('#settings').slideToggle('slow', function() {
				if($('#settings').is(':visible')) {
					$(this).removeClass('transparent');
					$('#download_button').addClass('transparent');
				}
				else {
					$(this).removeClass('transparent');
					$('#download_button').removeClass('transparent');
				}
			});
		}
		else if($(this).attr('id') == 'download_button') {
			$(this).removeClass('transparent');
			$('#settings').hide();
			$('#download').slideToggle('slow', function() {
				if($('#download').is(':visible')) {
					$(this).removeClass('transparent');
					$('#settings_button').addClass('transparent');
				}
				else {
					$(this).removeClass('transparent');
					$('#settings_button').removeClass('transparent');
				}
			});

		}
	});

	$(document).keyup(function(e) {
		if (e.keyCode == 27) {
			$('#lightbox').hide();
			$('body').css('overflow', 'auto');
		}
	});

	$('#modal-dialog-bg').click( function(){
		$('#preview').hide();
		$('body').css('overflow', 'auto');
	});


	$('#edit a').click( function(){
		$('#middle-row').children().hide();
		$('#authoring').show();
		$('#navi li').removeClass('active');
		$(this).parent().addClass('active');
	});

	$('#layout a').click( function(){
			$('#middle-row').children().hide();
			$('#selectStyle').show();
			$('#navi li').removeClass('active');
			$(this).parent().addClass('active');
	});

	$('#export a').click( function(){
			$('#middle-row').children().hide();
			$('#properties').show();
			$('#navi li').removeClass('active');
			$(this).parent().addClass('active');
	});

	$('#download').click( function () {
        show_lightbox(365, 200);
        $('#download_box').show();
    });

	$('.theme').click(function() {
        show_lightbox(960, 765);
        $('.modal-dialog > #previewIFrame').show();
        ;
		$('.theme').removeClass('selected');
		$(this).addClass('selected');

		update_preview();
	});
	/*$('#download').click( function(){
	var width, height;
	width = 400;
	height = 400;
		$(".modal-dialog")
		//.height(400)
		//.width(400)
		.css({
			'width' : width+'px',
			'height' : height+'px',
			'margin-left' : -width/2+'px',
			'margin-top' : -height/2+'px'


		});

	});*/
});
