import json

from django.contrib.auth import login, authenticate, logout
from django.http.response import HttpResponse
from django.views.decorators.csrf import ensure_csrf_cookie


@ensure_csrf_cookie
def login_user(request):
    data = {'id': None}
    if request.method == 'POST':
        json_object = json.loads(request.body)
        username = json_object.get('username')
        password = json_object.get('password')

        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                data = {
                    'id': user.id,
                    'username': user.username,
                    'is_active': user.is_active
                }
        else:
            data = {'is_active': False}
    elif request.method == "GET":
        data = {
            'id': request.user.id,
            'username': request.user.username,
            'is_active': request.user.is_active
        }
    data = json.dumps(data)
    return HttpResponse(data, content_type='application/json')


def logout_user(request):
    data = {'id': None}
    logout(request)
    data = {
        'success': True
    }
    data = json.dumps(data)
    return HttpResponse(data, content_type='application/json')