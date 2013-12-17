function financechart () {

  var
    V = envision,
    container = document.getElementById('charts'),
    summaryTicks = financeData.summaryTicks,
    options, vis;

  options = {
    container : container,
    data : {
      price : financeData.price,
      volume : financeData.volume,
      summary : financeData.price
    },
    trackFormatter : function (o) {

      var
        data = o.series.data,
        index = data[o.index][0],
        value;

      value = summaryTicks[index].date + ': $' + summaryTicks[index].close + ", Vol: " + summaryTicks[index].volume;

      return value;
    },
    xTickFormatter : function (index) {
      var date = new Date(financeData.summaryTicks[index].date);
      return date.getFullYear() + '';
    },

    price : {
      config : {
        'lite-lines' : {
          lineWidth : 1,
          show : true,
          fill : true,
          fillOpacity : 0.2

        },
        mouse : {
          track: true,
          trackY: false,
          trackAll: true,
          sensibility: 1,
          trackDecimals: 4,
          position: 'ne'
        },
        yaxis : { 
          autoscale : true,
          autoscaleMargin : 0.05,
          noTicks : 4,
          showLabels : true,
          min : undefined
        }
      }
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

  vis = new envision.templates.Finance(options);
}
