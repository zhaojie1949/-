"""
数据模型定义
"""
from typing import List, Optional
from pydantic import BaseModel, Field


class KnowledgePoint(BaseModel):
    """单个知识点"""
    title: str = Field(description="知识点标题")
    description: str = Field(description="知识点描述")
    importance: int = Field(description="重要性等级 1-5", ge=1, le=5)
    category: Optional[str] = Field(default=None, description="知识点分类")


class KnowledgeCard(BaseModel):
    """知识卡片"""
    title: str = Field(description="卡片标题")
    subtitle: Optional[str] = Field(default=None, description="副标题")
    key_points: List[str] = Field(description="核心要点列表")
    detailed_content: str = Field(description="详细内容说明")
    examples: Optional[List[str]] = Field(default=None, description="示例列表")
    tips: Optional[List[str]] = Field(default=None, description="提示和注意事项")
    related_topics: Optional[List[str]] = Field(default=None, description="相关主题")


class TrainingOverview(BaseModel):
    """培训总览"""
    title: str = Field(description="培训主题")
    summary: str = Field(description="培训摘要")
    main_categories: List[str] = Field(description="主要分类")
    knowledge_points: List[KnowledgePoint] = Field(description="核心知识点")
    total_cards: int = Field(description="生成的卡片总数")


class ProcessingResult(BaseModel):
    """处理结果"""
    overview: TrainingOverview
    cards: List[KnowledgeCard]
    success: bool = True
    message: Optional[str] = None
