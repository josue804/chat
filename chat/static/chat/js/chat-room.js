$(function() {
  var ws_scheme = window.location.protocol == "https:" ? "wss" : "ws";
  var chatsocket = new ReconnectingWebSocket(ws_scheme + '://' + window.location.host + "/chat" + window.location.pathname);

  function linkify(text) {
      var urlRegex =/(\b(https?|ftp|file):\/\/[-A-Z0-9+&@#\/%?=~_|!:,.;]*[-A-Z0-9+&@#\/%=~_|])/ig;
      return text.replace(urlRegex, function(url) {
          return '<a href="' + url + '" target="_blank">' + url + '</a>';
      });
  }

  chatsocket.onmessage = function(e) {
    var dataArray = e.data.split('GqbTvLGBHZ');
    var text = dataArray[0];
    var formattedHandle = dataArray[1];
    var handle = dataArray[2];
    var messageType = 'received'
    if (handle == $('.user-username').text()) {
      var messageType = 'sent';
    }
    $('.scrollbar').append("<div class='chatbox-text--line-"+ messageType +"'>" +
                              "<div class='chatbox-text--line-message-"+ messageType +"'>" +
                                "<p>" +
                                  text +
                                "</p>" +
                              "</div>" +
                              "<small class='chatbox-text--author-"+ messageType +"'>" +
                              formattedHandle +
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
          var anchoredMessage = anchorme(message, {attributes:[{name:"target", value:"_blank"}]});
          chatsocket.send(anchoredMessage);
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

  $('.chatbox-form--input').keypress(function(e) {
    if (e.which == 13 && !e.shiftKey) {
      $(e.target).submit();
      return false;
    }
  });

  $('body').on('click', '.subscribe-link', function(e) {
    var room = e.target.dataset.room;
    $.ajax({
      url: window.location.origin + '/chat/room-subscribe/' + room + '/',
      success: function(result) {
        $('.subscribe-link')
          .addClass('unsubscribe-link')
          .removeClass('subscribe-link')
          .off('active')
          .text('Unsubscribe');
      },
      error: function(result) {
        alert('Failed to subscribe, please try again later.');
      },
    });
  });

  $('body').on('click', '.unsubscribe-link', function(e) {
    var room = e.target.dataset.room;
    $.ajax({
      url: window.location.origin + '/chat/room-unsubscribe/' + room + '/',
      success: function(result) {
        $('.unsubscribe-link')
          .addClass('subscribe-link')
          .removeClass('unsubscribe-link')
          .off('active')
          .text('Subscribe');
      },
      error: function(result) {
        alert('Failed to unsubscribe, please try again later.');
      },
    });
  });
});
