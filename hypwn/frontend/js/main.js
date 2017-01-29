'use strict';
(function() {
  var BASE_URL = "";

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
      data: JSON.stringify(body),
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


  function makeToggle(name, toggleFunction, getFunction) {
    var inputSelector = 'input[name=' + name + ']';
    var input = $(inputSelector);
    input.click(function() {
      console.log('toggled ' + name);
      var value = input.filter(':checked').val();
      toggleFunction(value == 'on', function(data){
        console.log(JSON.stringify(data));
      });
    });
    return {
      input: input,
      set: toggleFunction,
      get: getFunction
    };
  }

  function makeSensor(name, get) {

  }

  function pollToggles(toggles) {
    Object.keys(toggles).forEach(function(k) {
      var toggle = toggles[k];
      toggle.get(function(data) {
        var state = data['state'];
        var sel = '[value=' + (state ? 'on' : 'off') + ']';
        toggle.input.filter(sel).prop(checked, true);
      });
    });
  }

  function pollSensors(sensors) {

  }

  $(function() {
    var toggles = {
      pump: makeToggle('pump', setPump, getPump),
      light: makeToggle('light', setLight, getLight),
    };

    var sensors = {
      light: makeSensor('light-sensor', getAmbientLight),
    };

    console.log('setup toggles complete');

    setInterval(function() { pollToggles(toggles); }, 1000);
    setInterval(function() { pollSensors(sensors); }, 1000);
  });
})();

