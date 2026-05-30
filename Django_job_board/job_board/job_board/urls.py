from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from jobs.views import JobViewSet, RegisterView

router = DefaultRouter()
router.register(r'jobs', JobViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    
    # 1. Put the registration endpoint FIRST
    path('api/register/', RegisterView.as_view(), name='register'),
    
    # 2. Put the router SECOND
    path('api/', include(router.urls)),
]