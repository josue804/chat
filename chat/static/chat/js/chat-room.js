// Note that the path doesn't matter for routing; any WebSocket
// connection gets bumped over to WebSocket consumers

var ws_scheme = window.location.protocol == "https:" ? "wss" : "ws";
var chatsocket = new ReconnectingWebSocket(ws_scheme + '://' + window.location.host + "/chat" + window.location.pathname);
chatsocket.onmessage = function(e) {
  data_array = e.data.split('/')
  text = data_array[0]
  handle = data_array[1]
  $('.scrollbar').append("<div class='chatbox-text--line-sent'>" +
                            "<p>" +
                              text +
                            "</p>" +
                          "</div>" +
                          "<p class='chatbox-text--author-sent'><strong>" +
                            handle +
                          "</strong></p>")
  $('.scrollbar').animate({scrollTop: $('.scrollbar').prop("scrollHeight")}, 500);
}

chatsocket.onopen = function() {
  if ($('.chatbox-text').length < 1) {
    return false;
  }
    $(document).ready(function() {
      $('.scrollbar')[0].scrollTop = $('.scrollbar')[0].scrollHeight;
      $(".chatbox-form").submit(function(e){
        e.preventDefault();
        var $input = $(".chatbox-form--input")
        var message = $input.val().replace(/\n/g,"<br>");
        $input.val("");
        $input.height("18px");
        $input.focus();
        chatsocket.send(message);
      });
    });
  var textarea = document.querySelector('textarea');
  textarea.addEventListener('keydown', autosize);
}
// Call onopen directly if chatsocket is already open
if (chatsocket.readyState == WebSocket.OPEN) chatsocket.onopen();


function autosize(){
  var el = this;
  setTimeout(function(){
    el.style.cssText = 'height:auto; padding:20px';
    el.style.cssText = 'height:' + el.scrollHeight  + 'px';
  },0);
}
