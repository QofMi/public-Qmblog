$(document).ready(function() {
  $('.menu-btn').on('click', function(e) {
    e.preventDefault;
    $(this).toggleClass('menu-btn_active');
    $('.menu-nav').toggleClass('menu-nav_active');
    $('.menu-a').toggleClass('menu-a_active');
  });

  $('.admin-btn').on('click', function(e) {
    e.preventDefault;
    $(this).toggleClass('admin-btn_active');
    $('.admin-btn i').toggleClass('adm_i_active')
    $('.admin_panel').toggleClass('admin_panel_active');
  });
});
