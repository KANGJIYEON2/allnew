const https = require('https');


const data = JSON.stringify({
    todo: '우유사세요'
})

//칭구ip
const option = {
    host: '192.168.1.12',
    port: 8000,
    path: '/todos',
    method: 'POST',
    header: {
        'Content-Type': 'application/json',
        'Content-Length': data.length
    }
}

const req = https.request(option, ress => {
    console.log(`statusCode : ${res.statusCode}`);
    res.on('data', d => {
        process.stdout.write(d);

    })
})


req.on('error', error => {
    console.log(error)
})

req.write(data)
req.end()

