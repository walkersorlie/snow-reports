// how to make zebra colors and change others???
$(document).ready(function(){
  $('.list-group a').hover(function()
    {
      //$(this).toggleClass('a.list-group-item:hover');
      $(this).toggleClass('.list-group-item-hover');
      //$(this).toggleClass('a.list-group-item > a:nth-of-type(odd)');
  });
});
