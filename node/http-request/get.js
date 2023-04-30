const https = require('https');

//칭구if
const option = {
    host: '192.168.1.12'
    port: 8000,
    path: 'todos',
    method: 'GET'
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

req.end()

