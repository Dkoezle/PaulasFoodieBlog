from .models import Recipe
from django.utils import timezone
from django.shortcuts import render, get_object_or_404
from .forms import RecipeForm, RawAdvancedSearch
from django.shortcuts import redirect


def recipe_list(request):
    recipes = Recipe.objects.filter(published_date__lte=timezone.now()).order_by('-created_date')
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
    cuis_recipes = Recipe.objects.filter(published_date__lte=timezone.now(), cuisine=cuis).order_by('-created_date')
    cuis_name = dict(Recipe.cuisine_types)[cuis]
    return render(request, 'blog/recipe_cuisfilter.html', {'cuis_recipes': cuis_recipes, 'cuis_name': cuis_name})


def recipe_allerfilter(request, aller):
    if aller == "NA":
        aller_recipes = Recipe.objects.filter(published_date__lte=timezone.now()).\
            filter(contained_allergen__contains=aller).order_by('-created_date')
    else:
        aller_recipes = Recipe.objects.filter(published_date__lte=timezone.now()).\
            exclude(contained_allergen__contains=aller).order_by('-created_date')

    aller_name = dict(Recipe.allergen_types)[aller]
    return render(request, 'blog/recipe_allerfilter.html', {'aller_recipes': aller_recipes, 'aller_name': aller_name})


def advanced_search(request):
    if request.method == "POST":
        user_query = request.POST
        searchform = RawAdvancedSearch()
        query = {}
        search_results = Recipe.objects.filter(published_date__lte=timezone.now())
        if user_query['title'] != '':
            search_results = search_results.filter(title__contains=user_query['title'])
            query[searchform.fields['title'].label] = user_query['title']

        if user_query['diet'] == 'VGN':
            search_results = search_results.filter(is_vegan=True)
            query[searchform.fields['diet'].label] = 'Vegan'
        elif user_query['diet'] == 'VGT':
            search_results = search_results.filter(is_veggie=True)
            query[searchform.fields['diet'].label] = 'Vegetarisch'

        if user_query['cuisine'] != 'DEF':
            search_results = search_results.filter(cuisine=user_query['cuisine'])
            query[searchform.fields['cuisine'].label] = dict(RawAdvancedSearch.cuisine_types)[user_query['cuisine']]

        if user_query.getlist('allergens'):
            query[searchform.fields['allergens'].label] = []
            for allergen in user_query.getlist('allergens'):
                search_results = search_results.exclude(contained_allergen__contains=allergen)
                query[searchform.fields['allergens'].label].append(dict(RawAdvancedSearch.allergen_types)[allergen])
            query[searchform.fields['allergens'].label] = ', '.join(query[searchform.fields['allergens'].label])

        search_results = search_results.order_by('-created_date')
        return render(request, 'blog/recipe_advsearch_results.html', {'search_results': search_results, 'query': query})

    else:
        form = RawAdvancedSearch()
        return render(request, 'blog/advanced_search.html', {'form': form})
