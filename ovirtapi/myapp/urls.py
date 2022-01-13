from django.urls import path, include

from . import views
from .views import *

urlpatterns = [

    # path('', views.index, name='index'),
    path('users<str:pk>/', views.get_userid, name='get_userid'),
    path('users<str:pk>/create/', views.get_createvm, name='get_createvm'),
    path('delete/users<str:pk>/<str:vm>', views.delete_vm, name='delete_vm'),
    path('console/', views.get_console, name='get_console'),
    path('', views.index, name='index'),
    path("see_request/", views.see_request),
    path("user_info/", views.user_info,  name='user_info'),
    path("accounts/", include("django.contrib.auth.urls")),
    path("profile/", views.profile,  name='profile'),

]
