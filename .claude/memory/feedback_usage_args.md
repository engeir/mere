---
name: feedback-usage-args
description: Use #USAGE comments + os.environ for arg parsing in mise Python tasks, not argparse or subprocess calls
metadata:
  type: feedback
---

Mise tasks (any language) use `#USAGE` spec comments. Mise injects parsed values as `usage_*` env vars at runtime — no eval, no subprocess call to usage CLI needed.

In Python tasks: `os.environ.get("usage_vault_root", "")` for flags; `sys.argv[1:]` for positional args passed after `--`.

**Why:** User pointed to `/home/eirikre/stowfiles/.mise/tasks/` as reference. Those bash tasks use `$usage_*` vars directly (e.g. `$usage_action`, `$usage_update`) without any `eval "$(usage eval ...)"`. The Python equivalent is `os.environ`.

**How to apply:** Any new mise task (Python or bash) in this project — use `#USAGE` spec comments + env var access. Do not use argparse, subprocess usage calls, or bash eval wrappers.
