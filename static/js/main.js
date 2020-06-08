$(document).ready(function() {
 // Гамбургер

  $('.menu-btn').on('click', function(e) {
    e.preventDefault;
    $(this).toggleClass('menu-btn_active');
    $('.menu_nav').toggleClass('menu-nav_active');
    $('.menu-a').toggleClass('menu-a_active');
    $('.blog_content').toggleClass('blog_content_none');
  });
 // ----------------------------------------------------------------------

 // Вход/Регистрация

  $('.txtb input').on('focus', function(){
    $(this).addClass('focus');
  });

  $('.txtb input').on('blur', function(){
    if($(this).val() == '')
    $(this).removeClass('focus');
  });

 // Алерт на удаление поста
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

// Изображения

  var fruit = [];
  $(".foo").text(fruit.length);

  var modal = document.getElementById("myModal");
  var span = $(".close");

  span.on("click", function() {
    modal.style.display = "none";
  });
  var images = document.getElementsByTagName("img");
  var modalImg = document.getElementById("img01");
  var captionText = document.getElementById("caption");
  var i;
  for (i = 0; i < images.length; i++) {
  images[i].onclick = function() {
    modal.style.display = "block";
    modalImg.src = this.src;
    modalImg.alt = this.alt;
    captionText.innerHTML = this.nextElementSibling.innerHTML;
  };
  }

// Адмиинка
  $('.admin-btn').on('click', function(e) {
    e.preventDefault;
    $(this).toggleClass('admin-btn_active');
    $('.admin-btn i').toggleClass('adm_i_active')
    $('.admin_panel').toggleClass('admin_panel_active');
  });
 // ----------------------------------------------------------------------
  // $('.gallery').on('click', function(e) {
  //     e.preventDefault;
  //     $(this).toggleClass('gallery_active')
  //   });
});
