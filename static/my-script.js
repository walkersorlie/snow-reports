$(function() {
    $(".list-group a").hover(
    function() {
        $(this).css('background-color', '#eee')
        $(this).css('color', '#222')
    }, function() {
        $(this).css('background-color', '#222')
        $(this).css('color', '#eee')
    });
});​
