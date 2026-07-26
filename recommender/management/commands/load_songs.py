# recommender/management/commands/load_songs.py
import pandas as pd
import umap.umap_ as umap
from sklearn.preprocessing import StandardScaler
from django.core.management.base import BaseCommand
from recommender.models import Artist, Song

FEATURES = ["danceability", "energy", "acousticness", "instrumentalness", "tempo", "valence"]


class Command(BaseCommand):
    help = "Load Spotify CSV, run UMAP once, populate the database"

    def add_arguments(self, parser):
        parser.add_argument("--csv", default="data/SpotifyAudioFeaturesApril2019.csv")
        parser.add_argument("--limit", type=int, default=2000, help="cap rows for a fast local demo")

    def handle(self, *args, **options):
        df = pd.read_csv(options["csv"])
        df = df.dropna(subset=FEATURES)
        df = df.drop_duplicates(subset="track_id")
        df = df.head(options["limit"])

        X = StandardScaler().fit_transform(df[FEATURES])
        reducer = umap.UMAP(n_neighbors=15, min_dist=0.3, metric="euclidean", random_state=42)
        embedding = reducer.fit_transform(X)

        Song.objects.all().delete()
        Artist.objects.all().delete()

        for (_, row), (x, y) in zip(df.iterrows(), embedding):
            artist, _ = Artist.objects.get_or_create(name=row["artist_name"])
            Song.objects.create(
                track_id=row["track_id"],
                track_name=row["track_name"],
                artist=artist,
                danceability=row["danceability"],
                energy=row["energy"],
                acousticness=row["acousticness"],
                instrumentalness=row["instrumentalness"],
                tempo=row["tempo"],
                valence=row["valence"],
                embedding_x=float(x),
                embedding_y=float(y),
            )

        self.stdout.write(self.style.SUCCESS(f"Loaded {Song.objects.count()} songs"))