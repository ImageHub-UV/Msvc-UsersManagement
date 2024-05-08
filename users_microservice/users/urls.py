from django.urls import path, include, re_path
from rest_framework.documentation import include_docs_urls
from rest_framework import routers  
from .views import *

router = routers.DefaultRouter()
router.register(r'users', UserViewSet)

urlpatterns = [
    path('get/<id>', UserViewSet.as_view(),name='user'),
    path('docs/', include_docs_urls(title='Users API')),
]
