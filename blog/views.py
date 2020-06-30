from django.shortcuts import render
from .models import Recipe
from django.utils import timezone
from django.shortcuts import render, get_object_or_404
from .forms import RecipeForm, AdvancedSearch
from django.shortcuts import redirect


def recipe_list(request):
    recipes = Recipe.objects.filter(published_date__lte=timezone.now()).order_by('created_date')
    return render(request, 'blog/recipe_list.html', {'recipes': recipes})


def recipe_detail(request, pk):
    recipe = get_object_or_404(Recipe, pk=pk)
    return render(request, 'blog/recipe_detail.html', {'recipe': recipe})


def recipe_new(request):
    if request.method == 'POST':
        form = RecipeForm(request.POST)
        if form.is_valid():
            recipe = form.save(commit=False)
            recipe.author = request.user
            recipe.published_date = timezone.now()
            recipe.save()
            return redirect('recipe_detail', pk=recipe.pk)
    else:
        form = RecipeForm()
    return render(request, 'blog/recipe_edit.html', {'form': form})


def recipe_edit(request, pk):
    recipe = get_object_or_404(Recipe, pk=pk)
    if request.method == "POST":
        form = RecipeForm(request.POST, instance=recipe)
        if form.is_valid():
            recipe = form.save(commit=False)
            recipe.author = request.user
            recipe.published_date = timezone.now()
            recipe.save()
            return redirect('recipe_detail', pk=recipe.pk)
    else:
        form = RecipeForm(instance=recipe)
    return render(request, 'blog/recipe_edit.html', {'form': form})

def recipe_cuisfilter(request, cuis):
    cuis_recipes = Recipe.objects.filter(published_date__lte=timezone.now(), cuisine=cuis)
    cuis_name = dict(Recipe.cuisine_types)[cuis]
    return render(request, 'blog/recipe_cuisfilter.html', {'cuis_recipes': cuis_recipes, 'cuis_name': cuis_name})


def recipe_allerfilter(request, aller):
    aller_recipes = Recipe.objects.filter(published_date__lte=timezone.now(), contained_allergen=aller)
    aller_name = dict(Recipe.allergen_types)[aller]
    return render(request, 'blog/recipe_allerfilter.html', {'aller_recipes': aller_recipes, 'aller_name': aller_name})


def advanced_search(request):
    form = AdvancedSearch()
    return render(request, 'blog/advanced_search.html', {'form': form})
