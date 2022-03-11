from django.test import TestCase
from rest_framework import status

from rest_framework.test import APIClient

from recipe.models import Recipe, Ingredient
from recipe.serializers import RecipeSerializer
import json


def sample_recipe():
    """Create and return a sample recipe"""
    defaults = {
        "name": "Sample recipe",
        "description": "instructions for the recipe",
    }
    recipe = Recipe.objects.create(**defaults)
    recipe.ingredients.create(name="ingredient1")
    recipe.ingredients.create(name="ingredient2")

    return recipe


class RecipeApiTests(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_retrieve_recipes(self):
        sample_recipe()
        res = self.client.get("/recipes/")

        recipes = Recipe.objects.all().order_by("-id")
        serializer = RecipeSerializer(recipes, many=True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_retrieve_recipe(self):
        recipe = sample_recipe()
        res = self.client.get(f"/recipes/{recipe.id}/")

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data["name"], recipe.name)

    def test_retrieve_filtered_recipes(self):
        sample_recipe()
        res = self.client.get("/recipes/?name=mple")

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data), 1)

    def test_create_recipe(self):
        payload = {
            "name": "soup",
            "description": "boil ingredients",
            "ingredients": [
                {"name": "carrot"},
                {"name": "onion"},
                {"name": "leek"},
            ],
        }
        response = self.client.post(
            "/recipes/",
            data=json.dumps(payload),
            content_type="application/json",
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        recipe = Recipe.objects.get(id=response.data["id"])
        self.assertEqual(response.data["name"], recipe.name)
        self.assertEqual(len(response.data["ingredients"]), recipe.ingredients.count())

    def test_modify_recipe(self):
        recipe = sample_recipe()

        payload = {
            "ingredients": [
                {"name": "carrot"},
                {"name": "onion"},
                {"name": "leek"},
            ],
        }

        response = self.client.patch(
            f"/recipes/{recipe.id}/",
            data=json.dumps(payload),
            content_type="application/json",
        )

        updated_recipe = Recipe.objects.get(id=recipe.id)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(updated_recipe.ingredients.count(), 3)

    def test_delete_recipe(self):
        recipe = sample_recipe()
        response = self.client.delete(f"/recipes/{recipe.id}/")

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Recipe.objects.count(), 0)
        self.assertEqual(Ingredient.objects.count(), 0)
