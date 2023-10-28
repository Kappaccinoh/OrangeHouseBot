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

// app.get('/poll', async (req, res, next) => {
//   try {
//     sqlQuery = `SELECT * FROM ${process.env.DB_TABLE_NAME} WHERE chatid = ${req.query['chatid']}`;
//     const result = await mysql.query(sqlQuery);
//     res.json(result);
//   } catch (e) {
//     console.log(e.message);
//     return next(e);
//   }
// })

app.post('/poll/create', async(req, res, next) => {
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

// app.post('/poll/join', async(req, res, next) => {
//   try {
//     sqlQuery = `INSERT INTO ${process.env.DB_TABLE_NAME} (name, room, telehandle, chatid) VALUES (${req.query['name']}, ${req.query['room']}, ${req.query['telehandle']}, ${req.query['chatid']})`;
//     const result = await mysql.query(sqlQuery)
//     res.json(result);
//   } catch (e) {
//     console.log(e.message);
//     return next(e);
//   }
// });

// app.delete('/poll/delete', async(req, res, next) => {
//   try {
//     sqlQuery = `DELETE FROM ${process.env.DB_TABLE_NAME2} WHERE chatid = ${req.query['chatid']}`;
//     const result = await mysql.query(sqlQuery)
//     res.json(result);
//   } catch (e) {
//     console.log(e.message);
//     return next(e);
//   }
// })

// Logic for Polling Bot End

app.listen(4000);
