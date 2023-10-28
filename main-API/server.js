const mysql = require('./utils/database');
const express = require('express');
const bodyParser = require("body-parser");
require('dotenv').config();

process.on('uncaughtException', function (err) {
  console.error(err);
  console.log("Node NOT Exiting...");
});

const app = express();
app.use(bodyParser.json());

// Landing Page for Bot
app.get('/', (req, res) => {
  res.send(
    'OrangeHouseBot API'
  )
})

// Logic for Polling Bot Start

app.get('/poll', async (req, res) => {
  sqlQuery = `SELECT * FROM ${process.env.DB_TABLE_NAME} WHERE chatid = ${req.query['chatid']}`;
  const result = await mysql.query(sqlQuery, function (err, results) {
    if (err) {
      console.log(result);
      res.status(500).send("Error Retreving Existing Poll");
    } else {
      console.log(result);
      res.status(200).send("Results Retreived Successfully");
    }
  });
})

app.post('/poll/create', async(req, res) => {
  sqlQuery = `INSERT INTO ${process.env.DB_TABLE_NAME2} (chatid, polltitle) VALUES (${req.body['chatid']}, '${req.body['polltitle']}')`;
  const poll = await mysql.query(sqlQuery, function (err, results) {
    if (err) {
      console.log(poll);
      res.status(500).send("Error Creating Poll");
    } else {
      console.log(poll);
      res.status(200).send("Poll Successfully Created");
    }
  });
});

app.post('/poll/join', async(req, res) => {
  sqlQuery = `INSERT INTO ${process.env.DB_TABLE_NAME} (name, room, telehandle, chatid) VALUES (${req.query['name']}, ${req.query['room']}, ${req.query['telehandle']}, ${req.query['chatid']})`;
  const join = await mysql.query(sqlQuery, function (err, results) {
    if (err) {
      console.log(join);
      res.status(500).send("Error Joining Poll");
    } else {
      console.log(join);
      res.status(200).send("Joined Poll Successfully");
    }
  });
});

app.delete('/poll/delete', async(req, res) => {
  sqlQuery = `DELETE FROM ${process.env.DB_TABLE_NAME2} WHERE chatid = ${req.query['chatid']}`;
  const join = await mysql.query(sqlQuery, function (err, results) {
    if (err) {
      console.log(join);
      res.status(500).send("Error Deleting Poll");
    } else {
      console.log(join);
      res.status(200).send("Poll Deleted Successfully");
    }
  });
})

// Logic for Polling Bot End

app.listen(4000);
