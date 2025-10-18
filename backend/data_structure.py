from pydantic import BaseModel, Field
from typing import Optional

class RecommendationRequest(BaseModel):
    title: Optional[str] = Field(None, description="Название аниме")
    synopsis: Optional[str] = Field(None, description="Описание сюжета")
    k: int = Field(10, description="Количество рекомендаций", ge=1, le=50)
