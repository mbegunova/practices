const text_box = '<div class="card-panel right" style="width: 75%; position: relative">' +
    '<div style="position: absolute; top: 0; left:3px; font-weight: bolder" class="title">{sender}</div>' +
    '{message}' +
     '<div style="position: absolute; top: 0; right:3px; font-weight: bolder" class="title">{{ message.timestamp }}</div>'
    + '</div>';


let userState = ''

const userDiv = (senderId, receiverId, name, online) =>
    (
        `<a href="/chat/${senderId}/${receiverId}" id="user${receiverId}" class="collection-item row">
                        <img src="https://png.pngtree.com/png-vector/20191027/ourmid/pngtree-user-icon-isolated-on-abstract-background-png-image_1875037.jpg" class="col s3">
<!--                        <img src="{% static 'images/profile.png' %}" class="col s3">-->
                        <div class="col s8">
                            <span class="title purple-text text-accent-3" style="font-weight: bolder">${name}</span>
                            <span class="btn-flat disable" style="color: ${online ? 'green' : 'red'}; float: right">${online ? 'в сети' : 'не в сети'}</span>
                        </div>
    </a>`)


function scrolltoend() {
    $('#board').stop().animate({
        scrollTop: $('#board')[0].scrollHeight
    }, 800);
}

function send(sender, receiver, message) {
    $.post('/api/messages', '{"sender": "' + sender + '", "receiver": "' + receiver + '","message": "' + message + '" }', function (data) {
        console.log(data);
        var box = text_box.replace('{sender}', "You");
        box = box.replace('{message}', message);
        $('#board').append(box);
        scrolltoend();
    })
}

function receive() {
    $.get('/api/messages/' + sender_id + '/' + receiver_id, function (data) {
        console.log(data);
        if (data.length !== 0) {
            for (var i = 0; i < data.length; i++) {
                console.log(data[i]);
                var box = text_box.replace('{sender}', data[i].sender);
                box = box.replace('{message}', data[i].message);
                box = box.replace('right', 'left putple lighten-5');
                $('#board').append(box);
                scrolltoend();
            }
        }
    })
}

function getUsers(senderId, callback) {
    return $.get('/api/users', function (data) {
        if (userState !== JSON.stringify(data)) {
            userState = JSON.stringify(data);
            const doc = data.reduce((res, user) => {
                if (user.id === senderId) {
                    return res
                } else {
                    return [userDiv(senderId, user.id, user.username, user.online), ...res]
                }
            }, [])
            callback(doc)
        }
    })
}

/* Register function takes two arguments: username and password, for creating the user. */
function register(username, password) {
     //Post to '/api/users' for creating a user, the data in JSON string format.
    $.post('/api/users', '{"username": "'+ username +'", "password": "'+ password +'"}',
        function (data) {
        window.location = '/'; //Redirect to login page if success
        })
        .fail(function (response) {
            $('#id_username').addClass('invalid'); //Add class 'invalid' which will display "Username already taken" in the registration form if failed
        })
}