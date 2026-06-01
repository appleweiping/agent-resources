# Public-safe smoke test for intent-based skill routing metadata.
# It does not call an LLM; it checks that the local index and skill metadata
# expose enough intent words for agents to choose skills without exact names.

$ErrorActionPreference = "Stop"

$root = Split-Path -Parent (Split-Path -Parent $MyInvocation.MyCommand.Path)
$index = Join-Path $root "SKILL-INDEX.md"
if (-not (Test-Path $index)) {
    throw "Missing SKILL-INDEX.md"
}

$text = Get-Content -LiteralPath $index -Raw
$skillFiles = Get-ChildItem -Path (Join-Path $root "skills") -Recurse -Filter "SKILL.md" -File -ErrorAction SilentlyContinue
$frontmatter = foreach ($file in $skillFiles) {
    $content = Get-Content -LiteralPath $file.FullName -Raw -ErrorAction SilentlyContinue
    if ($content -match "(?s)^---\s*(.*?)\s*---") { $Matches[1] }
}
$haystack = ($text + "`n" + ($frontmatter -join "`n")).ToLowerInvariant()

$checks = @(
    @{ Intent = "readme"; Terms = @("readme", "documentation", "docs") },
    @{ Intent = "agent architecture"; Terms = @("agent", "architecture", "mcp", "memory") },
    @{ Intent = "research audit"; Terms = @("research", "paper", "citation", "audit") },
    @{ Intent = "infrastructure"; Terms = @("infrastructure", "health", "launcher", "config") },
    @{ Intent = "frontend"; Terms = @("frontend", "design", "ui") }
)

$failed = @()
foreach ($check in $checks) {
    $hits = @($check.Terms | Where-Object { $haystack.Contains($_) })
    if ($hits.Count -eq 0) {
        $failed += $check.Intent
        Write-Host "FAIL $($check.Intent): no trigger terms found" -ForegroundColor Red
    } else {
        Write-Host "OK   $($check.Intent): $($hits -join ', ')" -ForegroundColor Green
    }
}

if ($failed.Count -gt 0) {
    throw "Implicit skill routing smoke test failed: $($failed -join ', ')"
}

Write-Host "Implicit skill routing metadata smoke test passed." -ForegroundColor Cyan
