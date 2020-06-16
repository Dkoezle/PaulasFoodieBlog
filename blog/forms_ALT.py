from django import forms
from .models import Recipe

class RecipeForm(forms.ModelForm):

    class Meta:
         model = Recipe
         fields = ('title', 'is_vegan', 'is_veggie', 'cuisine', 'contained_allergen', 'instruction', )


class RawRecipeForm(forms.Form):
    title = forms.CharField()
    is_vegan = forms.BooleanField(required=False, label='Vegan')
    is_veggie = forms.BooleanField(required=False, label='Vegetarisch')
    cuisine_types = (
        ('DEF', ''),
        ('INT', 'Internationale Kueche'),
        ('ASI', 'Asiatische Kueche'),
        ('AFR', 'Afrikanische Kueche'),
        ('EUR', 'Europäische Kueche'),
        ('AME', 'Amerikanische Kueche'),
        ('SUA', 'Suedamerikanische Kueche'),)
    cuisine = forms.ChoiceField(choices=cuisine_types)
    allergen_types = (
        ("nuts", "Nuesse"),
        ("glut", "Gluten"),
        ("lact", "Kuhmilch"),
        ("fish", "Fisch"),
        ("egg", "Huehnereier"),
    )
    contained_allergen = forms.MultipleChoiceField(widget=forms.CheckboxSelectMultiple, choices=allergen_types)
    instruction = forms.CharField(widget=forms.Textarea())
