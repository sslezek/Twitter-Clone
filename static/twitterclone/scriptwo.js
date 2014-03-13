$(document).ready(function() {
   $('div').mouseenter(function() {
       $(this).animate({
           height: '+=10px'
       });
   });
   $('div').mouseleave(function() {
       $(this).animate({
           height: '-=10px'
       }); 
   });
   $('a').mouseenter(function() {
      $(this).css('color','blue');
   });
   $('a').mouseleave(function() {
      $(this).css('color','red');
   });
   $('#error').click(function() {
      alert("Clicking this username will be a link in my next release");
   });
});