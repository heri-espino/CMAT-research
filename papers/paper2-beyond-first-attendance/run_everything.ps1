# Run the entire Paper 2 analysis suite and publish reviewed aggregate results.
# Works on Windows PowerShell 5.1+/PowerShell 7 with the cmat-research Conda env.
[CmdletBinding()]
param(
    [string]$Materias = "",
    [string]$Asesorias = "",
    [switch]$CheckOnly,
    [switch]$NoPublish,
    [switch]$BuildPublications,
    [switch]$RequireHistoricalCohort
)
Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

$repo = (Resolve-Path -LiteralPath (Join-Path $PSScriptRoot "..\..")).Path
$runner = Join-Path $PSScriptRoot "run_all.py"
Set-Location -LiteralPath $repo
$branch = (git branch --show-current).Trim()
if ($LASTEXITCODE -ne 0 -or $branch -ne "paper/paper2-beyond-first-attendance") {
    throw "Checkout paper/paper2-beyond-first-attendance first; this script never force-switches your working tree."
}

Write-Host "Ensuring the pinned Python 3.14 analysis package is installed..."
python -m pip install -e "./cmat_analysis[dev]"
if ($LASTEXITCODE -ne 0) {
    throw "Python environment installation failed. Activate conda env cmat-research and retry."
}

$runArgs = @($runner)
if ($Materias -ne "" -or $Asesorias -ne "") {
    if ($Materias -eq "" -or $Asesorias -eq "") {
        throw "Provide both -Materias and -Asesorias or neither."
    }
    $runArgs += @("--materias", $Materias, "--asesorias", $Asesorias)
}
if ($CheckOnly) {
    $runArgs += "--check"
} else {
    if (-not $NoPublish) { $runArgs += "--publish" }
    if ($BuildPublications) { $runArgs += "--build-publications" }
    if ($RequireHistoricalCohort) { $runArgs += "--require-historical-cohort" }
}
Write-Host "Running canonical Paper 2 orchestrator..."
& python @runArgs
if ($LASTEXITCODE -ne 0) {
    throw "Paper 2 suite was not fully successful. Nothing should be presented as a completed full rerun. See local execution log."
}
Write-Host "Paper 2 suite completed. See papers/paper2-beyond-first-attendance/results/provenance/latest_full_rerun.json."
