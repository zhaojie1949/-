# 培训知识卡片生成器 (Training Knowledge Card Generator)

一个基于 AI 的智能工具，能够将培训逐字稿自动转化为结构化的知识卡片，帮助提炼核心内容并生成易于理解和传播的学习资料。

## 功能特点

- 📝 **智能内容分析**：使用 Claude AI 深度理解培训内容
- 🗺️ **总图生成**：自动创建知识点总览思维导图
- 🎴 **知识卡片**：生成多张清晰的结构化知识卡片
- 📊 **Markdown 输出**：易于编辑和分享的格式
- 🎨 **Mermaid 图表**：美观的可视化图表支持

## 快速开始

### 1. 安装依赖

```bash
pip install -r requirements.txt
```

### 2. 配置 API Key

复制 `.env.example` 为 `.env` 并填入你的 Claude API Key：

```bash
cp .env.example .env
```

编辑 `.env` 文件：
```
ANTHROPIC_API_KEY=your_api_key_here
```

### 3. 运行

```bash
python main.py --input your_training_transcript.txt
```

## 使用方法

### 基本用法

```bash
# 处理单个培训逐字稿
python main.py --input training.txt

# 指定输出目录
python main.py --input training.txt --output ./my_cards

# 指定生成的卡片数量
python main.py --input training.txt --max-cards 10
```

### 输入格式

支持以下格式的培训逐字稿：
- 纯文本文件 (.txt)
- Markdown 文件 (.md)
- Word 文档 (.docx) - 计划支持

## 输出结构

```
output/
├── overview.md          # 总图和核心内容概览
├── cards/
│   ├── card_01.md      # 知识卡片 1
│   ├── card_02.md      # 知识卡片 2
│   └── ...
└── summary.json        # 结构化数据（可选）
```

## 示例

查看 `examples/` 目录中的示例培训逐字稿和生成的知识卡片。

## 技术栈

- **Python 3.8+**
- **Anthropic Claude API** - AI 内容分析
- **Mermaid** - 思维导图生成
- **Rich** - 命令行美化

## 贡献

欢迎提交 Issue 和 Pull Request！

## License

MIT License
