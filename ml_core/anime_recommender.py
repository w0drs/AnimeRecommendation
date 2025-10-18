import pandas as pd
import os
import faiss
from sentence_transformers import SentenceTransformer


class AnimeRecommender:
    def __init__(self, df=None, save_path=None):
        """
        Инициализация: либо из датафрейма, либо из сохраненных данных
        """
        if save_path and os.path.exists(save_path) and df is None:
            self._load_from_disk(save_path)
        elif df is not None:
            self._build_from_scratch(df)
            if save_path:
                self._save_to_disk(save_path)
        else:
            raise ValueError("Нужно указать либо df, либо save_path")

    def _build_from_scratch(self, df):
        """Создаем систему с нуля"""
        print("Создаем систему рекомендаций с нуля...")
        self.df = df.reset_index(drop=True)
        self.model = SentenceTransformer('paraphrase-multilingual-MiniLM-L12-v2')
        self.index = None
        self._build_index()

    def _build_index(self):
        """Построение FAISS индекса"""
        descriptions = self.df['synopsis'].dropna().tolist()
        print(f"Кодируем {len(descriptions)} описаний...")
        embeddings = self.model.encode(descriptions)

        dimension = embeddings.shape[1]
        self.index = faiss.IndexFlatIP(dimension)

        faiss.normalize_L2(embeddings)
        self.index.add(embeddings.astype('float32'))
        print("Индекс построен!")

    def _save_to_disk(self, save_path):
        """Сохраняем систему на диск"""
        print(f"Сохраняем систему в {save_path}...")

        os.makedirs(save_path, exist_ok=True)
        faiss.write_index(self.index, f"{save_path}/index.faiss")
        self.df.to_parquet(f"{save_path}/data.parquet")

        print("Сохранение завершено!")

    def _load_from_disk(self, save_path):
        """Загружаем систему с диска"""
        print(f"Загружаем систему из {save_path}...")

        self.index = faiss.read_index(f"{save_path}/index.faiss")
        self.df = pd.read_parquet(f"{save_path}/data.parquet")
        self.model = SentenceTransformer('paraphrase-multilingual-MiniLM-L12-v2')

        print("Загрузка завершена!")

    def recommend_by_title(self, title, k=5):
        mask = self.df['title'].str.lower() == title.lower()

        if not mask.any():
            return [f"Аниме '{title}' не найдено"]

        anime_idx = int(mask[mask].index[0])
        return self._get_recommendations(anime_idx, k)

    def recommend_by_synopsis(self, synopsis, k=5):
        embeddings = self.model.encode([synopsis])

        embeddings = embeddings.astype('float32')
        faiss.normalize_L2(embeddings)

        distances, indices = self.index.search(embeddings, k)

        # СОЗДАЕМ ДАТАФРЕЙМ ТОЛЬКО С ЗАПИСЯМИ, У КОТОРЫХ ЕСТЬ ОПИСАНИЕ
        df_with_synopsis = self.df[self.df['synopsis'].notna()].reset_index(drop=True)

        results = []
        for i, idx in enumerate(indices[0]):
            if idx >= len(df_with_synopsis):
                print(
                    f"⚠️ Предупреждение: индекс {idx} выходит за границы датафрейма (размер: {len(df_with_synopsis)})")
                continue

            row = df_with_synopsis.iloc[idx]
            results.append({
                "title": row.get("title","noname title"),
                "similarity": float(distances[0][i]),
                "genres": row.get("genres", ""),
                "image_url": row.get("image_jpg_large_url",""),
                "themes": row.get("themes",""),
                "score": row.get("score","52"),
                "type": row.get("type",""),
                "year": row.get("year","")
            })

        return results

    def _get_recommendations(self, query_idx, k):
        query_vector = self.index.reconstruct(query_idx).reshape(1, -1)
        distances, indices = self.index.search(query_vector.astype('float32'), k + 1)

        results = []
        for i, idx in enumerate(indices[0]):
            if idx != query_idx:
                row = self.df.iloc[idx]
                results.append({
                    "title": row.get("title", "noname title"),
                    "similarity": float(distances[0][i]),
                    "genres": row.get("genres", ""),
                    "image_url": row.get("image_jpg_large_url", ""),
                    "themes": row.get("themes", ""),
                    "score": row.get("score", "52"),
                    "type": row.get("type", ""),
                    "year": row.get("year", "")
                })
        return results