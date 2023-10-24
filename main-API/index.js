const express = require('express');

const app = express();
const PORT = 8080;

const Poll = require




// Logic for Polling Bot Start

app.get('/', (req, res) => {
  res.send(
    "HELLOO THEREE! My name is Soyaya, I am the mascot for Orange House! NICE TO MEET EVERYONE!\n\n" +
    "How may I assist yall today? Type in /help for my full list of commands.")
})

app.get('/help', (req, res) => {
  res.send(
    "/create <title> - Creates a new and empty list\n" +
    "/join <your_name> <room_number> - Joins and or updates the current list (type /join again to override your previous entry)\n" +
    "/remove - Removes your current entry\n" +
    "/end - Deletes the current list of names")
})

app.get('/poll/create', (req, res) => {
  try {
    const poll = await 
  }
})


// Logic for Polling Bot End


app.listen();
