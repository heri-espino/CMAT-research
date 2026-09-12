$ErrorActionPreference = "Stop"

$Root = (git rev-parse --show-toplevel).Trim()
Set-Location $Root

$StartBranch = (git branch --show-current).Trim()
$OutputDir = Join-Path (Split-Path $Root -Parent) "CMAT-compiled-papers"

$Branches = @(
    "paper/paper1-ppa-persistence",
    "paper/paper2-mu-performance",
    "paper/paper3-grading-heterogeneity"
)

$Names = @(
    "paper1-ppa-persistence",
    "paper2-mu-performance",
    "paper3-grading-heterogeneity"
)

# Refuse to start if there are local changes.
$Status = git status --porcelain
if ($Status) {
    Write-Host "ERROR: working tree is not clean." -ForegroundColor Red
    Write-Host ""
    git status --short
    Write-Host ""
    Write-Host "Commit/stash the changes, or discard them with:"
    Write-Host "  git reset --hard HEAD"
    Write-Host "  git clean -fd"
    exit 1
}

# Check Python version.
Write-Host "Python:"
python --version

python -c @"
import sys
if sys.version_info[:2] != (3, 14):
    raise SystemExit(
        f"ERROR: Python 3.14 is required; current version is {sys.version.split()[0]}"
    )
"@

if ($LASTEXITCODE -ne 0) {
    exit $LASTEXITCODE
}

# Check LaTeX.
$LatexMk = Get-Command latexmk -ErrorAction SilentlyContinue
$PdfLatex = Get-Command pdflatex -ErrorAction SilentlyContinue
$Bibtex = Get-Command bibtex -ErrorAction SilentlyContinue

if ($LatexMk) {
    Write-Host "LaTeX: $($LatexMk.Source)"
}
elseif ($PdfLatex -and $Bibtex) {
    Write-Host "LaTeX: pdflatex + bibtex"
}
else {
    Write-Host "ERROR: LaTeX is not installed or not available in PATH." -ForegroundColor Red
    exit 1
}

New-Item -ItemType Directory -Force -Path $OutputDir | Out-Null

try {
    git fetch origin --tags
    if ($LASTEXITCODE -ne 0) {
        throw "git fetch failed"
    }

    for ($i = 0; $i -lt $Branches.Count; $i++) {
        $Branch = $Branches[$i]
        $Name = $Names[$i]

        Write-Host ""
        Write-Host "============================================================"
        Write-Host "Compiling $Name"
        Write-Host "Branch: $Branch"
        Write-Host "============================================================"

        git switch $Branch
        if ($LASTEXITCODE -ne 0) {
            throw "Could not switch to $Branch"
        }

        # Match the remote branch exactly.
        git reset --hard "origin/$Branch"
        if ($LASTEXITCODE -ne 0) {
            throw "Could not reset $Branch"
        }

        git lfs pull
        if ($LASTEXITCODE -ne 0) {
            throw "git lfs pull failed on $Branch"
        }

        # Install the current branch version of cmat_analysis.
        python -m pip install -e "./cmat_analysis[dev]"
        if ($LASTEXITCODE -ne 0) {
            throw "cmat_analysis installation failed on $Branch"
        }

        # Compile figures + manuscript.
        python paper/build.py
        if ($LASTEXITCODE -ne 0) {
            throw "Paper compilation failed on $Branch"
        }

        $Pdf = Join-Path $Root "paper/main.pdf"

        if (-not (Test-Path $Pdf)) {
            throw "$Branch did not produce paper/main.pdf"
        }

        $Destination = Join-Path $OutputDir "$Name.pdf"
        Copy-Item $Pdf $Destination -Force

        Write-Host "Saved:"
        Write-Host "  $Destination"
    }

    Write-Host ""
    Write-Host "============================================================"
    Write-Host "All papers compiled successfully"
    Write-Host "============================================================"
    Write-Host ""

    foreach ($Name in $Names) {
        Write-Host "  $(Join-Path $OutputDir "$Name.pdf")"
    }
}
finally {
    Write-Host ""
    Write-Host "Returning to $StartBranch..."
    git switch $StartBranch | Out-Null
}