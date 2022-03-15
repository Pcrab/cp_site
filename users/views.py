# Create your views here.
import json

from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseNotFound
from django.utils.html import escape
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST, require_GET

from .models import User


@require_POST
@csrf_exempt
def login(request):
    user_post = get_user_post(request)
    if user_post is None:
        return HttpResponseBadRequest("username or password wrong format")
    elif not User.is_exist(username=user_post["username"], unencrypted_password=user_post["password"]):
        return HttpResponseNotFound("user not found")
    request.session["username"] = user_post["username"]
    return HttpResponse(f"welcome, {escape(user_post['username'])}")


@require_POST
@csrf_exempt
def create(request):
    user_post = get_user_post(request)
    if not user_post:
        return HttpResponseBadRequest("username or password wrong")
    if User.create_user(username=user_post["username"], unencrypted_password=user_post["password"]):
        return HttpResponse(escape(user_post))
    return HttpResponseBadRequest("create failed")


@require_GET
def logout(request):
    if request.session["username"]:
        request.session.flush()
        return HttpResponse("Successfully logout")
    return HttpResponseBadRequest("Already logout")


@require_POST
@csrf_exempt
def destroy(request):
    user_post = get_user_post(request)
    if request.session["username"] != user_post["username"]:
        return HttpResponseBadRequest("Wrong User")
    if User.destroy(user_post["username"], user_post["password"]):
        request.session.flush()
        return HttpResponse("Destroy user succeeded")
    return HttpResponseBadRequest("Destroy failed")


def get_user_post(request):
    user_post = json.loads(request.body)
    username = user_post["username"]
    password = user_post["password"]
    if username and password and User.is_valid(username=username, unencrypted_password=password):
        return user_post
    return None
