from django.conf import settings
from django.http import HttpResponseRedirect
from django.shortcuts import render, HttpResponse ,redirect
from . import forms 
from . import models
from django.contrib.auth import authenticate, login
from django.contrib.auth.hashers import check_password
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes,force_str
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from .tokens import generate_token
from django.core.mail import EmailMessage
from django.contrib.auth import logout
from django.conf import global_settings




def send_activation_email(user, request):
    current_site = get_current_site(request)
    email_subject = 'Activate your account'
    email_body = render_to_string('app_auth/account_activation_mail.html', {
        'user': user,
        'domain': current_site,
        'uid': urlsafe_base64_encode(force_bytes(user.pk)),
        'token': generate_token.make_token(user)
    })

    email = EmailMessage(subject=email_subject, body=email_body,
                         from_email=settings.DEFAULT_FROM_EMAIL,
                         to=[user.email]
                         )
    email.send()


def index_view(request):
    context = {}
    return render(request, template_name="app_auth/index.html", context=context)

def register_view(request):

    if request.method == "POST":
        form = forms.CustomForm(request.POST)
        if form.is_valid():
            model_instance=models.CustomUser(
                username=form.cleaned_data["username"],
                email=form.cleaned_data["email"],
                password=form.cleaned_data["password1"]
            )
            model_instance.set_password(model_instance.password)
            #model_instance.set_password(form.cleaned_data["password1"])
            model_instance.save()
            # user = authenticate(request,
            # username=form.cleaned_data["username"], 
            # password=form.cleaned_data["password1"],)
            ################################ bundan sonrası activation mail

            send_activation_email(model_instance, request)

            return HttpResponse('Please confirm your email address to complete the registration')

            

            # if user is not None:
            #     login(request, user)
            #     # Redirect to a success page.
            #     return redirect("app_auth:index_view_name"),

            # if not user.is_email_verified:
            #     #messages error verify ur mail
            #     #TODO yeni mail yollaması içinde bir link

            #return redirect("app_auth:index_view_name")

            
        else:
            form = forms.CustomForm(request.POST)
            context = {"form": form}
            return render( request, template_name="app_auth/register.html", context=context)
    if request.method == "GET":
        form = forms.CustomForm()
        context = {"form": form}
        return render(request, template_name="app_auth/register.html", context=context)

# def activate_view(request, uidb64, token):
#     try:
#         uid = force_str(urlsafe_base64_decode(uidb64))
#         user = models.CustomUser.objects.get(pk=uid)
#     except(TypeError, ValueError, OverflowError, models.CustomUser.DoesNotExist):
#         user = None
#     if user is not None and account_activation_token.check_token(user, token):
#         user.is_active = True
#         user.save()
#         login(request, user)
#         # return redirect('home')
#         return HttpResponse('Thank you for your email confirmation. Now you can login your account.')
#     else:
#         return HttpResponse('Activation link is invalid!')

def activate_view(request, uidb64, token):

    try:
        uid = force_str(urlsafe_base64_decode(uidb64))

        user = models.CustomUser.objects.get(pk=uid)

    except Exception as e:
        user = None

    if user and generate_token.check_token(user, token):
        user.is_email_verified = True
        user.is_active = True
        user.save()

        # messages.add_message(request, messages.SUCCESS,
        #                      'Email verified, you can now login')
        return redirect("app_auth:login_view_name")

    return render(request, 'app_auth/activate_failed.html', {"user": user})



def logout_view(request):
    logout(request)
    # Redirect to a success page.
    return redirect("app_auth:index_view_name")

def login_view(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            # Redirect to a success page.
            return redirect("app_auth:index_view_name")
        else:
            # Return an 'invalid login' error message.
            return render(request,template_name="app_auth/login.html")
    if request.method == "GET":
        return render(request,template_name="app_auth/login.html")

def change_password_view(request):

    if request.method == "POST":
        hashed_pass=request.user.password
        if request.POST.get("password1")==request.POST.get("password2") and check_password(request.POST.get("password_old"),hashed_pass):
            u = models.CustomUser.objects.get(username=request.user.username)
            u.set_password(request.POST.get("password1"))
            u.save()
            logout(request)
            return redirect("app_auth:index_view_name")
        else:
            return render(request, template_name="app_auth/change_password.html")
            

    if request.method == "GET":
        print(request.user.email)
        return render(request, template_name="app_auth/change_password.html")
