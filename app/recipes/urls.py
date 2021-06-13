from django.urls import path, include
from rest_framework.routers import DefaultRouter

from recipes import views


router = DefaultRouter()
router.register('_tags', views.TagViewSet)

app_name = 'recipes'

urlpatterns = [
    path('', include(router.urls)),
]
