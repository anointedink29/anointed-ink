"""Project commands using Python's standard library. Run project.cmd --help."""
import argparse
import os
from pathlib import Path
import shutil
import subprocess
import sys

ROOT = Path(__file__).resolve().parent
SETUP_FILES = [
    "AGENTS.md", "MEMORY.md", "WORKLOG.md", "SETUP.md", "README.md",
    "project.cmd", "manage.py", ".github/workflows/check-site.yml",
]


def run(*args):
    subprocess.run(args, cwd=ROOT, check=True)


def capture(*args):
    return subprocess.check_output(args, cwd=ROOT, text=True).strip()


def tool(name):
    path = shutil.which(name)
    if not path and name == "git" and os.name == "nt":
        candidate = Path("C:/Program Files/Git/cmd/git.exe")
        if candidate.exists():
            path = str(candidate)
    if not path:
        raise RuntimeError(f"{name} is unavailable. Reopen PowerShell after installing it.")
    return path


def check():
    run(sys.executable, "-X", "utf8", "build.py")
    run(sys.executable, "-X", "utf8", "lint.py")


def codex_command():
    command = [tool("codex")]
    # The desktop browser bridge requires context supplied by its host app.
    # Standalone CLI sessions cannot start it without that context. Keep the
    # shared app configuration intact and override only this invocation.
    if os.name == "nt" and not os.environ.get("CODEX_WINDOWS_REGISTERED_CORE"):
        command.extend(["-c", "mcp_servers.node_repl.enabled=false"])
    return command


def finish_setup():
    git = tool("git")
    expected = "https://github.com/anointedink29/anointed-ink.git"
    if capture(git, "remote", "get-url", "origin") != expected:
        raise RuntimeError("Origin does not match the expected Anointed Ink repository.")
    if capture(git, "branch", "--show-current") != "main":
        raise RuntimeError("Run this setup command on main.")
    staged = set(capture(git, "diff", "--cached", "--name-only").splitlines())
    unrelated = staged - set(SETUP_FILES)
    if unrelated:
        raise RuntimeError("Unrelated files are staged. Review them before finishing setup: "
                           + ", ".join(sorted(unrelated)))
    try:
        capture(git, "var", "GIT_AUTHOR_IDENT")
    except subprocess.CalledProcessError:
        raise RuntimeError("Set your Git user.name and user.email, then rerun finish-setup. "
                           "Already staged setup files can be resumed safely.") from None
    check()
    # Exact file list keeps unrelated files, including debug.log, out of the commit.
    run(git, "add", "--", *SETUP_FILES)
    if capture(git, "diff", "--cached", "--name-only"):
        run(git, "commit", "-m", "Set up project memory, local commands, and site checks")
    run(git, "push", "origin", "main")
    print("Project setup saved to GitHub.")
    run(tool("gh"), "api", "repos/anointedink29/anointed-ink/pages", "--jq",
        "{branch: .source.branch, path: .source.path, build_type: .build_type, cname: .cname, status: .status}")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("command", choices=["check", "preview", "codex", "resume", "doctor", "finish-setup"])
    parser.add_argument("--port", type=int, default=8000, help="Local preview port (default: 8000)")
    args = parser.parse_args()
    os.chdir(ROOT)
    if args.command == "check":
        check()
    elif args.command == "preview":
        check()
        print(f"Preview: http://127.0.0.1:{args.port} (Ctrl+C to stop)", flush=True)
        run(sys.executable, "-X", "utf8", "-m", "http.server", str(args.port), "--bind", "127.0.0.1")
    elif args.command == "codex":
        run(*codex_command(), "-C", str(ROOT))
    elif args.command == "resume":
        run(*codex_command(), "-C", str(ROOT), "resume", "--last")
    elif args.command == "doctor":
        run(*codex_command(), "doctor")
    else:
        finish_setup()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        pass
    except (subprocess.CalledProcessError, RuntimeError) as error:
        print(f"Stopped: {error}", file=sys.stderr)
        sys.exit(1)
