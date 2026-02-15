#!/usr/bin/env python3
"""Parse assembly_prompt.txt into rules.jsonl for RAG indexing.

Splits the monolithic prompt into individual rule nuggets with metadata
for topic_ids, construct_types, priority, and category.
"""
import json
import re
from pathlib import Path

ROOT = Path(__file__).parent.parent
PROMPT_PATH = ROOT / "config" / "assembly_prompt.txt"
OUTPUT_PATH = ROOT / "config" / "rules.jsonl"

CONSTRUCT_KEYWORDS = {
    "node": ["node"],
    "edge": ["edge", "typed edge"],
    "walker": ["walker", "spawn"],
    "obj": ["obj", "object"],
    "enum": ["enum"],
    "connect": ["++>", "<++>", "+>:", ":<+", "connect"],
    "traverse": ["-->", "<--", "->:", ":<-", "traversal"],
    "filter": ["filter", "(?:"],
    "spawn": ["spawn"],
    "visit": ["visit"],
    "report": ["report"],
    "by_llm": ["by llm", "llm", "sem "],
    "can": ["can ", "ability", "abilities"],
    "def": ["def ", "function", "lambda"],
    "glob": ["glob "],
    "import": ["import"],
    "match": ["match", "case"],
    "try_except": ["try", "except", "finally"],
    "async": ["async"],
    "websocket": ["websocket"],
    "api": ["__specs__", "endpoint", "jac start"],
    "jsx": ["jsx", "cl{", ".cl.jac", "<div", "useEffect", "useState"],
    "client": ["cl{", ".cl.jac", "sv import", "client"],
    "auth": ["auth", ":pub", "login", "signup"],
    "permissions": ["grant", "revoke", "Perm"],
    "persistence": ["persist", "save", "commit"],
    "testing": ["test "],
    "routing": ["Router", "Route", "Navigate"],
    "jac_toml": ["jac.toml", "[project]", "[dependencies"],
    "deploy": ["docker", "kubernetes", "deploy"],
    "env": [".env", "load_dotenv", "getenv"],
}

TOPIC_MAP = {
    "1": "types", "2": "control", "3": "functions", "4": "imports",
    "5": "archetypes", "6": "access", "7": "graph", "8": "abilities",
    "9": "walkers", "10": "by_llm", "11": "file_json", "12": "api",
    "13": "websocket", "14": "webhooks", "15": "scheduler", "16": "async",
    "17": "permissions", "18": "persistence", "19": "testing", "20": "stdlib",
    "21": "jsx_client", "22": "routing", "23": "client_auth",
    "24": "jac_toml", "25": "fullstack_setup", "26": "project_structure",
    "27": "walker_crud", "28": "component_patterns", "29": "dev_server",
    "30": "deploy", "31": "env_loading",
}


def detect_construct_types(text: str) -> list[str]:
    text_lower = text.lower()
    found = []
    for construct, keywords in CONSTRUCT_KEYWORDS.items():
        for kw in keywords:
            if kw.lower() in text_lower:
                found.append(construct)
                break
    return found or ["general"]


def detect_topic_ids(text: str) -> list[str]:
    text_lower = text.lower()
    topics = []
    topic_keywords = {
        "types": ["int", "float", "str", "bool", "list[", "dict["],
        "control": ["if ", "elif", "else", "for ", "while", "match"],
        "functions": ["def ", "lambda", "pipe", "glob "],
        "imports": ["import"],
        "archetypes": ["node ", "edge ", "walker ", "obj "],
        "access": [":priv", ":pub", ":protect"],
        "graph": ["++>", "+>:", "-->", "->:", "del-->", "connect", "traversal"],
        "abilities": ["can ", "with entry", "with exit"],
        "walkers": ["spawn", "visit", "report", "disengage"],
        "by_llm": ["by llm", "sem "],
        "api": ["__specs__", "endpoint", "jac start"],
        "jsx_client": ["jsx", "cl{", ".cl.jac", "useEffect", "useState"],
        "routing": ["Router", "Route"],
        "client_auth": ["jacLogin", "jacSignup", "jacLogout"],
        "testing": ["test ", "assert"],
    }
    for topic, keywords in topic_keywords.items():
        for kw in keywords:
            if kw.lower() in text_lower:
                topics.append(topic)
                break
    return topics or ["general"]


def split_syntax_rules(lines: list[str]) -> list[dict]:
    """Split HIGH-FAILURE SYNTAX section (lines 19-89) into individual rules."""
    nuggets = []
    rule_id = 0

    current_rule_lines = []
    for line in lines:
        stripped = line.strip()
        if stripped.startswith("- ") and current_rule_lines:
            rule_text = "\n".join(current_rule_lines).strip()
            if rule_text:
                rule_id += 1
                construct_types = detect_construct_types(rule_text)
                topic_ids = detect_topic_ids(rule_text)
                nuggets.append({
                    "id": f"rule-syntax-{rule_id:03d}",
                    "content": rule_text,
                    "topic_ids": topic_ids,
                    "construct_types": construct_types,
                    "priority": 1,
                    "category": "syntax_rule",
                })
            current_rule_lines = [stripped]
        elif stripped:
            current_rule_lines.append(stripped)

    if current_rule_lines:
        rule_text = "\n".join(current_rule_lines).strip()
        if rule_text:
            rule_id += 1
            construct_types = detect_construct_types(rule_text)
            topic_ids = detect_topic_ids(rule_text)
            nuggets.append({
                "id": f"rule-syntax-{rule_id:03d}",
                "content": rule_text,
                "topic_ids": topic_ids,
                "construct_types": construct_types,
                "priority": 1,
                "category": "syntax_rule",
            })

    return nuggets


def split_topics(lines: list[str]) -> list[dict]:
    """Split TOPICS section into individual topic definitions."""
    nuggets = []
    current_lines = []
    current_num = None

    for line in lines:
        stripped = line.strip()
        topic_match = re.match(r'^(\d+)\.\s+(\w+):', stripped)
        if topic_match and current_lines:
            topic_text = "\n".join(current_lines).strip()
            if topic_text and current_num:
                topic_name = TOPIC_MAP.get(current_num, f"topic_{current_num}")
                nuggets.append({
                    "id": f"rule-topic-{topic_name}",
                    "content": topic_text,
                    "topic_ids": [topic_name],
                    "construct_types": detect_construct_types(topic_text),
                    "priority": 2,
                    "category": "topic_definition",
                })
            current_lines = [stripped]
            current_num = topic_match.group(1)
        elif stripped:
            current_lines.append(stripped)

    if current_lines and current_num:
        topic_text = "\n".join(current_lines).strip()
        if topic_text:
            topic_name = TOPIC_MAP.get(current_num, f"topic_{current_num}")
            nuggets.append({
                "id": f"rule-topic-{topic_name}",
                "content": topic_text,
                "topic_ids": [topic_name],
                "construct_types": detect_construct_types(topic_text),
                "priority": 2,
                "category": "topic_definition",
            })

    return nuggets


def split_verified_examples(lines: list[str]) -> list[dict]:
    """Split VERIFIED SYNTAX EXAMPLES into individual examples."""
    nuggets = []
    example_id = 0
    current_comment = ""
    current_code_lines = []
    in_code = False

    for line in lines:
        stripped = line.strip()

        if stripped.startswith("# ") and not in_code:
            if current_code_lines and current_comment:
                example_id += 1
                code_text = "\n".join(current_code_lines).strip()
                full_text = f"{current_comment}\n{code_text}"
                nuggets.append({
                    "id": f"rule-example-{example_id:03d}",
                    "content": full_text,
                    "topic_ids": detect_topic_ids(full_text),
                    "construct_types": detect_construct_types(full_text),
                    "priority": 1,
                    "category": "verified_example",
                })
                current_code_lines = []

            current_comment = stripped
        elif stripped == "---":
            break
        elif stripped:
            current_code_lines.append(line.rstrip())
        elif current_code_lines:
            current_code_lines.append("")

    if current_code_lines and current_comment:
        example_id += 1
        code_text = "\n".join(current_code_lines).strip()
        full_text = f"{current_comment}\n{code_text}"
        nuggets.append({
            "id": f"rule-example-{example_id:03d}",
            "content": full_text,
            "topic_ids": detect_topic_ids(full_text),
            "construct_types": detect_construct_types(full_text),
            "priority": 1,
            "category": "verified_example",
        })

    return nuggets


def split_patterns(lines: list[str]) -> list[dict]:
    """Split PATTERNS section into individual pattern descriptions."""
    nuggets = []
    pattern_id = 0
    current_lines = []

    for line in lines:
        stripped = line.strip()
        if stripped.startswith("- PATTERN") and current_lines:
            pattern_text = "\n".join(current_lines).strip()
            if pattern_text:
                pattern_id += 1
                nuggets.append({
                    "id": f"rule-pattern-{pattern_id:03d}",
                    "content": pattern_text,
                    "topic_ids": detect_topic_ids(pattern_text),
                    "construct_types": detect_construct_types(pattern_text),
                    "priority": 2,
                    "category": "pattern_definition",
                })
            current_lines = [stripped]
        elif stripped:
            current_lines.append(stripped)

    if current_lines:
        pattern_text = "\n".join(current_lines).strip()
        if pattern_text:
            pattern_id += 1
            nuggets.append({
                "id": f"rule-pattern-{pattern_id:03d}",
                "content": pattern_text,
                "topic_ids": detect_topic_ids(pattern_text),
                "construct_types": detect_construct_types(pattern_text),
                "priority": 2,
                "category": "pattern_definition",
            })

    return nuggets


def main():
    text = PROMPT_PATH.read_text()
    all_lines = text.split("\n")

    # Find section boundaries by searching for marker text
    syntax_start = None
    topics_start = None
    patterns_start = None
    verified_start = None
    golden_start = None

    for i, line in enumerate(all_lines):
        if "HIGH-FAILURE SYNTAX" in line:
            syntax_start = i + 1
        elif line.strip().startswith("TOPICS"):
            topics_start = i + 2  # skip "TOPICS (cover all concisely):" and blank
        elif line.strip().startswith("PATTERNS"):
            patterns_start = i + 1
        elif "VERIFIED SYNTAX EXAMPLES" in line:
            verified_start = i + 2
        elif "GOLDEN STYLE EXAMPLE" in line:
            golden_start = i

    all_nuggets = []

    if syntax_start and topics_start:
        syntax_lines = all_lines[syntax_start:topics_start - 2]
        all_nuggets.extend(split_syntax_rules(syntax_lines))

    if topics_start and patterns_start:
        topic_lines = all_lines[topics_start:patterns_start - 1]
        all_nuggets.extend(split_topics(topic_lines))

    if patterns_start and verified_start:
        # Find the "---" separator before verified
        sep_idx = patterns_start
        for i in range(patterns_start, verified_start):
            if all_lines[i].strip() == "---":
                sep_idx = i
                break
        pattern_lines = all_lines[patterns_start:sep_idx]
        all_nuggets.extend(split_patterns(pattern_lines))

    if verified_start and golden_start:
        verified_lines = all_lines[verified_start:golden_start]
        all_nuggets.extend(split_verified_examples(verified_lines))

    # Add global directives as a single nugget
    global_lines = all_lines[:syntax_start - 1] if syntax_start else all_lines[:19]
    global_text = "\n".join(global_lines).strip()
    if global_text:
        all_nuggets.insert(0, {
            "id": "rule-global-directives",
            "content": global_text,
            "topic_ids": ["global"],
            "construct_types": ["general"],
            "priority": 1,
            "category": "global_directive",
        })

    # Add golden style example as a nugget
    if golden_start:
        golden_lines = all_lines[golden_start:]
        golden_text = "\n".join(golden_lines).strip()
        if golden_text:
            all_nuggets.append({
                "id": "rule-golden-style",
                "content": golden_text,
                "topic_ids": ["global"],
                "construct_types": ["general"],
                "priority": 1,
                "category": "golden_style",
            })

    with open(OUTPUT_PATH, "w") as f:
        for nugget in all_nuggets:
            f.write(json.dumps(nugget) + "\n")

    print(f"Wrote {len(all_nuggets)} rules to {OUTPUT_PATH}")
    by_category = {}
    for n in all_nuggets:
        cat = n["category"]
        by_category[cat] = by_category.get(cat, 0) + 1
    for cat, count in sorted(by_category.items()):
        print(f"  {cat}: {count}")


if __name__ == "__main__":
    main()
