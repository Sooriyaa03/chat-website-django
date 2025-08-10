var v1 = '', v2 = '';

setInterval(function(){

    v1 = document.forms["form1"]["message"].value;
    v2 = document.forms["form1"]["name"].value;


    if (v1 == '' && v2 == ''){

        if ( window.history.replaceState ) {
            window.history.replaceState( null, null, window.location.href );
        }

        location.reload(true);
    }

}, 3000);
