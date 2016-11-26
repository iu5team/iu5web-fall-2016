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

console.log(messages.filter(message => message.author != 'Vasja'));
console.log(messages.filter(message => message.text.length <= 20));