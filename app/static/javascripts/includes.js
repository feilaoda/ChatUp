window.FlashCanvasOptions = {
  swfPath: '/static/javascripts/FlashCanvas/bin/'
};
yepnope([
  // Libs
  '/static/javascripts/jquery/jquery-1.7.1.min.js',
  '/static/javascripts/flotr2/lib/bean.js',
  '/static/javascripts/flotr2/lib/underscore-min.js',
  {
  test : (navigator.appVersion.indexOf("MSIE") != -1  && parseFloat(navigator.appVersion.split("MSIE")[1]) < 9),
    // Load for IE < 9
    yep : [
      '/static/javascripts/FlashCanvas/bin/flashcanvas.js',
      /*'/static/javascripts/flotr2/lib/excanvas.js',*/
      '/static/javascripts/flotr2/lib/base64.js'
    ]
  },
  '/static/javascripts/flotr2/lib/canvas2image.js',
  /*'/static/javascripts/flotr2/lib/canvastext.js',*/
  '/static/javascripts/bonzo/bonzo.min.js',

  // Flotr
  '/static/javascripts/flotr2/js/Flotr.js',
  '/static/javascripts/flotr2/js/DefaultOptions.js',
  '/static/javascripts/flotr2/js/Color.js',
  '/static/javascripts/flotr2/js/Date.js',
  '/static/javascripts/flotr2/js/DOM.js',
  '/static/javascripts/flotr2/js/EventAdapter.js',
  '/static/javascripts/flotr2/js/Graph.js',
  '/static/javascripts/flotr2/js/Axis.js',
  '/static/javascripts/flotr2/js/Series.js',
  '/static/javascripts/flotr2/js/Text.js',
  '/static/javascripts/flotr2/js/types/lines.js',
  '/static/javascripts/flotr2/js/types/bars.js',
  '/static/javascripts/flotr2/js/types/points.js',
  '/static/javascripts/flotr2/js/plugins/selection.js',
  '/static/javascripts/flotr2/js/plugins/legend.js',
  '/static/javascripts/flotr2/js/plugins/hit.js',
  '/static/javascripts/flotr2/js/plugins/crosshair.js',
  '/static/javascripts/flotr2/js/plugins/labels.js',
  '/static/javascripts/flotr2/js/plugins/legend.js',
  '/static/javascripts/flotr2/js/plugins/titles.js',
  {
    test : ('ontouchstart' in window),
    nope : [
      '/static/javascripts/flotr2/js/plugins/handles.js'
    ]
  },

  // Visualization
  '/static/javascripts/envision/Envision.js',
  '/static/javascripts/envision/Visualization.js',
  '/static/javascripts/envision/Component.js',
  '/static/javascripts/envision/Interaction.js',
  '/static/javascripts/envision/Preprocessor.js',
  '/static/javascripts/envision/templates/namespace.js',
  '/static/javascripts/envision/templates/Finance.js',
  '/static/javascripts/envision/templates/TimeSeries.js',
  '/static/javascripts/envision/templates/Zoom.js',
  '/static/javascripts/envision/actions/namespace.js',
  '/static/javascripts/envision/actions/hit.js',
  '/static/javascripts/envision/actions/selection.js',
  '/static/javascripts/envision/actions/zoom.js',
  '/static/javascripts/envision/adapters/namespace.js',
  '/static/javascripts/envision/adapters/flotr/namespace.js',
  '/static/javascripts/envision/adapters/flotr/defaultOptions.js',
  '/static/javascripts/envision/adapters/flotr/Child.js',
  '/static/javascripts/envision/adapters/flotr/lite-lines.js',
  '/static/javascripts/envision/adapters/flotr/whiskers.js',
  '/static/javascripts/envision/components/namespace.js',
  '/static/javascripts/envision/components/QuadraticDrawing.js',

  { complete : financechart }
]);
