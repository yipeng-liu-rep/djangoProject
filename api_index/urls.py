from django.urls import path

from . import views


urlpatterns = [
    path('add_article', views.add_article),
    path('my_article', views.show_personal_article),
    path('home', views.show_index),
    path('detail', views.article_detail),
    path('addcollection', views.add_collection),
    path('delcollection', views.delete_collection),
    path('is_collected', views.is_collected),
    path('user_collected', views.user_collected_article)
]