#!/usr/bin/env python3
"""扫描唐式中文成稿中的高风险模板形状，不自动改稿。"""

from __future__ import annotations

import argparse
import collections
import re
import statistics
import sys
from dataclasses import dataclass
from pathlib import Path


PIVOTS = (
    re.compile(r"(?:并)?不是[^。！？\n]{0,80}而是"),
    re.compile(r"并非[^。！？\n]{0,80}而是"),
    re.compile(r"与其说[^。！？\n]{0,80}不如说"),
    re.compile(r"不在于[^。！？\n]{0,80}而在于"),
    re.compile(r"看似[^。！？\n]{0,80}(?:实则|其实|实际)"),
)

AI_ROADS = (
    "更重要的是",
    "真正的问题是",
    "真正的关键是",
    "值得注意的是",
    "需要指出的是",
    "更深一层",
    "还有一层",
    "从某种意义上说",
    "说白了",
    "先说结论",
)

JARGON = (
    "底层逻辑",
    "认知跃迁",
    "赋能",
    "抓手",
    "商业闭环",
    "价值闭环",
    "内容矩阵",
    "全链路",
    "组合拳",
    "顶层设计",
    "价值释放",
    "降本增效",
)

CONTEXT_JARGON = (
    "沉淀",
    "颗粒度",
    "对齐",
    "协同",
    "链路",
    "生态位",
    "心智",
    "范式",
    "方法论",
    "核心变量",
)

SOFT_MARKERS = (
    "真正",
    "本质上",
    "归根结底",
    "换句话说",
    "这意味着",
    "核心是",
    "关键在于",
)

MANIPULATION = (
    re.compile(r"所有人都(?:错了|被骗了|忽略了)"),
    re.compile(r"(?:再不|如果不|不)[^。！？\n]{0,20}(?:就会|迟早会)[^。！？\n]{0,20}(?:淘汰|抛弃|毁掉)"),
    re.compile(r"你必须[^。！？\n]{0,30}(?:否则|不然)"),
)

CHEAP_SOUP = (
    "愿你成为更好的自己",
    "请相信时间的力量",
    "人生没有白走的路",
    "未来属于那些",
    "一切都是最好的安排",
)

OPENERS = (
    "其实",
    "不过",
    "当然",
    "所以",
    "但是",
    "很多人",
    "问题是",
    "更重要的是",
    "真正的问题是",
)

ABSTRACT_QUOTES = re.compile(r"[“\"](?:所谓)?[\u4e00-\u9fff]{2,10}[”\"]")

METAPHOR_FIELDS = {
    "战争": ("战场", "弹药", "开火", "引爆", "杀死"),
    "建筑": ("地基", "底座", "支柱", "坍塌", "废墟"),
    "海洋": ("浪潮", "潮水", "蓝海", "彼岸", "航船"),
    "机器": ("齿轮", "引擎", "发动机", "骨架", "血管"),
    "道路": ("赛道", "跑道", "岔路", "十字路口", "终点线"),
    "温度": ("温度", "降温", "升温", "冷却", "余温"),
}


@dataclass(frozen=True)
class Profile:
    pivot_max: int
    dash_max: int
    road_max: int = 0
    jargon_max: int = 0
    manipulation_max: int = 0
    soup_max: int = 0


PROFILES = {
    "general": Profile(pivot_max=1, dash_max=2),
    "wechat": Profile(pivot_max=1, dash_max=1),
    "moments": Profile(pivot_max=1, dash_max=1),
}


def han_count(text: str) -> int:
    return len(re.findall(r"[\u4e00-\u9fff]", text))


def mask_non_prose(text: str) -> str:
    def blank(match: re.Match[str]) -> str:
        return "".join("\n" if char == "\n" else " " for char in match.group())

    patterns = (
        re.compile(r"\A---\s*\n.*?\n---\s*(?:\n|\Z)", re.DOTALL),
        re.compile(r"```.*?```", re.DOTALL),
        re.compile(r"`[^`\n]*`"),
        re.compile(r"https?://[^\s)>]+"),
        re.compile(r"\]\([^\n)]*\)"),
    )
    result = text
    for pattern in patterns:
        result = pattern.sub(blank, result)
    return result


def paragraph_texts(text: str) -> list[str]:
    values = []
    for block in re.split(r"\n\s*\n", text):
        clean = re.sub(r"^[#>*+\-\d.、\s]+", "", block.strip())
        if han_count(clean) >= 2:
            values.append(clean)
    return values


def pattern_count(text: str, patterns: tuple[re.Pattern[str], ...]) -> int:
    return sum(len(pattern.findall(text)) for pattern in patterns)


def term_count(text: str, terms: tuple[str, ...]) -> int:
    return sum(text.count(term) for term in terms)


def consecutive_short_paragraphs(paragraphs: list[str], limit: int = 3) -> int:
    streak = 0
    longest = 0
    for paragraph in paragraphs:
        sentences = len(re.findall(r"[。！？!?]", paragraph)) or 1
        if han_count(paragraph) <= 28 and sentences == 1:
            streak += 1
            longest = max(longest, streak)
        else:
            streak = 0
    return longest if longest >= limit else 0


def metaphor_cluster(text: str, distance: int = 800) -> tuple[int, list[str]]:
    hits = []
    for field, words in METAPHOR_FIELDS.items():
        for word in words:
            hits.extend((match.start(), field) for match in re.finditer(re.escape(word), text))
    hits.sort()
    for index, (start, _) in enumerate(hits):
        fields = {
            field
            for position, field in hits[index:]
            if position - start <= distance
        }
        if len(fields) >= 3:
            return len(fields), sorted(fields)
    return 0, []


def uniform_paragraph_lengths(paragraphs: list[str]) -> bool:
    if len(paragraphs) < 8:
        return False
    lengths = [han_count(paragraph) for paragraph in paragraphs]
    mean = statistics.fmean(lengths)
    return mean >= 12 and statistics.pstdev(lengths) / mean <= 0.15


def repeated_openers(paragraphs: list[str]) -> dict[str, int]:
    counts: collections.Counter[str] = collections.Counter()
    for paragraph in paragraphs:
        value = paragraph.lstrip("“‘\"（(")
        for opener in OPENERS:
            if value.startswith(opener):
                counts[opener] += 1
                break
    return {key: count for key, count in counts.items() if count >= 3}


def analyze(text: str, profile_name: str) -> tuple[dict[str, int], list[str], list[str]]:
    prose = mask_non_prose(text)
    paragraphs = paragraph_texts(prose)
    profile = PROFILES[profile_name]

    metrics = {
        "han": han_count(prose),
        "paragraphs": len(paragraphs),
        "pivots": pattern_count(prose, PIVOTS),
        "dashes": prose.count("—") + prose.count("–"),
        "colons": prose.count("：") + prose.count(":"),
        "ai_roads": term_count(prose, AI_ROADS),
        "jargon": term_count(prose, JARGON),
        "context_jargon": term_count(prose, CONTEXT_JARGON),
        "soft_markers": term_count(prose, SOFT_MARKERS),
        "manipulation": pattern_count(prose, MANIPULATION),
        "cheap_soup": term_count(prose, CHEAP_SOUP),
        "abstract_quotes": len(ABSTRACT_QUOTES.findall(prose)),
        "questions": prose.count("？") + prose.count("?"),
    }

    issues = []
    if metrics["pivots"] > profile.pivot_max:
        issues.append(f"翻案句 {metrics['pivots']} 处，当前档位最多 {profile.pivot_max} 处")
    if metrics["dashes"] > profile.dash_max:
        issues.append(f"破折号 {metrics['dashes']} 处，当前档位最多 {profile.dash_max} 处")
    if metrics["ai_roads"] > profile.road_max:
        issues.append(f"模型路标 {metrics['ai_roads']} 处")
    if metrics["jargon"] > profile.jargon_max:
        issues.append(f"抬价黑话 {metrics['jargon']} 处")
    if metrics["manipulation"] > profile.manipulation_max:
        issues.append(f"制造敌人或恐惧 {metrics['manipulation']} 处")
    if metrics["cheap_soup"] > profile.soup_max:
        issues.append(f"廉价鸡汤 {metrics['cheap_soup']} 处")

    warnings = []
    if metrics["colons"] >= max(3, metrics["han"] // 500 + 2):
        warnings.append(f"冒号 {metrics['colons']} 处，检查是否在连续下定义或列提纲")
    if metrics["abstract_quotes"] >= 3:
        warnings.append(f"抽象引号 {metrics['abstract_quotes']} 处，检查是否在制造假概念")
    if metrics["context_jargon"]:
        warnings.append(
            f"语境词 {metrics['context_jargon']} 处，确认是专业本义，不是给普通事情抬价"
        )

    marker_limit = max(2, metrics["han"] // 800)
    if metrics["soft_markers"] > marker_limit:
        warnings.append(
            f"洞察路标 {metrics['soft_markers']} 处，当前提醒线 {marker_limit} 处"
        )

    question_limit = max(4, metrics["han"] // 350 + 2)
    if metrics["questions"] > question_limit:
        warnings.append(
            f"问号 {metrics['questions']} 处，当前提醒线 {question_limit} 处，检查是否用反问制造节奏"
        )

    longest = consecutive_short_paragraphs(paragraphs)
    if longest:
        warnings.append(f"连续 {longest} 个短单句段，检查是否形成口号鼓点")

    field_count, fields = metaphor_cluster(prose)
    if field_count:
        warnings.append(
            f"八百字内出现 {field_count} 套比喻世界，{'、'.join(fields)}"
        )

    openers = repeated_openers(paragraphs)
    if openers:
        detail = "、".join(f"{key} {count} 次" for key, count in openers.items())
        warnings.append(f"段落开场重复，{detail}")

    if len(paragraphs) >= 8:
        one_sentence = sum(
            (len(re.findall(r"[。！？!?]", paragraph)) or 1) == 1
            for paragraph in paragraphs
        )
        if one_sentence / len(paragraphs) >= 0.85:
            warnings.append("超过八成段落只有一句话，检查节奏是否过度统一")
        if uniform_paragraph_lengths(paragraphs):
            warnings.append("段落长度过于整齐，检查是否按固定模具切段")

    return metrics, issues, warnings


def run_self_test() -> int:
    clean = (
        "客户把方案退回来，只说了一句，听起来都对，就是不知道先做什么。\n\n"
        "我重新看了一遍，问题出在顺序。前面讲了太多背景，真正要执行的动作藏在最后。\n\n"
        "后来我把第一步提到开头，删掉一半解释。客户当天就给了反馈。"
    )
    bad = (
        "说白了，这不是一次选择，而是一场认知跃迁—所有人都错了。\n\n"
        "真正的问题是，你如果不改变，就会被时代淘汰。\n\n"
        "愿你成为更好的自己。"
    )
    short_streak = "第一句。\n\n第二句。\n\n第三句。"
    mixed_metaphors = "这股浪潮冲进赛道，最后撞塌了原来的地基。"
    context_terms = "先对齐方法论，再讨论真实流程。"

    clean_metrics, clean_issues, clean_warnings = analyze(clean, "wechat")
    bad_metrics, bad_issues, _ = analyze(bad, "wechat")
    _, _, streak_warnings = analyze(short_streak, "wechat")
    _, _, metaphor_warnings = analyze(mixed_metaphors, "wechat")
    context_metrics, _, context_warnings = analyze(context_terms, "general")
    checks = {
        "clean_has_han": clean_metrics["han"] > 0,
        "clean_has_no_strict_issues": not clean_issues,
        "clean_has_no_warnings": not clean_warnings,
        "bad_detects_pivot": bad_metrics["pivots"] > 0,
        "bad_detects_road": bad_metrics["ai_roads"] > 0,
        "bad_detects_jargon": bad_metrics["jargon"] > 0,
        "bad_detects_manipulation": bad_metrics["manipulation"] > 0,
        "bad_detects_soup": bad_metrics["cheap_soup"] > 0,
        "bad_has_strict_issues": bool(bad_issues),
        "short_streak_warns": any("短单句段" in warning for warning in streak_warnings),
        "metaphor_cluster_warns": any("比喻世界" in warning for warning in metaphor_warnings),
        "context_jargon_counts": context_metrics["context_jargon"] == 2,
        "context_jargon_warns": any("语境词" in warning for warning in context_warnings),
    }
    for name, passed in checks.items():
        print(f"{name}={'PASS' if passed else 'FAIL'}")
    return 0 if all(checks.values()) else 1


def main() -> int:
    parser = argparse.ArgumentParser(description="扫描唐式中文成稿中的高风险模板形状")
    parser.add_argument("path", nargs="?", help="Markdown 或文本稿件，使用 - 从标准输入读取")
    parser.add_argument("--profile", choices=sorted(PROFILES), default="general")
    parser.add_argument("--strict", action="store_true", help="命中档位阈值时返回失败")
    parser.add_argument("--self-test", action="store_true", help="运行内置回归检查")
    args = parser.parse_args()

    if args.self_test:
        return run_self_test()
    if not args.path:
        parser.error("需要稿件路径，或使用 --self-test")

    try:
        text = sys.stdin.read() if args.path == "-" else Path(args.path).read_text(encoding="utf-8")
    except (OSError, UnicodeError) as error:
        print(f"无法读取稿件：{error}", file=sys.stderr)
        return 2

    metrics, issues, warnings = analyze(text, args.profile)
    print(
        f"档位 {args.profile}，汉字 {metrics['han']}，段落 {metrics['paragraphs']}，"
        f"翻案句 {metrics['pivots']}，破折号 {metrics['dashes']}，冒号 {metrics['colons']}，"
        f"模型路标 {metrics['ai_roads']}，黑话 {metrics['jargon']}，"
        f"语境词 {metrics['context_jargon']}，洞察路标 {metrics['soft_markers']}，"
        f"情绪绑架 {metrics['manipulation']}，鸡汤 {metrics['cheap_soup']}，"
        f"问号 {metrics['questions']}"
    )

    if issues:
        print("\n需要修改或明确保留理由")
        for issue in issues:
            print(f"- {issue}")

    if warnings:
        print("\n需要人工判断")
        for warning in warnings:
            print(f"- {warning}")

    if not issues and not warnings:
        print("\n未发现检查器覆盖的高风险形状。")

    return 1 if args.strict and issues else 0


if __name__ == "__main__":
    raise SystemExit(main())
