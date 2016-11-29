var express = require('express');
var router = express.Router();

var messages = [];

/* GET home page */
router.get('/', function (req, res, next) {
    res.render('index', {
        title: 'Chat'
    });
});

router.post('/api/message', function (req, res, next) {
    messages.push({
        text: req.body.text,
        id: messages.length
    });

    res.sendStatus(200);
});

router.get('/api/new_messages', function (req, res, next) {
    var fromId = req.query.fromId;

    var newMessages = [];
    for (var i = 0; i < messages.length; ++i) {
        if (messages[i].id > fromId) {
            newMessages.push(messages[i]);
        }
    }

    res.json({
        messages: newMessages
    });
});



module.exports = router;
