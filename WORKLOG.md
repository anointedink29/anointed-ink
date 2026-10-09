# Project work log

Keep entries concise and append new work below. Store durable context in `MEMORY.md`.

## 2026-10-09: GitHub connection and project continuity

- Request: connect GitHub and add persistent project notes for future chats.
- Completed: installed Git for Windows; user completed GitHub CLI authentication and credential setup, added `origin`, fetched the repository, and checked out `main` tracking `origin/main`.
- Verified: remote URL, tracking branch, and checked-out site files. Only the pre-existing `debug.log` was untracked before memory files were added.
- Added: `AGENTS.md` with startup and maintenance instructions, `MEMORY.md` with durable context, and this work log.
- Inspected: README, source structure, build workflow, content gate, launch settings, and environment limitations. The README launch section is older than the current configuration.
- Validation: documentation-only changes; no site rebuild required. No runtime or live deployment validation performed.
- Outstanding: continuity files are local and have not been committed or pushed. No additional site work has been requested.

## 2026-10-09: Local tooling assessment

- Request: identify useful setup for managing this project with Codex CLI.
- Verified: Codex CLI 0.160.1 and ripgrep are installed; Python is missing. Node/npm were not found in this tool session's PATH; the site's core build uses Python's standard library.
- Consulted current official Codex CLI, Windows sandbox, and project instruction documentation.
- Updated memory with confirmed tool availability. No software installations or configuration changes performed during this assessment.
- Next priorities: install Python, verify build/lint locally, commit continuity notes, and check CLI diagnostics and the deployment workflow.

## 2026-10-09: Implement project tooling setup

- Request: implement the recommended local tooling, preview, notes backup, and publishing workflow.
- Installed Python 3.13.15 using WinGet. Built all 32 pages; lint passed with zero failures and two existing sleeve-session warnings. Generated tracked files did not change.
- Added `project.cmd` and `manage.py` for check, preview, Codex start/resume, diagnostics, and finishing the setup commit/push from normal PowerShell.
- Added the build/lint/source-drift workflow and `SETUP.md`; corrected the README's obsolete preview status. Updated project instructions and memory.
- Verified launcher check command, Python syntax, diff whitespace, generated-file consistency, and loopback preview HTTP 200 with expected site content. Preview started in a terminal session during verification; run the launcher again if that session is no longer available.
- Ran Codex diagnostics. Database integrity and connectivity findings require a normal-PowerShell recheck. Built-in update failed to detect installation; WinGet update failed with access denied replacing a helper. CLI version still 0.160.1.
- Git staging failed on `.git/index.lock` permissions; Pages API access failed on the restricted proxy. No commits, pushes, or deployment-setting changes completed here.
- Remaining user step: run `.\project.cmd finish-setup` in normal PowerShell; close Codex and retry the WinGet update separately. GitHub CI activation and Pages configuration verification remain pending until those external steps succeed.

## 2026-10-09: Resume setup after missing Git identity

- User's normal-PowerShell build/lint passed; staging succeeded but commit stopped because Git author identity is not configured. No push was completed.
- Fixed finish-setup to accept already staged setup files while rejecting unrelated staged files, and to check author identity before staging.
- Commit name/email need user input. The existing setup files are still staged; rerunning the corrected command will refresh them before committing.
- Verified with mocked Git operations: setup-file retry proceeds; unrelated staged files are rejected; missing identity stops before checks/staging. No real commit/push was performed by these checks.
- User supplied the commit identity `Nestor <anointed.ink29@gmail.com>`. Attempt to set repository-local identity was blocked on `.git/config` permissions. Recorded the approved identity; configuration and commit/push remain pending in normal PowerShell.
