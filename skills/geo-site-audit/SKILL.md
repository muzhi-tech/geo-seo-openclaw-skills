---
name: geo-site-audit
version: "1.0.0"
description: |
  独立站GEO全站审计技能。输入网站URL或域名，自动执行完整的GEO分析流程：内容质量评估、AI可见性检测、平台优化建议、Schema生成、llms.txt创建。适用于希望提升AI平台引用率的独立站。
license: MIT
compatibility: "Claude Code ≥1.0"
metadata:
  author: custom
  version: "1.0.0"
  geo-relevance: "high"
  tags:
    - geo
    - ai-citations
    - site-audit
    - independent-site
    - dual-market
  triggers:
    - "GEO审计"
    - "AI可见性分析"
    - "独立站GEO"
    - "全站GEO优化"
---

# GEO Site Audit - 独立站GEO审计

## 触发条件

当用户提到以下内容时使用此技能：
- "审计我的网站GEO"
- "分析独立站AI可见性"
- "全站GEO优化"
- "网站GEO评分"

## 执行流程

### Step 1: 内容抓取与分析

```
1. 获取网站sitemap.xml
2. 识别主要页面（首页、产品页、博客、关于页）
3. 提取每个页面的：
   - 标题和描述
   - H1/H2/H3结构
   - 关键词密度
   - 统计数据
   - 引用和来源
```

### Step 2: GEO评分 (SHEEP框架)

| 维度 | 评分标准 | 权重 |
|------|---------|------|
| **S** - 语义覆盖 | 关键词数量、内容深度、主题覆盖 | 25% |
| **H** - 人类可信度 | 作者凭证、引用来源、E-E-A-T信号 | 25% |
| **E1** - 证据结构化 | Schema标记、表格数据、FAQ | 20% |
| **E2** - 生态集成 | 社交信号、外部引用、品牌一致性 | 15% |
| **P** - 性能监测 | 内容新鲜度、更新频率、技术性能 | 15% |

### Step 3: 双市场优化建议

#### 国际平台优化

**ChatGPT**:
- [ ] 添加作者凭证和专业背景
- [ ] 确保1500-2500词深度内容
- [ ] 添加PubMed/arXiv等主要来源

**Perplexity**:
- [ ] 30天内更新内容
- [ ] 添加[1][2]格式内联引用
- [ ] 使用H2→H3→项目符号结构

**Claude**:
- [ ] 仅使用主要来源
- [ ] 5-8个引用含出版商和年份
- [ ] 添加方法论说明

**Google AI Overview**:
- [ ] 前150字直接回答
- [ ] 添加FAQ Schema
- [ ] 数据表格化

#### 中国平台优化

| 平台 | 重点 | 权重 |
|------|------|------|
| 通义千问 | 商业应用场景 | 15% |
| 豆包 | 中文自然理解 | 14% |
| 文心一言 | 搜索+知识图谱 | 13% |
| GLM-4 | 学术严谨性 | 12% |
| DeepSeek | 技术深度 | 10% |

### Step 4: 输出报告

```markdown
# GEO全站审计报告

## 概览
- 网站: [domain]
- 审计页面数: [N]
- GEM平均分: [X]/100
- 评级: [A+/A/B+/B/C]

## 页面分析

| 页面 | GEM分 | S | H | E1 | E2 | P | 优先级 |
|------|-------|---|---|----|----|---|--------|
| 首页 | 75 | 80 | 70 | 75 | 65 | 80 | 中 |
| 产品页 | 62 | 65 | 60 | 70 | 55 | 60 | 高 |
| 博客 | 85 | 90 | 85 | 80 | 75 | 90 | 低 |

## 优化建议

### 高优先级
1. [具体建议1]
2. [具体建议2]

### 中优先级
1. [具体建议1]
2. [具体建议2]

## 生成的资产

- [ ] FAQ Schema (JSON-LD)
- [ ] Article Schema (JSON-LD)
- [ ] llms.txt
- [ ] llms-full.txt

## 平台可见性预测

| 平台 | 当前 | 优化后 |
|------|------|--------|
| ChatGPT | 低 | 中 |
| Perplexity | 中 | 高 |
| 通义千问 | 低 | 中 |
```

### Step 5: 生成Schema和llms.txt

**生成命令**:
```bash
# llms.txt
llmstxt gen https://your-site.com/sitemap.xml > public/llms.txt

# llms-full.txt (完整内容)
llmstxt gen-full https://your-site.com/sitemap.xml > public/llms-full.txt
```

**Schema模板**:
```json
{
  "@context": "https://schema.org",
  "@type": "Organization",
  "name": "[品牌名]",
  "url": "[网站URL]",
  "logo": "[Logo URL]",
  "sameAs": [
    "[社交媒体链接]"
  ]
}
```

## 工具连接

此技能可连接以下MCP服务增强功能：
- `~~SEO tool`: Ahrefs/SEMrush数据
- `~~AI monitor`: Profound/AthenaHQ可见性追踪
- `~~Analytics`: GA4 AI推荐流量

## 示例用法

```
用户: 帮我审计 https://mysite.com 的GEO
Claude: 正在执行GEO全站审计...

1. 获取sitemap...
2. 分析5个主要页面...
3. 计算GEM评分...
4. 生成优化建议...

[GEM评分: 68/100 - B级]

主要问题:
- 缺少作者凭证 (H维度 -15分)
- 无FAQ Schema (E1维度 -10分)
- 内容超过90天未更新 (P维度 -8分)

建议优先处理:
1. 添加作者简介和凭证
2. 为产品页添加FAQ Schema
3. 更新博客内容
```

## 相关技能

- `geo-content-optimizer` - 内容级别GEO优化
- `schema-markup-generator` - Schema生成
- `entity-optimizer` - 实体优化
