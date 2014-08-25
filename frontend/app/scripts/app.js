'use strict';

/**
 * @ngdoc overview
 * @name redApp
 * @description
 * # redApp
 *
 * Main module of the application.
 */
angular
  .module('redApp', [
    'ngAnimate',
    'ngCookies',
    'ngRoute',
    'ui.router'
  ])
  .config(function ($stateProvider,
                    $urlRouterProvider,
                    $httpProvider) {
        $stateProvider
            .state('home', {
                templateUrl: 'views/main.html',
                url: '/'
            })
            .state('auth', {
                url: '/auth',
                abstract: true,
                templateUrl: 'views/auth/auth.html',
                controller: 'AuthCtrl'
            })
            .state('auth.step1', {
                url : '',
                templateUrl: 'views/auth/step1.html'
            })
            .state('auth.step2', {
                templateUrl: 'views/auth/step2.html'
            })
            .state('profile', {
                url: '/profile',
                templateUrl: 'views/user/profile.html',
                controller: 'UserCtrl'
            });

        $urlRouterProvider.otherwise('/');
        $httpProvider.defaults.useXDomain = true;
        delete $httpProvider.defaults.headers.common['X-Requested-With'];
  })
    .run(function($rootScope,
                  $state,
                  $http,
                  $cookies,
                  $urlRouter,
                  $stateParams,
                  AuthFactory){

        $http.defaults.headers.post['X-CSRFToken'] = $cookies.csrftoken;
        // Add the following two lines
        $http.defaults.xsrfCookieName = 'csrftoken';
        $http.defaults.xsrfHeaderName = 'X-CSRFToken';


        $rootScope.$on('$stateChangeStart', function(event, toState, toParams, fromState, fromParams){
            if (!AuthFactory.authenticated){
                event.preventDefault();
                AuthFactory.isAuthenticated(toState, toParams);
            }
        });

        $rootScope.$state = $state;
        $rootScope.$stateParams = $stateParams;
    })
    .constant('API_SERVER', 'http://miropa.pe/api')
    .constant('END_POINT', {
        postRegisterUser: '/people/register/',
        postLoginUser: '/login/',
        postLogoutUser: '/logout/'
    });
