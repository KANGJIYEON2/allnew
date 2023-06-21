var express = require('express');
var mysql = require('mysql');
const env = require('dotenv').config({ path: "./.env" });

var connection = mysql.createConnection({
    host: process.env.host,
    user: process.env.user,
    port: process.env.port,
    password: process.env.password,
    database: process.env.database
});

var app = express();

connection.connect(function(err) {
    if (!err) {
        console.log("Database is connected....\n\n");
    } else {
        console.log("Error connecting Database....\n\n");
    }
});

app.get('/', function(req, res){
    connection.query('SELECT * FROM st_info', function(err, rows, fields){
        if(!err) {
            var template = `
                <table border="20"  style="margin:auto; text-align:center;">
                <tr>
                    <th> id </th>
                    <th> name </th>
                    <th> dept  </th>
                </tr>`;
            rows.forEach((row) => {
                template += `
                <tr>
                    <td> ${row.ST_ID} </td>
                    <td> ${row.NAME} </td>
                    <td> ${row.DEPT} </td>
                </tr>`;
            });
            template += `</table>`;
            res.send(template);
        } else {
            console.log('Error while performing Query.');
            res.status(500).send('Error while performing Query.');
        }
    });
});

app.listen(8000, function() {
    console.log('Server started on port 8000...');
});
