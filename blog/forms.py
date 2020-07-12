from django import forms
from .models import Recipe

class RecipeForm(forms.ModelForm):

    class Meta:
        model = Recipe
        fields = ('title', 'image', 'is_vegan', 'is_veggie', 'cuisine',
                  'contained_allergen', 'instruction')


class RawAdvancedSearch(forms.Form):
    title = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Rezeptname enthält...', 'size': '60'}),
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
