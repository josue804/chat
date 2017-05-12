$(function() {

  if ($('#condition').length > 0) {
    $('document').ready(function(){
      var $roomResults = $('#room-search-results');
      var $roomResultsList = $('#room-search-results-list');

      $('#condition').autocomplete({
        classes: {
          'ui-autocomplete': 'custom-autocomplete',
        },
        source: function(request, response){
          if (request.term != "") {
            data = $.ajax({
              url: window.location.origin + '/chat/room-autocomplete/' + request.term + '/',
              dataType: "json",
              success: function(conditions) {
                response($.map( conditions.splice(0,19), function(condition){
                  return {
                    label: condition.fields.name,
                    extra: {'connections': condition.fields.connections}
                  };
                }));
              }
            });
          }
        }
      }).data( "ui-autocomplete" )._renderItem = function( ul, item ) {
        return $( "<li></li>" )
        .data( "item.autocomplete", item )
        .append('<a>' + item.label + '</a>')
        .append(item.extra.connections ? '<span> | ' + item.extra.connections + ' Active User(s)</span>' : '')
        .appendTo(ul);
      };
    });
  };
});
