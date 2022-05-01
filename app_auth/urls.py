from django.urls import path
from app_auth import views

app_name="app_auth"

urlpatterns = [
    path("",views.index_view,name="index_view_name"),
    path("register/",views.register_view,name="register_view_name"),
    path("login/",views.login_view,name="login_view_name"),
    path("logout/",views.logout_view,name="logout_view_name"),
    path("change-password/",views.change_password_view,name="change_password_view_name"),

    # path('activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/',  
    #     views.activate_view, name='activate_view_name'),

    path('activate-user/<uidb64>/<token>',views.activate_view, name='activate_view_name'),  
]
