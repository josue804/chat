// Note that the path doesn't matter for routing; any WebSocket
// connection gets bumped over to WebSocket consumers
socket = new WebSocket("ws://" + window.location.host + "/chat/");
socket.onmessage = function(e) {
    $('.scrollbar').append("<div class='chatbox-text--line-sent'>" +
                              "<p>" +
                                e.data +
                              "</p>" +
                            "</div>" +
                            "<p class='chatbox-text--author-sent'><strong>Josue at 2:30PM</strong></p>")
    $('.scrollbar').animate({scrollTop: $('.scrollbar').prop("scrollHeight")}, 500);
}

socket.onopen = function() {
    $(document).ready(function() {
      $(".chatbox-form").submit(function(e){
        e.preventDefault();
        var $input = $(".chatbox-form--input")
        var message = $input.val().replace(/\n/g,"<br>");
        $input.val("");
        $input.height("18px");
        $input.focus()
        socket.send(message)
      });
    });
}
// Call onopen directly if socket is already open
if (socket.readyState == WebSocket.OPEN) socket.onopen();

var textarea = document.querySelector('textarea');

textarea.addEventListener('keydown', autosize);

function autosize(){
  var el = this;
  setTimeout(function(){
    el.style.cssText = 'height:auto; padding:20px';
    // for box-sizing other than "content-box" use:
    // el.style.cssText = '-moz-box-sizing:content-box';
    el.style.cssText = 'height:' + el.scrollHeight  + 'px';
  },0);
}
