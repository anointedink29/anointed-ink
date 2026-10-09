param([switch]$WaitForExit)

$ErrorActionPreference = 'Stop'
$updateFolder = Join-Path $env:TEMP 'anointed-codex-update'
New-Item -ItemType Directory -Path $updateFolder -Force | Out-Null
$updateLog = Join-Path $updateFolder 'cli-update.log'
$packageFolder = Join-Path $env:LOCALAPPDATA 'Microsoft\WinGet\Packages\OpenAI.Codex_Microsoft.Winget.Source_8wekyb3d8bbwe'
$deadline = (Get-Date).AddHours(1)

function Get-RunningPackageProcesses {
    Get-CimInstance Win32_Process | Where-Object {
        $_.ExecutablePath -and
        $_.ExecutablePath.StartsWith($packageFolder + '\', [StringComparison]::OrdinalIgnoreCase)
    }
}

try {
    "$(Get-Date -Format o) Requested CLI update." | Set-Content -LiteralPath $updateLog
    while (Get-RunningPackageProcesses) {
        if (-not $WaitForExit) {
            throw 'Close Codex CLI sessions first, or run this script with -WaitForExit.'
        }
        if ((Get-Date) -gt $deadline) {
            throw 'Timed out waiting for Codex to close; no update was attempted.'
        }
        Start-Sleep -Seconds 15
    }
    "$(Get-Date -Format o) Codex closed; updating through WinGet." | Add-Content -LiteralPath $updateLog
    & winget.exe upgrade --id OpenAI.Codex --exact --source winget --silent --disable-interactivity --accept-source-agreements --accept-package-agreements 2>&1 |
        Tee-Object -FilePath $updateLog -Append
    if ($LASTEXITCODE -ne 0) {
        throw "WinGet returned $LASTEXITCODE. Review $updateLog."
    }
    & codex --version 2>&1 | Tee-Object -FilePath $updateLog -Append
    if ($LASTEXITCODE -ne 0) { throw 'Codex version verification failed.' }
    "$(Get-Date -Format o) CLI update and version check succeeded." | Add-Content -LiteralPath $updateLog
} catch {
    "$(Get-Date -Format o) Stopped: $($_.Exception.Message)" | Add-Content -LiteralPath $updateLog
    Write-Error $_
    exit 1
}
