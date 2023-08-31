import json

from django.conf import settings
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect
from django.views.decorators.csrf import csrf_exempt

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from .forms import RecipeForm
from .models import Recipe
from .serializers import RecipeSerializer

@api_view(['GET'])
def examples(request):
    json_file_path = settings.BASE_DIR / 'apps' / 'recipes' / 'sample.json'
    with open(json_file_path, 'r') as json_file:
        recipes = json.load(json_file)
    serializer = RecipeSerializer(recipes, many=True)

    return Response(serializer.data)

@api_view(['GET'])
def recipe_list(request):
    print('GET ALL')
    recipes = Recipe.objects.all()
    serializer = RecipeSerializer(recipes, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def recipe_detail(request, pk):
    print('GET DETAIL')
    recipe = get_object_or_404(Recipe, pk=pk)
    serializer = RecipeSerializer(recipe)
    return Response(serializer.data)

@api_view(['POST'])
def recipe_create(request):
    print('POST')
    serializer = RecipeSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response({'message': 'Recipe created successfully'}, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['PUT'])
def recipe_update(request, pk):
    print('PUT')
    recipe = get_object_or_404(Recipe, pk=pk)
    serializer = RecipeSerializer(recipe, data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response({'message': 'Recipe updated successfully'})
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['DELETE'])
def recipe_delete(request, pk):
    print('DELETE')
    recipe = get_object_or_404(Recipe, pk=pk)
    recipe.delete()
    return Response({'message': 'Recipe deleted successfully'}, status=status.HTTP_204_NO_CONTENT)
