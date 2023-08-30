from django.urls import path

from . import views

urlpatterns = [
    path("index", views.index, name="index"),
    path('', views.recipe_list, name='recipe_list'),
    path('<int:pk>/', views.recipe_detail, name='recipe_detail'),
    path('new/', views.recipe_create, name='recipe_create'),
    path('<int:pk>/', views.recipe_update, name='recipe_update'),
    path('<int:pk>/', views.recipe_delete, name='recipe_delete'),
]
