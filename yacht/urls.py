from django.urls import path
from . import views

urlpatterns = [
    path('', views.index),
    path('register',views.register),
    path('home',views.home),
    path('login',views.login),
    path('logout',views.logout),
    path('post/add',views.edit),
    path('<int:post_id>/remove', views.delete),
    path('<int:post_id>/like',views.like),
    path('home/<int:post_id>',views.status),
    path('users/<int:this_user_id>', views.profile),

]