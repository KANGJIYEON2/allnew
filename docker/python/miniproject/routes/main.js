const express = require('express');
const bodyParser = require('body-parser');
const mysql = require('sync-mysql');
const env = require('dotenv').config({ path: "../.env" });
const morgan = require('morgan');
const fs = require('fs');
const path = require('path');
const mongoClient = require('mongodb').MongoClient;

const app = express();

app.set('port', process.env.PORT || 8000);
app.use(morgan('dev'));

var db;
var databaseUrl = "mongodb://192.168.1.77:27017";
app.get('/', (req, res) => {
  res.redirect('firstpage.html')
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



module.exports = app;
