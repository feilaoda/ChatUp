var now = new Date();

var version = '?v='+ now.getTime();

var beauty = angular.module('beauty', []).
  config(['$routeProvider', function($routeProvider) {
  
}]);



beauty.directive('planperoid', function(){
    return {
      restrict: 'E',
      replace: false,
      transclude: true,
      scope: {},
      templateUrl:'views/project-template.html' + version ,
      controller: PlanPeroidCtrl,
      link: function(scope, element, attrs) {
      }
    };
});
