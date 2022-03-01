# from xml.etree.ElementInclude import include
from django.urls import path, include
from rest_framework import routers

from recipe import views

# urlpatterns = [
#     path("", views.index, name="index"),
#     # path("<int:name>/", views.recipecontent, name="recipecontent"),
# ]

router = routers.DefaultRouter()
router.register("", views.RecipeViewSet)

# app_name = "recipe"

urlpatterns = [
    path("", include(router.urls)),
]
