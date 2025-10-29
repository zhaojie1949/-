"""
知识提取模块：从培训逐字稿中提取核心知识点
"""
import json
from typing import List
from anthropic import Anthropic
from .models import KnowledgePoint, TrainingOverview


class KnowledgeExtractor:
    """知识提取器"""

    def __init__(self, api_key: str, model: str = "claude-3-5-sonnet-20241022"):
        self.client = Anthropic(api_key=api_key)
        self.model = model

    def extract_overview(self, transcript: str) -> TrainingOverview:
        """
        从培训逐字稿中提取总览信息

        Args:
            transcript: 培训逐字稿文本

        Returns:
            TrainingOverview: 培训总览信息
        """
        prompt = f"""你是一位专业的培训内容分析师。请仔细阅读以下培训逐字稿，然后提取和总结核心信息。

培训逐字稿：
{transcript}

请分析这份培训内容，并提供以下信息（以 JSON 格式返回）：

1. title: 培训的主题（简洁明了，10-20字）
2. summary: 培训的核心摘要（100-200字，涵盖主要内容）
3. main_categories: 主要知识分类（3-6个分类）
4. knowledge_points: 核心知识点列表（每个知识点包含：）
   - title: 知识点标题
   - description: 知识点描述（30-50字）
   - importance: 重要性等级（1-5，5最重要）
   - category: 所属分类

请识别出 8-15 个最核心、最有价值的知识点，这些知识点将用于生成独立的知识卡片。

返回格式：
```json
{{
  "title": "培训主题",
  "summary": "培训摘要...",
  "main_categories": ["分类1", "分类2", "分类3"],
  "knowledge_points": [
    {{
      "title": "知识点标题",
      "description": "知识点描述",
      "importance": 5,
      "category": "分类1"
    }}
  ]
}}
```

只返回 JSON，不要有其他内容。"""

        response = self.client.messages.create(
            model=self.model,
            max_tokens=4096,
            messages=[{"role": "user", "content": prompt}]
        )

        # 提取 JSON 内容
        content = response.content[0].text.strip()

        # 移除可能的 markdown 代码块标记
        if content.startswith("```json"):
            content = content[7:]
        if content.startswith("```"):
            content = content[3:]
        if content.endswith("```"):
            content = content[:-3]
        content = content.strip()

        # 解析 JSON
        data = json.loads(content)

        # 转换为 TrainingOverview 对象
        return TrainingOverview(
            title=data["title"],
            summary=data["summary"],
            main_categories=data["main_categories"],
            knowledge_points=[KnowledgePoint(**kp) for kp in data["knowledge_points"]],
            total_cards=len(data["knowledge_points"])
        )

    def extract_knowledge_points(self, transcript: str, max_points: int = 10) -> List[KnowledgePoint]:
        """
        提取指定数量的核心知识点

        Args:
            transcript: 培训逐字稿
            max_points: 最大知识点数量

        Returns:
            List[KnowledgePoint]: 知识点列表
        """
        overview = self.extract_overview(transcript)

        # 按重要性排序，取前 max_points 个
        sorted_points = sorted(
            overview.knowledge_points,
            key=lambda x: x.importance,
            reverse=True
        )

        return sorted_points[:max_points]
