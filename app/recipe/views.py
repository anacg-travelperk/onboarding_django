from .models import Recipe
from .serializers import RecipeSerializer
from rest_framework import viewsets
from django_filters.rest_framework import DjangoFilterBackend


class RecipeViewSet(viewsets.ModelViewSet):
    """Manage recipes in the database"""

    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer

    def get_queryset(self):
        name = self.request.query_params.get("name")
        if name:
            return self.queryset.filter(name__icontains=name)

        return self.queryset
