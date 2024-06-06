from rest_framework import generics
from .models import *
from .serializers import *
from rest_framework.permissions import IsAuthenticated
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.response import Response

from rest_framework import generics

class RecipeListCreate(generics.ListCreateAPIView):
    queryset = Recipe.objects.prefetch_related('tags').all()  # Use prefetch_related for efficiency
    serializer_class = RecipeSerializer

class RecipeListName(generics.ListCreateAPIView):
    queryset = Recipe.objects.all()  # Use prefetch_related for efficiency
    serializer_class = RecipeNameSerializer

class CategoriesList(generics.ListCreateAPIView):
    queryset = Category.objects.all()  # Use prefetch_related for efficiency
    serializer_class = CategorySerializer

class IngredientListCategory(generics.ListCreateAPIView):
    queryset = Ingredient.objects.all()  # Use prefetch_related for efficiency
    serializer_class = IngredientSerializerCategory

class RecipeId(generics.ListCreateAPIView):
    serializer_class = RecipeNameSerializer

    def get(self,request,*args,**kwargs):
        data = request.data['recipe_id']
        print(data)
        recipe = Recipe.objects.filter(pk=data)
        print(recipe[0])
        return JsonResponse({'menu': recipe[0].id,'recipe_name':recipe[0].name})

class IngredientMesurement(generics.ListCreateAPIView):
    serializer_class = IngredientMesurementSerializer

    def get(self,request,*args,**kwargs):
        data = request.data['ingredient_name']
        print(data)
        ingredient = Ingredient.objects.filter(name=data)
        print(ingredient[0])
        return JsonResponse({'mesurement': ingredient[0].mesurement})

class IngredientsRecipeId(generics.ListAPIView):
    serializer_class = IngredientSerializer
    def get(self,request,*args,**kwargs):
        data = request.data['recipe_id']
        return Recipe.objects.prefetch_related('ingredients').all().filter(pk=data)


class IngredientList(generics.ListAPIView):
    serializer_class = IngredientSerializer
    def get(self,request,*args,**kwargs):
        data = request.data['recipe_id']
        recipe =  Recipe.objects.values('ingredients__ingredient__id','ingredients__ingredient__name','ingredients__ingredient__category__name','ingredients__ingredient__mesurement').filter(id=data).distinct()
        recipe_dict = {}
        for r in recipe:
            print(r['ingredients__ingredient__id'])
            recipe_dict[r['ingredients__ingredient__id']] = [r['ingredients__ingredient__id'],
                                                             r['ingredients__ingredient__name'],
                                                             r['ingredients__ingredient__category__name'],
                                                             r['ingredients__ingredient__mesurement'],]
        return JsonResponse(recipe_dict)

class IngredientVege(generics.ListAPIView):
    serializer_class = IngredientSerializer
    def get(self,request,*args,**kwargs):
        recipe_id = request.data['recipe_id']
        ingredient__id = request.data['ingredient_id']
        recipe =  RecipeXEngredient.objects.filter(recipe__id=recipe_id,age=Ages.GG,ingredient__id = ingredient__id).values('vege').distinct()
        return JsonResponse({'vege':recipe[0]['vege']})


class IngredientQuant(generics.ListAPIView):
    serializer_class = IngredientSerializer
    def get(self,request,*args,**kwargs):
        age = request.data['age']
        ingredient__id = request.data['ingredient_id']
        recipe_id = request.data['recipe_id']
        anim =  RecipeXEngredient.objects.filter(recipe__id=recipe_id,age=age,ingredient__id = ingredient__id).values('quantity').distinct()
        leaders =  RecipeXEngredient.objects.filter(recipe__id=recipe_id,age=Ages.GG,ingredient__id = ingredient__id).values('quantity').distinct()
        return JsonResponse({'anim':anim[0]['quantity'],'leaders':leaders[0]['quantity']})
    
from django.contrib.auth.models import User
from rest_framework import serializers, viewsets
from rest_framework.response import Response

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'password')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    http_method_names = ['post']

class CustomAuthToken(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        return Response({
            'token': token.key,
            'user_id': user.pk,
            'email': user.email
        })

from django.contrib.auth.views import LoginView as DjangoLoginView
from django.contrib.auth import login
from django.urls import path
from django.http import JsonResponse
from django.contrib.auth import authenticate, login

from django.http import JsonResponse
from django.contrib.auth import authenticate, login,logout
from django.http import JsonResponse
from django.middleware.csrf import get_token

def get_csrf_token(request):
    csrf_token = get_token(request)
    return JsonResponse({'csrfToken': csrf_token})

def CustomUserCreation(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        username = request.POST.get('username')
        password = request.POST.get('password')
        print(username,password)
        user = User.objects.create_user(email=email,username=username, password=password)
        if user:
            return JsonResponse({'message': 'Login successful'})
        else:
            return JsonResponse({'message': 'Invalid username or password'}, status=400)
    else:
        return JsonResponse({'message': 'Method not allowed'}, status=405)
def CustomLoginView(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        print(username,password)
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return JsonResponse({'message': 'Login successful'})
        else:
            return JsonResponse({'message': 'Invalid username or password'}, status=400)
    else:
        return JsonResponse({'message': 'Method not allowed'}, status=405)

def CustomLogoutView(request):
    logout(request)
    return JsonResponse({'message': 'Logged out successfully'})

def AuthenticatedView(request):
    if request.user.is_authenticated:
        return JsonResponse({'value':'True'})
    else:
        return JsonResponse({'value':'False'})