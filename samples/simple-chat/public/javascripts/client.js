
$(onLoad);

function onLoad() {
    const $messages = $('.messages');

    const $messageForm = $('.message-form');
    const $text = $messageForm.find('.message-form__text');
    const $send = $messageForm.find('.message-form__send');

    let fromId = -1;

    $send.click(function(e) {
        e.preventDefault();

        const text = $text.val();

        if (text) {
            const data = {
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

                const lastMessage = res.messages[res.messages.length - 1];
                fromId = lastMessage.id;

                for (let i = 0; i < res.messages.length; ++i) {
                    addMessage(res.messages[i]);
                }

                $('body').animate({ scrollTop: $(document).height() }, 100);
            })
            .fail(function(error) {
                alert('Failed to get messages');
                console.error(error);
            });
    }

    function addMessage(message) {
        const text = '<div>' + message.text + '</div>';

        const $message = $(text);
        $message.appendTo($messages);
    }
}

