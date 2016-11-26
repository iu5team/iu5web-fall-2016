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

function filter(messages, pred) {
    var filtered = [];
    for (var i = 0; i < messages.length; ++i) {
        if (pred(messages[i])) {
            filtered.push(messages[i]);
        }
    }
    
    return filtered;
}

function authorIsNotVasja(message) {
    return message.author != 'Vasja';
}

function isShort(message) {
    return message.text.length <= 20;
}

console.log(filter(messages, authorIsNotVasja));
console.log(filter(messages, isShort));