const mysql = require('./utils/database');
const express = require('express');
const bodyParser = require("body-parser");


const app = express();
app.use(bodyParser.json());

// Landing Page for Bot
app.get('/', (req, res) => {
  res.send(
    'OrangeHouseBot API'
  )
})

app.get('/help', (req, res) => {
  res.send(
    "/create <title> - Creates a new and empty list\n" +
    "/join <your_name> <room_number> - Joins and or updates the current list (type /join again to override your previous entry)\n" +
    "/remove - Removes your current entry\n" +
    "/end - Deletes the current list of names"
  )
})


// Logic for Polling Bot Start

app.get('/poll', (req, res) => {
  mysql.query(
    "SELECT * FROM PollTable",
    (err, results, fields) => {
      if (!err) {
        res.send(results);
      } else {
        console.log(err);
      }
    }
  );
})

app.post('/poll/create', async(req, res) => {
  try {
    const 
  } catch (e) {
    console.log(e.message);
    res.status(500).json({message:e.message})
  }
});





// Logic for Polling Bot End

app.listen(4000);
