'use strict';

angular.module('redApp')
  .service('Auth', function Auth(API_SERVER, END_POINT, $http) {
    // AngularJS will instantiate a singleton by calling "new" on this function
        return {
            registerUserService: function(data){
                var url = API_SERVER + END_POINT.postRegisterUser;
                return $http.post(url, data);
            },
            loginUserService: function(data){
                var url = API_SERVER + END_POINT.postLoginUser;
                return $http.post(url, data);
            },
            logOutUserService: function(){
                var url = API_SERVER + END_POINT.postLogoutUser;
                return $http.get(url);
            }
        }
  });
