from django.contrib import admin
from django.urls import include, path, re_path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path("api/recipes/", include("apps.recipes.urls")),
    path('api-auth/', include('rest_framework.urls')),
    path("admin/", admin.site.urls),
    re_path('login', views.login),
    re_path('signup', views.signup),
    re_path('test_token', views.test_token),
]
