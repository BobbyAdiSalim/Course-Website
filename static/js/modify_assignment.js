$(document).ready(function() {
    $('.del-a').on('click', function(event) {
        if (confirm('Delete confirmation. Are you sure?')) {
            return true;
        } else {
            event.stopPropagation();
            event.preventDefault();
        }
    });

    $('.alert-x').on('click', function(event)){
        $('.alert').hide();
    }
});
