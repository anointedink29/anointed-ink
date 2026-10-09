# Project instructions

## Start each chat

1. Read `MEMORY.md` and the latest entries in `WORKLOG.md` before project work.
2. Check `git status --short --branch` and inspect the files relevant to the request.
3. Use the current code and the user's latest instructions to resolve stale notes. Do not repeat completed setup or ask for authorization already given in the conversation.

## Work on this site

- Edit Python source files for generated site changes, then rebuild the HTML. Direct edits to generated pages will be overwritten.
- `_data.py` holds business facts and launch settings. `_css.py` holds shared styling; `_js.py` holds interactions; `_shell.py` holds shared markup; `build.py` holds page content and generation.
- Preserve accurate artist credits and photo provenance from `img/manifest.json`. Respect `atShop: false` disclosures and `noPromo` restrictions.
- Use existing project content rules in `README.md` and `lint.py`. Do not invent business facts, credentials, review counts, or portfolio ownership. Verify changing facts before updating them.
- After source changes, run `python -X utf8 build.py` and `python -X utf8 lint.py` if Python is available. Inspect the diff and relevant rendered pages for visual changes. Report any checks that could not run.
- On Windows, `.\project.cmd check` runs both checks with the installed Python. `.\project.cmd preview` checks and serves on loopback; `.\project.cmd codex` starts the CLI in this project. See `SETUP.md` for the full workflow.
- Keep the user's unrelated files and changes intact. `debug.log` was already present before the repository checkout.
- The GitHub connection request authorized local setup. It does not by itself authorize publishing future changes; use the user's task instructions to determine commit, push, and deployment scope.

## Maintain continuity

- Update `MEMORY.md` when durable project facts, preferences, decisions, or blockers change.
- Append a concise dated entry to `WORKLOG.md` after meaningful work: request, changes, validation, and outstanding work.
- Record completed work separately from proposed work. Remove resolved blockers and correct stale facts.
- Never store passwords, access tokens, authentication codes, or private credential contents in these files.
- These files provide continuity within this workspace. Do not claim they are global memory or will be read in chats outside this project.
