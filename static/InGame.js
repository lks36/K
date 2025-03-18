var socket = io.connect('http://127.0.0.1:5000');

    socket.on( 'connect', function() {
        socket.emit( 'mon message', {
            data: 'User Connected'
        })
        var form = $( 'form' ).on( 'submit', function( e ) {
            e.preventDefault()
            let user_input = $( 'input.message' ).val()
            socket.emit( 'mon message', {
                message : user_input
            })
            $( 'input.message' ).val( '' ).focus()
        })
    });

    socket.on( 'my response', function( msg ) {
        console.log( msg )
        if( typeof msg.message !== 'undefined' && msg.message!=="" ) {
            $( 'div.message_holder' ).append( '<div>' + msg.message + '</div>' )
    }
    });