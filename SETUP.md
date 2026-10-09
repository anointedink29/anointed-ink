# Managing this project

Run commands in normal PowerShell from this folder:

```powershell
cd "C:\Users\anoin\OneDrive\Desktop\anointed ink ai project"
.\project.cmd codex
```

The launcher uses the project folder, finds the installed Python 3.13 executable,
and adds Git to its own PATH. No permanent PowerShell profile changes are needed.

| Command | Purpose |
| --- | --- |
| `.\project.cmd codex` | Start Codex in this project |
| `.\project.cmd resume` | Resume the most recent Codex CLI session in this project |
| `.\project.cmd check` | Build the site and run the content/SEO gate |
| `.\project.cmd preview` | Build/check, then serve locally at http://127.0.0.1:8000 |
| `.\project.cmd doctor` | Run Codex health diagnostics |
| `.\project.cmd finish-setup` | Check, commit only setup files, push main, and inspect Pages settings |

Preview runs in the foreground; press Ctrl+C to stop. For another port, use
`.\project.cmd preview --port 8001`. The site's external analytics scripts can
still load during local preview.

The launcher skips the desktop-only browser bridge in standalone CLI sessions
when `CODEX_WINDOWS_REGISTERED_CORE` is absent. This removes its startup warning
without editing shared desktop configuration. App-hosted sessions with the
required context keep the bridge enabled.

To update the WinGet CLI after closing it, run
`powershell -NoProfile -File .\update-codex.ps1` from normal PowerShell.
With `-WaitForExit`, it waits up to
one hour for that installed CLI and its helpers to exit, then updates and checks
the version. It never terminates a session. Results are written to
`%TEMP%\anointed-codex-update\cli-update.log`.

## Finish this setup

Python 3.13.15 was installed and the 32-page build passed on 2026-10-09.
The linter reports two existing warnings about sleeve-session wording and no failures.

The current chat cannot write Git's index or reach GitHub through its restricted
terminal network. If setup has not yet been pushed, run:

```powershell
.\project.cmd finish-setup
```

This stages an explicit list of setup files, leaving `debug.log` and unrelated
changes out. It allows retrying with setup files already staged, but refuses
to proceed if unrelated files are staged. It checks commit identity before staging. A push
can trigger the repository's existing publishing behavior.
If Git reports missing author identity, configure your chosen commit name and
email yourself; this project does not infer an identity from your account name.
If the push is rejected, ask Codex to inspect divergence rather than force pushing.

The Pages API output establishes which branch/path or Actions workflow publishes
the site. Until that call succeeds, deployment settings remain unverified.
The new `Check site` workflow validates pushes and pull requests; it does not
deploy the site or block an existing branch-based Pages deployment. A required
check/branch rule must be configured separately if desired.

## Codex health and updates

Codex's built-in updater did not recognize the WinGet installation. A WinGet
upgrade attempt could not replace `codex-code-mode-host.exe`. Close Codex apps
and sessions, then run from a separate PowerShell window:

```powershell
winget upgrade --id OpenAI.Codex --exact --source winget
codex --version
codex doctor
```

Approved diagnostics outside the sandbox passed connectivity and all existing
database integrity checks on 2026-10-09. The earlier restricted-chat failure for
`memories_1.sqlite` did not reproduce. The project launcher now reports two
advisory warnings (Dev Drive and Defender) with zero failures. Administrator
inspection confirmed Defender and real-time protection are enabled, no
exclusions are set, and Controlled Folder Access is disabled. No recent blocking
was detected. Do not disable Defender or the sandbox based only on these notes.

The desktop Store update check found no upgrade on 2026-10-09. OpenAI's linked
signed MSIX was version 26.930.7945.0, older than installed 26.1002.7124.0;
Windows refused the downgrade. Doctor reports a newer build available, but its
installation remains pending until a current package is distributed.

## Daily workflow

Read project memory, state the outcome and constraints, edit Python sources,
run the checks, preview visual changes, inspect `git diff`, and update the notes.
For larger site changes, use a branch and pull request:

```powershell
git switch -c improve-booking-page
# Work, check, preview, then commit the intended files.
git push -u origin improve-booking-page
gh pr create
```

`AGENTS.md` directs new Codex sessions to read `MEMORY.md` and `WORKLOG.md`.
These are project context, not global chat memory. Keep notes concise and never
store credentials. The client brief and original photo-processing folder named
in older documentation are not available in this checkout.

References: [Codex project instructions](https://learn.chatgpt.com/docs/agent-configuration/agents-md),
[Windows sandbox](https://learn.chatgpt.com/docs/windows/windows-sandbox),
[GitHub Python checks](https://docs.github.com/en/actions/tutorials/build-and-test-code/python).
