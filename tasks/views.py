
from rest_framework import viewsets
from .models import Task, ContextEntry, Category
from .serializers import TaskSerializer, ContextEntrySerializer, CategorySerializer

class TaskViewSet(viewsets.ModelViewSet):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer

class ContextEntryViewSet(viewsets.ModelViewSet):
    queryset = ContextEntry.objects.all()
    serializer_class = ContextEntrySerializer

class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

from rest_framework.decorators import api_view
from rest_framework.response import Response
from .ai_utils import generate_task_suggestions

@api_view(['POST'])
def ai_suggestions(request):
    title = request.data.get("title", "")
    description = request.data.get("description", "")
    context = request.data.get("context", [])  # ✅ used now

    suggestions = generate_task_suggestions(title, description, context)
    return Response(suggestions)


