# Publish already-generated CMAT AGGREGATE research outputs. No raw data needed.
# Safe to resume after an interrupted previous attempt.
[CmdletBinding()]
param(
    [Parameter(Mandatory = $true)][string]$Source,
    [switch]$IncludeHistoricalFigures,
    [switch]$Publish
)

Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

function Assert-Git([string]$Description) {
    if ($LASTEXITCODE -ne 0) {
        throw "$Description failed (exit code $LASTEXITCODE). No push was performed."
    }
}

$repo = (Resolve-Path -LiteralPath (Join-Path $PSScriptRoot "..")).Path
$sourceRoot = (Resolve-Path -LiteralPath $Source).Path
$branch = "research/paper21-shapley-predictive-importance"
Set-Location -LiteralPath $repo

$currentBranch = (git branch --show-current).Trim()
Assert-Git "Checking branch"
if ($currentBranch -ne $branch) {
    throw "Expected branch $branch in the separate publication checkout; found $currentBranch."
}
if ($repo -eq $sourceRoot) {
    throw "Use the separate publication checkout. The original data checkout must remain untouched."
}

# Copy EXACTLY the already-generated aggregate outputs. The original raw
# spreadsheets, controlled tables and individual-level data are never copied.
$files = @(
    "notes/22_FOLLOWUP_QUESTIONS_RESULTS.md",
    "results/paper21/tables/followup_questions/degree_professor_period_overlap.csv",
    "results/paper21/tables/followup_questions/two_part_attendance_z_pass.csv",
    "results/paper21/tables/followup_questions/observed_numeric_grade_quantiles.csv",
    "results/paper21/tables/followup_questions/numeric_vs_administrative_composition.csv",
    "notes/24_ATTENDANCE_CURVE_RESULTS.md",
    "results/paper21/tables/attendance_curves/unadjusted_means_cluster_ci.csv",
    "results/paper21/tables/attendance_curves/model_comparison_in_sample.csv",
    "results/paper21/tables/attendance_curves/adjusted_curves_cluster_ci.csv",
    "results/paper21/tables/attendance_curves/adjacent_differences_holm.csv",
    "results/paper21/tables/attendance_curves/group_heldout_shape_cv.csv",
    "results/paper21/figures/attendance_curves/imputed_z_attendance_curve.png",
    "results/paper21/figures/attendance_curves/pass_lpm_attendance_curve.png",
    "results/paper21/figures/attendance_curves/numeric_only_z_attendance_curve.png",
    "results/paper21/figures/attendance_curves/observed_numeric_grade_attendance_curve.png"
)
$stage = New-Object System.Collections.Generic.List[string]
$missing = New-Object System.Collections.Generic.List[string]

foreach ($relative in $files) {
    $from = Join-Path $sourceRoot $relative
    $to = Join-Path $repo $relative
    if (Test-Path -LiteralPath $from -PathType Leaf) {
        New-Item -ItemType Directory -Path (Split-Path -Parent $to) -Force | Out-Null
        Copy-Item -LiteralPath $from -Destination $to -Force
    }
    if (Test-Path -LiteralPath $to -PathType Leaf) {
        $stage.Add($relative)
    } else {
        $missing.Add($relative)
    }
}

if ($IncludeHistoricalFigures) {
    git lfs install
    Assert-Git "Git LFS initialization"
    $relDir = "brainstorm/shared/historical_outputs/study/figures"
    $sourceDir = Join-Path $sourceRoot $relDir
    $targetDir = Join-Path $repo $relDir
    if (-not (Test-Path -LiteralPath $sourceDir -PathType Container)) {
        throw "Original historical figure directory not found: $sourceDir"
    }
    New-Item -ItemType Directory -Path $targetDir -Force | Out-Null
    $images = @(Get-ChildItem -LiteralPath $sourceDir -File -Filter "*.png" |
        Where-Object { $_.Name -match '^\d\d_.*\.png$' })
    if ($images.Count -ne 16) {
        throw "Expected 16 historical aggregate PNG figures, found $($images.Count)."
    }
    foreach ($file in $images) {
        $stream = [System.IO.File]::OpenRead($file.FullName)
        try {
            $header = [byte[]]::new(8)
            $read = $stream.Read($header, 0, 8)
            if ($read -ne 8 -or [System.BitConverter]::ToString($header) -ne "89-50-4E-47-0D-0A-1A-0A") {
                throw "Historical PNG is not an image: $($file.FullName)."
            }
        } finally {
            $stream.Dispose()
        }
        Copy-Item -LiteralPath $file.FullName -Destination (Join-Path $targetDir $file.Name) -Force
        $stage.Add("$relDir/$($file.Name)")
    }
}

Write-Host "Known aggregate files present: $($stage.Count)"
if ($missing.Count -gt 0) {
    Write-Host "Not generated yet (SKIPPED, not a publication failure):"
    foreach ($relative in $missing) { Write-Host "  $relative" }
}
if ($stage.Count -eq 0) {
    throw "No approved aggregate artifacts found. Nothing staged or pushed."
}

# Reject unexpected previously staged paths. This is a public repository.
$stagedBefore = @(git diff --cached --name-only)
Assert-Git "Inspecting staged changes"
foreach ($path in $stagedBefore) {
    if ($path -notin $stage.ToArray()) {
        throw "Unreviewed staged path: $path. Unstage it before publication."
    }
}

# Stage by exact filenames, never 'git add .' or broad directory patterns.
git add -- $stage.ToArray()
Assert-Git "Staging known aggregate files"
$stagedAfter = @(git diff --cached --name-only)
Assert-Git "Reading staged changes"
foreach ($path in $stagedAfter) {
    if ($path -notin $stage.ToArray()) {
        throw "Unexpected staged file: $path. Nothing committed."
    }
}
if ($IncludeHistoricalFigures) {
    git lfs status
    Assert-Git "Checking LFS status"
}
git diff --cached --stat
Assert-Git "Showing commit summary"

if ($stagedAfter.Count -eq 0) {
    Write-Host "All available approved outputs are already committed locally."
    if ($Publish) {
        git push origin $branch
        Assert-Git "Pushing branch"
        Write-Host "GitHub branch updated."
    }
    exit 0
}

if (-not $Publish) {
    Write-Host "Files staged but not pushed. Inspect them, then commit and push manually."
    exit 0
}

Write-Warning "This GitHub repository is PUBLIC. Only known aggregate outputs are staged."
$choice = Read-Host "Type PUBLISH to commit and push"
if ($choice -cne "PUBLISH") {
    throw "Not confirmed. Files remain staged, no commit or push performed."
}
git commit -m "Publish locally generated CMAT aggregate research outputs and figures"
Assert-Git "Committing outputs"
git push origin $branch
Assert-Git "Pushing outputs"
Write-Host "Published available aggregate research results to origin/$branch."
