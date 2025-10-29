# 项目架构设计

## 整体架构

```
training-knowledge-cards/
├── src/                          # 源代码目录
│   ├── __init__.py              # 包初始化
│   ├── models.py                # 数据模型定义
│   ├── agent.py                 # 主控制器
│   ├── knowledge_extractor.py   # 知识提取模块
│   ├── card_generator.py        # 卡片生成模块
│   └── overview_generator.py    # 总图生成模块
├── examples/                     # 示例文件
├── output/                       # 输出目录
├── docs/                         # 文档
├── main.py                       # 命令行入口
├── requirements.txt              # 依赖管理
├── .env.example                  # 环境变量模板
└── README.md                     # 项目说明
```

## 核心模块

### 1. 数据模型 (models.py)

定义了系统中使用的核心数据结构：

- **KnowledgePoint**: 单个知识点
  - title: 标题
  - description: 描述
  - importance: 重要性等级 (1-5)
  - category: 分类

- **KnowledgeCard**: 知识卡片
  - title: 卡片标题
  - subtitle: 副标题
  - key_points: 核心要点列表
  - detailed_content: 详细内容
  - examples: 示例列表
  - tips: 提示和建议
  - related_topics: 相关主题

- **TrainingOverview**: 培训总览
  - title: 培训主题
  - summary: 培训摘要
  - main_categories: 主要分类
  - knowledge_points: 核心知识点列表
  - total_cards: 卡片总数

- **ProcessingResult**: 处理结果
  - overview: 培训总览
  - cards: 知识卡片列表
  - success: 是否成功
  - message: 消息

### 2. 知识提取器 (knowledge_extractor.py)

**职责**: 从培训逐字稿中智能提取核心知识点

**核心方法**:
- `extract_overview()`: 提取培训总览信息
- `extract_knowledge_points()`: 提取指定数量的核心知识点

**工作流程**:
1. 接收培训逐字稿文本
2. 使用 Claude API 进行深度分析
3. 识别主题、分类和核心知识点
4. 按重要性排序知识点
5. 返回结构化的总览信息

**Prompt 设计**:
- 明确要求 JSON 格式输出
- 指定知识点的结构（标题、描述、重要性、分类）
- 要求识别 8-15 个最核心的知识点

### 3. 卡片生成器 (card_generator.py)

**职责**: 为每个知识点生成详细的知识卡片

**核心方法**:
- `generate_card()`: 为单个知识点生成卡片
- `generate_cards_batch()`: 批量生成卡片

**工作流程**:
1. 接收知识点和原始逐字稿
2. 使用 Claude API 深度挖掘该知识点
3. 从逐字稿中提取相关细节和示例
4. 生成结构化的卡片内容
5. 返回完整的知识卡片

**卡片结构**:
- 核心要点 (3-5 个)
- 详细说明 (150-300 字)
- 实际示例 (2-3 个)
- 提示建议 (2-3 条)
- 相关主题

### 4. 总图生成器 (overview_generator.py)

**职责**: 生成知识总览和思维导图

**核心方法**:
- `generate_mermaid_mindmap()`: 生成 Mermaid 思维导图
- `generate_overview_markdown()`: 生成总览文档
- `generate_card_markdown()`: 生成单张卡片文档

**思维导图设计**:
```
根节点（培训主题）
├── 分类1
│   ├── 知识点1 ⭐⭐⭐⭐⭐
│   └── 知识点2 ⭐⭐⭐⭐
├── 分类2
│   ├── 知识点3 ⭐⭐⭐⭐
│   └── 知识点4 ⭐⭐⭐
└── 分类3
    └── 知识点5 ⭐⭐⭐⭐⭐
```

**总览文档包含**:
1. 培训摘要
2. 思维导图
3. 主要分类
4. 核心知识点列表（按分类组织）
5. 卡片索引（带链接）
6. 使用说明

### 5. 主控制器 (agent.py)

**职责**: 协调各个模块，完成完整的处理流程

**核心方法**:
- `__init__()`: 初始化 Agent 和各个模块
- `load_transcript()`: 加载培训逐字稿
- `process()`: 执行完整的处理流程

**处理流程**:
1. 加载培训逐字稿
2. 提取知识总览（调用 KnowledgeExtractor）
3. 批量生成知识卡片（调用 CardGenerator）
4. 生成总览文档（调用 OverviewGenerator）
5. 保存所有生成的文档
6. 显示进度和结果

**UI 特性**:
- 使用 Rich 库提供美观的命令行界面
- 实时显示处理进度
- 彩色输出和进度条
- 清晰的错误提示

## 技术选型

### 1. Python
- 成熟的 AI 生态系统
- 丰富的第三方库
- 简洁易读的语法

### 2. Anthropic Claude API
- 强大的内容理解能力
- 出色的中文支持
- 结构化输出能力
- 长文本处理能力

### 3. Pydantic
- 数据验证和序列化
- 类型安全
- IDE 友好

### 4. Rich
- 美观的命令行界面
- 进度条和状态显示
- 彩色输出

### 5. Mermaid
- 简洁的图表语法
- 广泛的平台支持
- 易于渲染和分享

## 设计原则

### 1. 模块化
每个模块职责单一，低耦合高内聚

### 2. 可扩展性
- 易于添加新的输出格式
- 易于支持新的 AI 模型
- 易于添加新的功能

### 3. 用户友好
- 清晰的命令行界面
- 详细的进度反馈
- 有用的错误提示

### 4. 数据驱动
- 使用结构化数据模型
- JSON 格式交互
- 类型安全

## 扩展方向

### 1. 输出格式
- [ ] PDF 导出
- [ ] HTML 网页
- [ ] PowerPoint 演示文稿
- [ ] 思维导图软件格式 (XMind, MindNode)

### 2. 输入格式
- [ ] Word 文档 (.docx)
- [ ] PDF 文档
- [ ] 音频转录（集成语音识别）
- [ ] 视频字幕

### 3. AI 功能增强
- [ ] 自动生成练习题
- [ ] 生成培训总结报告
- [ ] 知识点关联分析
- [ ] 个性化学习路径推荐

### 4. 协作功能
- [ ] Web 界面
- [ ] 多人协作编辑
- [ ] 版本管理
- [ ] 分享和发布

### 5. 数据分析
- [ ] 知识点热度分析
- [ ] 学习效果追踪
- [ ] 培训质量评估
