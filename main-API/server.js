const mysql = require('./utils/database');
const express = require('express');
const bodyParser = require("body-parser");


const app = express();
app.use(bodyParser.json());

// const Poll = require

// Logic for Polling Bot Start

// "HELLOO THEREE! My name is Soyaya, I am the mascot for Orange House! NICE TO MEET EVERYONE!\n\n" +
// "How may I assist yall today? Type in /help for my full list of commands."

// "/create <title> - Creates a new and empty list\n" +
//     "/join <your_name> <room_number> - Joins and or updates the current list (type /join again to override your previous entry)\n" +
//     "/remove - Removes your current entry\n" +
// "/end - Deletes the current list of names")

app.get('/', (req, res) => {
  mysql.query(
    "SELECT * FROM new_table",
    (err, results, fields) => {
      if (!err) {
        res.send(results);
      } else {
        console.log(err);
      }
    }
  );
})

// Logic for Polling Bot End

app.listen(4000);
