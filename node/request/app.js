const express = require('express');
const request = require('request');
const CircularJSON = require('circular-json');
const app = express();

app.get('/', (req, res) => {
    res.send("Web Sever Started!");
})


app.get('/hello', (req, res) => {
    res.send("Hello Friend - KANG");
})

//짝궁 ip쓰기
let option = "http://192.168.1.12:8000/hello"

app.get("/rhello", function (req, res) {
    request(option, { json: true }, (err, result, body) => {
        if (err) { return console.log(err) }
        res.send(CircularJSON.stringify(body))
    })
})

const data = JSON.stringify({ todo: 'hihi Im Kang' })
app.get("/data", function (req, res) {
    res.send(data);
})

option = "http://192.168.1.12:8000/data"
app.get("/rdata", function (req, res) {
    request(option, { json: true }, (err, result, body) => {
        if (err) { return console.log(err) }
        res.send(CircularJSON.stringify(body))
    })
})

app.listen(8000, function () {
    console.log('8000 port : Server Started .....')

})










