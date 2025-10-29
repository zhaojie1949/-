# 使用指南

## 目录
1. [快速开始](#快速开始)
2. [详细使用](#详细使用)
3. [配置选项](#配置选项)
4. [最佳实践](#最佳实践)
5. [常见问题](#常见问题)
6. [示例演示](#示例演示)

## 快速开始

### 1. 环境准备

确保已安装 Python 3.8 或更高版本：
```bash
python --version
```

### 2. 安装依赖

```bash
pip install -r requirements.txt
```

### 3. 配置 API Key

复制环境变量模板：
```bash
cp .env.example .env
```

编辑 `.env` 文件，填入你的 Anthropic API Key：
```bash
ANTHROPIC_API_KEY=sk-ant-xxxxx
```

获取 API Key：访问 https://console.anthropic.com/settings/keys

### 4. 运行示例

```bash
python main.py --input examples/sample_training.txt
```

### 5. 查看结果

```bash
ls output/
# overview.md  cards/

cat output/overview.md
```

## 详细使用

### 命令行参数

```bash
python main.py [选项]
```

**必需参数**:
- `-i, --input <file>`: 培训逐字稿文件路径

**可选参数**:
- `-o, --output <dir>`: 输出目录（默认: ./output）
- `-m, --max-cards <num>`: 最大卡片数量（默认: 8）
- `--model <model>`: Claude 模型（默认: claude-3-5-sonnet-20241022）
- `--api-key <key>`: API Key（也可通过环境变量设置）

### 使用示例

#### 基本使用
```bash
python main.py --input my_training.txt
```

#### 指定输出目录
```bash
python main.py --input my_training.txt --output ./my_cards
```

#### 生成更多卡片
```bash
python main.py --input my_training.txt --max-cards 15
```

#### 使用不同模型
```bash
python main.py --input my_training.txt --model claude-3-opus-20240229
```

#### 通过命令行指定 API Key
```bash
python main.py --input my_training.txt --api-key sk-ant-xxxxx
```

## 配置选项

### 环境变量配置

在 `.env` 文件中配置：

```bash
# Anthropic API Key（必需）
ANTHROPIC_API_KEY=your_api_key_here

# Claude 模型（可选）
CLAUDE_MODEL=claude-3-5-sonnet-20241022

# 输出目录（可选）
OUTPUT_DIR=./output

# 最大卡片数量（可选）
MAX_CARDS=8
```

### 模型选择

支持的 Claude 模型：
- `claude-3-5-sonnet-20241022` (推荐) - 平衡性能和成本
- `claude-3-opus-20240229` - 最高质量，成本较高
- `claude-3-haiku-20240307` - 最快速度，成本最低

### 输出结构

```
output/
├── overview.md              # 总览文档
│   ├── 培训摘要
│   ├── 思维导图 (Mermaid)
│   ├── 主要分类
│   ├── 核心知识点列表
│   └── 卡片索引
└── cards/                   # 卡片目录
    ├── card_01.md          # 卡片 1
    ├── card_02.md          # 卡片 2
    ├── ...
    └── card_XX.md          # 卡片 X
```

### 卡片内容结构

每张知识卡片包含：
1. **标题**: 知识点主题
2. **副标题**: 一句话概括
3. **核心要点**: 3-5 个关键要点
4. **详细说明**: 深入解释
5. **实际示例**: 2-3 个具体案例
6. **提示建议**: 实用建议和注意事项
7. **相关主题**: 关联知识点

## 最佳实践

### 1. 准备培训逐字稿

**理想的逐字稿特征**:
- **长度**: 2000-10000 字（太短提取不出足够信息，太长可能超限）
- **结构**: 有清晰的主题和逻辑流程
- **内容**: 包含具体的概念、方法、示例
- **语言**: 清晰、专业、准确

**示例结构**:
```
培训标题

引言和背景

第一部分：核心概念
- 概念1的解释
- 概念2的解释
- 具体示例

第二部分：实践方法
- 方法1的步骤
- 方法2的应用
- 案例分析

第三部分：注意事项
- 常见误区
- 最佳实践
- 经验总结

总结
```

### 2. 调整卡片数量

根据培训内容长度和复杂度调整：
- **简短培训** (2000-3000字): 5-8 张卡片
- **中等培训** (3000-6000字): 8-12 张卡片
- **深入培训** (6000-10000字): 12-15 张卡片

### 3. 处理长文本

如果培训内容超过 10000 字，建议：
1. 分段处理：按主题分成多个文件
2. 分别生成：为每个部分生成卡片
3. 手动整合：将结果整合到一起

### 4. 优化输出质量

**技巧**:
1. **清晰的逐字稿**: 确保内容结构清晰、逻辑连贯
2. **包含示例**: 具体的案例能生成更好的卡片
3. **适当长度**: 每个主题有足够的阐述
4. **专业术语**: 使用标准的专业术语

### 5. 后期编辑

生成的卡片可能需要人工审核和调整：
1. 检查事实准确性
2. 补充缺失的示例
3. 调整语言表达
4. 优化结构布局

## 常见问题

### Q1: API Key 错误

**问题**: `❌ 错误: 未设置 ANTHROPIC_API_KEY`

**解决**:
1. 确认已创建 `.env` 文件
2. 检查 API Key 格式是否正确
3. 尝试使用命令行参数 `--api-key`

### Q2: 文件找不到

**问题**: `❌ 错误: 输入文件不存在`

**解决**:
1. 检查文件路径是否正确
2. 使用绝对路径或相对路径
3. 确认文件存在且有读取权限

### Q3: 生成的卡片质量不佳

**原因**:
- 逐字稿内容不够清晰
- 长度太短或太长
- 缺少具体示例

**解决**:
1. 优化逐字稿内容结构
2. 添加更多具体示例
3. 调整 `--max-cards` 参数
4. 尝试使用更高级的模型

### Q4: API 调用超时

**原因**: 网络问题或文本太长

**解决**:
1. 检查网络连接
2. 缩短培训逐字稿长度
3. 重试几次

### Q5: Markdown 渲染问题

**问题**: 思维导图无法显示

**解决**:
1. 使用支持 Mermaid 的查看器
2. 推荐工具: Typora, VS Code (with Mermaid plugin), GitHub
3. 在线预览: https://mermaid.live/

## 示例演示

### 示例 1: 处理产品培训

```bash
python main.py --input examples/sample_training.txt
```

**输入**: 产品经理敏捷开发培训逐字稿（约 3000 字）

**输出**: 8 张知识卡片，涵盖：
- 敏捷开发核心理念
- 用户故事 INVEST 原则
- Sprint 计划流程
- 每日站会实践
- 看板可视化管理
- Sprint 评审与回顾
- 技术债务管理
- 敏捷转型挑战

**查看结果**:
```bash
# 查看总览
cat output/overview.md

# 查看第一张卡片
cat output/cards/card_01.md

# 在 VS Code 中查看（支持 Mermaid 预览）
code output/overview.md
```

### 示例 2: 批量处理多个培训

创建批处理脚本 `batch_process.sh`:

```bash
#!/bin/bash

# 处理多个培训文件
for file in trainings/*.txt; do
    filename=$(basename "$file" .txt)
    python main.py --input "$file" --output "output/$filename"
    echo "已处理: $filename"
done

echo "全部完成！"
```

运行：
```bash
chmod +x batch_process.sh
./batch_process.sh
```

### 示例 3: 集成到工作流

使用 Python 脚本集成：

```python
from src.agent import TrainingKnowledgeCardAgent
import os

# 初始化 Agent
agent = TrainingKnowledgeCardAgent(
    api_key=os.getenv("ANTHROPIC_API_KEY"),
    output_dir="./my_output",
    max_cards=10
)

# 处理培训
result = agent.process("my_training.txt")

if result.success:
    print(f"成功生成 {len(result.cards)} 张卡片")
    print(f"培训主题: {result.overview.title}")
else:
    print(f"处理失败: {result.message}")
```

## 技巧和窍门

### 1. 快速预览

使用 `head` 快速查看生成的内容：
```bash
head -n 50 output/overview.md
```

### 2. 搜索特定内容

使用 `grep` 搜索卡片中的关键词：
```bash
grep -r "敏捷" output/cards/
```

### 3. 导出为单个文件

合并所有卡片：
```bash
cat output/overview.md output/cards/*.md > all_cards.md
```

### 4. 版本管理

使用 Git 管理生成的卡片：
```bash
git add output/
git commit -m "新增：产品管理培训卡片"
```

### 5. 分享和发布

- **GitHub**: 创建仓库，推送卡片
- **Notion**: 导入 Markdown 文件
- **博客**: 发布为系列文章
- **团队协作**: 使用 Confluence 或内部 Wiki

## 下一步

- 阅读 [架构设计文档](./ARCHITECTURE.md) 了解技术细节
- 查看 [示例目录](../examples/) 获取更多示例
- 贡献代码或反馈问题到项目仓库
