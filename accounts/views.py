from django.views import View
from django.views.generic import TemplateView
from django.contrib.auth import login, authenticate, logout
from django.shortcuts import redirect, render
from accounts.models import CustomUser


# Create your views here.


class LoginView(TemplateView):
    template_name = "account/login.html"

    def post(self, request, *args, **kwargs):
        print("login function called")
        email = request.POST.get("login")
        password = request.POST.get("password")
        user = authenticate(request, email=email, password=password)
        if user:
            login(request, user)
            print("login success")
            return redirect("letters:create")
        else:
            print("login failed")
            return render(
                request, "account/login.html", {"error": "Invalid credentials"}
            )


class SignupView(TemplateView):
    template_name = "account/signup.html"

    # def POST(self,request,*args,**kwargs):
    #     email = request.POST.get("email")
    #     password = request.POST.get("password")
    #     user = CustomUser.objects.create_user(email=email, password=password)
    #     login(request, user)
    #     return redirect("letters:create")


class LogoutView(View):
    def get(self, request, *args, **kwargs):
        logout(request)
        return redirect("account_login")
