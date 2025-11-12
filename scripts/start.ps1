param(
    [string]$EnvFile = ".env"
)

$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$projectRoot = Resolve-Path (Join-Path $scriptDir "..")
Set-Location $projectRoot

if (Test-Path $EnvFile) {
    Write-Host "Loading environment variables from $EnvFile"
    Get-Content $EnvFile | ForEach-Object {
        if (-not [string]::IsNullOrWhiteSpace($_) -and $_ -notmatch '^#') {
            $pair = $_ -split '=', 2
            if ($pair.Length -eq 2) {
                $name = $pair[0].Trim()
                $value = $pair[1].Trim()
                if ($name) {
                    Write-Host "  set" $name
                    $env:$name = $value
                }
            }
        }
    }
}

if (-not (Test-Path ".venv")) {
    Write-Host "Creating uv virtual environment..."
    uv venv
}

Write-Host "Installing project dependencies..."
uv pip install -e .

Write-Host "Starting MCP translation server..."
uv run python server.py
