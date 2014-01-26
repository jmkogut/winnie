<!doctype html>
<html>
<head>
  <meta charset='utf-8'>
  <meta http-equiv="X-UA-Compatible" content="IE=edge,chrome=1">
  <meta name="viewport" content="width=device-width">

  <title>
      <%block name="title">Somebody forgot to set a title</%block>
  </title>

    <link href='http://fonts.googleapis.com/css?family=Open+Sans:600|Montserrat:700' rel='stylesheet' type='text/css'>
    <link href="/static/style.css" media="screen, projection" rel="stylesheet" type="text/css" />


  <!-- Meta -->
  <meta content="winnie" property="og:title">
  <meta content="An IRC bot with a few features." name="description">

<!--
  <script type="text/javascript" src="script/dotfiles.js"></script>
  -->


    <script type="text/javascript">
         var socket = null;
         var isopen = false;

         window.onload = function() {

             socket = new WebSocket("ws://abzde.com:8888");
            socket.binaryType = "arraybuffer";

            socket.onopen = function() {
               console.log("Connected!");
               isopen = true;
            }

            socket.onmessage = function(e) {
               if (typeof e.data == "string") {
                  console.log("Text message received: " + e.data);
               } else {
                  var arr = new Uint8Array(e.data);
                  var hex = '';
                  for (var i = 0; i < arr.length; i++) {
                     hex += ('00' + arr[i].toString(16)).substr(-2);
                  }
                  console.log("Binary message received: " + hex);
               }
            }

            socket.onclose = function(e) {
               console.log("Connection closed.");
               socket = null;
               isopen = false;
            }
         };

         function sendText() {
            if (isopen) {
               socket.send("Hello, world!");
               console.log("Text message sent.");               
            } else {
               console.log("Connection not opened.")
            }
         };

         function sendBinary() {
            if (isopen) {
               var buf = new ArrayBuffer(32);
               var arr = new Uint8Array(buf);
               for (i = 0; i < arr.length; ++i) arr[i] = i;
               socket.send(buf);
               console.log("Binary message sent.");
            } else {
               console.log("Connection not opened.")
            }
         };
      </script>


</head>
<body>


    <div class="header">
        <nav>
        <ul>
            <li>home</li>
            <li>features</li>
            <li>shit</li>
            <li>musings</li>
            <li>credits</li>
        </ul>
        </nav>
    </div>


    <div class="image">
        <h1>much wow, such oblige</h1>

        <%block name="callout">Default callooot content</%block>
    </div>

    ${self.body()}
</body>
</html>
