const mysql = require('./utils/database');
const express = require('express');
const bodyParser = require("body-parser");
const CircularJSON = require('circular-json');
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
  chatid = parseInt(req.body['chatid'])
  sqlQuery = `SELECT * FROM ${process.env.DB_TABLE_NAME} WHERE chatid=${chatid}`;
  const result = await mysql.query(sqlQuery, function (err, results) {
    
    if (err) {
      console.log(result);
      res.status(500).send("Error Retreving Existing Poll");
    } else {
      console.log(results)
      res.status(200).send(results);
    }
  });
})

app.get('/poll/getTitle', async (req, res) => {
  sqlQuery = `SELECT polltitle FROM ${process.env.DB_TABLE_NAME2} WHERE chatid=${chatid}`;
  const result = await mysql.query(sqlQuery, function (err, results) {
    if (err) {
      console.log(result);
      res.status(500).send("Error Retreving Poll Title");
    } else {
      console.log(results)
      res.status(200).send(results);
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
  sqlQuery = `INSERT INTO ${process.env.DB_TABLE_NAME} (name, room, telehandle, chatid) ` +
    `VALUES ('${req.body['name']}', '${req.body['room']}', '${req.body['telehandle']}', ${req.body['chatid']}) ` +
    `ON DUPLICATE KEY UPDATE ` +
    `name = VALUES(name), ` +
    `room = VALUES(room), ` +
    `telehandle = VALUES(telehandle), ` +
    `chatid = VALUES(chatid);`
  

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

app.delete('/poll/remove', async(req, res) => {
  sqlQuery = `DELETE FROM ${process.env.DB_TABLE_NAME} WHERE telehandle='${req.body['telehandle']}' AND chatid=${req.body['chatid']}`
  const remove = await mysql.query(sqlQuery, function (err, results) {
    if (err) {
      console.log(remove);
      res.status(500).send("Error Removing Entry From Poll");
    } else {
      console.log(remove);
      res.status(200).send("Removed Entry From Poll Successfully");
    }
  });
});

app.delete('/poll/delete', async(req, res) => {
  sqlQuery = `DELETE FROM ${process.env.DB_TABLE_NAME2} WHERE chatid=${req.body['chatid']}`;
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
