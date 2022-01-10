from django.urls import path, include
from learning_user_app import views

app_name='learning_user_app'

urlpatterns = [
    path('register/', views.register, name='register'),
    path('user_login/', views.user_login, name="user_login")


]