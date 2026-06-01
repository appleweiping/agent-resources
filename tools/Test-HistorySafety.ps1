param(
    [string]$Path = (Split-Path -Parent (Split-Path -Parent $MyInvocation.MyCommand.Path))
)

$ErrorActionPreference = "Stop"
$resolved = (Resolve-Path -LiteralPath $Path).Path
$pattern = 'sk-proj-[A-Za-z0-9_-]{20,}|sk-ant-[A-Za-z0-9_-]{20,}|sk-[A-Za-z0-9]{32,}|ghp_[A-Za-z0-9_]{20,}|github_pat_[A-Za-z0-9_]{20,}|-----BEGIN (RSA |OPENSSH |EC |DSA )?PRIVATE KEY-----'
$allowedPlaceholders = @(
    "ghp_your_github_token",
    "ghp_your_new_github_token",
    "github_pat_your_github_token",
    "github_pat_your_new_github_token"
)

Push-Location $resolved
try {
    git rev-parse --is-inside-work-tree *> $null
    if ($LASTEXITCODE -ne 0) {
        throw "Not a git repository: $resolved"
    }

    $raw = @(git log -p --all -G $pattern -- . 2>$null)
    $findings = @()
    foreach ($line in $raw) {
        foreach ($match in [regex]::Matches($line, $pattern)) {
            $value = $match.Value
            if ($allowedPlaceholders -contains $value) {
                continue
            }
            $redacted = if ($value.Length -gt 12) {
                $value.Substring(0, 8) + "..." + $value.Substring($value.Length - 4)
            } else {
                "[redacted]"
            }
            $findings += $line.Replace($value, $redacted)
        }
    }

    if ($findings.Count -gt 0) {
        $findings | Select-Object -First 80
        throw "History safety scan failed in $resolved"
    }

    Write-Host "History safety scan passed: $resolved" -ForegroundColor Green
} finally {
    Pop-Location
}
