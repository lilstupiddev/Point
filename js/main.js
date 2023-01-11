const div = document.querySelector( '.box-sensed');


 
document.addEventListener( 'click', (e) => {
	const withinBoundaries = e.composedPath().includes(div);
 
	if ( ! withinBoundaries ) {
		document.querySelector('.form-sended').style.display = 'none';
	}
})
$('.telegram-form').submit(function (event) {
    event.stopPropagation();
    event.preventDefault();
    let form = this,
        submit = $('.submit', form),
        data = new FormData(),
        files = $('input[type=file]')
    data.append( 'name', 		$('[name="name"]', form).val() );
    data.append( 'phone', 		$('[name="phone"]', form).val() );
    data.append( 'telegram_username', $('[name="telegram_username"]', form).val() );
    files.each(function (key, file) {
        let cont = file.files;
        if ( cont ) {
            $.each( cont, function( key, value ) {
                data.append( key, value );
            });
        }
    });
    $.ajax({
        url: 'ajax.php',
        type: 'POST',
        data: data,
        cache: false,
        dataType: 'json',
        processData: false,
        contentType: false,
        xhr: function() {
            let myXhr = $.ajaxSettings.xhr();

            if ( myXhr.upload ) {
                myXhr.upload.addEventListener( 'progress', function(e) {
                    if ( e.lengthComputable ) {
                        let percentage = ( e.loaded / e.total ) * 100;
                            percentage = percentage.toFixed(0);
                        $('.submit', form)
                            .html( percentage + '%' );
                    }
                }, false );
            }
            return myXhr;
        },
        error: function( jqXHR, textStatus ) {
        },
        complete: function() {        
        $(".telegram-form").trigger("reset");
        document.querySelector('.form-sended').style.display = 'block';
        form.serialize();
        }
    });
    return false;
});


$("#form-button-exit").on("click", function() {
    document.querySelector('.form-sended').style.display = 'none';
});