from django.shortcuts import render
from django.http import HttpResponse
from .models import Recipe


def index(request):
    allRecipeNames = Recipe.objects.all()
    print(type(allRecipeNames))
    allRecipeNamesList = list(allRecipeNames)
    print(allRecipeNamesList)
    print(allRecipeNamesList[0])
    # for e in allRecipeNames:
    #     print(e.description)

    # print(type(allRecipeNames))
    # insideObject = allRecipeNames.description
    return HttpResponse("hola")
