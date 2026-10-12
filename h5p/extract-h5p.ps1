# Extracts every Lumi export in h5p/source/*.h5p to h5p/content/<name>/,
# which is what the h5p-standalone player reads. Re-run after each Lumi edit.
#
# Usage (from the repo root or anywhere):
#   powershell -ExecutionPolicy Bypass -File h5p\extract-h5p.ps1            # all files
#   powershell -ExecutionPolicy Bypass -File h5p\extract-h5p.ps1 circular-flow   # one file
#
# File names become the shortcode name: "Circular Flow.h5p" -> {{< h5p circular-flow >}}

param([string]$Name)

$root    = $PSScriptRoot
$source  = Join-Path $root 'source'
$content = Join-Path $root 'content'
New-Item -ItemType Directory -Force $content | Out-Null

$files = Get-ChildItem $source -Filter '*.h5p'
if ($Name) { $files = $files | Where-Object { $_.BaseName -eq $Name } }
if (-not $files) { Write-Warning "No .h5p files found in $source"; exit 1 }

foreach ($f in $files) {
    $id = ($f.BaseName.ToLower() -replace '\s+', '-') -replace '[^a-z0-9_-]', ''
    $dest = Join-Path $content $id
    if (Test-Path $dest) { Remove-Item $dest -Recurse -Force }
    New-Item -ItemType Directory $dest | Out-Null
    # tar (bsdtar, built into Windows 10+) reads zip archives whatever the extension
    tar -xf $f.FullName -C $dest
    if (-not (Test-Path (Join-Path $dest 'h5p.json'))) {
        Write-Warning "$($f.Name): no h5p.json after extraction, is this a valid .h5p file?"
        continue
    }
    Write-Host "$($f.Name) -> content/$id   use: {{< h5p $id >}}"
}
