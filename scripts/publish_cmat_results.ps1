# CMAT result publication: safe transfer from an older checkout to a clean research checkout.
# Run INSIDE a clean clone of research/paper21-shapley-predictive-importance.
# This script never deletes or resets the source checkout, never stages raw Excel
# institutional files, and requires a final human review before pushing.
[CmdletBinding()]
param(
    [Parameter(Mandatory=$true)][string]$Source,
    [string]$Materias = "",
    [string]$Asesorias = "",
    [switch]$IncludeHistoricalFigures,
    [switch]$Publish
)

Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

function Assert-Exit([string]$Operation) {
    if ($LASTEXITCODE -ne 0) {
        throw "$Operation failed with exit code $LASTEXITCODE. Nothing was pushed."
    }
}

$repo = (Resolve-Path (Join-Path $PSScriptRoot "..")).Path
$sourceRoot = (Resolve-Path -LiteralPath $Source).Path
$branch = "research/paper21-shapley-predictive-importance"
Set-Location -LiteralPath $repo

if ((git branch --show-current).Trim() -ne $branch) {
    throw "Run this only in a separate clean clone checked out on $branch."
}
Assert-Exit "Branch lookup"
$statusBefore = @(git status --porcelain)
Assert-Exit "Working tree check"
# A previous interrupted run can leave approved aggregate output directories.
# Reuse only those known locations; refuse any unrelated edits or additions.
foreach ($line in $statusBefore) {
    if ($line.Length -lt 4) {
        throw "Unrecognized git status entry: $line"
    }
    $change = $line.Substring(0, 2)
    $pathFromStatus = $line.Substring(3).Replace("\", "/")
    $isHistorical = ($IncludeHistoricalFigures -and $change -eq " M" -and
        $pathFromStatus -match '^brainstorm/shared/historical_outputs/study/figures/\d\d_.*\.png$')
    $isOutput = ($change -in @("??", " M", "M ")) -and (
        $pathFromStatus -match '^results/paper21/tables/followup_questions(/|$)' -or
        $pathFromStatus -match '^results/paper21/tables/attendance_curves(/|$)' -or
        $pathFromStatus -match '^results/paper21/figures/attendance_curves(/|$)' -or
        $pathFromStatus -in @(
            "notes/22_FOLLOWUP_QUESTIONS_RESULTS.md",
            "notes/24_ATTENDANCE_CURVE_RESULTS.md"
        )
    )
    if (-not ($isHistorical -or $isOutput)) {
        throw "Unexpected destination change: $line. Only known aggregate outputs may be reused."
    }
}
Write-Host "Preflight passed. Permitted outputs will be checked and regenerated."
if ($sourceRoot -eq $repo) {
    throw "The source and destination must be separate directories."
}

# Make the public research artifacts complete without copying row-level records.
$localArtifacts = @(
    "notes/22_FOLLOWUP_QUESTIONS_RESULTS.md",
    "results/paper21/tables/followup_questions/degree_professor_period_overlap.csv",
    "results/paper21/tables/followup_questions/two_part_attendance_z_pass.csv",
    "results/paper21/tables/followup_questions/observed_numeric_grade_quantiles.csv",
    "results/paper21/tables/followup_questions/numeric_vs_administrative_composition.csv"
)

Write-Host "Copying known aggregate-only outputs from the previous checkout..."
$copied = @()
foreach ($relative in $localArtifacts) {
    $src = Join-Path $sourceRoot $relative
    if (-not (Test-Path -LiteralPath $src -PathType Leaf)) {
        Write-Warning "Optional local result not found: $relative"
        continue
    }
    $dst = Join-Path $repo $relative
    $parent = Split-Path -Parent $dst
    New-Item -ItemType Directory -Force -Path $parent | Out-Null
    Copy-Item -LiteralPath $src -Destination $dst -Force
    $copied += $relative
}

# These 16 historical PNGs are already a versioned research asset family.
# Stage local replacements through a properly configured Git LFS clean filter
# rather than trying to merge them inside the problematic original checkout.
$historicRelative = "brainstorm/shared/historical_outputs/study/figures"
if ($IncludeHistoricalFigures) {
    git lfs install
    Assert-Exit "Git LFS setup"
    $histSource = Join-Path $sourceRoot $historicRelative
    $histTarget = Join-Path $repo $historicRelative
    if (-not (Test-Path -LiteralPath $histSource -PathType Container)) {
        throw "Historical figure directory was not found: $histSource"
    }
    New-Item -ItemType Directory -Force -Path $histTarget | Out-Null
    $figures = @(Get-ChildItem -LiteralPath $histSource -File -Filter "*.png" |
        Where-Object { $_.Name -match "^\d\d_.*\.png$" })
    if ($figures.Count -ne 16) {
        throw "Expected 16 numbered historical PNGs; found $($figures.Count). Verify the directory."
    }
    foreach ($fig in $figures) {
        # An LFS text pointer masquerading as a PNG must not be re-uploaded.
        $stream = [System.IO.File]::OpenRead($fig.FullName)
        try {
            $signature = [byte[]]::new(8)
            if ($stream.Read($signature, 0, 8) -ne 8 -or
                [System.BitConverter]::ToString($signature) -ne "89-50-4E-47-0D-0A-1A-0A") {
                throw "Not a PNG binary: $($fig.FullName). No push performed."
            }
        } finally {
            $stream.Dispose()
        }
        Copy-Item -LiteralPath $fig.FullName -Destination (Join-Path $histTarget $fig.Name) -Force
    }
    Write-Host "Copied 16 historical PNGs. Git LFS will manage these when staged."
}

# Use the SAME fallbacks as get_study_config(), relative to the ORIGINAL
# checkout where the authorized data were used previously. Never copy inputs.
function Resolve-ControlledInput([string]$Explicit, [string[]]$RelativeOptions, [string]$Label) {
    if ($Explicit) {
        if (-not (Test-Path -LiteralPath $Explicit -PathType Leaf)) {
            throw "$Label input does not exist at explicit path: $Explicit"
        }
        return (Resolve-Path -LiteralPath $Explicit).Path
    }
    foreach ($relative in $RelativeOptions) {
        $path = Join-Path $sourceRoot $relative
        if (Test-Path -LiteralPath $path -PathType Leaf) {
            return (Resolve-Path -LiteralPath $path).Path
        }
    }
    throw "$Label input not found at the repo-configured paths in $sourceRoot. Use -Materias and -Asesorias with explicit authorized local paths."
}
$Materias = Resolve-ControlledInput $Materias @(
    "data/raw/Materias estudiantes-profesores 2019-2025 P y O.xlsx",
    "data/raw/Materias.xlsx",
    "data/controlled/Materias_pseudonymized.csv",
    "data/Materias estudiantes-profesores 2019-2025 P y O.xlsx",
    "data/Materias_anonymized.csv"
) "Academic"
$Asesorias = Resolve-ControlledInput $Asesorias @(
    "data/raw/Asesorias2024.xlsx",
    "data/raw/Asesorias.xlsx",
    "data/controlled/Asesorias_pseudonymized.csv",
    "data/Asesorias2024.xlsx",
    "data/Asesorias_anonymized.csv"
) "CMAT"
Write-Host "Authorized inputs located in original checkout; source files will not be staged."

Write-Host "Installing the local reproducible analysis package..."
python -m pip install -e "./cmat_analysis[dev]"
Assert-Exit "Editable package installation"

Write-Host "Running synthetic follow-up and curve tests..."
python -m pytest -q "cmat_analysis/tests/test_paper21_followup_questions.py" "cmat_analysis/tests/test_paper21_attendance_curves.py"
Assert-Exit "Synthetic tests"

python "code/run_paper21_followup_questions.py" --check
Assert-Exit "Follow-up configuration check"
python "code/run_paper21_attendance_curves.py" --check
Assert-Exit "Curve configuration check"

# Rerunning the follow-up guarantees results correspond to the code in the
# destination rather than importing an incompatible local draft.
Write-Host "Regenerating follow-up aggregate results..."
python "code/run_paper21_followup_questions.py" --materias "$Materias" --asesorias "$Asesorias"
Assert-Exit "Follow-up institutional run"
Write-Host "Generating attendance-curve aggregate tables and four figures..."
python "code/run_paper21_attendance_curves.py" --materias "$Materias" --asesorias "$Asesorias"
Assert-Exit "Curve institutional run"

$pathsToStage = @(
    "notes/22_FOLLOWUP_QUESTIONS_RESULTS.md",
    "notes/24_ATTENDANCE_CURVE_RESULTS.md",
    "results/paper21/tables/followup_questions",
    "results/paper21/tables/attendance_curves",
    "results/paper21/figures/attendance_curves"
)
if ($IncludeHistoricalFigures) { $pathsToStage += $historicRelative }

Write-Host "Staging ONLY vetted research-output paths..."
git add -- $pathsToStage
Assert-Exit "Staging aggregates"

$expectedPaths = @($pathsToStage)
$staged = @(git diff --cached --name-only)
Assert-Exit "Staged path review"
foreach ($file in $staged) {
    $normalized = $file.Replace("\", "/")
    $allowed = $false
    foreach ($path in $expectedPaths) {
        $part = $path.TrimEnd("/")
        if ($normalized -eq $part -or $normalized.StartsWith("$part/")) {
            $allowed = $true
            break
        }
    }
    if (-not $allowed) {
        throw "UNEXPECTED STAGED PATH: $file. No commit or push occurred."
    }
    if ($normalized -match "(?i)\.(xlsx|xls|parquet|feather|dta|sav|sas7bdat|key|pem)$") {
        throw "Protected file extension detected: $file. Nothing was pushed."
    }
}
git diff --cached --stat
Assert-Exit "Staged statistics"
git diff --cached --name-only
Assert-Exit "Staged listing"

if ($IncludeHistoricalFigures) {
    Write-Host "Git LFS file status:"
    git lfs status
    Assert-Exit "LFS status"
}
if (-not $staged.Count) {
    Write-Host "No new files: everything staged already matches the remote content."
    exit 0
}
if (-not $Publish) {
    Write-Host ""
    Write-Host "Files are staged, but have NOT been committed or pushed."
    Write-Host "Review the staged files, then commit/push only these vetted paths."
    Write-Host "If you want the interactive publishing confirmation, pass -Publish on the first run."
    exit 0
}

Write-Host ""
Write-Warning "You are about to publish these results in a PUBLIC GitHub repository."
$answer = Read-Host "Type PUBLISH after reviewing the staged files and their disclosure safety"
if ($answer -cne "PUBLISH") {
    throw "Publication not confirmed. Changes remain staged locally."
}
git commit -m "Publish validated CMAT follow-up and attendance-curve outputs"
Assert-Exit "Commit"
git push origin $branch
Assert-Exit "Push"
Write-Host "Research results published to origin/$branch."
