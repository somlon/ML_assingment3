#!/bin/bash
# SessionStart hook: 세션 시작 시 프로젝트 루트의 모든 .md 파일을 컨텍스트로 주입한다.
# - 깊이 3까지의 .md 파일을 수집
# - 숨김 디렉터리(.git, .claude, .ipynb_checkpoints 등) 제외
# - rules.md 를 가장 먼저 배치 (규칙 우선 노출), 나머지는 알파벳 순
# - 각 파일은 '===== 상대경로 =====' 헤더와 함께 합쳐서 additionalContext 로 전달
set -euo pipefail

PROJECT_DIR="${CLAUDE_PROJECT_DIR:-$(pwd)}"

if [ ! -d "$PROJECT_DIR" ]; then
  exit 0
fi

mapfile -t MD_FILES < <(
  find "$PROJECT_DIR" -maxdepth 3 -type f -name "*.md" -not -path "*/.*" \
    | awk '{ if (index($0,"/rules.md")) print "0\t"$0; else print "1\t"$0 }' \
    | sort \
    | cut -f2-
)

if [ "${#MD_FILES[@]}" -eq 0 ]; then
  exit 0
fi

python3 - "$PROJECT_DIR" "${MD_FILES[@]}" <<'PY'
import json
import os
import sys

project_dir = sys.argv[1]
files = sys.argv[2:]

chunks = [
    "다음은 본 레포지토리의 agent 기본 규칙 및 관련 문서들입니다.",
    "세션 동안 반드시 준수하고, 작업 시 참조하세요.",
]

for fp in files:
    try:
        with open(fp, encoding="utf-8") as f:
            content = f.read()
    except Exception:
        continue
    rel = os.path.relpath(fp, project_dir)
    chunks.append(f"\n\n===== {rel} =====\n\n{content}")

payload = {
    "hookSpecificOutput": {
        "hookEventName": "SessionStart",
        "additionalContext": "\n".join(chunks),
    }
}
print(json.dumps(payload, ensure_ascii=False))
PY
