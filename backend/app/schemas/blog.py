from pydantic import BaseModel, Field
from typing import List
from datetime import datetime
from uuid import UUID

class BlogCreate(BaseModel):
    title: str
    content: str
    tags: List[str]
    topic: str

class BlogOut(BaseModel):
    id: UUID
    title: str
    content: str
    tags: List[str]
    topic: str
    created_at: datetime
    
    class Config:
        from_attributes = True

class BlogListItem(BaseModel):
    id: UUID
    title: str
    preview: str
    tags: List[str]
    created_at: datetime

class GenerateRequest(BaseModel):
    topic: str

class ChatRequest(BaseModel):
    question: str
    blog_id: str

class ChatResponse(BaseModel):
    answer: str

class SearchResult(BaseModel):
    id: str
    title: str
    preview: str
    tags: List[str]
