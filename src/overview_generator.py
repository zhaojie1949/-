"""
总图生成模块：生成知识点总览和思维导图
"""
from typing import List
from .models import TrainingOverview, KnowledgeCard


class OverviewGenerator:
    """总图生成器"""

    @staticmethod
    def generate_mermaid_mindmap(overview: TrainingOverview) -> str:
        """
        生成 Mermaid 思维导图

        Args:
            overview: 培训总览信息

        Returns:
            str: Mermaid 格式的思维导图代码
        """
        # 按分类组织知识点
        category_points = {}
        for point in overview.knowledge_points:
            category = point.category or "其他"
            if category not in category_points:
                category_points[category] = []
            category_points[category].append(point)

        # 生成 Mermaid 代码
        mermaid = ["```mermaid", "mindmap"]
        mermaid.append(f"  root(({overview.title}))")

        for category, points in category_points.items():
            mermaid.append(f"    {category}")
            for point in points:
                # 根据重要性添加标记
                importance_mark = "⭐" * point.importance
                mermaid.append(f"      {point.title} {importance_mark}")

        mermaid.append("```")

        return "\n".join(mermaid)

    @staticmethod
    def generate_overview_markdown(
        overview: TrainingOverview,
        cards: List[KnowledgeCard]
    ) -> str:
        """
        生成总览 Markdown 文档

        Args:
            overview: 培训总览信息
            cards: 知识卡片列表

        Returns:
            str: Markdown 格式的总览文档
        """
        md = [f"# {overview.title}\n"]

        # 培训摘要
        md.append("## 📋 培训摘要\n")
        md.append(f"{overview.summary}\n")

        # 思维导图
        md.append("## 🗺️ 知识总览\n")
        md.append(OverviewGenerator.generate_mermaid_mindmap(overview))
        md.append("")

        # 主要分类
        md.append("## 📚 主要分类\n")
        for i, category in enumerate(overview.main_categories, 1):
            md.append(f"{i}. **{category}**")
        md.append("")

        # 核心知识点列表
        md.append("## 💡 核心知识点\n")

        # 按分类组织
        category_points = {}
        for point in overview.knowledge_points:
            category = point.category or "其他"
            if category not in category_points:
                category_points[category] = []
            category_points[category].append(point)

        for category, points in category_points.items():
            md.append(f"### {category}\n")
            for i, point in enumerate(points, 1):
                importance = "⭐" * point.importance
                md.append(f"{i}. **{point.title}** {importance}")
                md.append(f"   - {point.description}")
            md.append("")

        # 卡片索引
        md.append("## 🎴 知识卡片索引\n")
        md.append(f"共生成 {len(cards)} 张知识卡片：\n")
        for i, card in enumerate(cards, 1):
            md.append(f"{i}. [{card.title}](./cards/card_{i:02d}.md)")
            if card.subtitle:
                md.append(f"   > {card.subtitle}")
        md.append("")

        # 使用说明
        md.append("## 📖 使用说明\n")
        md.append("1. 先阅读本总览，了解培训内容的整体结构")
        md.append("2. 根据思维导图和知识点列表，确定学习重点")
        md.append("3. 点击卡片索引中的链接，深入学习每个知识点")
        md.append("4. 每张卡片都包含核心要点、详细说明、示例和实用建议")
        md.append("5. 建议按照重要性（星级）优先学习高价值内容\n")

        md.append("---")
        md.append("*本知识卡片由 AI 自动生成，基于培训逐字稿提取核心内容*")

        return "\n".join(md)

    @staticmethod
    def generate_card_markdown(card: KnowledgeCard, card_number: int) -> str:
        """
        生成单张知识卡片的 Markdown 文档

        Args:
            card: 知识卡片
            card_number: 卡片编号

        Returns:
            str: Markdown 格式的卡片文档
        """
        md = [f"# 📇 卡片 {card_number:02d}: {card.title}\n"]

        # 副标题
        if card.subtitle:
            md.append(f"> {card.subtitle}\n")

        # 核心要点
        md.append("## 🎯 核心要点\n")
        for i, point in enumerate(card.key_points, 1):
            md.append(f"{i}. {point}")
        md.append("")

        # 详细内容
        md.append("## 📝 详细说明\n")
        md.append(f"{card.detailed_content}\n")

        # 示例
        if card.examples:
            md.append("## 💡 实际示例\n")
            for i, example in enumerate(card.examples, 1):
                md.append(f"### 示例 {i}\n")
                md.append(f"{example}\n")

        # 提示和注意事项
        if card.tips:
            md.append("## ⚠️ 提示与注意事项\n")
            for i, tip in enumerate(card.tips, 1):
                md.append(f"{i}. {tip}")
            md.append("")

        # 相关主题
        if card.related_topics:
            md.append("## 🔗 相关主题\n")
            for topic in card.related_topics:
                md.append(f"- {topic}")
            md.append("")

        md.append("---")
        md.append("[← 返回总览](../overview.md)")

        return "\n".join(md)
