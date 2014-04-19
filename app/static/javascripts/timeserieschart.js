function financechart () {

  var
    container = document.getElementById('charts'),
    options;

  options = {
    container : container,
    data : {
      detail : financeData.price,
      summary : financeData.price
    },
    // An initial selection
    selection : {
      data : {
        x : {
          min : 100,
          max : 200
        }
      }
    }
  };

  new envision.templates.TimeSeries(options);
}