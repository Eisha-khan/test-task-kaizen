from .views import *
from django.urls import path, include
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register('items', ItemViewSet, basename='Items')
router.register('categories', CategoryViewSet, basename='Categories')
urlpatterns = router.urls