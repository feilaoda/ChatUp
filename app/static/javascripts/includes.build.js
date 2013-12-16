window.FlashCanvasOptions = {
  swfPath: 'lib/FlashCanvas/bin/'
};
yepnope([

  /*'/static/javascripts/jquery/jquery-1.7.1.min.js',

  // IE
  {
    test : (navigator.appVersion.indexOf("MSIE") != -1  && parseFloat(navigator.appVersion.split("MSIE")[1]) < 9),
    yep : [
      '/static/javascripts/flotr2/lib/base64.js'
    ]
  },
  {
    test : (navigator.appVersion.indexOf("MSIE") != -1),
    yep : [
      'lib/FlashCanvas/bin/flashcanvas.js'
    ]
  },

  // Libs
  '/static/javascripts/flotr2/flotr2.min.js',
  {
    test : ('ontouchstart' in window),
    nope : [
      '/static/javascripts/flotr2/js/plugins/handles.js'
    ]
  },
  '/static/javascripts/bonzo/bonzo.min.js',
  '/static/javascripts/envision.min.js',
*/
  { complete : example }
]);
