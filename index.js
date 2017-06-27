'use strict';

var express = require('express');
var app = express();
var http = require('http').Server(app);
var io = require('socket.io')(http);
var fs = require('fs');
var path = require('path');
 
var spawn = require('child_process').spawn;
var proc;

var PythonShell = require('python-shell');
var pShell = new PythonShell('uex_controller.py');

app.use('/', express.static(path.join(__dirname, 'stream')));
app.use('/scripts', express.static(path.join(__dirname, 'scripts')));
 
app.get('/', function(req, res) {
  res.sendFile(__dirname + '/index.html');
});
 
var sockets = {};
 
io.on('connection', function(socket) {
 
  sockets[socket.id] = socket;
  console.log("Total clients connected : ", Object.keys(sockets).length);
 
  socket.on('disconnect', function() {
    delete sockets[socket.id];
 
    // no more sockets, kill the stream
    if (Object.keys(sockets).length == 0) {
      app.set('watchingFile', false);
      if (proc) proc.kill();
      fs.unwatchFile('./stream/image_stream.jpg');
    }
  });
 
  socket.on('start-stream', function() {
    startStreaming(io);
  });
  
  socket.on('test-move', function(){
	testMove();
  });
  
  socket.on('up-move', function(){
	console.log("up node");
	step('up');
  });
  
  socket.on('down-move', function(){
	step('down');
  });
  
  socket.on('left-move', function(){
	step('left');
  });
  
  socket.on('right-move', function(){
	step('right');
  });
  
 
});
 
http.listen(3000, function() {
  console.log('listening on *:3000');
});
 
function stopStreaming() {
  if (Object.keys(sockets).length == 0) {
    app.set('watchingFile', false);
    if (proc) proc.kill();
    fs.unwatchFile('./stream/image_stream.jpg');
  }
}
 
function startStreaming(io) {
 
  if (app.get('watchingFile')) {
    io.sockets.emit('liveStream', 'image_stream.jpg?_t=' + (Math.random() * 100000));
    return;
  }
 
  var args = ["-w", "1920", "-h", "1080", "-o", "./stream/image_stream.jpg", "-t", "999999999", "-tl", "70"];
  proc = spawn('raspistill', args);
 
  console.log('Watching for changes...');
 
  app.set('watchingFile', true);
 
  fs.watchFile('./stream/image_stream.jpg', function(current, previous) {
    io.sockets.emit('liveStream', 'image_stream.jpg?_t=' + (Math.random() * 100000));
  })
 
}

function testMove() {
	PythonShell.run('test.py', function(err){
		if(err) throw err;
		console.log('done');
	})
}


function step(dir){
	console.log("sending command");
	pShell.send(dir);
}
