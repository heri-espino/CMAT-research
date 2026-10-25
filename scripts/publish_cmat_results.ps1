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
# Some older Git history holds full PNG bytes even though .gitattributes
# now marks that path as LFS. Git can report exactly those 16 as modified
# immediately after a fresh clone. Permit ONLY that known mismatch when the
# caller explicitly asks to reimport the historical figures through Git LFS.
foreach ($line in $statusBefore) {
    $pathFromStatus = $line.Substring(3).Replace("\\", "/")
    $isHistorical = ($line.Substring(0, 2) -eq " M" -and
        $pathFromStatus -match '^brainstorm/shared/historical_outputs/study/figures/\\d\\d_.*\\.png
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
        Where-Object { $_.Name -match "^\\d\\d_.*\\.png$" })
    if ($figures.Count -ne 16) {
        throw "Expected 16 numbered historical PNGs; found $($figures.Count). Verify the directory."
    }
    foreach ($fig in $figures) {
        # Prevent accidentally uploading an LFS pointer text file as PNG bytes.
        $stream = [System.IO.File]::OpenRead($fig.FullName)
        try {
            $signature = [byte[]]::new(8)
            if ($stream.Read($signature, 0, 8) -ne 8 -or
                [Convert]::ToHexString($signature) -ne "89504E470D0A1A0A") {
                throw "Not a real PNG image: $($fig.FullName). Do not publish LFS pointer text."
            }
        } finally {
            $stream.Dispose()
        }
        Copy-Item -LiteralPath $fig.FullName -Destination (Join-Path $histTarget $fig.Name) -Force
    }
    Write-Host "Copied 16 historical PNGs. Git LFS will manage these when staged."
}

# Never place controlled spreadsheets in the new public checkout.
if (-not $Materias) {
    $Materias = Join-Path $sourceRoot "data/raw/Materias estudiantes-profesores 2019-2025 P y O.xlsx"
}
if (-not $Asesorias) {
    $Asesorias = Join-Path $sourceRoot "data/raw/Asesorias2024.xlsx"
}
if (-not (Test-Path -LiteralPath $Materias -PathType Leaf)) {
    throw "The academic workbook was not found: $Materias. Re-run with -Materias '<correct-path>'."
}
if (-not (Test-Path -LiteralPath $Asesorias -PathType Leaf)) {
    throw "The CMAT workbook was not found: $Asesorias. Re-run with -Asesorias '<correct-path>'."
}

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
    $normalized = $file.Replace("\\", "/")
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
    if ($normalized -match "(?i)\\.(xlsx|xls|parquet|feather|dta|sav|sas7bdat|key|pem)$") {
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
    Write-Host "Review staged files, then commit and push these paths manually."
    Write-Host "Alternatively, use -Publish in the FIRST run to request an interactive review."
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
)
    if (-not ($IncludeHistoricalFigures -and $isHistorical)) {
        throw "Unexpected local change in destination: $line. Use a separate clean checkout."
    }
}
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
        Where-Object { $_.Name -match "^\\d\\d_.*\\.png$" })
    if ($figures.Count -ne 16) {
        throw "Expected 16 numbered historical PNGs; found $($figures.Count). Verify the directory."
    }
    foreach ($fig in $figures) {
        Copy-Item -LiteralPath $fig.FullName -Destination (Join-Path $histTarget $fig.Name) -Force
    }
    Write-Host "Copied 16 historical PNGs. Git LFS will manage these when staged."
}

# Never place controlled spreadsheets in the new public checkout.
if (-not $Materias) {
    $Materias = Join-Path $sourceRoot "data/raw/Materias estudiantes-profesores 2019-2025 P y O.xlsx"
}
if (-not $Asesorias) {
    $Asesorias = Join-Path $sourceRoot "data/raw/Asesorias2024.xlsx"
}
if (-not (Test-Path -LiteralPath $Materias -PathType Leaf)) {
    throw "The academic workbook was not found: $Materias. Re-run with -Materias '<correct-path>'."
}
if (-not (Test-Path -LiteralPath $Asesorias -PathType Leaf)) {
    throw "The CMAT workbook was not found: $Asesorias. Re-run with -Asesorias '<correct-path>'."
}

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
    $normalized = $file.Replace("\\", "/")
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
    if ($normalized -match "(?i)\\.(xlsx|xls|parquet|feather|dta|sav|sas7bdat|key|pem)$") {
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
    Write-Host "Review the files, then use -Publish (on a clean checkout, reruns analyses),"
    Write-Host "or commit and push only these reviewed paths manually."
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
