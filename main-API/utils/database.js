const mysql = require('mysql');
require('dotenv').config()

const connection = mysql.createConnection({
  host: process.env.DB_HOST,
  user: process.env.DB_USER,
  password: process.env.DB_PASSWORD,
  database: process.env.DB_NAME,
  port: process.env.DB_PORT
});


connection.connect((err) => {
    if (!err) {
      console.log("Connected");
    } else {
      throw err;
    }
});

module.exports = connection;
