$(document).ready(function() {
    var header_height = $('header').outerHeight(true);
    document.styleSheets[0].insertRule(
        ('header.affix ~ section.content > .middle {' +
        'margin-top: ' + header_height + 'px' +
        '}')
    );
});