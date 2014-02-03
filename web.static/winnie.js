var socket = null;
var isopen = false;

window.onload = function() {

                function scr(){
                    var el = $$('div.fill')[0];
                    el.show();
                    el.scrollTop = el.scrollHeight; // auto-scroll
                }

                $$('div.fill')[0].hide();
                new Ajax.Request( "/static/filler.html", {
                        method: 'get',
                        onSuccess: function (trans) {
                            var content = trans.responseText || "";

                            var el = document.getElementsByClassName('fill')[0];
                            el.innerHTML = content;
                            el.innerHTML += "<br /><br /><br />";
                            el.innerHTML += "<br /><hr /><br />";

                            scr.delay(0.65);
                        }});

            socket = new WebSocket("ws://abzde.com:8888");
            socket.binaryType = "arraybuffer";

            socket.onopen = function() {
               console.log("Connected!");
               isopen = true;
            }

            socket.onmessage = function(e) {
                console.log("We got some datas.");
                console.log(e.data);

               if (typeof e.data == "string") {
                  console.log("Text message received: " + e.data);
                  var obj = JSON.parse(e.data);
                  if (obj.hasOwnProperty('irc_event')) {
                      var el = document.getElementsByClassName('fill')[0];
                      el.innerHTML += "<br /><br />" + obj.irc_event;
                      scr.delay(0.45);

                  } else if (obj.hasOwnProperty("irc_names")) {
                        var sb = document.getElementsByClassName('sidebar')[0];
                        //sb.innerHTML = "";
                        obj.irc_names.each(function(n){
                            sb.innerHTML += n + "<br />";
                        });
                  }
               }
            };

        socket.onerror = function(e) {
               console.log("ERR: "+e);
         };

        socket.onclose = function(e) {
               console.log("Connection closed.");
               socket = null;
               isopen = false;
         };

         function sendText( txt ) {
            if (isopen) {
                socket.send(txt);
               console.log("Text message sent.");               
            } else {
               console.log("Connection not opened.")
            }
         };
};
