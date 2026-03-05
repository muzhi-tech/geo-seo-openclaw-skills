#!/usr/bin/env python3
"""
GEO Content Optimizer - 独立站GEO优化核心脚本
基于 claude-skill-seo-geo-optimizer 和 SheepGeo 框架

功能:
1. 内容分析 - 提取关键词、实体、结构
2. GEO优化 - 添加统计数据、引用、FAQ
3. 国际市场适配 - 英文优化策略
4. Schema生成 - JSON-LD结构化数据
"""

import re
import json
import sys
from html.parser import HTMLParser
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass, field
from enum import Enum

class Market(Enum):
    GLOBAL = "global"  # 国际市场

class Platform(Enum):
    # 国际平台
    CHATGPT = "chatgpt"
    PERPLEXITY = "perplexity"
    CLAUDE = "claude"
    GEMINI = "gemini"
    GOOGLE_AI_OVERVIEW = "google_ai_overview"

@dataclass
class GEOScores:
    """GEO评分"""
    semantic_coverage: int = 0      # 语义覆盖 (S)
    human_credibility: int = 0      # 人类可信度 (H)
    evidence_structuring: int = 0   # 证据结构化 (E1)
    ecosystem_integration: int = 0  # 生态集成 (E2)
    performance_monitoring: int = 0 # 性能监测 (P)

    @property
    def gem_score(self) -> float:
        """计算GEM综合评分"""
        return (
            self.semantic_coverage * 0.25 +
            self.human_credibility * 0.25 +
            self.evidence_structuring * 0.20 +
            self.ecosystem_integration * 0.15 +
            self.performance_monitoring * 0.15
        )

@dataclass
class ContentAnalysis:
    """内容分析结果"""
    title: str = ""
    description: str = ""
    h1: List[str] = field(default_factory=list)
    h2: List[str] = field(default_factory=list)
    h3: List[str] = field(default_factory=list)
    paragraphs: List[str] = field(default_factory=list)
    keywords: Dict[str, List[str]] = field(default_factory=dict)
    entities: Dict[str, List[str]] = field(default_factory=dict)
    statistics: List[Dict] = field(default_factory=list)
    citations: List[str] = field(default_factory=list)
    geo_scores: GEOScores = field(default_factory=GEOScores)

class ContentParser(HTMLParser):
    """HTML内容解析器"""

    def __init__(self):
        super().__init__()
        self.analysis = ContentAnalysis()
        self.in_body = False
        self.current_tag = None
        self.current_text = ''
        self.in_script = False
        self.in_style = False

    def handle_starttag(self, tag, attrs):
        attrs_dict = dict(attrs)

        if tag == 'body':
            self.in_body = True
        elif tag in ('script', 'style'):
            if tag == 'script':
                self.in_script = True
            else:
                self.in_style = True
        elif tag == 'meta':
            if attrs_dict.get('name') == 'description':
                self.analysis.description = attrs_dict.get('content', '')
            elif attrs_dict.get('property') == 'og:description':
                if not self.analysis.description:
                    self.analysis.description = attrs_dict.get('content', '')

        if self.in_body and not self.in_script and not self.in_style:
            self.current_tag = tag

    def handle_endtag(self, tag):
        if tag == 'body':
            self.in_body = False
        elif tag == 'script':
            self.in_script = False
        elif tag == 'style':
            self.in_style = False

        if self.current_tag and self.current_text.strip():
            text = ' '.join(self.current_text.split())  # 清理空白

            if tag == 'title':
                self.analysis.title = text
            elif tag == 'h1':
                self.analysis.h1.append(text)
            elif tag == 'h2':
                self.analysis.h2.append(text)
            elif tag == 'h3':
                self.analysis.h3.append(text)
            elif tag == 'p':
                self.analysis.paragraphs.append(text)

        self.current_text = ''
        self.current_tag = None

    def handle_data(self, data):
        if self.current_tag and not self.in_script and not self.in_style:
            self.current_text += data

def count_words(text: str) -> int:
    """统计词数（支持中英文）"""
    # 英文单词
    english_words = len(re.findall(r'\b[a-zA-Z]+\b', text))
    # 中文字符
    chinese_chars = len(re.findall(r'[\u4e00-\u9fff]', text))
    return english_words + chinese_chars

def extract_keywords(text: str) -> Dict[str, List[str]]:
    """提取5类关键词"""
    keywords = {
        'primary': [],      # 主要关键词
        'semantic': [],     # 语义相关词
        'long_tail': [],    # 长尾关键词
        'questions': [],    # 问题关键词
        'brand': []         # 品牌关键词
    }

    # 问题关键词 (Who/What/Where/When/Why/How)
    question_pattern = r'(?:what|who|where|when|why|how|什么是|如何|为什么|哪里|谁|什么时候)[^\?]*\?'
    keywords['questions'] = re.findall(question_pattern, text, re.IGNORECASE)

    # 长尾关键词 (3-8词)
    sentences = re.split(r'[.!?。！？]', text)
    for sentence in sentences:
        words = count_words(sentence)
        if 3 <= words <= 8:
            keywords['long_tail'].append(sentence.strip())

    return keywords

def extract_entities(text: str) -> Dict[str, List[str]]:
    """提取实体"""
    entities = {
        'persons': [],
        'organizations': [],
        'locations': [],
        'products': [],
        'dates': []
    }

    # 日期
    date_patterns = [
        r'\d{4}[-/年]\d{1,2}[-/月]\d{1,2}[日]?',
        r'\d{1,2}[-/]\d{1,2}[-/]\d{4}',
        r'(?:January|February|March|April|May|June|July|August|September|October|November|December)\s+\d{1,2},?\s+\d{4}'
    ]
    for pattern in date_patterns:
        entities['dates'].extend(re.findall(pattern, text, re.IGNORECASE))

    return entities

def extract_statistics(text: str) -> List[Dict]:
    """提取统计数据"""
    statistics = []

    patterns = [
        # 百分比
        r'(\d+(?:\.\d+)?)\s*(?:%|percent|百分比|百分之)',
        # 金额
        r'(\$|¥|€|£)\s*(\d+(?:,\d{3})*(?:\.\d+)?(?:[MBKmbk])?)',
        # 数量
        r'(\d+(?:,\d{3})*(?:\.\d+)?)\s*(?:million|billion|trillion|万|亿|百万|十亿)',
        # 增长
        r'(?:increase|growth|增长|提升|提高)\s*(?:of\s*)?(\d+(?:\.\d+)?%?)',
        # 年份
        r'(?:in|since|自|从)\s*(\d{4})',
    ]

    for pattern in patterns:
        matches = re.finditer(pattern, text, re.IGNORECASE)
        for match in matches:
            context_start = max(0, match.start() - 50)
            context_end = min(len(text), match.end() + 50)
            statistics.append({
                'value': match.group(0),
                'context': text[context_start:context_end].strip()
            })

    return statistics

def calculate_geo_scores(analysis: ContentAnalysis) -> GEOScores:
    """计算GEO评分 (SHEEP框架)"""

    scores = GEOScores()

    # S - 语义覆盖 (25%)
    # 评估: 关键词数量、内容结构、H标签使用
    keyword_count = sum(len(v) for v in analysis.keywords.values())
    scores.semantic_coverage = min(100, keyword_count * 5 + len(analysis.h2) * 10)

    # H - 人类可信度 (25%)
    # 评估: 引用、作者信息、来源
    has_citations = len(analysis.citations) > 0
    has_stats = len(analysis.statistics) > 0
    scores.human_credibility = 50 + (20 if has_citations else 0) + (20 if has_stats else 0)

    # E1 - 证据结构化 (20%)
    # 评估: 表格、列表、Schema
    scores.evidence_structuring = min(100, len(analysis.statistics) * 10 + len(analysis.h3) * 5)

    # E2 - 生态集成 (15%)
    # 评估: 社交信号、外部链接
    scores.ecosystem_integration = 60  # 基础分

    # P - 性能监测 (15%)
    # 评估: 内容新鲜度、更新频率
    scores.performance_monitoring = 70  # 基础分

    return scores

def optimize_for_platform(content: str, platform: Platform) -> str:
    """针对特定平台优化内容"""

    optimizations = []

    if platform == Platform.CHATGPT:
        # ChatGPT: 权威性+凭证
        optimizations.append("添加作者凭证和专业背景")
        optimizations.append("确保1500-2500词深度覆盖")
        optimizations.append("添加主要来源引用(PubMed, arXiv)")

    elif platform == Platform.PERPLEXITY:
        # Perplexity: 新鲜度+引用
        optimizations.append("确保内容30天内更新")
        optimizations.append("添加内联引用 [1], [2] 格式")
        optimizations.append("使用H2→H3→项目符号结构")

    elif platform == Platform.CLAUDE:
        # Claude: 准确性+来源
        optimizations.append("仅使用主要来源")
        optimizations.append("5-8个引用，包含出版商和年份")
        optimizations.append("透明方法论")
        optimizations.append("承认局限性")

    return "\n".join(f"- {opt}" for opt in optimizations)

def generate_faq_schema(questions: List[Dict[str, str]]) -> str:
    """生成FAQ Schema"""
    schema = {
        "@context": "https://schema.org",
        "@type": "FAQPage",
        "mainEntity": []
    }

    for q in questions:
        schema["mainEntity"].append({
            "@type": "Question",
            "name": q.get("question", ""),
            "acceptedAnswer": {
                "@type": "Answer",
                "text": q.get("answer", "")
            }
        })

    return json.dumps(schema, ensure_ascii=False, indent=2)

def generate_article_schema(title: str, author: str = "", date: str = "") -> str:
    """生成Article Schema"""
    schema = {
        "@context": "https://schema.org",
        "@type": "Article",
        "headline": title,
        "author": {
            "@type": "Person",
            "name": author
        },
        "datePublished": date,
        "dateModified": date
    }

    return json.dumps(schema, ensure_ascii=False, indent=2)

def analyze_content(html_content: str) -> ContentAnalysis:
    """分析HTML内容"""

    parser = ContentParser()
    parser.feed(html_content)

    analysis = parser.analysis

    # 提取所有文本
    all_text = ' '.join(analysis.paragraphs)

    # 关键词提取
    analysis.keywords = extract_keywords(all_text)

    # 实体提取
    analysis.entities = extract_entities(all_text)

    # 统计数据提取
    analysis.statistics = extract_statistics(all_text)

    # 计算GEO评分
    analysis.geo_scores = calculate_geo_scores(analysis)

    return analysis

def generate_report(analysis: ContentAnalysis, output_format: str = "markdown") -> str:
    """生成分析报告"""

    if output_format == "json":
        return json.dumps({
            'title': analysis.title,
            'description': analysis.description,
            'h1': analysis.h1,
            'h2': analysis.h2,
            'h3': analysis.h3,
            'keywords': analysis.keywords,
            'statistics_count': len(analysis.statistics),
            'geo_scores': {
                'semantic_coverage': analysis.geo_scores.semantic_coverage,
                'human_credibility': analysis.geo_scores.human_credibility,
                'evidence_structuring': analysis.geo_scores.evidence_structuring,
                'ecosystem_integration': analysis.geo_scores.ecosystem_integration,
                'performance_monitoring': analysis.geo_scores.performance_monitoring,
                'gem_score': round(analysis.geo_scores.gem_score, 2)
            }
        }, ensure_ascii=False, indent=2)

    # Markdown格式
    report = f"""# GEO内容分析报告

## 基本信息

| 项目 | 内容 |
|------|------|
| 标题 | {analysis.title} |
| 描述 | {analysis.description[:100]}... |
| H1数量 | {len(analysis.h1)} |
| H2数量 | {len(analysis.h2)} |
| H3数量 | {len(analysis.h3)} |
| 段落数 | {len(analysis.paragraphs)} |

## GEO评分 (SHEEP框架)

| 维度 | 分数 | 权重 | 加权分 |
|------|------|------|--------|
| S - 语义覆盖 | {analysis.geo_scores.semantic_coverage} | 25% | {analysis.geo_scores.semantic_coverage * 0.25:.1f} |
| H - 人类可信度 | {analysis.geo_scores.human_credibility} | 25% | {analysis.geo_scores.human_credibility * 0.25:.1f} |
| E1 - 证据结构化 | {analysis.geo_scores.evidence_structuring} | 20% | {analysis.geo_scores.evidence_structuring * 0.20:.1f} |
| E2 - 生态集成 | {analysis.geo_scores.ecosystem_integration} | 15% | {analysis.geo_scores.ecosystem_integration * 0.15:.1f} |
| P - 性能监测 | {analysis.geo_scores.performance_monitoring} | 15% | {analysis.geo_scores.performance_monitoring * 0.15:.1f} |
| **GEM总分** | - | - | **{analysis.geo_scores.gem_score:.1f}** |

## 提取的统计数据 ({len(analysis.statistics)}个)

"""
    for i, stat in enumerate(analysis.statistics[:10], 1):
        report += f"{i}. {stat['value']}\n"

    report += """
## 平台优化建议

### 国际平台

"""
    report += f"**ChatGPT**:\n{optimize_for_platform('', Platform.CHATGPT)}\n\n"
    report += f"**Perplexity**:\n{optimize_for_platform('', Platform.PERPLEXITY)}\n\n"
    report += f"**Claude**:\n{optimize_for_platform('', Platform.CLAUDE)}\n\n"

    return report

def main():
    """主函数"""
    if len(sys.argv) < 2:
        print("用法: python geo_optimizer.py <html_file> [--format json|markdown]")
        print("\nGEO内容优化分析工具")
        print("基于 SheepGeo SHEEP框架 + claude-skill-seo-geo-optimizer")
        sys.exit(1)

    file_path = sys.argv[1]
    output_format = "markdown"

    if "--format" in sys.argv:
        idx = sys.argv.index("--format")
        if idx + 1 < len(sys.argv):
            output_format = sys.argv[idx + 1]

    # 读取文件
    with open(file_path, 'r', encoding='utf-8') as f:
        html_content = f.read()

    # 分析内容
    print(f"正在分析: {file_path}")
    analysis = analyze_content(html_content)

    # 生成报告
    report = generate_report(analysis, output_format)

    # 输出
    if output_format == "json":
        print(report)
    else:
        # 保存到文件
        output_file = file_path.rsplit('.', 1)[0] + '_geo_report.md'
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(report)
        print(f"报告已保存: {output_file}")
        print(f"\nGEM评分: {analysis.geo_scores.gem_score:.1f}/100")

if __name__ == '__main__':
    main()
