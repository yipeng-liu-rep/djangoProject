from wx_login import views
from django.urls import path, include


urlpatterns = [
    path('login/', views.Login.as_view()),
]