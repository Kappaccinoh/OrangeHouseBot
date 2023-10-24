const express = require('express');
const app = express();
const PORT = 8080;

const mysql = require('mysql');
const connection = mysql.createConnection({
  host: '',
  user: '',
  password: '',
  database: ''
});

connection.connect()

connection.query('SELECT 1 + 1 AS solution', (err, rows, fields) => {
    if (err) throw err;
    console.log('The solution is: ', rows[0].solution);
});
  
app.listen();