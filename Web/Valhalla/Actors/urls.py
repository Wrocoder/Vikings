from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('vikings/', views.history_vikings_list, name='history_vikings_list'),
    path('norsemen/', views.norsemen_list, name='norsemen_list'),
    path('actor_vikings/<int:actor_id>/', views.actor_vikings, name='actor_vikings'),
    path('actor_norsemen/<int:actor_id>/', views.actor_norsemen, name='actor_norsemen'),
]