import os
import re
import sys

import google.generativeai as genai
from github import Github

# ==============================================================================
# Configuration
# ==============================================================================
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
REPO_NAME = os.getenv("GITHUB_REPOSITORY")  # e.g. "username/project-euler"

try:
    PR_NUMBER = int(os.getenv("PR_NUMBER"))
except (ValueError, TypeError):
    print("Error: Could not read PR_NUMBER environment variable. Ensure it is passed correctly in the Workflow.")
    sys.exit(1)

# ==============================================================================
# System Prompt
# ==============================================================================
SYSTEM_PROMPT = """
PURPOSE
Act as a senior Python reviewer for a Project Euler solutions repository.
Provide precise, LeetCode-style feedback focused on algorithmic rigor and idiomatic Python.

SCOPE
Review ONLY files changed in this PR matching the pattern:
- Directories named: problem<int>
- Target file: sol.py

Ignore all other files including: description.txt, lockfiles, markdown, images, generated or non-Python artifacts.

Priorities (in order):
Correctness > Time & Space Complexity > Algorithmic improvements > Readability/Maintainability > Micro-style nitpicks.

OUTPUT FORMAT (STRICT, DO NOT DEVIATE)
For each changed `problem-<int>/sol.py` file, respond in EXACTLY this structure and nothing else:

-> Complexity Table:

| component | time_complexity | space_complexity | bottleneck | notes |
| --- | --- | --- | --- | --- |
| <function_or_block_name> | O(...) | O(...) | <short phrase> | <1–2 sentence explanation> |

Rules for the Complexity Table:
- Include 1–3 rows max, only for the main solution entry point(s) and any true bottleneck helper(s).
- "component" should be the function or logical block name (e.g., `solve`, `is_prime`, "outer loop").
- "notes" must be concise and reference specific lines or behavior
(e.g., "nested loop over all n-digit pairs, lines 10–24").
- If there is really only one relevant component, use a single row.

-> Improvements

List only concrete improvement items, each on its own line, using this pattern:

- [TAG] <short title>: <1–2 sentence explanation>. Complexity: O(old) → O(new). Ref: <lines>. Optional snippet:
  ```python
  # <= 10 lines showing the improved idea
  ```

Where:
TAG is one of: [ALG], [PERF], [MEM], [STYLE].

Focus on:
- Algorithmic optimizations (better approach, pruning, math formulas).
- Time/space improvements.
- Important Python style issues only when they impact readability or correctness.
- Every item must reference the actual code (function name and/or line range).
- Prefer at most 3–5 items per file. Skip tiny nitpicks.

HARD CONSTRAINTS:
- Do NOT add any other sections, headings, or prose before or after these two blocks.
- Do NOT restate the problem, the code, or this prompt.
- Do NOT use numbered sections like "1) Complexity Analysis" or "2) Algorithmic Improvements".
- If something is already optimal, say so briefly in the corresponding "notes" cell
and keep Improvements minimal or empty.

CONTEXT:
Each Euler challenge lives under problem<int>/ with:
- description.txt (problem description, not to be reviewed)
-sol.py (my solution code to evaluate)

The goal is to get high-signal feedback, similar to LeetCode editorial comments,
to improve both algorithm design and Python coding style over time.

```
You can now tweak the table columns or the Improvements bullet pattern if Codex still drifts,
but this should pull it very close to:

```text
-> Complexity Table:
| ... |

-> Improvements
- [ALG] ...
- [PERF] ...
```
"""

# ==============================================================================
# Main Functions
# ==============================================================================


def setup_gemini():
    if not GEMINI_API_KEY:
        print("Error: GEMINI_API_KEY not found")
        sys.exit(1)

    genai.configure(api_key=GEMINI_API_KEY)
    return genai.GenerativeModel("gemini-2.5-flash")


def get_target_files(repo, pr_number):
    pr = repo.get_pull(pr_number)
    target_files = []

    # Get all files changed in this PR
    files = pr.get_files()

    for file in files:
        if not re.match(r"problem\d+/sol\.py", file.filename):
            continue

        if file.status == "removed":
            continue

        print(f"Target file found: {file.filename}")

        try:
            content = repo.get_contents(file.filename, ref=pr.head.sha).decoded_content.decode("utf-8")
            target_files.append({"filename": file.filename, "content": content, "raw_file_obj": file})
        except Exception as e:
            print(f"Failed to read file {file.filename}: {e}")

    return pr, target_files


def generate_review(model, filename, code_content):
    # User Prompt
    user_message = f"""
    CONTEXT:
    The user has submitted a solution for a Project Euler problem in Python.

    FILE NAME: {filename}

    CODE CONTENT:
    ```python
    {code_content}
    ```

    Please review this code based on the SYSTEM PROMPT instructions provided.
    """

    try:
        response = model.generate_content(f"{SYSTEM_PROMPT}\n\n----------------\n\n{user_message}")
        return response.text
    except Exception as e:
        print(f"Gemini API call failed: {e}")
        return None


def post_comment(pr, filename, review_content):
    if not review_content:
        return

    comment_body = f"### 🤖 AI Code Review: `{filename}`\n\n{review_content}"

    try:
        pr.create_issue_comment(comment_body)
        print(f"Successfully posted comment on: {filename}")
    except Exception as e:
        print(f"Failed to post comment: {e}")


# ==============================================================================
# Main Execution
# ==============================================================================


def main():
    print("--- Starting AI Code Review ---")

    if not GITHUB_TOKEN:
        print("Error: GITHUB_TOKEN not found")
        sys.exit(1)

    model = setup_gemini()
    g = Github(GITHUB_TOKEN)
    repo = g.get_repo(REPO_NAME)

    print(f"Fetching data for PR #{PR_NUMBER}...")
    pr, files_to_review = get_target_files(repo, PR_NUMBER)

    if not files_to_review:
        print("No qualifying files found (problem-X/sol.py). Review finished.")
        return

    print(f"Found {len(files_to_review)} files requiring review in total.")

    for file_data in files_to_review:
        filename = file_data["filename"]
        content = file_data["content"]

        print(f"Analyzing: {filename} ...")
        review_result = generate_review(model, filename, content)

        if review_result:
            post_comment(pr, filename, review_result)
        else:
            print(f"Skipping {filename} (no analysis result)")

    print("--- AI Code Review Complete ---")


if __name__ == "__main__":
    main()
