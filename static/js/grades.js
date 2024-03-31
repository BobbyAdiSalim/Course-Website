$(document).ready(function() {
    $('.more').click(function() {
      $(this).parent().next('.comment-container').slideToggle();
    });
  });