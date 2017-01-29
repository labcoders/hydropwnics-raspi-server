'use strict';
(function() {
  var BASE_URL = "http://localhost:5000";

  function routeUrl(r) {
    return BASE_URL + r
  }

  function get(route, success) {
    return $.get({
      url: routeUrl(route),
      success: success,
    });
  }

  function post(route, body, success) {
    return $.post({
      url: routeUrl(route),
      data: body,
      contentType: 'application/json',
      success: success,
    });
  }

  function setPump(state, success) {
    return post('/pump', {state: state}, success);
  }

  function getPump(success) {
    return get('/pump');
  }

  function setLight(state, success) {
    return post('/light/internal', {state: state}, success);
  }

  function getLight(success) {
    return get('/light/internal', success);
  }

  function getAmbientLight(success) {
    return get('/light/ambient', success);
  }

  function makeToggle(toggleFunction, name) {
    var inputSelector = 'input[name=' + name + ']';
    var input = $(inputSelector);
    input.click() {
      var value = input.filter(':checked').val();
      toggleFunction(value == 'on', success);
  }

  $(function() {
    $("input[name=pump]").click(function() {
      var value = $("input[name=pump]:checked").val();
    });
  });
});

