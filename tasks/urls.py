from .views import TaskViewSet, ContextEntryViewSet, CategoryViewSet, ai_suggestions

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import TaskViewSet, ContextEntryViewSet, CategoryViewSet

router = DefaultRouter()
router.register(r'tasks', TaskViewSet)
router.register(r'context', ContextEntryViewSet)
router.register(r'categories', CategoryViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('ai/suggestions/', ai_suggestions, name='ai-suggestions'),
]
