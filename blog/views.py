from .models import Recipe, Ingredients
from django.utils import timezone
from django.shortcuts import render, get_object_or_404
from .forms import RecipeForm, RawAdvancedSearch
from django.shortcuts import redirect
from django.http import HttpResponseRedirect
from django.forms import inlineformset_factory


def recipe_list(request):
    recipes = Recipe.objects.filter(
        published_date__lte=timezone.now()).order_by('-created_date')
    return render(request, 'blog/recipe_list.html', {'recipes': recipes})


def recipe_detail(request, pk):
    recipe = get_object_or_404(Recipe, pk=pk)
    return render(request, 'blog/recipe_detail.html', {'recipe': recipe})


def recipe_new(request):
    IngredientFormset = inlineformset_factory(Recipe, Ingredients, fields=('amount', 'unit', 'ingredient'))

    if request.method == 'POST':
        form = RecipeForm(request.POST, request.FILES or None)
        if form.is_valid():
            recipe = form.save(commit=False)
            recipe.author = request.user
            recipe.published_date = timezone.now()
            formset = IngredientFormset(request.POST, instance=recipe)
            if formset.is_valid():
                recipe.save()
                formset.save()
                return redirect('recipe_detail', pk=recipe.pk)
    else:
        form = RecipeForm()
        formset = IngredientFormset()
        context = {'form': form,
                  'ingredformset': formset,
                  }
    return render(request, 'blog/recipe_edit.html', context)


def recipe_edit(request, pk):
    recipe = get_object_or_404(Recipe, pk=pk)
    IngredientFormset = inlineformset_factory(Recipe, Ingredients, fields=('amount', 'unit', 'ingredient'))

    if request.method == "POST":
        form = RecipeForm(request.POST, request.FILES or None, instance=recipe)
        print('tag1')
        if 'btn_submit' in request.POST:
            print('tag2')
            if form.is_valid():
                print('tag3')
                recipe = form.save(commit=False)
                recipe.author = request.user
                recipe.published_date = timezone.now()
                recipe.save()
                formset = IngredientFormset(request.POST, instance=recipe, initial=[{'id': ''}])
                if formset.is_valid():
                    print('tag4')
                    formset.save()
                    return redirect('recipe_detail', pk=recipe.pk)
        else:
            print('tag5')
            if 'btn_addfields' in request.POST:
                print('tag6')
                print(form.errors)
                if form.is_valid():
                    print('tag7')
                    recipe = form.save(commit=False)
                    recipe.author = request.user
                    recipe.published_date = timezone.now()
                    #recipe.save()
                    formset = IngredientFormset(request.POST, instance=recipe, initial=[{'id': ''}])
                    print(formset.errors)
                    if formset.is_valid():
                        print('tag8')
                        formset.save()
                        return redirect('recipe_edit', pk=recipe.pk)
    else:
        print('tag9')
        form = RecipeForm(instance=recipe)
        formset = IngredientFormset(instance=recipe)
        context = {'form': form,
                   'ingredformset': formset,
                   }
    return render(request, 'blog/recipe_edit.html', context)


def recipe_cuisfilter(request, cuis):
    if request.method == "POST":
        request.session['advsearch_data'] = dict(request.POST)
        return HttpResponseRedirect('/recipe/advsearch')
    else:
        cuis_recipes = Recipe.objects.filter(published_date__lte=timezone.now(),
                                             cuisine=cuis).order_by('-created_date')
        cuis_name = dict(Recipe.cuisine_types)[cuis]
        form = RawAdvancedSearch()

        context = {'cuis_recipes': cuis_recipes,
                   'cuis_name': cuis_name,
                   'form': form,
                   }
        return render(request, 'blog/recipe_cuisfilter.html', context)


def recipe_allerfilter(request, aller):
    if request.method == "POST":
        request.session['advsearch_data'] = dict(request.POST)
        return HttpResponseRedirect('/recipe/advsearch')
    else:
        if aller == "NA":
            aller_recipes = Recipe.objects.filter(published_date__lte=timezone.now()). \
                filter(contained_allergen__contains=aller).order_by('-created_date')
        else:
            aller_recipes = Recipe.objects.filter(published_date__lte=timezone.now()). \
                exclude(contained_allergen__contains=aller).order_by('-created_date')

        aller_name = dict(Recipe.allergen_types)[aller]
        form = RawAdvancedSearch()
        context = {'aller_recipes': aller_recipes,
                   'aller_name': aller_name,
                   'form': form,
                   }
        return render(request, 'blog/recipe_allerfilter.html', context)


def advanced_search(request):
    # suchanfragen (POST) können aus dieser oder auch aus anderen views reinkommen. Suchanfragen von anderen views
    # sind in request.session gespeichert
    if request.method == "POST" or request.session.get('advsearch_data'):
        # "rohe" suchanfrage lesen, je nachdem ob sie in POST oder in session stehen
        if request.session.get('advsearch_data', False):
            user_query = request.session.get('advsearch_data')
            # session löschen, damit daten beim nächsten aufruf nicht erneut verarbeitet werden
            del(request.session['advsearch_data'])
        else:
            user_query = dict(request.POST)
        searchform = RawAdvancedSearch()
        query = {}  # leeres dict, das mit sauberen Sucheinstellungen befüllt und an Ergebnis-HTML weitergegeben wird
        search_results = Recipe.objects.filter(
            published_date__lte=timezone.now())

        # nur wenn Titel-Textfeld nicht leer ist sollen rezepte nach Titel gefiltert werden
        if user_query['title'][0] != '':
            search_results = search_results.filter(title__contains=user_query['title'][0])
            # füge titel-einstellung zum query-dict hinzu,verwende Namen aus Formular (form.py) als key
            query[searchform.fields['title'].label] = user_query['title'][0]

        if user_query['diet'][0] == 'VGN':
            search_results = search_results.filter(is_vegan=True)
            query[searchform.fields['diet'].label] = 'Vegan'
        elif user_query['diet'][0] == 'VGT':
            search_results = search_results.filter(is_veggie=True)
            query[searchform.fields['diet'].label] = 'Vegetarisch'

        if user_query['cuisine'][0] != 'DEF':
            search_results = search_results.filter(cuisine=user_query['cuisine'][0])
            # verwende display-value aus Formular für das query-dict statt den cuisine_type key
            query[searchform.fields['cuisine'].label] = dict(RawAdvancedSearch.cuisine_types)[user_query['cuisine'][0]]

        # wenn mindestens ein Allergen angekreuzt wurde...
        if 'allergens' in user_query.keys():
            # ...initiiere leere liste im sauberen query-dict
            query[searchform.fields['allergens'].label] = []
            # ...und filtere jedes Allergen einzeln, welches in der rohen suchanfrage steht

            for allergen in user_query['allergens']:
                if allergen == "NA":
                    search_results = search_results.filter(contained_allergen__contains=allergen)
                else:
                    search_results = search_results.exclude(contained_allergen__contains=allergen)
                # hänge das allergen zur liste der allergene im sauberen query-dict an. Mit Bezeichnung aus Formular
                query[searchform.fields['allergens'].label].append(
                    dict(RawAdvancedSearch.allergen_types)[allergen])

            # wandle die saubere Allergen-Liste in einen komma-getrennten String um
            query[searchform.fields['allergens'].label] = ', '.join(
                query[searchform.fields['allergens'].label])

        # übergebe die Suchergebnisse und das saubere query-dict an die Suchergebnis-Seite
        search_results = search_results.order_by('-created_date')
        context = {'search_results': search_results,
                   'query': query,
                   'form': searchform,
                   }
        return render(request, 'blog/recipe_advsearch_results.html', context)

    else:
        form = RawAdvancedSearch()
        return render(request, 'blog/advanced_search.html', {'form': form})
