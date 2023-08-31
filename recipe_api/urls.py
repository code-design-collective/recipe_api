from django.contrib import admin
from django.urls import include, path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path("api/recipes/", include("apps.recipes.urls")),
    path('api-auth/', include('rest_framework.urls')),
    path("admin/", admin.site.urls),
]