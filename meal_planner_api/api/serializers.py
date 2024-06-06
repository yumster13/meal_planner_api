from rest_framework import serializers
from .models import *

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['name']
class SeasonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Season
        fields = ['name']
class IngredientMesurementSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ingredient
        fields = ['mesurement']
class IngredientSerializerCategory(serializers.ModelSerializer):
    category = CategorySerializer(many=False)  # Include TagSerializer for nested serialization
    season = SeasonSerializer(many=True)  # Include TagSerializer for nested serialization
    class Meta:
        model = Ingredient
        fields = ['name','mesurement','avg_price','category','season']

class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ['name']

class RecipeSerializer(serializers.ModelSerializer):
    tags = TagSerializer(many=False)  # Include TagSerializer for nested serialization

    class Meta:
        model = Recipe
        fields = ['name', 'prairie', 'tags']

class RecipeNameSerializer(serializers.ModelSerializer):
    class Meta:
        model = Recipe
        fields = ['id', 'name']

class IngredientSerializer(serializers.ModelSerializer):
    class Meta:
        model = RecipeXEngredient
        fields = '__all__'