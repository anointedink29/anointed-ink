# Anointed Ink project memory

Last updated: 2026-10-09

## Purpose and preferences

- This is the static marketing website for Anointed Ink, a tattoo shop in Chicago Ridge, Illinois, owned by Nestor Juarez (`Tat2Nestuhh`).
- The user requested persistent project notes so each chat can continue without repeating setup.
- Continue authorized work autonomously and keep updates clear and concise. Ask only when necessary information or authorization is missing.

## Workspace and GitHub

- Local workspace: `C:\Users\anoin\OneDrive\Desktop\anointed ink ai project`.
- Repository: https://github.com/anointedink29/anointed-ink
- Remote `origin`: `https://github.com/anointedink29/anointed-ink.git`.
- Local `main` tracks `origin/main`. Repository files were fetched and checked out successfully on 2026-10-09.
- GitHub CLI account: `anointedink29`, authenticated and Git credential setup completed in the user's PowerShell. Authentication was confirmed by user-provided `gh auth status` output.
- Git for Windows 2.55.0 is installed at `C:\Program Files\Git\cmd\git.exe`. Existing tool sessions may need this absolute path because their PATH predates installation.
- At setup completion, `debug.log` was an existing untracked file. Do not commit or delete it automatically.

## Site implementation

| File | Purpose |
| --- | --- |
| `_data.py` | Business details, artists, navigation, launch settings, and review data |
| `_css.py` | Shared design system and CSS |
| `_js.py` | Gallery filtering, lightbox, and mobile navigation |
| `_shell.py` | Shared page head, navigation, footer, schema, image helpers |
| `build.py` | Page content and static site generation |
| `lint.py` | Content, SEO, markup, and artist-credit validation gate |
| `img/manifest.json` | Photo metadata, artist attribution, and usage restrictions |
| `make-og.py` | Social preview image generation; currently has a macOS Chrome path |

- Generated HTML, `robots.txt`, and `sitemap.xml` are checked into the repository.
- Standard workflow: change sources, run `python -X utf8 build.py`, then `python -X utf8 lint.py`, and review the diff. UTF-8 mode matters because the builder writes Unicode using the interpreter's default encoding.
- Python 3.13.15 was installed on 2026-10-09 at `%LOCALAPPDATA%\Programs\Python\Python313\python.exe`. The project launcher uses this path, so an older shell's PATH or WindowsApps alias does not block builds.
- Codex CLI 0.160.1 is installed and responds to `codex --version`. Its local help supports `codex doctor`, `codex update`, `codex resume --last`, and project selection with `-C`.

## Launch configuration and source accuracy

- Observed in local source on 2026-10-09: `_data.py` has `INDEXABLE = True` and `BASE = "https://anointed.ink"`; `CNAME` contains `anointed.ink`; `robots.txt` allows crawling.
- The checked-out commit was `14cbef8`, titled "Go live: indexable (robots allow + sitemap, index,follow on every page)". Recheck Git for the current revision in future chats.
- These observations establish repository configuration, not an independent check of live hosting, DNS, or HTTPS.
- `README.md` launch section was corrected on 2026-10-09 to match the current public/indexable configuration. Live deployment settings still need separate verification.
- Business values and reviews in `_data.py` refer to verification dated 2026-09-24. Treat changing information as dated, not newly verified.
- The source references `../CLIENT-BRIEF.md` and `../photos/process.py`; neither exists in this workspace's parent directory as checked on 2026-10-09. Do not invent their contents.
- Preserve photo attribution, disclosures for work not tattooed at Anointed Ink, and `noPromo` restrictions. Follow the repository's existing content gate rather than treating its legal commentary as freshly verified advice.

## Environment limitations

- This session's terminal network access to GitHub was blocked by its proxy. The user's own PowerShell successfully authenticated and fetched the repository.
- This session could read Git metadata but writes to `.git/config`, `.git/index.lock`, and the user's `.gitconfig` were denied. The user completed remote setup and checkout in their own PowerShell.
- No controllable browser surfaces were available during connection setup.
- Recheck these limits when needed; they may differ in future sessions. Do not retry the same blocked action repeatedly or bypass the restrictions.

## Current work

- GitHub connection and initial checkout are complete.
- Continuity notes, `SETUP.md`, `manage.py`, and `project.cmd` are ready locally. The launcher supports check, preview, codex, resume, doctor, and finish-setup commands.
- `.github/workflows/check-site.yml` builds, lints, and checks generated files for source drift on main pushes and pull requests. It is not active on GitHub until pushed and is not a deployment workflow or required branch rule.
- Build and lint passed for all 32 pages, with zero failures and two existing warnings for sleeve-session wording. Rebuilding produced no tracked generated-file changes. Local preview returned HTTP 200 with expected site content.
- The user authorized implementing the recommended setup, including committing and pushing the setup notes. Staging remains blocked by this chat's filesystem restrictions. `.\project.cmd finish-setup` completes the exact-file commit/push and reads Pages settings in the user's own PowerShell.
- GitHub Pages API inspection was blocked by the restricted terminal network; the publishing branch/path is unverified.
- Codex remains 0.160.1. Built-in update did not recognize the installation method; WinGet offered 0.161.0 but failed to replace `codex-code-mode-host.exe` with access denied. Close Codex sessions/apps before retrying the WinGet update in a separate normal PowerShell.
- `codex doctor` in the restricted chat reported a memory-database integrity-check failure and connectivity/permission warnings. Recheck outside this sandbox before diagnosing corruption. No memory database or security controls were changed.
- The user's first finish-setup run passed build/lint and staged the setup files, but commit failed because Git user.name/user.email are missing. No push occurred. The launcher now supports retrying those staged files and checks identity before staging.
- User-approved commit identity for this repository: `Nestor <anointed.ink29@gmail.com>`. Setting the local Git configuration was blocked by this chat's `.git/config` write restrictions; apply it in the user's normal PowerShell, then rerun finish-setup.
