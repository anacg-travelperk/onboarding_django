from django.test import TestCase
from recipe.models import Ingredient, Recipe
from recipe.serializers import RecipeSerializer


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


def sample_invalid_recipe():
    """Create and return a invalid sample recipe"""

    defaults = {
        "name": 12,
        "description": 32,
    }
    recipe = Recipe.objects.create(**defaults)
    recipe.ingredients.create(name="ingredient1")
    recipe.ingredients.create(name="ingredient2")
    return recipe


class SerializersTests(TestCase):
    def test_serializer_valid_recipe(self):
        recipe = sample_recipe()

        serializer = RecipeSerializer(recipe)

        self.assertEqual(serializer.data["id"], recipe.id)
        self.assertEqual(serializer.data["name"], recipe.name)
        self.assertEqual(
            len(serializer.data["ingredients"]), recipe.ingredients.count()
        )
