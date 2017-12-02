$(document).ready(function(){
  $('ul li').click(function(){
    $(this).removeClass("active");
    $(this).addClass("active");
    console.log("hello");
});
});
