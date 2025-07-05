from rest_framework import serializers
from .models import Task, ContextEntry, Category
from .models import Category, Task
from rest_framework import serializers

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'
        
class TaskSerializer(serializers.ModelSerializer):
    # Accept category ID or omit entirely
    category = serializers.PrimaryKeyRelatedField(
        queryset=Category.objects.all(),
        required=False,
        allow_null=True,
    )

    class Meta:
        model = Task
        fields = '__all__'
        extra_kwargs = {
            'description':    {'required': False, 'allow_blank': True},
            'priority_score': {'required': False},
            'deadline':       {'required': False, 'allow_null': True},
        }

    def create(self, validated_data):
        # default description
        if not validated_data.get('description'):
            validated_data['description'] = validated_data.get('title', '')

        # default category = "General"
        if not validated_data.get('category'):
            cat, _ = Category.objects.get_or_create(name="General")
            validated_data['category'] = cat

        # default priority
        if 'priority_score' not in validated_data:
            validated_data['priority_score'] = 5.0

        return super().create(validated_data)

class ContextEntrySerializer(serializers.ModelSerializer):
    class Meta:
        model = ContextEntry
        fields = '__all__'

