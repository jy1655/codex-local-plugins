param(
    [Parameter(Mandatory = $true)]
    [string]$GitUrl
)

$ErrorActionPreference = "Stop"
$TempRoot = Join-Path ([System.IO.Path]::GetTempPath()) ("codex-env-sync-" + [System.Guid]::NewGuid().ToString())

try {
    New-Item -ItemType Directory -Path $TempRoot | Out-Null
    git clone --depth 1 $GitUrl (Join-Path $TempRoot "repo") | Out-Null
    $Python = Get-Command python -ErrorAction SilentlyContinue
    if (-not $Python) {
        $Python = Get-Command python3 -ErrorAction SilentlyContinue
    }
    if (-not $Python) {
        throw "python or python3 is required"
    }
    Push-Location (Join-Path $TempRoot "repo")
    try {
        & $Python.Source -m codex_env_sync.cli apply --repo-root . --snapshot
        if ($LASTEXITCODE -ne 0) {
            throw "codex-env-sync apply failed with exit code $LASTEXITCODE"
        }
    }
    finally {
        Pop-Location
    }
}
finally {
    if (Test-Path $TempRoot) {
        Remove-Item -Recurse -Force $TempRoot
    }
}
