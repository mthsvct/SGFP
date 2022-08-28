from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('home.urls')),
    path('home/', include('home.urls')),
    path('user/', include('users.urls')),
    path('categories/', include('categories.urls')),
    path('despesas/', include('despesas.urls')),
    path('poupanca/', include('poupanca.urls'))
]
