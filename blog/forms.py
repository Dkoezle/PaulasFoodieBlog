from django import forms
from .models import Recipe

class RecipeForm(forms.ModelForm):

    class Meta:
        model = Recipe
        fields = ('title', 'is_vegan', 'is_veggie', 'cuisine',
                  'contained_allergen', 'instruction')


class RawRecipeForm(forms.Form):
    title = forms.CharField()
    is_vegan = forms.BooleanField(required=False, label='Vegan')
    is_veggie = forms.BooleanField(required=False, label='Vegetarisch')
    cuisine_types = (
        ('DEF', 'Keine'),
        ('INT', 'Internationale Küche'),
        ('ASI', 'Asiatische Küche'),
        ('AFR', 'Afrikanische Küche'),
        ('EUR', 'Europäische Küche'),
        ('AME', 'Amerikanische Küche'),
        ('SUA', 'Südamerikanische Küche'),)
    cuisine = forms.ChoiceField(choices=cuisine_types)
    allergen_types = (
        ("nuts", "Nüsse"),
        ("glut", "Gluten"),
        ("lact", "Kuhmilch"),
        ("fish", "Fisch"),
        ("egg", "Hühnereier"),
    )
    contained_allergen = forms.MultipleChoiceField(
        widget=forms.CheckboxSelectMultiple, choices=allergen_types)
    instruction = forms.CharField(widget=forms.Textarea())

class AdvancedSearch(forms.ModelForm):

    class Meta:
        model = Recipe
        fields = ('is_vegan', 'is_veggie', 'cuisine', 'contained_allergen')
