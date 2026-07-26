# recommender/admin.py
from django.contrib import admin
from .models import Artist, Song


@admin.register(Artist)
class ArtistAdmin(admin.ModelAdmin):
    list_display = ("name",)
    search_fields = ("name",)


@admin.register(Song)
class SongAdmin(admin.ModelAdmin):
    list_display = ("track_name", "artist", "tempo", "valence")
    search_fields = ("track_name", "artist__name")
    list_filter = ("artist",)