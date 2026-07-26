# recommender/ml/engine.py
import numpy as np
from sklearn.neighbors import NearestNeighbors
from recommender.models import Song


class RecommendationEngine:
    _instance = None

    def __init__(self):
        songs = list(Song.objects.select_related("artist").all())
        self.songs = songs
        self.embedding = np.array([[s.embedding_x, s.embedding_y] for s in songs])
        self.id_to_index = {s.id: i for i, s in enumerate(songs)}
        self.model = NearestNeighbors(n_neighbors=6).fit(self.embedding)

    @classmethod
    def get_instance(cls):
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance

    # recommender/ml/engine.py
    def recommend(self, song_id, top_k=5):
        idx = self.id_to_index[song_id]
        distances, indices = self.model.kneighbors(
            [self.embedding[idx]], n_neighbors=top_k + 1
        )
        results = []
        for dist, i in zip(distances[0][1:], indices[0][1:]):
            s = self.songs[i]
            results.append({
                "id": s.id,
                "track_name": s.track_name,
                "artist_name": s.artist.name,
                "distance": float(dist),
                "similarity": 1 / (1 + float(dist)),
            })
        return results