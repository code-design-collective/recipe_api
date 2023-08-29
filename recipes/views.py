import json
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect
from django.views.decorators.csrf import csrf_exempt
from .models import Recipe
from .forms import RecipeForm

@csrf_exempt
def index(request):
    response_data = {"message": "Hello, world. You're at the recipes endpoint."}
    return JsonResponse(response_data)

@csrf_exempt
def recipe_list(request):
    print('RECIPE LIST')
    recipes = Recipe.objects.all()
    recipe_list = [{'id': recipe.id, 'title': recipe.title} for recipe in recipes]
    return JsonResponse(recipe_list, safe=False)

@csrf_exempt
def recipe_detail(request, pk):
    print('RECIPE DETAIL')
    recipe = get_object_or_404(Recipe, pk=pk)
    recipe_data = {
        'id': recipe.id,
        'title': recipe.title,
        'ingredients': recipe.ingredients,
        'instructions': recipe.instructions,
        'created_at': recipe.created_at,
    }
    return JsonResponse(recipe_data)

@csrf_exempt
def recipe_create(request):
    print('RECIPE CREATE')
    if request.method == 'POST':
        data = json.loads(request.body)
        print(request.body)
        form = RecipeForm(data)
        if form.is_valid():
            form.save()
            return JsonResponse({'message': 'Recipe created successfully'})
        else:
            return JsonResponse({'error': form.errors}, status=400)
    return JsonResponse({'error': 'Invalid request method'}, status=405)

@csrf_exempt
def recipe_update(request, pk):
    print('RECIPE UPDATE')
    recipe = get_object_or_404(Recipe, pk=pk)
    if request.method == 'PUT':
        data = json.loads(request.body)
        form = RecipeForm(data, instance=recipe)
        if form.is_valid():
            form.save()
            return JsonResponse({'message': 'Recipe updated successfully'})
        else:
            return JsonResponse({'error': form.errors}, status=400)
    return JsonResponse({'error': 'Invalid request method'}, status=405)

@csrf_exempt
def recipe_delete(request, pk):
    print('RECIPE DELETE')
    recipe = get_object_or_404(Recipe, pk=pk)
    if request.method == 'DELETE':
        recipe.delete()
        return JsonResponse({'message': 'Recipe deleted successfully'})
    return JsonResponse({'error': 'Invalid request method'}, status=405)
