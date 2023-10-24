const mysql = require('mysql');
const connection = mysql.createConnection({
  host: 'localhost',
  user: 'root',
  password: process.env.DBPASSWORD,
  database: process.env.DBNAME
});

connection.connect((err) => {
    if (!err) {
      console.log("Connected");
    } else {
      console.log("Connection Failed");
    }
});

module.exports = connection;
