const mysql = require('./utils/database');
const express = require('express');
const bodyParser = require("body-parser");
require('dotenv').config();

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
  try {
    sqlQuery = `SELECT * FROM ${process.env.DB_TABLE_NAME} WHERE chatid = ${req.query['chatid']}`;
    const result = await mysql.query(sqlQuery);
    res.status(200).json(result)
  } catch (e) {
    console.log(e.message);
    return res.status(500).json({message:e.message});
  }
})

app.post('/poll/create', async(req, res) => {
  try {
    sqlQuery = `INSERT INTO ${process.env.DB_TABLE_NAME2} (chatid, polltitle) VALUES (${req.body['chatid']}, '${req.body['polltitle']}')`;
    const result = await mysql.query(sqlQuery)
    res.status(200).json({message:"Success"})
  } catch (e) {
    console.log(e.message);
    res.status(500).json({message:e.message});
  }
});

app.post('/poll/join', async(req, res) => {
  try {
    sqlQuery = `INSERT INTO ${process.env.DB_TABLE_NAME} (name, room, telehandle, chatid) VALUES (${req.query['name']}, ${req.query['room']}, ${req.query['telehandle']}, ${req.query['chatid']})`;
    const result = await mysql.query(sqlQuery)
    res.status(200).json(result);
  } catch (e) {
    console.log(e.message);
    return res.status(500).json({message:e.message});
  }
});

app.delete('/poll/delete', async(req, res) => {
  try {
    sqlQuery = `DELETE FROM ${process.env.DB_TABLE_NAME2} WHERE chatid = ${req.query['chatid']}`;
    const result = await mysql.query(sqlQuery)
    res.status(200).json(result);
  } catch (e) {
    console.log(e.message);
    return res.status(500).json({message:e.message});
  }
})

// Logic for Polling Bot End

app.listen(4000);
