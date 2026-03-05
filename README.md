# OpenClaw Skills & Commands for SEO & GEO

> 专业的搜索引擎优化 (SEO) 和生成式引擎优化 (GEO) 技能库

---

## 简介

本项目提供一套完整的 Claude Code Skills 和 Commands，专注于：

- **SEO (Search Engine Optimization)** - 传统搜索引擎优化
- **GEO (Generative Engine Optimization)** - AI 生成引擎优化（ChatGPT、Perplexity、Gemini 等）

---

## 目录结构

```
geo-seo-openclaw-skills/
├── skills/              # SEO/GEO 技能模块
│   └── geo-site-audit/  # GEO 全站审计技能
├── commands/            # 快捷命令
├── config/              # 配置文件
│   └── platforms.json   # 平台优化配置
├── scripts/             # Python 脚本
│   └── geo_optimizer.py # GEO 优化核心脚本
├── templates/           # 模板文件
└── output/              # 输出报告
```

---

## 技能列表

### GEO 技能

| 技能 | 描述 | 状态 |
|------|------|------|
| geo-site-audit | 独立站GEO全站审计 - SHEEP框架评分、平台优化建议、Schema生成 | ✅ 可用 |

### 计划中的技能

| 技能 | 描述 | 状态 |
|------|------|------|
| keyword-research | 关键词研究与竞争分析 | 🚧 开发中 |
| content-optimization | 内容优化与 EEAT 提升 | 🚧 开发中 |
| technical-seo | 技术 SEO 审计 | 🚧 开发中 |
| entity-optimization | 实体与知识图谱优化 | 🚧 开发中 |

---

## 快速开始

### 1. 使用 GEO 审计技能

```bash
# 审计网站 GEO
/geo-site-audit https://your-site.com
```

### 2. 使用 Python 脚本

```bash
# 分析 HTML 文件
python scripts/geo_optimizer.py page.html

# JSON 格式输出
python scripts/geo_optimizer.py page.html --format json
```

### 3. 生成 llms.txt

```bash
# 安装 llmstxt
npm install -g llmstxt

# 从 sitemap 生成
llmstxt gen https://your-site.com/sitemap.xml > public/llms.txt

# 完整版
llmstxt gen-full https://your-site.com/sitemap.xml > public/llms-full.txt
```

---

## GEO 评分框架 (SHEEP)

基于 [SheepGeo](https://github.com/CN-Sheep/SheepGeo) 框架的 5 维度评分：

| 维度 | 评分标准 | 权重 |
|------|---------|------|
| **S** - 语义覆盖 | 关键词数量、内容深度、主题覆盖 | 25% |
| **H** - 人类可信度 | 作者凭证、引用来源、E-E-A-T信号 | 25% |
| **E1** - 证据结构化 | Schema标记、表格数据、FAQ | 20% |
| **E2** - 生态集成 | 社交信号、外部引用、品牌一致性 | 15% |
| **P** - 性能监测 | 内容新鲜度、更新频率、技术性能 | 15% |

---

## 平台优化策略

### 国际平台

| 平台 | 优化重点 | 预期提升 |
|------|---------|---------|
| ChatGPT | 权威性 + 凭证 | +40% 引用概率 |
| Perplexity | 新鲜度 + 内联引用 | 3.2x 引用率 |
| Claude | 准确性 + 主要来源 | 91.2% 归属准确率 |
| Google AI Overview | 结构化数据 + 直接回答 | 13% 查询覆盖 |
| Gemini | 社区 + 本地信号 | Google 生态集成 |

### 优化技巧

| 技巧 | 影响 | 描述 |
|------|------|------|
| 统计数据添加 | +41% | 添加精确统计数据 |
| 专家引用 | +28% | 添加专家引用 |
| 内容新鲜度 | 3.2x | 内容 < 30 天 |
| 作者凭证 | +40% | 添加作者凭证 |
| H2→H3→项目符号 | +40% | 结构化内容 |

---

## MCP 集成

```json
// .mcp.json
{
  "mcpServers": {
    "ahrefs": {
      "command": "npx",
      "args": ["-y", "@anthropic-ai/mcp-server-ahrefs"],
      "env": {
        "AHREFS_API_KEY": "your-key"
      }
    }
  }
}
```

---

## 参考资源

- [seo-geo-claude-skills](https://github.com/aaron-he-zhu/seo-geo-claude-skills)
- [claude-skill-seo-geo-optimizer](https://github.com/199-biotechnologies/claude-skill-seo-geo-optimizer)
- [SheepGeo](https://github.com/CN-Sheep/SheepGeo)
- [llmstxt](https://github.com/dotenvx/llmstxt)
- [awesome-generative-engine-optimization](https://github.com/amplifying-ai/awesome-generative-engine-optimization)

---

## 贡献指南

欢迎贡献新的 SEO/GEO 技能！

---

## 许可证

MIT License
