from django.urls import path, include
from rest_framework.routers import DefaultRouter

from recipes import views


router = DefaultRouter()
router.register('_tag', views.TagViewSet)
router.register('_ingredient', views.IngredientViewSet)

app_name = 'recipes'

urlpatterns = [
    path('', include(router.urls)),
]
