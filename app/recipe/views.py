# from django.shortcuts import render
# from django.http import HttpResponse, JsonResponse
from .models import Recipe
from .serializers import RecipeSerializer

from rest_framework import viewsets

# from rest_framework.response import Response

# from rest_framework.decorators import api_view, renderer_classes
# from rest_framework.renderers import JSONRenderer, TemplateHTMLRenderer

# @api_view(("GET",))
# @renderer_classes((TemplateHTMLRenderer, JSONRenderer))
# def index(request):
#     allRecipeNames = Recipe.objects.all()
#     serializer = RecipeSerializer(allRecipeNames)
#     # print(type(allRecipeNames))
#     # allRecipeNamesList = list(allRecipeNames)
#     # print(allRecipeNamesList)
#     # print(allRecipeNamesList[0])
#     # for e in allRecipeNames:
#     #     print(e.description)

#     # print(type(allRecipeNames))
#     # insideObject = allRecipeNames.description
#     return Response(allRecipeNames, template_name=None)


class RecipeViewSet(viewsets.ModelViewSet):
    """Manage recipes in the database"""

    # authentication_classes = (TokenAuthentication,)
    # permission_classes = (IsAuthenticated,)
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer
    # def get_queryset(self):
    #     """Return objects for the current authenticated user only"""
    #     return self.queryset.order_by("-name")
