$(document).ready(function($) {
  $('.menu-btn').on('click', function(e) {
    e.preventDefault;
    $(this).toggleClass('menu-btn_active');
    $('.menu-nav').toggleClass('menu-nav_active');
    $('.menu-a').toggleClass('menu-a_active');
  });


  $('.txtb input').on('focus', function(){
    $(this).addClass('focus');
  });

  $('.txtb input').on('blur', function(){
    if($(this).val() == '')
    $(this).removeClass('focus');
  });

});
window.onload = function () {
  document.body.classList.add('loaded_hiding');
  window.setTimeout(function () {
    document.body.classList.add('loaded');
    document.body.classList.remove('loaded_hiding');
  });
}
