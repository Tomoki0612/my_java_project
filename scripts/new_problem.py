#!/usr/bin/env python3
"""
LeetCode 問題テンプレート自動生成スクリプト

Usage:
  python3 scripts/new_problem.py <問題番号>
  python3 scripts/new_problem.py <slug>

Example:
  python3 scripts/new_problem.py 1
  python3 scripts/new_problem.py two-sum --ja
"""

import sys
import json
import urllib.request
import urllib.error
import re
import os
import subprocess

GRAPHQL_URL = "https://leetcode.com/graphql"
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC_ROOT  = os.path.join(PROJECT_ROOT, "src", "main", "java", "leetcode")
TEST_ROOT = os.path.join(PROJECT_ROOT, "src", "test", "java", "leetcode")


def graphql_request(query, variables=None):
    payload = json.dumps({"query": query, "variables": variables or {}}).encode()
    req = urllib.request.Request(
        GRAPHQL_URL,
        data=payload,
        headers={
            "Content-Type": "application/json",
            "Referer": "https://leetcode.com",
            "User-Agent": "Mozilla/5.0",
        },
    )
    with urllib.request.urlopen(req, timeout=10) as resp:
        return json.loads(resp.read())


def get_slug_by_number(number):
    query = """
    query($skip: Int!, $limit: Int!) {
        questionList(
            categorySlug: ""
            limit: $limit
            skip: $skip
            filters: {}
        ) {
            data {
                questionFrontendId
                titleSlug
            }
        }
    }
    """
    result = graphql_request(query, {"skip": number - 1, "limit": 1})
    questions = result["data"]["questionList"]["data"]
    if questions and int(questions[0]["questionFrontendId"]) == number:
        return questions[0]["titleSlug"]
    return None


def fetch_problem(slug):
    query = """
    query($titleSlug: String!) {
        question(titleSlug: $titleSlug) {
            questionFrontendId
            title
            titleSlug
            difficulty
            content
            metaData
            exampleTestcases
            codeSnippets {
                lang
                code
            }
        }
    }
    """
    result = graphql_request(query, {"titleSlug": slug})
    return result["data"]["question"]


def html_to_text(html):
    html = re.sub(r"<pre>(.*?)</pre>", lambda m: "\n" + m.group(1) + "\n", html, flags=re.DOTALL)
    html = re.sub(r"<br\s*/?>", "\n", html)
    html = re.sub(r"</p>|</li>|</ul>|</ol>", "\n", html)
    html = re.sub(r"<li>", "  - ", html)
    html = re.sub(r"<strong>(.*?)</strong>", r"\1", html)
    html = re.sub(r"<em>(.*?)</em>", r"\1", html)
    html = re.sub(r"<code>(.*?)</code>", r"`\1`", html, flags=re.DOTALL)
    html = re.sub(r"<[^>]+>", "", html)
    entities = {
        "&lt;": "<", "&gt;": ">", "&amp;": "&", "&quot;": '"',
        "&#39;": "'", "&nbsp;": " ", "&le;": "<=", "&ge;": ">=",
        "&times;": "x", "&hellip;": "...",
    }
    for ent, char in entities.items():
        html = html.replace(ent, char)
    html = re.sub(r"\n{3,}", "\n\n", html)
    return html.strip()


def translate_to_japanese(text):
    prompt = (
        "以下のLeetCode問題文を日本語に翻訳してください。\n"
        "- コード例・変数名・数値はそのまま残す\n"
        "- 翻訳文のみ出力し、前置きや説明は不要\n"
        "- 1行が長くなる場合は、文の意味の区切り（句点・読点・接続詞など）で改行する\n"
        "- 1行の目安は全角60文字程度\n\n"
        + text
    )
    result = subprocess.run(
        ["claude", "-p", prompt],
        capture_output=True, text=True, timeout=60
    )
    if result.returncode != 0:
        return text
    return result.stdout.strip()


def wrap_line(line, max_width=76):
    """1行が長すぎる場合に折り返す"""
    if len(line) <= max_width:
        return [line]
    result = []
    while len(line) > max_width:
        # 英語はスペースで折り返す、日本語は文字数で折り返す
        break_pos = line.rfind(' ', 0, max_width)
        if break_pos <= 0:
            break_pos = max_width
        result.append(line[:break_pos])
        line = line[break_pos:].lstrip()
    if line:
        result.append(line)
    return result


def wrap_as_java_comment(text):
    result = ["/*"]
    for line in text.split("\n"):
        if not line.strip():
            result.append(" *")
        else:
            for wrapped in wrap_line(line):
                result.append((" * " + wrapped).rstrip())
    result.append(" */")
    return "\n".join(result)


def to_package_dir(fid, slug):
    return f"p{fid:04d}_{slug.replace('-', '_')}"


# ---------- テスト生成 ----------

def extract_examples(content_html):
    """HTML から (input行, output値) のリストを抽出する"""
    pre_blocks = re.findall(r"<pre>(.*?)</pre>", content_html, re.DOTALL)
    examples = []
    for block in pre_blocks:
        text = re.sub(r"<[^>]+>", "", block)
        for ent, ch in {"&lt;": "<", "&gt;": ">", "&amp;": "&", "&nbsp;": " "}.items():
            text = text.replace(ent, ch)
        input_m  = re.search(r"Input:\s*(.+?)(?=\nOutput:)", text, re.DOTALL)
        output_m = re.search(r"Output:\s*(.+?)(?=\nExplanation:|\nInput:|$)", text, re.DOTALL)
        if input_m and output_m:
            examples.append({
                "input":  input_m.group(1).strip().replace("\n", " / "),
                "output": output_m.group(1).strip(),
            })
    return examples


def raw_to_java(raw, lc_type):
    raw = raw.strip()
    t = lc_type.lower()
    if t in ("integer", "int", "boolean", "long", "double", "float"):
        return raw
    if t == "string":
        return raw  # すでに "..." 形式
    if t in ("integer[]", "int[]"):
        inner = raw.strip("[]")
        return f"new int[]{{{inner}}}" if inner else "new int[]{}"
    if t == "string[]":
        inner = raw.strip("[]")
        return f'new String[]{{{inner}}}' if inner else "new String[]{}"
    if t == "long[]":
        inner = raw.strip("[]")
        return f"new long[]{{{inner}}}" if inner else "new long[]{}"
    return None  # 複雑な型は手動で


def build_test(problem, pkg_dir, examples):
    package = f"leetcode.{pkg_dir}"
    title = problem["title"]
    difficulty = problem["difficulty"]

    try:
        meta = json.loads(problem.get("metaData") or "{}")
        method_name = meta.get("name", "solve")
        params      = meta.get("params", [])
        return_type = meta.get("return", {}).get("type", "void")
    except Exception:
        method_name, params, return_type = "solve", [], "void"

    # exampleTestcases を問題ごとにグループ化
    raw_lines = [l.strip() for l in (problem.get("exampleTestcases") or "").split("\n") if l.strip()]
    n = len(params)
    grouped = [raw_lines[i:i+n] for i in range(0, len(raw_lines), n)] if n > 0 else []

    test_methods = []
    for i, ex in enumerate(examples):
        # アサーション生成を試みる
        assertion = None
        if i < len(grouped) and params and n == len(grouped[i]):
            java_args = [raw_to_java(grouped[i][j], params[j].get("type", "")) for j in range(n)]
            expected  = raw_to_java(ex["output"], return_type)
            if None not in java_args and expected is not None:
                call = f"solution.{method_name}({', '.join(java_args)})"
                rt = return_type.lower()
                if "[]" in rt:
                    assertion = f"assertArrayEquals({expected}, {call});"
                elif rt in ("double", "float"):
                    assertion = f"assertEquals({expected}, {call}, 1e-5);"
                else:
                    assertion = f"assertEquals({expected}, {call});"

        if assertion is None:
            assertion = f"// assertEquals(expected, solution.{method_name}(...));"

        test_methods.append(
            f"\n    @Test\n    void example{i + 1}() {{\n"
            f"        // Input:  {ex['input']}\n"
            f"        // Output: {ex['output']}\n"
            f"        {assertion}\n"
            f"    }}"
        )

    if not test_methods:
        test_methods.append("\n    @Test\n    void example1() {\n        // TODO: add test cases\n    }")

    return (
        f"package {package};\n\n"
        f"import org.junit.jupiter.api.Test;\n"
        f"import static org.junit.jupiter.api.Assertions.*;\n\n"
        f"// {title} [{difficulty}]\n"
        f"class SolutionTest {{\n"
        f"    private final Solution solution = new Solution();\n"
        + "\n".join(test_methods) +
        "\n}\n"
    )


# ---------- メイン ----------

def lc_type_to_java(t):
    t = t.strip()
    mapping = {
        "integer": "int", "int": "int",
        "string": "String",
        "boolean": "boolean",
        "double": "double", "float": "float",
        "long": "long",
        "character": "char",
        "void": "void",
        "integer[]": "int[]", "int[]": "int[]",
        "string[]": "String[]",
        "boolean[]": "boolean[]",
        "character[]": "char[]",
        "long[]": "long[]",
        "integer[][]": "int[][]",
        "string[][]": "String[][]",
    }
    lower = t.lower()
    if lower in mapping:
        return mapping[lower]
    m = re.match(r"list<(.+)>", lower)
    if m:
        inner = lc_type_to_java(m.group(1))
        box = {"int": "Integer", "long": "Long", "double": "Double",
               "boolean": "Boolean", "char": "Character"}.get(inner, inner)
        return f"List<{box}>"
    return t  # ListNode / TreeNode / Node など


def default_return(java_type):
    stmts = {"int": "return 0;", "boolean": "return false;",
              "double": "return 0.0;", "float": "return 0.0f;",
              "long": "return 0L;", "char": "return '\\0';", "void": ""}
    return stmts.get(java_type, "return null;")


def build_solution(problem, translate=False):
    fid        = int(problem["questionFrontendId"])
    slug       = problem["titleSlug"]
    title      = problem["title"]
    difficulty = problem["difficulty"]
    content    = html_to_text(problem.get("content") or "")

    if translate:
        print("日本語に翻訳中...")
        content = translate_to_japanese(content)

    pkg_dir = to_package_dir(fid, slug)
    header  = f"{title}\nDifficulty: {difficulty}\nhttps://leetcode.com/problems/{slug}/\n\n{content}"
    comment = wrap_as_java_comment(header)

    # LeetCode の Java コードスニペットを使う
    java_snippet = next(
        (s["code"] for s in (problem.get("codeSnippets") or []) if s["lang"] == "Java"),
        None
    )

    if java_snippet:
        # 空のメソッドボディにプレースホルダーの return を追加
        try:
            meta     = json.loads(problem.get("metaData") or "{}")
            ret_lc   = meta.get("return", {}).get("type", "void")
            ret_stmt = default_return(lc_type_to_java(ret_lc))
        except Exception:
            ret_stmt = "return null;"
        if ret_stmt:
            java_snippet = re.sub(
                r'(\{)\s*\n(\s*)\n(\s*\})',
                lambda m: f"{m.group(1)}\n{m.group(2)}{ret_stmt}\n{m.group(3)}",
                java_snippet
            )
        class_body = java_snippet
    else:
        # フォールバック: metaData から生成
        try:
            meta        = json.loads(problem.get("metaData") or "{}")
            method_name = meta.get("name", "solve")
            params      = meta.get("params", [])
            ret_lc      = meta.get("return", {}).get("type", "void")
            ret_java    = lc_type_to_java(ret_lc)
            params_java = [f"{lc_type_to_java(p['type'])} {p['name']}" for p in params]
            ret_stmt    = default_return(ret_java)
            body        = f"        {ret_stmt}" if ret_stmt else "        "
            method      = f"    public {ret_java} {method_name}({', '.join(params_java)}) {{\n{body}\n    }}"
            needs_list  = any("List<" in lc_type_to_java(p.get("type","")) for p in params) or "List<" in ret_java
            import_line = "import java.util.*;\n\n" if needs_list else ""
            class_body  = f"{import_line}class Solution {{\n{method}\n}}"
        except Exception:
            class_body = "class Solution {\n    // TODO: implement\n}"

    template = f"{comment}\npackage leetcode.{pkg_dir};\n\n{class_body}\n"
    return pkg_dir, template


def main():
    if len(sys.argv) < 2:
        print("Usage: python3 scripts/new_problem.py <問題番号またはslug> [--ja]")
        sys.exit(1)

    arg = sys.argv[1]
    if arg.isdigit():
        number = int(arg)
        print(f"#{number} の slug を検索中...")
        slug = get_slug_by_number(number)
        if not slug:
            print(f"問題 #{number} が見つかりませんでした")
            sys.exit(1)
        print(f"Slug: {slug}")
    else:
        slug = arg

    print(f"問題情報を取得中: {slug} ...")
    problem = fetch_problem(slug)
    if not problem:
        print(f"問題が見つかりませんでした: {slug}")
        sys.exit(1)

    translate = "--ja" in sys.argv
    pkg_dir, solution_code = build_solution(problem, translate=translate)

    src_dir   = os.path.join(SRC_ROOT, pkg_dir)
    test_dir  = os.path.join(TEST_ROOT, pkg_dir)
    sol_path  = os.path.join(src_dir, "Solution.java")
    test_path = os.path.join(test_dir, "SolutionTest.java")

    if os.path.exists(sol_path):
        print(f"既に存在します: {sol_path}")
        sys.exit(1)

    # Solution.java
    os.makedirs(src_dir, exist_ok=True)
    with open(sol_path, "w", encoding="utf-8") as f:
        f.write(solution_code)

    # SolutionTest.java
    examples  = extract_examples(problem.get("content") or "")
    test_code = build_test(problem, pkg_dir, examples)
    os.makedirs(test_dir, exist_ok=True)
    with open(test_path, "w", encoding="utf-8") as f:
        f.write(test_code)

    # progress.json
    progress_file = os.path.join(SRC_ROOT, "progress.json")
    progress = {}
    if os.path.exists(progress_file):
        with open(progress_file, encoding="utf-8") as f:
            progress = json.load(f)
    import datetime
    progress[pkg_dir] = {
        "title":        problem["title"],
        "difficulty":   problem["difficulty"],
        "status":       "in_progress",
        "added_date":   datetime.date.today().isoformat(),
        "next_review":  None,
        "mastered_date": None,
    }
    with open(progress_file, "w", encoding="utf-8") as f:
        json.dump(progress, f, ensure_ascii=False, indent=2)

    print(f"作成しました: [{problem['difficulty']}] {problem['title']}")
    print(f"  src/main/java/leetcode/{pkg_dir}/Solution.java")
    print(f"  src/test/java/leetcode/{pkg_dir}/SolutionTest.java")


if __name__ == "__main__":
    main()
