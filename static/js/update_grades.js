$(document).ready(function() {
    $('.grade-input').keypress(function (e) {
        if (e.keyCode === 13) {
            var currentIndex = $('.grade-input').index(this);
            $('.grade-input').eq(currentIndex + 1).focus();
            e.preventDefault();
        }
    });
    $('.grade-input').last().keypress(function (e) {
        if (e.keyCode === 13) {
            $('.add-button').click();
        }
    });
  });