from django.urls import path, include
from rest_framework.routers import DefaultRouter

from recipes import views


router = DefaultRouter()
router.register(r'tag', views.TagViewSet)
router.register(r'ingredient', views.IngredientViewSet)
router.register(r'recipes', views.RecipeViewSet)

app_name = 'recipe'

urlpatterns = [
    path('', include(router.urls)),
]
