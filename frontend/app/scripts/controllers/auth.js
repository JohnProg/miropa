'use strict';

angular.module('redApp')
  .controller('AuthCtrl', function ($scope, $window, Auth, AuthFactory) {
        $scope.loginUser = function(username, pass){
            var data = {
                username: username,
                password: pass
            };
            Auth.loginUserService(data)
                .then(function(response){
                    var user = response.data;
                    if (user === null){
                        console.log('no existe usuario');
                        AuthFactory.goTo('auth.step1');
                    } else if(user.hasOwnProperty('is_active')) {
                        if(user.is_active) {
                            $window.localStorage.isMasterUser = user.is_active;
                            AuthFactory.login();
                        }
                    }
                })
                .catch(function(response) {
                    console.log(56);
                });
        };
        $scope.registerUser = function(username, email, pass1, pass2) {
            var data = {
                username: username,
                password1: pass1,
                password2: pass2,
                email: email
            };
            Auth.registerUserService(data)
                .then(function(response){
                    var user = response.data;
                    if (user === null){
                        console.log('no existe usuario');
                        AuthFactory.goTo('auth.step1');
                    } else if(user.hasOwnProperty('is_active')) {
                        if(user.is_active) {
                            $window.localStorage.isMasterUser = user.is_active;
                            AuthFactory.login();
                        }
                    }
                })
        };
  });
