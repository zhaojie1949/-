"""
培训知识卡片生成 Agent
主控制器，协调各个模块完成知识卡片生成
"""
import os
from pathlib import Path
from typing import Optional
from rich.console import Console
from rich.progress import Progress, SpinnerColumn, TextColumn

from .knowledge_extractor import KnowledgeExtractor
from .card_generator import CardGenerator
from .overview_generator import OverviewGenerator
from .models import ProcessingResult


class TrainingKnowledgeCardAgent:
    """培训知识卡片生成 Agent"""

    def __init__(
        self,
        api_key: str,
        model: str = "claude-3-5-sonnet-20241022",
        output_dir: str = "./output",
        max_cards: int = 8
    ):
        """
        初始化 Agent

        Args:
            api_key: Anthropic API Key
            model: Claude 模型名称
            output_dir: 输出目录
            max_cards: 最大卡片数量
        """
        self.api_key = api_key
        self.model = model
        self.output_dir = Path(output_dir)
        self.max_cards = max_cards
        self.console = Console()

        # 初始化各个模块
        self.extractor = KnowledgeExtractor(api_key, model)
        self.card_generator = CardGenerator(api_key, model)
        self.overview_generator = OverviewGenerator()

        # 确保输出目录存在
        self.output_dir.mkdir(parents=True, exist_ok=True)
        (self.output_dir / "cards").mkdir(parents=True, exist_ok=True)

    def load_transcript(self, file_path: str) -> str:
        """
        加载培训逐字稿

        Args:
            file_path: 文件路径

        Returns:
            str: 逐字稿内容
        """
        with open(file_path, "r", encoding="utf-8") as f:
            return f.read()

    def process(self, transcript_path: str) -> ProcessingResult:
        """
        处理培训逐字稿，生成知识卡片

        Args:
            transcript_path: 培训逐字稿文件路径

        Returns:
            ProcessingResult: 处理结果
        """
        try:
            # 加载逐字稿
            self.console.print(f"[cyan]正在加载培训逐字稿: {transcript_path}[/cyan]")
            transcript = self.load_transcript(transcript_path)
            self.console.print(f"[green]✓ 已加载 {len(transcript)} 字符[/green]\n")

            # 提取知识总览
            with Progress(
                SpinnerColumn(),
                TextColumn("[progress.description]{task.description}"),
                console=self.console,
            ) as progress:
                task = progress.add_task("[cyan]正在分析培训内容，提取核心知识点...", total=None)
                overview = self.extractor.extract_overview(transcript)
                progress.update(task, completed=True)

            self.console.print(f"[green]✓ 已提取 {len(overview.knowledge_points)} 个核心知识点[/green]")
            self.console.print(f"[blue]培训主题: {overview.title}[/blue]\n")

            # 限制卡片数量
            knowledge_points = overview.knowledge_points[:self.max_cards]
            overview.total_cards = len(knowledge_points)

            # 生成知识卡片
            self.console.print(f"[cyan]正在生成 {len(knowledge_points)} 张知识卡片...[/cyan]")
            cards = []

            with Progress(
                SpinnerColumn(),
                TextColumn("[progress.description]{task.description}"),
                console=self.console,
            ) as progress:
                for i, point in enumerate(knowledge_points, 1):
                    task = progress.add_task(
                        f"[cyan]生成卡片 {i}/{len(knowledge_points)}: {point.title}",
                        total=None
                    )
                    card = self.card_generator.generate_card(point, transcript)
                    cards.append(card)
                    progress.update(task, completed=True)

            self.console.print(f"[green]✓ 已生成 {len(cards)} 张知识卡片[/green]\n")

            # 生成总览文档
            self.console.print("[cyan]正在生成总览文档...[/cyan]")
            overview_md = self.overview_generator.generate_overview_markdown(overview, cards)
            overview_path = self.output_dir / "overview.md"
            with open(overview_path, "w", encoding="utf-8") as f:
                f.write(overview_md)
            self.console.print(f"[green]✓ 已保存总览: {overview_path}[/green]")

            # 生成知识卡片文档
            self.console.print("[cyan]正在保存知识卡片...[/cyan]")
            for i, card in enumerate(cards, 1):
                card_md = self.overview_generator.generate_card_markdown(card, i)
                card_path = self.output_dir / "cards" / f"card_{i:02d}.md"
                with open(card_path, "w", encoding="utf-8") as f:
                    f.write(card_md)

            self.console.print(f"[green]✓ 已保存 {len(cards)} 张卡片到: {self.output_dir / 'cards'}[/green]\n")

            # 显示成功信息
            self.console.print("[bold green]🎉 知识卡片生成完成！[/bold green]")
            self.console.print(f"\n[yellow]输出目录: {self.output_dir.absolute()}[/yellow]")
            self.console.print(f"[yellow]- 总览: overview.md[/yellow]")
            self.console.print(f"[yellow]- 卡片: cards/card_01.md ~ cards/card_{len(cards):02d}.md[/yellow]")

            return ProcessingResult(
                overview=overview,
                cards=cards,
                success=True,
                message="处理成功"
            )

        except Exception as e:
            self.console.print(f"[bold red]❌ 处理失败: {str(e)}[/bold red]")
            return ProcessingResult(
                overview=None,
                cards=[],
                success=False,
                message=f"处理失败: {str(e)}"
            )
