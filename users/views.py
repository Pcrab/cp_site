# Create your views here.
import json

from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseNotFound
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST, require_GET

from .models import User, UserCreateException


@require_POST
@csrf_exempt
def login(request):
    user_post = get_user_post(request)
    if user_post is None:
        return HttpResponseBadRequest("username or password wrong")
    elif not User.is_exist(username=user_post["username"], password=user_post["password"]):
        return HttpResponseNotFound("user not found")
    request.session["username"] = user_post["username"]
    return HttpResponse(f"welcome, {user_post['username']}")


@require_POST
@csrf_exempt
def create(request):
    user_post = get_user_post(request)
    if not user_post:
        return HttpResponseBadRequest("username or password wrong")
    try:
        User.create_user(user_post)
        return HttpResponse(user_post)
    except UserCreateException as e:
        return HttpResponseBadRequest(e.errorInfo)


@require_GET
def logout(request):
    if request.session["username"]:
        request.session.flush()
        return HttpResponse("Successfully logout")
    return HttpResponseBadRequest("Already logout")


def get_user_post(request):
    user_post = json.loads(request.body)
    username = user_post["username"]
    password = user_post["password"]
    if username and password and User.is_valid_without_salt(username=username, password=password):
        return user_post
    return None
