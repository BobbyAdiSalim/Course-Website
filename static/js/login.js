$(document).ready(function(){
    $('.register_student').hide();
    $('.register_instructor').hide();
    
    // Select Student at the first (default)
    $('.newstud').slideToggle();
    $('.newins').hide();
    $('minibutton').hide();
    $('.minibutton1_student').css("background-color","#25355A");
    $('.minibutton1_student').css("color","#E5E4E2");
    $('.minibutton1_instructor').css("background-color","#E5E4E2");
    $('.minibutton1_instructor').css("color","#25355A");

        $('#radio_student').click(function(){
            $("#radio_student").attr("checked", "checked");

            $('.newstud').show();
            $('.newins').hide();
            $('minibutton').hide();
            $('.minibutton1_student').css("background-color","#25355A");
            $('.minibutton1_student').css("color","#E5E4E2");
            $('.minibutton1_instructor').css("background-color","#E5E4E2");
            $('.minibutton1_instructor').css("color","#25355A");
        });

        $('#radio_instructor').click(function(){
            $("#radio_instructor").attr("checked", "checked");

            $('.newins').show();
            $('.newstud').hide();
            $('.minibutton1_instructor').css("background-color","#25355A");
            $('.minibutton1_instructor').css("color","#E5E4E2");
            $('.minibutton1_student').css("background-color","#E5E4E2");
            $('.minibutton1_student').css("color","#25355A");
        });

        $('.click_register_student').click(function(){
            $('.register_student').show();
            $('.login_new').hide();
            $('.register_instructor').hide();
        });

        $('.click_register_instructor').click(function(){
            $('.register_instructor').show();
            $('.register_student').hide();
            $('.login_new').hide();
        });

        $('.choose_login').click(function(){
            $('.login_new').show();
            $('.register_student').hide();
            $('.register_instructor').hide();
            $('.minibutton1_student').css("background-color","#E5E4E2");
            $('.minibutton1_student').css("color","#25355A");
            $('.minibutton1_instructor').css("background-color","#E5E4E2");
            $('.minibutton1_instructor').css("color","#25355A");
        });

    });