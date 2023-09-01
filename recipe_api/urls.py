from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("admin/", admin.site.urls),
    path('api-auth/', include('rest_framework.urls')),
    path("api/recipes/", include("apps.recipes.urls")),
    path('users/', include('apps.users.urls')),  #
]
