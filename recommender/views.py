# recommender/views.py
import json
from django.shortcuts import render, get_object_or_404
from .models import Song
from .ml.engine import RecommendationEngine
from .forms import SongSearchForm
from django.db import models

def song_list(request):
    songs = Song.objects.select_related("artist").order_by("track_name")
    return render(request, "recommender/song_list.html", {"songs": songs})


def song_detail(request, song_id):
    song = get_object_or_404(Song, id=song_id)
    return render(request, "recommender/song_detail.html", {"song": song})


def recommend(request, song_id):
    song = get_object_or_404(Song, id=song_id)
    engine = RecommendationEngine.get_instance()
    results = engine.recommend(song_id=song.id, top_k=5)
    return render(
        request,
        "recommender/recommendations.html",
        {"song": song, "results": results},
    )


def embedding_map(request):
    songs = Song.objects.select_related("artist").all()
    points = [
        {
            "id": s.id,
            "name": s.track_name,
            "artist": s.artist.name,
            "x": s.embedding_x,
            "y": s.embedding_y,
        }
        for s in songs
    ]
    return render(
        request,
        "recommender/embedding_map.html",
        {"points": points},
    )

def song_list(request):
    form = SongSearchForm(request.GET)
    songs = Song.objects.select_related("artist").order_by("track_name")

    if form.is_valid() and form.cleaned_data["q"]:
        query = form.cleaned_data["q"]
        songs = songs.filter(
            models.Q(track_name__icontains=query) | models.Q(artist__name__icontains=query)
        )

    return render(request, "recommender/song_list.html", {"songs": songs, "form": form})
