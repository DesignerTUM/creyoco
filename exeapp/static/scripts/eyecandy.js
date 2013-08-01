define(['jquery', 'chosen', 'qtip2'], function($) {
    var eyecandy_exports = {
        show_lightbox: function(width, height, el) {
            $(".modal-dialog")
            //.height(400)
            //.width(400)
            .css({
                'width' : width+'px',
                'height' : height+'px',
                'margin-left' : -width/2+'px',
                'margin-top' : -height/2+'px'


            });
            $(".modal-dialog > :not(.icon-remove)").each(function() {
                $(this).hide();
            });
            $('#lightbox').show();
            $(el).show();
        },

        init: function() {
            $(document).ready(function() {
            $(".icon-remove, #modal-dialog-bg").click(function(){
                $("#lightbox").hide();
                $('body').css('overflow', 'auto');
            });

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
                exports.show_lightbox(365, 200, $("#download_box"));
            });

            $('.theme').click(function() {
                exports.show_lightbox(960, 765);
                $('.modal-dialog > #previewIFrame')
                    .show()
                    .load(function(){
                        $(this).parent().removeClass("loading")
                    })
                    .parent().addClass("loading");
                $('.theme').removeClass('selected');
                $(this).addClass('selected');

                update_preview();
            });
            $("#help_trigger").on("click", function() {
                        exports.show_lightbox(960, 756, $('#helpIFrame'));
                        return false;
                   });
            });
        }
    };
    return eyecandy_exports;
});
