
from django.contrib import admin
from django.urls import path, include
from users.urls import user_router

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(user_router.urls)),
]
