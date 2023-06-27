const express = require('express');
const morgan = require('morgan');
const path = require('path');
const bodyParser = require('body-parser');
const cookieParser = require('cookie-parser');
const mysql = require('mysql2/promise');
const env = require('dotenv').config({ path: "../../.env" });
const app = express();

const port = process.env.PORT || 8000;
app.set('port', port);
app.use(morgan('dev'));
app.use(bodyParser.json());
app.use(bodyParser.urlencoded({ extended: false }));
app.use(cookieParser());
app.use(express.static(path.join(__dirname, 'public')));

let pool;

async function setupConnection() {
    try {
        pool = mysql.createPool({
            host: process.env.host,
            user: process.env.user,
            password: process.env.password,
            database: process.env.database,
            waitForConnections: true,
            connectionLimit: 10,
            queueLimit: 0
        });
    } catch (error) {
        console.error('Error setting up database connection:', error);
        throw error;
    }
}

app.get('/image/_figure:year', async (req, res) => {
    const year = req.params.year;
    let imageName;

    if (year === 'total') {
        imageName = 'combined_figure';
    } else {
        imageName = `figure_${year}`;
    }

    console.log('Image name:', imageName);

    try {
        const sqlQuery = 'SELECT * FROM images WHERE name = ?';
        console.log('Executing query:', sqlQuery, imageName);
        /* MySQL 데이터베이스에 연결하고, SQL 쿼리를 실행한 후 연결을 해제.*/
        const connection = await pool.getConnection();
        const [results] = await connection.query(sqlQuery, [imageName]);
        connection.release();

        console.log('DB Results:', results);

        if (results.length === 0) {
            res.status(404).send('Image Not Found');
            return;
        }

        console.log('Image Name:', results[0].name);
        console.log('Image Data:', results[0].data);

        const imageData = results[0].data;
        /* buffer ---> 이미지 임시저장 바이너리 데이터 효과적 처리가능 */
        const imageBuffer = Buffer.from(imageData, 'base64');

        res.writeHead(200, {
            'Content-Type': 'image/png',
            'Content-Length': imageBuffer.length
        });

        res.end(imageBuffer);
    } catch (error) {
        console.error('Error executing query:', error);
        res.status(500).send('Internal Server Error');
    }
});

app.get('/image/piechart:year', async (req, res) => {
    const year = req.params.year;
    let imageName;

    if (year === 'total') {
        imageName = 'combined_pie_chart';
    } else {
        imageName = `pie_chart_${year}`;
    }

    console.log('Image name:', imageName);

    try {
        const sqlQuery = 'SELECT * FROM images WHERE name = ?';
        console.log('Executing query:', sqlQuery, imageName);

        const connection = await pool.getConnection();
        const [results] = await connection.query(sqlQuery, [imageName]);
        connection.release();

        console.log('DB Results:', results);

        if (results.length === 0) {
            res.status(404).send('Image Not Found');
            return;
        }

        console.log('Image Name:', results[0].name);
        console.log('Image Data:', results[0].data);

        const imageData = results[0].data;
        const imageBuffer = Buffer.from(imageData, 'base64');

        res.writeHead(200, {
            'Content-Type': 'image/png',
            'Content-Length': imageBuffer.length
        });

        res.end(imageBuffer);
    } catch (error) {
        console.error('Error executing query:', error);
        res.status(500).send('Internal Server Error');
    }
});





setupConnection().then(() => {
    app.listen(app.get('port'), () => {
        console.log(port, 'Port: Server Started...');
    });
}).catch((err) => {
    console.log('Error starting server:', err);
});
