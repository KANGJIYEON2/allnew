const express = require('express');
const bodyParser = require('body-parser');
const mysql = require('sync-mysql');
const env = require('dotenv').config({ path: "../../.env" });

var connection = new mysql({
    host: process.env.host,
    user: process.env.user,
    password: process.env.password,
    database: process.env.database
});

const app = express()

app.use(bodyParser.json());
app.use(bodyParser.urlencoded({ extended: false }));
app.use(express.json());
app.use(express.urlencoded({ extended: true }));

app.get('/hello', (req, res) => {
    res.send('Hello World~!!')
})

app.get('/select', (req, res) => {
    const result = connection.query('select * from usertbl');
    console.log(result);
    res.send(result);
})

app.post('/select', (req, res) => {
    const result = connection.query('select * from usertbl');
    console.log(result);
    res.send(result);
})

// request 1, query 1
app.post('/selectQuery', (req, res) => {
    const userid = req.body.userid;
    const result = connection.query("select * from usertbl where userid=?", [userid]);
    console.log(result);
    res.send(result);
})


app.get('/selectQuery', (req, res) => {
    const userid = req.query.userid;
    console.log(userid);
    const result = connection.query("select * from usertbl where userid=?", [userid]);
    console.log(result);
    res.send(result);
})


// request 1, query 1
app.post('/insert', (req, res) => {
    const userid = req.body.userid;
    const brith = req.body.brith;
    const addr = req.body.addr;
    const phone_num = req.body.phone_num;
    const use_pur = req.body.use_pur;
    const price = req.body.price;
    const platform_sc = req.body.platform_sc;
    const result = connection.query('insert into usertbl values (?, ?, ?, ?, ?, ?, ?)', [userid, brith, addr, phone_num, use_pur, price, platform_sc]);
    console.log(result);
    res.redirect('/selectQuery?userid=' + req.body.userid);
})

app.post('/update', (req, res) => {
    const userid = req.body.userid;
    const brith = req.body.brith;
    const addr = req.body.addr;
    const phone_num = req.body.phone_num;
    const use_pur = req.body.use_pur;
    const price = req.body.price;
    const platform_sc = req.body.platform_sc;
    const result = connection.query('update usertbl set brith=?, addr=?, phone_num=?, use_pur=?, price=?, platform_sc=? where userid=?', [brith, addr, phone_num, use_pur, price, platform_sc, userid]);
    console.log(result);
    res.redirect('/selectQuery?userid=' + req.body.userid);
})

app.post('/delete', (req, res) => {
    const userid = req.body.userid;
    const result = connection.query('delete from usertbl where userid=?', [userid]);
    console.log(result);
    res.redirect('/select');
})


module.exports = app;
