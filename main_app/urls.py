from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('status/', include('status.urls')),
    path('projects/', include('projects.urls')),
    path('tenants/', include('tenants.urls')),
    path('users/', include('users.urls')),
    path('tickets/', include('tickets.urls'))
]
