#!/usr/bin/env python3
"""
培训知识卡片生成器 - 命令行入口
"""
import os
import sys
import argparse
from pathlib import Path
from dotenv import load_dotenv
from rich.console import Console

from src.agent import TrainingKnowledgeCardAgent


def main():
    """主函数"""
    # 加载环境变量
    load_dotenv()

    # 解析命令行参数
    parser = argparse.ArgumentParser(
        description="培训知识卡片生成器 - 将培训逐字稿转化为结构化知识卡片",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  %(prog)s --input training.txt
  %(prog)s --input training.txt --output ./my_cards
  %(prog)s --input training.txt --max-cards 10

更多信息请访问: https://github.com/yourusername/training-knowledge-cards
        """
    )

    parser.add_argument(
        "-i", "--input",
        required=True,
        help="培训逐字稿文件路径（.txt 或 .md）"
    )

    parser.add_argument(
        "-o", "--output",
        default=os.getenv("OUTPUT_DIR", "./output"),
        help="输出目录（默认: ./output）"
    )

    parser.add_argument(
        "-m", "--max-cards",
        type=int,
        default=int(os.getenv("MAX_CARDS", "8")),
        help="最大卡片数量（默认: 8）"
    )

    parser.add_argument(
        "--model",
        default=os.getenv("CLAUDE_MODEL", "claude-3-5-sonnet-20241022"),
        help="Claude 模型（默认: claude-3-5-sonnet-20241022）"
    )

    parser.add_argument(
        "--api-key",
        default=os.getenv("ANTHROPIC_API_KEY"),
        help="Anthropic API Key（也可通过环境变量 ANTHROPIC_API_KEY 设置）"
    )

    args = parser.parse_args()

    # 初始化控制台
    console = Console()

    # 显示欢迎信息
    console.print("\n[bold cyan]🎴 培训知识卡片生成器[/bold cyan]")
    console.print("[dim]将培训逐字稿转化为结构化的知识卡片[/dim]\n")

    # 检查 API Key
    if not args.api_key:
        console.print("[bold red]❌ 错误: 未设置 ANTHROPIC_API_KEY[/bold red]")
        console.print("[yellow]请通过以下方式之一设置 API Key:[/yellow]")
        console.print("[yellow]1. 在 .env 文件中设置: ANTHROPIC_API_KEY=your_key[/yellow]")
        console.print("[yellow]2. 使用命令行参数: --api-key your_key[/yellow]")
        console.print("[yellow]3. 设置环境变量: export ANTHROPIC_API_KEY=your_key[/yellow]")
        sys.exit(1)

    # 检查输入文件
    input_path = Path(args.input)
    if not input_path.exists():
        console.print(f"[bold red]❌ 错误: 输入文件不存在: {input_path}[/bold red]")
        sys.exit(1)

    if not input_path.is_file():
        console.print(f"[bold red]❌ 错误: 输入路径不是文件: {input_path}[/bold red]")
        sys.exit(1)

    # 显示配置信息
    console.print("[bold]配置信息:[/bold]")
    console.print(f"  输入文件: {input_path.absolute()}")
    console.print(f"  输出目录: {args.output}")
    console.print(f"  最大卡片数: {args.max_cards}")
    console.print(f"  AI 模型: {args.model}\n")

    try:
        # 创建 Agent
        agent = TrainingKnowledgeCardAgent(
            api_key=args.api_key,
            model=args.model,
            output_dir=args.output,
            max_cards=args.max_cards
        )

        # 处理培训逐字稿
        result = agent.process(str(input_path))

        # 返回结果
        if result.success:
            sys.exit(0)
        else:
            sys.exit(1)

    except KeyboardInterrupt:
        console.print("\n[yellow]⚠️ 用户中断操作[/yellow]")
        sys.exit(130)
    except Exception as e:
        console.print(f"\n[bold red]❌ 发生错误: {str(e)}[/bold red]")
        import traceback
        console.print(f"[dim]{traceback.format_exc()}[/dim]")
        sys.exit(1)


if __name__ == "__main__":
    main()
