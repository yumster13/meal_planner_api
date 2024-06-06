from django.db import models

# Create your models here.

from django.db import models

from django.core.validators import MaxValueValidator, MinValueValidator 

class Ages(models.TextChoices):
    DEFAULT = '18+',
    PF = 'Petit F', 
    PG = 'Petit G', 
    GF = 'Grand F', 
    GG = 'Grand G',

class Mesurements(models.TextChoices):
    KG = 'KG',
    L = 'L', 
    PIECE = 'PIECE', 
    TRANCHE = 'TRANCHE', 
    CONDIMENT = 'CONDIMENT', 

class Season(models.Model):
    name = models.CharField("Name", null=False,unique=True,max_length=10)
    def __str__(self):
        return self.name

class Category(models.Model):
    name = models.CharField("Nom", null=False,blank=False, max_length=30)
    parent_category = models.ForeignKey("self", on_delete=models.RESTRICT,null=True)
    def __str__(self):
        return self.name

class Ingredient(models.Model):
    name = models.CharField("Nom", null=False,blank=False, max_length=30)
    category = models.ForeignKey(Category, on_delete=models.RESTRICT,null=True)
    season = models.ManyToManyField(Season)
    mesurement = models.CharField("Mesure", choices=Mesurements.choices, default=Mesurements.KG,max_length=10)
    avg_price = models.DecimalField("Prix moyen",max_digits=5, decimal_places=2,null=True)

    def __str__(self):
        return self.name

class RecipeXEngredient(models.Model):
    ingredient = models.ForeignKey(Ingredient, on_delete=models.RESTRICT, null=False)
    quantity = models.DecimalField("Quantité",max_digits=15, decimal_places=5)
    age = models.CharField("Tranche d'âge", choices=Ages.choices, default=Ages.DEFAULT,max_length=10)
    vege = models.BooleanField("Vege ?", null=False,blank=False,default=False)
    def __str__(self):
        return str(self.ingredient)+' '+str(self.age)

class Tag(models.Model):
    name = models.CharField("Nom", null=False,blank=False, max_length=30)
    parent_tag = models.ForeignKey("self", on_delete=models.RESTRICT,null=True,blank=True)

    def __str__(self):
        return str(self.name)

class Recipe(models.Model):
    name = models.TextField("Nom", null=False,blank=False)
    prairie = models.BooleanField("En prairie ?", null=False,blank=False,default=False)
    tags = models.ForeignKey(Tag, on_delete=models.RESTRICT,null=True,blank=True)
    ingredients = models.ManyToManyField(RecipeXEngredient)

    def calculate_total_price(self, age_group):
        total = 0
        for recipe_x_ingredient in self.ingredients.filter(age=age_group):
            ingredient = recipe_x_ingredient.ingredient
            quantity = recipe_x_ingredient.quantity
            total += ingredient.avg_price * quantity
        return total
    
    def __str__(self) -> str:
        return self.name