from recipe import models
from django.test import TestCase


class MoldelTests(TestCase):
    def test_recipe_str(self):
        """Test the recipe string representation"""
        recipe = models.Recipe.objects.create(name="Cucumber", description="peel")

        self.assertEqual(str(recipe), recipe.name)
