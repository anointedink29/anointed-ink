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
- Codex CLI 0.161.0 is installed and responds to `codex --version`, verified on 2026-10-09 after the queued WinGet update succeeded. Its local help supports `codex doctor`, `codex update`, `codex resume --last`, and project selection with `-C`.

## Launch configuration and source accuracy

- Observed in local source on 2026-10-09: `_data.py` has `INDEXABLE = True` and `BASE = "https://anointed.ink"`; `CNAME` contains `anointed.ink`; `robots.txt` allows crawling.
- The checked-out commit was `14cbef8`, titled "Go live: indexable (robots allow + sitemap, index,follow on every page)". Recheck Git for the current revision in future chats.
- Live hosting was independently checked on 2026-10-09: GitHub Pages reports built from `main` at `/`, custom domain `anointed.ink`, HTTPS enforced, and an approved certificate for `anointed.ink` and `www.anointed.ink` expiring 2026-12-30. The HTTPS homepage returned HTTP 200 with the expected Anointed Ink name.
- `README.md` launch section was corrected on 2026-10-09 to match the current public/indexable configuration. Live deployment settings were subsequently verified as recorded above.
- Business values and reviews in `_data.py` refer to verification dated 2026-09-24. Treat changing information as dated, not newly verified.
- The source references `../CLIENT-BRIEF.md` and `../photos/process.py`; neither exists in this workspace's parent directory as checked on 2026-10-09. Do not invent their contents.
- Preserve photo attribution, disclosures for work not tattooed at Anointed Ink, and `noPromo` restrictions. Follow the repository's existing content gate rather than treating its legal commentary as freshly verified advice.

## Environment limitations

- Sandboxed terminal network access to GitHub is blocked by its proxy. On 2026-10-09, an approved read-only GitHub CLI API check outside the sandbox succeeded for `anointedink29/anointed-ink`, confirming pull, push, maintain, triage, and admin permissions. The repository is public and its default branch is `main`.
- This session could read Git metadata but writes to `.git/config`, `.git/index.lock`, and the user's `.gitconfig` were denied. The user completed remote setup and checkout in their own PowerShell.
- No controllable browser surfaces were available during connection setup.
- Recheck these limits when needed; they may differ in future sessions. Do not retry the same blocked action repeatedly or bypass the restrictions.
- GitHub CLI authentication is working. This working session supports approved read-only commands outside its sandbox; Actions, Pages, live HTTPS, and Codex diagnostics succeeded through that route on 2026-10-09. Another restricted chat did not support escalation. Follow each session's actual permission policy; do not confuse restrictions with an invalid login or repeat authentication.
- The GitHub plugin was still reported as not installed in this chat's last check. It is optional for the verified CLI workflow; do not make installation a prerequisite for CLI-based project management.

## Current work

- GitHub connection and initial checkout are complete.
- Continuity notes, `SETUP.md`, `manage.py`, and `project.cmd` were committed and pushed in `fbcbeef` on 2026-10-09. Local HEAD and origin/main matched when verified. The launcher supports check, preview, codex, resume, doctor, and finish-setup commands.
- `.github/workflows/check-site.yml` was included in the pushed setup commit. It builds, lints, and checks generated files for source drift on main pushes and pull requests. Verified successful run for `fbcbeef`: https://github.com/anointedink29/anointed-ink/actions/runs/37978510909. It is not a deployment workflow or required branch rule.
- Build and lint passed for all 32 pages, with zero failures and two existing warnings for sleeve-session wording. Rebuilding produced no tracked generated-file changes. Local preview returned HTTP 200 with expected site content.
- The user completed finish-setup in normal PowerShell. Verified commit `fbcbeef`, author identity, and main matching origin/main. This chat's Git write restrictions remain; normal setup no longer needs repeating.
- GitHub Pages publishes from `main` at the repository root. Verified successful deployment of `fbcbeef`: https://github.com/anointedink29/anointed-ink/actions/runs/37978509145. Pages status is built; custom domain and HTTPS were verified on 2026-10-09.
- Codex CLI update to 0.161.0 succeeded through the queued WinGet worker on 2026-10-09 at 14:34 CDT, verified by its success log, `codex --version`, and project launcher doctor. Doctor still reports CLI 0.162.0 available. Desktop version 26.1002.7124.0 remains installed, with build 26.1007.2314.0 reported available; its update remains pending distribution availability.
- Approved outside-sandbox `codex doctor --json` and `.\project.cmd doctor` passed all existing database integrity checks, auth/configuration, provider reachability, and WebSocket handshake on 2026-10-09. The previous restricted-chat memory-database failure did not reproduce. The launcher resolves the stale-shell Git PATH warning. Final launcher report: 21 ok, 1 idle, 3 warnings, 0 failures. Remaining warnings concern optional node_repl environment (`CODEX_WINDOWS_REGISTERED_CORE` missing), Dev Drive performance advice, and unverified Defender exclusions; no recent security enforcement was found. No database repairs or security changes were made.
- Repository-local Git identity is configured and verified: `Nestor <anointed.ink29@gmail.com>`. The earlier missing-identity issue is resolved. The launcher supports retrying staged setup files and checks identity before staging.

## Next chat handoff

- GitHub connection, Git identity, Python installation, repository checkout, and initial setup commit/push are complete. Do not restart setup.
- Use the working Codex session's GitHub CLI access. Follow that session's actual permission policy; only request approved outside-sandbox execution where supported, and never bypass managed restrictions.
- Actions, Pages configuration/deployment, live HTTPS, and outside-sandbox Codex health checks are complete as recorded above. Do not repeat these as unresolved setup work.
- Codex CLI update is verified complete at 0.161.0; doctor advertises a further update to 0.162.0. Desktop update remains pending. Latest project launcher health diagnostics passed: 22 ok, 1 idle, 2 advisory warnings, 0 failures. Do not delete memory databases or change security protections as a routine fix.
- Read current Git status before changes. The user authorized a local commit of the reviewed tooling and continuity notes on 2026-10-09. This request does not include pushing or publishing; keep debug.log out of commits.
- No new site feature or design change has been requested. Ask for the user's next site task once outstanding setup verification is handled.

## Codex maintenance requested on 2026-10-09

- User authorized addressing Codex updates and diagnostic warnings. `manage.py` now disables the app-hosted `node_repl` bridge only for CLI invocations lacking `CODEX_WINDOWS_REGISTERED_CORE`; shared app configuration is untouched. Project launcher doctor verifies the MCP warning is gone: 22 ok, 1 idle, 2 warnings, 0 failures. Direct CLI doctor may still report the shared configuration warning.
- Added `update-codex.ps1`: checks for running processes in the WinGet Codex package, waits optionally up to one hour, upgrades through WinGet, and logs version verification. The hidden worker completed successfully on 2026-10-09 at 14:34 CDT; `%TEMP%\anointed-codex-update\cli-update.log` confirms installation and version verification at 0.161.0. It never kills processes. A subsequent project launcher doctor check passed with 22 ok, 1 idle, 2 warnings, and 0 failures; auth, connectivity, database integrity, and installation consistency passed. Doctor still advertises 0.162.0.
- Desktop update is blocked by distribution availability: Store reports no upgrade; the official signed download linked in OpenAI documentation is 26.930.7945.0, older than installed 26.1002.7124.0. Windows rejected it as a downgrade. No desktop update was installed.
- Administrator read-only Defender inspection succeeded: antivirus and real-time protection enabled, no exclusions, Controlled Folder Access off. No recent Codex blocking was found; no security changes were made. Doctor's generic unverified-exclusions advisory remains.
- Dev Drive requires administrator setup, at least 50 GB, and relocating the project outside OneDrive. A user preference question was sent; no choice had arrived when these notes were written. Preserve the current project location until the user chooses migration.
- Validation: build and lint passed for all 32 pages with the two existing content warnings; update script syntax and diff whitespace checks passed. No site content changed, commit, or push performed.

## Tooling review on 2026-10-09

- Reviewed `manage.py`, `update-codex.ps1`, setup guidance, and accumulated continuity notes for the user-requested local commit. The launcher override affects only invocations without desktop host context; the updater waits for package processes without terminating them.
- Re-ran `.\project.cmd check`: 32 pages passed, zero failures, two existing sleeve-session warnings, and no generated-file changes. PowerShell parser and diff whitespace checks passed. Latest launcher doctor verification remains 22 ok, 1 idle, 2 warnings, zero failures.
