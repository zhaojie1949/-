"""
知识卡片生成模块：为每个知识点生成详细的知识卡片
"""
import json
from anthropic import Anthropic
from .models import KnowledgePoint, KnowledgeCard


class CardGenerator:
    """知识卡片生成器"""

    def __init__(self, api_key: str, model: str = "claude-3-5-sonnet-20241022"):
        self.client = Anthropic(api_key=api_key)
        self.model = model

    def generate_card(self, knowledge_point: KnowledgePoint, original_transcript: str) -> KnowledgeCard:
        """
        为单个知识点生成详细的知识卡片

        Args:
            knowledge_point: 知识点信息
            original_transcript: 原始培训逐字稿（用于提取更多上下文）

        Returns:
            KnowledgeCard: 生成的知识卡片
        """
        prompt = f"""你是一位专业的教学内容设计师。请基于以下知识点和培训内容，生成一张清晰、结构化的知识卡片。

知识点信息：
- 标题：{knowledge_point.title}
- 描述：{knowledge_point.description}
- 分类：{knowledge_point.category}

原始培训内容（供参考，提取相关细节）：
{original_transcript}

请生成一张知识卡片，包含以下内容（以 JSON 格式返回）：

1. title: 卡片标题（使用知识点标题或优化后的版本）
2. subtitle: 副标题（可选，一句话概括核心价值）
3. key_points: 核心要点列表（3-5个要点，每个 20-40 字）
4. detailed_content: 详细内容说明（150-300字，深入解释这个知识点）
5. examples: 实际示例列表（2-3个实用示例）
6. tips: 提示和注意事项（2-3条实用建议）
7. related_topics: 相关主题（2-3个相关知识点）

要求：
- 内容要清晰易懂，适合快速学习和复习
- 要有实际价值，能够直接应用
- 语言简洁但不失准确性
- 结合培训内容中的具体例子

返回格式：
```json
{{
  "title": "知识点标题",
  "subtitle": "一句话概括",
  "key_points": [
    "要点1",
    "要点2",
    "要点3"
  ],
  "detailed_content": "详细说明...",
  "examples": [
    "示例1",
    "示例2"
  ],
  "tips": [
    "提示1",
    "提示2"
  ],
  "related_topics": [
    "相关主题1",
    "相关主题2"
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

        # 转换为 KnowledgeCard 对象
        return KnowledgeCard(**data)

    def generate_cards_batch(self, knowledge_points: list, original_transcript: str) -> list:
        """
        批量生成知识卡片

        Args:
            knowledge_points: 知识点列表
            original_transcript: 原始培训逐字稿

        Returns:
            list: 知识卡片列表
        """
        cards = []
        for point in knowledge_points:
            card = self.generate_card(point, original_transcript)
            cards.append(card)

        return cards
