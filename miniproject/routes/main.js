const express = require('express');
const bodyParser = require('body-parser');
const mysql = require('sync-mysql');
const env = require('dotenv').config({ path: "../.env" });
const morgan = require('morgan');
const fs = require('fs');
const path = require('path');
const mongoClient = require('mongodb').MongoClient;

const app = express();

app.set('port', process.env.Port || 8000);
app.use(morgan('dev'));

var db;
var databaseUrl = "mongodb://192.168.1.77:27017";
app.get('/', (req, res) => {
  res.redirect('loginpage.html')
})

const axios = require('axios');
const { kStringMaxLength } = require('buffer');

//*
axios.get('http://192.168.1.195:8000/book/selectdata')
  .then(res => {
    console.log(`statusCode : ${res.status}`)
    console.log(res)
  })

  .catch(error => {
    console.log(error)

  })


var connection = new mysql({
  host: process.env.host,
  user: process.env.user,
  password: process.env.password,
  database: process.env.database
});


app.use(bodyParser.json());
app.use(bodyParser.urlencoded({ extended: false }));
app.use(express.json());
app.use(express.urlencoded({ extended: true }));



app.post('/login', (req, res) => {
  const { US_ID, US_PW } = req.body;
  const result = connection.query("SELECT * FROM USERTBL WHERE US_ID=? AND US_PW=?", [US_ID, US_PW]);

  if (result.length == 0) {
    res.redirect('error.html');
    return;
  }

  if (US_ID == 100 || US_ID == 101) {
    console.log(US_ID + " => Administrator Logined");
    res.redirect('adminpage.html?US_ID=' + US_ID);
    return;
  }

  console.log(US_ID + " => User Logined");
  res.sendFile(__dirname + '/mainpage.html');

  if (result.length > 0) {
    res.redirect("http://192.168.1.195:8000/main.html")
  } else {
    res.redirect('"http://192.168.1.195:8000/error.html"');
  }
});

app.get('/hello', (req, res) => {
  res.send('관리자페이지 입니다!')
})

app.get('/select', (req, res) => {
  const result = connection.query('select * from USERTBL', []);
  console.log(result);

  res.writeHead(200);
  var template = `
    <!doctype html>
    <html>
      <head>
        <title>Result</title>
        <meta charset="utf-8">
      </head>
      <body>
        <table border="1" style="margin:auto; text-align:center;">
          <thead>
            <tr>
              <th>User ID</th>
              <th>Name</th>
              <th>Birth</th>
              <th>Address</th>
              <th>Mobile Number</th>
              <th>Home Number</th>
              <th>Join</th>
              <th>Password</th>
            </tr>
          </thead>
          <tbody>
    `;
  for (var i = 0; i < result.length; i++) {
    template += `
            <tr>
              <td>${result[i]['US_ID']}</td>
              <td>${result[i]['US_NAME']}</td>
              <td>${result[i]['US_Birth']}</td>
              <td>${result[i]['US_addr']}</td>
              <td>${result[i]['US_M_NUM']}</td>
              <td>${result[i]['US_H_NUM']}</td>
              <td>${result[i]['US_Join']}</td>
              <td>${result[i]['US_PW']}</td>
            </tr>
      `;
  }
  template += `
          </tbody>
        </table>
      </body>
    </html>
    `;
  res.write(template);
  res.end();
  return;
});

app.post('/joinpage', (req, res) => {
  res.redirect('/joinpage.html')
})

// request 1, query 1
app.post('/selectQuery', (req, res) => {
  const US_ID = req.body.US_ID;
  const result = connection.query("select * from USERTBL where US_ID=?", [US_ID]);
  console.log(result);
  res.send(result);
})


app.get('/selectQuery', (req, res) => {
  const US_ID = req.query.US_ID;
  console.log(US_ID);
  const result = connection.query("select * from USERTBL where US_ID=?", [US_ID]);
  res.writeHead(200);
  var template = `
    <!doctype html>
    <html>
      <head>
        <title>Result</title>
        <meta charset="utf-8">
      </head>
      <body>
        <table border="1" style="margin:auto; text-align:center;">
          <thead>
            <tr>
              <th>User ID</th>
              <th>Name</th>
              <th>Birth</th>
              <th>Address</th>
              <th>Mobile Number</th>
              <th>Home Number</th>
              <th>Join</th>
              <th>Password</th>
            </tr>
          </thead>
          <tbody>
    `;
  for (var i = 0; i < result.length; i++) {
    template += `
            <tr>
              <td>${result[i]['US_ID']}</td>
              <td>${result[i]['US_NAME']}</td>
              <td>${result[i]['US_Birth']}</td>
              <td>${result[i]['US_addr']}</td>
              <td>${result[i]['US_M_NUM']}</td>
              <td>${result[i]['US_H_NUM']}</td>
              <td>${result[i]['US_Join']}</td>
              <td>${result[i]['US_PW']}</td>
            </tr>
            `;
  }
  template += `
              </tbody>
            </table>
          </body>
        </html>
        `;
  res.write(template);
  res.end();
  return;
});

//회원가입을 위한 insert구문

app.post('/insert', (req, res) => {
  const { US_ID, US_NAME, US_Birth, US_addr, US_M_NUM, US_H_NUM, US_Join, US_PW } = req.body;
  const result = connection.query('insert into USERTBL values (?, ?, ?, ?, ?, ?, ?, ?)', [US_ID, US_NAME, US_Birth, US_addr, US_M_NUM, US_H_NUM, US_Join, US_PW]);
  console.log(result);
  res.send("http://192.168.1.195:8000/main.html");
});


app.post('/update', (req, res) => {
  let { US_ID, US_PW } = req.body;
  const result = connection.query("update USERTBL set US_PW=? where US_ID=?", [String(US_PW), String(US_ID)]);
  console.log(result);
  if (result.affectedRows > 0) {
    res.write('회원수정 완료');
  } else {
    res.write('회원수정 실패');
  }
  res.end();
  return;
});


app.post('/delete', (req, res) => {
  const US_ID = req.body.US_ID;
  const result = connection.query('delete from USERTBL where US_ID=?', [US_ID]);
  console.log(result);
  res.redirect('/select');
});



module.exports = app;
