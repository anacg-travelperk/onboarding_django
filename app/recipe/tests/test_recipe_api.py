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


def sample_recipe2():
    """Create and return a sample recipe"""
    defaults = {
        "name": "Lasagna",
        "description": "cook at 180",
    }
    recipe = Recipe.objects.create(**defaults)
    recipe.ingredients.create(name="frozen lasagna")
    recipe.ingredients.create(name="another frozen lasagna")

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

    def test_retrieve_filtered_recipe(self):
        sample_recipe()
        recipe = sample_recipe2()
        res = self.client.get(f"/recipes/?name=agna")

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data), 1)
        self.assertEqual(res.data[0]["name"], recipe.name)

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
        recipe = Recipe.objects.get(id=response.data["id"])
        ingredients = recipe.ingredients.all()
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(payload["name"], recipe.name)
        self.assertEqual(payload["description"], recipe.description)
        self.assertEqual(len(payload["ingredients"]), ingredients.count())
        for ingredient in ingredients:
            self.assertTrue({"name": ingredient.name} in payload["ingredients"])

    def test_modify_recipe_name_and_description(self):
        recipe = sample_recipe()
        payload = {
            "name": "modified name",
            "description": "modified description",
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
        self.assertEqual(updated_recipe.name, payload["name"])
        self.assertEqual(updated_recipe.description, payload["description"])

    def test_modify_recipe_ingredients(self):
        recipe = sample_recipe()
        payload = {
            "name": "Sample recipe",
            "description": "instructions for the recipe",
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
        updated_ingredients = updated_recipe.ingredients.all()

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(updated_recipe.ingredients.count(), 3)
        for ingredient in updated_ingredients:
            self.assertTrue({"name": ingredient.name} in payload["ingredients"])

    def test_delete_recipe(self):
        recipe = sample_recipe()
        response = self.client.delete(f"/recipes/{recipe.id}/")

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Recipe.objects.count(), 0)
        self.assertEqual(Ingredient.objects.count(), 0)

    def test_invalid_recipe_name(self):
        payload = {
            "name": "",
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
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_invalid_recipe_description(self):
        payload = {
            "name": "name",
            "description": "",
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
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_retrieve_non_existing_recipe(self):
        recipe = sample_recipe()
        recipeId = recipe.id
        res_delete = self.client.delete(f"/recipes/{recipeId}/")
        self.assertEqual(res_delete.status_code, status.HTTP_204_NO_CONTENT)
        res = self.client.get(f"/recipes/{recipeId}/")
        self.assertEqual(res.status_code, status.HTTP_404_NOT_FOUND)
