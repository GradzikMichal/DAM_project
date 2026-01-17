import django.middleware.csrf
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group
from django.db.models import F, Q
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect, JsonResponse, HttpResponsePermanentRedirect


@login_required(login_url='/login', redirect_field_name=None)
def home(request):
    user_groups = Group.objects.filter(Q(user=request.user.id)).all().values()
    print(user_groups)
    return JsonResponse(list(user_groups), safe=False)


def user_login(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            response = HttpResponsePermanentRedirect('/user-home')
            if request.session.session_key is not None:
                response.set_cookie("logged_in", "True")
            return response
        else:
            return HttpResponse("Wrong username or password.", status=403)
    elif request.method == "GET":
        csrf = django.middleware.csrf.get_token(request)
        return JsonResponse({"csrf": csrf})
