$(document).ready(function() {
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

	if($('#package_style').text() == 'vhb') {
		$("#vhb").addClass("StyleActive");
	}
	else if($('#package_style').text() == 'garden') {
		$("#garden").addClass("StyleActive");
	}
	else if($('#package_style').text() == 'silver') {
		$("#silver").addClass("StyleActive");
	}
	else if($('#package_style').text() == 'default') {
		$("#default").addClass("StyleActive");
	}
	
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
			$('#preview').hide();
			$('body').css('overflow', 'auto');
		}
	});
	
	$('#modal-dialog-bg').click( function(){
		$('#preview').hide();
		$('body').css('overflow', 'auto');
	});
	
	$('.button a').click( function(){
		if($(this).attr('href') == '#_preview') {
			$('#previewIFrame').attr("src", $('#previewIFrame').attr("src"));
			$('#preview').show();
			$('#previewIFrame').css({
				overflow: 'hidden',
				width: '0px',
				height: '0px',
				opacity: 0
			});
			$('#previewIFrame').animate({
				height: '756px',
				width: '1024px',
				opacity: 1
        	}, 1000);
		}
		else if($(this).attr('href') == '#_editor') {
			$('#middle-row').children().hide();
			$('#authoring').show();
			$('#navi span').removeClass('button_active');
			$(this).parent().addClass('button_active');
		}
		else if($(this).attr('href') == '#_theme') {
			$('#middle-row').children().hide();
			$('#selectStyle').show();
			$('#navi span').removeClass('button_active')
			$(this).parent().addClass('button_active');
		}
		else if($(this).attr('href') == '#_preferences') {
			$('#middle-row').children().hide();
			$('#properties').show();
			$('#navi span').removeClass('button_active');
			$(this).parent().addClass('button_active');
		}
	});
});