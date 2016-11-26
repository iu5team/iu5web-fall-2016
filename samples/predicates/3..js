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

function authorIsNotVasja(message) {
    return message.author != 'Vasja';
}

function isShort(message) {
    return message.text.length <= 20;
}

console.log(messages.filter(authorIsNotVasja));
console.log(messages.filter(isShort));