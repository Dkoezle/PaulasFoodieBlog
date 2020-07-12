from django.conf import settings
from django.db import models
from django.utils import timezone
from multiselectfield import MultiSelectField


class Recipe(models.Model):
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    image = models.ImageField(upload_to="images", blank=True)
    is_vegan = models.BooleanField("Vegan", default=False)
    is_veggie = models.BooleanField("Vegetarisch", default=False)
    cuisine_types = (
        ('DEF', ''),
        ('INT', 'Internationale Küche'),
        ('ASI', 'Asiatische Küche'),
        ('AFR', 'Afrikanische Küche'),
        ('EUR', 'Europäische Küche'),
        ('AME', 'Amerikanische Küche'),
        ('SUA', 'Südamerikanische Küche'),)
    cuisine = models.CharField(
        max_length=30, choices=cuisine_types, default='DEF')
    allergen_types = (
        ("NA", "Keine"),
        ("nuts", "Nüsse"),
        ("glut", "Gluten"),
        ("lact", "Laktose"),
        ("fish", "Fisch"),
        ("egg", "Hühnereier"),
    )
    contained_allergen = MultiSelectField(choices=allergen_types)
    instruction = models.TextField()
    created_date = models.DateTimeField(default=timezone.now)
    published_date = models.DateTimeField(blank=True, null=True)

    def publish(self):
        self.published_date = timezone.now()
        self.save()

    def __str__(self):
        return self.title
