from rest_framework import serializers
from .models import Recipe, Ingredient


class IngredientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ingredient
        # fields = "__all__"
        fields = ("name",)


class RecipeSerializer(serializers.ModelSerializer):
    ingredients = IngredientSerializer(read_only=False, many=True, allow_empty=False)

    class Meta:
        model = Recipe
        fields = (
            "id",
            "name",
            "description",
            "ingredients",
        )
        read_only_fields = [
            "id",
        ]

    def create(self, validated_data):
        recipe = Recipe.objects.create(
            name=validated_data["name"], description=validated_data["description"]
        )
        ingredients_data = validated_data["ingredients"]

        if ingredients_data:
            for ingredient in ingredients_data:
                Ingredient.objects.create(recipe=recipe, name=ingredient["name"])
        return recipe

    def update(self, instance, validated_data):
        recipe = instance
        ingredients_data = validated_data["ingredients"]

        recipe.name = validated_data.get("name", recipe.name)
        recipe.description = validated_data.get("description", recipe.description)
        recipe.save()

        recipe.ingredients.all().delete()
        for ingredient in ingredients_data:
            Ingredient.objects.create(recipe=recipe, name=ingredient["name"])

        return recipe
