#!/bin/bash
# SessionStart hook: 세션 시작 시 agent 기본 규칙(rules.md)을 컨텍스트로 주입한다.
set -euo pipefail

RULES_FILE="${CLAUDE_PROJECT_DIR:-$(pwd)}/rules.md"

if [ ! -f "$RULES_FILE" ]; then
  # 규칙 파일이 없으면 조용히 종료 (훅이 세션을 막지 않도록)
  exit 0
fi

RULES_CONTENT=$(cat "$RULES_FILE")

# Claude Code SessionStart 훅 스펙: hookSpecificOutput.additionalContext 로 컨텍스트 주입
python3 - "$RULES_CONTENT" <<'PY'
import json, sys
content = sys.argv[1]
payload = {
    "hookSpecificOutput": {
        "hookEventName": "SessionStart",
        "additionalContext": (
            "다음은 본 레포지토리의 agent 기본 규칙입니다. "
            "세션 동안 반드시 준수하세요.\n\n" + content
        ),
    }
}
print(json.dumps(payload, ensure_ascii=False))
PY
