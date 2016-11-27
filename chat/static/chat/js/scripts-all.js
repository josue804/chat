// Note that the path doesn't matter for routing; any WebSocket
// connection gets bumped over to WebSocket consumers

var ws_scheme = window.location.protocol == "https:" ? "wss" : "ws";
var chatsocket = new ReconnectingWebSocket(ws_scheme + '://' + window.location.host + "/chat" + window.location.pathname);
chatsocket.onmessage = function(e) {
  data_array = e.data.split('/')
  text = data_array[0]
  handle = data_array[1]
  $('.scrollbar').append("<div class='chatbox-text--line-sent'>" +
                            "<div class='chatbox-text--line-message-sent'>" +
                              "<p>" +
                                text +
                              "</p>" +
                            "</div>" +
                          "</div>" +
                          "<small class='chatbox-text--author-sent'>" +
                            handle +
                          "</small>")
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

if ($('#condition').length >= 1) {
  new Def.Autocompleter.Search('condition',
  'https://lforms-service.nlm.nih.gov/api/conditions/v3/search');
}

/* ========================================================================
 * Bootstrap: alert.js v3.3.7
 * http://getbootstrap.com/javascript/#alerts
 * ========================================================================
 * Copyright 2011-2016 Twitter, Inc.
 * Licensed under MIT (https://github.com/twbs/bootstrap/blob/master/LICENSE)
 * ======================================================================== */


+function ($) {
  'use strict';

  // ALERT CLASS DEFINITION
  // ======================

  var dismiss = '[data-dismiss="alert"]'
  var Alert   = function (el) {
    $(el).on('click', dismiss, this.close)
  }

  Alert.VERSION = '3.3.7'

  Alert.TRANSITION_DURATION = 150

  Alert.prototype.close = function (e) {
    var $this    = $(this)
    var selector = $this.attr('data-target')

    if (!selector) {
      selector = $this.attr('href')
      selector = selector && selector.replace(/.*(?=#[^\s]*$)/, '') // strip for ie7
    }

    var $parent = $(selector === '#' ? [] : selector)

    if (e) e.preventDefault()

    if (!$parent.length) {
      $parent = $this.closest('.alert')
    }

    $parent.trigger(e = $.Event('close.bs.alert'))

    if (e.isDefaultPrevented()) return

    $parent.removeClass('in')

    function removeElement() {
      // detach from parent, fire event then clean up data
      $parent.detach().trigger('closed.bs.alert').remove()
    }

    $.support.transition && $parent.hasClass('fade') ?
      $parent
        .one('bsTransitionEnd', removeElement)
        .emulateTransitionEnd(Alert.TRANSITION_DURATION) :
      removeElement()
  }


  // ALERT PLUGIN DEFINITION
  // =======================

  function Plugin(option) {
    return this.each(function () {
      var $this = $(this)
      var data  = $this.data('bs.alert')

      if (!data) $this.data('bs.alert', (data = new Alert(this)))
      if (typeof option == 'string') data[option].call($this)
    })
  }

  var old = $.fn.alert

  $.fn.alert             = Plugin
  $.fn.alert.Constructor = Alert


  // ALERT NO CONFLICT
  // =================

  $.fn.alert.noConflict = function () {
    $.fn.alert = old
    return this
  }


  // ALERT DATA-API
  // ==============

  $(document).on('click.bs.alert.data-api', dismiss, Alert.prototype.close)

}(jQuery);
