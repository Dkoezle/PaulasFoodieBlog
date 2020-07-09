from django.urls import path
from . import views


urlpatterns = [
    path('', views.recipe_list, name='recipe_list'),
    path('recipe/<int:pk>/', views.recipe_detail, name='recipe_detail'),
    path('recipe/new/', views.recipe_new, name='recipe_new'),
    path('recipe/<int:pk>/edit/', views.recipe_edit, name='recipe_edit'),
    path('recipe/filter/cuis=<str:cuis>/', views.recipe_cuisfilter, name='recipe_cuisfilter'),
    path('recipe/filter/aller=<str:aller>/', views.recipe_allerfilter, name='recipe_allerfilter'),
    path('recipe/advsearch', views.advanced_search, name='advanced_search'),
]
