function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie != '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) == (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
var csrftoken = getCookie('csrftoken');


$(function(){
    $('body').on('submit', 'form#login-form' ,function(e){
        e.preventDefault();

        var $inputs = $('#login-form :input');
        var values = {};

        $inputs.each(function() {
            values[this.name] = $(this).val();
        });
        values['csrfmiddlewaretoken'] = csrftoken
        $.ajax({
            async:false,
            type:"POST",
            url:$(this).attr('action'),
            data: values,
            cache: false,
            success:function(data, textStatus, jqXHR){
                $('#modal-login .modal-content').empty();
                $('#modal-login .modal-content').append(data);
            },
            error:function(data, textStatus, jqXHR){
                $('#modal-login .modal-content').empty();
                $('#modal-login .modal-content').append(data.responseText);
            }
        });
    });
    $('body').on('submit', 'form#signup-form' ,function(e){
        e.preventDefault();

        var $inputs = $('#signup-form :input');
        var values = {};

        $inputs.each(function() {
            values[this.name] = $(this).val();
        });
        values['csrfmiddlewaretoken'] = csrftoken
        $.ajax({
            async:false,
            type:"POST",
            url:$(this).attr('action'),
            data: values,
            cache: false,
            success:function(data, textStatus, jqXHR){
                $('#modal-signup .modal-content').empty();
                $('#modal-signup .modal-content').append(data);
            },
            error:function(data, textStatus, jqXHR){
                $('#modal-signup .modal-content').empty();
                $('#modal-signup .modal-content').append(data.responseText);
            }
        });
    });

    $('#channel-create-button').on('click', 'a', function(e){
        e.preventDefault();
        $.ajax({
            async:false,
            type:"GET",
            url:$(this).attr('href'),
            cache:false,
            success:function(data, textStatus, jqXHR){
                $('#modal-channel .modal-content').empty();
                $('#modal-channel .modal-content').append(data);

            },
            error:function(data, textStatus, jqXHR){
                $('#modal-channel .modal-content').empty();
                $('#modal-channel .modal-content').append(data.responseText);
            }
        });
    });

    $('#channels-bar').on('click', 'a', function(e){
        e.preventDefault();

        $.ajax({
            async:false,
            type:"GET",
            url:$(this).attr('href'),
            cache:false,
            success:function(data, textStatus, jqXHR){
                $('#msg-list').empty();
                $('#msg-list').append(data);

            },
            error:function(data, textStatus, jqXHR){
                alert('Ops!')
            }
        });
    });

    $('#modal-channel').on('submit', 'form#create-channel-form' ,function(e){
        e.preventDefault();

        var $inputs = $('#create-channel-form :input');
        var values = {};

        $inputs.each(function() {
            values[this.name] = $(this).val();
        });
        values['csrfmiddlewaretoken'] = csrftoken

        $.ajax({
            async:false,
            type:"POST",
            url:$(this).attr('action'),
            data: values,
            cache: false,
            success:function(data, textStatus, jqXHR){
                $('ul#channels-bar').append(data);
            },
            error:function(data, textStatus, jqXHR){
                alert('Ops!');
            }
        });
    });
});
