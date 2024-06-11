from django.urls import path
from . import views

urlpatterns = [
    path('recipes/', views.RecipeListCreate.as_view(), name='recipes-list-create'),
    path('recipesName/', views.RecipeListName.as_view(), name='recipesName-list'),
    path('recipe/', views.RecipeId.as_view(), name='recipeId'),
    path('recipesSearch/', views.RecipeSearch.as_view(), name='recipeSearch'),
    path('categoriesList/', views.CategoriesList.as_view(), name='categoriesList'),
    path('ingredients/', views.IngredientListCategory.as_view(), name='ingredients-list-category'),
    path('ingredientsMesure/', views.IngredientMesurement.as_view(), name='ingredients-list-mesurement'),
    path('ingredientsList/', views.IngredientList.as_view(), name='ingredients-list'),
    path('ingredientsRecipe/', views.IngredientsRecipeId.as_view(), name='ingredientsIdRecipe-list'),
    path('ingredientsVege/', views.IngredientVege.as_view(), name='ingredientsVege'),
    path('ingredientsQuant/', views.IngredientQuant.as_view(), name='ingredientsQuant'),
    path('ingredientsSearch/', views.IngredientSearch.as_view(), name='ingredientsSearch'),
]
