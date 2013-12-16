function financechart () {

  var financeData = {
  'summaryTicks': [{"date":"August 19, 2004","open":100.01,"high":104.06,"low":95.96,"close":100.34,"volume":22088000},
  {"date":"August 19, 2004","open":120.01,"high":104.06,"low":95.96,"close":102.34,"volume":23088000},
  {"date":"August 19, 2004","open":120.01,"high":104.06,"low":95.96,"close":103.34,"volume":23088000},
  {"date":"August 19, 2004","open":120.01,"high":104.06,"low":95.96,"close":104.34,"volume":23088000},
  ],
  'price':[[0,1,2,3],[150,175,176,75.4]], 
  'volume':[[0,1,2,3],[99,220,221,100]],
  'summary':[[0,2],[100,330]]};

  var
    V = envision,
    container = document.getElementById('charts'),
    summaryTicks = financeData.summaryTicks,
    options, finance;

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
    // An initial selection
    selection : {
      data : {
        x : {
          min : 1,
          max : 10
        }
      }
    }
  };

  finance = new envision.templates.Finance(options);

function show_message(message){
        var el = document.createElement('div');
        el.innerHTML = message;
        document.body.appendChild(el);
    }


  var ws = new WebSocket("ws://127.0.0.1:8888/ws/coins");
  ws.onopen = function() {
      show_message('Connected.');
  };
  ws.onmessage = function(event) {
      var price = event.data;
      if(financeData.summaryTicks.length>100){
        financeData.summaryTicks.shift();
        financeData.price[1].shift();

      }
      else
      {
        var c = financeData.price[0].length;
        var lastindex = financeData.price[0][c-1];
        financeData.price[0].push(lastindex);
      }
      financeData.summaryTicks.push(
        {"date":"August 19, 2004","open":price,"high":104.06,"low":95.96,"close":104.34,"volume":23088000}
      );
      financeData.price[1].push(event.data);
      finance.price.draw(null);
      finance.summary.draw(null);
  };
  ws.onclose = function() {
      show_message("Closed.");
  };


}
