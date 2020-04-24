$(document).ready(function() {
/* Гамбургер */

  $('.menu-btn').on('click', function(e) {
    e.preventDefault;
    $(this).toggleClass('menu-btn_active');
    $('.menu-nav').toggleClass('menu-nav_active');
    $('.menu-a').toggleClass('menu-a_active');
  });
/* ---------------------------------------------------------------------- */

/* Вход/Регистрация */

  $('.txtb input').on('focus', function(){
    $(this).addClass('focus');
  });

  $('.txtb input').on('blur', function(){
    if($(this).val() == '')
    $(this).removeClass('focus');
  });

/* Алерт на удаление поста */
  $('.post_delete_button').on('click', function(e) {
    e.preventDefault;
    $('.post_delete_form').addClass('post_delete_form_active');
    $('.post_delete_form_container').addClass('post_delete_form_container_active');
  });
  $('.post_cancel_delete_form_button').on('click', function(e) {
    e.preventDefault;
    $('.post_delete_form').removeClass('post_delete_form_active');
    $('.post_delete_form_container').removeClass('post_delete_form_container_active');
  });

/* Алерт на зугрузку изображения

  $('.post_create_form_img_button').on('click', function(e) {
    e.preventDefault;
    $('.post_create_form_img').addClass('post_create_form_img_active');
    $('.post_create_form_img_container').addClass('post_create_form_img_container_active');
  });
  $('.cancel_button_icon').on('click', function(e) {
    e.preventDefault;
    $('.post_create_form_img').removeClass('post_create_form_img_active');
    $('.post_create_form_img_container').removeClass('post_create_form_img_container_active');
  });*/

/* Адмиинка */
  $('.admin-btn').on('click', function(e) {
    e.preventDefault;
    $(this).toggleClass('admin-btn_active');
    $('.admin-btn i').toggleClass('adm_i_active')
    $('.admin_panel').toggleClass('admin_panel_active');
  });
/* ---------------------------------------------------------------------- */
});
