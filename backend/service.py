from fastapi import FastAPI, HTTPException
from ml_core.anime_recommender import AnimeRecommender
from backend.data_structure import RecommendationRequest

app = FastAPI()
recommender = AnimeRecommender(save_path="C:/Desktop/Desktop/Python/SystemProject/AnimeRecomendation/faiss")

@app.post("/recommend")
def get_anime_recommendation(request: RecommendationRequest):
    """
    Роут для выдачи аниме рекомендаций
    """
    if request.title:
        recommendation = recommender.recommend_by_title(title=request.title, k=request.k)
    elif request.synopsis:
        recommendation = recommender.recommend_by_synopsis(synopsis=request.synopsis, k=request.k)
    else:
        raise HTTPException(
            status_code=400,
            detail="Укажите либо title, либо synopsis"
        )
    responce = {"recommendation":recommendation}
    return responce
