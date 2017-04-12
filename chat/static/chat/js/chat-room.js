var ws_scheme = window.location.protocol == "https:" ? "wss" : "ws";
var chatsocket = new ReconnectingWebSocket(ws_scheme + '://' + window.location.host + "/chat" + window.location.pathname);

function linkify(text) {
    var urlRegex =/(\b(https?|ftp|file):\/\/[-A-Z0-9+&@#\/%?=~_|!:,.;]*[-A-Z0-9+&@#\/%=~_|])/ig;
    return text.replace(urlRegex, function(url) {
        return '<a href="' + url + '" target="_blank">' + url + '</a>';
    });
}

chatsocket.onmessage = function(e) {
  data_array = e.data.split('GqbTvLGBHZ');
  text = data_array[0];
  handle = data_array[1];
  $('.scrollbar').append("<div class='chatbox-text--line-sent'>" +
                            "<div class='chatbox-text--line-message-sent'>" +
                              "<p>" +
                                text +
                              "</p>" +
                            "</div>" +
                            "<small class='chatbox-text--author-sent'>" +
                            handle +
                            "</small>" +
                          "</div>");
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
        var token = $input.attr('token')
        $input.val("");
        $input.height("18px");
        $input.focus();
        anchored_message = anchorme(message, {attributes:[{name:"target", value:"_blank"}]});
        chatsocket.send(anchored_message);
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
    $(document).scrollTop($(document).height());
  },0);
}
