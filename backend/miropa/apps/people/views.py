# coding=utf-8
import json
from django.contrib.auth import login
from django.http.response import HttpResponse
from .models import UserProfile, Category
from .forms import UserForm


def register_user(request):
    data = {'id': None}
    if request.method == 'POST':
        json_object = json.loads(request.body)
        form = UserForm(json_object)
        if form.is_valid():
            new_user = form.save()
            new_user.backend = 'django.contrib.auth.backends.ModelBackend'
            UserProfile.objects.create(
                user=new_user
            )
            login(request, new_user)
            data = {
                'id': new_user.id,
                'username': new_user.username,
                'is_active': new_user.is_active,
                'email': new_user.email
            }
        else:
            data = {
                'errors': form.errors,
                'is_active': False
            }
    data = json.dumps(data)
    return HttpResponse(data, content_type='application/json')


def get_categories(request):
    categories = Category.objects.all()
    categories = [category.as_dict for category in categories]
    data = json.dumps(categories)
    return HttpResponse(data, content_type='application/json')