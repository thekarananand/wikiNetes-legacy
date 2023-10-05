from django.urls import path
from django.shortcuts import redirect
import random
from . import util

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("wiki/<str:Page>", views.RenderPage, name="RenderPage"),
    path("wiki/", views.index, name="index2"),
    path("search/", views.search, name="search"),
    path("new/", views.new, name="new"),
    path("random/", lambda request: redirect("/wiki/"+random.choice(util.list_entries())), name="RandomPage"),
    path("wiki/<str:Page>/edit/", views.editPage, name="editPage"),
    path("edit/", views.edit, name="edit"),
]
