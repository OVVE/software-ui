var express = require('express');
var app = express();
var http = require('http').createServer(app);
var io = require('socket.io')(http);
var SerialPort = require("serialport");
var serialport = new SerialPort("/dev/cu.usbmodem14201",{baudRate: 9600});



app.get('/', function(req, res){
  res.sendFile(__dirname + '/public/index.html');
});


io.on('connection', function(socket){
	// list values here emit broadcasts
	
	socket.on('mode', function(modedata){
    io.emit('mode', modedata);
    console.log("Mode changed to: " + modedata);
  });
});

// Serial port connection

serialport.on('open', function(){
  console.log('Serial Port Opened');
  serialport.on('data', function(data){
 // console.log(data[0]);
 // io.emit('data', data[0]);

  });
});

// Set static folder for assets
app.use(express.static(__dirname + '/public'));

http.listen(3000, function(){
  console.log('listening on *:3000');
});


