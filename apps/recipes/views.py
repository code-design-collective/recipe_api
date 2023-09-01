import json

from django.conf import settings
from django.shortcuts import get_object_or_404

from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated

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
@permission_classes([IsAuthenticated])
def recipe_list(request):
    user = request.user
    recipes = Recipe.objects.filter(author=user)
    serializer = RecipeSerializer(recipes, many=True)
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def recipe_detail(request, pk):
    recipe = get_object_or_404(Recipe, pk=pk)
    if recipe.author != request.user:
        return Response({'error': 'Error'}, status=status.HTTP_403_FORBIDDEN)

    serializer = RecipeSerializer(recipe)
    return Response(serializer.data)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def recipe_create(request):
    serializer = RecipeSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save(author=request.user)
        return Response({'message': 'Recipe created successfully'}, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def recipe_update(request, pk):
    recipe = get_object_or_404(Recipe, pk=pk)
    if recipe.author != request.user:
        return Response({'error': 'You are not authorized to edit this recipe'}, status=status.HTTP_403_FORBIDDEN)

    serializer = RecipeSerializer(recipe, data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response({'message': 'Recipe updated successfully'})
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def recipe_delete(request, pk):
    recipe = get_object_or_404(Recipe, pk=pk)
    if recipe.author != request.user:
        return Response({'error': 'You are not authorized to delete this recipe'}, status=status.HTTP_403_FORBIDDEN)

    recipe.delete()
    return Response({'message': 'Recipe deleted successfully'}, status=status.HTTP_204_NO_CONTENT)
