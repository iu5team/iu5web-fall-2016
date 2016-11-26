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

console.log(messages.filter(function authorIsNotVasja(message) {
    return message.author != 'Vasja';
}));

console.log(messages.filter(function isShort(message) {
    return message.text.length <= 20;
}));