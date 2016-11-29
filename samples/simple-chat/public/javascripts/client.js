
$(onLoad);

function onLoad() {
    var $messages = $('.messages');

    var $messageForm = $('.message-form');
    var $text = $messageForm.find('.message-form__text');
    var $send = $messageForm.find('.message-form__send');

    var fromId = -1;

    $send.click(function(e) {
        e.preventDefault();

        var text = $text.val();

        if (text) {
            var data = {
                'text': text
            };

            $.post('/api/message', data)
                .done(function(html) {
                    $text.val('');
                })
                .fail(function(error) {
                    alert('Failed to create message');
                    console.log(error);
                });
        }
    });

    setInterval(function () {
        getNewMessages();
    }, 1000);

    function getNewMessages() {
        $.get('/api/new_messages', {
                fromId: fromId
            })
            .done(function(res) {
                if (res.messages.length == 0) {
                    return;
                }

                var lastMessage = res.messages[res.messages.length - 1];
                fromId = lastMessage.id;

                for (var i = 0; i < res.messages.length; ++i) {
                    addMessage(res.messages[i]);
                }

                $('body').animate({ scrollTop: $(document).height() }, 100);
            })
            .fail(function(error) {
                alert('Failed to get messages');
                console.log(error);
            });
    }

    function addMessage(message) {
        var text = '<div>' + message.text + '</div>';

        var $message = $(text);
        $message.appendTo($messages);
    }
}

