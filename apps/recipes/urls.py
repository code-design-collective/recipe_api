from django.urls import path

from . import views

urlpatterns = [
    path("index", views.index, name="index"),
    path('', views.recipe_list, name='recipe_list'),
    path('recipe/<int:pk>/', views.recipe_detail, name='recipe_detail'),
    path('recipe/', views.recipe_create, name='recipe_create'),
    path('recipe/<int:pk>/', views.recipe_update, name='recipe_update'),
    path('recipe/<int:pk>/', views.recipe_delete, name='recipe_delete'),
]
