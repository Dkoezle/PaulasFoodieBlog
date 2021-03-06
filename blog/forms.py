from decimal import Decimal
from django import forms
from django.forms import formset_factory

from .models import Recipe

class RecipeForm(forms.ModelForm):

    class Meta:
        model = Recipe
        widgets = {
            'title': forms.TextInput(attrs={'size': '60%'}),
            'instruction': forms.Textarea(attrs={'style': 'width: 100%'}),
        }
        fields = ('title', 'image', 'is_vegan', 'is_veggie', 'cuisine',
                  'contained_allergen', 'instruction')


class IngredientFormFields (forms.Form):

    amount = forms.DecimalField(min_value=Decimal('0.01'),
                                widget=forms.NumberInput(attrs={'style': 'width: 5%'}))
    unit = forms.CharField(max_length=10)
    ingredient = forms.CharField(widget=forms.TextInput(attrs={'style': 'width: 100%'}),
                                 max_length=30)

IngredientFormset = formset_factory(IngredientFormFields, extra=5)


class RawAdvancedSearch(forms.Form):
    title = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Rezeptname enthält...', 'size': '25'}),
                            max_length=30, label="Rezeptname", required=False)
    diet_types = (
        ('DEF', 'Egal'),
        ('VGN', 'Vegan'),
        ('VGT', 'Vegetarisch'),)
    diet = forms.ChoiceField(choices=diet_types, label="Ernährungsform")

    cuisine_types = (
        ('DEF', 'Egal'),
        ('INT', 'Internationale Küche'),
        ('ASI', 'Asiatische Küche'),
        ('AFR', 'Afrikanische Küche'),
        ('EUR', 'Europäische Küche'),
        ('SUA', 'Südamerikanische Küche'),)
    cuisine = forms.ChoiceField(choices=cuisine_types, label="Kategorie")

    allergen_types = Recipe.allergen_types

    allergens = forms.MultipleChoiceField(widget=forms.CheckboxSelectMultiple,
                                          choices=allergen_types, label="Diese Allergene ausschließen")
