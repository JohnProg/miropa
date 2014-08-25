'use strict';

angular.module('redApp')
  .controller('NavCtrl', function ($scope, $window, AuthFactory) {
    $scope.logOutUser = function(){
        AuthFactory.logout();
    };
    $scope.isAuthenticated = $window.localStorage.isAuthenticated;
  });
