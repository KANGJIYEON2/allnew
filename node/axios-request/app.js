const axios = require('axios');
//친구 ip
axios
    .get('http://192.168.1.195:8000/book/selectdata')

    .then(res => {
        console.log(`statusCode : ${res.status}`)
        console.log(res)
    })

    .catch(error => {
        console.log(error)

    })