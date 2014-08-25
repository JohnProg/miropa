'use strict';

angular.module('redApp')
  .factory('AuthFactory', function ($state, $window, $http, $location, API_SERVER, END_POINT, Auth) {
    // Service logic
    // ...

    var privateRoutesWhenIsLogged = /course|profile|institution/;
    var privateRoutesWhenIsNoLogged = /auth|home/;

        // Public API here
        return {
            isAuthenticated: function(nextState, nextParams){
                //$window.localStorage.isAuthenticated = false;
                var self = this;
                $http.get(API_SERVER + END_POINT.postLoginUser)
                    .then(function(response){
                        var user = response.data;
                        //var response = {};
                        //response.data = {message: 'njnj'};
                        if (user.is_active !== true && self.isUrlInsideAllowed(nextState.name, privateRoutesWhenIsLogged)){
                            self.deleteIsAuthenticatedStorage();
                            changeAuthentication('auth.step1', {});
                        }
                        else if(user.is_active === true && self.isUrlInsideAllowed(nextState.name, privateRoutesWhenIsNoLogged)){
                            $window.localStorage.isAuthenticated = true;
                            changeAuthentication('profile', {});
                        }
                        else{
                            changeAuthentication(nextState.name, nextParams);
                        }
                        function changeAuthentication(state){
                            self.authenticated = true;
                            self.goTo(state, nextParams);
                            self.authenticated = false;
                        }
                    });
            },
            authenticated: false,
            isUrlInsideAllowed: function(next, urls){
                return urls.test(next);
            },
            deleteIsAuthenticatedStorage: function () {
                $window.localStorage.isAuthenticated = false;
                $window.localStorage.isMasterUser = false;
            },
            logout : function(){
                var self = this;
                Auth.logOutUserService()
                    .then(function(){
                        self.deleteIsAuthenticatedStorage();
                        self.goTo('auth.step1');
                    });
            },
            login : function(){
                $window.localStorage.isAuthenticated = true;
                this.goTo("profile");
            },
            goTo: function (path, params) {
                $state.go(path, params);
            }
        };
  });
