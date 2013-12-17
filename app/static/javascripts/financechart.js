Date.prototype.Format = function(fmt)   
{ //author: meizz   
  var o = {   
    "M+" : this.getMonth()+1,                 //月份   
    "d+" : this.getDate(),                    //日   
    "h+" : this.getHours(),                   //小时   
    "m+" : this.getMinutes(),                 //分   
    "s+" : this.getSeconds(),                 //秒   
    "q+" : Math.floor((this.getMonth()+3)/3), //季度   
    "S"  : this.getMilliseconds()             //毫秒   
  };   
  if(/(y+)/.test(fmt))   
    fmt=fmt.replace(RegExp.$1, (this.getFullYear()+"").substr(4 - RegExp.$1.length));   
  for(var k in o)   
    if(new RegExp("("+ k +")").test(fmt))   
  fmt = fmt.replace(RegExp.$1, (RegExp.$1.length==1) ? (o[k]) : (("00"+ o[k]).substr((""+ o[k]).length)));   
  return fmt;   
}
var coin__minprice = null;
var coin__maxprice = null;
var coin__lastprice = null;
var coin__showchart = true;
var finance;
function savealarm(){
  var min = $("#min_price").val();
  var max = $("#max_price").val();
  if(min){
    coin__minprice = parseFloat(min);
  }
  if(max){
    coin__maxprice = parseFloat(max);
  }
  checkalarm();
  $("#status").html("Save OK. " + new Date().Format('yyyy-MM-dd hh:mm:ss'));
}

function clearalarm(){
  $("#min_price").val("");
  $("#max_price").val("");
  coin__minprice = null;
  coin__maxprice = null;
  checkalarm();
}

function initalarm(){
  alarming = false;
}
function playalarm(type){
  console.log(type);
  alarmSound.play({
  loops: 100
});
  alarming = true;
}
function stopalarm(){
  alarming = false;
  alarmSound.stop();
}
function checkalarm(){
  if(coin__minprice != null && (coin__lastprice <= coin__minprice)){
        //play down alarm
        if(!alarming){
          playalarm("lower");
        }
        
    }else
    if(coin__maxprice != null && (coin__lastprice >= coin__maxprice)){
      //play up alarm
      if(!alarming){
          playalarm("upper");
        }
    }else{
      console.log("stop");
      stopalarm();
    }
}

function hidechart(){
  if(coin__showchart){
    $("#charts").hide();
    coin__showchart=false;
  }else{
    $("#charts").show();
    coin__showchart=true;
    financedraw();
  }
}

function financedraw(){
  finance.price.draw(null);
      finance.summary.draw(null);
}


function financechart () {
  var MaxPoints = 400;
  var now = new Date().Format('yyyy-MM-dd hh:mm:ss');
  var financeData = {
  'summaryTicks': [
  {"date":now,"open":100.01,"high":104.06,"low":95.96,"close":100.34,"volume":22088000}
  ],
  'price':[[0],[118]], 
  'volume':[[0],[110]],
  'summary':[[0],[100]]};

var
    V = envision,
    container = document.getElementById('charts'),
    summaryTicks = financeData.summaryTicks,
    options;

var popfirst = true;

  options = {
    container : container,
    data : {
      price : financeData.price,
      // volume : financeData.volume,
      summary : financeData.price
    },
    trackFormatter : function (o) {

      var
        data = o.series.data,
        index = data[o.index][0],
        value;

      value = summaryTicks[index].close +" / \n" + summaryTicks[index].date ;//+ ", Vol: " + summaryTicks[index].volume;

      return value;
    },
    xTickFormatter : function (index) {
      if(index < 0) return "";
      if(index >= summaryTicks.length) return "";
      var date = new Date(financeData.summaryTicks[index].date);
      return date.Format("MM-dd hh:mm") + '';
    },
    yTickFormatter : function (n) {
      return n;
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

  finance = new envision.templates.BitCoinFinance(options);

  function show_message(message){
        $("#status").html(message);
    }


  var ws = new WebSocket("ws://127.0.0.1:9888/ws/coins");
  ws.onopen = function() {
      show_message('Connected.');
  };
  ws.onmessage = function(event) {
      coin__lastprice = parseFloat(event.data);
      console.log([coin__minprice, coin__maxprice, coin__lastprice,coin__minprice != null, coin__lastprice > coin__minprice]);
      checkalarm();
      // if(coin__minprice != null && (coin__lastprice <= coin__minprice)){
      //   //play down alarm
      //   playalarm();
      // }else
      // if(coin__maxprice != null && (coin__lastprice >= coin__maxprice)){
      //   //play up alarm
      //   playalarm();
      // }else{
      //   if(alarming){
      //     stopalarm();
      //   }
      // }
      var len = financeData.price[0].length;
      var lastindex = financeData.price[0][len-1];
      $("#title").html(coin__lastprice + "  |  300Coin");
      $("#coin_price").html(coin__lastprice);
      if(popfirst){
        financeData.summaryTicks.shift();
        financeData.price[1].shift();
        popfirst = false;
      }
      else
      {
        if(financeData.summaryTicks.length>=MaxPoints){
          financeData.summaryTicks.shift();
          financeData.price[1].shift();
        }
        else
        {
          
          lastindex += 1;
          financeData.price[0].push(lastindex);
        }
      }
      var newnow = new Date().Format('yyyy-MM-dd hh:mm:ss');
      financeData.summaryTicks.push(
        {"date":newnow,"open":coin__lastprice,"high":coin__lastprice,"low":coin__lastprice,"close":coin__lastprice,"volume":coin__lastprice}
      );
      financeData.price[1].push(event.data);
      financedraw();

      var offset = 0;
      var min = 0;
      // Trigger the select interaction.
      // Update the select region and draw the detail graph.
      if(lastindex >= MaxPoints){
        finance.summary.trigger('select', {
          data : {
            x : {
              min : MaxPoints/2 ,
              max : MaxPoints 
            }
          }
        });
      }

     
      
  };
  ws.onclose = function() {
      show_message("Closed.");
  };


}
