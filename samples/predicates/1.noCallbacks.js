var messages = [{
    author: 'Vasja',
    text: 'hello'
}, {
    author: 'Anna',
    text: 'my message'
}, {
    author: 'Masha',
    text: '12345'
}];

function filterByName(messages, name) {
    var filtered = [];
    for (var i = 0; i < messages.length; ++i) {
        if (message.author != name) {
            filtered.push(messages[i]);
        }
    }

    return filtered;
}

function filterByMessageLength(messages, length) {
    var filtered = [];
    for (var i = 0; i < messages.length; ++i) {
        if (message.text.length <= length) {
            filtered.push(messages[i]);
        }
    }

    return filtered;
}

console.log(filterByName(messages, 'Vasja'));
console.log(filterByMessageLength(messages, 20));